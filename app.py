from flask import Flask, request, render_template, jsonify, make_response, Blueprint
import os
import base64
from pdf_generator import create_pattern_pdf
from PIL import Image
import logging
from knitting_patter_generator import KnittingPatternGenerator
from pattern_visualizer import KnittingPatternVisualizer
import sys
from dotenv import load_dotenv
from translator import translate

load_dotenv()
ENVIRONMENT = os.environ.get('FLASK_ENV', 'production')
print(ENVIRONMENT)
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

@app.route('/')
def home():
    language = get_language_from_domain()
    return render_template('index.html', lang=language)

@app.route('/process', methods=['POST'])
def process():
    color1 = "white"
    color2 = "black"
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
            image = Image.open(file)

            pattern_generator = KnittingPatternGenerator(
                image,
                desired_height_cm,
                pinde,
                masker,
                bottom_to_top,
                alternating_iteration)
            
            bw_image = pattern_generator.process_to_bw_pixels(intensity)
            instructions = pattern_generator.generate_knitting_instructions(bw_image, color1, color2, language)

            pattern_visualizer = KnittingPatternVisualizer(
                pattern_generator.width_px, 
                pattern_generator.height_px)
            # Generate illustration
            pattern_image = pattern_visualizer.generate_illustration(bw_image, language)
            img_str = base64.b64encode(pattern_image).decode()

            size_str = translate('final_size', language, size=desired_height_cm)
            gauge_str = translate('knit_gauge', language, pinde=pinde, masker=masker)
            pattern_size_str = translate('pattern_size', language, final_width=pattern_generator.width_px, final_height=pattern_generator.height_px)
            response =  jsonify({
                'message': 'Pattern generated successfully',
                'processed_image': img_str,
                'instructions': instructions,
                'parameters': {
                    'size': desired_height_cm,
                    'pinde': pinde,
                    'masker': masker,
                    'final_width':pattern_generator.width_px,
                    'final_height': pattern_generator.height_px,
                    'final_size': size_str,
                    'final_gauge': gauge_str,
                    'final_pattern_size': pattern_size_str
                }
            })
            return response
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
    app.logger.setLevel(logging.DEBUG)