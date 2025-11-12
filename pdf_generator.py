"""
PDF Generator for CCEW Forms - Exact Match to Official NSW Form
Uses green section blocks exactly as shown in the official form
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
import io
import base64
from datetime import datetime


# Colors matching official form
SECTION_GREEN = HexColor('#8DB04C')
TEXT_BLACK = black


def format_date_australian(date_str):
    """Convert date to Australian format DD/MM/YYYY"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str


def draw_checkbox(c, x, y, size=3*mm, checked=False):
    """Draw a checkbox"""
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, stroke=1, fill=1)
    if checked:
        c.setStrokeColor(black)
        c.setLineWidth(1.5)
        c.line(x + 0.5*mm, y + 0.5*mm, x + size - 0.5*mm, y + size - 0.5*mm)
        c.line(x + size - 0.5*mm, y + 0.5*mm, x + 0.5*mm, y + size - 0.5*mm)


def draw_field(c, x, y, width, height, value='', font_size=8, bold=False):
    """Draw a white field box with value"""
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=1)
    
    if value:
        c.setFillColor(TEXT_BLACK)
        if bold:
            c.setFont("Helvetica-Bold", font_size)
        else:
            c.setFont("Helvetica", font_size)
        c.drawString(x + 1*mm, y + 1.5*mm, str(value))


def draw_green_section(c, x, y, width, height, header_text, header_y):
    """Draw green background section with header"""
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=1)
    
    # Draw header in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 2*mm, header_y, header_text)


def get_pdf_filename(form_data):
    """Generate PDF filename"""
    job_no = form_data.get('serial_no', 'UNKNOWN')
    return f"CCEW_Form_Job_{job_no}.pdf"


