"""
CCEW PDF Generator - Overlay Approach using pypdf
Uses the official CCEW PDF as a template and overlays data on top
This guarantees an exact visual match to the official form
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
import base64
from datetime import datetime


def format_date_australian(date_str):
    """Convert date to Australian format DD/MM/YYYY"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str


def create_overlay_page(form_data, page_num):
    """
    Create a transparent overlay PDF page with just the data fields
    
    Args:
        form_data: Dictionary containing form values
        page_num: Page number (0, 1, or 2)
    
    Returns:
        BytesIO buffer containing the overlay PDF page
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Set default font
    font_size = 9
    can.setFont("Helvetica", font_size)
    can.setFillColor(colors.black)
    
    if page_num == 0:
        # ========== PAGE 1 - Installation Address & Customer Details ==========
        
        # Installation Address Section
        # Property Name (Y=590)
        if form_data.get('property_name'):
            can.drawString(70, height - 252, form_data['property_name'])
        
        # Floor/Unit/Street Number/Lot row (Y=567)
        if form_data.get('install_floor'):
            can.drawString(70, height - 275, form_data['install_floor'])
        if form_data.get('install_unit'):
            can.drawString(180, height - 275, form_data['install_unit'])
        if form_data.get('install_street_number'):
            can.drawString(280, height - 275, form_data['install_street_number'])
        if form_data.get('install_lot_rmb'):
            can.drawString(700, height - 275, form_data['install_lot_rmb'])
        
        # Street Name/Nearest Cross Street row (Y=544)
        if form_data.get('install_street_name'):
            can.drawString(70, height - 298, form_data['install_street_name'])
        if form_data.get('nearest_cross_street'):
            can.drawString(470, height - 298, form_data['nearest_cross_street'])
        
        # Suburb/State/Postcode row (Y=521)
        if form_data.get('install_suburb'):
            can.drawString(70, height - 321, form_data['install_suburb'])
        install_state = form_data.get('install_state', 'NSW')
        can.drawString(270, height - 321, install_state)
        if form_data.get('install_postcode'):
            can.drawString(540, height - 321, form_data['install_postcode'])
        
        # Pit/NMI/Meter/AEMO row (Y=495)
        if form_data.get('pit_pillar_pole_no'):
            can.drawString(70, height - 347, form_data['pit_pillar_pole_no'])
        if form_data.get('nmi'):
            can.drawString(280, height - 347, form_data['nmi'])
        if form_data.get('meter_no'):
            can.drawString(420, height - 347, form_data['meter_no'])
        if form_data.get('aemo_provider_id'):
            can.drawString(610, height - 347, form_data['aemo_provider_id'])
        
        # Customer Details Section
        # First/Last Name row (Y=447)
        if form_data.get('customer_first_name'):
            can.drawString(70, height - 395, form_data['customer_first_name'])
        if form_data.get('customer_last_name'):
            can.drawString(460, height - 395, form_data['customer_last_name'])
        
        # Company Name row (Y=417)
        if form_data.get('customer_company_name'):
            can.drawString(70, height - 425, form_data['customer_company_name'])
        
        # Floor/Unit/Street Number/Lot row (Y=397)
        if form_data.get('customer_floor'):
            can.drawString(70, height - 445, form_data['customer_floor'])
        if form_data.get('customer_unit'):
            can.drawString(180, height - 445, form_data['customer_unit'])
        if form_data.get('customer_street_number'):
            can.drawString(280, height - 445, form_data['customer_street_number'])
        if form_data.get('customer_lot_rmb'):
            can.drawString(700, height - 445, form_data['customer_lot_rmb'])
        
        # Street Name/Nearest Cross Street row (Y=374)
        if form_data.get('customer_street_name'):
            can.drawString(70, height - 468, form_data['customer_street_name'])
        if form_data.get('customer_nearest_cross_street'):
            can.drawString(470, height - 468, form_data['customer_nearest_cross_street'])
        
        # Suburb/State/Postcode row (Y=351)
        if form_data.get('customer_suburb'):
            can.drawString(70, height - 491, form_data['customer_suburb'])
        if form_data.get('customer_state'):
            can.drawString(270, height - 491, form_data['customer_state'])
        if form_data.get('customer_postcode'):
            can.drawString(540, height - 491, form_data['customer_postcode'])
        
        # Email/Office/Mobile row (Y=328)
        if form_data.get('customer_email'):
            can.drawString(70, height - 514, form_data['customer_email'])
        if form_data.get('customer_office_phone'):
            can.drawString(375, height - 514, form_data['customer_office_phone'])
        if form_data.get('customer_mobile_phone'):
            can.drawString(525, height - 514, form_data['customer_mobile_phone'])
        
        # Installation Details - Checkboxes (draw X in boxes)
        install_type = form_data.get('installation_type', 'residential').lower()
        if 'residential' in install_type:
            can.drawString(95, height - 540, "X")
        elif 'commercial' in install_type:
            can.drawString(200, height - 540, "X")
        
        work_type = form_data.get('work_type', '').lower()
        if 'new' in work_type:
            can.drawString(200, height - 565, "X")
        elif 'addition' in work_type or 'alteration' in work_type:
            can.drawString(95, height - 580, "X")
    
    elif page_num == 1:
        # ========== PAGE 2 - Equipment Details & Installer ==========
        
        # Equipment - Switchboard
        if form_data.get('equip_switchboard') == 'yes':
            can.drawString(95, height - 115, "X")
            
            if form_data.get('equip_switchboard_rating'):
                can.drawString(200, height - 115, form_data['equip_switchboard_rating'])
            
            if form_data.get('equip_switchboard_number'):
                can.drawString(350, height - 115, form_data['equip_switchboard_number'])
            
            if form_data.get('equip_switchboard_particulars'):
                can.drawString(450, height - 115, form_data['equip_switchboard_particulars'])
        
        # Meters Section
        if form_data.get('meter_1_i') == 'yes':
            can.drawString(95, height - 235, "X")
            
            if form_data.get('meter_1_number'):
                can.drawString(150, height - 235, form_data['meter_1_number'])
            
            if form_data.get('meter_1_dials'):
                can.drawString(250, height - 235, form_data['meter_1_dials'])
        
        # Load increase
        if form_data.get('load_increase'):
            can.drawString(300, height - 380, form_data['load_increase'])
        
        # Load within capacity
        if form_data.get('load_within_capacity', '').lower() == 'yes':
            can.drawString(430, height - 400, "X")
        else:
            can.drawString(480, height - 400, "X")
        
        # Work connected to supply
        if form_data.get('work_connected_supply', '').lower() == 'yes':
            can.drawString(430, height - 420, "X")
        else:
            can.drawString(480, height - 420, "X")
        
        # Installer Details
        if form_data.get('installer_first_name'):
            can.drawString(60, height - 495, form_data['installer_first_name'])
        
        if form_data.get('installer_last_name'):
            can.drawString(310, height - 495, form_data['installer_last_name'])
        
        if form_data.get('installer_street_number'):
            can.drawString(260, height - 541, form_data['installer_street_number'])
        
        if form_data.get('installer_street_name'):
            can.drawString(60, height - 564, form_data['installer_street_name'])
        
        if form_data.get('installer_suburb'):
            can.drawString(60, height - 587, form_data['installer_suburb'])
        
        if form_data.get('installer_state'):
            can.drawString(310, height - 587, form_data['installer_state'])
        
        if form_data.get('installer_postcode'):
            can.drawString(437, height - 587, form_data['installer_postcode'])
        
        if form_data.get('installer_email'):
            can.drawString(60, height - 610, form_data['installer_email'])
        
        if form_data.get('installer_office_phone'):
            can.drawString(310, height - 610, form_data['installer_office_phone'])
        
        if form_data.get('installer_license_no'):
            can.drawString(310, height - 656, form_data['installer_license_no'])
        
        if form_data.get('installer_license_expiry'):
            expiry_formatted = format_date_australian(form_data['installer_license_expiry'])
            can.drawString(450, height - 656, expiry_formatted)
    
    elif page_num == 2:
        # ========== PAGE 3 - Test Report & Tester Details ==========
        
        # Test checkboxes
        if form_data.get('test_earthing') == 'yes':
            can.drawString(95, height - 145, "X")
        
        if form_data.get('test_rcd') == 'yes':
            can.drawString(95, height - 160, "X")
        
        # Test completed date
        if form_data.get('test_date'):
            test_date_formatted = format_date_australian(form_data['test_date'])
            can.drawString(250, height - 265, test_date_formatted)
        
        # Tester Details
        if form_data.get('tester_first_name'):
            can.drawString(60, height - 340, form_data['tester_first_name'])
        
        if form_data.get('tester_last_name'):
            can.drawString(310, height - 340, form_data['tester_last_name'])
        
        if form_data.get('tester_street_number'):
            can.drawString(260, height - 386, form_data['tester_street_number'])
        
        if form_data.get('tester_street_name'):
            can.drawString(60, height - 409, form_data['tester_street_name'])
        
        if form_data.get('tester_suburb'):
            can.drawString(60, height - 432, form_data['tester_suburb'])
        
        if form_data.get('tester_state'):
            can.drawString(310, height - 432, form_data['tester_state'])
        
        if form_data.get('tester_postcode'):
            can.drawString(437, height - 432, form_data['tester_postcode'])
        
        if form_data.get('tester_email'):
            can.drawString(60, height - 455, form_data['tester_email'])
        
        if form_data.get('tester_license_no'):
            can.drawString(310, height - 524, form_data['tester_license_no'])
        
        if form_data.get('tester_license_expiry'):
            expiry_formatted = format_date_australian(form_data['tester_license_expiry'])
            can.drawString(450, height - 524, expiry_formatted)
        
        # Energy Provider
        if form_data.get('energy_provider'):
            can.drawString(100, height - 632, form_data['energy_provider'])
    
    can.save()
    packet.seek(0)
    return packet


def generate_ccew_pdf_overlay(form_data, template_pdf_path):
    """
    Generate filled CCEW PDF by overlaying data on official template
    
    Args:
        form_data: Dictionary containing all form field values
        template_pdf_path: Path to the official CCEW PDF template
    
    Returns:
        Base64 encoded PDF bytes
    """
    
    # Read the template PDF
    template_pdf = PdfReader(template_pdf_path)
    output_pdf = PdfWriter()
    
    # Process each page
    for page_num in range(len(template_pdf.pages)):
        # Get the template page
        template_page = template_pdf.pages[page_num]
        
        # Create overlay with data for this page
        overlay_buffer = create_overlay_page(form_data, page_num)
        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]
        
        # Merge overlay onto template
        template_page.merge_page(overlay_page)
        
        # Add to output
        output_pdf.add_page(template_page)
    
    # Write to bytes
    output_buffer = io.BytesIO()
    output_pdf.write(output_buffer)
    output_buffer.seek(0)
    
    # Return as base64
    pdf_bytes = output_buffer.getvalue()
    return base64.b64encode(pdf_bytes).decode('utf-8')


# Wrapper function for backward compatibility
def generate_ccew_pdf(form_data, template_pdf_path="CCEW_OFFICIAL_TEMPLATE.pdf"):
    """
    Backward compatible wrapper function
    """
    return generate_ccew_pdf_overlay(form_data, template_pdf_path)


def get_pdf_filename(job_number):
    """Generate PDF filename from job number"""
    return f"CCEW_Form_Job_{job_number}.pdf"
