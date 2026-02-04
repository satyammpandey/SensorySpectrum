"""
TCS34725 Sensor Standalone Test
Test sensor without full system
"""
from machine import I2C, Pin
import time

def scan_i2c(i2c):
    devices = i2c.scan()
    print("I2C devices:", [hex(d) for d in devices])
    return 0x29 in devices

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

print("🧪 TCS34725 Sensor Test")
if not scan_i2c(i2c):
    print("❌ Sensor not detected!")
    print("Check wiring: 3.3V, GND, SCL(GP22), SDA(GP21)")
else:
    print("✅ Sensor detected!")
    
    # Import sensor driver
    import tcs34725
    sensor = tcs34725.TCS34725(i2c)
    
    # Test readings
    print("\nTesting raw readings (point at colors):")
    for i in range(20):
        r, g, b, c = sensor.get_raw_data()
        total = r + g + b
        print(f"#{i+1:2d}: R={r:4d} G={g:4d} B={b:4d} Total={total:4d}")
        time.sleep(0.5)
