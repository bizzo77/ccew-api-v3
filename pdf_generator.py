"""
PDF Generator for CCEW Forms - Official Layout
Generates a PDF that matches the official NSW CCEW form exactly
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import base64


# Colors matching official form
HEADER_GREEN = HexColor('#8DB04C')
FIELD_BORDER = HexColor('#CCCCCC')
TEXT_BLACK = black


def draw_checkbox(c, x, y, size=3*mm, checked=False):
    """Draw a checkbox at the specified position"""
    c.setStrokeColor(black)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, stroke=1, fill=0)
    if checked:
        # Draw an X
        c.line(x, y, x + size, y + size)
        c.line(x + size, y, x, y + size)


def draw_field_box(c, x, y, width, height, value='', font_size=9):
    """Draw a field box with optional value"""
    # Draw border
    c.setStrokeColor(FIELD_BORDER)
    c.setFillColor(white)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=1)
    
    # Draw value if provided
    if value:
        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica", font_size)
        c.drawString(x + 2*mm, y + 2*mm, str(value))


def draw_green_header(c, y, text, width=170*mm):
    """Draw a green header section"""
    x = 20*mm
    height = 7*mm
    
    c.setFillColor(HEADER_GREEN)
    c.rect(x, y, width, height, stroke=0, fill=1)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2*mm, y + 2*mm, text)
    
    return y - height


def generate_ccew_pdf(form_data):
    """
    Generate a PDF document matching the official CCEW form
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
    
    # Property Name
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Property Name")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, form_data.get('property_name', ''))
    
    # Floor, Unit, Street Number, Lot/RMB
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Floor")
    c.drawString(50*mm, y + 1*mm, "Unit")
    c.drawString(80*mm, y + 1*mm, "*Street Number")
    c.drawString(115*mm, y + 1*mm, "&/or")
    c.drawString(130*mm, y + 1*mm, "Lot/RMB")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')  # Floor
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')  # Unit
    draw_field_box(c, 76*mm, y, 35*mm, 5*mm, form_data.get('install_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')  # Lot/RMB
    
    # Street Name, Nearest Cross Street
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Street Name")
    c.drawString(115*mm, y + 1*mm, "Nearest Cross Street")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('install_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, form_data.get('nearest_cross_street', ''))
    
    # Suburb, State, Post Code
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Suburb")
    c.drawString(115*mm, y + 1*mm, "*State")
    c.drawString(155*mm, y + 1*mm, "*Post Code")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('install_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('install_state', 'NSW'))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('install_postcode', ''))
    
    # Pit/Pillar, NMI, Meter No, AEMO
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Pit/Pillar/Pole No.")
    c.drawString(65*mm, y + 1*mm, "NMI")
    c.drawString(100*mm, y + 1*mm, "Meter No.")
    c.drawString(135*mm, y + 1*mm, "AEMO Metering Provider I.D.")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 40*mm, 5*mm, form_data.get('pit_pillar_pole_no', ''))
    draw_field_box(c, 63*mm, y, 32*mm, 5*mm, form_data.get('nmi', ''))
    draw_field_box(c, 98*mm, y, 32*mm, 5*mm, form_data.get('meter_no', ''))
    draw_field_box(c, 133*mm, y, 57*mm, 5*mm, form_data.get('aemo_provider_id', ''))
    
    # SECTION 2: CUSTOMER DETAILS
    y -= 12*mm
    y = draw_green_header(c, y, "CUSTOMER DETAILS")
    
    # Checkbox for same address
    y -= 8*mm
    draw_checkbox(c, 165*mm, y)
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(170*mm, y + 0.5*mm, "Please tick if Customer Address")
    y -= 3*mm
    c.drawString(170*mm, y + 0.5*mm, "details same as installation details")
    y += 3*mm
    
    # First Name, Last Name
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*First Name")
    c.drawString(105*mm, y + 1*mm, "*Last Name")
    y -= 6*mm
    customer_first = form_data.get('customer_first_name', '')
    customer_last = form_data.get('customer_last_name', '')
    draw_field_box(c, 20*mm, y, 80*mm, 5*mm, customer_first)
    draw_field_box(c, 103*mm, y, 87*mm, 5*mm, customer_last)
    
    # Company Name
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Company Name")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, form_data.get('customer_company_name', ''))
    
    # Floor, Unit, Street Number, Lot/RMB
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Floor")
    c.drawString(50*mm, y + 1*mm, "Unit")
    c.drawString(80*mm, y + 1*mm, "*Street Number")
    c.drawString(115*mm, y + 1*mm, "&/or")
    c.drawString(130*mm, y + 1*mm, "Lot/RMB")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 76*mm, y, 35*mm, 5*mm, form_data.get('customer_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')
    
    # Street Name, Nearest Cross Street
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Street Name")
    c.drawString(115*mm, y + 1*mm, "Nearest Cross Street")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')
    
    # Suburb, State, Post Code
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Suburb")
    c.drawString(115*mm, y + 1*mm, "*State")
    c.drawString(155*mm, y + 1*mm, "*Post Code")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('customer_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('customer_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('customer_postcode', ''))
    
    # Email, Office No, Mobile No
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Email")
    c.drawString(125*mm, y + 1*mm, "Office No.")
    c.drawString(160*mm, y + 1*mm, "Mobile No.")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 100*mm, 5*mm, '')
    draw_field_box(c, 123*mm, y, 30*mm, 5*mm, '')
    draw_field_box(c, 156*mm, y, 34*mm, 5*mm, '')
    
    # SECTION 3: INSTALLATION DETAILS
    y -= 12*mm
    y = draw_green_header(c, y, "INSTALLATION DETAILS")
    y -= 3*mm
    
    # Type of Installation
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "*Type of Installation")
    y -= 5*mm
    
    # Installation type checkboxes
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
    # Work checkboxes - row 2
    draw_checkbox(c, 25*mm, y, checked=form_data.get('work_addition_alteration') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Addition/alteration to existing")
    
    draw_checkbox(c, 85*mm, y, checked=form_data.get('work_advanced_meter') == 'yes')
    c.drawString(90*mm, y + 0.5*mm, "Install Advanced Meter")
    
    draw_checkbox(c, 145*mm, y, checked=form_data.get('work_ev_connection') == 'yes')
    c.drawString(150*mm, y + 0.5*mm, "EV Connection")
    
    y -= 5*mm
    # Work checkboxes - row 3
    draw_checkbox(c, 25*mm, y, checked=form_data.get('work_reinspection') == 'yes')
    c.drawString(30*mm, y + 0.5*mm, "Re-inspection of non-compliant work")
    
    c.drawString(90*mm, y + 0.5*mm, "Non-Compliance No.")
    draw_field_box(c, 125*mm, y - 1*mm, 65*mm, 5*mm, form_data.get('non_compliance_no', ''))
    
    # Special Conditions
    y -= 8*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(21*mm, y, "Special Conditions")
    y -= 5*mm
    
    # Special conditions - row 1
    draw_checkbox(c, 60*mm, y, checked=form_data.get('special_over_100_amps') == 'yes')
    c.setFont("Helvetica", 8)
    c.drawString(65*mm, y + 0.5*mm, "Over 100 amps")
    
    draw_checkbox(c, 105*mm, y, checked=form_data.get('special_hazardous_area') == 'yes')
    c.drawString(110*mm, y + 0.5*mm, "Hazardous Area")
    
    draw_checkbox(c, 155*mm, y, checked=form_data.get('special_off_grid') == 'yes')
    c.drawString(160*mm, y + 0.5*mm, "Off Grid Installation")
    
    y -= 5*mm
    # Special conditions - row 2
    draw_checkbox(c, 60*mm, y, checked=form_data.get('special_high_voltage') == 'yes')
    c.drawString(65*mm, y + 0.5*mm, "High Voltage")
    
    draw_checkbox(c, 105*mm, y, checked=form_data.get('special_unmetered') == 'yes')
    c.drawString(110*mm, y + 0.5*mm, "Unmetered Supply")
    
    draw_checkbox(c, 145*mm, y, checked=form_data.get('special_secondary_power') == 'yes')
    c.drawString(150*mm, y + 0.5*mm, "Secondary Power Supply")
    
    # ========== PAGE 2 ==========
    c.showPage()
    y = height - 30*mm
    
    # SECTION 4: DETAILS OF EQUIPMENT
    y = draw_green_header(c, y, "*DETAILS OF EQUIPMENT")
    y -= 3*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "Select equipment installed and estimate increase of work affected by the work carried out")
    y -= 5*mm
    
    # Equipment table
    table_x = 20*mm
    table_width = 170*mm
    col_widths = [5*mm, 50*mm, 35*mm, 40*mm, 40*mm]
    row_height = 7*mm
    
    # Table header
    c.setFillColor(HEADER_GREEN)
    c.rect(table_x, y - row_height, table_width, row_height, stroke=1, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
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
    c.setFillColor(HEADER_GREEN)
    
    for item_name, check_field, rating_field, number_field, particulars_field in equipment_items:
        # Draw row background
        c.rect(table_x, y - row_height, table_width, row_height, stroke=1, fill=1)
        
        # Checkbox
        c.setFillColor(white)
        draw_checkbox(c, table_x + 1*mm, y - row_height + 2*mm, checked=form_data.get(check_field) == 'yes')
        
        # Equipment name
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(table_x + col_widths[0] + 2*mm, y - row_height + 2*mm, item_name)
        
        # Draw white boxes for data fields
        c.setFillColor(white)
        c.setStrokeColor(black)
        # Rating
        c.rect(table_x + col_widths[0] + col_widths[1], y - row_height, col_widths[2], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.setFont("Helvetica", 8)
        c.drawString(table_x + col_widths[0] + col_widths[1] + 2*mm, y - row_height + 2*mm, form_data.get(rating_field, ''))
        
        # Number
        c.setFillColor(white)
        c.rect(table_x + col_widths[0] + col_widths[1] + col_widths[2], y - row_height, col_widths[3], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + 2*mm, y - row_height + 2*mm, form_data.get(number_field, ''))
        
        # Particulars
        c.setFillColor(white)
        c.rect(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3], y - row_height, col_widths[4], row_height, stroke=1, fill=1)
        c.setFillColor(black)
        c.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] + 2*mm, y - row_height + 2*mm, form_data.get(particulars_field, ''))
        
        y -= row_height
    
    # SECTION 5: METERS
    y -= 5*mm
    y = draw_green_header(c, y, "*Meters - Installed (I), Removed (R), Existing (E)")
    y -= 3*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "Master/Sub Status - No (N), Master (M), Sub (S)")
    y -= 5*mm
    
    # Meters table (simplified - showing structure)
    c.setStrokeColor(black)
    c.rect(20*mm, y - 30*mm, 170*mm, 30*mm, stroke=1, fill=0)
    c.setFont("Helvetica", 7)
    c.drawString(22*mm, y - 5*mm, "I  R  E")
    c.drawString(35*mm, y - 5*mm, "Meter No.")
    c.drawString(60*mm, y - 5*mm, "No. Dials")
    c.drawString(80*mm, y - 5*mm, "Master/Sub Status")
    c.drawString(115*mm, y - 5*mm, "Wired as Master/Sub")
    c.drawString(150*mm, y - 5*mm, "Register No.")
    
    y -= 35*mm
    
    # Load questions
    c.setFont("Helvetica", 8)
    c.drawString(21*mm, y, "Estimated increase in load A/ph")
    draw_field_box(c, 80*mm, y - 2*mm, 30*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(21*mm, y, "* Is increased load within capacity of installation/service mains?")
    c.drawString(130*mm, y, "Yes")
    draw_checkbox(c, 140*mm, y - 1*mm)
    c.drawString(150*mm, y, "No")
    draw_checkbox(c, 160*mm, y - 1*mm)
    
    y -= 6*mm
    c.drawString(21*mm, y, "* Is work connected to supply? (pending DSNP Inspection)")
    c.drawString(130*mm, y, "Yes")
    draw_checkbox(c, 140*mm, y - 1*mm)
    c.drawString(150*mm, y, "No")
    draw_checkbox(c, 160*mm, y - 1*mm)
    
    # SECTION 6: INSTALLERS LICENSE DETAILS
    y -= 12*mm
    y = draw_green_header(c, y, "INSTALLERS LICENSE DETAILS")
    y -= 3*mm
    
    # First Name, Last Name
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*First Name")
    c.drawString(105*mm, y + 1*mm, "*Last Name")
    y -= 6*mm
    installer_first = form_data.get('installer_first_name', '')
    installer_last = form_data.get('installer_last_name', '')
    draw_field_box(c, 20*mm, y, 80*mm, 5*mm, installer_first)
    draw_field_box(c, 103*mm, y, 87*mm, 5*mm, installer_last)
    
    # Floor, Unit, Street Number, Lot/RMB
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Floor")
    c.drawString(50*mm, y + 1*mm, "Unit")
    c.drawString(80*mm, y + 1*mm, "*Street Number")
    c.drawString(115*mm, y + 1*mm, "&/or")
    c.drawString(130*mm, y + 1*mm, "Lot/RMB")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 76*mm, y, 35*mm, 5*mm, form_data.get('installer_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')
    
    # Street Name, Nearest Cross Street
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Street Name")
    c.drawString(115*mm, y + 1*mm, "Nearest Cross Street")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')
    
    # Suburb, State, Post Code
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Suburb")
    c.drawString(115*mm, y + 1*mm, "*State")
    c.drawString(155*mm, y + 1*mm, "*Post Code")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('installer_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('installer_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('installer_postcode', ''))
    
    # Email, Office No, Mobile No
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Email")
    c.drawString(125*mm, y + 1*mm, "Office No.")
    c.drawString(160*mm, y + 1*mm, "Mobile No.")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 100*mm, 5*mm, form_data.get('installer_email', ''))
    draw_field_box(c, 123*mm, y, 30*mm, 5*mm, form_data.get('installer_office_phone', ''))
    draw_field_box(c, 156*mm, y, 34*mm, 5*mm, form_data.get('installer_mobile_phone', ''))
    
    # License details
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Qualified Supervisors No.")
    c.drawString(70*mm, y + 1*mm, "*Expiry Date")
    c.drawString(105*mm, y + 1*mm, "Or")
    c.drawString(115*mm, y + 1*mm, "*Contractor's License No.")
    c.drawString(165*mm, y + 1*mm, "*Expiry Date")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 45*mm, 5*mm, '')
    draw_field_box(c, 68*mm, y, 30*mm, 5*mm, '')
    draw_field_box(c, 113*mm, y, 45*mm, 5*mm, form_data.get('installer_license_no', ''))
    draw_field_box(c, 161*mm, y, 29*mm, 5*mm, form_data.get('installer_license_expiry', ''))
    
    # ========== PAGE 3 ==========
    c.showPage()
    y = height - 30*mm
    
    # SECTION 7: TEST REPORT
    y = draw_green_header(c, y, "*TEST REPORT")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "In respect to the test carried out by me on the above mentioned installation, I certify that:")
    y -= 5*mm
    c.drawString(21*mm, y, "1.   I have carried out the test below and that the installation has passed the following requirements:")
    y -= 5*mm
    
    # Test checkboxes
    test_items = [
        ('test_earthing', 'Earthing system integrity'),
        ('test_rcd', 'Residual current device operational'),
        ('test_insulation', 'Insulation resistance Mohms'),
        ('test_visual', 'Visual check that installation is suitable for connection to supply'),
        ('test_polarity', 'Polarity'),
        ('test_standalone', 'Stand-Alone system complies with AS4509'),
        ('test_current', 'Correct current connections'),
        ('test_fault_loop', 'Fault loop impedance (if necessary)'),
    ]
    
    for field, label in test_items:
        draw_checkbox(c, 25*mm, y, checked=form_data.get(field) == 'yes')
        c.drawString(30*mm, y + 0.5*mm, label)
        y -= 5*mm
    
    y -= 2*mm
    c.drawString(21*mm, y, "2.   I confirm that I have visually checked that the installation described in this Certificate complies with the")
    y -= 4*mm
    c.drawString(26*mm, y, "relevant Acts, Regulations, Codes and Standards:")
    
    y -= 6*mm
    c.drawString(21*mm, y, "3.   *The test was completed on")
    draw_field_box(c, 75*mm, y - 2*mm, 40*mm, 5*mm, form_data.get('test_date', ''))
    
    # SECTION 8: TESTERS LICENSE DETAILS
    y -= 12*mm
    y = draw_green_header(c, y, "TESTERS LICENSE DETAILS")
    
    # Checkbox for same as installer
    y -= 8*mm
    draw_checkbox(c, 165*mm, y)
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(170*mm, y + 0.5*mm, "Please tick if Testers Lic. details")
    y -= 3*mm
    c.drawString(170*mm, y + 0.5*mm, "same as Installers Lic. details")
    y += 3*mm
    
    # First Name, Last Name
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*First Name")
    c.drawString(105*mm, y + 1*mm, "*Last Name")
    y -= 6*mm
    tester_first = form_data.get('tester_first_name', '')
    tester_last = form_data.get('tester_last_name', '')
    draw_field_box(c, 20*mm, y, 80*mm, 5*mm, tester_first)
    draw_field_box(c, 103*mm, y, 87*mm, 5*mm, tester_last)
    
    # Floor, Unit, Street Number, Lot/RMB
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "Floor")
    c.drawString(50*mm, y + 1*mm, "Unit")
    c.drawString(80*mm, y + 1*mm, "*Street Number")
    c.drawString(115*mm, y + 1*mm, "&/or")
    c.drawString(130*mm, y + 1*mm, "Lot/RMB")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 48*mm, y, 25*mm, 5*mm, '')
    draw_field_box(c, 76*mm, y, 35*mm, 5*mm, form_data.get('tester_street_number', ''))
    draw_field_box(c, 128*mm, y, 62*mm, 5*mm, '')
    
    # Street Name, Nearest Cross Street
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Street Name")
    c.drawString(115*mm, y + 1*mm, "Nearest Cross Street")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_street_name', ''))
    draw_field_box(c, 108*mm, y, 82*mm, 5*mm, '')
    
    # Suburb, State, Post Code
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Suburb")
    c.drawString(115*mm, y + 1*mm, "*State")
    c.drawString(155*mm, y + 1*mm, "*Post Code")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 85*mm, 5*mm, form_data.get('tester_suburb', ''))
    draw_field_box(c, 108*mm, y, 40*mm, 5*mm, form_data.get('tester_state', ''))
    draw_field_box(c, 151*mm, y, 39*mm, 5*mm, form_data.get('tester_postcode', ''))
    
    # Email, Office No, Mobile No
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Email")
    c.drawString(125*mm, y + 1*mm, "Office No.")
    c.drawString(160*mm, y + 1*mm, "Mobile No.")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 100*mm, 5*mm, form_data.get('tester_email', ''))
    draw_field_box(c, 123*mm, y, 30*mm, 5*mm, '')
    draw_field_box(c, 156*mm, y, 34*mm, 5*mm, '')
    
    # License details
    y -= 8*mm
    c.setFillColor(white)
    c.drawString(21*mm, y + 1*mm, "*Qualified Supervisors No.")
    c.drawString(70*mm, y + 1*mm, "*Expiry Date")
    c.drawString(105*mm, y + 1*mm, "Or")
    c.drawString(115*mm, y + 1*mm, "*Contractor's License No.")
    c.drawString(165*mm, y + 1*mm, "*Expiry Date")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 45*mm, 5*mm, '')
    draw_field_box(c, 68*mm, y, 30*mm, 5*mm, '')
    draw_field_box(c, 113*mm, y, 45*mm, 5*mm, form_data.get('tester_license_no', ''))
    draw_field_box(c, 161*mm, y, 29*mm, 5*mm, form_data.get('tester_license_expiry', ''))
    
    y -= 8*mm
    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    c.drawString(21*mm, y, "In my capacity as the Tester, I certify that the electrical work carried out on the above mentioned property")
    y -= 3*mm
    c.drawString(21*mm, y, "was completed by the nominated electrician")
    
    # SECTION 9: SUBMIT CCEW
    y -= 10*mm
    y = draw_green_header(c, y, "*SUBMIT CCEW")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(21*mm, y, "Please select the energy provider for where this work has been carried out, to email a copy of this")
    y -= 4*mm
    c.drawString(21*mm, y, "CCEW directly to that provider")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, form_data.get('energy_provider', ''))
    
    y -= 8*mm
    c.drawString(21*mm, y, "Please enter the meter providers email to send a copy of this CCEW directly to that provider")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(21*mm, y, "Please confirm the owners email address to send a copy of this CCEW directly to the property owner")
    y -= 6*mm
    draw_field_box(c, 20*mm, y, 170*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(21*mm, y, "I certify that the information provided in this Certificate Compliance Electrical Work (CCEW) is true")
    y -= 4*mm
    c.drawString(21*mm, y, "and correct.")
    
    y -= 8*mm
    draw_field_box(c, 20*mm, y, 60*mm, 10*mm, '')
    c.setFont("Helvetica-Bold", 8)
    c.drawString(21*mm, y - 5*mm, "*Signature")
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(21*mm, y - 8*mm, "Signature is only required when")
    c.drawString(21*mm, y - 11*mm, "providing as a printed copy")
    
    # Signature value
    c.setFont("Helvetica", 10)
    c.drawString(22*mm, y + 3*mm, form_data.get('signature', ''))
    
    # Footer note
    y -= 15*mm
    c.setFont("Helvetica", 6)
    c.drawString(21*mm, y, "If completing this CCEW electronically, please click the SUBMIT button to generate an email with a copy of the CCEW which you can save and send to the")
    y -= 3*mm
    c.drawString(21*mm, y, "NSW Regulator, Customer, the Service Provider and Meter Provider.")
    
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
