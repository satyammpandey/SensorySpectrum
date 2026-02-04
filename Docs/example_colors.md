# 🎨 Example Colors - Sensory Spectrum

Comprehensive color testing guide with RGB values, real-world objects, and expected detection results.

---

## Table of Contents

1. [Primary Colors](#primary-colors)
2. [Secondary Colors](#secondary-colors)
3. [Neutral Colors](#neutral-colors)
4. [Real-World Test Objects](#real-world-test-objects)
5. [Challenging Colors](#challenging-colors)
6. [Color Calibration Reference](#color-calibration-reference)
7. [Testing Protocols](#testing-protocols)

---

## Primary Colors

### Red

**RGB Values:**
- Pure Red: (255, 0, 0)
- Typical Range: R > 200, G < 80, B < 80
- HSV: Hue 0°, Saturation 100%, Value 100%

**Common Test Objects:**
- Red apple (Fuji, Red Delicious)
- Red bell pepper
- Tomato (ripe)
- Red construction paper
- Red fabric (cotton)
- Red plastic (toys)
- Stop sign (outdoor test)
- Red book cover
- Red marker/crayon
- Red rose petals

**Expected Sensor Reading:**
```
Raw Values: R: 1200-1800, G: 200-400, B: 150-350
Normalized: R: 85-95%, G: 5-10%, B: 5-10%
Confidence: 90-95%
Detection: "Red"
```

**Common Variations:**
- **Crimson**: R: 220, G: 20, B: 60 → Still detected as "Red"
- **Scarlet**: R: 255, G: 36, B: 0 → "Red" or "Orange" (borderline)
- **Maroon**: R: 128, G: 0, B: 0 → May be "Red" or "Black" (low intensity)

---

### Green

**RGB Values:**
- Pure Green: (0, 255, 0)
- Typical Range: R < 80, G > 200, B < 80
- HSV: Hue 120°, Saturation 100%, Value 100%

**Common Test Objects:**
- Green apple (Granny Smith)
- Fresh grass
- Green leaves (spinach, lettuce)
- Green construction paper
- Lime (citrus fruit)
- Green plastic bottle
- Green traffic light (indoor simulation)
- Green fabric
- Green marker/crayon
- Cucumber

**Expected Sensor Reading:**
```
Raw Values: R: 200-400, G: 1200-1800, B: 200-400
Normalized: R: 5-10%, G: 85-95%, B: 5-10%
Confidence: 90-95%
Detection: "Green"
```

**Common Variations:**
- **Lime Green**: R: 50, G: 205, B: 50 → "Green" or "Yellow-Green"
- **Forest Green**: R: 34, G: 139, B: 34 → "Green" (may need calibration)
- **Olive**: R: 128, G: 128, B: 0 → May be "Green" or "Yellow"

---

### Blue

**RGB Values:**
- Pure Blue: (0, 0, 255)
- Typical Range: R < 80, G < 80, B > 200
- HSV: Hue 240°, Saturation 100%, Value 100%

**Common Test Objects:**
- Blue pen/marker
- Blue construction paper
- Blueberries
- Blue fabric (denim)
- Clear blue sky (outdoor)
- Blue plastic items
- Blue book cover
- Blue tape (painter's tape)
- Blue sticky notes
- Blue LED (off device)

**Expected Sensor Reading:**
```
Raw Values: R: 150-350, G: 200-450, B: 1200-1800
Normalized: R: 5-10%, G: 10-15%, B: 80-90%
Confidence: 85-92%
Detection: "Blue"
```

**Common Variations:**
- **Navy Blue**: R: 0, G: 0, B: 128 → "Blue" or "Black" (low intensity)
- **Sky Blue**: R: 135, G: 206, B: 235 → "Blue" or "Cyan"
- **Royal Blue**: R: 65, G: 105, B: 225 → "Blue" (strong detection)

---

## Secondary Colors

### Yellow

**RGB Values:**
- Pure Yellow: (255, 255, 0)
- Typical Range: R > 200, G > 200, B < 80
- HSV: Hue 60°, Saturation 100%, Value 100%

**Common Test Objects:**
- Banana (ripe)
- Yellow bell pepper
- Lemon
- Yellow sticky notes
- Yellow highlighter
- Yellow construction paper
- Corn kernels
- Yellow flowers (sunflower, daffodil)
- Yellow fabric
- Cheese (cheddar)

**Expected Sensor Reading:**
```
Raw Values: R: 1200-1700, G: 1200-1700, B: 200-400
Normalized: R: 45-50%, G: 45-50%, B: 5-10%
Confidence: 85-92%
Detection: "Yellow"
```

**Common Variations:**
- **Golden Yellow**: R: 255, G: 215, B: 0 → "Yellow" or "Orange"
- **Pale Yellow**: R: 255, G: 255, B: 224 → "Yellow" or "White"
- **Mustard**: R: 255, G: 219, B: 88 → "Yellow"

---

### Cyan

**RGB Values:**
- Pure Cyan: (0, 255, 255)
- Typical Range: R < 80, G > 200, B > 200
- HSV: Hue 180°, Saturation 100%, Value 100%

**Common Test Objects:**
- Cyan printer paper
- Turquoise beads
- Cyan marker
- Pool water (light reflection)
- Cyan plastic items
- Light blue fabric
- Cyan construction paper
- Aqua-colored items
- Cyan sticky notes
- Teal accessories

**Expected Sensor Reading:**
```
Raw Values: R: 200-400, G: 1100-1600, B: 1100-1600
Normalized: R: 5-10%, G: 45-50%, B: 45-50%
Confidence: 80-88%
Detection: "Cyan"
```

**Common Variations:**
- **Turquoise**: R: 64, G: 224, B: 208 → "Cyan"
- **Aquamarine**: R: 127, G: 255, B: 212 → "Cyan" or "Green"
- **Teal**: R: 0, G: 128, B: 128 → "Cyan" or "Green" (lower intensity)

---

### Magenta

**RGB Values:**
- Pure Magenta: (255, 0, 255)
- Typical Range: R > 200, G < 80, B > 200
- HSV: Hue 300°, Saturation 100%, Value 100%

**Common Test Objects:**
- Magenta printer paper
- Pink/purple flowers (orchids)
- Magenta marker
- Purple cabbage (inner leaves)
- Magenta construction paper
- Fuchsia fabric
- Purple grapes (dark)
- Magenta plastic items
- Purple nail polish
- Magenta sticky notes

**Expected Sensor Reading:**
```
Raw Values: R: 1200-1700, G: 200-400, B: 1200-1700
Normalized: R: 45-50%, G: 5-10%, B: 45-50%
Confidence: 80-88%
Detection: "Magenta"
```

**Common Variations:**
- **Fuchsia**: R: 255, G: 0, B: 255 → "Magenta" (exact match)
- **Hot Pink**: R: 255, G: 105, B: 180 → "Magenta" or "Red"
- **Purple**: R: 128, G: 0, B: 128 → "Magenta" or "Purple"

---

### Orange

**RGB Values:**
- Pure Orange: (255, 165, 0)
- Typical Range: R > 200, G 120-200, B < 80
- HSV: Hue 30°, Saturation 100%, Value 100%

**Common Test Objects:**
- Orange (fruit)
- Carrot
- Orange bell pepper
- Orange construction paper
- Pumpkin
- Orange marker
- Sweet potato
- Orange fabric
- Traffic cone
- Orange sticky notes

**Expected Sensor Reading:**
```
Raw Values: R: 1400-1800, G: 800-1200, B: 150-350
Normalized: R: 50-60%, G: 30-40%, B: 5-10%
Confidence: 85-92%
Detection: "Orange"
```

**Common Variations:**
- **Dark Orange**: R: 255, G: 140, B: 0 → "Orange"
- **Light Orange**: R: 255, G: 200, B: 124 → "Orange" or "Yellow"
- **Burnt Orange**: R: 204, G: 85, B: 0 → "Orange" or "Red"

---

### Purple

**RGB Values:**
- Purple: (128, 0, 128)
- Typical Range: R 100-180, G < 80, B 120-200
- HSV: Hue 300°, Saturation 100%, Value 50%

**Common Test Objects:**
- Purple grapes
- Eggplant (skin)
- Purple cabbage
- Purple construction paper
- Lavender flowers
- Purple marker
- Purple fabric
- Plums
- Purple onion
- Purple sticky notes

**Expected Sensor Reading:**
```
Raw Values: R: 800-1200, G: 200-400, B: 1000-1400
Normalized: R: 35-40%, G: 5-10%, B: 40-50%
Confidence: 80-88%
Detection: "Purple"
```

**Common Variations:**
- **Violet**: R: 138, G: 43, B: 226 → "Purple" or "Magenta"
- **Lavender**: R: 230, G: 230, B: 250 → "Purple" or "White" (pale)
- **Indigo**: R: 75, G: 0, B: 130 → "Purple" or "Blue"

---

## Neutral Colors

### White

**RGB Values:**
- Pure White: (255, 255, 255)
- Typical Range: R > 220, G > 220, B > 220 (all high and balanced)
- HSV: Hue any, Saturation 0%, Value 100%

**Common Test Objects:**
- White printer paper (standard for calibration)
- White wall
- White ceramic plate
- White fabric (cotton, polyester)
- White plastic (milk bottle)
- White foam board
- Egg shell
- White flower petals
- White construction paper
- Milk (in glass)

**Expected Sensor Reading:**
```
Raw Values: R: 1600-2000, G: 1600-2000, B: 1600-2000
Normalized: R: 33%, G: 33%, B: 33% (balanced)
Confidence: 88-95%
Detection: "White"
Total Intensity: Very High (>4500)
```

**Common Variations:**
- **Cream/Off-White**: R: 255, G: 253, B: 208 → "White" or "Yellow" (borderline)
- **Ivory**: R: 255, G: 255, B: 240 → "White"
- **Snow White**: R: 255, G: 250, B: 250 → "White"

---

### Black

**RGB Values:**
- Pure Black: (0, 0, 0)
- Typical Range: R < 50, G < 50, B < 50 (all low)
- HSV: Hue any, Saturation any, Value 0%

**Common Test Objects:**
- Black construction paper
- Black fabric (felt, cotton)
- Black plastic
- Black marker/pen
- Black foam board
- Charcoal
- Black rubber
- Black book cover
- Black tape
- Smartphone screen (off)

**Expected Sensor Reading:**
```
Raw Values: R: 100-300, G: 100-300, B: 100-300
Normalized: R: 33%, G: 33%, B: 33% (balanced but low)
Confidence: 85-92%
Detection: "Black"
Total Intensity: Very Low (<600)
```

**Common Variations:**
- **Dark Gray**: R: 80, G: 80, B: 80 → "Black" or borderline
- **Jet Black**: R: 0, G: 0, B: 0 → "Black" (strong detection)
- **Charcoal**: R: 54, G: 69, B: 79 → "Black" (slight blue tint)

---

## Real-World Test Objects

### Kitchen/Food Items

| Object | Expected Color | Confidence | Notes |
|--------|---------------|------------|-------|
| Red Apple (Fuji) | Red | 92-95% | Consistent surface |
| Green Apple (Granny Smith) | Green | 90-94% | Slightly waxy surface |
| Banana (ripe) | Yellow | 88-92% | Test at different ripeness |
| Banana (unripe) | Green | 85-90% | May show Yellow tones |
| Orange | Orange | 90-94% | Textured surface |
| Blueberries | Blue/Purple | 80-85% | Small size, test multiple |
| Tomato | Red | 90-94% | Glossy surface |
| Lemon | Yellow | 88-92% | Textured skin |
| Lime | Green | 88-92% | Similar to lemon |
| Eggplant | Purple | 85-90% | Dark, may read Black |
| Carrot | Orange | 88-92% | Test peeled vs unpeeled |
| Cucumber | Green | 88-92% | Smooth surface |
| Bell Pepper (Red) | Red | 90-94% | Glossy |
| Bell Pepper (Green) | Green | 88-92% | Darker than apple |
| Bell Pepper (Yellow) | Yellow | 88-92% | Bright |
| Strawberry | Red | 85-90% | Small seeds affect reading |

---

### Clothing/Fabric

| Item | Expected Color | Confidence | Notes |
|------|---------------|------------|-------|
| White T-shirt | White | 92-96% | Best calibration reference |
| Black Jeans | Black | 90-94% | Denim may have slight blue |
| Red Cotton Shirt | Red | 88-92% | Fabric texture affects reading |
| Blue Denim | Blue | 85-90% | May show purple tones |
| Yellow Safety Vest | Yellow | 90-94% | Reflective material |
| Green Jacket | Green | 85-90% | Varies by fabric type |
| Orange Hoodie | Orange | 88-92% | Fleece texture |
| Purple Scarf | Purple | 82-88% | Lighter fabrics harder |
| Pink/Magenta Dress | Magenta | 80-86% | Depends on shade |
| Gray Sweater | Black/White | 75-85% | May be ambiguous |

---

### Stationery/Office

| Item | Expected Color | Confidence | Notes |
|------|---------------|------------|-------|
| White Printer Paper | White | 95-98% | **Primary calibration object** |
| Post-it Notes (Yellow) | Yellow | 90-94% | Standard office item |
| Post-it Notes (Pink) | Magenta/Red | 82-88% | Depends on exact shade |
| Post-it Notes (Blue) | Blue | 88-92% | Lighter shades |
| Post-it Notes (Green) | Green | 88-92% | Mint green variety |
| Red Pen | Red | 90-94% | Consistent plastic |
| Blue Pen | Blue | 88-92% | Common test object |
| Highlighter (Yellow) | Yellow | 92-95% | Very bright |
| Highlighter (Pink) | Magenta | 85-90% | Fluorescent |
| Highlighter (Green) | Green | 88-92% | Fluorescent |
| Black Marker | Black | 92-95% | Matte finish |
| Construction Paper | Varies | 90-95% | Excellent test set |

---

## Challenging Colors

### Problematic Color Combinations

**1. Pastel Colors**
```
Issue: Low saturation, high brightness
Example: Pastel pink, baby blue, mint green
Expected: May read as "White" if too pale
Solution: Increase sensor gain, reduce MIN_INTENSITY threshold
```

**2. Dark Colors**
```
Issue: Low total light intensity
Example: Navy blue, dark brown, burgundy
Expected: May all read as "Black"
Solution: Improve lighting, increase integration time
```

**3. Metallic/Reflective Surfaces**
```
Issue: Specular reflection, inconsistent readings
Example: Chrome, gold foil, mirrors
Expected: Unstable readings, low confidence
Solution: Angle sensor to avoid direct reflection
```

**4. Transparent/Translucent Objects**
```
Issue: Light passes through instead of reflecting
Example: Clear glass, water, transparent plastic
Expected: Reads background color or "White"
Solution: Place object on white background
```

**5. Multicolored/Patterned Objects**
```
Issue: Multiple colors in sensor field of view
Example: Striped fabric, polka dots, gradients
Expected: Averaged color or unstable readings
Solution: Focus on single-color areas
```

---

### Borderline Color Pairs

**Colors that may be confused:**

| Color 1 | Color 2 | Distinguishing Factor | Tips |
|---------|---------|----------------------|------|
| Orange | Red | Green channel (Orange > Red) | Check G: 120+ for Orange |
| Orange | Yellow | Red channel (Orange > Yellow) | Check R: R/G ratio |
| Yellow | White | Total intensity (White higher) | White has R+G+B > 4500 |
| Cyan | Blue | Green channel (Cyan > Blue) | Cyan has more green |
| Cyan | Green | Blue channel (Cyan > Green) | Cyan has more blue |
| Magenta | Purple | Intensity (Purple darker) | Purple R+G+B < Magenta |
| Purple | Blue | Red channel (Purple > Blue) | Purple has significant red |
| Black | Dark Colors | Total intensity (Black lowest) | Black < 600 total |

---

## Color Calibration Reference

### Standard Calibration Procedure

**Required Object:** White printer paper (80gsm, standard white)

**Steps:**
1. Place sensor 5-7cm from white paper
2. Ensure even lighting (avoid shadows)
3. Run calibration routine (10 samples)
4. System calculates R, G, B correction factors
5. Factors stored in memory

**Expected Calibration Results:**
```
Raw readings from white paper:
R: 1800, G: 1600, B: 1700

Calculated factors:
R factor: 1.0 (reference)
G factor: 1.125 (to match R)
B factor: 1.059 (to match R)

After calibration, white reads as:
R: 1800, G: 1800, B: 1800 (balanced)
```

---

### Lighting Conditions

**Optimal Conditions:**
- Natural daylight (not direct sun): Best overall
- LED white light (5000-6500K): Good consistency
- Distance from source: 50-150cm overhead
- Avoid: Colored lights, flickering fluorescent

**Testing Different Lighting:**

| Lighting Type | Impact | Compensation |
|--------------|--------|--------------|
| Direct sunlight | Oversaturation | Move to shade |
| Incandescent | Yellow tint | Recalibrate |
| Fluorescent | Green tint | Recalibrate |
| LED (cool white) | Slight blue tint | Usually OK |
| LED (warm white) | Slight yellow tint | Recalibrate |
| Dim lighting | Low readings | Increase gain |
| Shadow | Inconsistent | Improve lighting |

---

## Testing Protocols

### Basic Test Sequence

**Test 1: Primary Colors**
```
1. Red apple → Should detect "Red" (90%+)
2. Green apple → Should detect "Green" (90%+)
3. Blue pen → Should detect "Blue" (85%+)

Pass criteria: All 3 detected with >85% confidence
```

**Test 2: Secondary Colors**
```
1. Banana → Should detect "Yellow" (85%+)
2. Orange → Should detect "Orange" (85%+)
3. Purple grapes → Should detect "Purple" (80%+)

Pass criteria: All 3 detected with >80% confidence
```

**Test 3: Neutrals**
```
1. White paper → Should detect "White" (90%+)
2. Black marker → Should detect "Black" (85%+)

Pass criteria: Both detected correctly
```

---

### Advanced Test Sequence

**Test 4: Borderline Colors**
```
1. Pale yellow → "Yellow" or "White"
2. Dark blue → "Blue" or "Black"
3. Light orange → "Orange" or "Yellow"

Pass criteria: Consistent reading (not flickering)
```

**Test 5: Varying Distances**
```
Test red apple at:
- 2cm: Should still detect
- 5cm: Optimal (highest confidence)
- 10cm: Should still detect
- 15cm: May fail or low confidence

Pass criteria: Reliable detection 2-10cm
```

**Test 6: Speed Test**
```
Quickly move sensor across:
Red → Green → Blue → Yellow

Pass criteria: 
- Each color detected within 1 second
- No phantom detections between colors
```

---

### Stress Test

**Environmental Challenges:**
```
1. Low light (evening/indoor): Test all colors
2. Bright light (outdoor noon): Test all colors
3. Mixed lighting: Test problematic pairs
4. Rapid testing: 50 detections in 5 minutes

Pass criteria: >80% accuracy maintained
```

---

### Test Data Logging

**Record Format:**
```
Test Date: YYYY-MM-DD
Lighting: [Type, intensity]
Temperature: [°C]
Calibration: [Last calibration date]

Object | Expected | Detected | Confidence | Raw R | Raw G | Raw B | Pass/Fail
-------|----------|----------|------------|-------|-------|-------|----------
Apple  | Red      | Red      | 94%        | 1650  | 320   | 280   | PASS
Banana | Yellow   | Yellow   | 89%        | 1580  | 1520  | 340   | PASS
...
```

---

### Accuracy Calculation

```
Accuracy = (Correct Detections / Total Tests) × 100%

Target Accuracy: >85% overall

Per-color accuracy:
- Primary colors (R, G, B): >90%
- Secondary colors: >85%
- Neutrals (White, Black): >90%
- Borderline colors: >75%
```

---

End of Example Colors Documentation.