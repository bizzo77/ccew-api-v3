"""
Coordinate finder - generates test PDFs with markers at different positions
to help identify exact field locations
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

def create_test_markers(test_positions):
    """Create overlay with test text at specified positions"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    can.setFont("Helvetica", 9)
    can.setFillColor(colors.red)
    
    for label, (x, y) in test_positions.items():
        # Draw the test text
        can.drawString(x, y, f"[{label}]")
        
        # Draw a small crosshair
        can.setStrokeColor(colors.red)
        can.setLineWidth(0.5)
        can.line(x-5, y, x+5, y)
        can.line(x, y-5, x, y+5)
    
    can.save()
    packet.seek(0)
    return packet

def generate_test_pdf(test_positions, output_name):
    """Generate a test PDF with markers"""
    template_path = 'CCEW_OFFICIAL_TEMPLATE.pdf'
    
    # Read template
    template_pdf = PdfReader(template_path)
    output_pdf = PdfWriter()
    
    # Create test overlay
    overlay_buffer = create_test_markers(test_positions)
    overlay_pdf = PdfReader(overlay_buffer)
    overlay_page = overlay_pdf.pages[0]
    
    # Apply to first page
    first_page = template_pdf.pages[0]
    first_page.merge_page(overlay_page)
    output_pdf.add_page(first_page)
    
    # Add remaining pages
    for page_num in range(1, len(template_pdf.pages)):
        output_pdf.add_page(template_pdf.pages[page_num])
    
    # Save
    with open(output_name, 'wb') as f:
        output_pdf.write(f)
    
    print(f"✅ Test PDF created: {output_name}")

if __name__ == "__main__":
    # Test different Y positions for Property Name field
    # We know X should be around 60-70
    # Let's test Y positions from 550 to 570 in steps of 5
    
    test_positions = {}
    
    # Test Property Name field positions
    for y in range(550, 571, 5):
        test_positions[f"PN{y}"] = (70, y)
    
    # Test Street Number field positions  
    for y in range(500, 521, 5):
        test_positions[f"SN{y}"] = (210, y)
    
    generate_test_pdf(test_positions, 'test_coordinates_page1.pdf')
    
    print("\nOpen test_coordinates_page1.pdf and check which markers align with field boxes")
    print("The marker labels show the Y coordinate being tested")
