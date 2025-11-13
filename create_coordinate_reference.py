"""
Create a reference PDF with coordinate markers to help identify exact field positions
This overlays coordinate markers on the official form to help with calibration
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

def create_coordinate_markers():
    """Create a PDF with coordinate markers every 50 points"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Draw vertical grid lines
    can.setStrokeColor(colors.Color(1, 0, 0, alpha=0.3))
    can.setLineWidth(0.5)
    for x in range(0, int(width), 50):
        can.line(x, 0, x, height)
        # Add coordinate label
        can.setFillColor(colors.red)
        can.setFont("Helvetica", 6)
        can.drawString(x + 2, height - 10, str(x))
        can.drawString(x + 2, 5, str(x))
    
    # Draw horizontal grid lines
    for y in range(0, int(height), 50):
        can.line(0, y, width, y)
        # Add coordinate label
        can.setFillColor(colors.red)
        can.setFont("Helvetica", 6)
        can.drawString(5, y + 2, str(int(height - y)))
        can.drawString(width - 30, y + 2, str(int(height - y)))
    
    # Add title
    can.setFillColor(colors.red)
    can.setFont("Helvetica-Bold", 10)
    can.drawString(width/2 - 100, height - 30, "Coordinate Reference Grid (50pt spacing)")
    
    can.save()
    packet.seek(0)
    return packet

def overlay_grid_on_official_form():
    """Overlay coordinate grid on official CCEW form"""
    
    template_path = 'CCEW_OFFICIAL_TEMPLATE.pdf'
    output_path = 'CCEW_WITH_GRID.pdf'
    
    # Read template
    template_pdf = PdfReader(template_path)
    output_pdf = PdfWriter()
    
    # Create grid overlay
    grid_buffer = create_coordinate_markers()
    grid_pdf = PdfReader(grid_buffer)
    grid_page = grid_pdf.pages[0]
    
    # Apply grid to first page only
    first_page = template_pdf.pages[0]
    first_page.merge_page(grid_page)
    output_pdf.add_page(first_page)
    
    # Add remaining pages without grid
    for page_num in range(1, len(template_pdf.pages)):
        output_pdf.add_page(template_pdf.pages[page_num])
    
    # Save
    with open(output_path, 'wb') as f:
        output_pdf.write(f)
    
    print(f"✅ Created coordinate reference PDF: {output_path}")
    print("Use this to identify exact field positions")
    print("Grid shows coordinates from bottom-left origin")

if __name__ == "__main__":
    overlay_grid_on_official_form()
