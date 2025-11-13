"""
CCEW PDF Generator - Overlay Approach with PRECISELY MEASURED Coordinates
Coordinates measured from POSITION_REFERENCE.pdf grid
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
    """Create overlay with data fields at precisely measured positions"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    font_size = 9
    can.setFont("Helvetica", font_size)
    can.setFillColor(colors.black)
    
    if page_num == 0:
        # ========== PAGE 1 - Installation Address & Customer Details ==========
        # All coordinates precisely measured from position reference grid
        
        # Serial Number (top right)
        if form_data.get('serial_no'):
            can.setFont("Helvetica-Bold", 9)
            can.drawString(760, 757, form_data['serial_no'])
            can.setFont("Helvetica", 9)
        
        # INSTALLATION ADDRESS SECTION
        # Property Name - X=70, Y=650
        if form_data.get('property_name'):
            can.drawString(70, 650, form_data['property_name'])
        
        # Floor/Unit/Street Number/Lot row - Y=605
        if form_data.get('install_floor'):
            can.drawString(70, 605, form_data.get('install_floor', ''))
        
        if form_data.get('install_unit'):
            can.drawString(180, 605, form_data.get('install_unit', ''))
        
        if form_data.get('install_street_number'):
            can.drawString(460, 605, form_data['install_street_number'])
        
        if form_data.get('install_lot'):
            can.drawString(700, 605, form_data.get('install_lot', ''))
        
        # Street Name / Nearest Cross Street - Y=560
        if form_data.get('install_street_name'):
            can.drawString(70, 560, form_data['install_street_name'])
        
        if form_data.get('nearest_cross_street'):
            can.drawString(470, 560, form_data['nearest_cross_street'])
        
        # Suburb / State / Postcode - Y=515
        if form_data.get('install_suburb'):
            can.drawString(70, 515, form_data['install_suburb'])
        
        if form_data.get('install_state'):
            can.drawString(470, 515, form_data.get('install_state', 'NSW'))
        
        if form_data.get('install_postcode'):
            can.drawString(730, 515, form_data['install_postcode'])
        
        # Pit/Pillar / NMI / Meter / AEMO - Y=470
        if form_data.get('pit_pillar_pole_no'):
            can.drawString(70, 470, form_data['pit_pillar_pole_no'])
        
        if form_data.get('nmi'):
            can.drawString(240, 470, form_data['nmi'])
        
        if form_data.get('meter_no'):
            can.drawString(420, 470, form_data['meter_no'])
        
        if form_data.get('aemo_provider_id'):
            can.drawString(600, 470, form_data['aemo_provider_id'])
        
        # CUSTOMER DETAILS SECTION
        # First Name / Last Name - Y=450
        if form_data.get('customer_first_name'):
            can.drawString(70, 450, form_data['customer_first_name'])
        
        if form_data.get('customer_last_name'):
            can.drawString(470, 450, form_data['customer_last_name'])
        
        # Company Name - Y=405
        if form_data.get('customer_company_name'):
            can.drawString(70, 405, form_data['customer_company_name'])
        
        # Floor/Unit/Street Number/Lot - Y=360
        if form_data.get('customer_floor'):
            can.drawString(70, 360, form_data.get('customer_floor', ''))
        
        if form_data.get('customer_unit'):
            can.drawString(180, 360, form_data.get('customer_unit', ''))
        
        if form_data.get('customer_street_number'):
            can.drawString(460, 360, form_data['customer_street_number'])
        
        if form_data.get('customer_lot'):
            can.drawString(700, 360, form_data.get('customer_lot', ''))
        
        # Street Name / Nearest Cross - Y=315
        if form_data.get('customer_street_name'):
            can.drawString(70, 315, form_data['customer_street_name'])
        
        if form_data.get('customer_cross_street'):
            can.drawString(470, 315, form_data.get('customer_cross_street', ''))
        
        # Suburb / State / Postcode - Y=270
        if form_data.get('customer_suburb'):
            can.drawString(70, 270, form_data['customer_suburb'])
        
        if form_data.get('customer_state'):
            can.drawString(470, 270, form_data['customer_state'])
        
        if form_data.get('customer_postcode'):
            can.drawString(730, 270, form_data['customer_postcode'])
        
        # Email / Office / Mobile - Y=225
        if form_data.get('customer_email'):
            can.drawString(70, 225, form_data['customer_email'])
        
        if form_data.get('customer_office_phone'):
            can.drawString(580, 225, form_data['customer_office_phone'])
        
        if form_data.get('customer_mobile_phone'):
            can.drawString(720, 225, form_data['customer_mobile_phone'])
        
        # INSTALLATION DETAILS SECTION
        # Type of Installation checkboxes - Y=180
        install_type = form_data.get('installation_type', 'residential').lower()
        checkbox_y = 180
        if 'residential' in install_type:
            can.drawString(85, checkbox_y, "X")
        elif 'commercial' in install_type:
            can.drawString(195, checkbox_y, "X")
        elif 'industrial' in install_type:
            can.drawString(305, checkbox_y, "X")
        elif 'rural' in install_type:
            can.drawString(415, checkbox_y, "X")
        elif 'mixed' in install_type:
            can.drawString(550, checkbox_y, "X")
        
        # Work carried out checkboxes - Y=155, 140, 125
        work_type = form_data.get('work_type', '').lower()
        if 'new' in work_type:
            can.drawString(245, 155, "X")
        elif 'installed meter' in work_type:
            can.drawString(445, 155, "X")
        elif 'network' in work_type:
            can.drawString(680, 155, "X")
        elif 'addition' in work_type or 'alteration' in work_type:
            can.drawString(85, 140, "X")
        elif 'advanced meter' in work_type:
            can.drawString(445, 140, "X")
        elif 'ev' in work_type:
            can.drawString(680, 140, "X")
        elif 're-inspection' in work_type:
            can.drawString(85, 125, "X")
            if form_data.get('non_compliance_no'):
                can.drawString(640, 125, form_data['non_compliance_no'])
        
        # Special Conditions checkboxes - Y=95, 80
        if form_data.get('over_100_amps') == 'yes':
            can.drawString(245, 95, "X")
        if form_data.get('hazardous_area') == 'yes':
            can.drawString(445, 95, "X")
        if form_data.get('off_grid') == 'yes':
            can.drawString(680, 95, "X")
        if form_data.get('high_voltage') == 'yes':
            can.drawString(245, 80, "X")
        if form_data.get('unmetered_supply') == 'yes':
            can.drawString(445, 80, "X")
        if form_data.get('secondary_power') == 'yes':
            can.drawString(680, 80, "X")
    
    elif page_num == 1:
        # ========== PAGE 2 - Equipment & Installer ==========
        
        # Equipment - Switchboard - Y=729
        if form_data.get('equip_switchboard') == 'yes':
            can.drawString(70, 729, "X")
            if form_data.get('equip_switchboard_rating'):
                can.drawString(145, 729, form_data['equip_switchboard_rating'])
            if form_data.get('equip_switchboard_number'):
                can.drawString(295, 729, form_data['equip_switchboard_number'])
            if form_data.get('equip_switchboard_particulars'):
                can.drawString(395, 729, form_data['equip_switchboard_particulars'])
        
        # Circuits - Y=706
        if form_data.get('equip_circuits') == 'yes':
            can.drawString(70, 706, "X")
            if form_data.get('equip_circuits_rating'):
                can.drawString(145, 706, form_data['equip_circuits_rating'])
            if form_data.get('equip_circuits_number'):
                can.drawString(295, 706, form_data['equip_circuits_number'])
            if form_data.get('equip_circuits_particulars'):
                can.drawString(395, 706, form_data['equip_circuits_particulars'])
        
        # Meters - Y=609
        if form_data.get('meter_1_i') == 'yes':
            can.drawString(70, 609, "X")
            if form_data.get('meter_1_number'):
                can.drawString(120, 609, form_data['meter_1_number'])
            if form_data.get('meter_1_dials'):
                can.drawString(220, 609, form_data['meter_1_dials'])
        
        # Load increase - Y=464
        if form_data.get('load_increase'):
            can.drawString(250, 464, form_data['load_increase'])
        
        # Load within capacity - Y=444
        if form_data.get('load_within_capacity', '').lower() == 'yes':
            can.drawString(380, 444, "X")
        else:
            can.drawString(420, 444, "X")
        
        # Work connected to supply - Y=424
        if form_data.get('work_connected_supply', '').lower() == 'yes':
            can.drawString(380, 424, "X")
        else:
            can.drawString(420, 424, "X")
        
        # Installer Details - Y=349
        if form_data.get('installer_first_name'):
            can.drawString(70, 349, form_data['installer_first_name'])
        
        if form_data.get('installer_last_name'):
            can.drawString(470, 349, form_data['installer_last_name'])
        
        # Installer address - Y=303
        if form_data.get('installer_street_number'):
            can.drawString(460, 303, form_data['installer_street_number'])
        
        # Installer street - Y=280
        if form_data.get('installer_street_name'):
            can.drawString(70, 280, form_data['installer_street_name'])
        
        # Installer suburb/state/postcode - Y=257
        if form_data.get('installer_suburb'):
            can.drawString(70, 257, form_data['installer_suburb'])
        
        if form_data.get('installer_state'):
            can.drawString(470, 257, form_data['installer_state'])
        
        if form_data.get('installer_postcode'):
            can.drawString(730, 257, form_data['installer_postcode'])
        
        # Installer email/phone - Y=234
        if form_data.get('installer_email'):
            can.drawString(70, 234, form_data['installer_email'])
        
        if form_data.get('installer_office_phone'):
            can.drawString(580, 234, form_data['installer_office_phone'])
        
        # Installer license - Y=188
        if form_data.get('installer_license_no'):
            can.drawString(470, 188, form_data['installer_license_no'])
        
        if form_data.get('installer_license_expiry'):
            expiry_formatted = format_date_australian(form_data['installer_license_expiry'])
            can.drawString(680, 188, expiry_formatted)
    
    elif page_num == 2:
        # ========== PAGE 3 - Test Report & Tester ==========
        
        # Test checkboxes - starting Y=699
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
        
        # Test date - Y=579
        if form_data.get('test_date'):
            test_date_formatted = format_date_australian(form_data['test_date'])
            can.drawString(200, 579, test_date_formatted)
        
        # Tester Details - Y=504
        if form_data.get('tester_first_name'):
            can.drawString(70, 504, form_data['tester_first_name'])
        
        if form_data.get('tester_last_name'):
            can.drawString(470, 504, form_data['tester_last_name'])
        
        # Tester address - Y=458
        if form_data.get('tester_street_number'):
            can.drawString(460, 458, form_data['tester_street_number'])
        
        # Tester street - Y=435
        if form_data.get('tester_street_name'):
            can.drawString(70, 435, form_data['tester_street_name'])
        
        # Tester suburb/state/postcode - Y=412
        if form_data.get('tester_suburb'):
            can.drawString(70, 412, form_data['tester_suburb'])
        
        if form_data.get('tester_state'):
            can.drawString(470, 412, form_data['tester_state'])
        
        if form_data.get('tester_postcode'):
            can.drawString(730, 412, form_data['tester_postcode'])
        
        # Tester email - Y=389
        if form_data.get('tester_email'):
            can.drawString(70, 389, form_data['tester_email'])
        
        # Tester license - Y=320
        if form_data.get('tester_license_no'):
            can.drawString(470, 320, form_data['tester_license_no'])
        
        if form_data.get('tester_license_expiry'):
            expiry_formatted = format_date_australian(form_data['tester_license_expiry'])
            can.drawString(680, 320, expiry_formatted)
        
        # Energy Provider - Y=212
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
