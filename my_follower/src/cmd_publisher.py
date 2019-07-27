#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from math import pi

class OutAndBack():
    def __init__(self):
        # Set rospy to execute a shutdown function when exiting       
        rospy.on_shutdown(self.shutdown)
        
        # Publisher to control the robot's speed
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    def shutdown(self):
        # Always stop the robot when shutting down the node.
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
    def move_linear(self, linear_speed, goal_distance, rate):
	r = rospy.Rate(rate)
            # Initialize the movement command
        move_cmd = Twist()
        # How long should it take us to get there?
        linear_duration = goal_distance / linear_speed
            
            # Set the forward speed
        move_cmd.linear.x = linear_speed
            # Move forward for a time to go the desired distance
        ticks = int(linear_duration * rate)
            
        for t in range(ticks):
            OutAndBack_Object.cmd_vel.publish(move_cmd)
            r.sleep()
            # Stop the robot before the rotation
        move_cmd = Twist()
        OutAndBack_Object.cmd_vel.publish(move_cmd)
        rospy.sleep(1)
    def move_angular(self, angular_speed,angular_distance, rate):
	r = rospy.Rate(rate)
            # Initialize the movement command
        move_cmd = Twist()
        # How long should it take us to get there?
        angular_duration = angular_distance / angular_speed
            
            # Set the forward speed
        move_cmd.angular.z = angular_speed
            # Move forward for a time to go the desired distance
        ticks = int(angular_duration * rate)
            
        for t in range(ticks):
            OutAndBack_Object.cmd_vel.publish(move_cmd)
            r.sleep()
            # Stop the robot before the rotation
        move_cmd = Twist()
        OutAndBack_Object.cmd_vel.publish(move_cmd)
        rospy.sleep(1)


OutAndBack_Object=OutAndBack()
rospy.on_shutdown(OutAndBack_Object.shutdown)
rospy.init_node('cmd_publisher', anonymous=False)
r = rospy.Rate(10)
move_cmd = Twist()
move_cmd.linear.x=0.5
while not rospy.is_shutdown():
    OutAndBack_Object.cmd_vel.publish(move_cmd)
    r.sleep()
