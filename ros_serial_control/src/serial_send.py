#!/usr/bin/env python

import rospy
import struct
import serial
import numpy
import binascii
from std_msgs.msg import Float32


# import time


class serialport_write():
    def __init__(self, port="/dev/ttyUSB0", BaudRate=9600):
        rospy.loginfo("OK")
        rospy.init_node("serial_send")
        rospy.on_shutdown(self.shutdown)
        try:
            self.serialcon = serial.Serial(port, BaudRate, timeout=10)
            # self.serialcon.open()
        except:
            print("cant open")
            raise
        self.motor_cmd = 0
        self.loop = rospy.Rate(20)
        data = struct.pack('4B1H2B', 00, 04, 01, 01, 200, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        self.serialcon.write(data)
        rospy.wait_for_message('/actuators/A1', Float32)
        rospy.Subscriber('/actuators/A1', Float32, self.send1, queue_size=5)

    def send1(self, motor):
        print("A1 called")
        self.motor_cmd = int(motor.data*100)
        rospy.loginfo(self.motor_cmd)
        if self.motor_cmd >= 0:
            motor_sign = 01
        else:
            motor_sign = 0
#       if self.motor_cmd<=3000 & self.motor_cmd>=-3000:
#           x = struct.pack('4B1H2B', 00, 04, 01, 00, 00, 13, 10)
#       else:
#           x = struct.pack('4B1H2B', 00, 04, 01, motor_sign, 00, 13, 10)
        data = struct.pack('4B1H2B', 01, 04, 01, motor_sign, abs(self.motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
#            self.serialcon.write(x)
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
               pass
        self.loop.sleep()
    def shutdown(self):
        rospy.loginfo("Stopping")
        data = struct.pack('4B1H2B', 01, 04, 01, 00, 0000, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
            self.serialcon.write(data)
            self.serialcon.close()
        except:
            pass


if __name__ == '__main__':
    try:
        obj = serialport_write()
        rospy.spin()
    except:
        raise


# rospy.loginfo("send node terminated.")
