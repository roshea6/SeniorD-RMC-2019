#!/usr/bin/env python

import odrive
from odrive.enums import *
import time
import rospy

# Custom robot command message
from controller_teleop.msg import robot_cmd


# Controls the motor attached to the odrive based on incoming ROS messages
def dtCallback(cmd_msg):
	vel = 600 * cmd_msg.dt_linear.x

	print vel

	odrv0.axis0.controller.vel_setpoint = vel
	odrv0.axis1.controller.vel_setpoint = vel

if __name__ == "__main__":
	print("Connecting to Odrive 0")

	# Find an available odrive device. This function will hold until a device is found
	odrv0 = odrive.find_any(serial_number="2060387E304E")

	print("Connected")

	# odrv0.axis0.motor.config.pre_calibrated = True

	# Calibrate the system
	# TODO: Take out and set pre_calibrated tag to true
	print("starting calibration of M0")
	odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while odrv0.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	# Set state to closed loop control
	# In this state the odrive will try to maintain whatever state you send it
	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	# Request the odrive to enter velocity control mode
	odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL

	# Calibrate the system
	# TODO: Take out and set pre_calibrated tag to true
	print("starting calibration of M1")
	odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while odrv0.axis1.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	# Set state to closed loop control
	# In this state the odrive will try to maintain whatever state you send it
	odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	# Request the odrive to enter velocity control mode
	odrv0.axis1.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL


	# Initiliaze the ROS node
	rospy.init_node('drivetrain_control', anonymous=True)

	# Subscribe to robot command topic
	rospy.Subscriber("/rmc_bot/commands", robot_cmd, dtCallback)

	rospy.spin()
	
	