# tcs34725.py - TCS34725 Color Sensor Driver for MicroPython
from micropython import const
import time

# Register addresses
_COMMAND_BIT = const(0x80)
_ENABLE = const(0x00)
_ATIME = const(0x01)
_CONTROL = const(0x0F)
_ID = const(0x12)
_STATUS = const(0x13)
_CDATAL = const(0x14)
_RDATAL = const(0x16)
_GDATAL = const(0x18)
_BDATAL = const(0x1A)

# Enable register bits
_ENABLE_PON = const(0x01)
_ENABLE_AEN = const(0x02)

# Integration time settings (longer = more accurate but slower)
_INTEGRATION_TIME_2_4MS = const(0xFF)
_INTEGRATION_TIME_24MS = const(0xF6)
_INTEGRATION_TIME_50MS = const(0xEB)
_INTEGRATION_TIME_101MS = const(0xD5)
_INTEGRATION_TIME_154MS = const(0xC0)
_INTEGRATION_TIME_700MS = const(0x00)

# Gain settings
_GAIN_1X = const(0x00)
_GAIN_4X = const(0x01)
_GAIN_16X = const(0x02)
_GAIN_60X = const(0x03)

class TCS34725:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self.address = address
        
        # Check sensor ID
        sensor_id = self._read_byte(_ID)
        if sensor_id not in (0x44, 0x4D):
            raise RuntimeError(f"TCS34725 not found. ID: {sensor_id:#x}")
        
        # Initialize sensor
        self._write_byte(_ENABLE, _ENABLE_PON)
        time.sleep(0.003)  # Wait 3ms for power on
        self._write_byte(_ENABLE, _ENABLE_PON | _ENABLE_AEN)
        
        # Set default integration time and gain
        self.integration_time(_INTEGRATION_TIME_50MS)
        self.gain(_GAIN_4X)
        
        time.sleep(0.003)
    
    def _write_byte(self, register, value):
        self.i2c.writeto_mem(self.address, _COMMAND_BIT | register, bytes([value]))
    
    def _read_byte(self, register):
        return self.i2c.readfrom_mem(self.address, _COMMAND_BIT | register, 1)[0]
    
    def _read_word(self, register):
        data = self.i2c.readfrom_mem(self.address, _COMMAND_BIT | register, 2)
        return data[0] | (data[1] << 8)
    
    def integration_time(self, value=None):
        if value is None:
            return self._integration_time
        self._integration_time = value
        self._write_byte(_ATIME, value)
    
    def gain(self, value=None):
        if value is None:
            return self._gain
        self._gain = value
        self._write_byte(_CONTROL, value)
    
    def get_raw_data(self):
        """Read RGBC values. Returns tuple (r, g, b, clear)"""
        # Check if data is ready
        status = self._read_byte(_STATUS)
        if not (status & 0x01):
            time.sleep(0.003)  # Wait a bit if not ready
        
        c = self._read_word(_CDATAL)
        r = self._read_word(_RDATAL)
        g = self._read_word(_GDATAL)
        b = self._read_word(_BDATAL)
        
        return (r, g, b, c)
    
    def read_rgb(self):
        """Simplified RGB read (without clear channel)"""
        r, g, b, _ = self.get_raw_data()
        return (r, g, b)
    
    def enable(self, enable=True):
        if enable:
            self._write_byte(_ENABLE, _ENABLE_PON | _ENABLE_AEN)
        else:
            self._write_byte(_ENABLE, 0x00)
