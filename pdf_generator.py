"""
PDF Generator for CCEW Forms - Matching Official Layout Exactly
Generates a PDF that matches the official NSW CCEW form with green backgrounds and white labels
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
import io
import base64
from datetime import datetime


# Colors matching official form
HEADER_GREEN = HexColor('#8DB04C')
LABEL_GREEN = HexColor('#8DB04C')
FIELD_BORDER = HexColor('#CCCCCC')
TEXT_BLACK = black


def format_date_australian(date_str):
    """Convert date to Australian format DD/MM/YYYY"""
    if not date_str:
        return ''
    try:
        # Try parsing ISO format (YYYY-MM-DD)
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        # If already in correct format or invalid, return as is
        return date_str


def draw_checkbox(c, x, y, size=3*mm, checked=False):
    """Draw a checkbox at the specified position"""
    c.setStrokeColor(black)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, stroke=1, fill=0)
    if checked:
        # Draw an X
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.line(x, y, x + size, y + size)
        c.line(x + size, y, x, y + size)


def draw_label_row(c, y, labels_and_widths, row_height=6*mm):
    """
    Draw a row of labels with green background
    labels_and_widths: list of tuples [(label, x_position, width), ...]
    Returns: y position after the row
    """
    x_start = 20*mm
    total_width = 170*mm
    
    # Draw green background for entire row
    c.setFillColor(LABEL_GREEN)
    c.setStrokeColor(black)
    c.rect(x_start, y, total_width, row_height, stroke=1, fill=1)
    
    # Draw labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    
    for label, x_pos, width in labels_and_widths:
        c.drawString(x_pos, y + 1.5*mm, label)
        
    return y - row_height


def draw_field_box(c, x, y, width, height, value='', font_size=9):
    """Draw a field box with optional value"""
    # Draw border
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=1)
    
    # Draw value if provided
    if value:
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica", font_size)
        c.drawString(x + 2*mm, y + 1.5*mm, str(value))


def draw_green_header(c, y, text, width=170*mm):
    """Draw a green header section"""
    x = 20*mm
    height = 7*mm
    
    c.setFillColor(HEADER_GREEN)
    c.setStrokeColor(black)
    c.rect(x, y, width, height, stroke=1, fill=1)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2*mm, y + 2*mm, text)
    
    return y - height


def get_pdf_filename(form_data):
    """Generate PDF filename"""
    job_no = form_data.get('serial_no', 'UNKNOWN')
    return f"CCEW_Form_Job_{job_no}.pdf"


def generate_ccew_pdf(form_data):
    """
    Generate a PDF document matching the official CCEW form exactly
    Returns: base64 encoded PDF string
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # ========== PAGE 1 ==========
    y = height - 30*mm
    
    # Header - NSW Fair Trading logo area
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor('#C41E3A'))  # NSW red
    c.drawString(20*mm, y, "NSW")
    c.setFillColor(black)
    c.drawString(35*mm, y, "Fair Trading")
    
    # Serial No
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150*mm, y, "*Serial No:")
    draw_field_box(c, 170*mm, y - 3*mm, 20*mm, 5*mm, form_data.get('serial_no', ''))
    
    # Title
    y -= 10*mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, y, "Online Certificate Compliance Electrical Work (CCEW)")
    
    y -= 5*mm
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, y, "Any field marked with an * is mandatory")
    
    # SECTION 1: INSTALLATION ADDRESS
    y -= 10*mm
    y = draw_green_header(c, y, "INSTALLATION ADDRESS")
    y -= 3*mm
    
    # Property Name label row
    y = draw_label_row(c, y, [("Property Name", 21*mm, 170*mm)])
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, form_data.get('property_name', ''))
    y -= 5*mm
    
    # Floor, Unit, Street Number, Lot/RMB label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Floor", 21*mm, 25*mm),
        ("Unit", 49*mm, 25*mm),
        ("*Street Number", 77*mm, 30*mm),
        ("&/or", 110*mm, 15*mm),
        ("Lot/RMB", 129*mm, 61*mm)
    ])
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')  # Floor
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')  # Unit
    draw_field_box(c, 76*mm, y, 30*mm, 5*mm, form_data.get('install_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')  # Lot/RMB
    y -= 5*mm
    
    # Street Name, Nearest Cross Street label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Street Name", 21*mm, 85*mm),
        ("Nearest Cross Street", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('install_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, form_data.get('nearest_cross_street', ''))
    y -= 5*mm
    
    # Suburb, State, Post Code label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Suburb", 21*mm, 85*mm),
        ("*State", 109*mm, 40*mm),
        ("*Post Code", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('install_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('install_state', 'NSW'))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('install_postcode', ''))
    y -= 5*mm
    
    # Pit/Pillar, NMI, Meter No, AEMO label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Pit/Pillar/Pole No.", 21*mm, 40*mm),
        ("NMI", 63*mm, 32*mm),
        ("Meter No.", 98*mm, 32*mm),
        ("AEMO Metering Provider I.D.", 133*mm, 57*mm)
    ])
    draw_field_box(c, 20*mm, y, 40*mm, 5*mm, form_data.get('pit_pillar_pole_no', ''))
    draw_field_box(c, 62*mm, y, 32*mm, 5*mm, form_data.get('nmi', ''))
    draw_field_box(c, 97*mm, y, 32*mm, 5*mm, form_data.get('meter_no', ''))
    draw_field_box(c, 132*mm, y, 58*mm, 5*mm, form_data.get('aemo_provider_id', ''))
    y -= 5*mm
    
    # SECTION 2: CUSTOMER DETAILS
    y -= 8*mm
    y = draw_green_header(c, y, "CUSTOMER DETAILS")
    y -= 3*mm
    
    # First Name, Last Name label row
    y = draw_label_row(c, y, [
        ("*First Name", 21*mm, 85*mm),
        ("*Last Name", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_first_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, form_data.get('customer_last_name', ''))
    y -= 5*mm
    
    # Company Name label row
    y -= 3*mm
    y = draw_label_row(c, y, [("Company Name", 21*mm, 170*mm)])
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, form_data.get('customer_company_name', ''))
    y -= 5*mm
    
    # Floor, Unit, Street Number, Lot/RMB label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Floor", 21*mm, 25*mm),
        ("Unit", 49*mm, 25*mm),
        ("*Street Number", 77*mm, 30*mm),
        ("&/or", 110*mm, 15*mm),
        ("Lot/RMB", 129*mm, 61*mm)
    ])
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')  # Floor
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')  # Unit
    draw_field_box(c, 76*mm, y, 30*mm, 5*mm, form_data.get('customer_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')  # Lot/RMB
    y -= 5*mm
    
    # Street Name, Nearest Cross Street label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Street Name", 21*mm, 85*mm),
        ("Nearest Cross Street", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')  # Nearest Cross Street
    y -= 5*mm
    
    # Suburb, State, Post Code label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Suburb", 21*mm, 85*mm),
        ("*State", 109*mm, 40*mm),
        ("*Post Code", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('customer_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('customer_postcode', ''))
    y -= 5*mm
    
    # Email, Office No, Mobile No label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Email", 21*mm, 85*mm),
        ("Office No.", 109*mm, 40*mm),
        ("Mobile No.", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_email', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('customer_office_phone', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('customer_mobile_phone', ''))
    y -= 5*mm
    
    # SECTION 3: INSTALLATION DETAILS
    y -= 8*mm
    y = draw_green_header(c, y, "INSTALLATION DETAILS")
    y -= 5*mm
    
    # Type of Installation
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "*Type of Installation")
    y -= 5*mm
    
    inst_type = form_data.get('installation_type', '')
    draw_checkbox(c, 25*mm, y, checked=(inst_type == 'Residential'))
    c.setFont("Helvetica", 8)
    c.drawString(30*mm, y + 0.5*mm, "Residential")
    
    draw_checkbox(c, 55*mm, y, checked=(inst_type == 'Commercial'))
    c.drawString(60*mm, y + 0.5*mm, "Commercial")
    
    draw_checkbox(c, 90*mm, y, checked=(inst_type == 'Industrial'))
    c.drawString(95*mm, y + 0.5*mm, "Industrial")
    
    draw_checkbox(c, 120*mm, y, checked=(inst_type == 'Rural'))
    c.drawString(125*mm, y + 0.5*mm, "Rural")
    
    draw_checkbox(c, 145*mm, y, checked=(inst_type == 'Mixed Development'))
    c.drawString(150*mm, y + 0.5*mm, "Mixed Development")
    
    # Work carried out
    y -= 8*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(21*mm, y, "*Work carried out")
    y -= 5*mm
    
    # Work checkboxes - row 1
    draw_checkbox(c, 60*mm, y, checked=form_data.get('work_new_work') == 'yes')
    c.setFont("Helvetica", 8)
    c.drawString(65*mm, y + 0.5*mm, "New Work")
    
    draw_checkbox(c, 100*mm, y, checked=form_data.get('work_installed_meter') == 'yes')
    c.drawString(105*mm, y + 0.5*mm, "Installed Meter")
    
    draw_checkbox(c, 145*mm, y, checked=form_data.get('work_network_connection') == 'yes')
    c.drawString(150*mm, y + 0.5*mm, "Network connection")
    
    y -= 5*mm
    draw_checkbox(c, 25*mm, y, checked=form_data.get('work_addition_alteration') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Addition/alteration to existing")
    
    draw_checkbox(c, 100*mm, y, checked=form_data.get('work_advanced_meter') == 'yes')
    c.drawString(105*mm, y + 0.5*mm, "Install Advanced Meter")
    
    draw_checkbox(c, 145*mm, y, checked=form_data.get('work_ev_connection') == 'yes')
    c.drawString(150*mm, y + 0.5*mm, "EV Connection")
    
    y -= 5*mm
    draw_checkbox(c, 25*mm, y, checked=form_data.get('work_reinspection') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Re-inspection of non-compliant work")
    
    c.drawString(100*mm, y + 0.5*mm, "Non-Compliance No.")
    draw_field_box(c, 135*mm, y - 1*mm, 55*mm, 5*mm, form_data.get('non_compliance_no', ''))
    
    # Special Conditions
    y -= 8*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(21*mm, y, "Special Conditions")
    y -= 5*mm
    
    draw_checkbox(c, 70*mm, y, checked=form_data.get('special_over_100_amps') == 'yes')
    c.setFont("Helvetica", 8)
    c.drawString(75*mm, y + 0.5*mm, "Over 100 amps")
    
    draw_checkbox(c, 120*mm, y, checked=form_data.get('special_hazardous_area') == 'yes')
    c.drawString(125*mm, y + 0.5*mm, "Hazardous Area")
    
    draw_checkbox(c, 165*mm, y, checked=form_data.get('special_off_grid') == 'yes')
    c.drawString(170*mm, y + 0.5*mm, "Off Grid Installation")
    
    y -= 6*mm
    draw_checkbox(c, 70*mm, y, checked=form_data.get('special_high_voltage') == 'yes')
    c.drawString(75*mm, y + 0.5*mm, "High Voltage")
    
    draw_checkbox(c, 120*mm, y, checked=form_data.get('special_unmetered') == 'yes')
    c.drawString(125*mm, y + 0.5*mm, "Unmetered Supply")
    
    draw_checkbox(c, 165*mm, y, checked=form_data.get('special_secondary_power') == 'yes')
    c.drawString(170*mm, y + 0.5*mm, "Secondary Power Supply")
    
    # ========== PAGE 2 ==========
    c.showPage()
    y = height - 20*mm
    
    # SECTION 4: DETAILS OF EQUIPMENT
    y = draw_green_header(c, y, "*DETAILS OF EQUIPMENT")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "Select equipment installed and estimate increase of work affected by the work carried out")
    y -= 8*mm
    
    # Equipment table
    table_x = 20*mm
    table_width = 170*mm
    row_height = 6*mm
    col_widths = [10*mm, 50*mm, 35*mm, 35*mm, 40*mm]
    
    # Table header
    c.setFillColor(HEADER_GREEN)
    c.setStrokeColor(black)
    c.rect(table_x, y - row_height, table_width, row_height, stroke=1, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(table_x + 2*mm, y - row_height + 2*mm, "")  # Checkbox column
    c.drawString(table_x + col_widths[0] + 2*mm, y - row_height + 2*mm, "EQUIPMENT")
    c.drawString(table_x + col_widths[0] + col_widths[1] + 2*mm, y - row_height + 2*mm, "RATING")
    c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + 2*mm, y - row_height + 2*mm, "NUMBER INSTALLED")
    c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] + 2*mm, y - row_height + 2*mm, "PARTICULARS")
    
    y -= row_height
    
    # Equipment rows
    equipment_items = [
        ('Switchboard', 'equip_switchboard', 'equip_switchboard_rating', 'equip_switchboard_number', 'equip_switchboard_particulars'),
        ('Circuits', 'equip_circuits', 'equip_circuits_rating', 'equip_circuits_number', 'equip_circuits_particulars'),
        ('Lighting', 'equip_lighting', 'equip_lighting_rating', 'equip_lighting_number', 'equip_lighting_particulars'),
        ('Socket Outlets', 'equip_sockets', 'equip_sockets_rating', 'equip_sockets_number', 'equip_sockets_particulars'),
        ('Appliances', 'equip_appliances', 'equip_appliances_rating', 'equip_appliances_number', 'equip_appliances_particulars'),
        ('Generation', 'equip_generation', 'equip_generation_rating', 'equip_generation_number', 'equip_generation_particulars'),
        ('Storage', 'equip_storage', 'equip_storage_rating', 'equip_storage_number', 'equip_storage_particulars'),
    ]
    
    c.setFont("Helvetica", 8)
    
    for item_name, check_field, rating_field, number_field, particulars_field in equipment_items:
        # Draw checkbox column (white background)
        c.setStrokeColor(black)
        c.setFillColor(white)
        c.rect(table_x, y - row_height, col_widths[0], row_height, stroke=1, fill=1)
        
        # Draw checkbox
        draw_checkbox(c, table_x + 1*mm, y - row_height + 2*mm, checked=form_data.get(check_field) == 'yes')
        
        # Draw equipment name column (green background)
        c.setFillColor(LABEL_GREEN)
        c.rect(table_x + col_widths[0], y - row_height, col_widths[1], row_height, stroke=1, fill=1)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(table_x + col_widths[0] + 2*mm, y - row_height + 2*mm, item_name)
        
        # Draw rating column (white background)
        c.setFillColor(white)
        c.setStrokeColor(black)
        c.rect(table_x + col_widths[0] + col_widths[1], y - row_height, col_widths[2], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.setFont("Helvetica", 8)
        c.drawString(table_x + col_widths[0] + col_widths[1] + 2*mm, y - row_height + 2*mm, str(form_data.get(rating_field, '')))
        
        # Draw number column (white background)
        c.setFillColor(white)
        c.rect(table_x + col_widths[0] + col_widths[1] + col_widths[2], y - row_height, col_widths[3], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + 2*mm, y - row_height + 2*mm, str(form_data.get(number_field, '')))
        
        # Draw particulars column (white background)
        c.setFillColor(white)
        c.rect(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3], y - row_height, col_widths[4], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] + 2*mm, y - row_height + 2*mm, str(form_data.get(particulars_field, '')))
        
        y -= row_height
    
    # SECTION 5: INSTALLERS LICENSE DETAILS
    y -= 10*mm
    y = draw_green_header(c, y, "INSTALLERS LICENSE DETAILS")
    y -= 3*mm
    
    # First Name, Last Name label row
    y = draw_label_row(c, y, [
        ("*First Name", 21*mm, 85*mm),
        ("*Last Name", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_first_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, form_data.get('installer_last_name', ''))
    y -= 5*mm
    
    # Floor, Unit, Street Number, Lot/RMB label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Floor", 21*mm, 25*mm),
        ("Unit", 49*mm, 25*mm),
        ("*Street Number", 77*mm, 30*mm),
        ("&/or", 110*mm, 15*mm),
        ("Lot/RMB", 129*mm, 61*mm)
    ])
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')  # Floor
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')  # Unit
    draw_field_box(c, 76*mm, y, 30*mm, 5*mm, form_data.get('installer_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')  # Lot/RMB
    y -= 5*mm
    
    # Street Name, Nearest Cross Street label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Street Name", 21*mm, 85*mm),
        ("Nearest Cross Street", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')  # Nearest Cross Street
    y -= 5*mm
    
    # Suburb, State, Post Code label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Suburb", 21*mm, 85*mm),
        ("*State", 109*mm, 40*mm),
        ("*Post Code", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('installer_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('installer_postcode', ''))
    y -= 5*mm
    
    # Email, Office Phone, Mobile Phone label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Email", 21*mm, 85*mm),
        ("*Office Phone", 109*mm, 40*mm),
        ("Mobile Phone", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_email', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('installer_office_phone', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('installer_mobile_phone', ''))
    y -= 5*mm
    
    # License details label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Contractor License Class", 21*mm, 42*mm),
        ("Electrician License Class", 66*mm, 42*mm),
        ("*License Number", 111*mm, 40*mm),
        ("*License Expiry", 154*mm, 36*mm)
    ])
    draw_field_box(c, 20*mm, y, 42*mm, 5*mm, '')  # Contractor License Class
    draw_field_box(c, 65*mm, y, 42*mm, 5*mm, '')  # Electrician License Class
    draw_field_box(c, 110*mm, y, 40*mm, 5*mm, form_data.get('installer_license_no', ''))
    draw_field_box(c, 153*mm, y, 37*mm, 5*mm, format_date_australian(form_data.get('installer_license_expiry', '')))
    y -= 5*mm
    
    # ========== PAGE 3 ==========
    c.showPage()
    y = height - 20*mm
    
    # SECTION 6: TEST REPORT
    y = draw_green_header(c, y, "*TEST REPORT")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "In respect to the test carried out by me on the above mentioned installation, I certify that:")
    y -= 5*mm
    
    c.drawString(21*mm, y, "1.  I have carried out the test below and that the installation has passed the following requirements:")
    y -= 5*mm
    
    # Test checkboxes
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_earthing') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Earthing system integrity")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_rcd') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Residual current device operational")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_insulation') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Insulation resistance Mohms")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_visual') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Visual check that installation is suitable for connection to supply")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_polarity') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Polarity")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_standalone') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Stand-Alone system complies with AS4509")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_current') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Correct current connections")
    y -= 5*mm
    
    draw_checkbox(c, 25*mm, y, checked=form_data.get('test_fault_loop') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Fault loop impedance (if necessary)")
    y -= 8*mm
    
    c.drawString(21*mm, y, "2.  I confirm that I have visually checked that the installation described in this Certificate complies with the")
    y -= 4*mm
    c.drawString(25*mm, y, "relevant Acts, Regulations, Codes and Standards:")
    y -= 8*mm
    
    c.drawString(21*mm, y, "3.  *The test was completed on")
    draw_field_box(c, 70*mm, y - 2*mm, 40*mm, 5*mm, format_date_australian(form_data.get('test_date', '')))
    y -= 10*mm
    
    # SECTION 7: TESTERS LICENSE DETAILS
    y = draw_green_header(c, y, "TESTERS LICENSE DETAILS")
    y -= 3*mm
    
    # First Name, Last Name label row
    y = draw_label_row(c, y, [
        ("*First Name", 21*mm, 85*mm),
        ("*Last Name", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_first_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, form_data.get('tester_last_name', ''))
    y -= 5*mm
    
    # Floor, Unit, Street Number, Lot/RMB label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Floor", 21*mm, 25*mm),
        ("Unit", 49*mm, 25*mm),
        ("*Street Number", 77*mm, 30*mm),
        ("&/or", 110*mm, 15*mm),
        ("Lot/RMB", 129*mm, 61*mm)
    ])
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')  # Floor
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')  # Unit
    draw_field_box(c, 76*mm, y, 30*mm, 5*mm, form_data.get('tester_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')  # Lot/RMB
    y -= 5*mm
    
    # Street Name, Nearest Cross Street label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Street Name", 21*mm, 85*mm),
        ("Nearest Cross Street", 109*mm, 81*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')  # Nearest Cross Street
    y -= 5*mm
    
    # Suburb, State, Post Code label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Suburb", 21*mm, 85*mm),
        ("*State", 109*mm, 40*mm),
        ("*Post Code", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('tester_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('tester_postcode', ''))
    y -= 5*mm
    
    # Email, Office Phone, Mobile Phone label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("*Email", 21*mm, 85*mm),
        ("Office Phone", 109*mm, 40*mm),
        ("Mobile Phone", 152*mm, 38*mm)
    ])
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_email', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('tester_office_phone', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('tester_mobile_phone', ''))
    y -= 5*mm
    
    # License details label row
    y -= 3*mm
    y = draw_label_row(c, y, [
        ("Contractor License Class", 21*mm, 42*mm),
        ("Electrician License Class", 66*mm, 42*mm),
        ("*License Number", 111*mm, 40*mm),
        ("*License Expiry", 154*mm, 36*mm)
    ])
    draw_field_box(c, 20*mm, y, 42*mm, 5*mm, '')  # Contractor License Class
    draw_field_box(c, 65*mm, y, 42*mm, 5*mm, '')  # Electrician License Class
    draw_field_box(c, 110*mm, y, 40*mm, 5*mm, form_data.get('tester_license_no', ''))
    draw_field_box(c, 153*mm, y, 37*mm, 5*mm, format_date_australian(form_data.get('tester_license_expiry', '')))
    y -= 8*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "In my capacity as the Tester, I certify that the electrical work carried out on the above mentioned property")
    y -= 4*mm
    c.drawString(21*mm, y, "was completed by the nominated electrician")
    y -= 10*mm
    
    # SECTION 8: SUBMIT CCEW
    y = draw_green_header(c, y, "*SUBMIT CCEW")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "Please select the energy provider for where this work has been carried out, to email a copy of this")
    y -= 4*mm
    c.drawString(21*mm, y, "CCEW directly to that provider")
    y -= 6*mm
    draw_field_box(c, 20*mm, y - 2*mm, 170*mm, 5*mm, form_data.get('energy_provider', ''))
    y -= 10*mm
    
    c.drawString(21*mm, y, "Please enter the meter providers email to send a copy of this CCEW directly to that provider")
    y -= 6*mm
    draw_field_box(c, 20*mm, y - 2*mm, 170*mm, 5*mm, '')
    y -= 10*mm
    
    # Signature
    c.drawString(21*mm, y, "Signature:")
    draw_field_box(c, 20*mm, y - 8*mm, 80*mm, 20*mm, form_data.get('signature', ''))
    
    # Finalize PDF
    c.save()
    
    # Get PDF bytes and encode to base64
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_bytes).decode('utf-8')
