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

def parse_address(address_string):
    """Parse address string into components"""
    # Simple parser - can be improved
    parts = address_string.split(',') if address_string else []
    
    result = {
        'street_number': '',
        'street_name': '',
        'suburb': '',
        'state': '',
        'postcode': ''
    }
    
    if len(parts) >= 1:
        # First part usually contains street number and name
        street_parts = parts[0].strip().split(' ', 1)
        if len(street_parts) >= 2:
            result['street_number'] = street_parts[0]
            result['street_name'] = street_parts[1]
        else:
            result['street_name'] = parts[0].strip()
    
    if len(parts) >= 2:
        # Second part usually suburb
        result['suburb'] = parts[1].strip()
    
    if len(parts) >= 3:
        # Third part usually state and postcode
        state_postcode = parts[2].strip().split()
        if len(state_postcode) >= 2:
            result['state'] = state_postcode[0]
            result['postcode'] = state_postcode[1]
    
    return result

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "CCEW API v3",
        "version": "3.0",
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
        custom_fields = simpro_data.get('custom_fields', {})
        
        # Split technician name
        tech_name = simpro_data.get('technician_name', '').split()
        tech_first = tech_name[0] if len(tech_name) > 0 else ''
        tech_last = ' '.join(tech_name[1:]) if len(tech_name) > 1 else ''
        
        # AUTO fields (from SimPro custom fields)
        auto_fields = {
            # Installation Address
            'serial_no': str(simpro_data.get('job_id', '')),
            'property_name': simpro_data.get('site_name', ''),
            'install_street_number': custom_fields.get('Install Street Number', ''),
            'install_street_name': custom_fields.get('Install Street Name', ''),
            'install_suburb': custom_fields.get('Install Suburb', ''),
            'install_postcode': custom_fields.get('Install Postcode', ''),
            
            # Customer Details
            'customer_first_name': custom_fields.get('Customer First Name', ''),
            'customer_last_name': custom_fields.get('Customer Last Name', ''),
            'customer_company_name': simpro_data.get('customer_company_name', ''),
            'customer_street_number': custom_fields.get('Customer Street Number', ''),
            'customer_street_name': custom_fields.get('Customer Street Name', ''),
            'customer_suburb': custom_fields.get('Customer Suburb', ''),
            'customer_state': custom_fields.get('Customer State', ''),
            'customer_postcode': custom_fields.get('Customer Postcode', ''),
            
            # Installer (from custom fields)
            'installer_first_name': tech_first,
            'installer_last_name': tech_last,
            'installer_license_no': custom_fields.get('Tech Licence Number', ''),
            'installer_license_expiry': custom_fields.get('Tech License Expiry', ''),
            
            # Tester (same as installer)
            'tester_first_name': tech_first,
            'tester_last_name': tech_last,
            'tester_license_no': custom_fields.get('Tech Licence Number', ''),
            'tester_license_expiry': custom_fields.get('Tech License Expiry', ''),
            
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
        return jsonify({
            "success": False,
            "error": str(e)
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
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CCEW Form - {{ serial_no }}</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; margin-bottom: 10px; font-size: 24px; }
            h2 { color: #666; margin-top: 30px; margin-bottom: 15px; font-size: 18px; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
            .field-group { margin-bottom: 20px; }
            label { display: block; font-weight: bold; margin-bottom: 5px; color: #555; font-size: 14px; }
            input[type="text"], input[type="date"], input[type="email"], select, textarea {
                width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;
            }
            input[readonly] { background: #f9f9f9; color: #666; cursor: not-allowed; }
            .readonly-note { font-size: 12px; color: #999; font-style: italic; margin-top: 3px; }
            .checkbox-group { margin: 10px 0; }
            .checkbox-group label { display: inline-block; margin-right: 20px; font-weight: normal; }
            .checkbox-group input[type="checkbox"] { margin-right: 5px; }
            .submit-btn { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; width: 100%; margin-top: 30px; }
            .submit-btn:hover { background: #0056b3; }
            .info-box { background: #e7f3ff; border-left: 4px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 4px; }
            .info-box p { margin: 5px 0; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Certificate of Compliance for Electrical Work (CCEW)</h1>
            
            <div class="info-box">
                <p><strong>Job #{{ serial_no }}</strong></p>
                <p>Pre-filled fields are read-only. Please complete the remaining fields.</p>
            </div>
            
            <form id="ccewForm" method="POST" action="/api/ccew/submit">
                <input type="hidden" name="session_id" value="{{ session_id }}">
                
                <h2>1. Installation Address</h2>
                
                <div class="field-group">
                    <label>Serial No</label>
                    <input type="text" value="{{ serial_no }}" readonly>
                    <div class="readonly-note">Auto-filled from SimPro</div>
                </div>
                
                <div class="field-group">
                    <label>Property Name</label>
                    <input type="text" value="{{ property_name }}" readonly>
                    <div class="readonly-note">Auto-filled from SimPro</div>
                </div>
                
                <div class="field-group">
                    <label>Street Number</label>
                    <input type="text" value="{{ install_street_number }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Street Name</label>
                    <input type="text" value="{{ install_street_name }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Nearest Cross Street</label>
                    <input type="text" name="nearest_cross_street" placeholder="Enter nearest cross street">
                </div>
                
                <div class="field-group">
                    <label>Suburb</label>
                    <input type="text" value="{{ install_suburb }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>State</label>
                    <input type="text" value="{{ install_state }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Post Code</label>
                    <input type="text" value="{{ install_postcode }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Pit/Pillar/Pole No.</label>
                    <input type="text" name="pit_pillar_pole_no" placeholder="Enter pit/pillar/pole number">
                </div>
                
                <div class="field-group">
                    <label>NMI (National Meter Identifier)</label>
                    <input type="text" name="nmi" placeholder="Enter NMI">
                </div>
                
                <div class="field-group">
                    <label>Meter No.</label>
                    <input type="text" name="meter_no" placeholder="Enter meter number">
                </div>
                
                <div class="field-group">
                    <label>AEMO Metering Provider I.D.</label>
                    <input type="text" name="aemo_provider_id" placeholder="Enter AEMO provider ID">
                </div>
                
                <h2>2. Customer Details</h2>
                
                <div class="field-group">
                    <label>First Name</label>
                    <input type="text" value="{{ customer_first_name }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Last Name</label>
                    <input type="text" value="{{ customer_last_name }}" readonly>
                </div>
                
                <div class="field-group">
                    <label>Company Name</label>
                    <input type="text" value="{{ customer_company_name }}" readonly>
                </div>
                
                <h2>3. Installation Details</h2>
                
                <div class="field-group">
                    <label>Type of Installation</label>
                    <select name="installation_type" required>
                        <option value="">Select type...</option>
                        <option value="Residential">Residential</option>
                        <option value="Commercial">Commercial</option>
                        <option value="Industrial">Industrial</option>
                        <option value="Rural">Rural</option>
                        <option value="Mixed Development">Mixed Development</option>
                    </select>
                </div>
                
                <div class="field-group">
                    <label>Work Carried Out (select all that apply)</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" name="work_new_work" value="yes"> New Work</label><br>
                        <label><input type="checkbox" name="work_installed_meter" value="yes"> Installed Meter</label><br>
                        <label><input type="checkbox" name="work_network_connection" value="yes"> Network Connection</label><br>
                        <label><input type="checkbox" name="work_addition_alteration" value="yes"> Addition/Alteration to Existing</label><br>
                        <label><input type="checkbox" name="work_advanced_meter" value="yes"> Install Advanced Meter</label><br>
                        <label><input type="checkbox" name="work_ev_connection" value="yes"> EV Connection</label><br>
                        <label><input type="checkbox" name="work_reinspection" value="yes"> Re-inspection of Non-Compliant Work</label><br>
                    </div>
                </div>
                
                <div class="field-group">
                    <label>Non-Compliance No. (if applicable)</label>
                    <input type="text" name="non_compliance_no" placeholder="Enter non-compliance number">
                </div>
                
                <h2>9. Submit CCEW</h2>
                
                <div class="field-group">
                    <label>Energy Provider</label>
                    <select name="energy_provider" required>
                        <option value="">Select provider...</option>
                        <option value="Ausgrid">Ausgrid</option>
                        <option value="Endeavour Energy">Endeavour Energy</option>
                        <option value="Essential Energy">Essential Energy</option>
                    </select>
                </div>
                
                <div class="field-group">
                    <label>Meter Provider's Email</label>
                    <input type="email" name="meter_provider_email" placeholder="Enter meter provider email" required>
                </div>
                
                <div class="field-group">
                    <label>Confirm Meter Provider's Email</label>
                    <input type="email" name="meter_provider_email_confirm" placeholder="Confirm meter provider email" required>
                </div>
                
                <button type="submit" class="submit-btn">Submit CCEW</button>
            </form>
        </div>
        
        <script>
            document.getElementById('ccewForm').addEventListener('submit', function(e) {
                const email = document.querySelector('input[name="meter_provider_email"]').value;
                const confirm = document.querySelector('input[name="meter_provider_email_confirm"]').value;
                
                if (email !== confirm) {
                    e.preventDefault();
                    alert('Meter provider email addresses do not match!');
                }
            });
        </script>

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
            
            # Work Carried Out
            'work_new_work': request.form.get('work_new_work', ''),
            'work_installed_meter': request.form.get('work_installed_meter', ''),
            'work_network_connection': request.form.get('work_network_connection', ''),
            'work_addition_alteration': request.form.get('work_addition_alteration', ''),
            'work_advanced_meter': request.form.get('work_advanced_meter', ''),
            'work_ev_connection': request.form.get('work_ev_connection', ''),
            'work_reinspection': request.form.get('work_reinspection', ''),
            'non_compliance_no': request.form.get('non_compliance_no', ''),
            
            # Special Conditions
            'special_over_100_amps': request.form.get('special_over_100_amps', ''),
            'special_hazardous_area': request.form.get('special_hazardous_area', ''),
            'special_off_grid': request.form.get('special_off_grid', ''),
            'special_high_voltage': request.form.get('special_high_voltage', ''),
            'special_unmetered': request.form.get('special_unmetered', ''),
            'special_secondary_power': request.form.get('special_secondary_power', ''),
            
            # Equipment Details
            'equip_switchboard': request.form.get('equip_switchboard', ''),
            'equip_switchboard_rating': request.form.get('equip_switchboard_rating', ''),
            'equip_switchboard_number': request.form.get('equip_switchboard_number', ''),
            'equip_switchboard_particulars': request.form.get('equip_switchboard_particulars', ''),
            
            'equip_circuits': request.form.get('equip_circuits', ''),
            'equip_circuits_rating': request.form.get('equip_circuits_rating', ''),
            'equip_circuits_number': request.form.get('equip_circuits_number', ''),
            'equip_circuits_particulars': request.form.get('equip_circuits_particulars', ''),
            
            'equip_lighting': request.form.get('equip_lighting', ''),
            'equip_lighting_rating': request.form.get('equip_lighting_rating', ''),
            'equip_lighting_number': request.form.get('equip_lighting_number', ''),
            'equip_lighting_particulars': request.form.get('equip_lighting_particulars', ''),
            
            'equip_sockets': request.form.get('equip_sockets', ''),
            'equip_sockets_rating': request.form.get('equip_sockets_rating', ''),
            'equip_sockets_number': request.form.get('equip_sockets_number', ''),
            'equip_sockets_particulars': request.form.get('equip_sockets_particulars', ''),
            
            'equip_appliances': request.form.get('equip_appliances', ''),
            'equip_appliances_rating': request.form.get('equip_appliances_rating', ''),
            'equip_appliances_number': request.form.get('equip_appliances_number', ''),
            'equip_appliances_particulars': request.form.get('equip_appliances_particulars', ''),
            
            'equip_generation': request.form.get('equip_generation', ''),
            'equip_generation_rating': request.form.get('equip_generation_rating', ''),
            'equip_generation_number': request.form.get('equip_generation_number', ''),
            'equip_generation_particulars': request.form.get('equip_generation_particulars', ''),
            
            'equip_storage': request.form.get('equip_storage', ''),
            'equip_storage_rating': request.form.get('equip_storage_rating', ''),
            'equip_storage_number': request.form.get('equip_storage_number', ''),
            'equip_storage_particulars': request.form.get('equip_storage_particulars', ''),
            
            # Meters
            'meter_status': request.form.get('meter_status', ''),
            'meter_number': request.form.get('meter_number', ''),
            'meter_dials': request.form.get('meter_dials', ''),
            'meter_master_sub': request.form.get('meter_master_sub', ''),
            'meter_wired_as': request.form.get('meter_wired_as', ''),
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
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

