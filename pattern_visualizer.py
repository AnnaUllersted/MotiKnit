from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class KnittingPatternVisualizer:


    def __init__(self, width_px, height_px):
        self.width_px = width_px
        self.height_px = height_px
        self.square_px_size = 20


    def generate_illustration(self, bw_image):
        """Generate knitting illustration with grey area and row numbers """
        # Save processed image to base64 for display
        img_buffer = BytesIO()

        # resize image so it fits a boundary
        width_w_boundary = self.width_px*self.square_px_size
        height_w_boundary = self.height_px*self.square_px_size

        # Opret et nyt billede med ekstra plads til tekst og grå kanter
        text_space_width = 60  # Bredden på pladsen til teksten
        canvas = Image.new('RGB', (width_w_boundary + text_space_width, height_w_boundary), (120, 120, 120))  # Grå baggrund

        # Tegn det originale billede på det nye lærred med grå kanter
        for y in range(self.height_px):
            for x in range(self.width_px):
                pixel_color = bw_image.getpixel((x, y))  # 0 eller 255
                color = (0, 0, 0) if pixel_color == 0 else (255, 255, 255)  # Sort eller hvid
                pixel_x = text_space_width + x * self.square_px_size
                pixel_y = y * self.square_px_size
                # Fyld midten af det grå område med den originale pixels farve
                for i in range(1, self.square_px_size - 1):  # Undgå de yderste pixels (grå kant)
                    for j in range(1, self.square_px_size - 1):
                        canvas.putpixel((pixel_x + i, pixel_y + j), color)

        # Tilføj tekst ud for hver række
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype("arial.ttf", size=14)  # Brug en passende skrifttype og størrelse
        for y in range(self.height_px):
            text = f"Pind {y + 1}"
            text_position = (10, y * self.square_px_size + self.square_px_size // 4)  # Placer teksten midt på pixel-rækken
            draw.text(text_position, text, font=font, fill=(0, 0, 0))  # Hvid tekst

        bw_image_for_display = canvas
        bw_image_for_display = bw_image_for_display.resize((self.width_px*self.square_px_size+text_space_width, self.height_px*self.square_px_size), Image.Resampling.NEAREST)  # Scale up for better visibility
        bw_image_for_display.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return img_buffer.getvalue()