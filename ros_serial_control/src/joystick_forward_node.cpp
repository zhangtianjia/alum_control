//
// Created by sheep on 19-7-28.
//

#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Bool.h>

std_msgs::Float32 make_std_float32( float data ){
    std_msgs::Float32 rst;
    rst.data = data;
    return rst;
}

std_msgs::Bool make_std_bool( bool data ){
    std_msgs::Bool rst;
    rst.data = data;
    return rst;
}

float remap_control( float val, float start = 0.3 ){

    float v = std::abs(val);

    float sgn = val > 0 ? 1 : -1;

    if ( v > start ) {
        v = (v-start)/(1-start);
    }
    else {
        v = 0;
    }

    return sgn * v;

}

enum class control_mode_e {
    gun_xy,
    gun_z,
};

struct joystick_interpreter_t {

    ros::NodeHandle nh;

    ros::Publisher pub_A1;

    ros::Publisher pub_A2;

    ros::Publisher pub_A3;

    ros::Publisher pub_A4;

    joystick_interpreter_t(){
        pub_A1 = nh.advertise<std_msgs::Float32>("/actuators/A1",1);
        pub_A2 = nh.advertise<std_msgs::Float32>("/actuators/A2",1);
        pub_A3 = nh.advertise<std_msgs::Float32>("/actuators/A3",1);
        pub_A4 = nh.advertise<std_msgs::Bool>("/actuators/A4",1);
    }

    void joy_callback( sensor_msgs::JoyConstPtr const & msg ){

        control_mode_e mode = control_mode_e::gun_xy;

        if ( msg->buttons.at(0) > 0 ) {
            mode = control_mode_e::gun_z;
        }
        else {
            mode = control_mode_e::gun_xy;
        }

        //////////////////////

        if ( mode == control_mode_e::gun_xy ) {
            pub_A1.publish(make_std_float32(remap_control(msg->axes.at(0))));
            pub_A2.publish(make_std_float32(remap_control(msg->axes.at(3))));
        }
        else {
            pub_A1.publish(make_std_float32(remap_control(0)));
            pub_A2.publish(make_std_float32(remap_control(0)));
        }

        /////////////////////

        if ( mode == control_mode_e::gun_z ) {
            pub_A3.publish(make_std_float32(remap_control(msg->axes.at(0))));
        }
        else {
            pub_A3.publish(make_std_float32(remap_control(0)));
        }

        //////////////////////

        pub_A4.publish(make_std_bool(msg->buttons.at(2) > 0));

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