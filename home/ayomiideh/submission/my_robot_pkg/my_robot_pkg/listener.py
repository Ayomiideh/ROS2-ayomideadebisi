import rclpy 
from rclpy.node import Node 
from std_msgs.msg import String 
class ListenerNode(Node): 
    def __init__(self): 
        super().__init__('listener_node') 
        self.subscription = self.create_subscription( 
            String, 
            'group_info',  # Topic name 
            self.listener_callback, 
            10) 
        self.subscription  # Prevent unused variable warning 
 
    def listener_callback(self, msg): 
        self.get_logger().info(f'Received: {msg.data}') 
 
def main(args=None): 
    rclpy.init(args=args) 
    node = ListenerNode() 
    rclpy.spin(node)  # Keep the node running 
    node.destroy_node() 
    rclpy.shutdown() 
 
if __name__ == '__main__': 
    main()