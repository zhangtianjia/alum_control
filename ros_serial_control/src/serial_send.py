#!/usr/bin/env python

import rospy
import struct
import serial
from ros_serial_control.msg import Motor_cmd
#import binascii
#import time

class serialport_write():
    def __init__(self,port="/dev/ttyUSB0", BaudRate=9600):
        rospy.init_node("serial_send")
        try:
            self.serial=serial.Serial(port, BaudRate)
        except:
            pass
        self.motor1_cmd=0
        self.motor2_cmd=0
        self.motor3_cmd=0
    
        rospy.wait_for_message('motor_pid', Motor_cmd)
        rospy.Subscriber('motor_pid', Motor_cmd, self.send)
    def send(self,motor):
        self.motor1_cmd= int(motor.motor1_control*10000)
        self.motor2_cmd= int(motor.motor2_control*10000)
        self.motor3_cmd= int(motor.motor3_control*10000)
        data1=struct.pack('4B1H2B',02,04,01,01,self.motor1_cmd,13,10)
        data2=struct.pack('4B1H2B',02,04,02,01,self.motor2_cmd,13,10)
        data3=struct.pack('4B1H2B',02,04,03,01,self.motor3_cmd,13,10)
        self.serial.write(data1)
        self.serial.write(data2)
        self.serial.write(data3)

    
if __name__ == '__main__':
    try:
        serialport_write()
        rospy.spin()
    except:
        rospy.loginfo("send node terminated.")

