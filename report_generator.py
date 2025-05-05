from reportlab.lib.colors import HexColor
from io import BytesIO
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, ListItem, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from utils.visualization import create_radar_chart
from reportlab.platypus import Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Use CSS variables in PDF generation
KERMIT_COLORS = {
    'primary': HexColor('#FF6B35'),
    'dark': HexColor('#292929'),
    'accent': HexColor('#D90429')
}

def create_pdf_styles():
    print("Creating PDF styles with corporate colors...")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'KermitTitle',
        parent=styles['Title'],
        textColor=KERMIT_COLORS['dark'],
        fontName='Helvetica-Bold',
        fontSize=16
    ))
    return styles

# Updated styles with corporate colors

def generate_pdf_report(data, output_dir):
    # Initialize content list FIRST
    content = []
    PAGE_HEIGHT = 842  # A4 height in points (11.69 inches)
    current_height = 0
    MARGIN = 50
    
    # 1. Create document template
    filename = f"{output_dir}/{data['name'].replace(' ', '_')}_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # 2. Define styles PROPERLY
    styles = getSampleStyleSheet()
    
    # Create and register custom styles
    custom_styles = {
        'Title': ParagraphStyle(
            name='KermitTitle',
            parent=styles['Title'],
            textColor=colors.HexColor('#292929'),
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=TA_CENTER
        ),
        'Heading2': ParagraphStyle(
            name='KermitHeading2',
            parent=styles['Heading2'],
            textColor=colors.HexColor('#FF6B35'),
            fontName='Helvetica-Bold',
            fontSize=12
        ),
        'Normal': ParagraphStyle(
            name='KermitNormal',
            parent=styles['Normal'],
            textColor=colors.HexColor('#292929'),
            fontSize=10,
            leading=10
        )
    }

    print("Available custom styles:", list(custom_styles.keys()))

    try:
        print("title to be added")

        # Add header with proper style reference
        content.append(Paragraph("Kermit Tech Candidate Report", custom_styles['Title']))
        content.append(Spacer(1, 5))
        print("Generating PDF report...")
    except KeyError as e:
        raise RuntimeError(f"Missing style: {e}. Available styles: {list(custom_styles.keys())}") from e
    
    # Create document template
    filename = f"{output_dir}/{data['name'].replace(' ', '_')}_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
   
    # Add sections
    sections = [
        ("Candidate Name", data['name']),
        ("Professional Summary", data['summary']),
        ("Education", f"{data['education']['degree']} - {data['education']['university']}"),
        ("Experience", f"Last Role: {data['experience']['last_title']} "),
        ("Skills Analysis", "Ratings:")

    ]
    
    for section in sections:
        content.append(Paragraph(section[0], custom_styles['Heading2']))
        content.append(Paragraph(section[1], custom_styles['Normal']))
        content.append(Spacer(1, 5))
    
    # Add radar chart
    chart_path = create_radar_chart(data['analysis'])
    print("Radar chart path:", chart_path)
    content.append(Image(chart_path, width=300, height=250))
    content.append(Spacer(1, 5))
    
    # Add interview questions table
    content.append(Paragraph("Interview Questions", custom_styles['Heading2']))
    questions_table = Table(
        [
            [str(i+1), Paragraph(q, styles['Normal'])] 
            for i, q in enumerate(data['interview_questions'])
        ],
        colWidths=[30, 300],
        rowHeights=[None] * len(data['interview_questions']),  # Auto-height
        style=[
            ('BACKGROUND', (0,0), (-1,0), KERMIT_COLORS['primary']),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, KERMIT_COLORS['accent']),
            ('WORDWRAP', (1,0), (1,-1), 'CJK'),  # Enable word wrap
            ('VALIGN', (0,0), (-1,-1), 'TOP')     # Align content to top
        ]
    )
    content.append(questions_table)
    
    # Build the PDF
    doc.build(content)
    print("PDF report generated successfully.")
    print("PDF file path:", filename)
    return filename

