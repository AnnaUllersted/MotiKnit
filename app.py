from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(filepath)
        
        try:
            # Process the image
            with Image.open(filepath) as image:
                extracted_text = "testing testing"
            
            # Close any remaining file handles explicitly
            try:
                image.close()
            except:
                pass
            
            # Add a small delay to ensure all handles are released
            import time
            time.sleep(0.1)
            
            # Try to remove the file
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {filepath}: {str(e)}")
                # Continue execution even if we couldn't remove the file
                
            return jsonify({
                'message': 'File successfully uploaded and processed',
                'extracted_text': extracted_text
            })
            
        except Exception as e:
            # If any error occurs during processing, attempt to clean up
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    app.run(host=host, port=port, debug=True)
