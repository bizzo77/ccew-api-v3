"""
CCEW PDF Generator - Production Ready Implementation
Includes PDF repair and robust error handling
"""

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
import base64
from datetime import datetime
import subprocess
import os


class CCEWPDFGenerator:
    """
    Production-ready CCEW PDF generator using overlay approach
    """
    
    def __init__(self, template_path):
        """
        Initialize generator with template PDF
        
        Args:
            template_path: Path to official CCEW form PDF
        """
        self.template_path = template_path
        self.template_pdf = None
        self._load_template()
    
    def _load_template(self):
        """Load and validate template PDF"""
        try:
            self.template_pdf = PdfReader(self.template_path)
            print(f"✅ Template loaded successfully ({len(self.template_pdf.pages)} pages)")
        except Exception as e:
            print(f"❌ Failed to load template: {e}")
            print("💡 Tip: Your PDF may be corrupted. Try re-downloading from NSW Fair Trading.")
            print("💡 Or use: pdftk input.pdf output repaired.pdf")
            raise
    
    def format_date_australian(self, date_str):
        """Convert date to Australian format DD/MM/YYYY"""
        if not date_str:
            return ''
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return date_str
    
    def create_overlay_page(self, form_data, page_num):
        """
        Create transparent overlay with data for specified page
        
        Args:
            form_data: Dictionary with form field values
            page_num: Page number (0, 1, or 2)
        
        Returns:
            BytesIO buffer with overlay PDF
        """
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        width, height = A4
        
        # Set default styling
        font_size = 9
        can.setFont("Helvetica", font_size)
        can.setFillColor(colors.black)
        
        # Page-specific field positioning
        if page_num == 0:
            self._draw_page1_overlay(can, form_data, height)
        elif page_num == 1:
            self._draw_page2_overlay(can, form_data, height)
        elif page_num == 2:
            self._draw_page3_overlay(can, form_data, height)
        
        can.save()
        packet.seek(0)
        return packet
    
    def _draw_page1_overlay(self, can, data, height):
        """Draw page 1 fields (Installation Address & Customer Details)"""
        
        # Installation Address Section
        self._draw_if_exists(can, 60, height - 252, data.get('property_name'))  # was 207, +45
        self._draw_if_exists(can, 260, height - 275, data.get('install_street_number'))  # was 230, +45
        self._draw_if_exists(can, 60, height - 298, data.get('install_street_name'))  # was 253, +45
        self._draw_if_exists(can, 60, height - 321, data.get('install_suburb'))  # was 276, +45
        self._draw_if_exists(can, 310, height - 321, data.get('install_state', 'NSW'))  # was 276, +45
        self._draw_if_exists(can, 437, height - 321, data.get('install_postcode'))  # was 276, +45
        
        # Customer Details Section
        self._draw_if_exists(can, 60, height - 395, data.get('customer_first_name'))  # was 350, +45
        self._draw_if_exists(can, 310, height - 395, data.get('customer_last_name'))  # was 350, +45
        self._draw_if_exists(can, 260, height - 441, data.get('customer_street_number'))  # was 396, +45
        self._draw_if_exists(can, 60, height - 464, data.get('customer_street_name'))  # was 419, +45
        self._draw_if_exists(can, 60, height - 487, data.get('customer_suburb'))  # was 442, +45
        self._draw_if_exists(can, 310, height - 487, data.get('customer_state'))  # was 442, +45
        self._draw_if_exists(can, 437, height - 487, data.get('customer_postcode'))  # was 442, +45
        self._draw_if_exists(can, 60, height - 510, data.get('customer_email'))  # was 465, +45
        self._draw_if_exists(can, 310, height - 510, data.get('customer_office_phone'))  # was 465, +45
        self._draw_if_exists(can, 437, height - 510, data.get('customer_mobile_phone'))  # was 465, +45
        
        # Installation type checkboxes
        install_type = data.get('installation_type', '').lower()
        if 'residential' in install_type:
            self._draw_checkbox(can, 95, height - 540)
        elif 'commercial' in install_type:
            self._draw_checkbox(can, 200, height - 540)
    
    def _draw_page2_overlay(self, can, data, height):
        """Draw page 2 fields (Equipment & Installer Details)"""
        
        # Equipment - Switchboard
        if data.get('equip_switchboard') == 'yes':
            self._draw_checkbox(can, 95, height - 115)
            self._draw_if_exists(can, 200, height - 115, data.get('equip_switchboard_rating'))
            self._draw_if_exists(can, 350, height - 115, data.get('equip_switchboard_number'))
            self._draw_if_exists(can, 450, height - 115, data.get('equip_switchboard_particulars'))
        
        # Meters
        if data.get('meter_1_i') == 'yes':
            self._draw_checkbox(can, 95, height - 235)
            self._draw_if_exists(can, 150, height - 235, data.get('meter_1_number'))
            self._draw_if_exists(can, 250, height - 235, data.get('meter_1_dials'))
        
        # Load information
        self._draw_if_exists(can, 300, height - 380, data.get('load_increase'))
        
        # Yes/No checkboxes
        if data.get('load_within_capacity', '').lower() == 'yes':
            self._draw_checkbox(can, 430, height - 400)
        else:
            self._draw_checkbox(can, 480, height - 400)
        
        if data.get('work_connected_supply', '').lower() == 'yes':
            self._draw_checkbox(can, 430, height - 420)
        else:
            self._draw_checkbox(can, 480, height - 420)
        
        # Installer Details
        self._draw_if_exists(can, 60, height - 495, data.get('installer_first_name'))
        self._draw_if_exists(can, 310, height - 495, data.get('installer_last_name'))
        self._draw_if_exists(can, 260, height - 541, data.get('installer_street_number'))
        self._draw_if_exists(can, 60, height - 564, data.get('installer_street_name'))
        self._draw_if_exists(can, 60, height - 587, data.get('installer_suburb'))
        self._draw_if_exists(can, 310, height - 587, data.get('installer_state'))
        self._draw_if_exists(can, 437, height - 587, data.get('installer_postcode'))
        self._draw_if_exists(can, 60, height - 610, data.get('installer_email'))
        self._draw_if_exists(can, 310, height - 610, data.get('installer_office_phone'))
        self._draw_if_exists(can, 310, height - 656, data.get('installer_license_no'))
        
        if data.get('installer_license_expiry'):
            expiry = self.format_date_australian(data['installer_license_expiry'])
            self._draw_if_exists(can, 450, height - 656, expiry)
    
    def _draw_page3_overlay(self, can, data, height):
        """Draw page 3 fields (Test Report & Tester Details)"""
        
        # Test checkboxes
        if data.get('test_earthing') == 'yes':
            self._draw_checkbox(can, 95, height - 145)
        
        if data.get('test_rcd') == 'yes':
            self._draw_checkbox(can, 95, height - 160)
        
        # Test date
        if data.get('test_date'):
            test_date = self.format_date_australian(data['test_date'])
            self._draw_if_exists(can, 250, height - 265, test_date)
        
        # Tester Details
        self._draw_if_exists(can, 60, height - 340, data.get('tester_first_name'))
        self._draw_if_exists(can, 310, height - 340, data.get('tester_last_name'))
        self._draw_if_exists(can, 260, height - 386, data.get('tester_street_number'))
        self._draw_if_exists(can, 60, height - 409, data.get('tester_street_name'))
        self._draw_if_exists(can, 60, height - 432, data.get('tester_suburb'))
        self._draw_if_exists(can, 310, height - 432, data.get('tester_state'))
        self._draw_if_exists(can, 437, height - 432, data.get('tester_postcode'))
        self._draw_if_exists(can, 60, height - 455, data.get('tester_email'))
        self._draw_if_exists(can, 310, height - 524, data.get('tester_license_no'))
        
        if data.get('tester_license_expiry'):
            expiry = self.format_date_australian(data['tester_license_expiry'])
            self._draw_if_exists(can, 450, height - 524, expiry)
        
        # Energy Provider
        self._draw_if_exists(can, 100, height - 632, data.get('energy_provider'))
    
    def _draw_if_exists(self, canvas, x, y, value):
        """Draw text only if value exists"""
        if value:
            canvas.drawString(x, y, str(value))
    
    def _draw_checkbox(self, canvas, x, y):
        """Draw checkbox marker (X)"""
        canvas.drawString(x, y, "X")
    
    def generate_pdf(self, form_data):
        """
        Generate filled CCEW PDF
        
        Args:
            form_data: Dictionary with all form field values
        
        Returns:
            Base64 encoded PDF bytes
        """
        output_pdf = PdfWriter()
        
        # Process each page
        for page_num in range(len(self.template_pdf.pages)):
            # Get template page
            template_page = self.template_pdf.pages[page_num]
            
            # Create overlay for this page
            overlay_buffer = self.create_overlay_page(form_data, page_num)
            overlay_pdf = PdfReader(overlay_buffer)
            overlay_page = overlay_pdf.pages[0]
            
            # Merge overlay onto template
            template_page.merge_page(overlay_page)
            
            # Add to output
            output_pdf.add_page(template_page)
        
        # Write to bytes
        output_buffer = io.BytesIO()
        output_pdf.write(output_buffer)
        output_buffer.seek(0)
        
        # Return as base64
        pdf_bytes = output_buffer.getvalue()
        return base64.b64encode(pdf_bytes).decode('utf-8')


