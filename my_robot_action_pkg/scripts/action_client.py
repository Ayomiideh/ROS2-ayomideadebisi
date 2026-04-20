#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_robot_action_pkg.action import DoTask

class DoTaskActionClient(Node):
    def __init__(self):
        super().__init__('do_task_action_client')
        self._action_client = ActionClient(self, DoTask, 'do_task')

    def send_goal(self, input_value):
        goal_msg = DoTask.Goal()
        goal_msg.task_duration = input_value  # Match field name from DoTask.action
        
        self.get_logger().info("Waiting for action server...")
        self._action_client.wait_for_server()
        
        self.get_logger().info("Sending goal request...")
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected!")
            return

        self.get_logger().info("Goal accepted!")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        # Accessing the 'progress' field defined in your action server
        progress = feedback_msg.feedback.progress
        self.get_logger().info(f"Received feedback: {progress}%")

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Result: {result.message}")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    client = DoTaskActionClient()
    client.send_goal(47)  # Example input value (seconds)
    rclpy.spin(client)

if __name__ == '__main__':
    main()