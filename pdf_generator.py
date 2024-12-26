from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
from PIL import Image
import base64

def create_pattern_pdf(processed_image_base64, parameters, instructions):
    # Create buffer for PDF
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Prepare story (content)
    story = []
    styles = getSampleStyleSheet()
    
    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    story.append(Paragraph("Strikke Mønster", title_style))
    
    # Add parameters
    story.append(Paragraph("Detaljer:", styles['Heading2']))
    details = [
        f"Endelig størrelse: {parameters['size']} x {parameters['size']} cm",
        f"Strikkefasthed: {parameters['pinde']} pinde × {parameters['masker']} masker per 10cm",
        f"Endeligt størrelse af mønster: {parameters['final_width']} masker × {parameters['final_height']} pinde"
    ]
    for detail in details:
        story.append(Paragraph(detail, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Add processed image
    if processed_image_base64:
        image_data = base64.b64decode(processed_image_base64)
        image_buffer = io.BytesIO(image_data)
        img = RLImage(image_buffer, width=400, height=300)
        story.append(img)
        story.append(Spacer(1, 20))
    
    # Add instructions
    story.append(Paragraph("Strikkeopskrift:", styles['Heading2']))
    for instruction_set in instructions:
        instruction_text = " ".join(instruction_set)
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer