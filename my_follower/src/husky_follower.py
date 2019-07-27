#!/usr/bin/env python

""" timed_out_and_back.py - Version 1.2 2014-12-14

    A basic demo of the using odometry data to move the robot along
    and out-and-back trajectory.

    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2012 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
      
"""

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
# Give the node a name
rospy.init_node('out_and_back', anonymous=False)

# Set rospy to execute a shutdown function when exiting       
rospy.on_shutdown(OutAndBack_Object.shutdown)
        
        # How fast will we update the robot's movement?
rate = 50
        
linear_speed=0.2
angular_speed=-0.15
goal_distance_1=1
angular_distance=-pi/2
OutAndBack_Object.move_linear(linear_speed, goal_distance_1, rate)
OutAndBack_Object.move_angular(angular_speed, angular_distance, rate)
#OutAndBack_Object.move_linear(linear_speed, goal_distance_1, rate)
#OutAndBack_Object.move_angular(angular_speed, angular_distance, rate)
#OutAndBack_Object.move_linear(linear_speed, goal_distance_1, rate)
#OutAndBack_Object.move_angular(angular_speed, angular_distance, rate)
#OutAndBack_Object.move_linear(linear_speed, goal_distance_1, rate)
#OutAndBack_Object.move_angular(angular_speed, angular_distance, rate)


