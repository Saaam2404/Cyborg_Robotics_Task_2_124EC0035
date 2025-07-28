import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import math
from tf_transformations import euler_from_quaternion

class Task2B_controller(Node):
    def __init__(self):
        super().__init__("Control")
        self.sub_=self.create_subscription(Odometry,"/odom",self.odom_callback,10)
        self.pub_=self.create_publisher(Twist,"/cmd_vel",10)
        self.pose=None
        self.timer=self.create_timer(0.1,self.vel)
        self.cnt=0
        self.goal_x=None
        self.goal_y=None
        self.check=0

        self.shape=0

        self.sqr_side=5.0
        self.sqr_ang=1.57
        self.state="move_forward"
        self.start_theta=None
        self.turn=0
    
    def odom_callback(self,msg):
        self.pose=msg.pose.pose

    def normalize_angle(self, angle):
        while angle>math.pi:
            angle-=2*math.pi
        while angle<-math.pi:
            angle+=2*math.pi
        return angle

    
    def vel(self):
        if self.pose is None:
            return
        
        x=self.pose.position.x
        y=self.pose.position.y
        q=self.pose.orientation
        (r,p,theta)=euler_from_quaternion([q.x,q.y,q.z,q.w])

        twist=Twist()

        if(self.cnt<1):
            self.goal_x=x
            self.goal_y=y
            self.cnt+=1
        er_x=self.goal_x-x
        er_y=self.goal_y-y
        dist=math.sqrt((er_x**2)+(er_y**2))


        
        
        self.get_logger().info(f"goal_x={self.goal_x:.2f},goal_y={self.goal_y:.2f}")
        self.get_logger().info(f"x={x:.2f},goal_y={y:.2f}")
        self.get_logger().info(f"dist={dist:.2f}")

        if(self.shape==0):

            #----Moving in a circle----

            self.get_logger().info(f"---moving in a circle---")
            if(dist>0.09):
                self.check+=1
            if(dist<0.09 and self.check>1):
                twist.angular.z=0.0
                twist.linear.x=0.0
                self.shape+=1
            else:
                twist.angular.z=0.9
                twist.linear.x=0.4
            
            self.pub_.publish(twist)
        
        elif(self.shape==1):

            #----Moving in a square----
            if(self.turn>3):
                self.shape+=1

            self.get_logger().info(f"---moving in a square---")
            if(dist<self.sqr_side):
                twist.linear.x=0.4
                twist.angular.z=0.0
            else:
                if(self.state!="rotate"):
                    self.start_theta=theta
                    self.state="rotate"
                else:
                    del_theta=self.normalize_angle(self.start_theta-theta)
                    if(abs(del_theta)<math.pi/2):
                        twist.linear.x=0.0
                        twist.angular.z=0.9
                    else:
                        self.goal_x=x
                        self.goal_y=y
                        self.state="move_forward"
                        self.turn+=1
                        
            self.pub_.publish(twist)
        
        else:
            twist.linear.x=0.0
            twist.angular.z=0.0
            self.pub_.publish(twist)

    
def main(args=None):
    rclpy.init(args=args)
    node=Task2B_controller()
    rclpy.spin(node)
    rclpy.shutdown()