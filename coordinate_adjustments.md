# CCEW PDF Coordinate Adjustments Needed

## Analysis of Generated PDF vs Official Form

### Page 1 - Installation Address Section

#### Current Issues:
1. **Property Name** - Text appearing in Floor field area
   - Current Y: height - 205
   - Should be: height - 265 (inside the Property Name box)

2. **Floor field** - Shows "Test Building" instead of being empty
   - Need to map to correct field

3. **Street Number** - Position looks approximately correct
   - Current: 220, height - 228
   - May need minor adjustment

4. **Street Name** - Appears correct
   - Current: 65, height - 251

5. **Suburb, State, Postcode** - Need to verify exact positions

### Page 1 - Customer Details Section

Similar positioning issues as Installation Address

### Strategy:
Instead of manually measuring each field, I'll create a Python script that:
1. Extracts the exact pixel positions from a correctly filled official PDF
2. Or uses the form field coordinates if available
3. Or allows interactive clicking to set positions

Let me create an automated coordinate finder that will save us time.
