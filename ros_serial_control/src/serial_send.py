#!/usr/bin/env python

import rospy
import struct
import serial
import binascii
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy

# import time


class AlumSerialInterface:

    def __init__(self, port="/dev/ttyUSB0", BaudRate=9600):
        rospy.loginfo("OK")
        rospy.init_node("serial_send")
        rospy.on_shutdown(self.shutdown)
        try:
            self.serialcon = serial.Serial(port, BaudRate, timeout=10)
        except:
            print("cant open")
            raise
        self.motor_cmd = 0
        self.loop = rospy.Rate(20)
        data = struct.pack('4B1H2B', 01, 04, 01, 01, 00, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))

    def send_A1(self, motor_cmd, motor_sign):
        data = struct.pack('4B1H2B', 01, 04, 01, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
            print("serial send failed!")
            raise

    def send_A2(self, motor_cmd, motor_sign):
        data = struct.pack('4B1H2B', 01, 04, 02, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
            print("serial send failed!")
            raise

    def send_A3(self, motor_cmd, motor_sign):
        data = struct.pack('4B1H2B', 01, 04, 03, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
            print("serial send failed!")
            raise

    def send_A4(self, motor_cmd, motor_sign):
        data = struct.pack('4B1H2B', 01, 04, 04, motor_sign, 0, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
            print("serial send failed!")
            raise

    def shutdown(self):
        rospy.loginfo("Stopping")
        data1 = struct.pack('4B1H2B', 01, 04, 01, 00, 0000, 13, 10)
        data2 = struct.pack('4B1H2B', 01, 04, 02, 00, 0000, 13, 10)
        data3 = struct.pack('4B1H2B', 01, 04, 03, 00, 0000, 13, 10)
        data4 = struct.pack('4B1H2B', 01, 04, 04, 00, 0000, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data1))
        rospy.loginfo(binascii.b2a_hex(data2))
        rospy.loginfo(binascii.b2a_hex(data3))
        rospy.loginfo(binascii.b2a_hex(data4))
        try:
            self.serialcon.write(data1)
            self.serialcon.write(data2)
            self.serialcon.write(data3)
            self.serialcon.write(data4)
            self.serialcon.close()
        except:
            pass


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
        data = struct.pack('4B1H2B', 01, 04, 01, 01, 00, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        #self.serialcon.write(data)
        rospy.wait_for_message('/actuators/A1', Float32)
        rospy.Subscriber('/actuators/A1', Float32, self.send1, queue_size=1)
        rospy.Subscriber('/actuators/A2', Float32, self.send2, queue_size=1)
        #rospy.Subscriber('/actuators/A3', Float32, self.send3, queue_size=5)
        #rospy.Subscriber('/actuators/A4', Float32, self.send4, queue_size=5)

    def send1(self, motor):
        print("A1 called")
        motor_cmd = int(motor.data*800)
        rospy.loginfo(motor_cmd)
        if motor_cmd >= 0:
            motor_sign = 01
        else:
            motor_sign = 0
#       if self.motor_cmd<=3000 & self.motor_cmd>=-3000:
#           x = struct.pack('4B1H2B', 00, 04, 01, 00, 00, 13, 10)
#       else:
#           x = struct.pack('4B1H2B', 00, 04, 01, motor_sign, 00, 13, 10)
        data = struct.pack('4B1H2B', 01, 04, 01, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
#            self.serialcon.write(x)
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
               pass
        self.loop.sleep()

    def send2(self, motor):
        print("A2 called")
        motor_cmd = int(motor.data * 800)
        rospy.loginfo(motor_cmd)
        if motor_cmd >= 0:
            motor_sign = 01
        else:
            motor_sign = 0
            #       if self.motor_cmd<=3000 & self.motor_cmd>=-3000:
            #           x = struct.pack('4B1H2B', 00, 04, 01, 00, 00, 13, 10)
            #       else:
            #           x = struct.pack('4B1H2B', 00, 04, 01, motor_sign, 00, 13, 10)
        data = struct.pack('4B1H2B', 01, 04, 02, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
                #            self.serialcon.write(x)
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
                pass
        self.loop.sleep()
    def send3(self, motor):
        print("A3 called")
        motor_cmd = int(motor.data * 800)
        rospy.loginfo(motor_cmd)
        if motor_cmd >= 0:
            motor_sign = 01
        else:
            motor_sign = 0
            #       if self.motor_cmd<=3000 & self.motor_cmd>=-3000:
            #           x = struct.pack('4B1H2B', 00, 04, 01, 00, 00, 13, 10)
            #       else:
            #           x = struct.pack('4B1H2B', 00, 04, 01, motor_sign, 00, 13, 10)
        data = struct.pack('4B1H2B', 01, 04, 03, motor_sign, abs(motor_cmd), 13, 10)
        rospy.loginfo(binascii.b2a_hex(data))
        try:
                #            self.serialcon.write(x)
            self.serialcon.write(data)
            rospy.loginfo("send successful")
        except:
                pass
        self.loop.sleep()
    def send4(self, motor):
        print("A4 called")
        motor_cmd = motor.data
        rospy.loginfo(motor_cmd)
        if motor_cmd == 0:
            motor_sign = 0
        else:
            motor_sign = 1

        data = struct.pack('4B1H2B', 01, 04, 04, motor_sign, 0, 13, 10)
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
        data1 = struct.pack('4B1H2B', 01, 04, 01, 00, 0000, 13, 10)
        data2 = struct.pack('4B1H2B', 01, 04, 02, 00, 0000, 13, 10)
        data3 = struct.pack('4B1H2B', 01, 04, 03, 00, 0000, 13, 10)
        data4 = struct.pack('4B1H2B', 01, 04, 04, 00, 0000, 13, 10)
        rospy.loginfo(binascii.b2a_hex(data1))
        rospy.loginfo(binascii.b2a_hex(data2))
        rospy.loginfo(binascii.b2a_hex(data3))
        rospy.loginfo(binascii.b2a_hex(data4))
        try:
            self.serialcon.write(data1)
            self.serialcon.write(data2)
            self.serialcon.write(data3)
            self.serialcon.write(data4)
            self.serialcon.close()
        except:
            pass


if __name__ == '__main__':
    try:
        obj = serialport_write()
        rospy.spin()
    except:
        raise