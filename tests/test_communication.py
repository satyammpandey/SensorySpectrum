"""
UDP Communication Test
Test sender-receiver communication on network
"""
import socket
import time
import sys

def test_receiver(port=4210, timeout=10):
    """Listen for UDP packets (run on receiver ESP32)"""
    print(f"📡 Starting receiver on port {port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.settimeout(timeout)
    
    print(f"Listening for {timeout} seconds...")
    try:
        data, addr = sock.recvfrom(1024)
        print(f"✅ Received: '{data.decode()}' from {addr[0]}:{addr[1]}")
        
        # Send ACK back
        sock.sendto(b"ACK", addr)
        print(f"📤 Sent ACK to {addr[0]}")
        return True
    except socket.timeout:
        print("❌ No data received (timeout)")
        return False
    finally:
        sock.close()

def test_sender(receiver_ip, port=4210):
    """Send test UDP packet (run on sender ESP32)"""
    print(f"📤 Sending test to {receiver_ip}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    
    test_msg = "Red:0.95".encode()
    sock.sendto(test_msg, (receiver_ip, port))
    print(f"✅ Sent: '{test_msg.decode()}'")
    
    # Wait for ACK
    try:
        data, addr = sock.recvfrom(1024)
        print(f"✅ Received ACK from {addr[0]}")
        return True
    except socket.timeout:
        print("⚠️ No ACK received (receiver might be offline)")
        return False
    finally:
        sock.close()

# Main test
print("🧪 UDP Communication Test")
print("=" * 40)

if len(sys.argv) > 1 and sys.argv[1] == "receiver":
    # Receiver mode
    test_receiver()
elif len(sys.argv) > 1:
    # Sender mode with IP argument
    receiver_ip = sys.argv[1]
    test_sender(receiver_ip)
else:
    print("Usage:")
    print("  Receiver: python test_communication.py receiver")
    print("  Sender:   python test_communication.py 192.168.1.100")
