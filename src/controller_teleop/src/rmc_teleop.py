#!/usr/bin/env python

"""
Description: Node to read msgs from the joy node and send out control messages
for the custom RMC robot. Uses custom robot_cmd messages defined in this package

Authors: Ryan

"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3

# Custom robot command message
from controller_teleop.msg import robot_cmd


# Callback function to convert joy data to velocity commands
def cmd_callback(msg):
	# Setup the publisher for the robot commmands topic
	pub = rospy.Publisher('/rmc_bot/commands', robot_cmd, queue_size=1)

	# Create a new robot command message
	cmd_msg = robot_cmd()

	cmd_msg.header.stamp = rospy.Time.now()

	# Check if the deadman drive switch, currently LB, is held down
	if(msg.buttons[4] == 1):

		cmd_msg.dt_linear.x = msg.axes[1] # Left stick forward and backwards
		cmd_msg.dt_linear.y = 0
		cmd_msg.dt_linear.z = 0
		cmd_msg.dt_angular.x = 0
		cmd_msg.dt_angular.y = 0
		cmd_msg.dt_angular.z = msg.axes[3] # Right stick left and right

		pub.publish(cmd_msg)

		return

	# Check if the deadman dig switch, currently RB, is held down
	elif(msg.buttons[5] == 1):
		# TODO: May need to swap these around in the future if we need the digger to be able to spin both ways
		cmd_msg.convey_spd = -.5*(msg.axes[5] - 1) # RT. In joy node not pressed = 1, half pressed = 0, full pressed = -1. This math should make not pressed = 0 and full pressed = 1
		cmd_msg.lin_act_spd = msg.axes[1] # Left stick forward and backward
		cmd_msg.rot_spd = msg.axes[4] # Right stick forward and backward

		pub.publish(cmd_msg)

		return

	# Check if deadman dispense switch, currently LT, is mostly held down
	elif((-.5*(msg.axes[2] - 1)) > .9):
		cmd_msg.scissor_spd = msg.axes[1] # Left stick forward and backward
		cmd_msg.bucket_spd = msg.axes[4] # Right stick forward and backward

		pub.publish(cmd_msg)

		return


if __name__ == '__main__':
	# Initialize the node
	rospy.init_node('teleop_node', anonymous=True)

	# Subscribe to joy topic to get input from controller
	rospy.Subscriber("joy", Joy, cmd_callback)

	rospy.spin()
