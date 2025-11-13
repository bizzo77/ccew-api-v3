# Correct X-Coordinates for CCEW Form Fields

Based on reference line analysis of official template:

## Installation Address Section

### Row 1: Property Name
- Property Name: X=60 ✓ (full width field)

### Row 2: Floor/Unit/Street Number/Lot
- Floor: X=60 ✓
- Unit: X=180 ✓
- Street Number: X=260 ❌ (currently 460 - WRONG!)
- Lot/RMB: X=700 ✓

### Row 3: Street Name / Nearest Cross Street
- Street Name: X=60 ✓
- Nearest Cross Street: X=470 ✓

### Row 4: Suburb / State / Postcode
- Suburb: X=60 ✓
- State: X=310 ❌ (currently 470 - WRONG!)
- Postcode: X=437 ❌ (currently 730 - WRONG!)

### Row 5: Pit/Pillar / NMI / Meter / AEMO
- Pit/Pillar: X=60 ✓
- NMI: X=240 ✓
- Meter No: X=420 ✓
- AEMO: X=600 ✓

## Customer Details Section

### Row 1: First Name / Last Name
- First Name: X=60 ✓
- Last Name: X=470 ✓

### Row 2: Company Name
- Company Name: X=60 ✓ (full width field)

### Row 3: Floor/Unit/Street Number/Lot
- Floor: X=60 ✓
- Unit: X=180 ✓
- Street Number: X=260 ❌ (currently 460 - WRONG!)
- Lot/RMB: X=700 ✓

### Row 4: Street Name / Nearest Cross Street
- Street Name: X=60 ✓
- Nearest Cross Street: X=470 ✓

### Row 5: Suburb / State / Postcode
- Suburb: X=60 ✓
- State: X=310 ❌ (currently 470 - WRONG!)
- Postcode: X=437 ❌ (currently 730 - WRONG!)

### Row 6: Email / Office / Mobile
- Email: X=60 ✓
- Office Phone: X=580 ✓
- Mobile Phone: X=720 ✓

## Summary of Required Changes

**Installation Address:**
1. install_street_number: 460 → 260
2. install_state: 470 → 310
3. install_postcode: 730 → 437

**Customer Details:**
1. customer_street_number: 460 → 260
2. customer_state: 470 → 310
3. customer_postcode: 730 → 437

Total: 6 X-coordinate changes needed
