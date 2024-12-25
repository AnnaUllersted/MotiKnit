from flask import Flask, request, render_template, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO


app = Flask(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_and_text(image, pinde, masker):
    # Convert to greyscale
    greyscale_image = image.convert('L')
    
    # Extract text
    extracted_text = "testing testing"
    
    # Log the received parameters (you can modify the processing based on these values)
    print(f"Processing with pinde: {pinde}, masker: {masker}")
    
    # Convert processed image to base64
    img_buffer = BytesIO()
    greyscale_image.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    return img_str, extracted_text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Get pinde and masker values from form data
    try:
        pinde = float(request.form.get('pinde', 0))
        masker = float(request.form.get('masker', 0))
    except ValueError:
        return jsonify({'error': 'Invalid numeric values for pinde or masker'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Open and process the image
            image = Image.open(file)
            
            # Process image and get text
            processed_image_b64, extracted_text = process_image_and_text(image, pinde, masker)
            
            return jsonify({
                'message': 'File processed successfully',
                'processed_image': processed_image_b64,
                'extracted_text': extracted_text,
                'parameters': {
                    'pinde': pinde,
                    'masker': masker
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    app.run(host=host, port=port, debug=True)
