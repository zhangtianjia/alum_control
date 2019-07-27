#!/usr/bin/env python

import rospy
import struct
import serial
from ros_serial_control.msg import Motor_cmd
import binascii
#import time

def shutdown():
    rospy.loginfo("Stopping")
    publi=rospy.Publisher("motor_pid",Motor_cmd,queue_size=5)
    publi.publish(Motor_cmd())
  

rospy.init_node("pub_example")
rospy.on_shutdown(shutdown)
pub=rospy.Publisher("motor_pid",Motor_cmd,queue_size=5)
motor=Motor_cmd()
motor.motor1_control=-0.2356
motor.motor2_control=-0.2356
motor.motor3_control=-0.2356
while not rospy.is_shutdown():
    pub.publish(motor)
    rospy.sleep(1)


