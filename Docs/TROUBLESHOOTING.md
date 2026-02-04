# 🔧 Troubleshooting Guide - Sensory Spectrum

Comprehensive problem-solving guide for hardware, software, and network issues.

---

## Table of Contents

1. [Quick Diagnostic Flowchart](#quick-diagnostic-flowchart)
2. [Power & Connectivity Issues](#power--connectivity-issues)
3. [Sensor Problems](#sensor-problems)
4. [Audio Issues](#audio-issues)
5. [Network & Communication](#network--communication)
6. [Software & Configuration](#software--configuration)
7. [Hardware Diagnostics](#hardware-diagnostics)
8. [Error Messages](#error-messages)
9. [Advanced Debugging](#advanced-debugging)

---

## Quick Diagnostic Flowchart

```
                    [System Not Working]
                            │
                            ↓
                    [Is LED blinking?]
                    ╱              ╲
                 NO                 YES
                 ↓                   ↓
        [Power Issue]      [LED blinks but no function]
                                     │
                            ┌────────┴────────┐
                            ↓                 ↓
                    [WiFi Problem]    [Sensor/Audio Problem]
```

---

## Power & Connectivity Issues

### Problem: ESP32 Won't Power On

**Symptoms:**
- No LED activity
- Computer doesn't recognize USB device
- No serial output

**Possible Causes & Solutions:**

**1. USB Cable Issue**
```
Test: Try different USB cable (data capable, not charge-only)
Check: Some cables are power-only and won't transfer data
Solution: Use known-good data cable (included with phones/tablets)
```

**2. USB Port Problem**
```
Test: Try different USB port or computer
Check: USB 3.0 ports sometimes have compatibility issues
Solution: Use USB 2.0 port or powered USB hub
```

**3. ESP32 Board Damaged**
```
Test: Check for:
  - Burnt components (brown/black spots)
  - Bent pins
  - Loose USB connector
Solution: If damaged, replace ESP32 board
```

**4. Voltage Regulator Issue**
```
Test: Measure voltage between 3.3V and GND pins
Expected: 3.3V (±0.1V)
If low: Board's regulator may be faulty, replace board
```

**Diagnostic Steps:**
```
1. Connect USB cable
2. Press EN (Enable) button on ESP32
3. Check if any LED lights up (even briefly)
4. Open Device Manager (Windows) or lsusb (Linux)
5. Look for "CP210x" or "CH340" device

If device appears: Cable/port OK, check software
If device missing: Cable/port/board issue
```

---

### Problem: ESP32 Boots But Resets Constantly

**Symptoms:**
- LED flashes rapidly
- Serial monitor shows repeated boot messages
- Device seems to restart every few seconds

**Possible Causes:**

**1. Power Supply Insufficient**
```
Cause: USB port can't provide enough current (especially during WiFi)
Symptoms: Reboots when WiFi initializes
Solution: 
  - Use powered USB hub
  - Connect to wall adapter (5V, 1A+)
  - Try power bank (2A output)
```

**2. GPIO Conflict**
```
Cause: GPIO 0 or GPIO 2 shorted to ground
Symptoms: Boot loops, won't enter normal mode
Solution:
  - Check wiring to GPIO 0 and GPIO 2
  - Remove all connections except USB
  - If boots normally, reconnect one by one
```

**3. Code Exception**
```
Cause: Software error causing crash
Symptoms: Specific error message before reset
Solution:
  - Read serial output for error details
  - Check code for infinite loops or memory issues
  - Flash known-good firmware to test
```

**Diagnostic Commands:**
```python
# Add to boot.py to catch exceptions
import sys
sys.print_exception = lambda e: print("Exception:", e)

# Monitor brownout detector
import esp32
print("Brownout reset:", esp32.wake_reason())
```

---

### Problem: WiFi Won't Connect

**Symptoms:**
- "Connecting to WiFi..." message appears
- Never shows "WiFi connected"
- Eventually times out

**Possible Causes & Solutions:**

**1. Wrong SSID/Password**
```
Check: config.json has correct credentials
Test: Temporarily use phone hotspot (simple password)
Solution: Fix SSID/password in config.json, re-upload
```

**2. 5GHz Network**
```
Cause: ESP32 only supports 2.4GHz WiFi
Symptoms: Can't find network
Solution: 
  - Use 2.4GHz network
  - Create separate 2.4GHz SSID on dual-band router
  - Check router settings for 2.4GHz enabled
```

**3. Special Characters in Password**
```
Cause: Some special chars cause issues
Problematic: Quotes (", '), backslash (\)
Solution: 
  - Temporarily change WiFi password to alphanumeric
  - Or escape special characters in JSON
```

**4. Router Settings**
```
Check router:
  - MAC address filtering disabled (or add ESP32 MAC)
  - SSID broadcast enabled
  - WPA2 encryption (not WPA3 only)
  - Channel 1-11 (ESP32 doesn't support 12-14)

Find ESP32 MAC: Run this code:
import network
wlan = network.WLAN(network.STA_IF)
print("MAC:", wlan.config('mac'))
```

**5. Distance from Router**
```
Cause: Weak signal
Test: Move closer to router
Solution:
  - Position ESP32 within 10m of router
  - Remove obstacles (metal, concrete)
  - Check antenna orientation
```

**6. Network Overload**
```
Cause: Too many devices on network
Symptoms: Connects sometimes, not others
Solution:
  - Disconnect other devices temporarily
  - Assign static IP to ESP32
  - Reduce network traffic
```

**Debug WiFi Connection:**
```python
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Scan for networks
networks = wlan.scan()
print("Available networks:")
for net in networks:
    print("  SSID:", net[0].decode(), "Channel:", net[2], "Signal:", net[3])

# Try to connect with detailed output
print("Connecting to:", SSID)
wlan.connect(SSID, PASSWORD)

for i in range(20):
    if wlan.isconnected():
        print("Connected! IP:", wlan.ifconfig()[0])
        break
    print(f"Attempt {i+1}/20... Status:", wlan.status())
    time.sleep(1)
else:
    print("Failed. Status codes:")
    print("  0: STAT_IDLE")
    print("  1: STAT_CONNECTING")
    print("  3: STAT_GOT_IP (success)")
    print("  -1: STAT_WRONG_PASSWORD")
    print("  -2: STAT_NO_AP_FOUND")
    print("Current status:", wlan.status())
```

---

## Sensor Problems

### Problem: Sensor Not Detected (I2C Error)

**Symptoms:**
- "I2C device not found" error
- "OSError: [Errno 19] ENODEV"
- Sensor values all zero

**Possible Causes:**

**1. Wiring Issues**
```
Check connections:
  ESP32 Pin     →  TCS34725 Pin
  ────────────────────────────
  3.3V          →  VIN (NOT 5V!)
  GND           →  GND
  GPIO 22 (SCL) →  SCL
  GPIO 21 (SDA) →  SDA

Common mistakes:
  ✗ Using 5V instead of 3.3V (damages sensor)
  ✗ Swapped SCL and SDA
  ✗ Loose connection (try reseating wires)
  ✗ Broken jumper wire (test continuity)
```

**2. Wrong I2C Pins**
```
Check code uses correct pins:
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

If using different pins, update both code and wiring
```

**3. I2C Address Wrong**
```
Test: Scan for I2C devices
from machine import I2C, Pin
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
devices = i2c.scan()
print("I2C devices found:", [hex(d) for d in devices])

Expected: [0x29] (TCS34725 default address)
If empty: Wiring issue
If different address: Update code to match
```

**4. Pull-up Resistors Missing**
```
Most TCS34725 modules have built-in pull-ups
If using bare sensor chip:
  - Add 4.7kΩ resistors from SCL to 3.3V
  - Add 4.7kΩ resistors from SDA to 3.3V
```

**5. Sensor Damaged**
```
Test with multimeter:
  - VIN to GND: Should read 3.3V
  - Check for short circuits

If voltages wrong: Sensor may be damaged, replace
```

**Diagnostic I2C Test:**
```python
from machine import I2C, Pin

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

print("I2C Scan:")
devices = i2c.scan()

if len(devices) == 0:
    print("✗ No I2C devices found!")
    print("  Check: Wiring, power (3.3V), connections")
elif 0x29 in devices:
    print("✓ TCS34725 found at address 0x29")
else:
    print("✗ Device found but not TCS34725:")
    print("  Found addresses:", [hex(d) for d in devices])
```

---

### Problem: Sensor Gives All Zeros or Strange Values

**Symptoms:**
- Raw readings: R=0, G=0, B=0, C=0
- Or extremely high values (65535)
- Inconsistent readings

**Possible Causes:**

**1. Sensor Not Enabled**
```
Solution: Ensure initialization code runs:
sensor = tcs34725.TCS34725(i2c)
sensor.enable(True)  # Must call this!
time.sleep(0.1)  # Wait for sensor to stabilize
```

**2. Integration Time Too Short/Long**
```
If all zeros:
  - Integration time too short
  - Not enough light
Solution:
  sensor.integration_time(tcs34725._INTEGRATION_TIME_50MS)

If all 65535 (maxed out):
  - Integration time too long
  - Too much light
Solution:
  sensor.integration_time(tcs34725._INTEGRATION_TIME_2_4MS)
```

**3. Gain Setting Wrong**
```
For normal lighting:
  sensor.gain(tcs34725._GAIN_4X)  # Default

For low light:
  sensor.gain(tcs34725._GAIN_16X or _GAIN_60X)

For bright light:
  sensor.gain(tcs34725._GAIN_1X)
```

**4. Sensor Obstructed**
```
Check: Nothing blocking sensor window
Remove: Protective film/sticker if present
Position: Sensor facing the object (2-10cm away)
```

**5. Sensor Chip Damaged**
```
If consistently zeros despite correct setup:
  - Sensor may be burnt (if 5V was applied)
  - Test with different TCS34725 module
```

---

### Problem: Colors Detected Incorrectly

**Symptoms:**
- Red detected as Orange
- Green detected as Yellow
- All colors seem shifted

**Solutions:**

**1. Calibration Needed**
```
Perform calibration:
  1. Point sensor at white paper
  2. Ensure even lighting
  3. Run calibration routine
  4. System adjusts R/G/B factors

Recalibrate when:
  - Lighting conditions change
  - Moving between rooms
  - Using different light sources
```

**2. Lighting Issues**
```
Optimal lighting:
  ✓ Natural daylight (indirect)
  ✓ White LED (5000-6500K)
  ✗ Incandescent (too yellow)
  ✗ Colored lights
  ✗ Direct sunlight (too bright)
  ✗ Shadows or uneven light

Solution: Improve lighting or recalibrate
```

**3. Distance from Object**
```
Optimal range: 5-7cm
Too close (<2cm): Readings may saturate
Too far (>10cm): Weak signal, noise increases

Solution: Maintain 5-7cm distance
```

**4. Reflective Surfaces**
```
Problem: Chrome, mirrors, glossy surfaces
Cause: Specular reflection instead of diffuse
Solution: Angle sensor slightly (not perpendicular)
```

**5. Threshold Values Wrong**
```
Check config.json:
{
  "sensor": {
    "min_intensity": 200,          ← Too high misses dark colors
    "confidence_threshold": 0.6    ← Too high rejects good readings
  }
}

Adjust:
  - Lower min_intensity for dark colors
  - Lower confidence_threshold for more detections
```

---

## Audio Issues

### Problem: No Sound from Speaker

**Symptoms:**
- Receiver receives color data (LED blinks)
- No audio output
- Silent operation

**Possible Causes:**

**1. DFPlayer Not Powered**
```
Check:
  - VCC connected to 5V (or 3.3V)
  - GND connected
Measure: Voltage between VCC and GND should be 5V

Solution: Fix power connections
```

**2. Speaker Connection Wrong**
```
Check:
  DFPlayer SPK_1 → Speaker +
  DFPlayer SPK_2 → Speaker -

Test: Swap polarity if unsure (won't damage, just wrong phase)
```

**3. SD Card Issue**
```
Common problems:
  ✗ SD card not inserted
  ✗ SD card not formatted as FAT32
  ✗ Files not named correctly (0001.mp3, 0002.mp3...)
  ✗ Files in wrong folder (must be in root)

Solution:
  1. Format SD card as FAT32
  2. Copy MP3 files with correct names
  3. Files must be in root directory (not in folders)
  4. Safely eject, reinsert into DFPlayer
```

**4. UART Connection Wrong**
```
CRITICAL: TX/RX crossover!

Correct:
  ESP32 TX (GPIO 17) → DFPlayer RX
  ESP32 RX (GPIO 16) → DFPlayer TX

Common mistake: Connecting TX to TX
Solution: Swap TX and RX wires
```

**5. Volume Too Low**
```
Check: Volume setting in config.json
{
  "dfplayer": {
    "volume": 20  ← Range 0-30
  }
}

Solution: Increase volume to 25-30 and re-upload config
```

**6. MP3 Files Corrupt**
```
Test: Play MP3 files on computer
Check: Files play correctly before copying to SD

Solution: Re-encode MP3 files:
  - Bitrate: 128kbps or higher
  - Sample rate: 44100Hz
  - Format: Standard MP3 (no VBR)
```

**Diagnostic Test:**
```python
from machine import UART, Pin
import time

# Initialize UART
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))

def dfplayer_send(cmd, param1, param2):
    # DFPlayer command packet
    buf = bytearray(10)
    buf[0] = 0x7E  # Start
    buf[1] = 0xFF  # Version
    buf[2] = 0x06  # Length
    buf[3] = cmd   # Command
    buf[4] = 0x00  # Feedback
    buf[5] = param1
    buf[6] = param2
    checksum = -(sum(buf[1:7]))
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF  # End
    uart.write(buf)

# Test sequence
print("Testing DFPlayer...")

# Set volume to 25
print("1. Setting volume to 25")
dfplayer_send(0x06, 0x00, 0x19)
time.sleep(0.2)

# Play track 1
print("2. Playing track 1")
dfplayer_send(0x03, 0x00, 0x01)
time.sleep(2)

print("Did you hear sound? If yes, DFPlayer works!")
```

---

### Problem: Audio Plays But Distorted/Crackling

**Symptoms:**
- Sound plays but poor quality
- Crackling or popping noises
- Volume fluctuates

**Possible Causes:**

**1. Insufficient Power**
```
Cause: DFPlayer + speaker draw too much current
Symptoms: Sound cuts out, distortion at high volume

Solution:
  - Use 5V 2A power supply (not 500mA USB port)
  - Add 100μF capacitor across DFPlayer VCC/GND
  - Use powered USB hub
```

**2. Speaker Impedance Wrong**
```
DFPlayer works best with: 8Ω speakers
Too low (<4Ω): May damage DFPlayer
Too high (>16Ω): Quiet volume

Solution: Use 8Ω, 3-5W speaker
```

**3. MP3 Files Poor Quality**
```
Symptoms: All tracks sound bad
Solution: Re-encode with higher bitrate
  - Minimum: 128kbps
  - Recommended: 192kbps or higher
```

**4. SD Card Slow/Corrupt**
```
Symptoms: Intermittent glitches
Solution:
  - Use Class 10 SD card
  - Reformat and recopy files
  - Test with different SD card
```

---

## Network & Communication

### Problem: Sender and Receiver Can't Communicate

**Symptoms:**
- Both devices connected to WiFi
- Sender shows "Sent: [color]" but no ACK
- Receiver never plays audio
- No error messages

**Diagnostic Steps:**

**1. Verify IP Addresses**
```
On receiver, check serial output:
"WiFi connected, IP: 192.168.1.100"  ← Note this IP

In sender config.json:
{
  "network": {
    "receiver_ip": "192.168.1.100"  ← Must match!
  }
}

If different: Update sender config, re-upload
```

**2. Check UDP Port**
```
Both must use same port:

Sender config.json:
"udp_port": 4210

Receiver config.json:
"udp_port": 4210

If different: Change to match, re-upload
```

**3. Firewall Blocking**
```
Test: Temporarily disable firewall
If works: Add exception for UDP port 4210

On router:
  - Port forwarding not needed (local network)
  - UPnP doesn't affect local UDP
  - Check AP isolation is OFF
```

**4. Different Subnets**
```
Check: Both devices have IPs in same range

Same subnet example:
  Sender:   192.168.1.50  ← Same 192.168.1.x
  Receiver: 192.168.1.100 ← Same 192.168.1.x

Different subnet example (won't work):
  Sender:   192.168.1.50  ← Different
  Receiver: 192.168.2.100 ← Different

Solution: Connect both to same WiFi network
```

**5. AP Isolation Enabled**
```
Some routers have "AP Isolation" or "Client Isolation"
Effect: Devices can't communicate with each other
Test: Connect both devices to same router, not guest network

Solution: Disable AP isolation in router settings
```

**Network Test Script:**
```python
import socket
import time

# On Sender: Send test packet
def test_send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_ip = "192.168.1.100"  # Update with receiver IP
    port = 4210

    for i in range(10):
        message = f"Test {i}".encode()
        sock.sendto(message, (receiver_ip, port))
        print(f"Sent test {i}")
        time.sleep(1)

# On Receiver: Listen for packets
def test_receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 4210))
    sock.settimeout(5.0)

    print("Listening for packets...")
    try:
        for i in range(10):
            data, addr = sock.recvfrom(512)
            print(f"Received from {addr}: {data.decode()}")
    except OSError:
        print("Timeout - no packets received")
```

---

### Problem: Connection Drops Intermittently

**Symptoms:**
- Works for a while, then stops
- WiFi reconnects frequently
- "WiFi connect failed" messages

**Solutions:**

**1. Router Distance**
```
Signal strength matters for stability
Test: Move devices closer to router
Check: No thick walls/metal obstacles between

Ideal: Within 10m line-of-sight to router
```

**2. WiFi Channel Congestion**
```
Solution: Change router to less crowded channel
Recommended 2.4GHz channels: 1, 6, or 11

Use WiFi analyzer app to find best channel
```

**3. Power Management**
```
ESP32 WiFi sleep mode may cause drops

Add to code:
import network
wlan = network.WLAN(network.STA_IF)
wlan.config(pm=wlan.PM_NONE)  # Disable power saving
```

**4. Network Instability**
```
Router issues:
  - Overheating (check router temperature)
  - Too many devices
  - Firmware outdated

Solution: Restart router, update firmware
```

---

## Software & Configuration

### Problem: Code Won't Upload to ESP32

**Symptoms:**
- "Failed to connect" error
- Upload times out
- Stuck at "Connecting..."

**Solutions:**

**1. Wrong Port Selected**
```
Windows: Should be COMx (e.g., COM3)
Linux: Should be /dev/ttyUSBx
Mac: Should be /dev/cu.usbserial-xxx

Check Device Manager (Windows) or ls /dev/tty* (Linux/Mac)
```

**2. ESP32 Not in Upload Mode**
```
Manual method:
  1. Hold BOOT button
  2. Press EN (reset) button
  3. Release EN
  4. Release BOOT after 1 second
  5. Try upload immediately

Some boards auto-reset, but manual method more reliable
```

**3. USB Driver Missing**
```
ESP32 uses: CP210x or CH340 chip

Windows: Install driver from manufacturer
Linux: Usually works out of box
Mac: May need driver installation

Test: Device appears in device list
```

**4. Wrong Baud Rate**
```
Try different upload speeds:
  - 115200 (standard)
  - 460800 (faster)
  - 921600 (fastest, may be unstable)

Use lower speed if upload fails
```

**5. Flash Size Mismatch**
```
Check board flash size (usually 4MB)
In esptool, specify: --flash_size=detect

If mismatch: Use correct flash size parameter
```

---

### Problem: Config File Not Loading

**Symptoms:**
- "Config not found" error
- Default values used
- JSON error messages

**Solutions:**

**1. File Not Uploaded**
```
Verify with ampy:
ampy --port /dev/ttyUSB0 ls

Should show:
  boot.py
  config.json
  main.py
  ...

If missing: Upload with ampy put config.json
```

**2. JSON Syntax Error**
```
Common mistakes:
  ✗ Missing comma
  ✗ Trailing comma
  ✗ Single quotes instead of double
  ✗ Unescaped backslash in password

Validate JSON: Use online JSON validator first
```

**3. Wrong File Name**
```
Must be exactly: config.json (lowercase)
Not: Config.json, config.JSON, config.txt

Check with: ampy ls
```

**Test Config Loading:**
```python
import json

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("✓ Config loaded successfully")
    print(json.dumps(config, indent=2))
except OSError:
    print("✗ File not found")
except ValueError as e:
    print("✗ JSON error:", e)
```

---

## Hardware Diagnostics

### Voltage Tests

**Essential Measurements:**
```
Test Point        Expected    What It Means
────────────────────────────────────────────
ESP32 3.3V → GND   3.3V ±0.1V  Regulator working
ESP32 5V → GND     5.0V ±0.2V  USB power OK
Sensor VIN → GND   3.3V        Sensor powered
DFPlayer VCC → GND 5.0V        DFPlayer powered

If wrong: Check connections, look for shorts
```

---

### Continuity Tests

**Check Wiring:**
```
Use multimeter in continuity mode (beep)

Test:
1. ESP32 GPIO 22 ↔ Sensor SCL (should beep)
2. ESP32 GPIO 21 ↔ Sensor SDA (should beep)
3. ESP32 GPIO 17 ↔ DFPlayer RX (should beep)
4. ESP32 GPIO 16 ↔ DFPlayer TX (should beep)
5. ESP32 GND ↔ Sensor GND ↔ DFPlayer GND (should beep)

No beep = broken connection
```

---

### Current Draw Test

**Normal Current:**
```
Component          Idle    Active
────────────────────────────────
ESP32 (WiFi on)    80mA    170mA
TCS34725           0.2mA   0.2mA
DFPlayer (no play) 20mA    20mA
DFPlayer (playing) 100mA   200mA
LED                20mA    20mA

Total Sender:      ~100mA  ~190mA
Total Receiver:    ~220mA  ~400mA

If much higher: Short circuit or damaged component
```

---

## Error Messages

### Common Error Messages & Fixes

**"OSError: [Errno 19] ENODEV"**
```
Meaning: I2C device not found
Fix: Check sensor wiring, I2C address, power
```

**"OSError: [Errno 116] ETIMEDOUT"**
```
Meaning: Network timeout
Fix: Check WiFi connection, IP address, firewall
```

**"MemoryError"**
```
Meaning: RAM exhausted
Fix: Reduce buffer sizes, avoid large data structures
```

**"OSError: [Errno 2] ENOENT"**
```
Meaning: File not found
Fix: Upload missing file (config.json, main.py)
```

**"ValueError: invalid syntax for integer"**
```
Meaning: JSON parsing error
Fix: Check config.json for syntax errors
```

**"WiFi connect failed"**
```
Meaning: Can't connect to network
Fix: Check SSID/password, 2.4GHz, signal strength
```

---

## Advanced Debugging

### Enable Debug Mode

**Add to boot.py:**
```python
import esp
esp.osdebug(None)  # Disable OS debug (cleaner output)

# Or enable for deep debugging:
# esp.osdebug(0)  # Enable all debug

# Set exception handling
import sys
sys.print_exception = lambda e: print(f"EXCEPTION: {e}")
```

---

### Serial Monitor Settings

**Correct Settings:**
```
Baud Rate: 115200
Data Bits: 8
Parity: None
Stop Bits: 1
Flow Control: None

Line Ending: CR+LF (for sending commands)
```

---

### Memory Debugging

**Check Free RAM:**
```python
import gc
gc.collect()
print(f"Free memory: {gc.mem_free()} bytes")
print(f"Used memory: {gc.mem_alloc()} bytes")

# If low (<10KB): Memory leak, reduce variables
```

---

### Reset to Factory State

**Complete Reset:**
```bash
# Erase entire flash
esptool.py --port /dev/ttyUSB0 erase_flash

# Re-flash MicroPython
esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-firmware.bin

# Re-upload all files
```

---

## Getting Help

**Before Asking for Help:**

1. ✓ Read this troubleshooting guide
2. ✓ Check error messages carefully
3. ✓ Test with known-good components
4. ✓ Try on different WiFi network
5. ✓ Verify all connections
6. ✓ Check power supply

**When Asking for Help, Provide:**

```
1. Hardware:
   - ESP32 board model
   - Sensor/DFPlayer module brand
   - Power supply details

2. Software:
   - MicroPython version
   - Complete error message
   - Serial monitor output (paste full log)

3. What You've Tried:
   - List troubleshooting steps taken
   - What changed before it stopped working

4. Code:
   - Share relevant code snippets
   - Include config.json (remove password)
```

---

## Contact & Support

**GitHub Issues:**
- [github.com/madhurtyagii/Sensory-Spectrum/issues]

**Documentation:**
- Setup Guide: SETUP_GUIDE.md
- API Reference: API_DOCUMENTATION.md
- Circuit Diagrams: circuit_diagram.md

---

End of Troubleshooting Guide.
