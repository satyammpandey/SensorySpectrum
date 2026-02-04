"""
ESP32 Flash Helper for Sensory Spectrum
Automates flashing MicroPython and uploading code files
"""

import subprocess
import sys
import argparse
import os

def run_command(cmd, check=True):
    """Run shell command and print output"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def flash_esp32(port, firmware_path="micropython-esp32.bin"):
    """Flash MicroPython firmware"""
    print(f"🔥 Flashing {port}...")
    run_command(["esptool.py", "--port", port, "erase_flash"])
    run_command([
        "esptool.py", "--port", port, "--baud", "460800", 
        "write_flash", "-z", "0x1000", firmware_path
    ])
    print("✅ Firmware flashed!")

def upload_sender(port):
    """Upload sender files"""
    print(f"📤 Uploading sender to {port}...")
    for filename in ["boot.py", "config.json", "sender.py", "tcs34725.py"]:
        run_command(["ampy", "--port", port, "put", f"sender/{filename}"])
    run_command(["ampy", "--port", port, "put", "sender/sender.py", "main.py"])
    print("✅ Sender uploaded!")

def upload_receiver(port):
    """Upload receiver files"""
    print(f"📤 Uploading receiver to {port}...")
    for filename in ["boot.py", "config.json", "receiver.py"]:
        run_command(["ampy", "--port", port, "put", f"receiver/{filename}"])
    run_command(["ampy", "--port", port, "put", "receiver/receiver.py", "main.py"])
    print("✅ Receiver uploaded!")

def main():
    parser = argparse.ArgumentParser(description="Sensory Spectrum Flash Helper")
    parser.add_argument("--sender-port", required=True, help="Sender ESP32 port (COM3)")
    parser.add_argument("--receiver-port", required=True, help="Receiver ESP32 port (COM4)")
    parser.add_argument("--firmware", default="micropython-esp32.bin", help="MicroPython firmware")
    args = parser.parse_args()

    # Flash both ESP32s
    flash_esp32(args.sender_port, args.firmware)
    flash_esp32(args.receiver_port, args.firmware)

    # Upload code
    upload_sender(args.sender_port)
    upload_receiver(args.receiver_port)

    print("\n🎉 Flash complete!")
    print(f"💡 Next: Update config.json WiFi settings")
    print("💡 Boot receiver first to get IP address")

if __name__ == "__main__":
    main()
