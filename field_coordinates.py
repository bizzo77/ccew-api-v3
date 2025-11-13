"""
Precise field coordinates for CCEW PDF overlay
Based on visual analysis of the official CCEW form

Coordinate system: ReportLab uses bottom-left as origin (0,0)
A4 page height = 842 points
"""

# Page 1 - Installation Address and Customer Details
PAGE1_FIELDS = {
    # Serial Number (top right)
    'serial_no': (485, 757),  # height - 85
    
    # INSTALLATION ADDRESS SECTION
    'property_name': (68, 562),  # height - 280
    'install_floor': (68, 512),  # height - 330  
    'install_unit': (155, 512),
    'install_street_number': (210, 512),
    'install_lot_rmb': (380, 512),
    
    'install_street_name': (68, 467),  # height - 375
    'nearest_cross_street': (320, 467),
    
    'install_suburb': (68, 417),  # height - 425
    'install_state': (320, 417),
    'install_postcode': (440, 417),
    
    'pit_pillar_pole_no': (68, 350),  # height - 492
    'nmi': (190, 350),
    'meter_no': (285, 350),
    'aemo_provider_id': (420, 350),
    
    # CUSTOMER DETAILS SECTION  
    'customer_first_name': (68, 247),  # height - 595
    'customer_last_name': (320, 247),
    
    'customer_company_name': (68, 207),  # height - 635
    
    'customer_floor': (68, 142),  # height - 700
    'customer_unit': (155, 142),
    'customer_street_number': (210, 142),
    'customer_lot_rmb': (380, 142),
    
    'customer_street_name': (68, 87),  # height - 755
    'customer_nearest_cross': (320, 87),
    
    'customer_suburb': (68, 32),  # height - 810
    'customer_state': (320, 32),
    'customer_postcode': (440, 32),
}

# Checkboxes for Installation Details (Page 1)
PAGE1_CHECKBOXES = {
    'residential': (70, -95),  # Approximate, needs adjustment
    'commercial': (145, -95),
    'industrial': (220, -95),
    'rural': (295, -95),
    'mixed_development': (400, -95),
    
    'new_work': (145, -118),
    'addition_alteration': (70, -133),
    'installed_meter': (295, -118),
    'network_connection': (450, -118),
}

# Page 2 - Equipment and Installer Details
PAGE2_FIELDS = {
    # Equipment section
    'equip_switchboard_rating': (145, 729),
    'equip_switchboard_number': (295, 729),
    'equip_switchboard_particulars': (395, 729),
    
    'equip_circuits_rating': (145, 706),
    'equip_circuits_number': (295, 706),
    'equip_circuits_particulars': (395, 706),
    
    # Meters section
    'meter_1_number': (120, 609),
    'meter_1_dials': (220, 609),
    
    # Load section
    'load_increase': (250, 464),
    
    # Installer Details
    'installer_first_name': (68, 349),
    'installer_last_name': (320, 349),
    
    'installer_floor': (68, 303),
    'installer_unit': (155, 303),
    'installer_street_number': (210, 303),
    'installer_lot_rmb': (380, 303),
    
    'installer_street_name': (68, 280),
    'installer_nearest_cross': (320, 280),
    
    'installer_suburb': (68, 257),
    'installer_state': (320, 257),
    'installer_postcode': (440, 257),
    
    'installer_email': (68, 234),
    'installer_office_phone': (320, 234),
    
    'installer_license_no': (320, 188),
    'installer_license_expiry': (445, 188),
}

# Page 3 - Test Report and Tester Details  
PAGE3_FIELDS = {
    # Test date
    'test_date': (200, 579),
    
    # Tester Details
    'tester_first_name': (68, 504),
    'tester_last_name': (320, 504),
    
    'tester_floor': (68, 458),
    'tester_unit': (155, 458),
    'tester_street_number': (210, 458),
    'tester_lot_rmb': (380, 458),
    
    'tester_street_name': (68, 435),
    'tester_nearest_cross': (320, 435),
    
    'tester_suburb': (68, 412),
    'tester_state': (320, 412),
    'tester_postcode': (440, 412),
    
    'tester_email': (68, 389),
    
    'tester_license_no': (320, 320),
    'tester_license_expiry': (445, 320),
    
    # Energy Provider
    'energy_provider': (100, 212),
}


def get_field_position(field_name, page=1):
    """
    Get the (x, y) position for a field
    
    Args:
        field_name: Name of the field
        page: Page number (1, 2, or 3)
    
    Returns:
        Tuple of (x, y) coordinates, or None if field not found
    """
    if page == 1:
        return PAGE1_FIELDS.get(field_name) or PAGE1_CHECKBOXES.get(field_name)
    elif page == 2:
        return PAGE2_FIELDS.get(field_name)
    elif page == 3:
        return PAGE3_FIELDS.get(field_name)
    return None
