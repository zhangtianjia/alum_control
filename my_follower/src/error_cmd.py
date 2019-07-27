#!/usr/bin/env python

"""
    ar_follower.py - Version 1.0 2013-08-25
    
    Follow an AR tag published on the /ar_pose_marker topic.  The /ar_pose_marker topic
    is published by the ar_track_alvar package
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2013 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
"""

import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Twist


class ARFollower():
    def __init__(self):
        rospy.init_node("ar_follower")
                        
        # Set the shutdown function (stop the robot)
        rospy.on_shutdown(self.shutdown)
        
        # How often should we update the robot's motion?
        self.rate = rospy.get_param("~rate", 10)
        r = rospy.Rate(self.rate) 
        rospy.loginfo("target_offset_y = %s",self.rate)
        # Publisher to control the robot's movement
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        
        # Intialize the movement command
        self.move_cmd = Twist()
        self.goal_x=0.6
        # How much do we weight the goal distance (x) when making a movement
        self.x_scale = rospy.get_param("~x_scale", 1.0)

        # How much do we weight y-displacement when making a movement        
        self.y_scale = rospy.get_param("~y_scale", 1.0)
        
        # Set flag to indicate when the AR marker is visible
        self.target_visible = False
        
        # Wait for the ar_pose_marker topic to become available
        rospy.loginfo("Waiting for ar_pose_marker topic...")
        rospy.wait_for_message('ar_pose_marker', AlvarMarkers)
        
        # Subscribe to the ar_pose_marker topic to get the image width and height
        rospy.Subscriber('ar_pose_marker', AlvarMarkers, self.set_cmd_vel)

        

	rospy.loginfo("Marker messages detected. Starting follower...")
        
        # Begin the cmd_vel publishing loop
        while not rospy.is_shutdown():
            # Send the Twist command to the robot
            self.cmd_vel_pub.publish(self.move_cmd)

            
            # Sleep for 1/self.rate seconds
            r.sleep()
    	

    def set_cmd_vel(self, msg):
        # Pick off the first marker (in case there is more than one)
        try:
            marker = msg.markers[0]
        except:
            return
                
        # Get the displacement of the marker relative to the base
        target_offset_y = marker.pose.pose.position.y
        
        # Get the distance of the marker from the base
        target_offset_x = marker.pose.pose.position.x
        
        # Rotate the robot only if the displacement of the target exceeds the threshold
            # Set the rotation speed proportional to the displacement of the target
        speed = target_offset_y * self.y_scale

        self.move_cmd.angular.z = speed
 

        speed = target_offset_x
        self.move_cmd.linear.x = speed
        rospy.loginfo("move_cmd.linear.x %s",self.move_cmd.linear.x)

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)     

if __name__ == '__main__':
    try:
        ARFollower()
	rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AR follower node terminated.")

