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
        results = sensor.read()
        num_faces = results[0]
        bboxes = results[1]
        print("Found ",num_faces," faces:")
        #print(bboxes)
        for i in range(num_faces):
            bbox = bboxes[i]
            print("X0: ",bbox["x0"]," Y0: ",bbox["y0"]," X1: ", bbox["x1"]," Y1: ", bbox["y1"], " Confidence: ", bbox["confidence"], " ID: ", bbox["id"], " ID Confidence: ", bbox["id_confidence"], " Face On: ", bbox["face_on"] )
        time.sleep(1)
except Exception as e: print(e)
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()