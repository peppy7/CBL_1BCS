import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

# has the following tasks:
# receive pressure data
# synchronize & adjust sprayer pressure
# tell physical twin where to go using /navigate_to_pose action from nav2
class Dashboard(Node):

    def __init__(self):
        super().__init__('dashboard')

        # setup action client for navigate_to_pose
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # TODO: remove test
        # tell robot to go to (x,y,w) = (4, 4, 1)
        self.send_navigation_goal(4, 4, 1)
    
    # navigate_to_pose goal sender
    def send_navigation_goal(self, x, y, w):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = w

        self.get_logger().info(f'Sending navigation goal: x:{x}, y:{y}, w:{w}')

        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        return future

    # print out all feedback
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

def main(args=None):
    rclpy.init(args=args)

    dashboard = Dashboard()

    rclpy.spin(dashboard)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    dashboard.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()