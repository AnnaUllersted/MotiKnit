from app import generate_knitting_instructions
import numpy as np
from PIL import Image


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
    def test_top_to_bottom_alternating_iteration(self): 
        image = Image.fromarray(self.pixels.astype('uint8'))
        height = 4
        width = 5
        correct_instructions = [['2 white', '2 black', '1 white'], 
                                ['2 white', '3 black'],
                                ['3 white', '2 black'], 
                                ['1 black', '2 white', '2 black']
                                ]
        
        bottom_to_top = False
        alternating_iteration = True
        instructions = generate_knitting_instructions(image, bottom_to_top, alternating_iteration)
        for i,row in enumerate(correct_instructions):
            self.assertEqual(instructions[i],row)

    def test_bottom_to_top_alternating_iteration(self): 
        image = Image.fromarray(self.pixels.astype('uint8'))
        height = 4
        width = 5
        correct_instructions = [['1 black', '2 white', '2 black'],
                                ['3 white', '2 black'],
                                ['2 white', '3 black'],
                                ['2 white', '2 black', '1 white']
                                ]
        
        bottom_to_top = True
        alternating_iteration = True
        instructions = generate_knitting_instructions(image, bottom_to_top, alternating_iteration)
        for i,row in enumerate(correct_instructions):
            self.assertEqual(instructions[i],row)
        
    def test_bottom_to_top_non_alternating_iteration(self): 
        image = Image.fromarray(self.pixels.astype('uint8'))
        height = 4
        width = 5
        correct_instructions = [['1 black', '2 white', '2 black'],
                                ['2 black', '3 white'],
                                ['2 white', '3 black'],
                                ['1 white', '2 black', '2 white']
                                ]
        
        bottom_to_top = True
        alternating_iteration = False
        instructions = generate_knitting_instructions(image, bottom_to_top, alternating_iteration)
        for i,row in enumerate(correct_instructions):
            self.assertEqual(instructions[i],row)

    def test_top_to_bottom_non_alternating_iteration(self): 
        image = Image.fromarray(self.pixels.astype('uint8'))
        height = 4
        width = 5
        correct_instructions = [['2 white', '2 black', '1 white'], 
                                ['3 black', '2 white'],
                                ['3 white', '2 black'], 
                                ['2 black', '2 white', '1 black']
                                ]
        
        bottom_to_top = False
        alternating_iteration = False
        instructions = generate_knitting_instructions(image, bottom_to_top, alternating_iteration)
        for i,row in enumerate(correct_instructions):
            self.assertEqual(instructions[i],row)        
  
if __name__ == '__main__': 
    unittest.main() 