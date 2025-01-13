from flask import Flask, request, render_template, jsonify, make_response
import os
import base64
from io import BytesIO
import numpy as np
from pdf_generator import create_pattern_pdf
from PIL import Image, ImageDraw, ImageFont
import logging
import sys

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_language_from_domain():
    host = request.host
    return 'da' if 'motiknit.dk' in host else 'en'

# Translations
i18n = {
    'en': {
        'no_file': 'No file part',
        'no_selection': 'No selected file',
        'invalid_values': 'Invalid numeric values',
        'file_not_allowed': 'File type not allowed',
        'pattern_generated': 'Pattern generated successfully',
        'row_instructions': 'Row {row}: {details}',
        'ret_pind': 'Row {row} is a knit row',
        'vrang_pind': 'Row {row} is a purl row',
        'masker_details': '{count} {color} stitches',
        'error_message': 'An error occurred: {error}',
        'pinde_index': 'Row {index}'
    },
    'da': {
        'no_file': 'Ingen fil fundet',
        'no_selection': 'Ingen fil valgt',
        'invalid_values': 'Ugyldige numeriske værdier',
        'file_not_allowed': 'Filtype ikke tilladt',
        'pattern_generated': 'Mønster genereret med succes',
        'row_instructions': 'Pind {row}: {details}',
        'ret_pind': 'Pind {row} er en retpind',
        'vrang_pind': 'Pind {row} er en vrangpind',
        'masker_details': '{count} {color} masker',
        'error_message': 'Der opstod en fejl: {error}',
        'pinde_index': 'Pind {index}'
    }
}

def translate(key, lang, **kwargs):
    return i18n[lang][key].format(**kwargs)

def calculate_pixels(desired_height_cm, image, pinde, masker):
    """Calculate the number of pixels needed based on the desired size and knitting gauge"""
    # Get the original dimensions
    original_width, original_height = image.size
    # Calculate aspect ratio
    aspect_ratio = original_width / original_height
    # Calculate pixels needed for desired size
    desired_width_cm = desired_height_cm * aspect_ratio
    target_width_px = int((masker * desired_width_cm) / 10)
    target_height_px = int((pinde * desired_height_cm) / 10)
    return target_width_px, target_height_px

def process_to_bw_pixels(image, target_width_px, target_height_px, intensity):
    """Convert image to black and white pixels of specified size"""

    # remap the intensity variable
    intensity_remap = intensity * 255/100

    # Resize image
    resized = image.resize((target_width_px, target_height_px), Image.Resampling.LANCZOS)

    # Convert to grayscale
    grayscale: Image = resized.convert('L')

    # Convert to pure black and white (threshold at 128)
    bw_image = grayscale.point(lambda x: 0 if x < intensity_remap else 255, '1')

    return bw_image

def generate_row_instructions(row_data, ret_pind, row_number, lang):
    current_color = row_data[0]  # Start with the first pixel's color
    count = 1
    row_instructions = []
    row_key = 'ret_pind' if ret_pind else 'vrang_pind'
    row_instructions.append(translate(row_key, lang, row=row_number + 1))
    # Process each pixel in the row
    for col in range(1, len(row_data)):
        if row_data[col] == current_color:
            count += 1
        else:
            color = 'hvide' if current_color == 1 else 'sorte'
            row_instructions.append(translate('masker_details', lang, count=count, color=color))
            current_color = row_data[col]
            count = 1
    color = 'hvide' if current_color == 1 else 'sorte'
    row_instructions.append(translate('masker_details', lang, count=count, color=color))
    return row_instructions

def generate_knitting_instructions(bw_image, bottom_to_top, alternating_iteration, lang):
    """Generate knitting instructions reading from bottom up, left to right"""
    width, height = bw_image.size
    pixels = np.array(bw_image)
    instructions = []

    if bottom_to_top:
        for i,row in enumerate(reversed(pixels)):
            right_to_left = True
            if alternating_iteration: 
                right_to_left = i % 2 == 0
                if right_to_left: #even row number
                    row_data = row[::-1] #reversed array
                else: 
                    row_data = row
            else: #start lower right corner
                row_data = row[::-1] #reversed array
            instructions.append(generate_row_instructions(row_data,right_to_left, i, lang))
    else: #top to bottom
        for i,row in enumerate(pixels):
            left_to_right = True
            if alternating_iteration:
                left_to_right = i % 2 == 0
                if left_to_right: #even row number
                    row_data = row
                else: 
                    row_data = row[::-1] #reversed array
            else: #start upper left corner
                row_data = row
            row_instructions = generate_row_instructions(row_data, left_to_right, i, lang)
            instructions.append(row_instructions)
    return instructions

