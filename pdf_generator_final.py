"""
CCEW PDF Generator - Overlay Approach with CORRECTED Coordinates
Based on systematic testing with the official form
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
    Coordinates corrected based on testing: Y values need +150 adjustment
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    font_size = 9
    can.setFont("Helvetica", font_size)
    can.setFillColor(colors.black)
    
    if page_num == 0:
        # ========== PAGE 1 ==========
        
        # Serial Number (top right)
        if form_data.get('serial_no'):
            can.setFont("Helvetica-Bold", 9)
            can.drawString(485, 757, form_data['serial_no'])
            can.setFont("Helvetica", 9)
        
        # INSTALLATION ADDRESS SECTION
        # Adjusted Y coordinates: original + 150
        
        # Property Name - Y was 562, now 712
        if form_data.get('property_name'):
            can.drawString(70, 562, form_data['property_name'])
        
        # Floor/Unit/Street Number row - Y was 512, now 662
        if form_data.get('install_street_number'):
            can.drawString(210, 512, form_data['install_street_number'])
        
        # Street Name / Nearest Cross Street - Y was 467, now 617
        if form_data.get('install_street_name'):
            can.drawString(70, 467, form_data['install_street_name'])
        
        if form_data.get('nearest_cross_street'):
            can.drawString(320, 467, form_data['nearest_cross_street'])
        
        # Suburb / State / Postcode - Y was 417, now 567
        if form_data.get('install_suburb'):
            can.drawString(70, 417, form_data['install_suburb'])
        
        install_state = form_data.get('install_state', 'NSW')
        can.drawString(320, 417, install_state)
        
        if form_data.get('install_postcode'):
            can.drawString(440, 417, form_data['install_postcode'])
        
        # Pit/Pillar / NMI / Meter / AEMO - Y was ~350, now ~500
        if form_data.get('pit_pillar_pole_no'):
            can.drawString(70, 350, form_data['pit_pillar_pole_no'])
        
        if form_data.get('nmi'):
            can.drawString(190, 350, form_data['nmi'])
        
        if form_data.get('meter_no'):
            can.drawString(285, 350, form_data['meter_no'])
        
        if form_data.get('aemo_provider_id'):
            can.drawString(420, 350, form_data['aemo_provider_id'])
        
        # CUSTOMER DETAILS SECTION
        # First Name / Last Name - Y was 247, now ~397
        if form_data.get('customer_first_name'):
            can.drawString(70, 247, form_data['customer_first_name'])
        
        if form_data.get('customer_last_name'):
            can.drawString(320, 247, form_data['customer_last_name'])
        
        # Company Name - Y ~207, now ~357
        if form_data.get('customer_company_name'):
            can.drawString(70, 207, form_data['customer_company_name'])
        
        # Floor/Unit/Street Number - Y ~142, now ~292
        if form_data.get('customer_street_number'):
            can.drawString(210, 142, form_data['customer_street_number'])
        
        # Street Name / Nearest Cross - Y ~87, now ~237
        if form_data.get('customer_street_name'):
            can.drawString(70, 87, form_data['customer_street_name'])
        
        # Suburb / State / Postcode - Y ~32, now ~182
        if form_data.get('customer_suburb'):
            can.drawString(70, 32, form_data['customer_suburb'])
        
        if form_data.get('customer_state'):
            can.drawString(320, 32, form_data['customer_state'])
        
        if form_data.get('customer_postcode'):
            can.drawString(440, 32, form_data['customer_postcode'])
        
        # Email / Office / Mobile - below suburb row
        if form_data.get('customer_email'):
            can.drawString(70, -23, form_data['customer_email'])
        
        if form_data.get('customer_office_phone'):
            can.drawString(320, -23, form_data['customer_office_phone'])
        
        if form_data.get('customer_mobile_phone'):
            can.drawString(440, -23, form_data['customer_mobile_phone'])
        
        # Installation Details - Checkboxes
        install_type = form_data.get('installation_type', 'residential').lower()
        if 'residential' in install_type:
            can.drawString(70, -95, "X")
        elif 'commercial' in install_type:
            can.drawString(145, -95, "X")
        elif 'industrial' in install_type:
            can.drawString(220, -95, "X")
        elif 'rural' in install_type:
            can.drawString(295, -95, "X")
        elif 'mixed' in install_type:
            can.drawString(400, -95, "X")
        
        work_type = form_data.get('work_type', '').lower()
        if 'new' in work_type:
            can.drawString(145, -118, "X")
        elif 'addition' in work_type or 'alteration' in work_type:
            can.drawString(70, -133, "X")
    
    elif page_num == 1:
        # ========== PAGE 2 - Equipment & Installer ==========
        
        # Equipment - Switchboard
        if form_data.get('equip_switchboard') == 'yes':
            can.drawString(70, 729, "X")
            if form_data.get('equip_switchboard_rating'):
                can.drawString(145, 729, form_data['equip_switchboard_rating'])
            if form_data.get('equip_switchboard_number'):
                can.drawString(295, 729, form_data['equip_switchboard_number'])
            if form_data.get('equip_switchboard_particulars'):
                can.drawString(395, 729, form_data['equip_switchboard_particulars'])
        
        # Circuits
        if form_data.get('equip_circuits') == 'yes':
            can.drawString(70, 706, "X")
            if form_data.get('equip_circuits_rating'):
                can.drawString(145, 706, form_data['equip_circuits_rating'])
            if form_data.get('equip_circuits_number'):
                can.drawString(295, 706, form_data['equip_circuits_number'])
            if form_data.get('equip_circuits_particulars'):
                can.drawString(395, 706, form_data['equip_circuits_particulars'])
        
        # Meters
        if form_data.get('meter_1_i') == 'yes':
            can.drawString(70, 609, "X")
            if form_data.get('meter_1_number'):
                can.drawString(120, 609, form_data['meter_1_number'])
            if form_data.get('meter_1_dials'):
                can.drawString(220, 609, form_data['meter_1_dials'])
        
        # Load increase
        if form_data.get('load_increase'):
            can.drawString(250, 464, form_data['load_increase'])
        
        # Load within capacity
        if form_data.get('load_within_capacity', '').lower() == 'yes':
            can.drawString(380, 444, "X")
        else:
            can.drawString(420, 444, "X")
        
        # Work connected to supply
        if form_data.get('work_connected_supply', '').lower() == 'yes':
            can.drawString(380, 424, "X")
        else:
            can.drawString(420, 424, "X")
        
        # Installer Details
        if form_data.get('installer_first_name'):
            can.drawString(70, 349, form_data['installer_first_name'])
        
        if form_data.get('installer_last_name'):
            can.drawString(320, 349, form_data['installer_last_name'])
        
        if form_data.get('installer_street_number'):
            can.drawString(210, 303, form_data['installer_street_number'])
        
        if form_data.get('installer_street_name'):
            can.drawString(70, 280, form_data['installer_street_name'])
        
        if form_data.get('installer_suburb'):
            can.drawString(70, 257, form_data['installer_suburb'])
        
        if form_data.get('installer_state'):
            can.drawString(320, 257, form_data['installer_state'])
        
        if form_data.get('installer_postcode'):
            can.drawString(440, 257, form_data['installer_postcode'])
        
        if form_data.get('installer_email'):
            can.drawString(70, 234, form_data['installer_email'])
        
        if form_data.get('installer_office_phone'):
            can.drawString(320, 234, form_data['installer_office_phone'])
        
        if form_data.get('installer_license_no'):
            can.drawString(320, 188, form_data['installer_license_no'])
        
        if form_data.get('installer_license_expiry'):
            expiry_formatted = format_date_australian(form_data['installer_license_expiry'])
            can.drawString(445, 188, expiry_formatted)
    
    elif page_num == 2:
        # ========== PAGE 3 - Test Report & Tester ==========
        
        # Test checkboxes
        if form_data.get('test_earthing') == 'yes':
            can.drawString(70, 699, "X")
        
        if form_data.get('test_rcd') == 'yes':
            can.drawString(70, 684, "X")
        
        if form_data.get('test_insulation') == 'yes':
            can.drawString(70, 669, "X")
        
        if form_data.get('test_visual') == 'yes':
            can.drawString(70, 654, "X")
        
        if form_data.get('test_polarity') == 'yes':
            can.drawString(70, 639, "X")
        
        # Test date
        if form_data.get('test_date'):
            test_date_formatted = format_date_australian(form_data['test_date'])
            can.drawString(200, 579, test_date_formatted)
        
        # Tester Details
        if form_data.get('tester_first_name'):
            can.drawString(70, 504, form_data['tester_first_name'])
        
        if form_data.get('tester_last_name'):
            can.drawString(320, 504, form_data['tester_last_name'])
        
        if form_data.get('tester_street_number'):
            can.drawString(210, 458, form_data['tester_street_number'])
        
        if form_data.get('tester_street_name'):
            can.drawString(70, 435, form_data['tester_street_name'])
        
        if form_data.get('tester_suburb'):
            can.drawString(70, 412, form_data['tester_suburb'])
        
        if form_data.get('tester_state'):
            can.drawString(320, 412, form_data['tester_state'])
        
        if form_data.get('tester_postcode'):
            can.drawString(440, 412, form_data['tester_postcode'])
        
        if form_data.get('tester_email'):
            can.drawString(70, 389, form_data['tester_email'])
        
        if form_data.get('tester_license_no'):
            can.drawString(320, 320, form_data['tester_license_no'])
        
        if form_data.get('tester_license_expiry'):
            expiry_formatted = format_date_australian(form_data['tester_license_expiry'])
            can.drawString(445, 320, expiry_formatted)
        
        # Energy Provider
        if form_data.get('energy_provider'):
            can.drawString(100, 212, form_data['energy_provider'])
    
    can.save()
    packet.seek(0)
    return packet


def generate_ccew_pdf(form_data):
    """Generate filled CCEW PDF by overlaying data on official template"""
    
    template_pdf_path = os.path.join(os.path.dirname(__file__), 'CCEW_OFFICIAL_TEMPLATE.pdf')
    
    if not os.path.exists(template_pdf_path):
        raise FileNotFoundError(f"Official CCEW template not found at: {template_pdf_path}")
    
    template_pdf = PdfReader(template_pdf_path)
    output_pdf = PdfWriter()
    
    for page_num in range(len(template_pdf.pages)):
        template_page = template_pdf.pages[page_num]
        overlay_buffer = create_overlay_page(form_data, page_num)
        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]
        template_page.merge_page(overlay_page)
        output_pdf.add_page(template_page)
    
    output_buffer = io.BytesIO()
    output_pdf.write(output_buffer)
    output_buffer.seek(0)
    
    pdf_bytes = output_buffer.getvalue()
    return base64.b64encode(pdf_bytes).decode('utf-8')


def get_pdf_filename(form_data):
    """Generate PDF filename"""
    job_no = form_data.get('serial_no', 'UNKNOWN')
    return f"CCEW_Form_Job_{job_no}.pdf"
