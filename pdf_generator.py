from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
from PIL import Image
from translator import translate
import base64

def create_pattern_pdf(processed_image_base64, parameters, instructions, lang='en'):
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
    story.append(Paragraph(translate('pattern_title', lang), title_style))

    # Add parameters
    story.append(Paragraph(translate('details_title', lang), styles['Heading2']))
    details = [
        translate('final_size', lang, size=parameters['size']),
        translate('knit_gauge', lang, pinde=parameters['pinde'], masker=parameters['masker']),
        translate('pattern_size', lang, final_width=parameters['final_width'], final_height=parameters['final_height'])
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
    story.append(Paragraph(translate('instructions_title', lang), styles['Heading2']))
    for instruction_set in instructions:
        instruction_text = " ".join(instruction_set)
        story.append(Paragraph(instruction_text, styles['Normal']))
        story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer