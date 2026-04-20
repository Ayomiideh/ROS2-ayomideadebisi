#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

def main():
    rclpy.init()
    
    # Check if arguments are provided to avoid index errors
    if len(sys.argv) < 3:
        print("Usage: ros2 run <pkg_name> <node_name> <a> <b>")
        return

    node = AddTwoIntsClient()
    
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        response = node.send_request(a, b)
        node.get_logger().info(f"Result: {a} + {b} = {response.sum}")
    except ValueError:
        node.get_logger().error("Arguments must be integers")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()