"""
Reverse engineer coordinates by testing where text actually appears
We know "123" appears in Street Name field when we set it at X=460, Y=605
Let's find where it SHOULD appear (Street Number field)
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

template_path = "CCEW_OFFICIAL_TEMPLATE.pdf"

def create_test(label, x, y):
    """Create a test PDF with text at specific coordinates"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)
    can.setFillColor(colors.red)
    can.drawString(x, y, f"{label}@{x},{y}")
    can.save()
    packet.seek(0)
    return packet

# Current observation: When I put text at X=460, Y=605, it appears in Street Name field
# Street Name field is BELOW Street Number field
# So Street Number must be at a HIGHER Y value

# Let's test a range of positions for Street Number
tests = [
    ("STR_NUM_1", 460, 625),  # Try 20 points higher
    ("STR_NUM_2", 460, 630),  # Try 25 points higher  
    ("STR_NUM_3", 460, 635),  # Try 30 points higher
    ("STR_NUM_4", 460, 640),  # Try 35 points higher
    ("STR_NUM_5", 460, 645),  # Try 40 points higher
]

print("Creating reverse-engineering test PDF...")

template_pdf = PdfReader(template_path)
output_pdf = PdfWriter()

template_page = template_pdf.pages[0]

# Add all test markers
for label, x, y in tests:
    overlay_buffer = create_test(label, x, y)
    overlay_pdf = PdfReader(overlay_buffer)
    overlay_page = overlay_pdf.pages[0]
    template_page.merge_page(overlay_page)

output_pdf.add_page(template_page)

# Add remaining pages
for page_num in range(1, len(template_pdf.pages)):
    output_pdf.add_page(template_pdf.pages[page_num])

output_file = "REVERSE_TEST.pdf"
with open(output_file, 'wb') as f:
    output_pdf.write(f)

print(f"✅ Created {output_file}")
print("\nCheck which STR_NUM marker appears in the Street Number field")
print("(The field on the RIGHT side of the Floor/Unit row)")