def generate_illustration(target_width_px, target_height_px, bw_image, lang):
    """Generate knitting illustration with grey area and row numbers """
    # Save processed image to base64 for display
    img_buffer = BytesIO()

    pixel_size = 20  # Justér for tykkelse af grå kant

    # resize image so it fits a boundary
    width_w_boundary = target_width_px*pixel_size
    height_w_boundary = target_height_px*pixel_size

    logger.info("creating canvas with background and boarder")
    # Opret et nyt billede med ekstra plads til tekst og grå kanter
    text_space_width = 60  # Bredden på pladsen til teksten
    canvas = Image.new('RGB', (width_w_boundary + text_space_width, height_w_boundary), (120, 120, 120))  # Grå baggrund

    logger.info("draw new image based on old")
    # Tegn det originale billede på det nye lærred med grå kanter
    for y in range(target_height_px):
        for x in range(target_width_px):
            pixel_color = bw_image.getpixel((x, y))  # 0 eller 255
            color = (0, 0, 0) if pixel_color == 0 else (255, 255, 255)  # Sort eller hvid
            pixel_x = text_space_width + x * pixel_size
            pixel_y = y * pixel_size
            # Fyld midten af det grå område med den originale pixels farve
            for i in range(1, pixel_size - 1):  # Undgå de yderste pixels (grå kant)
                for j in range(1, pixel_size - 1):
                    canvas.putpixel((pixel_x + i, pixel_y + j), color)

    logger.info("writing text on image")
    # Tilføj tekst ud for hver række
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("arial.ttf", size=14)  # Brug en passende skrifttype og størrelse
    for y in range(target_height_px):
        text = translate('pinde_index', lang, index=y+1)
        text_position = (10, y * pixel_size + pixel_size // 4)  # Placer teksten midt på pixel-rækken
        draw.text(text_position, text, font=font, fill=(0, 0, 0))  # Hvid tekst

    bw_image_for_display = canvas
    logger.info("resizing image")
    bw_image_for_display = bw_image_for_display.resize((target_width_px*pixel_size+text_space_width, target_height_px*pixel_size), Image.Resampling.NEAREST)  # Scale up for better visibility
    bw_image_for_display.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    return img_str

@app.route('/')
def home():
    language = get_language_from_domain()
    return render_template('index.html', lang=language)

@app.route('/process', methods=['POST'])
def process():
    language = get_language_from_domain()
    logging.info("Processing request")
    if 'file' not in request.files:
        return jsonify({'error': translate('no_file', language)}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': translate('no_selection', language)}), 400
    
    # Get parameters from form data
    try:
        desired_height_cm = float(request.form.get('size', 15))  # Default 15cm
        pinde = float(request.form.get('pinde', 24))        # Default 24 stitches/10cm
        masker = float(request.form.get('masker', 18))      # Default 18 rows/10cm
        alternating_iteration = bool(request.form.get('alternating_iteration', False, type=is_it_true))  # Default er at der strikkes rundt på rundpind
        bottom_to_top = bool(request.form.get('bottom_to_top', False, type=is_it_true))  # Default er at der startes fra toppen
        intensity = float(request.form.get('intensity', 50)) # default er 50% på intensiteten af motivets farve
    except ValueError:
        return jsonify({'error': translate('invalid_values', language)}), 400
    
    if file and allowed_file(file.filename):
        try:    
        # Open the image
            logger.info("opening file")
            image = Image.open(file)
            
            # Calculate required pixels
            logger.info("calculating pixels")
            target_width_px, target_height_px = calculate_pixels(desired_height_cm, image, pinde, masker)

            # Process image to black and white pixels
            logger.info("processing to black and white")
            bw_image = process_to_bw_pixels(image, target_width_px, target_height_px, intensity)

            # Generate knitting instructions
            logger.info("generating knitting instructions")
            instructions = generate_knitting_instructions(bw_image,bottom_to_top,alternating_iteration,language)

            # Generate illustration
            img_str = generate_illustration(target_width_px, target_height_px, bw_image, language)

            return jsonify({
                'message': 'Pattern generated successfully',
                'processed_image': img_str,
                'instructions': instructions,
                'parameters': {
                    'size': desired_height_cm,
                    'pinde': pinde,
                    'masker': masker,
                    'final_width': target_width_px,
                    'final_height': target_height_px
                }
            })
        except Exception as e:
            logger.error(str(e))
            return jsonify({'error': translate('error_message', language, error=str(e))}), 500
            
    return jsonify({'error': translate('file_not_allowed', language)}), 400

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    language = get_language_from_domain()
    try:
        data = request.json
        pdf_buffer = create_pattern_pdf(
            data['processed_image'],
            data['parameters'],
            data['instructions']
        )
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=knitting_pattern.pdf'
        return response
    except Exception as e:
        return jsonify({'error': translate('error_message', language, error=str(e))}), 500

def is_it_true(value):
  return value.lower() == 'true'

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logger.info('Started')
    app.run(host=host, port=port, debug=False)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)