"""
DFPlayer Mini Audio Test
Test DFPlayer and speaker independently
"""
from machine import UART, Pin
import time

def dfplayer_send(cmd, param1=0, param2=0):
    """Send command to DFPlayer Mini"""
    buf = bytearray(10)
    buf[0] = 0x7E  # Start byte
    buf[1] = 0xFF  # Version
    buf[2] = 0x06  # Length
    buf[3] = cmd   # Command
    buf[4] = 0x00  # Feedback
    buf[5] = param1
    buf[6] = param2
    # Calculate checksum
    checksum = -sum(buf[1:7])
    buf[7] = (checksum >> 8) & 0xFF
    buf[8] = checksum & 0xFF
    buf[9] = 0xEF  # End byte
    uart.write(buf)

# Initialize UART
uart = UART(2, baudrate=9600, tx=Pin(17), rx=Pin(16))
time.sleep(1)

print("🔊 DFPlayer Mini Test")
print("=" * 40)

print("\n1. Setting volume to 25/30...")
dfplayer_send(0x06, 0x00, 25)  # Volume command
time.sleep(0.5)

print("2. Playing test tracks...")
for track in range(1, 4):
    print(f"   Playing track {track:04d}.mp3...")
    dfplayer_send(0x03, 0x00, track)  # Play track command
    time.sleep(3)
    print(f"   ✅ Track {track} complete")

print("\n3. Stopping playback...")
dfplayer_send(0x0E)  # Stop command
time.sleep(0.5)

print("\n✅ DFPlayer test complete!")
print("If you heard audio, hardware is working!")
