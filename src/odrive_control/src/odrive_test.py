#!/usr/bin/env python

import odrive
from odrive.enums import *
import time

print("Connecting to Odrive...")

# Find an available odrive device. This function will hold until a device is found
odrv0 = odrive.find_any(serial_number="2060387E304E")

print("starting calibration...")
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL

print("changing vel")
while(True):
	odrv0.axis0.controller.vel_setpoint = 300
	time.sleep(1)
	odrv0.axis0.controller.vel_setpoint = 400
	time.sleep(1)
