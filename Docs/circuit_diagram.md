# 🔌 Circuit Diagrams - Sensory Spectrum

Detailed wiring diagrams and circuit specifications for both sender and receiver units.

---

## Table of Contents

1. [Component Specifications](#component-specifications)
2. [Sender Unit Circuit](#sender-unit-circuit)
3. [Receiver Unit Circuit](#receiver-unit-circuit)
4. [Power Requirements](#power-requirements)
5. [PCB Design Guidelines](#pcb-design-guidelines)
6. [Testing Points](#testing-points)

---

## Component Specifications

### ESP32 Development Board

**Pin Configuration:**
```
ESP32 (30-pin variant)
┌─────────────────────────────────┐
│                                 │
│  EN    ○                    ○ D23│
│  VP    ○                    ○ D22│ ← SCL (I2C Clock)
│  VN    ○                    ○ TX0│
│  D34   ○                    ○ RX0│
│  D35   ○                    ○ D21│ ← SDA (I2C Data)
│  D32   ○                    ○ GND│
│  D33   ○                    ○ D19│
│  D25   ○                    ○ D18│
│  D26   ○                    ○ D5 │
│  D27   ○                    ○ D17│ ← TX (UART)
│  D14   ○                    ○ D16│ ← RX (UART)
│  D12   ○                    ○ D4 │
│  GND   ○                    ○ D0 │
│  D13   ○                    ○ D2 │ ← Built-in LED
│  D9    ○                    ○ D15│
│  D10   ○                    ○ D8 │
│  D11   ○                    ○ D7 │
│  VIN   ○                    ○ D6 │
│  5V    ○                    ○ GND│
│  3.3V  ○                    ○ 3.3V│
│                                 │
└─────────────────────────────────┘
```

**Power Specifications:**
- Operating Voltage: 3.3V (internal)
- Input Voltage: 5V via USB or VIN (7-12V)
- Max Current per GPIO: 40mA
- Total GPIO Current: 200mA

---

### TCS34725 RGB Color Sensor

**Pinout:**
```
TCS34725 Module
┌───────────────┐
│   TCS34725    │
│               │
│  ○ VIN        │ ← 3.3V Power
│  ○ GND        │ ← Ground
│  ○ SCL        │ ← I2C Clock (GPIO 22)
│  ○ SDA        │ ← I2C Data (GPIO 21)
│  ○ INT        │ ← Interrupt (optional, not used)
│  ○ LED        │ ← White LED control (optional)
│               │
└───────────────┘
```

**Specifications:**
- Operating Voltage: 3.3V (do NOT use 5V!)
- Current Draw: ~200μA active, ~2.5μA sleep
- I2C Address: 0x29
- Detection Range: 2-10cm
- Light Sensitivity: 3,800,000:1 dynamic range

---

### DFPlayer Mini MP3 Module

**Pinout:**
```
DFPlayer Mini
┌──────────────────┐
│                  │
│  VCC  ○      ○ SPK_1  │ ← Speaker +
│  RX   ○      ○ GND    │
│  TX   ○      ○ SPK_2  │ ← Speaker -
│  DAC_R○      ○ IO_1   │
│  DAC_L○      ○ GND    │
│  IO_2 ○      ○ ADKEY_2│
│  GND  ○      ○ ADKEY_1│
│  USB+ ○      ○ BUSY   │
│  USB- ○      ○ GND    │
│                  │
└──────────────────┘
```

**Specifications:**
- Operating Voltage: 3.2V - 5V (5V recommended)
- Current Draw: 20-30mA idle, up to 200mA during playback
- Audio Output: 3W max (with proper power supply)
- Supported Formats: MP3, WAV
- SD Card: FAT16/FAT32, up to 32GB

---

### Speaker

**Specifications:**
- Impedance: 8Ω (recommended)
- Power: 3-5W
- Type: Full-range driver
- Frequency Range: 100Hz - 18kHz (for voice clarity)

---

## Sender Unit Circuit

### Complete Wiring Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SENDER UNIT                              │
└─────────────────────────────────────────────────────────────┘

                    ESP32                    TCS34725
                ┌──────────┐              ┌──────────┐
                │          │              │          │
    USB ───────>│  USB     │              │  Sensor  │
                │          │              │  Module  │
                │  3.3V    ├──────────────┤ VIN      │
                │          │   (RED)      │          │
                │  GND     ├──────────────┤ GND      │
                │          │  (BLACK)     │          │
                │  GPIO 22 ├──────────────┤ SCL      │
                │  (SCL)   │  (YELLOW)    │          │
                │  GPIO 21 ├──────────────┤ SDA      │
                │  (SDA)   │   (BLUE)     │          │
                │          │              │          │
                │  GPIO 2  ├─────[220Ω]───┤►├ LED    │
                │  (LED)   │              │  (Status)│
                └──────────┘              └──────────┘

                                          Optional:
                                    ┌──────────────────┐
                                    │   Power Bank     │
                                    │   (5000mAh)      │
                                    │                  │
                                    │   USB Out ───────┘
                                    └──────────────────┘
```

---

### Detailed Connection Table

| Component | Pin | Wire Color | ESP32 Pin | Notes |
|-----------|-----|------------|-----------|-------|
| TCS34725 | VIN | Red | 3.3V | MUST be 3.3V, NOT 5V! |
| TCS34725 | GND | Black | GND | Common ground |
| TCS34725 | SCL | Yellow | GPIO 22 | I2C Clock line |
| TCS34725 | SDA | Blue | GPIO 21 | I2C Data line |
| LED (Status) | Anode | - | GPIO 2 | Built-in or external |
| LED (Status) | Cathode | - | GND | Via 220Ω resistor |

---

### I2C Pull-up Resistors

Most TCS34725 modules include built-in pull-up resistors. If using bare sensor:

```
      3.3V
        │
        ├─────[4.7kΩ]──── GPIO 22 (SCL)
        │
        └─────[4.7kΩ]──── GPIO 21 (SDA)
```

---

### Power Distribution

```
USB (5V) ─────> ESP32 Voltage Regulator ─────> 3.3V Rail
                                                   │
                                                   ├─> TCS34725 VIN
                                                   ├─> LED (via resistor)
                                                   └─> I2C Pull-ups
```

**Current Budget:**
- ESP32: ~80mA (WiFi active)
- TCS34725: ~0.2mA
- LED: ~20mA
- **Total: ~100mA**

Standard USB port (500mA) is sufficient.

---

## Receiver Unit Circuit

### Complete Wiring Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    RECEIVER UNIT                             │
└─────────────────────────────────────────────────────────────┘

        ESP32               DFPlayer Mini           Speaker
    ┌──────────┐          ┌──────────────┐       ┌─────────┐
    │          │          │              │       │         │
    │  5V(VIN) ├──────────┤ VCC          │       │  8Ω     │
    │          │  (RED)   │              │       │  3-5W   │
    │  GND     ├──────────┤ GND          │       │         │
    │          │ (BLACK)  │              │       │         │
    │  GPIO 17 ├──────────┤ RX           │       │         │
    │  (TX)    │ (YELLOW) │              │       │         │
    │  GPIO 16 ├──────────┤ TX        SPK_1 ├────┤ +       │
    │  (RX)    │  (BLUE)  │              │       │         │
    │          │          │           SPK_2 ├────┤ -       │
    │  GPIO 2  ├──[220Ω]──┤►├ LED     │       └─────────┘
    │          │          │              │
    └──────────┘          │   [SD Card]  │
         │                │   Slot       │
         │                └──────────────┘
         │
    ┌────┴─────┐
    │   USB    │
    │   Power  │
    └──────────┘
```

---

### Detailed Connection Table

| Component | Pin | Wire Color | ESP32 Pin | Notes |
|-----------|-----|------------|-----------|-------|
| DFPlayer | VCC | Red | 5V (VIN) | Use 5V for better audio output |
| DFPlayer | GND | Black | GND | Common ground |
| DFPlayer | RX | Yellow | GPIO 17 | ESP32 TX → DFPlayer RX |
| DFPlayer | TX | Blue | GPIO 16 | ESP32 RX ← DFPlayer TX |
| DFPlayer | SPK_1 | - | - | To Speaker + |
| DFPlayer | SPK_2 | - | - | To Speaker - |
| LED | Anode | - | GPIO 2 | Via 220Ω resistor |
| LED | Cathode | - | GND | Status indicator |

---

### UART Connection Detail

**CRITICAL: TX/RX Crossover**

```
ESP32           DFPlayer
  │                │
  TX (GPIO 17) ───>│ RX
  │                │
  RX (GPIO 16) <───│ TX
  │                │
```

**Common Mistake:** Connecting TX to TX and RX to RX will NOT work!

---

### DFPlayer Power Considerations

**Option 1: Direct 5V (Recommended)**
```
ESP32 5V Pin ──────> DFPlayer VCC
```
- Pros: Loudest audio, best performance
- Cons: Higher current draw (~200mA peak)
- Use when: Powered by good USB supply or power bank

**Option 2: 3.3V (Low Power)**
```
ESP32 3.3V Pin ──────> DFPlayer VCC
```
- Pros: Lower power consumption
- Cons: Quieter audio
- Use when: Battery constrained

---

### Speaker Connection

```
DFPlayer Mini
┌──────────────┐
│   SPK_1  ────┼───────> Speaker + (Red)
│              │
│   SPK_2  ────┼───────> Speaker - (Black)
│              │
└──────────────┘

Optional: 100μF capacitor across speaker for filtering
```

---

### SD Card Preparation

**Physical Installation:**
```
DFPlayer Mini
┌──────────────────┐
│                  │
│   ┌───────────┐  │
│   │ microSD   │  │ ← Insert with contacts facing down
│   │ Card Slot │  │
│   └───────────┘  │
│                  │
└──────────────────┘
```

**File Structure:**
```
SD Card (FAT32)
├── 0001.mp3  (Red)
├── 0002.mp3  (Green)
├── 0003.mp3  (Blue)
├── 0004.mp3  (Yellow)
├── 0005.mp3  (Cyan)
├── 0006.mp3  (Magenta)
├── 0007.mp3  (Orange)
├── 0008.mp3  (Purple)
├── 0009.mp3  (White)
└── 0010.mp3  (Black)
```

---

## Power Requirements

### Sender Unit

| Component | Voltage | Current (Typical) | Current (Peak) |
|-----------|---------|-------------------|----------------|
| ESP32 (WiFi) | 3.3V | 80mA | 170mA |
| TCS34725 | 3.3V | 0.2mA | 0.2mA |
| LED | 3.3V | 20mA | 20mA |
| **Total** | - | **~100mA** | **~190mA** |

**Recommended Power Source:**
- USB port (5V, 500mA) ✓
- Power bank (5V, 1A+) ✓
- Battery (3.7V LiPo + regulator) ✓

**Battery Life Estimate:**
- 1000mAh battery: ~10 hours
- 5000mAh power bank: ~50 hours

---

### Receiver Unit

| Component | Voltage | Current (Typical) | Current (Peak) |
|-----------|---------|-------------------|----------------|
| ESP32 (WiFi) | 3.3V | 80mA | 170mA |
| DFPlayer (idle) | 5V | 20mA | 20mA |
| DFPlayer (playing) | 5V | 100mA | 200mA |
| Speaker | 5V | - | 600mA |
| LED | 3.3V | 20mA | 20mA |
| **Total** | - | **~220mA** | **~1000mA** |

**Recommended Power Source:**
- USB port (5V, 500mA) - marginal ⚠️
- Wall adapter (5V, 2A) ✓
- Power bank (5V, 2A+) ✓

**Battery Life Estimate:**
- 1000mAh battery: ~4 hours
- 5000mAh power bank: ~20 hours (with audio)

---

## PCB Design Guidelines

### Single-Layer PCB Layout

**Dimensions:** 60mm × 40mm (fits standard project box)

```
┌────────────────────────────────────────┐
│  Sender PCB Layout                     │
│                                        │
│   [TCS34725]         [ESP32]          │
│      │                  │              │
│      └──────I2C─────────┘              │
│                                        │
│   [Power]  [LED]  [Headers]           │
│      │       │        │                │
│      └───────┴────────┘                │
└────────────────────────────────────────┘

Key Considerations:
1. Keep I2C traces short (<10cm)
2. Use ground plane on bottom layer
3. Place bypass capacitors near ICs
4. Separate power and signal traces
```

---

### Component Placement

**Sender Unit:**
1. ESP32 module: Center of board
2. TCS34725 sensor: Near board edge for easy access to colors
3. Power connector: Opposite side
4. LED: Near edge for visibility

**Receiver Unit:**
1. ESP32 module: Center
2. DFPlayer: Adjacent to ESP32
3. Speaker connector: Board edge
4. SD card slot: Accessible from case exterior

---

### Trace Width Guidelines

| Signal Type | Min Width | Recommended |
|-------------|-----------|-------------|
| Power (5V) | 0.5mm | 1.0mm |
| Power (3.3V) | 0.4mm | 0.8mm |
| GPIO signals | 0.25mm | 0.4mm |
| I2C (SCL/SDA) | 0.3mm | 0.5mm |
| UART (TX/RX) | 0.3mm | 0.5mm |
| Ground | - | Pour/plane |

---

## Testing Points

### Sender Unit Test Points

```
Test Point Locations:

TP1: 3.3V ───────────────── Voltage check
TP2: GND ────────────────── Ground reference
TP3: GPIO 22 (SCL) ──────── I2C clock signal
TP4: GPIO 21 (SDA) ──────── I2C data signal
TP5: TCS34725 VIN ───────── Sensor power
TP6: ESP32 EN ───────────── Enable/reset
```

---

### Receiver Unit Test Points

```
Test Point Locations:

TP1: 5V ─────────────────── Main power
TP2: 3.3V ───────────────── Logic power
TP3: GND ────────────────── Ground reference
TP4: GPIO 17 (TX) ───────── UART transmit
TP5: GPIO 16 (RX) ───────── UART receive
TP6: DFPlayer VCC ───────── Module power
TP7: SPK_1 ──────────────── Audio output +
TP8: SPK_2 ──────────────── Audio output -
```

---

### Testing Procedure

**1. Power Test:**
```
Multimeter: DC Voltage Mode
- TP1 (5V) to TP2 (GND) → Should read ~5.0V
- TP1 (3.3V) to TP2 (GND) → Should read ~3.3V
```

**2. I2C Communication Test:**
```
Logic Analyzer / Oscilloscope:
- TP3 (SCL) → Should show clock pulses (100kHz or 400kHz)
- TP4 (SDA) → Should show data transitions
```

**3. UART Communication Test:**
```
Logic Analyzer:
- TP4 (TX) → Should show data at 9600 baud
- TP5 (RX) → Should receive DFPlayer responses
```

**4. Audio Output Test:**
```
Multimeter: AC Voltage Mode
- TP7 to TP8 → Should read 1-3V AC during playback
```

---

### Troubleshooting with Test Points

| Issue | Test Point | Expected | Action if Wrong |
|-------|------------|----------|-----------------|
| No power | TP1, TP2 | 5V, 3.3V | Check USB connection |
| Sensor not detected | TP3, TP4 | Clock/data activity | Check I2C wiring |
| No audio | TP7, TP8 | AC voltage | Check DFPlayer, SD card |
| ESP32 won't boot | TP6 | 3.3V | Check EN pin connection |

---

End of Circuit Diagrams Documentation.
