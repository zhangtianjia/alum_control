#!/usr/bin/env python

import rospy
import struct
import serial
from ros_serial_control.msg import Motor_cmd
import binascii
#import time

class serialport_write():
    def __init__(self,port="/dev/ttyUSB0", BaudRate=9600):
        rospy.init_node("serial_send")
        try:
            self.serialcon=serial.Serial(port, BaudRate, timeout=10)
            #self.serialcon.open() 
	except:
            print("cant open")
	    raise
        self.motor1_cmd=0
        self.motor2_cmd=0
        self.motor3_cmd=0
        data=struct.pack('4B1H2B',00,04,01,01,800,13,10)
        rospy.loginfo(binascii.b2a_hex(data))
	self.serial_con.write(data)      
        rospy.wait_for_message('motor_pid', Motor_cmd)
        rospy.Subscriber('motor_pid', Motor_cmd, self.send)

    def send(self,motor):
        print("called")
        self.motor1_cmd= int(motor.motor1_control*10000)
	rospy.loginfo(self.motor1_cmd)
        self.motor2_cmd= int(motor.motor2_control*10000)
        self.motor3_cmd= int(motor.motor3_control*10000)
        if self.motor1_cmd>=0:
	    motor1_sign=01
	else:
            motor1_sign=0
        if self.motor2_cmd>=0:
            motor2_sign=01
	else:
	    motor2_sign=0
	if self.motor3_cmd>=0:
	    motor3_sign=01
	else:
	    motor3_sign=00
        data1=struct.pack('4B1H2B',01,04,01,motor1_sign,abs(self.motor1_cmd),13,10)  
	rospy.loginfo(binascii.b2a_hex(data1))
        data2=struct.pack('4B1H2B',01,04,02,motor2_sign,abs(self.motor2_cmd),13,10)
        data3=struct.pack('4B1H2B',01,04,03,motor3_sign,abs(self.motor3_cmd),13,10)
	try:
            self.serial_con.write(data1)
            self.serial_con.write(data2)
            self.serial_con.write(data3)
	except:
	    pass
    
if __name__ == '__main__':
    try:
        obj = serialport_write()
        rospy.spin()
    except:
	raise        
#rospy.loginfo("send node terminated.")

