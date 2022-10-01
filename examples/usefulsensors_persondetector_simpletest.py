# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Luke Berndt for Robotastic
#
# SPDX-License-Identifier: Unlicense

import time
import board
import usefulsensors_persondetector

i2c = board.I2C()  # uses board.SCL and board.SDA

# To initialise using the default address:
sensor = usefulsensors_persondetector.PersonDetector(i2c)

while not i2c.try_lock():
    pass

try:
    while True:
        (x0,y0,x1,y1,confidence,id,id_confidence) = sensor.read()
        print("X0: ",x0," Y0: ",y0," X1: ", x1," Y1: ", y1, " Confidence: ", confidence, " ID: ", id, " ID Confidence: ", id_confidence)
        time.sleep(1)
except Exception as e: print(e)
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()