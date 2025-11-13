"""
Test script for the new pypdf-based overlay PDF generator
"""

from pdf_generator_overlay import generate_ccew_pdf, get_pdf_filename
import base64

# Test data - comprehensive sample
test_data = {
    # Serial Number
    'serial_no': '3015',
    
    # Installation Address
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
    
    # Customer Details
    'customer_first_name': 'John',
    'customer_last_name': 'Smith',
    'customer_company_name': 'Smith Enterprises Pty Ltd',
    'customer_street_number': '456',
    'customer_street_name': 'Customer Road',
    'customer_suburb': 'Sydney',
    'customer_state': 'NSW',
    'customer_postcode': '2000',
    'customer_email': 'john.smith@test.com',
    'customer_office_phone': '0298765432',
    'customer_mobile_phone': '0412345678',
    
    # Installation Details
    'installation_type': 'residential',
    'work_type': 'new work',
    
    # Equipment
    'equip_switchboard': 'yes',
    'equip_switchboard_rating': '100A',
    'equip_switchboard_number': '1',
    'equip_switchboard_particulars': 'Main board',
    'equip_circuits': 'yes',
    'equip_circuits_rating': '20A',
    'equip_circuits_number': '5',
    'equip_circuits_particulars': 'Power circuits',
    
    # Meters
    'meter_1_i': 'yes',
    'meter_1_number': 'M123456',
    'meter_1_dials': '5',
    
    # Load
    'load_increase': '50A',
    'load_within_capacity': 'Yes',
    'work_connected_supply': 'Yes',
    
    # Installer
    'installer_first_name': 'James',
    'installer_last_name': 'Installer',
    'installer_street_number': '789',
    'installer_street_name': 'Installer Ave',
    'installer_suburb': 'Sydney',
    'installer_state': 'NSW',
    'installer_postcode': '2000',
    'installer_email': 'james@installer.com',
    'installer_office_phone': '0287654321',
    'installer_license_no': 'L123456',
    'installer_license_expiry': '2025-12-31',
    
    # Test Report
    'test_earthing': 'yes',
    'test_rcd': 'yes',
    'test_insulation': 'yes',
    'test_visual': 'yes',
    'test_polarity': 'yes',
    'test_date': '2024-11-11',
    
    # Tester
    'tester_first_name': 'Sarah',
    'tester_last_name': 'Tester',
    'tester_street_number': '321',
    'tester_street_name': 'Tester Street',
    'tester_suburb': 'Sydney',
    'tester_state': 'NSW',
    'tester_postcode': '2000',
    'tester_email': 'sarah@tester.com',
    'tester_license_no': 'T654321',
    'tester_license_expiry': '2025-12-31',
    
    # Energy Provider
    'energy_provider': 'Ausgrid'
}

print("Generating PDF using pypdf overlay approach...")
print(f"Template location: CCEW_OFFICIAL_TEMPLATE.pdf")

try:
    pdf_base64 = generate_ccew_pdf(test_data)
    pdf_bytes = base64.b64decode(pdf_base64)
    
    filename = get_pdf_filename(test_data)
    output_path = f'/home/ubuntu/ccew-api-v3/{filename}'
    
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"✅ PDF generated successfully!")
    print(f"PDF size: {len(pdf_bytes)} bytes")
    print(f"Output saved to: {output_path}")
    print(f"\nNow compare this with the official form to verify positioning.")
    
except Exception as e:
    print(f"❌ Error generating PDF: {e}")
    import traceback
    traceback.print_exc()
