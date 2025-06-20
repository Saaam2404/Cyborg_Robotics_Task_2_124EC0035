#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tutorial_interfaces.srv import Fibonacci
import sys


class Service(Node):
    def __init__(self):
        super().__init__("Service")
        self.service=self.create_service(Fibonacci,"Fibonacci",self.service_callback)

    def fibonacci_terms(self, x):
        sequence = []
        a, b = 0, 1
        for _ in range(x):
            sequence.append(a)
            a, b = b, a + b
        return sequence

    def service_callback(self,req,response):
        a = req.a
        sequence= self.fibonacci_terms(a)
        response.sequence=sequence
        self.get_logger().info(f"Incoming: {a}")
        self.get_logger().info(f"Fibonacci Sequence: {sequence}")
        return response
    
def main(args=None):
    rclpy.init(args=args)
    node =Service()
    rclpy.spin(node)
    rclpy.shutdown()

