#!/usr/bin/env python

"""
Description: Node to read msgs from the joy node and send out cmd_vel msgs that
the robot joint state controller listens for

Authors: Ryan

"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

class teleopController(object):
	def __init__(self):
		# Publishers
		self.vel_pub = rospy.Publisher('/diffdrive_controller/cmd_vel', Twist, queue_size=1)
		self.end_effector_rotate_pub = rospy.Publisher('/end_effector_rotate_controller/command', Float64, queue_size=1)
		self.end_effector_rack_pub = rospy.Publisher('/end_effector_rack_controller/command', Float64, queue_size=1)
		self.dispense_dump_pub = rospy.Publisher('/dispense_dump_controller/command', Float64, queue_size=1)
		self.dispense_scissor_pub = rospy.Publisher('/dispense_scissor_controller/command', Float64, queue_size=1)

		# Indexes of the joints in the joint state message
		self.rotate_idx = 0
		self.rack_idx = 0
		self.scissor_idx = 0
		self.dump_idx = 0

		# Variables to hold the current positions of the joints
		self.rotate_pos = 0
		self.rack_pos = 0
		self.scissor_pos = 0
		self.dump_pos = 0

		self.initialized = False


	# Callback function to convert joy data to velocity commands
	def velCallback(self, msg):
		# Check if the A button has been hit to initialize the robot
		if(msg.buttons[0] == 1):
			self.initialized = True
			print("Robot has been initialized")
		
		# Check if the robot has been initialized yet. 
		# If it hasn't then send the starting state to the robot
		if(not self.initialized):
			print "Press A to initialize the robot"

			# Empty position messages
			rotate_msg = Float64()
			rack_msg = Float64()
			scissor_msg = Float64()
			dump_msg = Float64()

			# Fill messages with ideal starting positions. Determined through testing
			rotate_msg.data = 1.25
			rack_msg.data = 0.0
			scissor_msg.data = -0.15
			dump_msg.data = 0.5

			# Publish the starting state to the robot so it isn't coliding with the ground at all
			self.end_effector_rotate_pub.publish(rotate_msg)
			self.end_effector_rack_pub.publish(rack_msg)
			self.dispense_scissor_pub.publish(scissor_msg)
			self.dispense_dump_pub.publish(dump_msg)

			return

		# Check if the deadman drive switch, currently LB, is held down
		if(msg.buttons[4] == 1):
			# Twist message for linear and angular velocity
			vel_msg = Twist()

			# Populate the message
			vel_msg.linear.x = msg.axes[1]*1 # Left joystick forward and backwards
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0
			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = msg.axes[3]*1.5 # Right joysick left and right

			self.vel_pub.publish(vel_msg)

			return

		# Check if the deadman dig switch, currently RB, is held down
		elif(msg.buttons[5] == 1):
			# Empty position messages
			rotate_msg = Float64()
			rack_msg = Float64()

			# Increment the position of the end effector rotate joint based on the 
			# Left joystick
			rotate_msg.data = self.rotate_pos - .1*msg.axes[1]

			# Increment the position of the end effector rack joint based on the 
			# Left joystick
			rack_msg.data = self.rack_pos - .1*msg.axes[4]

			# Publish the commands to the joint controllers for the end effector
			self.end_effector_rotate_pub.publish(rotate_msg)
			self.end_effector_rack_pub.publish(rack_msg)

			return

		# Check if deadman dispense switch, currently LT, is mostly held down
		elif((-.5*(msg.axes[2] - 1)) > .9):
			# Empty position messages
			scissor_msg = Float64()
			dump_msg = Float64()

			# Increment the position of the end effector rotate joint based on the 
			# Left joystick
			scissor_msg.data = self.scissor_pos + .1*msg.axes[1]

			# Increment the position of the end effector rack joint based on the 
			# Left joystick
			dump_msg.data = self.dump_pos - .15*msg.axes[4]

			# Publish the commands to the joint controlelrs for the dispensing systems
			self.dispense_scissor_pub.publish(scissor_msg)
			self.dispense_dump_pub.publish(dump_msg)

			return


	# Gets the current joint state of the joints on the robot
	def jointStatesCallback(self, msg):
		# Get the indexes of the joints in the message
		self.rotate_idx = msg.name.index("rotate")
		self.rack_idx = msg.name.index("rack")
		self.scissor_idx = msg.name.index("scissor")
		self.dump_idx = msg.name.index("dispense")

		# Update the position of each of the joints
		self.rotate_pos = msg.position[self.rotate_idx]
		self.rack_pos = msg.position[self.rack_idx]
		self.scissor_pos = msg.position[self.scissor_idx]
		self.dump_pos = msg.position[self.dump_idx]

		# print("Rotate: " + str(self.rotate_pos))
		# print("Rack: " + str(self.rack_pos))
		# print("Scissor: " + str(self.scissor_pos))
		# print("Dump: " + str(self.dump_pos))



if __name__ == '__main__':
	# Initialize the node
	rospy.init_node('teleop_node', anonymous=True)

	controller = teleopController()

	# Subscribe to joy topic to get input from controller
	rospy.Subscriber("joy", Joy, controller.velCallback)

	rospy.Subscriber("joint_states", JointState, controller.jointStatesCallback)

	rospy.spin()