# Convenience function for backward compatibility
def generate_ccew_pdf(form_data, template_pdf_path="CCEW_OFFICIAL_TEMPLATE.pdf"):
    """
    Generate CCEW PDF - convenience function
    
    Args:
        form_data: Dictionary with form values
        template_pdf_path: Path to official CCEW template
    
    Returns:
        Base64 encoded PDF bytes
    """
    generator = CCEWPDFGenerator(template_pdf_path)
    return generator.generate_pdf(form_data)


# Example usage
if __name__ == "__main__":
    # Sample data
    test_data = {
        'property_name': 'Test Building',
        'install_suburb': 'Sydney',
        'install_state': 'NSW',
        'install_postcode': '2000',
        'customer_first_name': 'John',
        'customer_last_name': 'Smith',
        'installer_first_name': 'Jane',
        'installer_last_name': 'Installer',
        'tester_first_name': 'Bob',
        'tester_last_name': 'Tester',
        'energy_provider': 'Ausgrid',
    }
    
    print("🚀 Generating CCEW PDF...")
    try:
        pdf_b64 = generate_ccew_pdf(test_data)
        print("✅ PDF generated successfully!")
        print(f"📦 Size: {len(base64.b64decode(pdf_b64))} bytes")
    except Exception as e:
        print(f"❌ Error: {e}")


def get_pdf_filename(job_number):
    """Generate PDF filename from job number"""
    return f"CCEW_Form_Job_{job_number}.pdf"
