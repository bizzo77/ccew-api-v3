"""
Test with HIGHER Y values since current values are appearing too low on the page
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

def test_position(x, y, text, filename):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)
    can.setFillColor(colors.black)
    can.drawString(x, y, text)
    can.save()
    packet.seek(0)
    
    template_pdf = PdfReader('CCEW_OFFICIAL_TEMPLATE.pdf')
    output_pdf = PdfWriter()
    
    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.pages[0]
    
    first_page = template_pdf.pages[0]
    first_page.merge_page(overlay_page)
    output_pdf.add_page(first_page)
    
    for page_num in range(1, len(template_pdf.pages)):
        output_pdf.add_page(template_pdf.pages[page_num])
    
    with open(filename, 'wb') as f:
        output_pdf.write(f)

if __name__ == "__main__":
    # Test Property Name with higher Y values
    # Current Y=562 appears in Suburb, so Property Name should be higher
    # Try Y values from 600 to 650
    
    for y in [600, 610, 620, 630, 640, 650]:
        test_position(70, y, f"PROP_{y}", f"test_prop_{y}.pdf")
        print(f"✅ Created test_prop_{y}.pdf")
    
    print("\nCheck which Y value places text correctly in the Property Name field")
