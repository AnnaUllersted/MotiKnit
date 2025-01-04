from flask import Flask, request, render_template, jsonify, send_file
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


def calculate_pixels(desired_size_cm, pinde, masker):
    """Calculate the number of pixels needed based on the desired size and knitting gauge"""
    # Calculate pixels needed for desired size
    # If 'pinde' stitches x 'masker' rows = 10cm x 10cm
    # Then for desired_size we need:
    pixels_width = int((masker * desired_size_cm) / 10)
    pixels_height = int((pinde * desired_size_cm) / 10)
    return pixels_width, pixels_height

def process_to_bw_pixels(image, width, height):
    """Convert image to black and white pixels of specified size"""
    # Resize image
    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    # Convert to grayscale
    grayscale: Image = resized.convert('L')
    # Convert to pure black and white (threshold at 128)
    bw_image = grayscale.point(lambda x: 0 if x < 130 else 255, '1')

    return bw_image

def generate_row_instructions(row_data, ret_pind, row_number):
    current_color = row_data[0]  # Start with the first pixel's color
    count = 1
    row_instructions = []
    if ret_pind:
        row_instructions.append(f"Pind {row_number +1} er en retpind")
    else:
        row_instructions.append(f"Pind {row_number +1} er en vrangpind")
    # Process each pixel in the row
    for col in range(1, len(row_data)):
        if row_data[col] == current_color:
            count += 1
        else:
            row_instructions.append(f" {count} {'hvide masker' if current_color == 1 else 'sorte masker'}")
            current_color = row_data[col]
            count = 1
    row_instructions.append(f" {count} {'hvide masker' if current_color == 1 else 'sorte masker'}")
    return row_instructions

def generate_knitting_instructions(bw_image, bottom_to_top, alternating_iteration):
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
            instructions.append(generate_row_instructions(row_data,right_to_left, i))
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
            row_instructions = generate_row_instructions(row_data, left_to_right, i)
            instructions.append(row_instructions)
    return instructions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    logging.info("Processing request")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Get parameters from form data
    try:
        desired_size = float(request.form.get('size', 10))  # Default 10cm
        pinde = float(request.form.get('pinde', 37))        # Default 37 stitches/10cm
        masker = float(request.form.get('masker', 19))      # Default 19 rows/10cm
        alternating_iteration = bool(request.form.get('alternating_iteration', False, type=is_it_true))  # Default er at der strikkes rundt på rundpind
        bottom_to_top = bool(request.form.get('bottom_to_top', False, type=is_it_true))  # Default er at der startes fra toppen
    except ValueError:
        return jsonify({'error': 'Invalid numeric values'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Open the image
            logger.info("opening file")
            image = Image.open(file)
            
            # Calculate required pixels
            logger.info("calculating pixels")
            width, height = calculate_pixels(desired_size, pinde, masker)
            
            # Process image to black and white pixels
            logger.info("processing to black and white")
            bw_image = process_to_bw_pixels(image, width, height)
            # Generate knitting instructions
            logger.info("generating knitting instructions")
            instructions = generate_knitting_instructions(bw_image,bottom_to_top,alternating_iteration)

            # Save processed image to base64 for display
            img_buffer = BytesIO()

            pixel_size = 20  # Justér for tykkelse af grå kant

            # resize image so it fits a boundary
            width_w_boundary = width*pixel_size
            height_w_boundary = height*pixel_size

            logger.info("creating canvas with background and boarder")
            # Opret et nyt billede med ekstra plads til tekst og grå kanter
            text_space_width = 60  # Bredden på pladsen til teksten
            canvas = Image.new('RGB', (width_w_boundary + text_space_width, height_w_boundary), (120, 120, 120))  # Grå baggrund

            logger.info("draw new image based on old")
            print("canvas class", canvas.__class__)

            print("bw_image class", bw_image.__class__)
            # Tegn det originale billede på det nye lærred med grå kanter
            try:

                for y in range(height):
                    for x in range(width):
                        pixel_color = bw_image.getpixel((x, y))  # 0 eller 255
                        color = (0, 0, 0) if pixel_color == 0 else (255, 255, 255)  # Sort eller hvid
                        pixel_x = text_space_width + x * pixel_size
                        pixel_y = y * pixel_size
                        # Fyld midten af det grå område med den originale pixels farve
                        for i in range(1, pixel_size - 1):  # Undgå de yderste pixels (grå kant)
                            for j in range(1, pixel_size - 1):
                                canvas.putpixel((pixel_x + i, pixel_y + j), color)
            except:
                print("height",height)
                print("width",width)
                print(bw_image)
                print("pixel_size",pixel_size)
                print(canvas)
                logger.info("caught expection in creating new image")

            logger.info("writing text")
            # Tilføj tekst ud for hver række
            draw = ImageDraw.Draw(canvas)
            logger.info("using font")
            font = ImageFont.truetype("arial.ttf", size=14)  # Brug en passende skrifttype og størrelse
            logger.info("writing rows of text")
            for y in range(height):
                text = f"Pind {y + 1}"
                text_position = (10, y * pixel_size + pixel_size // 4)  # Placer teksten midt på pixel-rækken
                draw.text(text_position, text, font=font, fill=(0, 0, 0))  # Hvid tekst

            bw_image_for_display = canvas
            logger.info("resizing image")
            bw_image_for_display = bw_image_for_display.resize((width*pixel_size+text_space_width, height*pixel_size), Image.Resampling.NEAREST)  # Scale up for better visibility
            bw_image_for_display.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.getvalue()).decode()

            return jsonify({
                'message': 'Pattern generated successfully',
                'processed_image': img_str,
                'instructions': instructions,
                'parameters': {
                    'size': desired_size,
                    'pinde': pinde,
                    'masker': masker,
                    'final_width': width,
                    'final_height': height
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        data = request.json
        pdf_buffer = create_pattern_pdf(
            data['processed_image'],
            data['parameters'],
            data['instructions']
        )
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='knitting_pattern.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def is_it_true(value):
  return value.lower() == 'true'

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logger.info('Started')
    app.run(host=host, port=port, debug=False)