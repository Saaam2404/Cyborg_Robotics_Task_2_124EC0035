#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class take_pos(Node):
    def __init__(self):
        super().__init__("Travel")

        self.PosList=[[1.5,8.5], [8.5, 1.5], [5.197,5.197], [8.5, 8.5], [1.5,1.5], [5.197,5.197]]

        self.ind=0
        self.pose=None
        self.sub_=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.start_time = self.get_clock().now()
        self.cmd_vel_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer=self.create_timer(0.1,self.vel)

    def pose_callback(self,msg):
        self.pose=msg

    def vel(self):

        if self.pose is None:
            return
        

        x=self.pose.x
        y=self.pose.y
        theta=self.pose.theta

        self.get_logger().info(f"x={x:.2f}, y={y:.2f}, θ={theta:.2f}")

        goal_x=self.PosList[self.ind][0]
        goal_y=self.PosList[self.ind][1]

        er_x=goal_x-x
        er_y=goal_y-y
        angle=0
        if(er_x==0 and er_y==0):
            angle=0
        else:
            angle=math.atan2(er_y,er_x)

        dist=math.sqrt(er_x**2 + er_y**2)
        er_ang=angle-theta

        
        twist=Twist()

        if(abs(er_ang)<0.001 and dist<0.001):
            self.get_logger().info(f"Reached location {self.ind + 1}")
            self.ind+=1
            if(self.ind>=len(self.PosList)):
                self.get_logger().info("Travelled all the locations")
                self.destroy_node()

        if(abs(er_ang)<0.001):
            twist.angular.z=0.0
            if(dist>=0.001):
                twist.linear.x=1*dist
            else:
                twist.linear.x=0.0
        else:
            twist.angular.z=0.9*er_ang
            twist.linear.x=0.0

        self.cmd_vel_pub_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node=take_pos()
    rclpy.spin(node)
    rclpy.shutdown()