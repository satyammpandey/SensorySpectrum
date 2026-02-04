"""
Network Scanner for Sensory Spectrum
Finds ESP32 devices on local network by hostname
"""

import socket
import subprocess
import time
from scapy.all import ARP, Ether, srp  # Requires: pip install scapy

def scan_network(interface="wlan0"):
    """Scan local network for devices"""
    print("🔍 Scanning local network...")

    # Get local IP range
    result = subprocess.run(["ip", "route"], capture_output=True, text=True)
    gateway = result.stdout.split("default via ")[1].split(" ")[0]
    ip_range = ".".join(gateway.split(".")[:-1]) + ".1/24"

    print(f"Scanning {ip_range}...")

    # ARP scan
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        mac = received.hwsrc
        ip = received.psrc
        devices.append((ip, mac))

    print("📡 Devices found:")
    for ip, mac in devices:
        hostname = socket.gethostbyaddr(ip)[0] if socket.gethostbyaddr(ip) else "Unknown"
        print(f"  {ip} ({hostname}) - {mac}")
        if "sensory" in hostname.lower():
            print(f"🎯 RECEIVER FOUND: {ip}")

    return devices

def ping_esp32(ip):
    """Test if ESP32 is responsive"""
    print(f"🏓 Pinging {ip}...")
    result = subprocess.run(["ping", "-c", "3", ip], capture_output=True)
    if result.returncode == 0:
        print(f"✅ {ip} is online!")
        return True
    else:
        print(f"❌ {ip} not responding")
        return False

if __name__ == "__main__":
    scan_network()
