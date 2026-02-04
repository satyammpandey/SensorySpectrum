# 🔧 Sensory Spectrum – Setup Guide

Step-by-step hardware assembly and software setup for the Sensory Spectrum project.

---

## 1. Before You Start

### 1.1. Required Hardware

**Sender unit:**

- ESP32 development board (Wi‑Fi enabled)
- TCS34725 RGB color sensor (I2C)
- Jumper wires (male–female)
- Micro USB cable
- Optional: Power bank for portable power

**Receiver unit:**

- ESP32 development board
- DFPlayer Mini MP3 module
- Micro SD card (≤ 32 GB, FAT32)
- 3–5 W, 8 Ω speaker
- Jumper wires (male–female)
- Micro USB cable
- Optional: Power bank

### 1.2. Required Software

- Python 3.7+
- MicroPython firmware for ESP32
- `esptool` (flash firmware)
- `ampy` or Thonny (upload files)
- Serial terminal (Thonny, PuTTY, screen, etc.)
- Text editor (VS Code recommended)

---

## 2. Hardware Assembly

### 2.1. Sender Unit (ESP32 + TCS34725)

**TCS34725 pins:**

- VIN – power (3.3 V)
- GND – ground
- SCL – I2C clock
- SDA – I2C data

**Connections:**

| ESP32 pin | TCS34725 pin |
|-----------|--------------|
| 3.3V      | VIN          |
| GND       | GND          |
| GPIO 22   | SCL          |
| GPIO 21   | SDA          |

**Notes:**

- Use only 3.3 V for the sensor.
- Keep I2C wires short for stability.
- On most ESP32 boards, GPIO 2 has a built‑in LED used for status.

---

### 2.2. Receiver Unit (ESP32 + DFPlayer Mini + Speaker)

**DFPlayer Mini pins (simplified):**

- VCC – power (3.3–5 V, 5 V recommended)
- GND – ground
- RX – UART data in
- TX – UART data out
- SPK_1 / SPK_2 – speaker outputs

**Connections:**

| ESP32 pin | DFPlayer pin |
|-----------|--------------|
| 5V (VIN)  | VCC          |
| GND       | GND          |
| GPIO 17   | RX           |
| GPIO 16   | TX           |

**Speaker connections:**

- DFPlayer `SPK_1` → Speaker +
- DFPlayer `SPK_2` → Speaker −

**Notes:**

- Double‑check TX/RX crossover (ESP32 TX → DFPlayer RX, ESP32 RX → DFPlayer TX).
- Use a proper power source; DFPlayer + speaker can cause brownouts on weak USB ports.

---

## 3. Flashing MicroPython to ESP32

Do this once for each ESP32 (sender and receiver).

### 3.1. Install tools

```bash
pip install esptool adafruit-ampy
```

### 3.2. Erase flash

Replace port with your actual port (`/dev/ttyUSB0`, `COM3`, etc.).

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

### 3.3. Flash MicroPython firmware

Download a recent ESP32 firmware `.bin` file from the MicroPython site, then:

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 \
  write_flash -z 0x1000 esp32-firmware.bin
