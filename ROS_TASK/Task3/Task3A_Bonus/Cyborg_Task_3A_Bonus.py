#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn


class draw_infinity(Node):
    def __init__(self):
        super().__init__("draw_infinity_two")
        self.pose=None
        self.turtle2_spawned = False
        self.sub_=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.cmd_vel1_pub_=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.cmd_vel2_pub_=self.create_publisher(Twist,"/turtle2/cmd_vel",10)
        self.start_time = self.get_clock().now()
        self.timer=self.create_timer(0.1,self.vel)

    def pose_callback(self,msg):
        self.pos=msg
        if not self.turtle2_spawned:
            self.spawn(msg)
            self.turtle2_spawned=True

    def spawn(self,msg):
        if self.pos is None:
            return
        
        request = Spawn.Request()
        request.x = msg.x
        request.y = msg.y
        request.theta = msg.theta
        request.name = 'turtle2'
        future = self.spawn_client.call_async(request)
        future.add_done_callback(self.spawn_response)
        self.turtle2_spawned=True

    def spawn_response(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Turtle spawned: {response.name}")
        except Exception as e:
            self.get_logger().error(f"Spawn service call failed: {e}")

    

    def vel(self):
        current_time = self.get_clock().now()
        elapsed = (current_time - self.start_time).nanoseconds / 1e9 

        msg1=Twist()
        msg2=Twist()

        #For Turtle1
        if(elapsed<=1.5708):
            msg1.angular.z=-1.0
            msg1.linear.x=0.0
        elif(elapsed<7.854):
            msg1.angular.z=1.0
            msg1.linear.x=1.0
        else:
            msg1.angular.z=0.0
            msg1.linear.x=0.0
        
        #For Turtle2
        if(elapsed<=1.5708):
            msg2.angular.z=1.0
            msg2.linear.x=0.0
        elif(elapsed<7.854):
            msg2.angular.z=1.0
            msg2.linear.x=1.0
        else:
            msg2.angular.z=0.0
            msg2.linear.x=0.0

        self.cmd_vel2_pub_.publish(msg2)
        self.cmd_vel1_pub_.publish(msg1)

def main(args=None):
    rclpy.init(args=args)
    node=draw_infinity()
    rclpy.spin(node)
    rclpy.shutdown()