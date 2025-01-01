from app import generate_knitting_instructions, process_to_bw_pixels
import numpy as np
from PIL import Image
import base64


# unit test case 
import unittest 
  
class TestStringMethods(unittest.TestCase): 
    # Sample pixels array (representing image rows)
    pixels = np.array([
        [1, 1, 0, 0, 1],  # Row 1 (white, white, black, black, white)
        [0, 0, 0, 1, 1],  # Row 2 (black, black, black, white, white)
        [1, 1, 1, 0, 0],  # Row 3 (white, white, white, black, black)
        [0, 0, 1, 1, 0]   # Row 4 (black, white, white, white, black)
    ])
    # test function to test equality of two value     

    def test_process_to_bw_pixels(self):
        # Input data: grayscale image
        grayscale_pixels = np.array([
            [200, 200, 50, 50, 200], 
            [50, 50, 50, 200, 200],
            [200, 200, 200, 50, 50], 
            [50, 50, 200, 200, 50]
        ], dtype='uint8')
        image = Image.fromarray(grayscale_pixels, mode='L')

        # Expected output data without borders
        expected_bw_pixels = np.array([
            [255, 255, 0, 0, 255],
            [0, 0, 0, 255, 255],
            [255, 255, 255, 0, 0],
            [0, 0, 255, 255, 0]
        ], dtype='uint8')  # Binary output (0 or 255 for black or white)

        # Parameters
        width, height = 5, 4  # Dimensions for resizing

        # Process the image
        bw_image, img_str = process_to_bw_pixels(image, width, height)

        #bw_image.show()
        #bw_image_for_display.show()
        #print(type(bw_image_for_display))

        with open("debug_image.png", "wb") as f:
            f.write(base64.b64decode(img_str))


        decoded_image = base64.b64decode(img_str)
        with open("debug_image_from_base64.png", "wb") as f:
            f.write(decoded_image)

  
if __name__ == '__main__': 
    unittest.main() 

