#!/usr/bin/env python3

import rclpy
import sys
from rclpy.node import Node
from tutorial_interfaces.srv import Fibonacci

class Client(Node):
    def __init__(self):
        super().__init__("Client")
        self.get_logger().info("Fibonacci Client is ready")
        self.client=self.create_client(Fibonacci,"Fibonacci")
        while not self.client.wait_for_service(timeout_sec=1):
            self.get_logger().info("Waiting for response")
        self.req=Fibonacci.Request()

    def send_request(self):
        self.req.a=int(sys.argv[1])
        self.future=self.client.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    node=Client()
    node.send_request()
    rclpy.spin(node)
    if node.future.result() is not None:
        print('Fibonacci sequence:', node.future.result().sequence)
    else:
        print("Failed")
    rclpy.shutdown()