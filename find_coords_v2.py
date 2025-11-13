"""
Improved coordinate finder with correct Y ranges
A4 height = 842 points
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

def create_single_test_field(x, y, text):
    """Create overlay with a single test field"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    can.setFont("Helvetica", 9)
    can.setFillColor(colors.black)
    can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    return packet

def test_field_position(x, y, text, output_name):
    """Test a single field position"""
    template_path = 'CCEW_OFFICIAL_TEMPLATE.pdf'
    
    template_pdf = PdfReader(template_path)
    output_pdf = PdfWriter()
    
    overlay_buffer = create_single_test_field(x, y, text)
    overlay_pdf = PdfReader(overlay_buffer)
    overlay_page = overlay_pdf.pages[0]
    
    first_page = template_pdf.pages[0]
    first_page.merge_page(overlay_page)
    output_pdf.add_page(first_page)
    
    for page_num in range(1, len(template_pdf.pages)):
        output_pdf.add_page(template_pdf.pages[page_num])
    
    with open(output_name, 'wb') as f:
        output_pdf.write(f)

if __name__ == "__main__":
    # Based on grid analysis:
    # Property Name field should be around Y = 842 - 280 = 562
    # Let's test a range around that
    
    print("Testing Property Name field positions...")
    
    # Test Property Name
    test_field_position(70, 562, "TEST_PROPERTY_NAME", "test_property_name.pdf")
    print(f"✅ Created: test_property_name.pdf (X=70, Y=562)")
    
    # Test Street Number (should be around 842 - 330 = 512)
    test_field_position(210, 512, "TEST_ST_NUM", "test_street_number.pdf")
    print(f"✅ Created: test_street_number.pdf (X=210, Y=512)")
    
    # Test Street Name (should be around 842 - 375 = 467)
    test_field_position(70, 467, "TEST_STREET_NAME", "test_street_name.pdf")
    print(f"✅ Created: test_street_name.pdf (X=70, Y=467)")
    
    # Test Suburb (should be around 842 - 425 = 417)
    test_field_position(70, 417, "TEST_SUBURB", "test_suburb.pdf")
    print(f"✅ Created: test_suburb.pdf (X=70, Y=417)")
    
    # Test Customer First Name (should be around 842 - 595 = 247)
    test_field_position(70, 247, "TEST_FIRST_NAME", "test_customer_first.pdf")
    print(f"✅ Created: test_customer_first.pdf (X=70, Y=247)")
    
    print("\n✅ All test PDFs created!")
    print("Check each PDF to see if the text appears in the correct field box")
