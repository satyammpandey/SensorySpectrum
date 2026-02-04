# boot.py - runs on boot
import esp
import gc

# Disable debug output
esp.osdebug(None)

# Run garbage collection
gc.collect()

print("\n" + "="*40)
print("Sensory Spectrum - Booting...")
print("="*40)
