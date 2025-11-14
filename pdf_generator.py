"""
CCEW PDF Generator - Using coordinates from user measurements (IMG_7482-7488)
All coordinates transcribed from handwritten measurements on grid overlay
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
from datetime import datetime
import base64


def draw_checkbox(can, x, y, checked=False):
    """Draw a checkbox mark at given coordinates"""
    if checked:
        can.drawString(x, y, "X")


def create_overlay_page(form_data, page_num):
    """Create transparent overlay with data fields"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    font_size = 9
    can.setFont("Helvetica", font_size)
    can.setFillColor(colors.black)
    
    if page_num == 0:
        # ===== PAGE 1 =====
        
        # SERIAL NUMBER (top right header)
        if form_data.get('serial_no'):
            can.drawString(490, 762, form_data['serial_no'])
        
        # INSTALLATION ADDRESS
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
        
        # Note: State field marked as N/A by user - not implemented
        
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
        
        # CUSTOMER DETAILS
        if form_data.get('customer_first_name'):
            can.drawString(50, 450, form_data['customer_first_name'])
        
        if form_data.get('customer_last_name'):
            can.drawString(305, 450, form_data['customer_last_name'])
        
        if form_data.get('customer_company_name'):
            can.drawString(50, 415, form_data['customer_company_name'])
        
        if form_data.get('customer_floor'):
            can.drawString(50, 380, form_data['customer_floor'])
        
        if form_data.get('customer_unit'):
            can.drawString(175, 380, form_data['customer_unit'])
        
        if form_data.get('customer_street_number'):
            can.drawString(305, 380, form_data['customer_street_number'])
        
        if form_data.get('customer_lot_rmb'):
            can.drawString(435, 380, form_data['customer_lot_rmb'])
        
        if form_data.get('customer_street_name'):
            can.drawString(50, 345, form_data['customer_street_name'])
        
        if form_data.get('customer_cross_street'):
            can.drawString(305, 345, form_data['customer_cross_street'])
        
        if form_data.get('customer_suburb'):
            can.drawString(50, 310, form_data['customer_suburb'])
        
        if form_data.get('customer_state'):
            can.drawString(305, 310, form_data['customer_state'])
        
        if form_data.get('customer_postcode'):
            can.drawString(475, 310, form_data['customer_postcode'])
        
        if form_data.get('customer_email'):
            can.drawString(50, 275, form_data['customer_email'])
        
        if form_data.get('customer_office_phone'):
            can.drawString(375, 275, form_data['customer_office_phone'])
        
        if form_data.get('customer_mobile_phone'):
            can.drawString(475, 275, form_data['customer_mobile_phone'])
        
        # INSTALLATION DETAILS - Type of Installation (checkboxes)
        install_type = form_data.get('installation_type', '').lower()
        if 'residential' in install_type:
            draw_checkbox(can, 115, 205, True)
        if 'commercial' in install_type:
            draw_checkbox(can, 225, 205, True)
        if 'industrial' in install_type:
            draw_checkbox(can, 315, 205, True)
        if 'rural' in install_type:
            draw_checkbox(can, 390, 205, True)
        if 'mixed' in install_type or 'development' in install_type:
            draw_checkbox(can, 535, 205, True)
        
        # Work carried out (checkboxes) - check individual fields
        if form_data.get('work_new_work'):
            draw_checkbox(can, 205, 170, True)
        if form_data.get('work_installed_meter'):
            draw_checkbox(can, 360, 170, True)
        if form_data.get('work_network_connection'):
            draw_checkbox(can, 535, 170, True)
        if form_data.get('work_addition_alteration'):
            draw_checkbox(can, 205, 150, True)
        if form_data.get('work_advanced_meter'):
            draw_checkbox(can, 360, 150, True)
        if form_data.get('work_ev_connection'):
            draw_checkbox(can, 535, 150, True)
        if form_data.get('work_reinspection'):
            draw_checkbox(can, 240, 130, True)
        
        if form_data.get('non_compliance_no'):
            can.drawString(410, 130, form_data['non_compliance_no'])
        
        # Special Conditions (checkboxes) - check individual fields
        if form_data.get('special_over_100_amps'):
            draw_checkbox(can, 205, 90, True)
        if form_data.get('special_hazardous_area'):
            draw_checkbox(can, 360, 90, True)
        if form_data.get('special_off_grid'):
            draw_checkbox(can, 535, 90, True)
        if form_data.get('special_high_voltage'):
            draw_checkbox(can, 205, 70, True)
        if form_data.get('special_unmetered'):
            draw_checkbox(can, 360, 70, True)
        if form_data.get('special_secondary_power'):
            draw_checkbox(can, 535, 70, True)
    
    elif page_num == 1:
        # ===== PAGE 2 =====
        
        # DETAILS OF EQUIPMENT (Table)
        equipment = form_data.get('equipment', {})
        
        # Switchboard
        if equipment.get('switchboard_checked'):
            draw_checkbox(can, 45, 735, True)
        if equipment.get('switchboard_rating'):
            can.drawString(160, 735, str(equipment['switchboard_rating']))
        if equipment.get('switchboard_number'):
            can.drawString(245, 735, str(equipment['switchboard_number']))
        if equipment.get('switchboard_particulars'):
            can.drawString(365, 735, equipment['switchboard_particulars'])
        
        # Circuits
        if equipment.get('circuits_checked'):
            draw_checkbox(can, 45, 715, True)
        if equipment.get('circuits_rating'):
            can.drawString(160, 715, str(equipment['circuits_rating']))
        if equipment.get('circuits_number'):
            can.drawString(245, 715, str(equipment['circuits_number']))
        if equipment.get('circuits_particulars'):
            can.drawString(365, 715, equipment['circuits_particulars'])
        
        # Lighting
        if equipment.get('lighting_checked'):
            draw_checkbox(can, 45, 695, True)
        if equipment.get('lighting_rating'):
            can.drawString(160, 695, str(equipment['lighting_rating']))
        if equipment.get('lighting_number'):
            can.drawString(245, 695, str(equipment['lighting_number']))
        if equipment.get('lighting_particulars'):
            can.drawString(365, 695, equipment['lighting_particulars'])
        
        # Socket Outlets
        if equipment.get('socket_outlets_checked'):
            draw_checkbox(can, 45, 675, True)
        if equipment.get('socket_outlets_rating'):
            can.drawString(160, 675, str(equipment['socket_outlets_rating']))
        if equipment.get('socket_outlets_number'):
            can.drawString(245, 675, str(equipment['socket_outlets_number']))
        if equipment.get('socket_outlets_particulars'):
            can.drawString(365, 675, equipment['socket_outlets_particulars'])
        
        # Appliances
        if equipment.get('appliances_checked'):
            draw_checkbox(can, 45, 655, True)
        if equipment.get('appliances_rating'):
            can.drawString(160, 655, str(equipment['appliances_rating']))
        if equipment.get('appliances_number'):
            can.drawString(245, 655, str(equipment['appliances_number']))
        if equipment.get('appliances_particulars'):
            can.drawString(365, 655, equipment['appliances_particulars'])
        
        # Generation
        if equipment.get('generation_checked'):
            draw_checkbox(can, 45, 635, True)
        if equipment.get('generation_rating'):
            can.drawString(160, 635, str(equipment['generation_rating']))
        if equipment.get('generation_number'):
            can.drawString(245, 635, str(equipment['generation_number']))
        if equipment.get('generation_particulars'):
            can.drawString(365, 635, equipment['generation_particulars'])
        
        # Storage
        if equipment.get('storage_checked'):
            draw_checkbox(can, 45, 615, True)
        if equipment.get('storage_rating'):
            can.drawString(160, 615, str(equipment['storage_rating']))
        if equipment.get('storage_number'):
            can.drawString(245, 615, str(equipment['storage_number']))
        if equipment.get('storage_particulars'):
            can.drawString(365, 615, equipment['storage_particulars'])
        
        # METERS TABLE (8 rows)
        meters = form_data.get('meters', [])
        y_positions = [520, 500, 480, 460, 440, 420, 400, 380]
        
        for idx, meter in enumerate(meters[:8]):  # Max 8 rows
            y = y_positions[idx]
            
            # I/R/E checkboxes
            if meter.get('type_i'):
                draw_checkbox(can, 45, y, True)
            if meter.get('type_r'):
                draw_checkbox(can, 70, y, True)
            if meter.get('type_e'):
                draw_checkbox(can, 95, y, True)
            
            # Text fields
            if meter.get('meter_no'):
                can.drawString(120, y, str(meter['meter_no']))
            if meter.get('no_dials'):
                can.drawString(175, y, str(meter['no_dials']))
            if meter.get('master_sub_status'):
                can.drawString(230, y, str(meter['master_sub_status']))
            if meter.get('wired_as_master_sub'):
                can.drawString(300, y, str(meter['wired_as_master_sub']))
            if meter.get('register_no'):
                can.drawString(385, y, str(meter['register_no']))
            if meter.get('reading'):
                can.drawString(430, y, str(meter['reading']))
            if meter.get('tariff'):
                tariff_val = str(meter['tariff'])
                # Add 'T' prefix if not already present
                if not tariff_val.startswith('T'):
                    tariff_val = 'T' + tariff_val
                can.drawString(480, y, tariff_val)
        
        # Additional Page 2 Fields (between meters and installer details)
        if form_data.get('estimated_load_increase'):
            can.drawString(230, 360, form_data['estimated_load_increase'])
        
        # Load capacity checkboxes - handle various input formats
        load_capacity = str(form_data.get('load_within_capacity', '')).lower()
        if load_capacity in ['yes', 'y', 'true', '1', 'on']:
            draw_checkbox(can, 415, 340, True)
        elif load_capacity in ['no', 'n', 'false', '0']:
            draw_checkbox(can, 480, 340, True)
        
        # Work connected checkboxes - handle various input formats
        work_connected = str(form_data.get('work_connected_supply', '')).lower()
        if work_connected in ['yes', 'y', 'true', '1', 'on']:
            draw_checkbox(can, 415, 323, True)
        elif work_connected in ['no', 'n', 'false', '0']:
            draw_checkbox(can, 480, 320, True)
        
        # INSTALLERS LICENSE DETAILS (Page 2)
        if form_data.get('installer_first_name'):
            can.drawString(50, 260, form_data['installer_first_name'])
        
        if form_data.get('installer_last_name'):
            can.drawString(305, 260, form_data['installer_last_name'])
        
        if form_data.get('installer_floor'):
            can.drawString(50, 230, form_data['installer_floor'])
        
        if form_data.get('installer_unit'):
            can.drawString(175, 230, form_data['installer_unit'])
        
        if form_data.get('installer_street_number'):
            can.drawString(305, 230, form_data['installer_street_number'])
        
        if form_data.get('installer_lot_rmb'):
            can.drawString(435, 230, form_data['installer_lot_rmb'])
        
        if form_data.get('installer_street_name'):
            can.drawString(50, 200, form_data['installer_street_name'])
        
        if form_data.get('installer_cross_street'):
            can.drawString(305, 200, form_data['installer_cross_street'])
        
        if form_data.get('installer_suburb'):
            can.drawString(50, 170, form_data['installer_suburb'])
        
        if form_data.get('installer_state'):
            can.drawString(305, 170, form_data['installer_state'])
        
        if form_data.get('installer_postcode'):
            can.drawString(470, 170, form_data['installer_postcode'])
        
        if form_data.get('installer_email'):
            can.drawString(50, 142, form_data['installer_email'])
        
        if form_data.get('installer_office_phone'):
            can.drawString(375, 142, form_data['installer_office_phone'])
        
        if form_data.get('installer_mobile_phone'):
            can.drawString(470, 142, form_data['installer_mobile_phone'])
        
        if form_data.get('installer_supervisor_no'):
            can.drawString(50, 112, form_data['installer_supervisor_no'])
        
        if form_data.get('installer_supervisor_expiry'):
            can.drawString(195, 112, form_data['installer_supervisor_expiry'])
        
        if form_data.get('installer_contractor_license'):
            can.drawString(310, 112, form_data['installer_contractor_license'])
        
        if form_data.get('installer_contractor_expiry'):
            can.drawString(450, 112, form_data['installer_contractor_expiry'])
    
    elif page_num == 2:
        # ===== PAGE 3 =====
        
        # TEST REPORT - Checkboxes
        tests = form_data.get('tests', {})
        
        if tests.get('earthing_system'):
            draw_checkbox(can, 65, 742, True)
        if tests.get('rcd_operational'):  # Fixed: was residual_current_device
            draw_checkbox(can, 65, 725, True)
        if tests.get('insulation_resistance'):
            draw_checkbox(can, 65, 707, True)
        if tests.get('visual_check'):
            draw_checkbox(can, 65, 691, True)
        if tests.get('polarity'):
            draw_checkbox(can, 65, 673, True)
        if tests.get('standalone_system'):
            draw_checkbox(can, 65, 657, True)
        if tests.get('correct_current_connections'):
            draw_checkbox(can, 65, 640, True)
        if tests.get('fault_loop_impedance'):
            draw_checkbox(can, 65, 622, True)
        
        # Test completed on (date field)
        if form_data.get('test_date'):
            can.drawString(220, 577, form_data['test_date'])
        
        # TESTERS LICENSE DETAILS
        if form_data.get('tester_same_as_installer'):
            draw_checkbox(can, 240, 552, True)
        
        if form_data.get('tester_first_name'):
            can.drawString(50, 517, form_data['tester_first_name'])
        
        if form_data.get('tester_last_name'):
            can.drawString(305, 517, form_data['tester_last_name'])
        
        if form_data.get('tester_floor'):
            can.drawString(50, 490, form_data['tester_floor'])
        
        if form_data.get('tester_unit'):
            can.drawString(175, 490, form_data['tester_unit'])
        
        if form_data.get('tester_street_number'):
            can.drawString(305, 490, form_data['tester_street_number'])
        
        if form_data.get('tester_lot_rmb'):
            can.drawString(435, 490, form_data['tester_lot_rmb'])
        
        if form_data.get('tester_street_name'):
            can.drawString(50, 460, form_data['tester_street_name'])
        
        if form_data.get('tester_cross_street'):
            can.drawString(305, 460, form_data['tester_cross_street'])
        
        if form_data.get('tester_suburb'):
            can.drawString(50, 430, form_data['tester_suburb'])
        
        if form_data.get('tester_state'):
            can.drawString(305, 430, form_data['tester_state'])
        
        if form_data.get('tester_postcode'):
            can.drawString(470, 430, form_data['tester_postcode'])
        
        if form_data.get('tester_email'):
            can.drawString(50, 402, form_data['tester_email'])
        
        if form_data.get('tester_office_phone'):
            can.drawString(370, 402, form_data['tester_office_phone'])
        
        if form_data.get('tester_mobile_phone'):
            can.drawString(470, 402, form_data['tester_mobile_phone'])
        
        if form_data.get('tester_supervisor_no'):
            can.drawString(50, 372, form_data['tester_supervisor_no'])
        
        if form_data.get('tester_supervisor_expiry'):
            can.drawString(195, 372, form_data['tester_supervisor_expiry'])
        
        if form_data.get('tester_contractor_license'):
            can.drawString(310, 372, form_data['tester_contractor_license'])
        
        if form_data.get('tester_contractor_expiry'):
            can.drawString(450, 372, form_data['tester_contractor_expiry'])
        
        # SUBMIT CCEW
        if form_data.get('meter_provider_email'):
            can.drawString(50, 225, form_data['meter_provider_email'])
        
        if form_data.get('owner_email'):
            can.drawString(50, 180, form_data['owner_email'])
        
        # Signature field (text placeholder)
        if form_data.get('signature'):
            can.drawString(50, 112, form_data['signature'])
    
    can.save()
    packet.seek(0)
    return packet


def generate_ccew_pdf(form_data, template_path=None):
    if template_path is None:
        import os
        template_path = os.path.join(os.path.dirname(__file__), 'CCEWfillableform(unlocked).pdf')
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


def get_pdf_filename(form_data_or_job_number):
    """Generate PDF filename"""
    if isinstance(form_data_or_job_number, dict):
        job_number = form_data_or_job_number.get('serial_no', 'Unknown')
    else:
        job_number = form_data_or_job_number
    return f"CCEW_{job_number}.pdf"
