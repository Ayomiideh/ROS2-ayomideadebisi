#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_action_pkg.action import DoTask
import time

class DoTaskActionServer(Node):
    def __init__(self):
        super().__init__('do_task_action_server')
        self._action_server = ActionServer(
            self,
            DoTask,
            'do_task',
            self.execute_callback
        )
        self.get_logger().info("Action Server is ready!")

    async def execute_callback(self, goal_handle):
        self.get_logger().info(f"Processing task for {goal_handle.request.task_duration} seconds...")
        
        # Send feedback at intervals
        feedback_msg = DoTask.Feedback()
        feedback_msg.progress = 0.0  # Initialize feedback
        total_duration = goal_handle.request.task_duration
        
        for i in range(1, 11):
            feedback_msg.progress = (i / 10.0) * 100  # Progress percentage
            self.get_logger().info(f"Progress: {feedback_msg.progress}%")
            goal_handle.publish_feedback(feedback_msg)
            
            # Distribute progress over duration
            time.sleep(total_duration / 10.0) 
            
        # Complete the action
        goal_handle.succeed()
        result = DoTask.Result()
        result.success = True
        result.message = "Task completed successfully!"
        return result

def main(args=None):
    rclpy.init(args=args)
    node = DoTaskActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()