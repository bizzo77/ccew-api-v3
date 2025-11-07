import os
import json
import uuid
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, g
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
import requests
import base64
from pdf_generator import generate_ccew_pdf, get_pdf_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ccew-secret-key-2025')
DATABASE = '/tmp/ccew_sessions.db'

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

def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                simpro_data TEXT,
                prefilled_data TEXT,
                mobile_data TEXT,
                created_at TEXT,
                status TEXT
            )
        ''')
        db.commit()

def save_session(session_id, simpro_data, prefilled_data):
    """Save a new session to database"""
    db = get_db()
    db.execute('''
        INSERT INTO sessions (session_id, simpro_data, prefilled_data, mobile_data, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        session_id,
        json.dumps(simpro_data),
        json.dumps(prefilled_data),
        json.dumps({}),
        datetime.now().isoformat(),
        'pending'
    ))
    db.commit()

def get_session(session_id):
    """Get session from database"""
    db = get_db()
    cursor = db.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
    row = cursor.fetchone()
    if row:
        return {
            'session_id': row['session_id'],
            'simpro_data': json.loads(row['simpro_data']),
            'prefilled_data': json.loads(row['prefilled_data']),
            'mobile_data': json.loads(row['mobile_data']),
            'created_at': row['created_at'],
            'status': row['status']
        }
    return None

