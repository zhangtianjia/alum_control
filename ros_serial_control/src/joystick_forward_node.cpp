//
// Created by sheep on 19-7-28.
//

#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float32.h>

std_msgs::Float32 make_std_float32( float data ){
    std_msgs::Float32 rst;
    rst.data = data;
    return rst;
}

struct joystick_interpreter_t {

    ros::NodeHandle nh;

    ros::Publisher pub_A1;

    ros::Publisher pub_A2;

    joystick_interpreter_t(){
        pub_A1 = nh.advertise<std_msgs::Float32>("/actuators/A1",1);
        pub_A2 = nh.advertise<std_msgs::Float32>("/actuators/A2",1);
    }

    void joy_callback( sensor_msgs::JoyConstPtr const & msg ){
        pub_A1.publish(make_std_float32(msg->axes.at(0)));
        pub_A2.publish(make_std_float32(msg->axes.at(1)));
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