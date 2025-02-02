from PIL import Image
import numpy as np
from translator import translate
from sklearn.cluster import KMeans
from collections import Counter

class KnittingPatternGenerator:
    def __init__(self, image, desired_height_cm, desired_rows, desired_columns, bottom_to_top, alternating_iterations, intensity):
        self.image = image
        self.desired_height_cm = desired_height_cm
        self.desired_rows = desired_rows
        self.desired_columns = desired_columns
        self.bottom_to_top = bottom_to_top
        self.alternating_iterations = alternating_iterations
        self.greyscale_image: Image = None
        self.width_px, self.height_px = self.get_target_px_width_and_height()
        self.intensity = intensity


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

    
    def process_to_bw_pixels(self):
        """Convert image to black and white pixels of specified size"""
        if self.greyscale_image is None:

            # Resize image
            resized = self.image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)
            # Convert to grayscale
            self.grayscale: Image = resized.convert('L')

        intensity_remap = self.intensity * 255/100
        # Convert to pure black and white (threshold at 128)
        bw_image = self.grayscale.point(lambda x: 0 if x < intensity_remap else 255, '1')

        return bw_image


    # def process_to_color_quantized(self, n_colors):
    #     # Åbn billedet
    #     image = self.image.convert('RGB')

    #     # Resize image
    #     image = self.image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)

    #     # Konverter billedet til en numpy-array
    #     img_data = np.array(image)
    #     w, h, d = img_data.shape
    #     img_flat = img_data.reshape((-1, 3))  # Flad array til (pixels, RGB)

    #     # Udfør KMeans clustering
    #     kmeans = KMeans(n_clusters=n_colors, random_state=42)
    #     kmeans.fit(img_flat)

    #     # Erstat hver pixel med dens nærmeste centroids farve
    #     clustered_img = kmeans.cluster_centers_[kmeans.labels_]
    #     clustered_img = clustered_img.reshape((w, h, 3)).astype('uint8')

    #     # Konverter tilbage til et PIL Image og gem resultatet
    #     quantized_image = Image.fromarray(clustered_img)
        
    #     return quantized_image
    

    # def process_to_color_quantized(self, n_colors):
    #     # Åbn billedet og konverter til RGB
    #     image = self.image.convert('RGB')

    #     # Konverter det originale billede til en numpy-array
    #     original_img_data = np.array(image)
    #     w, h, d = original_img_data.shape
    #     img_flat = original_img_data.reshape((-1, 3))  # Flad array til (pixels, RGB)

    #     # Udfør KMeans clustering på det originale billede
    #     kmeans = KMeans(n_clusters=n_colors, random_state=42)
    #     kmeans.fit(img_flat)

    #     # Hent de fundne farver (centroids)
    #     centroids = kmeans.cluster_centers_

    #     # Resize det oprindelige billede
    #     resized_image = image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)
    #     resized_img_data = np.array(resized_image)

    #     # Erstat hver pixel i det resized billede med dens nærmeste farve fra centroids
    #     resized_flat = resized_img_data.reshape((-1, 3))  # Flad array til (pixels, RGB)
    #     labels = kmeans.predict(resized_flat)  # Brug KMeans modelen til at forudsige farver
    #     clustered_img = centroids[labels]
    #     clustered_img = clustered_img.reshape((self.height_px, self.width_px, 3)).astype('uint8')

    #     # Konverter tilbage til et PIL Image og returnér
    #     quantized_image = Image.fromarray(clustered_img)
    #     return quantized_image

    # def process_to_color_quantized(self, n_colors):
    #     # Åbn billedet og konverter til RGB
    #     image = self.image.convert('RGB')

    #     # Konverter det originale billede til en numpy-array
    #     original_img_data = np.array(image)
    #     w, h, d = original_img_data.shape
    #     img_flat = original_img_data.reshape((-1, 3))  # Flad array til (pixels, RGB)

    #     # Find de mest hyppige farver i det originale billede
    #     color_counts = Counter(map(tuple, img_flat))  # Tæl unikke farver
    #     most_common_colors = [color for color, _ in color_counts.most_common(n_colors)]

    #     # Opret en lookup-tabel for farveklassifikation
    #     color_lookup = {tuple(color): idx for idx, color in enumerate(most_common_colors)}

    #     # Resize det oprindelige billede
    #     resized_image = image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)
    #     resized_img_data = np.array(resized_image)

    #     # Erstat hver pixel i det resized billede med den nærmeste farve fra de fundne farver
    #     clustered_img = np.zeros_like(resized_img_data)
    #     for i, row in enumerate(resized_img_data):
    #         for j, pixel in enumerate(row):
    #             pixel_tuple = tuple(pixel)
    #             if pixel_tuple in color_lookup:
    #                 clustered_img[i, j] = most_common_colors[color_lookup[pixel_tuple]]
    #             else:
    #                 # Hvis en pixel ikke findes i de mest almindelige farver, tag den nærmeste
    #                 clustered_img[i, j] = min(most_common_colors, key=lambda c: np.linalg.norm(np.array(c) - pixel))

    #     # Konverter tilbage til et PIL Image og returnér
    #     quantized_image = Image.fromarray(clustered_img.astype('uint8'))
    #     return quantized_image


    def process_to_color_quantized(self, n_colors, tolerance=10):
        """
        Process image to a color-quantized version with n_colors distinct colors.
        """
        # Åbn billedet og konverter til RGB
        image = self.image.convert('RGB')

        # Konverter det originale billede til en numpy-array
        original_img_data = np.array(image)
        img_flat = original_img_data.reshape((-1, 3))  # Flad array til (pixels, RGB)

        # Gruppér lignende farver inden for en tolerance
        def find_or_add_color(color, color_list, tolerance):
            for existing_color in color_list:
                if np.linalg.norm(np.array(color) - np.array(existing_color)) <= tolerance:
                    return existing_color
            color_list.append(color)
            return color

        # Reducer farvepaletten med tolerance
        reduced_colors = []
        for color in map(tuple, img_flat):
            find_or_add_color(color, reduced_colors, tolerance)

        # Tæl de reducerede farver
        reduced_color_counts = Counter(map(tuple, reduced_colors))
        most_common_colors = [color for color, _ in reduced_color_counts.most_common(n_colors)]

        # Resize det oprindelige billede
        resized_image = image.resize((self.width_px, self.height_px), Image.Resampling.LANCZOS)
        resized_img_data = np.array(resized_image)

        # Erstat hver pixel i det resized billede med den nærmeste farve fra de fundne farver
        clustered_img = np.zeros_like(resized_img_data)
        for i, row in enumerate(resized_img_data):
            for j, pixel in enumerate(row):
                # Find den nærmeste farve
                closest_color = min(
                    most_common_colors,
                    key=lambda c: np.linalg.norm(np.array(c) - np.array(pixel))
                )
                clustered_img[i, j] = closest_color

        # Konverter tilbage til et PIL Image og returnér
        quantized_image = Image.fromarray(clustered_img.astype('uint8'))
        return quantized_image






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

