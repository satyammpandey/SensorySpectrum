# 📚 API Documentation - Sensory Spectrum

Complete code structure and function reference for the Sensory Spectrum project.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Sender Unit API](#sender-unit-api)
3. [Receiver Unit API](#receiver-unit-api)
4. [TCS34725 Driver API](#tcs34725-driver-api)
5. [Configuration Schema](#configuration-schema)
6. [Network Protocol](#network-protocol)

---

## Project Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Sensory Spectrum System                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐           WiFi/UDP          ┌──────────────┐
│  │   SENDER     │ ────────────────────────► │   RECEIVER   │
│  │              │                             │              │
│  │  ESP32       │   Color Data + Confidence  │  ESP32       │
│  │  TCS34725    │                             │  DFPlayer    │
│  │  Sensor      │ ◄──────────────────────── │  Speaker     │
│  └──────────────┘      ACK Response          └──────────────┘
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### File Structure

```
sender/
  ├── boot.py           - Boot initialization
  ├── sender.py         - Main sender logic
  ├── tcs34725.py       - Sensor driver
  └── config.json       - Configuration

receiver/
  ├── boot.py           - Boot initialization
  ├── receiver.py       - Main receiver logic
  └── config.json       - Configuration
```

---

## Sender Unit API

### Main Module: `sender.py`

#### Global Variables

```python
# LED pin for status indication
led = Pin(2, Pin.OUT)

# Calibration factors (R, G, B multipliers)
calibration_factors = (1.0, 1.0, 1.0)

# Configuration loaded from config.json
SSID = str
PASSWORD = str
RECEIVER_IP = str
UDP_PORT = int
SAMPLE_DELAY = float
MIN_INTENSITY = int
CONFIDENCE_THRESHOLD = float
```

---

### Functions

#### `blink_led(times=1, duration=0.1)`

Blink the status LED a specified number of times.

**Parameters:**
- `times` (int): Number of blinks (default: 1)
- `duration` (float): Duration of each blink in seconds (default: 0.1)

**Returns:** None

**Example:**
```python
blink_led(3, 0.2)  # Blink 3 times, 0.2s each
```

---

#### `load_config(filename='config.json')`

Load configuration from JSON file.

**Parameters:**
- `filename` (str): Path to config file (default: 'config.json')

**Returns:** 
- `dict`: Configuration dictionary
- `None`: If file not found or invalid JSON

**Example:**
```python
config = load_config()
if config:
    ssid = config["wifi"]["ssid"]
```

---

#### `wifi_connect(ssid, password, timeout=20)`

Connect to WiFi network with timeout.

**Parameters:**
- `ssid` (str): WiFi network name
- `password` (str): WiFi password
- `timeout` (int): Connection timeout in seconds (default: 20)

**Returns:**
- `WLAN`: WiFi object if connected
- `None`: If connection failed

**Example:**
```python
wlan = wifi_connect("MyWiFi", "password123")
if wlan:
    print(f"Connected: {wlan.ifconfig()[0]}")
```

---

#### `monitor_wifi(wlan)`

Check WiFi connection status and reconnect if dropped.

**Parameters:**
- `wlan` (WLAN): Existing WiFi connection object

**Returns:**
- `WLAN`: Reconnected WiFi object or original if still connected

**Example:**
```python
wlan = monitor_wifi(wlan)
```

---

#### `calibrate_sensor(samples=10)`

Calibrate color sensor against white surface.

**Parameters:**
- `samples` (int): Number of samples to average (default: 10)

**Returns:**
- `tuple`: (r_factor, g_factor, b_factor) calibration multipliers

**Side Effects:**
- Updates global `calibration_factors` variable
- Prints calibration progress

**Example:**
```python
factors = calibrate_sensor(10)
# factors = (1.2, 0.95, 1.1)
```

---

#### `detect_rgb_color_enhanced(r, g, b)`

Detect color from RGB values with enhanced algorithm.

**Parameters:**
- `r` (int): Red channel value (0-65535)
- `g` (int): Green channel value (0-65535)
- `b` (int): Blue channel value (0-65535)

**Returns:**
- `tuple`: (color_name, confidence)
  - `color_name` (str): "Red", "Green", "Blue", "Yellow", "Cyan", "Magenta", "Orange", "Purple", "White", "Black", or "Unknown"
  - `confidence` (float): Confidence score (0.0-1.0)

**Algorithm:**
1. Apply calibration factors
2. Normalize to 0-255 range
3. Calculate total intensity
4. Detect black/white based on total
5. Calculate RGB percentages
6. Match to color categories

**Example:**
```python
color, conf = detect_rgb_color_enhanced(1500, 800, 200)
# Returns: ("Red", 0.87)
```

**Color Detection Logic:**

| Color | Condition |
|-------|-----------|
| Black | total < MIN_TOTAL |
| White | total > MAX_TOTAL and RGB balanced |
| Red | r_pct > 0.5, others < 0.3 |
| Green | g_pct > 0.5, others < 0.3 |
| Blue | b_pct > 0.5, others < 0.3 |
| Yellow | r_pct > 0.35 and g_pct > 0.35 |
| Magenta | r_pct > 0.35 and b_pct > 0.35 |
| Cyan | g_pct > 0.35 and b_pct > 0.35 |
| Orange | r_pct > 0.45, g_pct 0.25-0.40 |
| Purple | b_pct > 0.35, r_pct > 0.30, g_pct < 0.25 |

---

#### `send_with_ack(sock, message, addr, port, timeout=0.5, retries=3)`

Send UDP message with acknowledgment retry logic.

**Parameters:**
- `sock` (socket): UDP socket object
- `message` (bytes): Message to send
- `addr` (str): Destination IP address
- `port` (int): Destination UDP port
- `timeout` (float): ACK wait timeout in seconds (default: 0.5)
- `retries` (int): Number of retry attempts (default: 3)

**Returns:**
- `bool`: True if ACK received, False otherwise

**Example:**
```python
msg = "Red:0.92".encode('utf-8')
success = send_with_ack(sock, msg, "192.168.1.100", 4210)
```

---

## Receiver Unit API

### Main Module: `receiver.py`

#### Global Variables

```python
# LED pin for status
led = Pin(2, Pin.OUT)

# Configuration
SSID = str
PASSWORD = str
UDP_PORT = int
DF_TX = int
DF_RX = int
VOLUME = int
COLOR_TO_TRACK = dict

# UART for DFPlayer
uart = UART(2, baudrate=9600, tx=DF_TX, rx=DF_RX)
```

---

### Functions

#### `blink_led(times=1, duration=0.1)`

Same as sender unit - blink status LED.

---

#### `load_config(filename='config.json')`

Same as sender unit - load configuration from JSON.

---

#### `wifi_connect(ssid, password, timeout=20)`

Same as sender unit - connect to WiFi.

---

#### `dfplayer_send(cmd, param1=0, param2=0)`

Send command to DFPlayer Mini using serial protocol.

**Parameters:**
- `cmd` (int): DFPlayer command byte
- `param1` (int): High byte parameter (default: 0)
- `param2` (int): Low byte parameter (default: 0)

**Returns:** None

**DFPlayer Protocol:**
```
[START] [VER] [LEN] [CMD] [FB] [P1] [P2] [CHK_H] [CHK_L] [END]
  0x7E   0xFF  0x06  cmd   0x00  p1   p2   chkh    chkl   0xEF
```

**Example:**
```python
# Play track 3
dfplayer_send(0x03, 0x00, 0x03)
```

---

#### `df_play(track_no)`

Play specific track number on DFPlayer.

**Parameters:**
- `track_no` (int): Track number (1-3000)

**Returns:** None

**Example:**
```python
df_play(5)  # Plays 0005.mp3
```

---

#### `df_set_volume(volume)`

Set DFPlayer volume level.

**Parameters:**
- `volume` (int): Volume level (0-30)

**Returns:** None

**Example:**
```python
df_set_volume(25)  # Set to 83% volume
```

---

#### `df_stop()`

Stop current playback.

**Returns:** None

**Example:**
```python
df_stop()
```

---

## TCS34725 Driver API

### Module: `tcs34725.py`

#### Class: `TCS34725`

I2C-based RGB color sensor driver.

---

#### `__init__(i2c, address=0x29)`

Initialize TCS34725 sensor.

**Parameters:**
- `i2c` (I2C): MicroPython I2C object
- `address` (int): I2C address (default: 0x29)

**Raises:**
- `RuntimeError`: If sensor not detected

**Example:**
```python
from machine import I2C, Pin
import tcs34725

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = tcs34725.TCS34725(i2c)
```

---

#### `get_raw_data()`

Read raw RGBC values from sensor.

**Returns:**
- `tuple`: (red, green, blue, clear)
  - All values are integers (0-65535)

**Example:**
```python
r, g, b, c = sensor.get_raw_data()
print(f"R={r}, G={g}, B={b}, Clear={c}")
```

---

#### `read_rgb()`

Read RGB values (without clear channel).

**Returns:**
- `tuple`: (red, green, blue)

**Example:**
```python
r, g, b = sensor.read_rgb()
```

---

#### `integration_time(value=None)`

Get or set integration time.

**Parameters:**
- `value` (int or None): Integration time constant (default: None to get)

**Returns:**
- `int`: Current integration time (if value=None)

**Constants:**
- `_INTEGRATION_TIME_2_4MS` = 0xFF (2.4ms, fastest)
- `_INTEGRATION_TIME_50MS` = 0xEB (50ms, default)
- `_INTEGRATION_TIME_700MS` = 0x00 (700ms, slowest/most accurate)

**Example:**
```python
sensor.integration_time(_INTEGRATION_TIME_50MS)
```

---

#### `gain(value=None)`

Get or set sensor gain.

**Parameters:**
- `value` (int or None): Gain constant (default: None to get)

**Returns:**
- `int`: Current gain (if value=None)

**Constants:**
- `_GAIN_1X` = 0x00 (1x gain)
- `_GAIN_4X` = 0x01 (4x gain, default)
- `_GAIN_16X` = 0x02 (16x gain)
- `_GAIN_60X` = 0x03 (60x gain)

**Example:**
```python
sensor.gain(_GAIN_16X)  # Increase sensitivity
```

---

#### `enable(enable=True)`

Enable or disable sensor.

**Parameters:**
- `enable` (bool): True to enable, False to disable

**Example:**
```python
sensor.enable(False)  # Power down sensor
```

---

## Configuration Schema

### Sender `config.json`

```json
{
  "wifi": {
    "ssid": "string",           // WiFi network name
    "password": "string"        // WiFi password
  },
  "network": {
    "receiver_ip": "string",    // Receiver IP address
    "udp_port": 4210            // UDP port number
  },
  "sensor": {
    "sample_delay": 1.0,        // Seconds between readings
    "min_intensity": 200,       // Minimum light threshold
    "confidence_threshold": 0.6 // Minimum confidence (0.0-1.0)
  }
}
```

---

### Receiver `config.json`

```json
{
  "wifi": {
    "ssid": "string",
    "password": "string"
  },
  "network": {
    "udp_port": 4210
  },
  "dfplayer": {
    "tx_pin": 17,              // ESP32 TX pin
    "rx_pin": 16,              // ESP32 RX pin
    "volume": 20               // Volume (0-30)
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

---

## Network Protocol

### UDP Message Format

**Sender → Receiver:**

```
Format: "ColorName:Confidence"
Example: "Red:0.92"
Encoding: UTF-8
Max Size: 64 bytes
```

**Receiver → Sender (ACK):**

```
Format: "ACK"
Encoding: UTF-8
Size: 3 bytes
```

---

### Communication Flow

```
Sender                          Receiver
  │                                │
  │   "Red:0.92"                  │
  ├──────────────────────────────►│
  │                                │
  │         (Process color)        │
  │         (Play audio)           │
  │                                │
  │         "ACK"                  │
  │◄──────────────────────────────┤
  │                                │
```

---

### Error Handling

**Connection Errors:**
- WiFi drops: Auto-reconnect with `monitor_wifi()`
- Socket timeout: Retry logic in `send_with_ack()`

**Sensor Errors:**
- I2C failure: Catch exception, wait 1s, retry
- Invalid readings: Filter with `MIN_INTENSITY`

**Audio Errors:**
- DFPlayer non-responsive: Continue operation, log error
- SD card missing: Silent failure (DFPlayer handles)

---

## Usage Examples

### Complete Sender Example

```python
from machine import I2C, Pin
import tcs34725
import network
import socket
import time

# Initialize
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = tcs34725.TCS34725(i2c)
wlan = wifi_connect("MyWiFi", "pass123")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Calibrate
calibrate_sensor(10)

# Main loop
while True:
    r, g, b, _ = sensor.get_raw_data()
    color, conf = detect_rgb_color_enhanced(r, g, b)

    if conf > 0.6:
        msg = f"{color}:{conf:.2f}".encode()
        send_with_ack(sock, msg, "192.168.1.100", 4210)

    time.sleep(1.0)
```

---

### Complete Receiver Example

```python
from machine import UART, Pin
import network
import socket

# Initialize
uart = UART(2, baudrate=9600, tx=17, rx=16)
df_set_volume(20)
wlan = wifi_connect("MyWiFi", "pass123")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 4210))

# Main loop
while True:
    try:
        data, addr = sock.recvfrom(512)
        text = data.decode().strip()
        color, conf = text.split(':')

        if color in COLOR_TO_TRACK:
            df_play(COLOR_TO_TRACK[color])
            sock.sendto(b"ACK", addr)
    except:
        continue
```

---

## Performance Considerations

### Memory Usage

- **Sender**: ~15-20 KB RAM
- **Receiver**: ~12-18 KB RAM
- **Config files**: <1 KB each

### Timing

- **Color detection**: ~100ms per reading
- **Network latency**: <100ms (local WiFi)
- **Audio trigger**: ~50ms from receive to play
- **Total loop**: ~1 second per detection

### Optimization Tips

1. **Reduce `sample_delay`** for faster detection (min 0.5s)
2. **Lower `confidence_threshold`** for more triggers
3. **Use static IP** to reduce DHCP overhead
4. **Disable debug prints** in production for speed

---

End of API Documentation.
