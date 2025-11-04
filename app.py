import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ccew-secret-key-2025')

# In-memory session storage (use database in production)
sessions = {}

# Hardcoded company data
COMPANY_DATA = {
    'street_number': '177',
    'street_name': 'Bringelly Rd',
    'suburb': 'Leppington',
    'state': 'NSW',
    'postcode': '2179',
    'email': 'admin@proformelec.com.au',
    'office_phone': '47068270'
}

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "CCEW API v3",
        "version": "3.0.1",
        "endpoints": {
            "generate": "/api/ccew/generate (POST)",
            "form": "/form/<session_id> (GET)",
            "submit": "/api/ccew/submit (POST)"
        }
    })

@app.route('/api/ccew/generate', methods=['POST'])
def generate_ccew():
    """
    Generate a new CCEW form session from SimPro job data
    
    Expected input from Make.com:
    {
        "job_id": 3015,
        "site_name": "Level 2, 121 Walker Street North Sydney",
        "customer_company_name": "Proform Electrical",
        "technician_name": "Karl Knopp",
        "custom_fields": {
            "Tech Licence Number": "1234567",
            "Tech License Expiry": "2032-11-30",
            "Install Street Number": "77",
            "Install Street Name": "Seventy Seven St",
            "Install Suburb": "Newport",
            "Install Postcode": "2106",
            "Customer First Name": "Jim",
            "Customer Last Name": "Badans",
            "Customer Street Number": "58",
            "Customer Street Name": "Grandview St",
            "Customer Suburb": "Mona Vale",
            "Customer State": "NSW",
            "Customer Postcode": "2105"
        }
    }
    """
    try:
        simpro_data = request.json
        
        # Create unique session ID
        session_id = str(uuid.uuid4())
        
        # Extract custom fields from SimPro job data
        custom_fields_array = simpro_data.get('custom_fields_array', [])
        
        # Helper function to find custom field value by name
        def get_custom_field(field_name):
            for field in custom_fields_array:
                if field.get('Name') == field_name:
                    return field.get('Value', '')
            return ''
        
        # Split technician name
        tech_name = simpro_data.get('technician_name', '').split()
        tech_first = tech_name[0] if len(tech_name) > 0 else ''
        tech_last = ' '.join(tech_name[1:]) if len(tech_name) > 1 else ''
        
        # AUTO fields (from SimPro custom fields)
        auto_fields = {
            # Installation Address
            'serial_no': str(simpro_data.get('job_id', '')),
            'property_name': simpro_data.get('site_name', ''),
            'install_street_number': get_custom_field('Install Street Number'),
            'install_street_name': get_custom_field('Install Street Name'),
            'install_suburb': get_custom_field('Install Suburb'),
            'install_postcode': get_custom_field('Install Postcode'),
            
            # Customer Details
            'customer_first_name': get_custom_field('Customer First Name'),
            'customer_last_name': get_custom_field('Customer Last Name'),
            'customer_company_name': simpro_data.get('customer_company_name', ''),
            'customer_street_number': get_custom_field('Customer Street Number'),
            'customer_street_name': get_custom_field('Customer Street Name'),
            'customer_suburb': get_custom_field('Customer Suburb'),
            'customer_state': get_custom_field('Customer State'),
            'customer_postcode': get_custom_field('Customer Postcode'),
            
            # Installer (from custom fields)
            'installer_first_name': tech_first,
            'installer_last_name': tech_last,
            'installer_license_no': get_custom_field('Tech Licence Number'),
            'installer_license_expiry': get_custom_field('Tech License Expiry'),
            
            # Tester (same as installer)
            'tester_first_name': tech_first,
            'tester_last_name': tech_last,
            'tester_license_no': get_custom_field('Tech Licence Number'),
            'tester_license_expiry': get_custom_field('Tech License Expiry'),
            
            # Signature
            'signature': f"{tech_first} {tech_last}"
        }
        
        # HARDCODE fields (company data)
        hardcode_fields = {
            # Installation Address
            'install_state': 'NSW',
            
            # Installer Address
            'installer_street_number': COMPANY_DATA['street_number'],
            'installer_street_name': COMPANY_DATA['street_name'],
            'installer_suburb': COMPANY_DATA['suburb'],
            'installer_state': COMPANY_DATA['state'],
            'installer_postcode': COMPANY_DATA['postcode'],
            'installer_email': COMPANY_DATA['email'],
            'installer_office_phone': COMPANY_DATA['office_phone'],
            
            # Tester Address (same as installer)
            'tester_street_number': COMPANY_DATA['street_number'],
            'tester_street_name': COMPANY_DATA['street_name'],
            'tester_suburb': COMPANY_DATA['suburb'],
            'tester_state': COMPANY_DATA['state'],
            'tester_postcode': COMPANY_DATA['postcode'],
            'tester_email': COMPANY_DATA['email'],
        }
        
        # Combine AUTO and HARDCODE fields
        prefilled_data = {**auto_fields, **hardcode_fields}
        
        # Store session data
        sessions[session_id] = {
            'simpro_data': simpro_data,
            'prefilled_data': prefilled_data,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'mobile_data': {}  # Will be filled by tech on mobile form
        }
        
        # Return form URL
        form_url = f"{request.host_url}form/{session_id}"
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "form_url": form_url,
            "message": "CCEW form generated successfully"
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in generate_ccew: {str(e)}")
        print(f"Full traceback: {error_details}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": error_details
        }), 500

