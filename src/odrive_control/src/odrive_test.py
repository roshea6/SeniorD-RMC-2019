#!/usr/bin/env python

import odrive
from odrive.enums import *
import time
import rospy

# Custom robot command message
from controller_teleop.msg import robot_cmd


# Controls the motor attached to the odrive based on incoming ROS messages
def dtCallback(cmd_msg):
	odrv0.axis0.controller.vel_setpoint = 600 * cmd_msg.dt_linear.x

if __name__ == "__main__":
	print("Connecting to Odrive...")

	# Find an available odrive device. This function will hold until a device is found
	odrv0 = odrive.find_any(serial_number="2060387E304E")

	# Calibrate the system
	# TODO: Take out and set pre_calibrated tag to true
	print("starting calibration...")
	odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while odrv0.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	# Set state to closed loop control
	# In this state the odrive will try to maintain whatever state you send it
	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	# Request the odrive to enter velocity control mode
	odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL

	# print("changing vel")
	# while(True):
	# 	odrv0.axis0.controller.vel_setpoint = 300
	# 	time.sleep(1)
	# 	odrv0.axis0.controller.vel_setpoint = 400
	# 	time.sleep(1)

	# Initiliaze the ROS node
	rospy.init_node('drivetrain_control', anonymous=True)

	# Subscribe to robot command topic
	rospy.Subscriber("/rmc_bot/commands", robot_cmd, dtCallback)

	rospy.spin()
	
	