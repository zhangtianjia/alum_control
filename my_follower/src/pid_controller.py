#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from math import copysign
import time

class PID:
    def __init__(self, Kp, Td, Ti, dt):
        self.Kp = Kp
        self.Td = Td
        self.Ti = Ti
        self.curr_error = 0
        self.prev_error = 0
        self.sum_error = 0
        self.prev_error_deriv = 0
        self.curr_error_deriv = 0
        self.control = 0
        self.dt = dt

    def srv_callback(self, config, level):
	    self.Kp = config.Kp
	    self.Td = config.Td
	    self.Ti = config.Ti
	    self.dt = config.dt
    	    return config

    def update_control(self, current_error, reset_prev=False):
        self.curr_error_deriv = (self.curr_error - self.prev_error) / self.dt
        p_gain = self.Kp * self.curr_error

        i_gain = self.sum_error + self.Ti * self.curr_error * self.dt
        self.sum_error = i_gain
        d_gain = self.Td * self.curr_error_deriv

        #PID control
        w = p_gain + d_gain + i_gain # = control?
        self.control = w

        # update error
        self.prev_error = self.curr_error
        self.curr_error = current_error
        self.prev_error_deriv = self.curr_error_deriv
        #print("control", self.control)
        return self.control
class A_controller:
    def __init__(self, actuator_topic, kp, kd, ki, dt, error_topic):
        rospy.on_shutdown(self.shutdown)
        r = rospy.Rate(10)
        self.error=0
        self.max_cmd = 1
        self.min_cmd = 0
        self.threshold = 0.05
        self.command = Float32()
        self.pid_control = PID(kp, kd, ki, dt)
        self.pub_cmd = rospy.Publisher(actuator_topic, Float32, queue_size = 5)
        rospy.wait_for_message(error_topic, Float32)
        rospy.Subscriber(error_topic, Float32, self.set_cmd)
        self.target_reached = False
        #while not self.target_reached:
        while not self.target_reached:
            if abs(self.error) > self.threshold:
                speed = self.pid_control.update_control(self.error)
                self.command.data = copysign(max(self.min_cmd, min(self.max_cmd, abs(speed))), speed)
            else:
                self.target_reached = True
                self.command.data = 0.0
            self.pub_cmd.publish(self.command)
            r.sleep()
    def set_cmd(self, msg):
        self.error = msg.data
    def shutdown(self):
        self.pub_cmd.publish(Float32())

def move_actuator(actuator_topic, duration, speed):
    pub_cmd = rospy.Publisher(actuator_topic, Float32, queue_size = 10)
    data_send = Float32()
    r = rospy.Rate(10)
    data_send.data = speed
    ticks=int(duration*10)
    for i in range(ticks):
        pub_cmd.publish(data_send)
        r.sleep()

    pub_cmd.publish(Float32())



if __name__ == '__main__':
    rospy.init_node('pid_controller')
    #obj3=A_controller('/actuators/A1', 2, 0, 0, 0.1, 'error_input')
    #rospy.spin()
    move_actuator('/actuators/A1', 2, 0.6)