def generate_pdf_report_with_audio(data, adata, output_dir):
    # Initialize content list FIRST
    content = []
    PAGE_HEIGHT = 842  # A4 height in points (11.69 inches)
    current_height = 0
    MARGIN = 50
    
    # 1. Create document template
    filename = f"{output_dir}/{data['name'].replace(' ', '_')}_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # 2. Define styles PROPERLY
    styles = getSampleStyleSheet()
    
    # Create and register custom styles
    custom_styles = {
        'Title': ParagraphStyle(
            name='KermitTitle',
            parent=styles['Title'],
            textColor=colors.HexColor('#292929'),
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=TA_CENTER
        ),
        'Heading2': ParagraphStyle(
            name='KermitHeading2',
            parent=styles['Heading2'],
            textColor=colors.HexColor('#FF6B35'),
            fontName='Helvetica-Bold',
            fontSize=12
        ),
        'Normal': ParagraphStyle(
            name='KermitNormal',
            parent=styles['Normal'],
            textColor=colors.HexColor('#292929'),
            fontSize=10,
            leading=10
        )
    }

    print("Available custom styles:", list(custom_styles.keys()))

    try:
        print("title to be added")

        # Add header with proper style reference
        content.append(Paragraph("Kermit Tech Candidate Report", custom_styles['Title']))
        content.append(Spacer(1, 5))
        print("Generating PDF report...")
    except KeyError as e:
        raise RuntimeError(f"Missing style: {e}. Available styles: {list(custom_styles.keys())}") from e
    
    # Create document template
    filename = f"{output_dir}/{data['name'].replace(' ', '_')}_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
   
    # Add sections
    sections = [
        ("Candidate Name", data['name']),
        ("Professional Summary", data['summary']),
        ("Education", f"{data['education']['degree']} - {data['education']['university']}"),
        ("Experience", f"Last Role: {data['experience']['last_title']} "),
        ("Skills Analysis", "Ratings:")

    ]
    
    for section in sections:
        content.append(Paragraph(section[0], custom_styles['Heading2']))
        content.append(Paragraph(section[1], custom_styles['Normal']))
        content.append(Spacer(1, 5))
    
    # Add radar chart
    chart_path = create_radar_chart(data['analysis'])
    print("Radar chart path:", chart_path)
    content.append(Image(chart_path, width=300, height=250))
    content.append(Spacer(1, 5))
    

    # Add interview questions table
    content.append(Paragraph("Interview Questions", custom_styles['Heading2']))
    questions_table = Table(
        [
            [str(i+1), Paragraph(q, styles['Normal'])] 
            for i, q in enumerate(data['interview_questions'])
        ],
        colWidths=[30, 300],
        rowHeights=[None] * len(data['interview_questions']),  # Auto-height
        style=[
            ('BACKGROUND', (0,0), (-1,0), KERMIT_COLORS['primary']),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, KERMIT_COLORS['accent']),
            ('WORDWRAP', (1,0), (1,-1), 'CJK'),  # Enable word wrap
            ('VALIGN', (0,0), (-1,-1), 'TOP')     # Align content to top
        ]
    )
    content.append(questions_table)
    
    content.append(Paragraph("Skills Interview Analysis", custom_styles['Heading2']))
    content.append(Paragraph("Interview Ratings:", custom_styles['Normal']))
    content.append(Spacer(1, 5))

    achart_path = create_radar_chart(adata['analysis'])

    print("Interview Radar chart path:", achart_path)
    content.append(Image(achart_path, width=300, height=250))
    content.append(Spacer(1, 5))

    content.append(Paragraph("Concerns", custom_styles['Heading2']))
    red_flag_items = [
        ListItem(Paragraph(flag, custom_styles['Normal']), bulletColor='red') 
        for flag in adata['red_flags']
    ]

    content.append(ListFlowable(
        red_flag_items,
        bulletType='bullet',
        start='square',
        bulletColor=KERMIT_COLORS['accent'],  # Use your red accent color
        leftIndent=20
    ))
    content.append(Spacer(1, 5))

    content.append(Paragraph("Interview Summary", custom_styles['Heading2']))
    content.append(Paragraph(adata['summary'], custom_styles['Normal']))
    content.append(Spacer(1, 5))

    
    # Build the PDF
    doc.build(content)
    print("PDF report generated successfully.")
    print("PDF file path:", filename)
    return filename


def combine_pdfs(pdf_paths):
    """Combine multiple PDF files into one in memory"""
    merger = PdfMerger()
    
    for pdf_path in pdf_paths:
        with open(pdf_path, 'rb') as f:
            merger.append(f)
    
    combined_buffer = BytesIO()
    merger.write(combined_buffer)
    merger.close()
    
    return combined_buffer.getvalue()

