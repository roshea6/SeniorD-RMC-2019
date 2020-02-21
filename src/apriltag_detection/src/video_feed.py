#!/usr/bin/env python

import cv2 
import rospy 
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

if __name__ == '__main__':
	# Initialize the node
	rospy.init_node('video_feed_node', anonymous=True)

	# Define the publisher object
	vid_pub = rospy.Publisher('/camera_img', CompressedImage, queue_size=1)

	# Open the web camera
	camera = cv2.VideoCapture(1)

	while(1):
		# Grab a frame from the webcam
		ret, cv_img = camera.read()

		cv2.imshow("Camera img", cv_img)
		key = cv2.waitKey(1)

		if key == ord('q'):
			break

		# CvBridge object for converting from cv images to ROS images
		bridge = CvBridge()

		# Convert to a ROS message
		# ros_img = bridge.cv2_to_imgmsg(cv_img, 'bgr8')

		ros_img = CompressedImage()
		ros_img.header.stamp = rospy.Time.now()
		ros_img.format = "jpeg"
		ros_img.data = np.array(cv2.imencode('.jpg', cv_img)[1]).tostring()

		# Publish a ROS message to the topic
		vid_pub.publish(ros_img)