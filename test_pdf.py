import sys
sys.path.insert(0, '/home/ubuntu/ccew-api-v3')
from pdf_generator import generate_ccew_pdf
import base64

# Test data with all fields populated
test_data = {
    'install_address': '123 Test Street',
    'install_suburb': 'Sydney',
    'install_state': 'NSW',
    'install_postcode': '2000',
    'customer_name': 'Test Customer',
    'customer_phone': '0412345678',
    'work_type': 'Installation',
    'work_description': 'Test electrical work',
    'equip_switchboard': 'yes',
    'equip_switchboard_rating': '100A',
    'equip_switchboard_number': '1',
    'equip_switchboard_particulars': 'Main board',
    'meter_1_i': 'yes',
    'meter_1_number': 'M123456',
    'meter_1_dials': '5',
    'load_increase': '50A',
    'load_within_capacity': 'Yes',
    'work_connected_supply': 'Yes',
    'installer_first_name': 'John',
    'installer_last_name': 'Smith',
    'installer_street_number': '456',
    'installer_street_name': 'Main Road',
    'installer_suburb': 'Sydney',
    'installer_state': 'NSW',
    'installer_postcode': '2000',
    'installer_email': 'john@test.com',
    'installer_office_phone': '0298765432',
    'installer_license_no': 'L123456',
    'installer_license_expiry': '2025-12-31',
    'test_earthing': 'yes',
    'test_rcd': 'yes',
    'test_date': '2024-11-11',
    'tester_first_name': 'Jane',
    'tester_last_name': 'Doe',
    'tester_street_number': '789',
    'tester_street_name': 'Test Avenue',
    'tester_suburb': 'Sydney',
    'tester_state': 'NSW',
    'tester_postcode': '2000',
    'tester_email': 'jane@test.com',
    'tester_license_no': 'T654321',
    'tester_license_expiry': '2025-12-31',
    'energy_provider': 'Ausgrid'
}

print("Generating PDF...")
pdf_base64 = generate_ccew_pdf(test_data)
pdf_bytes = base64.b64decode(pdf_base64)

output_path = '/home/ubuntu/test_ccew.pdf'
with open(output_path, 'wb') as f:
    f.write(pdf_bytes)

print(f"PDF generated successfully: {output_path}")
