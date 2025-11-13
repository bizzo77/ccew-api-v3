"""
CCEW PDF Generator - Using verified coordinates from user testing
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
from datetime import datetime
import base64


def create_overlay_page(form_data, page_num):
    """Create transparent overlay with data fields"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    font_size = 9
    can.setFont("Helvetica", font_size)
    can.setFillColor(colors.black)
    
    if page_num == 0:
        # PAGE 1 - Installation Address & Customer Details
        # All coordinates verified by user testing
        
        # Installation Address Section
        if form_data.get('property_name'):
            can.drawString(50, 660, form_data['property_name'])
        
        if form_data.get('install_floor'):
            can.drawString(50, 625, form_data['install_floor'])
        
        if form_data.get('install_unit'):
            can.drawString(180, 625, form_data['install_unit'])
        
        if form_data.get('install_street_number'):
            can.drawString(305, 625, form_data['install_street_number'])
        
        if form_data.get('install_lot_rmb'):
            can.drawString(435, 625, form_data['install_lot_rmb'])
        
        if form_data.get('install_street_name'):
            can.drawString(50, 590, form_data['install_street_name'])
        
        if form_data.get('nearest_cross_street'):
            can.drawString(305, 590, form_data['nearest_cross_street'])
        
        if form_data.get('install_suburb'):
            can.drawString(50, 555, form_data['install_suburb'])
        
        # Install State - COORDINATES NOT YET VERIFIED
        # if form_data.get('install_state'):
        #     can.drawString(?, ?, form_data['install_state'])
        
        if form_data.get('install_postcode'):
            can.drawString(475, 555, form_data['install_postcode'])
        
        if form_data.get('pit_pillar_pole_no'):
            can.drawString(50, 518, form_data['pit_pillar_pole_no'])
        
        if form_data.get('nmi'):
            can.drawString(180, 515, form_data['nmi'])
        
        if form_data.get('meter_no'):
            can.drawString(275, 515, form_data['meter_no'])
        
        if form_data.get('aemo_provider_id'):
            can.drawString(390, 515, form_data['aemo_provider_id'])
        
        # Customer Details Section  
        if form_data.get('customer_first_name'):
            can.drawString(50, 450, form_data['customer_first_name'])
        
        # Customer Last Name - COORDINATES NOT YET VERIFIED
        # if form_data.get('customer_last_name'):
        #     can.drawString(?, ?, form_data['customer_last_name'])
        
        if form_data.get('customer_company_name'):
            can.drawString(50, 415, form_data['customer_company_name'])
        
        if form_data.get('customer_floor'):
            can.drawString(50, 380, form_data['customer_floor'])
        
        # Customer Unit - COORDINATES NOT YET VERIFIED
        # Customer Street Number - COORDINATES NOT YET VERIFIED
        # Customer Lot/RMB - COORDINATES NOT YET VERIFIED
        
        if form_data.get('customer_street_name'):
            can.drawString(50, 345, form_data['customer_street_name'])
        
        # Customer Nearest Cross Street - COORDINATES NOT YET VERIFIED
        
        if form_data.get('customer_suburb'):
            can.drawString(50, 310, form_data['customer_suburb'])
        
        # Customer State - COORDINATES NOT YET VERIFIED
        # Customer Post Code - COORDINATES NOT YET VERIFIED
        
        if form_data.get('customer_email'):
            can.drawString(50, 275, form_data['customer_email'])
        
        # Customer Office Phone - COORDINATES NOT YET VERIFIED
        # Customer Mobile Phone - COORDINATES NOT YET VERIFIED
        
        # Installation Details - Checkboxes (coordinates not yet verified)
        # install_type = form_data.get('installation_type', 'residential').lower()
        # if 'residential' in install_type:
        #     can.drawString(?, ?, "X")
    
    elif page_num == 1:
        # PAGE 2 - Equipment Details & Installer License
        # COORDINATES NOT YET VERIFIED
        pass
    
    elif page_num == 2:
        # PAGE 3 - Test Report & Tester License
        # COORDINATES NOT YET VERIFIED
        pass
    
    can.save()
    packet.seek(0)
    return packet


def generate_ccew_pdf(form_data, template_path):
    """Generate filled CCEW PDF by overlaying data on template"""
    template_pdf = PdfReader(template_path)
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


def get_pdf_filename(job_number):
    """Generate PDF filename"""
    return f"CCEW_Form_Job_{job_number}.pdf"
