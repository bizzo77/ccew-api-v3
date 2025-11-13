"""
CCEW PDF Generator - Overlay Approach
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
import os


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
        
        # Serial Number (top right)
        if form_data.get('serial_no'):
            can.setFont("Helvetica-Bold", 9)
            can.drawString(485, height - 85, form_data['serial_no'])
            can.setFont("Helvetica", 9)
        
        # Installation Address Section
        # Property Name field - inside white box at Y~191 from top
        if form_data.get('property_name'):
            can.drawString(68, height - 280, form_data['property_name'])
        
        # Floor, Unit, Street Number, Lot/RMB row - Y~241 from top
        if form_data.get('install_street_number'):
            can.drawString(470, height - 330, form_data['install_street_number'])
        
        # Street Name and Nearest Cross Street - Y~291 from top  
        if form_data.get('install_street_name'):
            can.drawString(68, height - 375, form_data['install_street_name'])
        
        if form_data.get('nearest_cross_street'):
            can.drawString(470, height - 375, form_data['nearest_cross_street'])
        
        # Suburb, State, Postcode - Y~341 from top
        if form_data.get('install_suburb'):
            can.drawString(68, height - 425, form_data['install_suburb'])
        
        install_state = form_data.get('install_state', 'NSW')
        can.drawString(315, height - 425, install_state)
        
        if form_data.get('install_postcode'):
            can.drawString(520, height - 425, form_data['install_postcode'])
        
        # Pit/Pillar, NMI, Meter No, AEMO - Y~391 from top
        if form_data.get('pit_pillar_pole_no'):
            can.drawString(68, height - 495, form_data['pit_pillar_pole_no'])
        
        if form_data.get('nmi'):
            can.drawString(190, height - 495, form_data['nmi'])
        
        if form_data.get('meter_no'):
            can.drawString(300, height - 495, form_data['meter_no'])
        
        if form_data.get('aemo_provider_id'):
            can.drawString(430, height - 495, form_data['aemo_provider_id'])
        
        # Customer Details Section - starts at Y~391 from top
        # First Name, Last Name - Y~441 from top
        if form_data.get('customer_first_name'):
            can.drawString(68, height - 595, form_data['customer_first_name'])
        
        if form_data.get('customer_last_name'):
            can.drawString(470, height - 595, form_data['customer_last_name'])
        
        # Company Name - Y~491 from top
        if form_data.get('customer_company_name'):
            can.drawString(68, height - 635, form_data['customer_company_name'])
        
        # Floor, Unit, Street Number, Lot/RMB - Y~541 from top
        if form_data.get('customer_street_number'):
            can.drawString(470, height - 700, form_data['customer_street_number'])
        
        # Street Name, Nearest Cross Street - Y~591 from top
        if form_data.get('customer_street_name'):
            can.drawString(68, height - 755, form_data['customer_street_name'])
        
        # Suburb, State, Postcode - Y~641 from top
        if form_data.get('customer_suburb'):
            can.drawString(68, height - 810, form_data['customer_suburb'])
        
        if form_data.get('customer_state'):
            can.drawString(470, height - 810, form_data['customer_state'])
        
        if form_data.get('customer_postcode'):
            can.drawString(520, height - 810, form_data['customer_postcode'])
        
        # Email, Office No, Mobile No - Y~691 from top
        if form_data.get('customer_email'):
            can.drawString(68, height - 865, form_data['customer_email'])
        
        if form_data.get('customer_office_phone'):
            can.drawString(315, height - 865, form_data['customer_office_phone'])
        
        if form_data.get('customer_mobile_phone'):
            can.drawString(520, height - 865, form_data['customer_mobile_phone'])
        
        # Installation Details - Checkboxes (draw X in boxes)
        install_type = form_data.get('installation_type', 'residential').lower()
        if 'residential' in install_type:
            can.drawString(70, height - 537, "X")
        elif 'commercial' in install_type:
            can.drawString(145, height - 537, "X")
        elif 'industrial' in install_type:
            can.drawString(220, height - 537, "X")
        elif 'rural' in install_type:
            can.drawString(295, height - 537, "X")
        elif 'mixed' in install_type:
            can.drawString(400, height - 537, "X")
        
        work_type = form_data.get('work_type', '').lower()
        if 'new' in work_type:
            can.drawString(145, height - 560, "X")
        elif 'addition' in work_type or 'alteration' in work_type:
            can.drawString(70, height - 575, "X")
        elif 'meter' in work_type and 'installed' in work_type:
            can.drawString(295, height - 560, "X")
        elif 'network' in work_type:
            can.drawString(450, height - 560, "X")
    
    elif page_num == 1:
        # ========== PAGE 2 - Equipment Details & Installer ==========
        
        # Equipment - Switchboard
        if form_data.get('equip_switchboard') == 'yes':
            can.drawString(70, height - 113, "X")
            
            if form_data.get('equip_switchboard_rating'):
                can.drawString(145, height - 113, form_data['equip_switchboard_rating'])
            
            if form_data.get('equip_switchboard_number'):
                can.drawString(295, height - 113, form_data['equip_switchboard_number'])
            
            if form_data.get('equip_switchboard_particulars'):
                can.drawString(395, height - 113, form_data['equip_switchboard_particulars'])
        
        # Circuits
        if form_data.get('equip_circuits') == 'yes':
            can.drawString(70, height - 136, "X")
            
            if form_data.get('equip_circuits_rating'):
                can.drawString(145, height - 136, form_data['equip_circuits_rating'])
            
            if form_data.get('equip_circuits_number'):
                can.drawString(295, height - 136, form_data['equip_circuits_number'])
            
            if form_data.get('equip_circuits_particulars'):
                can.drawString(395, height - 136, form_data['equip_circuits_particulars'])
        
        # Meters Section
        if form_data.get('meter_1_i') == 'yes':
            can.drawString(70, height - 233, "X")
            
            if form_data.get('meter_1_number'):
                can.drawString(120, height - 233, form_data['meter_1_number'])
            
            if form_data.get('meter_1_dials'):
                can.drawString(220, height - 233, form_data['meter_1_dials'])
        
        # Load increase
        if form_data.get('load_increase'):
            can.drawString(250, height - 378, form_data['load_increase'])
        
        # Load within capacity
        if form_data.get('load_within_capacity', '').lower() == 'yes':
            can.drawString(380, height - 398, "X")
        else:
            can.drawString(420, height - 398, "X")
        
        # Work connected to supply
        if form_data.get('work_connected_supply', '').lower() == 'yes':
            can.drawString(380, height - 418, "X")
        else:
            can.drawString(420, height - 418, "X")
        
        # Installer Details
        if form_data.get('installer_first_name'):
            can.drawString(65, height - 493, form_data['installer_first_name'])
        
        if form_data.get('installer_last_name'):
            can.drawString(315, height - 493, form_data['installer_last_name'])
        
        if form_data.get('installer_street_number'):
            can.drawString(220, height - 539, form_data['installer_street_number'])
        
        if form_data.get('installer_street_name'):
            can.drawString(65, height - 562, form_data['installer_street_name'])
        
        if form_data.get('installer_suburb'):
            can.drawString(65, height - 585, form_data['installer_suburb'])
        
        if form_data.get('installer_state'):
            can.drawString(315, height - 585, form_data['installer_state'])
        
        if form_data.get('installer_postcode'):
            can.drawString(445, height - 585, form_data['installer_postcode'])
        
        if form_data.get('installer_email'):
            can.drawString(65, height - 608, form_data['installer_email'])
        
        if form_data.get('installer_office_phone'):
            can.drawString(315, height - 608, form_data['installer_office_phone'])
        
        if form_data.get('installer_license_no'):
            can.drawString(315, height - 654, form_data['installer_license_no'])
        
        if form_data.get('installer_license_expiry'):
            expiry_formatted = format_date_australian(form_data['installer_license_expiry'])
            can.drawString(445, height - 654, expiry_formatted)
    
    elif page_num == 2:
        # ========== PAGE 3 - Test Report & Tester Details ==========
        
        # Test checkboxes
        if form_data.get('test_earthing') == 'yes':
            can.drawString(70, height - 143, "X")
        
        if form_data.get('test_rcd') == 'yes':
            can.drawString(70, height - 158, "X")
        
        if form_data.get('test_insulation') == 'yes':
            can.drawString(70, height - 173, "X")
        
        if form_data.get('test_visual') == 'yes':
            can.drawString(70, height - 188, "X")
        
        if form_data.get('test_polarity') == 'yes':
            can.drawString(70, height - 203, "X")
        
        # Test completed date
        if form_data.get('test_date'):
            test_date_formatted = format_date_australian(form_data['test_date'])
            can.drawString(200, height - 263, test_date_formatted)
        
        # Tester Details
        if form_data.get('tester_first_name'):
            can.drawString(65, height - 338, form_data['tester_first_name'])
        
        if form_data.get('tester_last_name'):
            can.drawString(315, height - 338, form_data['tester_last_name'])
        
        if form_data.get('tester_street_number'):
            can.drawString(220, height - 384, form_data['tester_street_number'])
        
        if form_data.get('tester_street_name'):
            can.drawString(65, height - 407, form_data['tester_street_name'])
        
        if form_data.get('tester_suburb'):
            can.drawString(65, height - 430, form_data['tester_suburb'])
        
        if form_data.get('tester_state'):
            can.drawString(315, height - 430, form_data['tester_state'])
        
        if form_data.get('tester_postcode'):
            can.drawString(445, height - 430, form_data['tester_postcode'])
        
        if form_data.get('tester_email'):
            can.drawString(65, height - 453, form_data['tester_email'])
        
        if form_data.get('tester_license_no'):
            can.drawString(315, height - 522, form_data['tester_license_no'])
        
        if form_data.get('tester_license_expiry'):
            expiry_formatted = format_date_australian(form_data['tester_license_expiry'])
            can.drawString(445, height - 522, expiry_formatted)
        
        # Energy Provider
        if form_data.get('energy_provider'):
            can.drawString(100, height - 630, form_data['energy_provider'])
    
    can.save()
    packet.seek(0)
    return packet


def generate_ccew_pdf(form_data):
    """
    Generate filled CCEW PDF by overlaying data on official template
    
    Args:
        form_data: Dictionary containing all form field values
    
    Returns:
        Base64 encoded PDF bytes
    """
    
    # Path to the official CCEW PDF template
    template_pdf_path = os.path.join(os.path.dirname(__file__), 'CCEW_OFFICIAL_TEMPLATE.pdf')
    
    if not os.path.exists(template_pdf_path):
        raise FileNotFoundError(f"Official CCEW template not found at: {template_pdf_path}")
    
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


def get_pdf_filename(form_data):
    """Generate PDF filename"""
    job_no = form_data.get('serial_no', 'UNKNOWN')
    return f"CCEW_Form_Job_{job_no}.pdf"
