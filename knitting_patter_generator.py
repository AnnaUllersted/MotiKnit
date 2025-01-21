from PIL import Image
import numpy as np
from translator import translate

class KnittingPatternGenerator:
    def __init__(self, image, desired_height_cm, desired_rows, desired_columns, bottom_to_top, alternating_iterations):
        self.image = image
        self.desired_height_cm = desired_height_cm
        self.desired_rows = desired_rows
        self.desired_columns = desired_columns
        self.bottom_to_top = bottom_to_top
        self.alternating_iterations = alternating_iterations
        self.greyscale_image: Image = None
        self.width_px, self.height_px = self.get_target_px_width_and_height()


    def get_target_px_width_and_height(self):
        """Calculate the number of pixels needed based on the desired size and knitting gauge"""
        # Get the original dimensions
        original_width, original_height = self.image.size
        # Calculate aspect ratio
        aspect_ratio = original_width / original_height
        # Calculate pixels needed for desired size
        desired_width_cm = self.desired_height_cm * aspect_ratio
        target_width_px = int((self.desired_columns * desired_width_cm) / 10)
        target_height_px = int((self.desired_rows * self.desired_height_cm) / 10)
        return target_width_px, target_height_px

    
    def process_to_bw_pixels(self,intensity):
        """Convert image to black and white pixels of specified size"""
        if self.greyscale_image is None:

            # Resize image
            resized = self.image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)
            # Convert to grayscale
            self.grayscale: Image = resized.convert('L')

        intensity_remap = intensity * 255/100
        # Convert to pure black and white (threshold at 128)
        bw_image = self.grayscale.point(lambda x: 0 if x < intensity_remap else 255, '1')

        return bw_image


    def generate_knitting_instructions(self, bw_image, color1, color2, lang='en'):
        """Generate knitting instructions reading from bottom up, left to right"""
        pixels = np.array(bw_image)
        instructions = []

        if self.bottom_to_top:
            for i,row in enumerate(reversed(pixels)):
                right_to_left = True
                if self.alternating_iterations: 
                    right_to_left = i % 2 == 0
                    if right_to_left: #even row number
                        row_data = row[::-1] #reversed array
                    else: 
                        row_data = row
                else: #start lower right corner
                    row_data = row[::-1] #reversed array
                instructions.append(self.generate_row_instructions(row_data, left_to_right, i, color1, color2, lang))
        else: #top to bottom
            for i,row in enumerate(pixels):
                left_to_right = True
                if self.alternating_iterations:
                    left_to_right = i % 2 == 0
                    if left_to_right: #even row number
                        row_data = row
                    else: 
                        row_data = row[::-1] #reversed array
                else: #start upper left corner
                    row_data = row
                row_instructions = self.generate_row_instructions(row_data, left_to_right, i, color1, color2, lang)
                instructions.append(row_instructions)
        return instructions
    
    def generate_row_instructions(self, row_data, ret_pind, row_number, color1, color2, lang):
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
                color = translate(color1,lang) if current_color == 1 else translate(color2,lang)
                row_instructions.append(translate('masker_details', lang, count=count, color=color))
                current_color = row_data[col]
                count = 1
        color = translate(color1,lang) if current_color == 1 else translate(color2,lang)
        row_instructions.append(translate('masker_details', lang, count=count, color=color))
        return row_instructions

