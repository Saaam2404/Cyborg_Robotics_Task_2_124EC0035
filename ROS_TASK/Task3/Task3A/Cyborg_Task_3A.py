#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class draw_circle(Node):
    def __init__(self):
        super().__init__("drawinfinity")
        self.start_time = self.get_clock().now()
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer=self.create_timer(0.1,self.vel)
    def vel(self):
        current_time = self.get_clock().now()
        elapsed = (current_time - self.start_time).nanoseconds / 1e9 

        msg=Twist()
        if(elapsed<0.5236):
            msg.linear.x=0.0
            msg.angular.z=-1.0
        elif(elapsed<3.5236):
            msg.linear.x=1.0
            msg.angular.z=0.0
        elif(elapsed<7.736):
            msg.linear.x=1.0
            msg.angular.z=1.0
        elif(elapsed<11.1):
            msg.linear.x=1.0
            msg.angular.z=0.0
        elif(elapsed<16.114):
            msg.linear.x=1.0
            msg.angular.z=-1.0
        else:
            msg.linear.x=0.0
            msg.angular.z=0.0


        self.cmd_vel_pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node=draw_circle()
    rclpy.spin(node)
    rclpy.shutdown()