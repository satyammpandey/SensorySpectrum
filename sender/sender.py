# sender.py - Enhanced MicroPython for ESP32
import network, socket, time, ujson
from machine import I2C, Pin
import tcs34725

# ===== LED for status indication =====
led = Pin(2, Pin.OUT)

def blink_led(times=1, duration=0.1):
    for _ in range(times):
        led.on()
        time.sleep(duration)
        led.off()
        time.sleep(duration)

# ===== Load Configuration =====
def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as f:
            return ujson.load(f)
    except Exception as e:
        print("Config load error:", e)
        return None

config = load_config()
if not config:
    print("ERROR: No config file. Using defaults (may not work!)")
    config = {
        "wifi": {"ssid": "Your_SSID", "password": "Your_PASSWORD"},
        "network": {"receiver_ip": "192.168.4.2", "udp_port": 4210},
        "sensor": {"sample_delay": 1.0, "min_intensity": 200, "confidence_threshold": 0.6}
    }

SSID = config["wifi"]["ssid"]
PASSWORD = config["wifi"]["password"]
RECEIVER_IP = config["network"]["receiver_ip"]
UDP_PORT = config["network"]["udp_port"]
SAMPLE_DELAY = config["sensor"]["sample_delay"]
MIN_INTENSITY = config["sensor"]["min_intensity"]
CONFIDENCE_THRESHOLD = config["sensor"]["confidence_threshold"]

