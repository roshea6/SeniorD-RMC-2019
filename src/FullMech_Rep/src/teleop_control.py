#!/usr/bin/env python

"""
Description: Node to read msgs from the joy node and send out cmd_vel msgs that
the robot joint state controller listens for

Authors: Ryan

"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

# Callback function to convert joy data to velocity commands
def vel_callback(msg):
	pub = rospy.Publisher('/diffdrive_controller/cmd_vel', Twist, queue_size=1)
	vel_msg = Twist()

	vel_msg.linear.x = msg.axes[1]*2
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = msg.axes[3]*2

	pub.publish(vel_msg)


if __name__ == '__main__':
	# Initialize the node
	rospy.init_node('teleop_node', anonymous=True)

	# Subscribe to joy topic to get input from controller
	rospy.Subscriber("joy", Joy, vel_callback)

	rospy.spin()
