"""
PDF Generator for CCEW Forms
Generates a professional PDF document from form data
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import io
import base64


def generate_ccew_pdf(form_data):
    """
    Generate a PDF document from CCEW form data
    Returns: base64 encoded PDF string
    """
    # Create a BytesIO buffer
    buffer = io.BytesIO()
    
    # Create the PDF object
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Colors
    header_color = HexColor('#007bff')
    section_color = HexColor('#333333')
    label_color = HexColor('#555555')
    
    # Starting position
    y = height - 40
    
    # Title
    c.setFillColor(header_color)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, "Certificate of Compliance for Electrical Work (CCEW)")
    y -= 30
    
    # Job Number
    c.setFillColor(section_color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Job #{form_data.get('serial_no', 'N/A')}")
    y -= 25
    
    # Helper function to add a section
    def add_section(title, fields, start_y):
        y = start_y
        c.setFillColor(section_color)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, title)
        y -= 18
        
        c.setFont("Helvetica", 10)
        for label, value in fields:
            if value:  # Only show fields with values
                c.setFillColor(label_color)
                c.drawString(50, y, f"{label}:")
                c.setFillColor(HexColor('#000000'))
                c.drawString(200, y, str(value))
                y -= 15
        
        return y - 10
    
    # Section 1: Installation Address
    fields = [
        ("Property Name", form_data.get('property_name', '')),
        ("Street", f"{form_data.get('install_street_number', '')} {form_data.get('install_street_name', '')}"),
        ("Suburb", form_data.get('install_suburb', '')),
        ("State", form_data.get('install_state', '')),
        ("Postcode", form_data.get('install_postcode', '')),
        ("Nearest Cross Street", form_data.get('nearest_cross_street', '')),
        ("Pit/Pillar/Pole No", form_data.get('pit_pillar_pole_no', '')),
        ("NMI", form_data.get('nmi', '')),
        ("Meter No", form_data.get('meter_no', '')),
        ("AEMO Provider ID", form_data.get('aemo_provider_id', '')),
    ]
    y = add_section("Installation Address", fields, y)
    
    # Section 2: Customer Details
    fields = [
        ("Name", f"{form_data.get('customer_first_name', '')} {form_data.get('customer_last_name', '')}"),
        ("Company", form_data.get('customer_company_name', '')),
        ("Address", f"{form_data.get('customer_street_number', '')} {form_data.get('customer_street_name', '')}, {form_data.get('customer_suburb', '')} {form_data.get('customer_state', '')} {form_data.get('customer_postcode', '')}"),
    ]
    y = add_section("Customer Details", fields, y)
    
    # Section 3: Installation Details
    fields = [
        ("Type", form_data.get('installation_type', '')),
        ("Description", form_data.get('installation_description', '')),
        ("Work Type", form_data.get('work_type', '')),
        ("Work Description", form_data.get('work_description', '')),
    ]
    y = add_section("Installation Details", fields, y)
    
    # Check if we need a new page
    if y < 200:
        c.showPage()
        y = height - 40
    
    # Section 4: Electrical Work Details
    fields = [
        ("Supply Type", form_data.get('supply_type', '')),
        ("Phases", form_data.get('supply_phases', '')),
        ("Voltage", form_data.get('supply_voltage', '')),
        ("Frequency", form_data.get('supply_frequency', '')),
        ("Earthing Type", form_data.get('earthing_type', '')),
        ("Main Switch Rating", form_data.get('main_switch_rating', '')),
        ("RCD Rating", form_data.get('rcd_rating', '')),
        ("Circuit Details", form_data.get('circuit_details', '')),
    ]
    y = add_section("Electrical Work Details", fields, y)
    
    # Section 5: Testing Results
    fields = [
        ("Insulation Test", form_data.get('insulation_test', '')),
        ("Earth Continuity", form_data.get('earth_continuity', '')),
        ("Polarity Test", form_data.get('polarity_test', '')),
        ("RCD Test", form_data.get('rcd_test', '')),
    ]
    y = add_section("Testing Results", fields, y)
    
    # Check if we need a new page
    if y < 200:
        c.showPage()
        y = height - 40
    
    # Section 6: Installer Details
    fields = [
        ("Name", f"{form_data.get('installer_first_name', '')} {form_data.get('installer_last_name', '')}"),
        ("License No", form_data.get('installer_license_no', '')),
        ("License Expiry", form_data.get('installer_license_expiry', '')),
        ("Mobile", form_data.get('installer_mobile_phone', '')),
        ("Address", f"{form_data.get('installer_street_number', '')} {form_data.get('installer_street_name', '')}, {form_data.get('installer_suburb', '')} {form_data.get('installer_state', '')} {form_data.get('installer_postcode', '')}"),
        ("Email", form_data.get('installer_email', '')),
        ("Office Phone", form_data.get('installer_office_phone', '')),
    ]
    y = add_section("Installer Details", fields, y)
    
    # Section 7: Tester Details
    fields = [
        ("Name", f"{form_data.get('tester_first_name', '')} {form_data.get('tester_last_name', '')}"),
        ("License No", form_data.get('tester_license_no', '')),
        ("License Expiry", form_data.get('tester_license_expiry', '')),
        ("Mobile", form_data.get('tester_mobile_phone', '')),
        ("Address", f"{form_data.get('tester_street_number', '')} {form_data.get('tester_street_name', '')}, {form_data.get('tester_suburb', '')} {form_data.get('tester_state', '')} {form_data.get('tester_postcode', '')}"),
        ("Email", form_data.get('tester_email', '')),
    ]
    y = add_section("Tester Details", fields, y)
    
    # Section 8: Dates
    fields = [
        ("Work Completed", form_data.get('date_work_completed', '')),
        ("Work Tested", form_data.get('date_work_tested', '')),
    ]
    y = add_section("Dates", fields, y)
    
    # Section 9: Signature
    y -= 20
    c.setFillColor(section_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Signature")
    y -= 18
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#000000'))
    c.drawString(50, y, f"Signed by: {form_data.get('signature', '')}")
    
    # Footer
    y = 40
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(label_color)
    c.drawString(40, y, "This document certifies that the electrical work described has been carried out in accordance with AS/NZS 3000.")
    
    # Save the PDF
    c.save()
    
    # Get the PDF data and encode as base64
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_data).decode('utf-8')


def get_pdf_filename(form_data):
    """Generate a filename for the PDF"""
    job_no = form_data.get('serial_no', 'Unknown')
    return f"CCEW_Form_Job_{job_no}.pdf"
