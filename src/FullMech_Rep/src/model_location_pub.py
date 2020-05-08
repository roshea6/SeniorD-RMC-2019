#!/usr/bin/env python

"""
Description: Node to listen for gazebo model states messages, parse them for the robot model, 
and then publish its positions to proper odom topic

Authors: Ryan

"""

import rospy
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
import copy
import tf

# Callback function for the gazebo model states
def modelCallback(states_msg):
    # odom publisher
    odom_pub = rospy.Publisher('/diffdrive_controller/good_odom', Odometry, queue_size=1)

    # Get the index of the robot model in the gazebo model state message
    # This index will be used to get the pose from the list of poses in the msg
    idx = states_msg.name.index("FullMech_Rep")

    # Create a new odom message
    odom = Odometry()

    # Populate the header with time and frame ids
    odom.header.stamp = rospy.Time.now()
    odom.header.frame_id = "good_odom"
    odom.child_frame_id = "drivetrain"

    # Get the pose of the model 
    odom.pose.pose = copy.deepcopy(states_msg.pose[idx])

    odom.pose.covariance = []

    # Fill in the position covariance. Based off the default values in the diffdrive config file
    for i in range(0, 36):
        if i % 6 == 0 and i < 35:
            odom.pose.covariance.append(0.001)
        elif i == 35:
            odom.pose.covariance.append(0.3)
        else:
            odom.pose.covariance.append(0.0)

    # Get the velocity of the model
    odom.twist.twist = copy.deepcopy(states_msg.twist[idx])

    odom.twist.covariance = []

    # Fill in the velocity covariance. Based off the default values in the diffdrive config file
    for i in range(0, 36):
        if i % 6 == 0 and i < 35:
            odom.twist.covariance.append(0.001)
        elif i == 35:
            odom.twist.covariance.append(0.3)
        else:
            odom.twist.covariance.append(0.0)

    odom_pub.publish(odom)

    # Transform broadcaster to broadcast the transform between good odom and the drivetrain
    br = tf.TransformBroadcaster()

    # Publish the transform
    # We kinda cheat here and just use the model state as the transform but it works
    br.sendTransform((odom.pose.pose.position.x, odom.pose.pose.position.y, odom.pose.pose.position.z), 
        (odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w),
        rospy.Time.now(),
        "drivetrain",
        "good_odom")

if __name__ == '__main__':
    # Initialize the node
    rospy.init_node('model_location_pub', anonymous=True)

    # Subscribe to the Gazebo model states topic
    rospy.Subscriber("/gazebo/model_states", ModelStates, modelCallback)

    rospy.spin()