```

After flashing, connect with a serial terminal at 115200 baud and confirm you get a `>>>` MicroPython prompt.

---

## 4. Project Files Layout

Recommended folder layout on your PC:

```text
SensorySpectrum/
├── sender/
│   ├── boot.py
│   ├── config.json
│   ├── sender.py
│   └── tcs34725.py
├── receiver/
│   ├── boot.py
│   ├── config.json
│   └── receiver.py
├── audio_files/
├── readme.md
└── SETUP_GUIDE.md
```

Each ESP32 will get the files from its own folder.

---

## 5. Configuration Files

### 5.1. Sender `config.json`

```json
{
  "wifi": {
    "ssid": "Your_WiFi_Name",
    "password": "Your_WiFi_Password"
  },
  "network": {
    "receiver_ip": "192.168.1.100",
    "udp_port": 4210
  },
  "sensor": {
    "sample_delay": 1.0,
    "min_intensity": 200,
    "confidence_threshold": 0.6
  }
}
```

- `ssid` / `password`: your 2.4 GHz Wi‑Fi network.
- `receiver_ip`: IP address of the receiver ESP32 (you will fill this after you boot the receiver once).
- `udp_port`: any free UDP port, same on both sides.

### 5.2. Receiver `config.json`

```json
{
  "wifi": {
    "ssid": "Your_WiFi_Name",
    "password": "Your_WiFi_Password"
  },
  "network": {
    "udp_port": 4210
  },
  "dfplayer": {
    "tx_pin": 17,
    "rx_pin": 16,
    "volume": 20
  },
  "audio": {
    "track_map": {
      "Red": 1,
      "Green": 2,
      "Blue": 3,
      "Yellow": 4,
      "Cyan": 5,
      "Magenta": 6,
      "Orange": 7,
      "Purple": 8,
      "White": 9,
      "Black": 10
    }
  }
}
```

- `volume`: 0–30, adjust for your speaker.
- `track_map`: maps color names to MP3 track numbers.

---

## 6. Preparing Audio Files (DFPlayer)

1. Format the micro SD card as **FAT32**.
2. Generate or record audio for each color (e.g., "Red", "Green", ...).
3. Name files exactly as:

```text
0001.mp3  → Red
0002.mp3  → Green
0003.mp3  → Blue
0004.mp3  → Yellow
0005.mp3  → Cyan
0006.mp3  → Magenta
0007.mp3  → Orange
0008.mp3  → Purple
0009.mp3  → White
0010.mp3  → Black
```

4. Copy all MP3 files to the root of the SD card.
5. Insert the SD card into the DFPlayer Mini.

---

## 7. Uploading Code to ESP32

You can use `ampy` or Thonny; below is with `ampy`.

### 7.1. Sender ESP32

Set an environment variable for convenience:

```bash
export PORT=/dev/ttyUSB0   # or COM3 on Windows
```

Upload files:

```bash
ampy --port $PORT put sender/boot.py
ampy --port $PORT put sender/config.json
ampy --port $PORT put sender/tcs34725.py
ampy --port $PORT put sender/sender.py main.py
```

### 7.2. Receiver ESP32

```bash
export PORT=/dev/ttyUSB1   # or your receiver port
```

Upload files:

```bash
ampy --port $PORT put receiver/boot.py
ampy --port $PORT put receiver/config.json
ampy --port $PORT put receiver/receiver.py main.py
```

---

## 8. First Boot Sequence

### 8.1. Boot the Receiver First

1. Connect the receiver ESP32 via USB.
2. Open a serial monitor at 115200 baud.
3. Press the reset button.

You should see something like:

```text
SENSORY SPECTRUM - Receiver Unit
Connecting to WiFi...
WiFi connected, IP: 192.168.1.100
Listening on UDP port 4210
DFPlayer initialized, volume set.
```

4. Note the **IP address** (e.g., `192.168.1.100`).

5. Put this IP into the sender's `config.json` as `receiver_ip`, re‑upload `config.json` to the sender.

---

### 8.2. Boot the Sender

1. Connect the sender ESP32 via USB.
2. Open a serial monitor at 115200 baud.
3. Press reset.

Expected output:

```text
SENSORY SPECTRUM - Sender Unit
Connecting to WiFi...
WiFi connected, IP: 192.168.1.x
=== CALIBRATION MODE ===
Point sensor at WHITE surface...
Sampling...
Calibration complete
Starting color detection loop...
```

During calibration:

- Point the sensor at a **white** surface (paper, wall) at normal lighting.
- Hold still until calibration finishes.

---

## 9. Testing & Verification

### 9.1. Basic Connectivity

- Make sure both ESP32 boards show "WiFi connected".
- Ensure both are on the same Wi‑Fi network.
- Confirm no "Wi‑Fi connect failed" messages.

### 9.2. Color Detection Test

1. After calibration, point the sensor at a **red** object.
2. In the sender serial output you should see lines like:

```text
Raw: R=1234 G=200 B=150 | Red (92.0%)
✓ Sent: Red (ACK received)
```

3. On the receiver serial:

```text
Received from 192.168.1.x: Red (92.0%)
Playing track 1: Red
```

4. The speaker should play the "Red" audio file.

Repeat with other colors (Green, Blue, etc.).

---

## 10. Quick Troubleshooting Checklist

- No Wi‑Fi:
  - Check SSID/password.
  - Ensure 2.4 GHz network.
  - Move closer to router.

- Sensor values all zero:
  - Check 3.3 V and GND wiring.
  - Swap SDA/SCL if miswired.

- No sound:
  - Check DFPlayer VCC (5 V) and GND.
  - Confirm SD card format and filenames.
  - Verify TX/RX orientation.
  - Increase volume in `config.json`.

For deeper debugging, see `TROUBLESHOOTING.md`.

---

Setup is complete. Your Sensory Spectrum system is ready to use.
