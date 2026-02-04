# receiver.py - Enhanced MicroPython for ESP32
import network, socket, time, ujson
from machine import UART, Pin

# ===== LED for status =====
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
    except:
        return None

config = load_config()
if not config:
    print("ERROR: No config file!")
    config = {
        "wifi": {"ssid": "Your_SSID", "password": "Your_PASSWORD"},
        "network": {"udp_port": 4210},
        "dfplayer": {"tx_pin": 17, "rx_pin": 16, "volume": 20},
        "audio": {
            "track_map": {
                "Red": 1, "Green": 2, "Blue": 3, "Yellow": 4,
                "Cyan": 5, "Magenta": 6, "Orange": 7, "Purple": 8,
                "White": 9, "Black": 10
            }
        }
    }

SSID = config["wifi"]["ssid"]
PASSWORD = config["wifi"]["password"]
UDP_PORT = config["network"]["udp_port"]
DF_TX = config["dfplayer"]["tx_pin"]
DF_RX = config["dfplayer"]["rx_pin"]
VOLUME = config["dfplayer"]["volume"]
COLOR_TO_TRACK = config["audio"]["track_map"]

# ===== WiFi Functions =====
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
    return wlan

# ===== DFPlayer Functions =====
uart = UART(2, baudrate=9600, tx=DF_TX, rx=DF_RX)
time.sleep(0.1)

def dfplayer_send(cmd, param1=0, param2=0):
    head = 0x7E
    ver = 0xFF
    length = 0x06
    feedback = 0x00
    high = param1 & 0xFF
    low = param2 & 0xFF
    checksum = -(ver + length + cmd + feedback + high + low) & 0xFFFF
    chkh = (checksum >> 8) & 0xFF
    chkl = checksum & 0xFF
    packet = bytearray([head, ver, length, cmd, feedback, high, low, chkh, chkl, 0xEF])
    uart.write(packet)

def df_play(track_no):
    if 1 <= track_no <= 3000:
        dfplayer_send(0x03, 0x00, track_no)

def df_set_volume(volume):
    volume = max(0, min(30, volume))
    dfplayer_send(0x06, 0x00, volume)

def df_stop():
    dfplayer_send(0x16)

# ===== Initialize =====
print("\n" + "="*40)
print("SENSORY SPECTRUM - Receiver Unit")
print("="*40)

wlan = wifi_connect(SSID, PASSWORD)
if not wlan:
    print("ERROR: WiFi failed!")
    blink_led(10, 0.1)
    raise SystemExit

ip = wlan.ifconfig()[0]
print(f"WiFi connected! IP: {ip}")
blink_led(3, 0.1)

# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1.0)
sock.bind(('', UDP_PORT))
print(f"Listening on UDP port {UDP_PORT}")

# Initialize DFPlayer
time.sleep(0.3)
df_set_volume(VOLUME)
time.sleep(0.2)
print(f"DFPlayer ready (Volume: {VOLUME})")

print("\nWaiting for color data...")
print("="*40 + "\n")

# ===== Main Loop =====
last_played = None
last_play_time = 0
MIN_PLAY_INTERVAL = 3  # seconds between same color plays

while True:
    try:
        data, addr = sock.recvfrom(512)
        if not data:
            continue
        
        # Parse message: "Color:confidence"
        text = data.decode('utf-8').strip()
        parts = text.split(':')
        color = parts[0]
        confidence = float(parts[1]) if len(parts) > 1 else 0.0
        
        print(f"Received from {addr[0]}: {color} ({confidence:.1%})")
        
        # Send ACK
        sock.sendto(b"ACK", addr)
        
        # Check if valid color
        if color not in COLOR_TO_TRACK:
            print(f"  Unknown color: {color}")
            continue
        
        # Avoid replaying same color too quickly
        current_time = time.time()
        if color == last_played and (current_time - last_play_time) < MIN_PLAY_INTERVAL:
            print(f"  Skipping (played recently)")
            continue
        
        # Play track
        track = COLOR_TO_TRACK[color]
        print(f"  ♪ Playing track {track}: {color}")
        df_play(track)
        blink_led(2, 0.1)
        
        last_played = color
        last_play_time = current_time
        
    except socket.timeout:
        continue
    except Exception as e:
        print("Error:", e)
        blink_led(5, 0.05)
        time.sleep(0.5)
