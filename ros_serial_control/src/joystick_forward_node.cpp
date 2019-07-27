//
// Created by sheep on 19-7-28.
//

#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float32.h>

struct joystick_interpreter_t {

    ros::NodeHandle nh;

    ros::Publisher pub_A1;

    joystick_interpreter_t(){
        pub_A1 = nh.advertise<std_msgs::Float32>("/actuators/A1",1);
    }

    void joy_callback( sensor_msgs::JoyConstPtr const & msg ){
        std_msgs::Float32 out;
        out.data = msg->axes.front();
        pub_A1.publish(out);
    }

};



int main( int argc, char** argv ) {

    ros::init(argc,argv,"joystick_forward_node");

    joystick_interpreter_t interpreter;

    ros::NodeHandle nh;

    ros::Subscriber sub = nh.subscribe<sensor_msgs::Joy>("/joy",1,&joystick_interpreter_t::joy_callback,&interpreter);

    ros::spin();
    
    return 0;

}