@app.route('/form/<session_id>', methods=['GET'])
def show_form(session_id):
    """Display the CCEW form with pre-filled and editable fields"""
    
    if session_id not in sessions:
        return "Invalid or expired session", 404
    
    session = sessions[session_id]
    prefilled = session['prefilled_data']
    
    # Render the complete CCEW form template
    return render_template('ccew_form.html',
                         session_id=session_id,
                         **prefilled)


@app.route('/api/ccew/submit', methods=['POST'])
def submit_ccew():
    """Handle CCEW form submission"""
    try:
        session_id = request.form.get('session_id')
        
        if session_id not in sessions:
            return jsonify({"success": False, "error": "Invalid session"}), 404
        
        session = sessions[session_id]
        
        # Collect ALL mobile data from form
        mobile_data = {
            # Installation Address
            'nearest_cross_street': request.form.get('nearest_cross_street', ''),
            'pit_pillar_pole_no': request.form.get('pit_pillar_pole_no', ''),
            'nmi': request.form.get('nmi', ''),
            'meter_no': request.form.get('meter_no', ''),
            'aemo_provider_id': request.form.get('aemo_provider_id', ''),
            
            # Installation Details
            'installation_type': request.form.get('installation_type', ''),
            'installation_description': request.form.get('installation_description', ''),
            'work_type': request.form.get('work_type', ''),
            'work_description': request.form.get('work_description', ''),
            'work_date': request.form.get('work_date', ''),
            
            # Installer Contact
            'installer_mobile': request.form.get('installer_mobile', ''),
            
            # Tester Contact
            'tester_mobile': request.form.get('tester_mobile', ''),
            
            # Meter Details
            'meter_register_no': request.form.get('meter_register_no', ''),
            'meter_reading': request.form.get('meter_reading', ''),
            'meter_tariff': request.form.get('meter_tariff', ''),
            'load_increase': request.form.get('load_increase', ''),
            'load_within_capacity': request.form.get('load_within_capacity', ''),
            'work_connected': request.form.get('work_connected', ''),
            
            # Test Report
            'test_earthing': request.form.get('test_earthing', ''),
            'test_rcd': request.form.get('test_rcd', ''),
            'test_insulation': request.form.get('test_insulation', ''),
            'test_visual': request.form.get('test_visual', ''),
            'test_polarity': request.form.get('test_polarity', ''),
            'test_standalone': request.form.get('test_standalone', ''),
            'test_current': request.form.get('test_current', ''),
            'test_fault_loop': request.form.get('test_fault_loop', ''),
            'test_date': request.form.get('test_date', ''),
            
            # Submit CCEW
            'energy_provider': request.form.get('energy_provider', ''),
            'meter_provider_email': request.form.get('meter_provider_email', ''),
        }
        
        # Update session with mobile data
        session['mobile_data'] = mobile_data
        session['status'] = 'submitted'
        session['submitted_at'] = datetime.now().isoformat()
        
        # Combine all data
        complete_data = {**session['prefilled_data'], **mobile_data}
        
        # TODO: Generate PDF with complete_data
        # TODO: Send email to energy provider, meter provider, and owner
        
        return jsonify({
            "success": True,
            "message": "CCEW submitted successfully",
            "session_id": session_id
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in generate_ccew: {str(e)}")
        print(f"Full traceback: {error_details}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": error_details
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
