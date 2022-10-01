# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Luke Berndt for Robotastic
#
# SPDX-License-Identifier: MIT
"""
`usefulsensorpersondetector`
================================================================================

I2C interface for the Useful Sensor Person Detector


* Author(s): Luke Berndt

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/robotastic/CircuitPython_UsefulSensorPersonDetector.git"



# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()


from adafruit_bus_device.i2c_device import I2CDevice
import struct
from micropython import const
from busio import I2C


_USEFUL_SENSOR_DEFAULT_ADDRESS = const(0x62)
_USEFUL_SENSOR_MODE_REGISTER = const(0x01)
_USEFUL_SENSOR_RUN_ID_MODEL_REGISTER = const(0x02)
_USEFUL_SENSOR_SINGLE_CAPTURE_REGISTER = const(0x03)
_USEFUL_SENSOR_CALIBRATION_REGISTER = const(0x04)
_USEFUL_SENSOR_SMOOTHING_REGISTER = const(0x05)


class PersonDetector:
    def __init__(self, i2c: I2C, address: int= _USEFUL_SENSOR_DEFAULT_ADDRESS):
        self.i2c_device = I2CDevice(i2c, address)
        self.reg_buf = bytearray(3)
        self.cmd_buf = bytearray(1)    

    def _write_register(self, reg: int, value: int):
        """Write 16 bit value to register."""
        self.reg_buf[0] = reg
        self.reg_buf[1] = (value >> 8) & 0xFF
        self.reg_buf[2] = value & 0xFF
        with self.i2c_device as i2c:
            i2c.write(self.reg_buf)

    def read(self):
        format = "ffBBBBb"
        result = bytearray(struct.calcsize(format))
        self.i2c_device.readinto(result, end=16)

        (confidence,id_confidence,x0,y0,x1,y1,id) = struct.unpack(format,result)
        
        return (x0,y0,x1,y1,confidence, id, id_confidence)

    def setStandbyMode(self):
        self._write_register(_USEFUL_SENSOR_MODE_REGISTER,0)

    def setContinuousMode(self):
        self._write_register(_USEFUL_SENSOR_MODE_REGISTER,1)

    def setIdModelEnabled(self, enabled):
        self._write_register(_USEFUL_SENSOR_RUN_ID_MODEL_REGISTER, int(enabled))

    def setSmoothingEnabled(self, enabled):
        self._write_register(_USEFUL_SENSOR_SMOOTHING_REGISTER, int(enabled))

    def singleCapture(self):
        """Write to register."""
        self.cmd_buf[0] = _USEFUL_SENSOR_SINGLE_CAPTURE_REGISTER
        with self.i2c_device as i2c:
            i2c.write(self.cmd_buf)
        
    def calibrate(self, id):
        self._write_register(_USEFUL_SENSOR_CALIBRATION_REGISTER, id)

