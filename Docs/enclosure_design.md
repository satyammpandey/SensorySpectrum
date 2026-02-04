# 📦 Enclosure Design - Sensory Spectrum

3D printable case specifications and assembly guide for professional-looking portable devices.

---

## Table of Contents

1. [Design Overview](#design-overview)
2. [Sender Unit Enclosure](#sender-unit-enclosure)
3. [Receiver Unit Enclosure](#receiver-unit-enclosure)
4. [Materials & Printing](#materials--printing)
5. [Assembly Instructions](#assembly-instructions)
6. [Alternative Designs](#alternative-designs)

---

## Design Overview

### Design Goals

- **Portable**: Pocket-sized, lightweight design
- **Durable**: Impact-resistant for daily use
- **Accessible**: Easy to hold and operate
- **Professional**: Clean, modern aesthetic
- **Functional**: Proper ventilation, cable management, status visibility

---

### Design Specifications

**Sender Unit:**
- Dimensions: 80mm × 50mm × 25mm
- Weight: ~60g (with components)
- Material: PLA or PETG
- Color: White or light colors (for visibility)

**Receiver Unit:**
- Dimensions: 100mm × 65mm × 30mm
- Weight: ~120g (with components)
- Material: PLA or PETG
- Color: Black or dark colors (for audio equipment aesthetic)

---

## Sender Unit Enclosure

### External Features

```
Top View:
┌──────────────────────────────────┐
│                                  │
│         SENSORY SPECTRUM         │ ← Logo/Text
│                                  │
│    ┌─────────────────────┐      │
│    │    TCS34725         │      │ ← Sensor Window (clear acrylic)
│    │    Sensor Window    │      │
│    └─────────────────────┘      │
│                                  │
│               ○                  │ ← LED Indicator Hole
│                                  │
└──────────────────────────────────┘

Side View:
         ┌─────────────┐
    ┌────┤ Sensor Area ├────┐
    │    └─────────────┘    │
    │                       │ ← 25mm height
    │  [Components Inside]  │
    └───────────────────────┘
         [USB Port]

Front View:
┌─────────────────────────┐
│    ╔═══════════════╗    │ ← Sensor Window
│    ║               ║    │
│    ║   TCS34725    ║    │
│    ║               ║    │
│    ╚═══════════════╝    │
│                         │
│         LED ○           │ ← Status LED
│                         │
└─────────────────────────┘
```

---

### Internal Layout

```
┌────────────────────────────────────────┐
│  Top Shell                             │
│  ┌──────────────────────────────────┐  │
│  │  Sensor Mount (recessed)         │  │
│  │  ┌────────────────────┐          │  │
│  │  │    TCS34725        │          │  │
│  │  │    Mounting Holes  │          │  │
│  │  └────────────────────┘          │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘

┌────────────────────────────────────────┐
│  Bottom Shell                          │
│  ┌──────────────────────────────────┐  │
│  │  ESP32 Mount                     │  │
│  │  ┌──────────────────┐            │  │
│  │  │     ESP32        │            │  │
│  │  │  Screw Mounts    │            │  │
│  │  └──────────────────┘            │  │
│  │                                  │  │
│  │  USB Port Cutout ────────►       │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

### Component Mounting

**ESP32 Mounting Posts:**
```
Diameter: 3mm (for M2.5 screws)
Height: 5mm
Spacing: Match ESP32 mounting holes
```

**Sensor Window:**
```
Material: Clear acrylic sheet (2mm thick)
Size: 30mm × 20mm
Mounting: Press-fit with retention clips
Purpose: Protect sensor while allowing light
```

**LED Light Pipe:**
```
Material: Clear or translucent filament
Diameter: 3mm
Length: 5mm
Purpose: Channel LED light to exterior
```

---

### Ventilation

```
Side Vents Pattern:
│││││││ ← 1mm wide slots
│││││││    2mm spacing
│││││││    Angled 45° for water resistance
```

---

### Assembly Features

**Snap-Fit Clips:**
```
Location: Four corners
Type: Cantilever snap
Retention Force: 5-10N
Allows: Tool-free assembly
```

**Screw Bosses (Optional):**
```
For permanent assembly:
- 4x M2 screw holes
- Self-tapping threads
- 8mm depth
```

---

## Receiver Unit Enclosure

### External Features

```
Top View:
┌──────────────────────────────────────────┐
│                                          │
│         SENSORY SPECTRUM                 │
│            RECEIVER                      │
│                                          │
│    ┌───────────────────────────┐        │
│    │  ////////////////////     │        │ ← Speaker Grille
│    │  // SPEAKER GRILLE //     │        │
│    │  ////////////////////     │        │
│    └───────────────────────────┘        │
│                                          │
│              ○  ○  ○                     │ ← LED Indicators
│                                          │
└──────────────────────────────────────────┘

Side View:
         ┌──────────────┐
    ┌────┤ Speaker Area ├────┐
    │    └──────────────┘    │
    │                        │ ← 30mm height
    │  [Components Inside]   │
    └────────────────────────┘
    [USB] [SD Card Slot]

Back View:
┌──────────────────────────┐
│                          │
│    ┌────┐   SD ┌──┐     │
│ USB│    │  CARD│  │     │ ← Port cutouts
│    └────┘      └──┘     │
│                          │
└──────────────────────────┘
```

---

### Internal Layout

```
Top Shell:
┌────────────────────────────────────────────┐
│  ╔═══════════════════════════════════╗    │
│  ║   Speaker Grille (honeycomb)     ║    │
│  ║   Hole pattern for audio         ║    │
│  ╚═══════════════════════════════════╝    │
│                                            │
│  Speaker Mount Ring (45mm dia)             │
└────────────────────────────────────────────┘

Bottom Shell:
┌────────────────────────────────────────────┐
│  Component Bay:                            │
│  ┌──────────────┐    ┌──────────────┐     │
│  │   ESP32      │    │  DFPlayer    │     │
│  │   Mount      │    │  Mini Mount  │     │
│  └──────────────┘    └──────────────┘     │
│                                            │
│  Cable channels and wire management        │
└────────────────────────────────────────────┘
```

---

### Speaker Mount

```
Speaker Mounting System:

┌─────────────────────────┐
│   Retention Ring        │
│   ┌─────────────────┐   │
│   │   Speaker       │   │ ← 40-45mm diameter
│   │   (8Ω, 3-5W)    │   │
│   └─────────────────┘   │
│   Foam Gasket           │
└─────────────────────────┘

Mounting Method:
- Screw-down retaining ring
- Foam gasket for seal
- 4x M2 screws
- Acoustic chamber behind speaker
```

---

### Cable Management

```
Internal Cable Routing:

┌─────────────────────────────────┐
│                                 │
│  ESP32 ──┬──> DFPlayer (UART)  │
│          │                      │
│          ├──> Speaker           │
│          │                      │
│          └──> USB (External)    │
│                                 │
│  Cable Clips: ═══►              │ ← Integrated clips
│  Wire Channels: ────────►       │ ← Recessed paths
│                                 │
└─────────────────────────────────┘
```

---

### SD Card Access

```
SD Card Slot:
┌────────────┐
│  ┌──────┐  │ ← External access panel
│  │ PUSH │  │    (magnetic or snap-fit)
│  │  SD  │  │
│  └──────┘  │
└────────────┘

Features:
- Push-to-eject mechanism
- Dust cover (sliding)
- Label area for card info
```

---

## Materials & Printing

### Recommended Materials

**PLA (Polylactic Acid):**
- **Pros**: Easy to print, good finish, eco-friendly
- **Cons**: Less heat resistant, brittle in cold
- **Use for**: Prototypes, indoor use
- **Print temp**: 190-220°C

**PETG (Polyethylene Terephthalate Glycol):**
- **Pros**: Strong, flexible, UV resistant
- **Cons**: Harder to print, stringing issues
- **Use for**: Final product, outdoor use
- **Print temp**: 220-250°C

**ABS (Acrylonitrile Butadiene Styrene):**
- **Pros**: Very strong, heat resistant
- **Cons**: Requires heated bed, fumes
- **Use for**: High durability needs
- **Print temp**: 220-250°C

---

### Print Settings

**Layer Height:** 0.2mm (standard) or 0.15mm (high quality)  
**Infill:** 20-30% (grid or gyroid pattern)  
**Wall Thickness:** 3 perimeters (1.2mm)  
**Top/Bottom Layers:** 4-5 layers  
**Print Speed:** 50-60mm/s  
**Support:** Only for overhangs >45°  
**Bed Adhesion:** Brim (5mm) for large parts  

---

### Special Features Printing

**Sensor Window Frame:**
```
Print Settings:
- Layer height: 0.1mm (smoother finish)
- Infill: 100% (solid)
- Print speed: 30mm/s (precision)
- No support needed (print face-down)
```

**Speaker Grille:**
```
Print Settings:
- Layer height: 0.2mm
- Pattern: Honeycomb or radial
- Infill: 0% (hollow structure)
- Bridge settings: Enabled for holes
```

**Snap-Fit Clips:**
```
Print Settings:
- Orientation: Clips perpendicular to bed
- Layer lines: Along stress direction
- Infill: 100% at clips
- Test fit before final print
```

---

### Post-Processing

**Sanding:**
1. 220 grit - Remove layer lines
2. 400 grit - Smooth surface
3. 600 grit - Fine finish (optional)

**Painting (Optional):**
1. Prime with plastic primer
2. 2-3 light coats of paint
3. Clear coat for protection

**Assembly Prep:**
1. Clean holes with drill bit
2. Test fit all components
3. Deburr edges with knife

---

## Assembly Instructions

### Sender Unit Assembly

**Step 1: Install Components**

```
Order of assembly:
1. ESP32 → Screw to bottom shell (4x M2.5 screws)
2. TCS34725 → Mount in sensor bracket
3. LED → Insert into light pipe
4. Wiring → Route through cable channels
```

**Step 2: Install Sensor Window**

```
1. Clean acrylic window
2. Apply thin foam gasket (optional, for dust seal)
3. Press-fit into top shell recess
4. Secure with retention clips
```

**Step 3: Close Enclosure**

```
1. Route wires neatly
2. Align top and bottom shells
3. Press together until clips engage
4. Optional: Add 4x M2 screws for permanence
```

---

### Receiver Unit Assembly

**Step 1: Install Electronics**

```
Order:
1. ESP32 → Mount in bottom shell
2. DFPlayer Mini → Mount adjacent to ESP32
3. Wire connections (UART, power)
4. Insert SD card with audio files
```

**Step 2: Install Speaker**

```
1. Place foam gasket on speaker mount
2. Position speaker (check polarity)
3. Place retaining ring
4. Secure with 4x M2 screws
5. Test audio before closing
```

**Step 3: Final Assembly**

```
1. Check all connections
2. Route USB cable through port
3. Align top shell with grille facing up
4. Snap together
5. Test all functions before sealing
```

---

### Testing Checklist

Before permanent assembly:

- [ ] Power on both units
- [ ] Check LED indicators
- [ ] Test WiFi connection
- [ ] Verify color detection
- [ ] Check audio output
- [ ] Test all ports accessible
- [ ] Verify buttons/switches work
- [ ] Check thermal performance (10 min run)

---

## Alternative Designs

### Wearable Design (Wristband Style)

```
Sender as Wrist-Mounted Unit:
┌────────────────────────────┐
│     Velcro/Elastic Strap   │
│  ┌──────────────────────┐  │
│  │   Sensor on Top      │  │
│  │   ESP32 on Bottom    │  │
│  └──────────────────────┘  │
│     Battery Compartment    │
└────────────────────────────┘

Dimensions: 60mm × 40mm × 20mm
Weight: <80g
Battery: 500mAh LiPo (3-4 hours)
```

---

### Keychain Design (Ultra-Portable)

```
Micro Sender Unit:
┌─────────────┐
│   Keyring   │ ○
│   ┌───────┐ │
│   │Sensor │ │
│   │  &    │ │ ← 35mm × 25mm × 15mm
│   │ESP32  │ │
│   └───────┘ │
│   [USB-C]   │
└─────────────┘

Features:
- Integrated battery (250mAh)
- Ruggedized case (TPU)
- IP54 water resistance
```

---

### Desktop Station Design

```
Receiver as Desktop Base:
┌──────────────────────────┐
│    Speaker Array         │
│  ╔════════════════════╗  │
│  ║  Stereo Speakers   ║  │ ← Better audio
│  ╚════════════════════╝  │
│                          │
│   [Volume] [Power]       │ ← Physical controls
│   ┌──────────────────┐   │
│   │  Status Display  │   │ ← OLED screen (optional)
│   └──────────────────┘   │
└──────────────────────────┘

Dimensions: 150mm × 100mm × 50mm
Power: Wall adapter (better quality)
Features: Volume knob, display, better speakers
```

---

### Modular Design

```
Stackable Component Bays:

┌────────────────┐
│  Sensor Bay    │ ← Top module
├────────────────┤
│  ESP32 Bay     │ ← Middle module
├────────────────┤
│  Battery Bay   │ ← Bottom module
└────────────────┘

Advantages:
- Easy repairs
- Upgradeable components
- Custom configurations
- Educational demonstrations
```

---

## Design Files

### File Formats

Provide designs in multiple formats:
- **STL**: For 3D printing
- **STEP**: For CAD editing
- **OBJ**: For rendering
- **PDF**: Assembly diagrams

### Recommended CAD Software

**Free:**
- Fusion 360 (free for students/hobbyists)
- FreeCAD
- Tinkercad (browser-based, beginner-friendly)
- Blender (for organic shapes)

**Paid:**
- SolidWorks
- AutoCAD
- Inventor

---

## Design Guidelines Summary

**Do's:**
✓ Leave 2-3mm clearance around components  
✓ Include mounting posts for PCBs  
✓ Design snap-fits for easy access  
✓ Add ventilation holes  
✓ Label ports and indicators  
✓ Use chamfers on edges (0.5-1mm)  
✓ Test print critical parts first  

**Don'ts:**
✗ Don't make walls thinner than 1.5mm  
✗ Avoid sharp internal corners (stress points)  
✗ Don't trap components without access  
✗ Avoid overhangs >45° without support  
✗ Don't ignore cable routing  
✗ Avoid tight tolerances (<0.2mm)  

---

## Cost Estimate

**3D Printing Costs:**

| Item | Material (g) | Cost (PLA @ $20/kg) |
|------|--------------|---------------------|
| Sender shell | ~50g | $1.00 |
| Receiver shell | ~80g | $1.60 |
| Mounting brackets | ~10g | $0.20 |
| **Total** | **~140g** | **~$2.80** |

**Additional Materials:**
- Acrylic sheet: $1-2
- Foam gaskets: $0.50
- M2/M2.5 screws: $0.50
- **Total accessories: ~$2-3**

**Grand Total: $5-6** (enclosures only)

---

End of Enclosure Design Documentation.
