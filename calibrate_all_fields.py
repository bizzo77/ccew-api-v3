"""
Systematic field coordinate calibration
Tests multiple Y values for each field to find correct position
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io

template_path = "CCEW_OFFICIAL_TEMPLATE.pdf"

def create_test_overlay(test_fields):
    """Create overlay with test fields at different Y positions"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)
    can.setFillColor(colors.red)  # Use red for visibility
    
    for field_name, x, y_values in test_fields:
        for y in y_values:
            text = f"{field_name}_{y}"
            can.drawString(x, y, text)
    
    can.save()
    packet.seek(0)
    return packet

# Test Installation Address fields with range of Y values
print("Creating calibration test PDF...")

# Based on observation: fields are appearing too low, need higher Y values
# Property Name was at Y=650 but appearing correct
# Street Number at Y=605 appeared in Street Name
# Need to test higher values

test_fields_page1 = [
    # Property Name - test around 650
    ("PROP", 70, [645, 648, 651, 654, 657]),
    
    # Street Number - test higher than 605
    ("STNUM", 485, [595, 600, 605, 610, 615]),
    
    # Street Name - test higher than 560  
    ("STNAME", 70, [550, 555, 560, 565, 570]),
    
    # Suburb - test higher than 515
    ("SUBURB", 70, [505, 510, 515, 520, 525]),
    
    # Customer First Name - test higher than 400
    ("CUSTFN", 70, [390, 395, 400, 405, 410]),
]

# Create test PDF
template_pdf = PdfReader(template_path)
output_pdf = PdfWriter()

# Page 1 with test markers
template_page = template_pdf.pages[0]
overlay_buffer = create_test_overlay(test_fields_page1)
overlay_pdf = PdfReader(overlay_buffer)
overlay_page = overlay_pdf.pages[0]
template_page.merge_page(overlay_page)
output_pdf.add_page(template_page)

# Add remaining pages unchanged
for page_num in range(1, len(template_pdf.pages)):
    output_pdf.add_page(template_pdf.pages[page_num])

# Save
output_file = "CALIBRATION_TEST.pdf"
with open(output_file, 'wb') as f:
    output_pdf.write(f)

print(f"✅ Created {output_file}")
print("\nInstructions:")
print("1. Open CALIBRATION_TEST.pdf")
print("2. For each field, note which Y value places text correctly IN the field box")
print("3. Use those Y values in pdf_generator.py")
print("\nFields being tested:")
print("- PROP_XXX = Property Name field")
print("- STNUM_XXX = Street Number field")
print("- STNAME_XXX = Street Name field")
print("- SUBURB_XXX = Suburb field")
print("- CUSTFN_XXX = Customer First Name field")