def update_session(session_id, mobile_data):
    """Update session with mobile data"""
    db = get_db()
    db.execute('''
        UPDATE sessions 
        SET mobile_data = ?, status = ?
        WHERE session_id = ?
    ''', (json.dumps(mobile_data), 'submitted', session_id))
    db.commit()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "CCEW API v3",
        "version": "3.0.2",
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
    """
    # Log incoming request details
    print(f"\n{'='*80}")
    print(f"INCOMING REQUEST to /api/ccew/generate")
    print(f"Content-Type: {request.content_type}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Raw data (first 500 chars): {request.data.decode('utf-8')[:500]}")
    print(f"{'='*80}\n")
    
    try:
        # Handle both JSON and raw data from Make.com
        try:
            simpro_data = request.json
        except Exception as json_error:
            # If request.json fails, try parsing raw data
            try:
                raw_data = request.data.decode('utf-8')
                # Try to unescape if it's double-escaped
                if raw_data.startswith('"') and raw_data.endswith('"'):
                    raw_data = raw_data[1:-1].replace('\\"', '"').replace('\\\\', '\\')
                simpro_data = json.loads(raw_data)
            except Exception as parse_error:
                return jsonify({
                    "success": False,
                    "error": f"Failed to parse request data: {str(json_error)}, {str(parse_error)}",
                    "received_data": request.data.decode('utf-8')[:500]
                }), 400
        
        # Create unique session ID
        session_id = str(uuid.uuid4())
        
        # Extract custom fields from SimPro job data
        custom_fields_raw = simpro_data.get('custom_fields_array', [])
        
        # Handle both array format and nested CustomField object format
        custom_fields_array = []
        if isinstance(custom_fields_raw, dict):
            # If it's a dict with CustomField keys, extract the values
            for key, value in custom_fields_raw.items():
                if isinstance(value, dict) and 'Name' in value:
                    custom_fields_array.append(value)
        elif isinstance(custom_fields_raw, list):
            # If it's an array, normalize the structure
            for item in custom_fields_raw:
                if isinstance(item, dict):
                    # Handle structure: {"CustomField": {"Name": "...", ...}, "Value": "..."}
                    if 'CustomField' in item and 'Value' in item:
                        custom_field = item['CustomField']
                        custom_fields_array.append({
                            'Name': custom_field.get('Name', ''),
                            'Value': item.get('Value', '')
                        })
                    # Handle structure: {"Name": "...", "Value": "..."}
                    elif 'Name' in item:
                        custom_fields_array.append(item)
        
        print(f"Parsed custom fields: {custom_fields_array}")
        
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
        
        # Save session to database
        save_session(session_id, simpro_data, prefilled_data)
        
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
    
    session = get_session(session_id)
    if not session:
        return "Invalid or expired session", 404
    
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
        
        session = get_session(session_id)
        if not session:
            return jsonify({"success": False, "error": "Invalid session"}), 404
        
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
            
            # Electrical Work Details
            'supply_type': request.form.get('supply_type', ''),
            'supply_phases': request.form.get('supply_phases', ''),
            'supply_voltage': request.form.get('supply_voltage', ''),
            'supply_frequency': request.form.get('supply_frequency', ''),
            'earthing_type': request.form.get('earthing_type', ''),
            'main_switch_rating': request.form.get('main_switch_rating', ''),
            'rcd_rating': request.form.get('rcd_rating', ''),
            'circuit_details': request.form.get('circuit_details', ''),
            
            # Testing Results
            'insulation_test': request.form.get('insulation_test', ''),
            'earth_continuity': request.form.get('earth_continuity', ''),
            'polarity_test': request.form.get('polarity_test', ''),
            'rcd_test': request.form.get('rcd_test', ''),
            
            # Installer Contact
            'installer_mobile_phone': request.form.get('installer_mobile_phone', ''),
            
            # Tester Contact
            'tester_mobile_phone': request.form.get('tester_mobile_phone', ''),
            
            # Dates
            'date_work_completed': request.form.get('date_work_completed', ''),
            'date_work_tested': request.form.get('date_work_tested', '')
        }
        
        # Update session with mobile data
        update_session(session_id, mobile_data)
        
        # Combine all data for email
        all_data = {**session['prefilled_data'], **mobile_data}
        
        # Get energy provider
        energy_provider = request.form.get('energy_provider', '')
        all_data['energy_provider'] = energy_provider
        
        # Send email notification
        send_email_notification(session_id, all_data)
        
        # Return HTML success page
        return render_template('success.html', job_number=all_data.get('serial_no', 'N/A'))
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in submit_ccew: {str(e)}")
        print(f"Full traceback: {error_details}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": error_details
        }), 500


def send_email_notification(session_id, form_data):
    """Send form data to Make.com webhook for email processing"""
    try:
        # Make.com webhook URL for email sending
        webhook_url = os.environ.get('MAKECOM_EMAIL_WEBHOOK', '')
        
        if not webhook_url:
            print("WARNING: MAKECOM_EMAIL_WEBHOOK not configured, skipping email")
            return
        
        # Create HTML email body
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
                .section h2 {{ margin-top: 0; color: #333; }}
                .field {{ margin: 5px 0; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ color: #000; }}
            </style>
        </head>
        <body>
            <h1>CCEW Form Submission - TEST</h1>
            
            <div class="section">
                <h2>Installation Address</h2>
                <div class="field"><span class="label">Serial No:</span> <span class="value">{form_data.get('serial_no', '')}</span></div>
                <div class="field"><span class="label">Property Name:</span> <span class="value">{form_data.get('property_name', '')}</span></div>
                <div class="field"><span class="label">Street:</span> <span class="value">{form_data.get('install_street_number', '')} {form_data.get('install_street_name', '')}</span></div>
                <div class="field"><span class="label">Suburb:</span> <span class="value">{form_data.get('install_suburb', '')}</span></div>
                <div class="field"><span class="label">State:</span> <span class="value">{form_data.get('install_state', '')}</span></div>
                <div class="field"><span class="label">Postcode:</span> <span class="value">{form_data.get('install_postcode', '')}</span></div>
                <div class="field"><span class="label">Nearest Cross Street:</span> <span class="value">{form_data.get('nearest_cross_street', '')}</span></div>
                <div class="field"><span class="label">Pit/Pillar/Pole No:</span> <span class="value">{form_data.get('pit_pillar_pole_no', '')}</span></div>
                <div class="field"><span class="label">NMI:</span> <span class="value">{form_data.get('nmi', '')}</span></div>
                <div class="field"><span class="label">Meter No:</span> <span class="value">{form_data.get('meter_no', '')}</span></div>
                <div class="field"><span class="label">AEMO Provider ID:</span> <span class="value">{form_data.get('aemo_provider_id', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Customer Details</h2>
                <div class="field"><span class="label">Name:</span> <span class="value">{form_data.get('customer_first_name', '')} {form_data.get('customer_last_name', '')}</span></div>
                <div class="field"><span class="label">Company:</span> <span class="value">{form_data.get('customer_company_name', '')}</span></div>
                <div class="field"><span class="label">Address:</span> <span class="value">{form_data.get('customer_street_number', '')} {form_data.get('customer_street_name', '')}, {form_data.get('customer_suburb', '')} {form_data.get('customer_state', '')} {form_data.get('customer_postcode', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Installation Details</h2>
                <div class="field"><span class="label">Type:</span> <span class="value">{form_data.get('installation_type', '')}</span></div>
                <div class="field"><span class="label">Description:</span> <span class="value">{form_data.get('installation_description', '')}</span></div>
                <div class="field"><span class="label">Work Type:</span> <span class="value">{form_data.get('work_type', '')}</span></div>
                <div class="field"><span class="label">Work Description:</span> <span class="value">{form_data.get('work_description', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Electrical Work Details</h2>
                <div class="field"><span class="label">Supply Type:</span> <span class="value">{form_data.get('supply_type', '')}</span></div>
                <div class="field"><span class="label">Phases:</span> <span class="value">{form_data.get('supply_phases', '')}</span></div>
                <div class="field"><span class="label">Voltage:</span> <span class="value">{form_data.get('supply_voltage', '')}</span></div>
                <div class="field"><span class="label">Frequency:</span> <span class="value">{form_data.get('supply_frequency', '')}</span></div>
                <div class="field"><span class="label">Earthing Type:</span> <span class="value">{form_data.get('earthing_type', '')}</span></div>
                <div class="field"><span class="label">Main Switch Rating:</span> <span class="value">{form_data.get('main_switch_rating', '')}</span></div>
                <div class="field"><span class="label">RCD Rating:</span> <span class="value">{form_data.get('rcd_rating', '')}</span></div>
                <div class="field"><span class="label">Circuit Details:</span> <span class="value">{form_data.get('circuit_details', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Testing Results</h2>
                <div class="field"><span class="label">Insulation Test:</span> <span class="value">{form_data.get('insulation_test', '')}</span></div>
                <div class="field"><span class="label">Earth Continuity:</span> <span class="value">{form_data.get('earth_continuity', '')}</span></div>
                <div class="field"><span class="label">Polarity Test:</span> <span class="value">{form_data.get('polarity_test', '')}</span></div>
                <div class="field"><span class="label">RCD Test:</span> <span class="value">{form_data.get('rcd_test', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Installer Details</h2>
                <div class="field"><span class="label">Name:</span> <span class="value">{form_data.get('installer_first_name', '')} {form_data.get('installer_last_name', '')}</span></div>
                <div class="field"><span class="label">License No:</span> <span class="value">{form_data.get('installer_license_no', '')}</span></div>
                <div class="field"><span class="label">License Expiry:</span> <span class="value">{form_data.get('installer_license_expiry', '')}</span></div>
                <div class="field"><span class="label">Mobile:</span> <span class="value">{form_data.get('installer_mobile_phone', '')}</span></div>
                <div class="field"><span class="label">Address:</span> <span class="value">{form_data.get('installer_street_number', '')} {form_data.get('installer_street_name', '')}, {form_data.get('installer_suburb', '')} {form_data.get('installer_state', '')} {form_data.get('installer_postcode', '')}</span></div>
                <div class="field"><span class="label">Email:</span> <span class="value">{form_data.get('installer_email', '')}</span></div>
                <div class="field"><span class="label">Office Phone:</span> <span class="value">{form_data.get('installer_office_phone', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Tester Details</h2>
                <div class="field"><span class="label">Name:</span> <span class="value">{form_data.get('tester_first_name', '')} {form_data.get('tester_last_name', '')}</span></div>
                <div class="field"><span class="label">License No:</span> <span class="value">{form_data.get('tester_license_no', '')}</span></div>
                <div class="field"><span class="label">License Expiry:</span> <span class="value">{form_data.get('tester_license_expiry', '')}</span></div>
                <div class="field"><span class="label">Mobile:</span> <span class="value">{form_data.get('tester_mobile_phone', '')}</span></div>
                <div class="field"><span class="label">Address:</span> <span class="value">{form_data.get('tester_street_number', '')} {form_data.get('tester_street_name', '')}, {form_data.get('tester_suburb', '')} {form_data.get('tester_state', '')} {form_data.get('tester_postcode', '')}</span></div>
                <div class="field"><span class="label">Email:</span> <span class="value">{form_data.get('tester_email', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Dates</h2>
                <div class="field"><span class="label">Work Completed:</span> <span class="value">{form_data.get('date_work_completed', '')}</span></div>
                <div class="field"><span class="label">Work Tested:</span> <span class="value">{form_data.get('date_work_tested', '')}</span></div>
            </div>
            
            <div class="section">
                <h2>Signature</h2>
                <div class="field"><span class="label">Signed by:</span> <span class="value">{form_data.get('signature', '')}</span></div>
            </div>
            
            <p><em>This is a TEST email. No action required.</em></p>
        </body>
        </html>
        """
        
        # Generate PDF
        pdf_base64 = generate_ccew_pdf(form_data)
        pdf_filename = get_pdf_filename(form_data)
        
        # Send PDF data directly as base64 - Make.com will handle it
        
        # Create professional email body
        job_no = form_data.get('serial_no', 'N/A')
        property_name = form_data.get('property_name', 'N/A')
        install_address = f"{form_data.get('install_street_number', '')} {form_data.get('install_street_name', '')}, {form_data.get('install_suburb', '')} {form_data.get('install_state', '')} {form_data.get('install_postcode', '')}"
        customer_name = f"{form_data.get('customer_first_name', '')} {form_data.get('customer_last_name', '')}"
        tech_name = f"{form_data.get('installer_first_name', '')} {form_data.get('installer_last_name', '')}"
        date_completed = form_data.get('date_work_completed', 'N/A')
        energy_provider = form_data.get('energy_provider', '')
        
        email_body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <p>Dear Energy Provider,</p>
    
    <p>Please find attached the Certificate of Compliance for Electrical Work (CCEW) for the following job:</p>
    
    <table style="margin: 20px 0; border-collapse: collapse;">
        <tr><td style="padding: 5px 10px; font-weight: bold;">Job Number:</td><td style="padding: 5px 10px;">{job_no}</td></tr>
        <tr><td style="padding: 5px 10px; font-weight: bold;">Property:</td><td style="padding: 5px 10px;">{property_name}</td></tr>
        <tr><td style="padding: 5px 10px; font-weight: bold;">Address:</td><td style="padding: 5px 10px;">{install_address}</td></tr>
        <tr><td style="padding: 5px 10px; font-weight: bold;">Customer:</td><td style="padding: 5px 10px;">{customer_name}</td></tr>
        <tr><td style="padding: 5px 10px; font-weight: bold;">Technician:</td><td style="padding: 5px 10px;">{tech_name}</td></tr>
        <tr><td style="padding: 5px 10px; font-weight: bold;">Date Completed:</td><td style="padding: 5px 10px;">{date_completed}</td></tr>
    </table>
    
    <p>The attached PDF contains the complete CCEW form with all required details and test results.</p>
    
    <p>If you have any questions, please contact:</p>
    <p style="margin-left: 20px;">
        <strong>Proform Electrical</strong><br>
        Phone: 47068270<br>
        Email: admin@proformelec.com.au
    </p>
    
    <p>Kind regards,<br>
    <strong>Proform Electrical</strong></p>
</body>
</html>"""
        
        # Send form data to Make.com webhook
        import requests
        
        payload = {
            'session_id': session_id,
            'subject': f"CCEW Form Submission - Job #{job_no} - {customer_name}",
            'to_email': 'jimbadans@evolutionbc.com.au',
            'email_body': email_body,
            'pdf_data': pdf_base64,
            'pdf_filename': pdf_filename,
            'energy_provider': energy_provider,
            'form_data': form_data
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        print(f"Email data sent to Make.com for session {session_id}")
        print(f"Make.com webhook response status: {response.status_code}")
        
    except Exception as e:
        print(f"ERROR sending email: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

