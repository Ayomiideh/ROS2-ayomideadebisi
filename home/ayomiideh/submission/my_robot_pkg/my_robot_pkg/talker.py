import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):
    def __init__(self):
        super().__init__('talker_node')
        self.publisher = self.create_publisher(String, 'topic', 10)
        # Creating a timer that calls the callback every 2.5 seconds
        self.timer = self.create_timer(2.5, self.publish_info)

    def publish_info(self):
        msg = String()
        msg.data = "Adebisi Ayomide Hannah, Group 06, Matric: 230410010"
        
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = TalkerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()