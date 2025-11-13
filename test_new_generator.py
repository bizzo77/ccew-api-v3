"""Test the new PDF generator with sample data"""

import base64
from pdf_generator import generate_ccew_pdf, get_pdf_filename

# Sample test data
test_data = {
    'serial_no': '3015',
    'property_name': 'Test Building',
    'install_street_number': '123',
    'install_street_name': 'Test Street',
    'nearest_cross_street': 'Cross Road',
    'install_suburb': 'Sydney',
    'install_state': 'NSW',
    'install_postcode': '2000',
    'pit_pillar_pole_no': 'PP123',
    'nmi': 'NMI123456',
    'meter_no': 'M789',
    'aemo_provider_id': 'AEMO001',
    
    'customer_first_name': 'John',
    'customer_last_name': 'Smith',
    'customer_company_name': 'Smith Enterprises Pty Ltd',
    'customer_street_number': '456',
    'customer_street_name': 'Customer Road',
    'customer_suburb': 'Sydney',
    'customer_state': 'NSW',
    'customer_postcode': '2000',
    'customer_email': 'john@example.com',
    'customer_office_phone': '02 1234 5678',
    'customer_mobile_phone': '0412 345 678',
    
    'installation_type': 'residential',
    'work_type': 'new work',
    
    'equip_switchboard': 'yes',
    'equip_switchboard_rating': '100A',
    'equip_switchboard_number': '1',
    'equip_switchboard_particulars': 'Main switchboard',
    
    'equip_circuits': 'yes',
    'equip_circuits_rating': '20A',
    'equip_circuits_number': '12',
    'equip_circuits_particulars': 'Lighting and power',
    
    'meter_1_i': 'yes',
    'meter_1_number': 'M123456',
    'meter_1_dials': '5',
    
    'load_increase': '15kW',
    'load_within_capacity': 'yes',
    'work_connected_supply': 'yes',
    
    'installer_first_name': 'Bob',
    'installer_last_name': 'Builder',
    'installer_street_number': '789',
    'installer_street_name': 'Installer Ave',
    'installer_suburb': 'Sydney',
    'installer_state': 'NSW',
    'installer_postcode': '2000',
    'installer_email': 'bob@builder.com',
    'installer_office_phone': '02 9876 5432',
    'installer_license_no': 'LIC123456',
    'installer_license_expiry': '2025-12-31',
    
    'test_earthing': 'yes',
    'test_rcd': 'yes',
    'test_insulation': 'yes',
    'test_visual': 'yes',
    'test_polarity': 'yes',
    'test_date': '2024-11-13',
    
    'tester_first_name': 'Test',
    'tester_last_name': 'Engineer',
    'tester_street_number': '321',
    'tester_street_name': 'Tester St',
    'tester_suburb': 'Sydney',
    'tester_state': 'NSW',
    'tester_postcode': '2000',
    'tester_email': 'test@engineer.com',
    'tester_license_no': 'TEST123',
    'tester_license_expiry': '2026-06-30',
    
    'energy_provider': 'Ausgrid',
}

print("Generating PDF with new overlay approach...")
print(f"Using calibrated coordinates (Property Name Y=650)")

try:
    pdf_base64 = generate_ccew_pdf(test_data)
    pdf_bytes = base64.b64decode(pdf_base64)
    
    filename = get_pdf_filename(test_data.get('serial_no', '3015'))
    with open(filename, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"✅ PDF generated successfully!")
    print(f"   Output: {filename}")
    print(f"   Size: {len(pdf_bytes)} bytes")
    print("\nPlease review the PDF to verify field positioning.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
