#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
import cv2
import numpy as np
import math
import cv2.aruco as aruco

class Task2C_controller(Node):
    def __init__(self):
        super().__init__("Control")
        self.sub_=self.create_subscription(Image,"/camera/image_raw",self.image_callback,10)
        self.convert=CvBridge()
        self.pub_=self.create_publisher(Pose2D,"/bot_pose",10)
        self.twist_=self.create_publisher(Twist,"/cmd_vel",10)
        self.timer=self.create_timer(0.5,self.vel)
        self.count=0
        self.draw_=self.create_publisher(Bool,"/draw",10)
        self.draw_bool=False
    
    def image_callback(self,msg):
        try:
            image=self.convert.imgmsg_to_cv2(msg,desired_encoding="bgr8")
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            dict=aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
            parameter=aruco.DetectorParameters()
            detector=aruco.ArucoDetector(dict,parameter)
            corners,ids,reject_img=detector.detectMarkers(gray)
            if ids is not None:
                for i in range(len(ids)):
                    if(ids[i][0]==1):
                        marked_corner=corners[i][0]

                        centre_x=np.mean(marked_corner[:,0])
                        centre_y=np.mean(marked_corner[:,1])

                        del_x=marked_corner[1][0]-marked_corner[0][0]
                        del_y=marked_corner[1][1]-marked_corner[0][1]
                        theta=math.atan2(del_y,del_x)

                        pose=Pose2D()
                        

                        pose.x=float(centre_x)
                        pose.y=float(centre_y)
                        pose.theta=float(theta)
                        self.pub_.publish(pose)
                        self.get_logger().info(f"x={pose.x},y={pose.y},theta={pose.theta}")

                        id_img=aruco.drawDetectedMarkers(image,[corners[i]],ids[i],(255,0,14))
                        cv2.imshow("image",id_img)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().info(f"Image can't be loaded {e}")
    
    def vel(self):
        twist=Twist()
        draw_bool=Bool()
        if(self.count<1):
            twist.linear.x=0.0
            twist.angular.z=0.0
            draw_bool.data=False

        elif(self.count>200):
            twist.linear.x=0.0
            twist.angular.z=0.0
            draw_bool.data=False
        
        else:
            twist.linear.x=0.005*self.count
            twist.angular.z=3.0
            draw_bool.data=True
        
        self.count+=1
        self.twist_.publish(twist)
        self.draw_.publish(draw_bool)

def main(args=None):
    rclpy.init(args=args)
    node=Task2C_controller()
    rclpy.spin(node)
    rclpy.shutdown()

