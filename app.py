from flask import Flask, request, render_template, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO
import numpy as np

app = Flask(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
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
    bw_image = grayscale.point(lambda x: 0 if x < 210 else 255, '1')
    return bw_image

def generate_knitting_instructions(bw_image,start,method):
    """Generate knitting instructions reading from bottom up, left to right"""
    width, height = bw_image.size
    pixels = np.array(bw_image)
    instructions = []

    if start == 0: # from bottom to top
        if method == 0: # knitting back and forth

            # Process rows from bottom to top
            for row in reversed(range(height)):
                # Reverse the row if it is an even row in the original order

                if row % 2 != 0:  # Check if the row number is odd
                    row_data = pixels[row][::-1]
                else:
                    row_data = pixels[row]   
                current_color = row_data[0]  # Start with the first pixel's color
                count = 1
                row_instructions = []

                # Process each pixel in the row
                for col in range(1, width):
                    if row_data[col] == current_color:
                        count += 1
                    else:
                        row_instructions.append(f"{count} {'white' if current_color == 1 else 'black'}")
                        current_color = row_data[col]
                        count = 1

                # Add the last group
                row_instructions.append(f"{count} {'white' if current_color == 1 else 'black'}")
                instructions.append(", ".join(row_instructions))

        else: # knitting around        

            # Process rows from bottom to top
            for row in reversed(range(height)):
                current_color = pixels[row][-1]  # Start with the last pixel in the row (reversed row)
                count = 1
                row_instructions = []

                # Process each pixel in the reversed row (from right to left)
                for col in range(width - 2, -1, -1):  # Iterate backwards through the row
                    if pixels[row][col] == current_color:
                        count += 1
                    else:
                        row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                        current_color = pixels[row][col]
                        count = 1

                # Add the last group
                row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                instructions.append(", ".join(row_instructions))

    else:         
        # Process rows from top to bottom
        if method == 0: # Knitting back and forth
            # Process rows from top to bottom
            for row in range(height):
                current_color = pixels[row][0]  # Start with first pixel's color
                count = 1
                row_instructions = []
                
                if row % 2 != 0:  # Check if the row number is odd
                    row_data = pixels[row][::-1]
                else:
                    row_data = pixels[row]  

                # Process each pixel in the row
                for col in range(1, width):
                    if row_data[col] == current_color:
                        count += 1
                    else:
                        row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                        current_color = row_data[col]
                        count = 1

                # Add the last group
                row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                instructions.append(", ".join(row_instructions))

        else: # knitting around
            for row in range(height):
                current_color = pixels[row][0]  # Start with first pixel's color
                count = 1
                row_instructions = []
                
                # Process each pixel in the row
                for col in range(1, width):
                    if pixels[row][col] == current_color:
                        count += 1
                    else:
                        row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                        current_color = pixels[row][col]
                        count = 1

                # Add the last group
                row_instructions.append(f"{count} {'white' if current_color else 'black'}")
                instructions.append(", ".join(row_instructions))
    return instructions

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
    
    # Get parameters from form data
    try:
        desired_size = float(request.form.get('size', 10))  # Default 10cm
        pinde = float(request.form.get('pinde', 37))        # Default 37 stitches/10cm
        masker = float(request.form.get('masker', 19))      # Default 19 rows/10cm
        method = float(request.form.get('method', 1))      # Default er at der strikkes rundt på rundpind
        start = float(request.form.get('start', 1))      # Default er at der startes fra toppen
    except ValueError:
        return jsonify({'error': 'Invalid numeric values'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Open the image
            image = Image.open(file)
            
            # Calculate required pixels
            width, height = calculate_pixels(desired_size, pinde, masker)
            
            # Process image to black and white pixels
            bw_image = process_to_bw_pixels(image, width, height)
            
            # Generate knitting instructions
            instructions = generate_knitting_instructions(bw_image,start,method)
            
            # Save processed image to base64 for display
            img_buffer = BytesIO()
            bw_image = bw_image.resize((width*10, height*10), Image.Resampling.NEAREST)  # Scale up for better visibility
            bw_image.save(img_buffer, format='PNG')
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

if __name__ == '__main__':
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 33507))
    app.run(host=host, port=port, debug=True)
