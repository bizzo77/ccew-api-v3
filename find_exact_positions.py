"""
Find exact X and Y positions by placing test markers at field boundaries
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

template_path = "CCEW_OFFICIAL_TEMPLATE.pdf"

def create_marker_overlay():
    """Create overlay with position markers"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 7)
    can.setFillColor(colors.blue)
    
    # Draw X-axis markers every 50 points
    for x in range(50, 600, 50):
        can.drawString(x, 800, f"X{x}")
        can.drawString(x, 400, f"X{x}")
        can.drawString(x, 100, f"X{x}")
    
    # Draw Y-axis markers every 50 points  
    for y in range(50, 850, 50):
        can.drawString(10, y, f"Y{y}")
        can.drawString(550, y, f"Y{y}")
    
    can.save()
    packet.seek(0)
    return packet

print("Creating position reference PDF...")

template_pdf = PdfReader(template_path)
output_pdf = PdfWriter()

# Add markers to page 1
template_page = template_pdf.pages[0]
overlay_buffer = create_marker_overlay()
overlay_pdf = PdfReader(overlay_buffer)
overlay_page = overlay_pdf.pages[0]
template_page.merge_page(overlay_page)
output_pdf.add_page(template_page)

# Add remaining pages
for page_num in range(1, len(template_pdf.pages)):
    output_pdf.add_page(template_pdf.pages[page_num])

output_file = "POSITION_REFERENCE.pdf"
with open(output_file, 'wb') as f:
    output_pdf.write(f)

print(f"✅ Created {output_file}")
print("\nUse this to identify exact X and Y coordinates for each field")
print("The blue markers show X and Y positions in 50-point intervals")