# ===== Wi-Fi Functions =====
def wifi_connect(ssid, password, timeout=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                return None
            time.sleep(0.5)
            blink_led(1, 0.05)
    return wlan

def monitor_wifi(wlan):
    if not wlan.isconnected():
        print("WiFi dropped! Reconnecting...")
        blink_led(5, 0.1)  # Error indication
        return wifi_connect(SSID, PASSWORD)
    return wlan

# ===== Sensor Setup =====
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = tcs34725.TCS34725(i2c)

# ===== Calibration Function =====
calibration_factors = (1.0, 1.0, 1.0)

def calibrate_sensor(samples=10):
    global calibration_factors
    print("\n=== CALIBRATION MODE ===")
    print("Point sensor at WHITE surface in 3 seconds...")
    blink_led(3, 0.3)
    time.sleep(3)
    
    r_sum, g_sum, b_sum = 0, 0, 0
    print("Sampling...")
    for i in range(samples):
        try:
            r, g, b, _ = sensor.get_raw_data()
            r_sum += r
            g_sum += g
            b_sum += b
            print(f"  Sample {i+1}: R={r} G={g} B={b}")
            time.sleep(0.2)
        except:
            continue
    
    r_avg = r_sum / samples
    g_avg = g_sum / samples
    b_avg = b_sum / samples
    
    max_avg = max(r_avg, g_avg, b_avg)
    r_factor = max_avg / r_avg if r_avg > 0 else 1.0
    g_factor = max_avg / g_avg if g_avg > 0 else 1.0
    b_factor = max_avg / b_avg if b_avg > 0 else 1.0
    
    calibration_factors = (r_factor, g_factor, b_factor)
    print(f"Calibration complete!")
    print(f"Factors: R={r_factor:.2f}, G={g_factor:.2f}, B={b_factor:.2f}")
    blink_led(2, 0.2)
    return calibration_factors

# ===== Enhanced Color Detection =====
def detect_rgb_color_enhanced(r, g, b):
    # Apply calibration
    r = int(r * calibration_factors[0])
    g = int(g * calibration_factors[1])
    b = int(b * calibration_factors[2])
    
    # Normalize to 0-255 if needed
    max_val = max(r, g, b)
    if max_val > 255:
        scale = 255 / max_val
        r, g, b = int(r * scale), int(g * scale), int(b * scale)
    
    total = r + g + b
    MIN_TOTAL = MIN_INTENSITY * 3
    MAX_TOTAL = 700
    
    # Black detection
    if total < MIN_TOTAL:
        return "Black", 0.9
    
    # White detection
    if total > MAX_TOTAL and abs(r-g) < 50 and abs(g-b) < 50 and abs(r-b) < 50:
        return "White", 0.9
    
    # Calculate percentages
    if total == 0:
        return "Unknown", 0.0
    
    r_pct = r / total
    g_pct = g / total
    b_pct = b / total
    
    # Primary colors
    if r_pct > 0.5 and g_pct < 0.3 and b_pct < 0.3:
        return "Red", min(r_pct * 1.5, 0.95)
    if g_pct > 0.5 and r_pct < 0.3 and b_pct < 0.3:
        return "Green", min(g_pct * 1.5, 0.95)
    if b_pct > 0.5 and r_pct < 0.3 and g_pct < 0.3:
        return "Blue", min(b_pct * 1.5, 0.95)
    
    # Secondary colors
    if r_pct > 0.35 and g_pct > 0.35 and b_pct < 0.25:
        return "Yellow", 0.8
    if r_pct > 0.35 and b_pct > 0.35 and g_pct < 0.25:
        return "Magenta", 0.8
    if g_pct > 0.35 and b_pct > 0.35 and r_pct < 0.25:
        return "Cyan", 0.8
    
    # Orange
    if r_pct > 0.45 and g_pct > 0.25 and g_pct < 0.40 and b_pct < 0.2:
        return "Orange", 0.75
    
    # Purple
    if b_pct > 0.35 and r_pct > 0.30 and g_pct < 0.25:
        return "Purple", 0.75
    
    return "Unknown", 0.3

# ===== UDP with Acknowledgment =====
def send_with_ack(sock, message, addr, port, timeout=0.5, retries=3):
    for attempt in range(retries):
        try:
            sock.sendto(message, (addr, port))
            sock.settimeout(timeout)
            ack, _ = sock.recvfrom(64)
            if ack == b"ACK":
                return True
        except:
            if attempt < retries - 1:
                print(f"  Retry {attempt + 1}...")
                continue
    return False

# ===== Main Initialization =====
print("\n" + "="*40)
print("SENSORY SPECTRUM - Sender Unit")
print("="*40)

# Connect to WiFi
wlan = wifi_connect(SSID, PASSWORD)
if not wlan:
    print("ERROR: WiFi connection failed!")
    blink_led(10, 0.1)
    raise SystemExit

print(f"WiFi connected! IP: {wlan.ifconfig()[0]}")
blink_led(3, 0.1)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# Run calibration
calibrate_sensor(10)

# ===== Main Loop =====
print("\nStarting color detection loop...")
print("="*40 + "\n")

last_wifi_check = time.time()
last_color = None
color_stable_count = 0
WIFI_CHECK_INTERVAL = 10
STABILITY_THRESHOLD = 2  # Same color must appear 2 times

while True:
    try:
        # WiFi monitoring
        if time.time() - last_wifi_check > WIFI_CHECK_INTERVAL:
            wlan = monitor_wifi(wlan)
            last_wifi_check = time.time()
        
        # Read sensor
        try:
            r, g, b, _ = sensor.get_raw_data()
        except Exception as e:
            print("Sensor read error:", e)
            time.sleep(1)
            continue
        
        # Detect color
        color, confidence = detect_rgb_color_enhanced(r, g, b)
        
        print(f"Raw: R={r:4d} G={g:4d} B={b:4d} | {color:8s} ({confidence:.1%})")
        
        # Stability check - only send if color is stable
        if color == last_color:
            color_stable_count += 1
        else:
            color_stable_count = 0
            last_color = color
        
        # Send if stable and confident
        if (color_stable_count >= STABILITY_THRESHOLD and 
            confidence >= CONFIDENCE_THRESHOLD and 
            color != "Unknown"):
            
            msg = f"{color}:{confidence:.2f}".encode('utf-8')
            success = send_with_ack(sock, msg, RECEIVER_IP, UDP_PORT)
            
            if success:
                print(f"✓ Sent: {color} (ACK received)")
                blink_led(1, 0.05)
            else:
                print(f"✗ Send failed (no ACK)")
                blink_led(3, 0.05)
            
            # Reset to avoid spam
            color_stable_count = 0
            time.sleep(2)  # Cooldown after successful send
        
    except Exception as e:
        print("Loop error:", e)
        blink_led(5, 0.05)
    
    time.sleep(SAMPLE_DELAY)