def generate_ccew_pdf(form_data):
    """Generate PDF matching official CCEW form exactly"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # ========== PAGE 1 ==========
    y = height - 25*mm
    
    # Header
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor('#C41E3A'))
    c.drawString(20*mm, y, "NSW")
    c.setFillColor(black)
    c.drawString(35*mm, y, "Fair Trading")
    
    # Serial No
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150*mm, y, "*Serial No:")
    draw_field(c, 170*mm, y - 3*mm, 20*mm, 5*mm, form_data.get('serial_no', ''))
    
    # Title
    y -= 10*mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, y, "Online Certificate Compliance Electrical Work (CCEW)")
    y -= 5*mm
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, y, "Any field marked with an * is mandatory")
    
    # ========== INSTALLATION ADDRESS SECTION ==========
    y -= 8*mm
    section_start_y = y
    
    # Section header (will be drawn later)
    header_text = "INSTALLATION ADDRESS"
    header_y = y - 5*mm
    
    y -= 10*mm
    # Property Name
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "Property Name")
    y -= 5*mm
    draw_field(c, 21*mm, y, 168*mm, 5*mm, form_data.get('property_name', ''))
    
    y -= 8*mm
    # Floor, Unit, Street Number, Lot/RMB
    c.drawString(22*mm, y, "Floor")
    c.drawString(48*mm, y, "Unit")
    c.drawString(77*mm, y, "*Street Number")
    c.drawString(115*mm, y, "&/or")
    c.drawString(130*mm, y, "Lot/RMB")
    y -= 5*mm
    draw_field(c, 21*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, y, 35*mm, 5*mm, form_data.get('install_street_number', ''))
    draw_field(c, 128*mm, y, 61*mm, 5*mm, '')
    
    y -= 8*mm
    # Street Name, Nearest Cross Street
    c.drawString(22*mm, y, "*Street Name")
    c.drawString(115*mm, y, "Nearest Cross Street")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('install_street_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, form_data.get('nearest_cross_street', ''))
    
    y -= 8*mm
    # Suburb, State, Post Code
    c.drawString(22*mm, y, "*Suburb")
    c.drawString(115*mm, y, "*State")
    c.drawString(155*mm, y, "*Post Code")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('install_suburb', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('install_state', 'NSW'))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('install_postcode', ''))
    
    y -= 8*mm
    # Pit/Pillar, NMI, Meter No, AEMO
    c.drawString(22*mm, y, "Pit/Pillar/Pole No.")
    c.drawString(65*mm, y, "NMI")
    c.drawString(100*mm, y, "Meter No.")
    c.drawString(135*mm, y, "AEMO Metering Provider I.D.")
    y -= 5*mm
    draw_field(c, 21*mm, y, 40*mm, 5*mm, form_data.get('pit_pillar_pole_no', ''))
    draw_field(c, 64*mm, y, 32*mm, 5*mm, form_data.get('nmi', ''))
    draw_field(c, 99*mm, y, 32*mm, 5*mm, form_data.get('meter_no', ''))
    draw_field(c, 134*mm, y, 55*mm, 5*mm, form_data.get('aemo_provider_id', ''))
    
    # Now draw green background covering entire section
    section_end_y = y - 2*mm  # Add padding at bottom
    section_height = section_start_y - section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, section_end_y, 170*mm, section_height, stroke=1, fill=1)
    
    # Draw section header and all labels in WHITE on top of green background
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, header_y, header_text)
    
    # Draw labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, section_start_y - 13*mm, "Property Name")
    c.drawString(22*mm, section_start_y - 21*mm, "Floor")
    c.drawString(48*mm, section_start_y - 21*mm, "Unit")
    c.drawString(74*mm, section_start_y - 21*mm, "*Street Number")
    c.drawString(115*mm, section_start_y - 21*mm, "&/or")
    c.drawString(129*mm, section_start_y - 21*mm, "Lot/RMB")
    c.drawString(22*mm, section_start_y - 29*mm, "*Street Name")
    c.drawString(110*mm, section_start_y - 29*mm, "Nearest Cross Street")
    c.drawString(22*mm, section_start_y - 37*mm, "*Suburb")
    c.drawString(110*mm, section_start_y - 37*mm, "*State")
    c.drawString(155*mm, section_start_y - 37*mm, "*Post Code")
    c.drawString(22*mm, section_start_y - 45*mm, "Pit/Pillar /Pole No.")
    c.drawString(65*mm, section_start_y - 45*mm, "NMI")
    c.drawString(100*mm, section_start_y - 45*mm, "Meter No.")
    c.drawString(135*mm, section_start_y - 45*mm, "AEMO Metering Provider I.D.")
        # Redraw all field boxes on top of green background
    draw_field(c, 21*mm, section_start_y - 24*mm, 168*mm, 5*mm, form_data.get('property_name', ''))
    draw_field(c, 21*mm, section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, section_start_y - 32*mm, 35*mm, 5*mm, form_data.get('install_street_number', ''))
    draw_field(c, 128*mm, section_start_y - 32*mm, 61*mm, 5*mm, '')
    draw_field(c, 21*mm, section_start_y - 40*mm, 85*mm, 5*mm, form_data.get('install_street_name', ''))
    draw_field(c, 109*mm, section_start_y - 40*mm, 80*mm, 5*mm, '')
    draw_field(c, 21*mm, section_start_y - 48*mm, 85*mm, 5*mm, form_data.get('install_suburb', ''))
    draw_field(c, 109*mm, section_start_y - 48*mm, 42*mm, 5*mm, form_data.get('install_state', ''))
    draw_field(c, 154*mm, section_start_y - 48*mm, 35*mm, 5*mm, form_data.get('install_postcode', ''))
    draw_field(c, 21*mm, section_start_y - 56*mm, 40*mm, 5*mm, '')
    draw_field(c, 64*mm, section_start_y - 56*mm, 32*mm, 5*mm, '')
    draw_field(c, 99*mm, section_start_y - 56*mm, 32*mm, 5*mm, '')
    draw_field(c, 134*mm, section_start_y - 56*mm, 55*mm, 5*mm, '')
    
    # ========== CUSTOMER DETAILS SECTION ==========
    y -= 12*mm
    cust_section_start_y = y
    cust_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "*First Name")
    c.drawString(115*mm, y, "*Last Name")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('customer_first_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, form_data.get('customer_last_name', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Company Name")
    y -= 5*mm
    draw_field(c, 21*mm, y, 168*mm, 5*mm, form_data.get('customer_company_name', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Floor")
    c.drawString(48*mm, y, "Unit")
    c.drawString(77*mm, y, "*Street Number")
    c.drawString(115*mm, y, "&/or")
    c.drawString(130*mm, y, "Lot/RMB")
    y -= 5*mm
    draw_field(c, 21*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, y, 35*mm, 5*mm, form_data.get('customer_street_number', ''))
    draw_field(c, 128*mm, y, 61*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Street Name")
    c.drawString(115*mm, y, "Nearest Cross Street")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('customer_street_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Suburb")
    c.drawString(115*mm, y, "*State")
    c.drawString(155*mm, y, "*Post Code")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('customer_suburb', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('customer_state', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('customer_postcode', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Email")
    c.drawString(115*mm, y, "Office No.")
    c.drawString(155*mm, y, "Mobile No.")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('customer_email', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('customer_office_phone', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('customer_mobile_phone', ''))
    
    # Draw green background for Customer Details
    cust_section_end_y = y - 2*mm
    cust_section_height = cust_section_start_y - cust_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.rect(20*mm, cust_section_end_y, 170*mm, cust_section_height, stroke=1, fill=1)
    
    # Draw header and labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, cust_header_y, "CUSTOMER DETAILS")
    
    # Draw labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, cust_section_start_y - 13*mm, "*First Name")
    c.drawString(110*mm, cust_section_start_y - 13*mm, "*Last Name")
    c.drawString(22*mm, cust_section_start_y - 21*mm, "Company Name")
    c.drawString(22*mm, cust_section_start_y - 29*mm, "Floor")
    c.drawString(48*mm, cust_section_start_y - 29*mm, "Unit")
    c.drawString(74*mm, cust_section_start_y - 29*mm, "*Street Number")
    c.drawString(115*mm, cust_section_start_y - 29*mm, "&/or")
    c.drawString(129*mm, cust_section_start_y - 29*mm, "Lot/RMB")
    c.drawString(22*mm, cust_section_start_y - 37*mm, "*Street Name")
    c.drawString(110*mm, cust_section_start_y - 37*mm, "Nearest Cross Street")
    c.drawString(22*mm, cust_section_start_y - 45*mm, "*Suburb")
    c.drawString(110*mm, cust_section_start_y - 45*mm, "*State")
    c.drawString(155*mm, cust_section_start_y - 45*mm, "*Post Code")
    c.drawString(22*mm, cust_section_start_y - 53*mm, "Email")
    c.drawString(115*mm, cust_section_start_y - 53*mm, "Office No.")
    c.drawString(155*mm, cust_section_start_y - 53*mm, "Mobile No.")
    
    # Redraw all field boxes on top of green background
    draw_field(c, 21*mm, cust_section_start_y - 24*mm, 85*mm, 5*mm, form_data.get('customer_first_name', ''))
    draw_field(c, 109*mm, cust_section_start_y - 24*mm, 80*mm, 5*mm, form_data.get('customer_last_name', ''))
    draw_field(c, 21*mm, cust_section_start_y - 32*mm, 168*mm, 5*mm, form_data.get('customer_company_name', ''))
    draw_field(c, 21*mm, cust_section_start_y - 40*mm, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, cust_section_start_y - 40*mm, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, cust_section_start_y - 40*mm, 35*mm, 5*mm, form_data.get('customer_street_number', ''))
    draw_field(c, 128*mm, cust_section_start_y - 40*mm, 61*mm, 5*mm, '')
    draw_field(c, 21*mm, cust_section_start_y - 48*mm, 85*mm, 5*mm, form_data.get('customer_street_name', ''))
    draw_field(c, 109*mm, cust_section_start_y - 48*mm, 80*mm, 5*mm, '')
    draw_field(c, 21*mm, cust_section_start_y - 56*mm, 85*mm, 5*mm, form_data.get('customer_suburb', ''))
    draw_field(c, 109*mm, cust_section_start_y - 56*mm, 42*mm, 5*mm, form_data.get('customer_state', ''))
    draw_field(c, 154*mm, cust_section_start_y - 56*mm, 35*mm, 5*mm, form_data.get('customer_postcode', ''))
    draw_field(c, 21*mm, cust_section_start_y - 64*mm, 90*mm, 5*mm, form_data.get('customer_email', ''))
    draw_field(c, 114*mm, cust_section_start_y - 64*mm, 37*mm, 5*mm, form_data.get('customer_office_phone', ''))
    draw_field(c, 154*mm, cust_section_start_y - 64*mm, 35*mm, 5*mm, form_data.get('customer_mobile_phone', ''))
    
    # ========== INSTALLATION DETAILS SECTION ==========
    y -= 12*mm
    inst_section_start_y = y
    inst_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "*Type of Installation")
    y -= 5*mm
    
    inst_type = form_data.get('installation_type', '')
    c.setFont("Helvetica", 8)
    draw_checkbox(c, 25*mm, y, checked=(inst_type == 'Residential'))
    c.drawString(30*mm, y + 0.5*mm, "Residential")
    draw_checkbox(c, 55*mm, y, checked=(inst_type == 'Commercial'))
    c.drawString(60*mm, y + 0.5*mm, "Commercial")
    draw_checkbox(c, 90*mm, y, checked=(inst_type == 'Industrial'))
    c.drawString(95*mm, y + 0.5*mm, "Industrial")
    draw_checkbox(c, 120*mm, y, checked=(inst_type == 'Rural'))
    c.drawString(125*mm, y + 0.5*mm, "Rural")
    draw_checkbox(c, 145*mm, y, checked=(inst_type == 'Mixed Development'))
    c.drawString(150*mm, y + 0.5*mm, "Mixed Development")
    
    y -= 7*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "*Work carried out")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    draw_checkbox(c, 60*mm, y, checked=form_data.get('work_new_work') == 'yes')
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
    draw_field(c, 135*mm, y - 1*mm, 54*mm, 5*mm, form_data.get('non_compliance_no', ''))
    
    y -= 7*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "Special Conditions")
    y -= 5*mm
    
    c.setFont("Helvetica", 8)
    draw_checkbox(c, 75*mm, y, checked=form_data.get('special_over_100_amps') == 'yes')
    c.drawString(80*mm, y + 0.5*mm, "Over 100 amps")
    draw_checkbox(c, 125*mm, y, checked=form_data.get('special_hazardous_area') == 'yes')
    c.drawString(130*mm, y + 0.5*mm, "Hazardous Area")
    draw_checkbox(c, 155*mm, y, checked=form_data.get('special_off_grid') == 'yes')
    c.drawString(160*mm, y + 0.5*mm, "Off Grid Install")
    
    y -= 5*mm
    draw_checkbox(c, 75*mm, y, checked=form_data.get('special_high_voltage') == 'yes')
    c.drawString(80*mm, y + 0.5*mm, "High Voltage")
    draw_checkbox(c, 125*mm, y, checked=form_data.get('special_unmetered') == 'yes')
    c.drawString(130*mm, y + 0.5*mm, "Unmetered Supply")
    draw_checkbox(c, 155*mm, y, checked=form_data.get('special_secondary_power') == 'yes')
    c.drawString(160*mm, y + 0.5*mm, "Secondary M")
    
    # Draw green background for Installation Details
    inst_section_end_y = y - 2*mm
    inst_section_height = inst_section_start_y - inst_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.rect(20*mm, inst_section_end_y, 170*mm, inst_section_height, stroke=1, fill=1)
    
    # Draw header and labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, inst_header_y, "INSTALLATION DETAILS")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, inst_section_start_y - 10*mm, "*Type of Installation")
    c.drawString(22*mm, inst_section_start_y - 22*mm, "*Work carried out")
    c.drawString(22*mm, inst_section_start_y - 39*mm, "Special Conditions")
    
    # Redraw all checkboxes and fields on top of green background
    c.setFont("Helvetica", 8)
    y_inst = inst_section_start_y - 15*mm
    draw_checkbox(c, 25*mm, y_inst, checked=(inst_type == 'Residential'))
    c.setFillColor(white)
    c.drawString(30*mm, y_inst + 0.5*mm, "Residential")
    draw_checkbox(c, 55*mm, y_inst, checked=(inst_type == 'Commercial'))
    c.drawString(60*mm, y_inst + 0.5*mm, "Commercial")
    draw_checkbox(c, 90*mm, y_inst, checked=(inst_type == 'Industrial'))
    c.drawString(95*mm, y_inst + 0.5*mm, "Industrial")
    draw_checkbox(c, 120*mm, y_inst, checked=(inst_type == 'Rural'))
    c.drawString(125*mm, y_inst + 0.5*mm, "Rural")
    draw_checkbox(c, 145*mm, y_inst, checked=(inst_type == 'Mixed Development'))
    c.drawString(150*mm, y_inst + 0.5*mm, "Mixed Development")
    
    y_inst -= 7*mm
    draw_checkbox(c, 60*mm, y_inst, checked=form_data.get('work_new_work') == 'yes')
    c.drawString(65*mm, y_inst + 0.5*mm, "New Work")
    draw_checkbox(c, 100*mm, y_inst, checked=form_data.get('work_installed_meter') == 'yes')
    c.drawString(105*mm, y_inst + 0.5*mm, "Installed Meter")
    draw_checkbox(c, 145*mm, y_inst, checked=form_data.get('work_network_connection') == 'yes')
    c.drawString(150*mm, y_inst + 0.5*mm, "Network connection")
    
    y_inst -= 5*mm
    draw_checkbox(c, 25*mm, y_inst, checked=form_data.get('work_addition_alteration') == 'yes')
    c.drawString(30*mm, y_inst + 0.5*mm, "Addition/alteration to existing")
    draw_checkbox(c, 100*mm, y_inst, checked=form_data.get('work_advanced_meter') == 'yes')
    c.drawString(105*mm, y_inst + 0.5*mm, "Install Advanced Meter")
    draw_checkbox(c, 145*mm, y_inst, checked=form_data.get('work_ev_connection') == 'yes')
    c.drawString(150*mm, y_inst + 0.5*mm, "EV Connection")
    
    y_inst -= 5*mm
    draw_checkbox(c, 25*mm, y_inst, checked=form_data.get('work_reinspection') == 'yes')
    c.drawString(30*mm, y_inst + 0.5*mm, "Re-inspection of non-compliant work")
    c.drawString(100*mm, y_inst + 0.5*mm, "Non-Compliance No.")
    draw_field(c, 135*mm, y_inst - 1*mm, 54*mm, 5*mm, form_data.get('non_compliance_no', ''))
    
    y_inst -= 7*mm
    draw_checkbox(c, 75*mm, y_inst, checked=form_data.get('special_over_100_amps') == 'yes')
    c.setFillColor(white)
    c.drawString(80*mm, y_inst + 0.5*mm, "Over 100 amps")
    draw_checkbox(c, 125*mm, y_inst, checked=form_data.get('special_hazardous_area') == 'yes')
    c.drawString(130*mm, y_inst + 0.5*mm, "Hazardous Area")
    draw_checkbox(c, 170*mm, y_inst, checked=form_data.get('special_off_grid') == 'yes')
    c.drawString(175*mm, y_inst + 0.5*mm, "Off Grid Installation")
    
    y_inst -= 5*mm
    draw_checkbox(c, 75*mm, y_inst, checked=form_data.get('special_high_voltage') == 'yes')
    c.drawString(80*mm, y_inst + 0.5*mm, "High Voltage")
    draw_checkbox(c, 125*mm, y_inst, checked=form_data.get('special_unmetered') == 'yes')
    c.drawString(130*mm, y_inst + 0.5*mm, "Unmetered Supply")
    draw_checkbox(c, 170*mm, y_inst, checked=form_data.get('special_secondary_power') == 'yes')
    c.drawString(175*mm, y_inst + 0.5*mm, "Secondary Power Supply")
    
    # Redraw page 1 header and title in BLACK on top of everything
    c.setFillColor(HexColor('#C41E3A'))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, height - 25*mm, "NSW")
    c.setFillColor(black)
    c.drawString(35*mm, height - 25*mm, "Fair Trading")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150*mm, height - 25*mm, "*Serial No:")
    draw_field(c, 170*mm, height - 28*mm, 20*mm, 5*mm, form_data.get('serial_no', ''))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, height - 35*mm, "Online Certificate Compliance Electrical Work (CCEW)")
    c.setFont("Helvetica", 8)
    c.setFillColor(black)
    c.drawString(20*mm, height - 40*mm, "Any field marked with an * is mandatory")
    
    # ========== PAGE 2 ==========
    c.showPage()
    y = height - 20*mm
    
    # ========== EQUIPMENT SECTION ==========
    equip_section_start_y = y
    equip_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica", 8)
    c.drawString(22*mm, y, "Select equipment installed and estimate increase of work affected by the work carried out")
    
    y -= 7*mm
    # Equipment table header
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "EQUIPMENT")
    c.drawString(75*mm, y, "RATING")
    c.drawString(110*mm, y, "NUMBER INSTALLED")
    c.drawString(150*mm, y, "PARTICULARS")
    
    y -= 5*mm
    # Equipment rows
    equipment = [
        ('Switchboard', 'equip_switchboard', 'equip_switchboard_rating', 'equip_switchboard_number', 'equip_switchboard_particulars'),
        ('Circuits', 'equip_circuits', 'equip_circuits_rating', 'equip_circuits_number', 'equip_circuits_particulars'),
        ('Lighting', 'equip_lighting', 'equip_lighting_rating', 'equip_lighting_number', 'equip_lighting_particulars'),
        ('Socket Outlets', 'equip_sockets', 'equip_sockets_rating', 'equip_sockets_number', 'equip_sockets_particulars'),
        ('Appliances', 'equip_appliances', 'equip_appliances_rating', 'equip_appliances_number', 'equip_appliances_particulars'),
        ('Generation', 'equip_generation', 'equip_generation_rating', 'equip_generation_number', 'equip_generation_particulars'),
        ('Storage', 'equip_storage', 'equip_storage_rating', 'equip_storage_number', 'equip_storage_particulars'),
    ]
    
    c.setFont("Helvetica", 8)
    for name, check_field, rating_field, number_field, particulars_field in equipment:
        draw_checkbox(c, 22*mm, y, checked=form_data.get(check_field) == 'yes')
        c.drawString(27*mm, y + 0.5*mm, name)
        draw_field(c, 72*mm, y, 32*mm, 5*mm, form_data.get(rating_field, ''))
        draw_field(c, 107*mm, y, 35*mm, 5*mm, form_data.get(number_field, ''))
        draw_field(c, 145*mm, y, 44*mm, 5*mm, form_data.get(particulars_field, ''))
        y -= 6*mm
    
    # Draw green background for Equipment
    equip_section_end_y = y
    equip_section_height = equip_section_start_y - equip_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, equip_section_end_y, 170*mm, equip_section_height, stroke=1, fill=1)
    
    # Draw header and labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, equip_header_y, "*DETAILS OF EQUIPMENT")
    c.setFont("Helvetica", 8)
    c.drawString(22*mm, equip_section_start_y - 10*mm, "Select equipment installed and estimate increase of work affected by the work carried out")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, equip_section_start_y - 19*mm, "EQUIPMENT")
    c.drawString(75*mm, equip_section_start_y - 19*mm, "RATING")
    c.drawString(110*mm, equip_section_start_y - 19*mm, "NUMBER INSTALLED")
    c.drawString(150*mm, equip_section_start_y - 19*mm, "PARTICULARS")
    
    # Redraw equipment rows on top of green background
    y_row = equip_section_start_y - 22*mm
    c.setFont("Helvetica", 8)
    for name, check_field, rating_field, number_field, particulars_field in equipment:
        draw_checkbox(c, 22*mm, y_row, checked=form_data.get(check_field) == 'yes')
        c.setFillColor(white)
        c.drawString(27*mm, y_row + 0.5*mm, name)
        draw_field(c, 72*mm, y_row, 32*mm, 5*mm, form_data.get(rating_field, ''))
        draw_field(c, 107*mm, y_row, 35*mm, 5*mm, form_data.get(number_field, ''))
        draw_field(c, 145*mm, y_row, 44*mm, 5*mm, form_data.get(particulars_field, ''))
        y_row -= 6*mm
    
    # ========== METERS SECTION ==========
    y -= 5*mm
    meters_section_start_y = y
    meters_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "Master/Sub Status - No (N), Master (M), Sub (S)")
    
    y -= 5*mm
    # Meters table header
    c.setFont("Helvetica-Bold", 7)
    c.drawString(22*mm, y, "I")
    c.drawString(27*mm, y, "R")
    c.drawString(32*mm, y, "E")
    c.drawString(40*mm, y, "Meter No.")
    c.drawString(65*mm, y, "No. Dials")
    c.drawString(85*mm, y, "Master/Sub Status")
    c.drawString(115*mm, y, "Wired as Master/Sub")
    c.drawString(145*mm, y, "Register No.")
    c.drawString(165*mm, y, "Reading")
    c.drawString(180*mm, y, "Tariff")
    
    y -= 5*mm
    # Meter rows - display data from up to 4 meters
    c.setFont("Helvetica", 7)
    
    meters_data = [
        {
            'i': form_data.get('meter_1_i') == 'yes',
            'r': form_data.get('meter_1_r') == 'yes',
            'e': form_data.get('meter_1_e') == 'yes',
            'number': form_data.get('meter_1_number', ''),
            'dials': form_data.get('meter_1_dials', ''),
            'master_sub': form_data.get('meter_1_master_sub', ''),
            'wired_as': form_data.get('meter_1_wired_as', ''),
            'register': form_data.get('meter_1_register', ''),
            'reading': form_data.get('meter_1_reading', ''),
            'tariff': form_data.get('meter_1_tariff', '')
        },
        {
            'i': form_data.get('meter_2_i') == 'yes',
            'r': form_data.get('meter_2_r') == 'yes',
            'e': form_data.get('meter_2_e') == 'yes',
            'number': form_data.get('meter_2_number', ''),
            'dials': form_data.get('meter_2_dials', ''),
            'master_sub': form_data.get('meter_2_master_sub', ''),
            'wired_as': form_data.get('meter_2_wired_as', ''),
            'register': form_data.get('meter_2_register', ''),
            'reading': form_data.get('meter_2_reading', ''),
            'tariff': form_data.get('meter_2_tariff', '')
        },
        {
            'i': form_data.get('meter_3_i') == 'yes',
            'r': form_data.get('meter_3_r') == 'yes',
            'e': form_data.get('meter_3_e') == 'yes',
            'number': form_data.get('meter_3_number', ''),
            'dials': form_data.get('meter_3_dials', ''),
            'master_sub': form_data.get('meter_3_master_sub', ''),
            'wired_as': form_data.get('meter_3_wired_as', ''),
            'register': form_data.get('meter_3_register', ''),
            'reading': form_data.get('meter_3_reading', ''),
            'tariff': form_data.get('meter_3_tariff', '')
        },
        {
            'i': form_data.get('meter_4_i') == 'yes',
            'r': form_data.get('meter_4_r') == 'yes',
            'e': form_data.get('meter_4_e') == 'yes',
            'number': form_data.get('meter_4_number', ''),
            'dials': form_data.get('meter_4_dials', ''),
            'master_sub': form_data.get('meter_4_master_sub', ''),
            'wired_as': form_data.get('meter_4_wired_as', ''),
            'register': form_data.get('meter_4_register', ''),
            'reading': form_data.get('meter_4_reading', ''),
            'tariff': form_data.get('meter_4_tariff', '')
        }
    ]
    
    # Draw 8 rows (4 with data, 4 empty)
    for i in range(8):
        if i < 4:
            meter = meters_data[i]
            draw_checkbox(c, 22*mm, y, size=2.5*mm, checked=meter['i'])
            draw_checkbox(c, 27*mm, y, size=2.5*mm, checked=meter['r'])
            draw_checkbox(c, 32*mm, y, size=2.5*mm, checked=meter['e'])
            draw_field(c, 37*mm, y, 24*mm, 4*mm, meter['number'])
            draw_field(c, 63*mm, y, 18*mm, 4*mm, meter['dials'])
            draw_field(c, 83*mm, y, 28*mm, 4*mm, meter['master_sub'])
            draw_field(c, 113*mm, y, 28*mm, 4*mm, meter['wired_as'])
            draw_field(c, 143*mm, y, 18*mm, 4*mm, meter['register'])
            draw_field(c, 163*mm, y, 13*mm, 4*mm, meter['reading'])
            draw_field(c, 178*mm, y, 11*mm, 4*mm, meter['tariff'])
        else:
            # Empty rows
            draw_checkbox(c, 22*mm, y, size=2.5*mm)
            draw_checkbox(c, 27*mm, y, size=2.5*mm)
            draw_checkbox(c, 32*mm, y, size=2.5*mm)
            draw_field(c, 37*mm, y, 24*mm, 4*mm, '')
            draw_field(c, 63*mm, y, 18*mm, 4*mm, '')
            draw_field(c, 83*mm, y, 28*mm, 4*mm, '')
            draw_field(c, 113*mm, y, 28*mm, 4*mm, '')
            draw_field(c, 143*mm, y, 18*mm, 4*mm, '')
            draw_field(c, 163*mm, y, 13*mm, 4*mm, '')
            draw_field(c, 178*mm, y, 11*mm, 4*mm, '')
        y -= 5*mm
    
    y -= 3*mm
    c.setFont("Helvetica-Bold", 8)
    y_load_increase = y
    c.drawString(22*mm, y, "Estimated increase in load A/ph")
    draw_field(c, 75*mm, y - 2*mm, 30*mm, 5*mm, form_data.get('load_increase', ''))
    
    y -= 7*mm
    y_first_question = y
    c.drawString(22*mm, y, "* Is increased load within capacity of installation/service mains?")
    c.drawString(125*mm, y, "Yes")
    draw_checkbox(c, 135*mm, y - 1*mm, checked=form_data.get('load_within_capacity') == 'Yes')
    c.drawString(145*mm, y, "No")
    draw_checkbox(c, 155*mm, y - 1*mm, checked=form_data.get('load_within_capacity') == 'No')
    
    y -= 6*mm
    y_second_question = y
    c.drawString(22*mm, y, "* Is work connected to supply? (pending DSNP Inspection)")
    c.drawString(125*mm, y, "Yes")
    draw_checkbox(c, 135*mm, y - 1*mm, checked=form_data.get('work_connected_supply') == 'Yes')
    c.drawString(145*mm, y, "No")
    draw_checkbox(c, 155*mm, y - 1*mm, checked=form_data.get('work_connected_supply') == 'No')
    
    # Draw green background for Meters
    meters_section_end_y = y - 2*mm
    meters_section_height = meters_section_start_y - meters_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, meters_section_end_y, 170*mm, meters_section_height, stroke=1, fill=1)
    
    # Draw header and labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, meters_header_y, "*Meters - Installed (I), Removed (R), Existing (E)")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, meters_section_start_y - 10*mm, "Master/Sub Status - No (N), Master (M), Sub (S)")
    c.setFont("Helvetica-Bold", 7)
    c.drawString(22*mm, meters_section_start_y - 13*mm, "I")
    c.drawString(27*mm, meters_section_start_y - 13*mm, "R")
    c.drawString(32*mm, meters_section_start_y - 13*mm, "E")
    c.drawString(40*mm, meters_section_start_y - 13*mm, "Meter No.")
    c.drawString(65*mm, meters_section_start_y - 13*mm, "No. Dials")
    c.drawString(85*mm, meters_section_start_y - 13*mm, "Master/Sub Status")
    c.drawString(115*mm, meters_section_start_y - 13*mm, "Wired as Master/Sub")
    c.drawString(145*mm, meters_section_start_y - 13*mm, "Register No.")
    c.drawString(165*mm, meters_section_start_y - 13*mm, "Reading")
    c.drawString(180*mm, meters_section_start_y - 13*mm, "Tariff")
    
    # Redraw all meter rows on top of green background
    y_meter = meters_section_start_y - 20*mm
    c.setFont("Helvetica", 7)
    for i in range(8):
        if i < 4:
            meter = meters_data[i]
            draw_checkbox(c, 22*mm, y_meter, size=2.5*mm, checked=meter['i'])
            draw_checkbox(c, 27*mm, y_meter, size=2.5*mm, checked=meter['r'])
            draw_checkbox(c, 32*mm, y_meter, size=2.5*mm, checked=meter['e'])
            draw_field(c, 37*mm, y_meter, 24*mm, 4*mm, meter['number'])
            draw_field(c, 63*mm, y_meter, 18*mm, 4*mm, meter['dials'])
            draw_field(c, 83*mm, y_meter, 28*mm, 4*mm, meter['master_sub'])
            draw_field(c, 113*mm, y_meter, 28*mm, 4*mm, meter['wired_as'])
            draw_field(c, 143*mm, y_meter, 18*mm, 4*mm, meter['register'])
            draw_field(c, 163*mm, y_meter, 13*mm, 4*mm, meter['reading'])
            draw_field(c, 178*mm, y_meter, 11*mm, 4*mm, meter['tariff'])
        else:
            # Empty rows
            draw_checkbox(c, 22*mm, y_meter, size=2.5*mm)
            draw_checkbox(c, 27*mm, y_meter, size=2.5*mm)
            draw_checkbox(c, 32*mm, y_meter, size=2.5*mm)
            draw_field(c, 37*mm, y_meter, 24*mm, 4*mm, '')
            draw_field(c, 63*mm, y_meter, 18*mm, 4*mm, '')
            draw_field(c, 83*mm, y_meter, 28*mm, 4*mm, '')
            draw_field(c, 113*mm, y_meter, 28*mm, 4*mm, '')
            draw_field(c, 143*mm, y_meter, 18*mm, 4*mm, '')
            draw_field(c, 163*mm, y_meter, 13*mm, 4*mm, '')
            draw_field(c, 178*mm, y_meter, 11*mm, 4*mm, '')
        y_meter -= 5*mm
    
    # Redraw bottom section with fields and checkboxes using saved positions
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y_load_increase, "Estimated increase in load A/ph")
    draw_field(c, 75*mm, y_load_increase - 2*mm, 30*mm, 5*mm, form_data.get('load_increase', ''))
    
    c.drawString(22*mm, y_first_question, "* Is increased load within capacity of installation/service mains?")
    c.drawString(125*mm, y_first_question, "Yes")
    draw_checkbox(c, 135*mm, y_first_question - 1*mm, checked=form_data.get('load_within_capacity') == 'Yes')
    c.drawString(145*mm, y_first_question, "No")
    draw_checkbox(c, 155*mm, y_first_question - 1*mm, checked=form_data.get('load_within_capacity') == 'No')
    
    c.drawString(22*mm, y_second_question, "* Is work connected to supply? (pending DSNP Inspection)")
    c.drawString(125*mm, y_second_question, "Yes")
    draw_checkbox(c, 135*mm, y_second_question - 1*mm, checked=form_data.get('work_connected_supply') == 'Yes')
    c.drawString(145*mm, y_second_question, "No")
    draw_checkbox(c, 155*mm, y_second_question - 1*mm, checked=form_data.get('work_connected_supply') == 'No')
    
    # ========== INSTALLERS LICENSE DETAILS SECTION ==========
    y -= 10*mm
    installers_section_start_y = y
    installers_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "*First Name")
    c.drawString(115*mm, y, "*Last Name")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('installer_first_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, form_data.get('installer_last_name', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Floor")
    c.drawString(48*mm, y, "Unit")
    c.drawString(77*mm, y, "*Street Number")
    c.drawString(115*mm, y, "&/or")
    c.drawString(130*mm, y, "Lot/RMB")
    y -= 5*mm
    draw_field(c, 21*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, y, 35*mm, 5*mm, form_data.get('installer_street_number', ''))
    draw_field(c, 128*mm, y, 61*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Street Name")
    c.drawString(115*mm, y, "Nearest Cross Street")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('installer_street_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Suburb")
    c.drawString(115*mm, y, "*State")
    c.drawString(155*mm, y, "*Post Code")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('installer_suburb', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('installer_state', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('installer_postcode', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Email")
    c.drawString(115*mm, y, "*Office Phone")
    c.drawString(155*mm, y, "Mobile Phone")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('installer_email', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('installer_office_phone', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('installer_mobile_phone', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Qualified Supervisors No.")
    c.drawString(65*mm, y, "*Expiry Date")
    c.drawString(95*mm, y, "Or")
    c.drawString(105*mm, y, "*Contractor's License No.")
    c.drawString(155*mm, y, "*Expiry Date")
    y -= 5*mm
    draw_field(c, 21*mm, y, 40*mm, 5*mm, '')
    draw_field(c, 64*mm, y, 28*mm, 5*mm, '')
    draw_field(c, 104*mm, y, 47*mm, 5*mm, form_data.get('installer_license_no', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, format_date_australian(form_data.get('installer_license_expiry', '')))
    
    # Draw green background for Installers License
    installers_section_end_y = y - 2*mm
    installers_section_height = installers_section_start_y - installers_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, installers_section_end_y, 170*mm, installers_section_height, stroke=1, fill=1)
    
    # Draw header and all labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, installers_header_y, "INSTALLERS LICENSE DETAILS")
    
    c.setFont("Helvetica-Bold", 8)
    y_label = installers_section_start_y - 13*mm
    c.drawString(22*mm, y_label, "*First Name")
    c.drawString(115*mm, y_label, "*Last Name")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "Floor")
    c.drawString(48*mm, y_label, "Unit")
    c.drawString(77*mm, y_label, "*Street Number")
    c.drawString(115*mm, y_label, "&/or")
    c.drawString(130*mm, y_label, "Lot/RMB")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Street Name")
    c.drawString(115*mm, y_label, "Nearest Cross Street")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Suburb")
    c.drawString(115*mm, y_label, "*State")
    c.drawString(155*mm, y_label, "*Post Code")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Email")
    c.drawString(115*mm, y_label, "*Office Phone")
    c.drawString(155*mm, y_label, "Mobile Phone")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Qualified Supervisors No.")
    c.drawString(65*mm, y_label, "*Expiry Date")
    c.drawString(95*mm, y_label, "Or")
    c.drawString(105*mm, y_label, "*Contractor's License No.")
    c.drawString(155*mm, y_label, "*Expiry Date")
    
    # Redraw all field boxes on top of green background
    draw_field(c, 21*mm, installers_section_start_y - 24*mm, 85*mm, 5*mm, form_data.get('installer_first_name', ''))
    draw_field(c, 109*mm, installers_section_start_y - 24*mm, 80*mm, 5*mm, form_data.get('installer_last_name', ''))
    draw_field(c, 21*mm, installers_section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, installers_section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, installers_section_start_y - 32*mm, 35*mm, 5*mm, form_data.get('installer_street_number', ''))
    draw_field(c, 128*mm, installers_section_start_y - 32*mm, 61*mm, 5*mm, '')
    draw_field(c, 21*mm, installers_section_start_y - 40*mm, 85*mm, 5*mm, form_data.get('installer_street_name', ''))
    draw_field(c, 109*mm, installers_section_start_y - 40*mm, 80*mm, 5*mm, '')
    draw_field(c, 21*mm, installers_section_start_y - 48*mm, 85*mm, 5*mm, form_data.get('installer_suburb', ''))
    draw_field(c, 109*mm, installers_section_start_y - 48*mm, 42*mm, 5*mm, form_data.get('installer_state', ''))
    draw_field(c, 154*mm, installers_section_start_y - 48*mm, 35*mm, 5*mm, form_data.get('installer_postcode', ''))
    draw_field(c, 21*mm, installers_section_start_y - 56*mm, 85*mm, 5*mm, form_data.get('installer_email', ''))
    draw_field(c, 109*mm, installers_section_start_y - 56*mm, 42*mm, 5*mm, form_data.get('installer_office_phone', ''))
    draw_field(c, 154*mm, installers_section_start_y - 56*mm, 35*mm, 5*mm, form_data.get('installer_mobile_phone', ''))
    draw_field(c, 21*mm, installers_section_start_y - 64*mm, 40*mm, 5*mm, '')
    draw_field(c, 64*mm, installers_section_start_y - 64*mm, 28*mm, 5*mm, '')
    draw_field(c, 104*mm, installers_section_start_y - 64*mm, 47*mm, 5*mm, form_data.get('installer_license_no', ''))
    draw_field(c, 154*mm, installers_section_start_y - 64*mm, 35*mm, 5*mm, format_date_australian(form_data.get('installer_license_expiry', '')))
    
    # ========== PAGE 3 ==========
    c.showPage()
    y = height - 20*mm
    
    # ========== TEST REPORT SECTION ==========
    test_section_start_y = y
    test_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica", 8)
    c.drawString(22*mm, y, "In respect to the test carried out by me on the above mentioned installation, I certify that:")
    y -= 5*mm
    c.drawString(22*mm, y, "1.  I have carried out the test below and that the installation has passed the following requirements:")
    y -= 5*mm
    
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
    y -= 7*mm
    
    c.drawString(22*mm, y, "2.  I confirm that I have visually checked that the installation described in this Certificate complies with the")
    y -= 4*mm
    c.drawString(26*mm, y, "relevant Acts, Regulations, Codes and Standards:")
    y -= 7*mm
    
    c.drawString(22*mm, y, "3.  *The test was completed on")
    draw_field(c, 70*mm, y - 2*mm, 40*mm, 5*mm, format_date_australian(form_data.get('test_date', '')))
    
    # Draw green background for Test Report
    test_section_end_y = y - 2*mm
    test_section_height = test_section_start_y - test_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, test_section_end_y, 170*mm, test_section_height, stroke=1, fill=1)
    
    # Draw header and all text in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, test_header_y, "*TEST REPORT")
    
    c.setFont("Helvetica", 8)
    y_text = test_section_start_y - 10*mm
    c.drawString(22*mm, y_text, "In respect to the test carried out by me on the above mentioned installation, I certify that:")
    y_text -= 5*mm
    c.drawString(22*mm, y_text, "1.  I have carried out the test below and that the installation has passed the following requirements:")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Earthing system integrity")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Residual current device operational")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Insulation resistance Mohms")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Visual check that installation is suitable for connection to supply")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Polarity")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Stand-Alone system complies with AS4509")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Correct current connections")
    y_text -= 5*mm
    c.drawString(30*mm, y_text + 0.5*mm, "Fault loop impedance (if necessary)")
    y_text -= 7*mm
    c.drawString(22*mm, y_text, "2.  I confirm that I have visually checked that the installation described in this Certificate complies with the")
    y_text -= 4*mm
    c.drawString(26*mm, y_text, "relevant Acts, Regulations, Codes and Standards:")
    y_text -= 7*mm
    c.drawString(22*mm, y_text, "3.  *The test was completed on")
    
    # Redraw test date field on top of green background
    draw_field(c, 70*mm, y_text - 2*mm, 40*mm, 5*mm, format_date_australian(form_data.get('test_date', '')))
    
    # Redraw all checkboxes on top of green background
    y_check = test_section_start_y - 15*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_earthing') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_rcd') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_insulation') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_visual') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_polarity') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_standalone') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_current') == 'yes')
    y_check -= 5*mm
    draw_checkbox(c, 25*mm, y_check, checked=form_data.get('test_fault_loop') == 'yes')
    
    # ========== TESTERS LICENSE DETAILS SECTION ==========
    y -= 12*mm
    testers_section_start_y = y
    testers_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica-Bold", 8)
    c.drawString(22*mm, y, "*First Name")
    c.drawString(115*mm, y, "*Last Name")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('tester_first_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, form_data.get('tester_last_name', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Floor")
    c.drawString(48*mm, y, "Unit")
    c.drawString(77*mm, y, "*Street Number")
    c.drawString(115*mm, y, "&/or")
    c.drawString(130*mm, y, "Lot/RMB")
    y -= 5*mm
    draw_field(c, 21*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, y, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, y, 35*mm, 5*mm, form_data.get('tester_street_number', ''))
    draw_field(c, 128*mm, y, 61*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Street Name")
    c.drawString(115*mm, y, "Nearest Cross Street")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('tester_street_name', ''))
    draw_field(c, 109*mm, y, 80*mm, 5*mm, '')
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Suburb")
    c.drawString(115*mm, y, "*State")
    c.drawString(155*mm, y, "*Post Code")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('tester_suburb', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('tester_state', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('tester_postcode', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Email")
    c.drawString(115*mm, y, "Office Phone")
    c.drawString(155*mm, y, "Mobile Phone")
    y -= 5*mm
    draw_field(c, 21*mm, y, 85*mm, 5*mm, form_data.get('tester_email', ''))
    draw_field(c, 109*mm, y, 42*mm, 5*mm, form_data.get('tester_office_phone', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, form_data.get('tester_mobile_phone', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "*Qualified Supervisors No.")
    c.drawString(65*mm, y, "*Expiry Date")
    c.drawString(95*mm, y, "Or")
    c.drawString(105*mm, y, "*Contractor's License No.")
    c.drawString(155*mm, y, "*Expiry Date")
    y -= 5*mm
    draw_field(c, 21*mm, y, 40*mm, 5*mm, '')
    draw_field(c, 64*mm, y, 28*mm, 5*mm, '')
    draw_field(c, 104*mm, y, 47*mm, 5*mm, form_data.get('tester_license_no', ''))
    draw_field(c, 154*mm, y, 35*mm, 5*mm, format_date_australian(form_data.get('tester_license_expiry', '')))
    
    y -= 10*mm
    c.setFont("Helvetica", 8)
    c.drawString(21*mm, y, "In my capacity as the Tester, I certify that the electrical work carried out on the above mentioned property")
    y -= 4*mm
    c.drawString(21*mm, y, "was completed by the nominated electrician")
    
    # Draw green background for Testers License
    testers_section_end_y = y - 2*mm
    testers_section_height = testers_section_start_y - testers_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, testers_section_end_y, 170*mm, testers_section_height, stroke=1, fill=1)
    
    # Draw header and all labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, testers_header_y, "TESTERS LICENSE DETAILS")
    
    c.setFont("Helvetica-Bold", 8)
    y_label = testers_section_start_y - 13*mm
    c.drawString(22*mm, y_label, "*First Name")
    c.drawString(115*mm, y_label, "*Last Name")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "Floor")
    c.drawString(48*mm, y_label, "Unit")
    c.drawString(77*mm, y_label, "*Street Number")
    c.drawString(115*mm, y_label, "&/or")
    c.drawString(130*mm, y_label, "Lot/RMB")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Street Name")
    c.drawString(115*mm, y_label, "Nearest Cross Street")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Suburb")
    c.drawString(115*mm, y_label, "*State")
    c.drawString(155*mm, y_label, "*Post Code")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Email")
    c.drawString(115*mm, y_label, "Office Phone")
    c.drawString(155*mm, y_label, "Mobile Phone")
    
    y_label -= 8*mm
    c.drawString(22*mm, y_label, "*Qualified Supervisors No.")
    c.drawString(65*mm, y_label, "*Expiry Date")
    c.drawString(95*mm, y_label, "Or")
    c.drawString(105*mm, y_label, "*Contractor's License No.")
    c.drawString(155*mm, y_label, "*Expiry Date")
    
    y_label -= 13*mm
    c.setFont("Helvetica", 8)
    c.drawString(21*mm, y_label, "In my capacity as the Tester, I certify that the electrical work carried out on the above mentioned property")
    y_label -= 4*mm
    c.drawString(21*mm, y_label, "was completed by the nominated electrician")
    
    # Redraw all field boxes on top of green background
    draw_field(c, 21*mm, testers_section_start_y - 24*mm, 85*mm, 5*mm, form_data.get('tester_first_name', ''))
    draw_field(c, 109*mm, testers_section_start_y - 24*mm, 80*mm, 5*mm, form_data.get('tester_last_name', ''))
    draw_field(c, 21*mm, testers_section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 47*mm, testers_section_start_y - 32*mm, 23*mm, 5*mm, '')
    draw_field(c, 73*mm, testers_section_start_y - 32*mm, 35*mm, 5*mm, form_data.get('tester_street_number', ''))
    draw_field(c, 128*mm, testers_section_start_y - 32*mm, 61*mm, 5*mm, '')
    draw_field(c, 21*mm, testers_section_start_y - 40*mm, 85*mm, 5*mm, form_data.get('tester_street_name', ''))
    draw_field(c, 109*mm, testers_section_start_y - 40*mm, 80*mm, 5*mm, '')
    draw_field(c, 21*mm, testers_section_start_y - 48*mm, 85*mm, 5*mm, form_data.get('tester_suburb', ''))
    draw_field(c, 109*mm, testers_section_start_y - 48*mm, 42*mm, 5*mm, form_data.get('tester_state', ''))
    draw_field(c, 154*mm, testers_section_start_y - 48*mm, 35*mm, 5*mm, form_data.get('tester_postcode', ''))
    draw_field(c, 21*mm, testers_section_start_y - 56*mm, 85*mm, 5*mm, form_data.get('tester_email', ''))
    draw_field(c, 109*mm, testers_section_start_y - 56*mm, 42*mm, 5*mm, form_data.get('tester_office_phone', ''))
    draw_field(c, 154*mm, testers_section_start_y - 56*mm, 35*mm, 5*mm, form_data.get('tester_mobile_phone', ''))
    draw_field(c, 21*mm, testers_section_start_y - 64*mm, 40*mm, 5*mm, '')
    draw_field(c, 64*mm, testers_section_start_y - 64*mm, 28*mm, 5*mm, '')
    draw_field(c, 104*mm, testers_section_start_y - 64*mm, 47*mm, 5*mm, form_data.get('tester_license_no', ''))
    draw_field(c, 154*mm, testers_section_start_y - 64*mm, 35*mm, 5*mm, format_date_australian(form_data.get('tester_license_expiry', '')))
    
    # ========== SUBMIT CCEW SECTION ==========
    y -= 10*mm
    submit_section_start_y = y
    submit_header_y = y - 5*mm
    
    y -= 10*mm
    c.setFont("Helvetica", 8)
    c.drawString(22*mm, y, "Please select the energy provider for where this work has been carried out, to email a copy of this")
    y -= 4*mm
    c.drawString(22*mm, y, "CCEW directly to that provider")
    y -= 6*mm
    draw_field(c, 21*mm, y, 168*mm, 5*mm, form_data.get('energy_provider', ''))
    
    y -= 8*mm
    c.drawString(22*mm, y, "Please enter the meter providers email to send a copy of this CCEW directly to that provider")
    y -= 6*mm
    draw_field(c, 21*mm, y, 168*mm, 5*mm, '')
    
    y -= 10*mm
    c.drawString(21*mm, y, "Signature:")
    draw_field(c, 21*mm, y - 8*mm, 80*mm, 20*mm, form_data.get('signature', ''))
    
    # Draw green background for Submit CCEW
    submit_section_end_y = y - 2*mm
    submit_section_height = submit_section_start_y - submit_section_end_y
    c.setFillColor(SECTION_GREEN)
    c.setStrokeColor(black)
    c.rect(20*mm, submit_section_end_y, 170*mm, submit_section_height, stroke=1, fill=1)
    
    # Draw header and labels in white
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(22*mm, submit_header_y, "*SUBMIT CCEW")
    
    c.setFont("Helvetica", 8)
    y_text = submit_section_start_y - 10*mm
    c.drawString(22*mm, y_text, "Please select the energy provider for where this work has been carried out, to email a copy of this")
    y_text -= 4*mm
    c.drawString(22*mm, y_text, "CCEW directly to that provider")
    
    y_text -= 12*mm
    c.drawString(22*mm, y_text, "Please enter the meter providers email to send a copy of this CCEW directly to that provider")
    
    y_text -= 18*mm
    c.drawString(21*mm, y_text, "Signature:")
    
    # Redraw all field boxes on top of green background
    draw_field(c, 21*mm, submit_section_start_y - 16*mm, 168*mm, 5*mm, form_data.get('energy_provider', ''))
    draw_field(c, 21*mm, submit_section_start_y - 28*mm, 168*mm, 5*mm, '')
    draw_field(c, 21*mm, submit_section_start_y - 50*mm, 80*mm, 20*mm, form_data.get('signature', ''))
    
    # Finalize
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(pdf_bytes).decode('utf-8')
