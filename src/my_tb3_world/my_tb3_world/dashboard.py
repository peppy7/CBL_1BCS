import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.srv import SetInitialPose

from my_tb3_world.pressure_prediction_model import Pressure_prediction_model
from my_tb3_world.global_measurement import Global_measurement
from my_tb3_world.local_measurement import Local_measurement
from measurement_interfaces.msg import Measurement

# has the following tasks:
# TODO: receive pressure data
# TODO: synchronize & adjust sprayer pressure
# TODO: tell physical twin where to go using /navigate_to_pose action from nav2
class Dashboard(Node):

    def __init__(self):
        super().__init__('dashboard')

        # define prediction map
        self.declare_parameter('prediction_map_sizex', 4)
        self.declare_parameter('prediction_map_sizey', 3)
        self.prediction_map = Pressure_prediction_model(
            self.get_parameter('prediction_map_sizex').value,
            self.get_parameter('prediction_map_sizey').value,
            Global_measurement(1.0, 0.0),
            self.get_logger()
        )

        self.timer = self.create_timer(self.prediction_map.delta, self.prediction_map.update)

        #setup service client to send initial pose
        self.client = self.create_client(SetInitialPose, 'set_initial_pose')

        # setup action client for navigate_to_pose
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # setup topic subscriber for measurement
        self.subscriber = self.create_subscription(Measurement, 'measurement', self.measurement_callback, 10)

        # TODO: remove tests
        self.send_initial_pose(0.0, 0.0, 0.0)
        
        self.i = 1
        # self.timer = self.create_timer(1, self.navigation_timer_callback)
        self.send_navigation_goal(1.0, 0.0, 0.0)

    def measurement_callback(self, msg):
        self.get_logger().info(f'measurement: {msg}')
        if msg.cell_x == -1 and msg.cell_y == -1:
            self.prediction_map.handle_global_measurement(
                Global_measurement(msg.pressure, msg.time)
            )
        else:
            self.prediction_map.handle_local_measurement(
                Local_measurement(msg.pressure, msg.time, msg.cell_x, msg.cell_y)
            )

    def navigation_timer_callback(self):
        self.send_navigation_goal(1.0, 0.0, 0.0)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
        newGoal = self.prediction_map.get_cleaning_goal()
        self.send_navigation_goal(
            float(newGoal.x),
            float(newGoal.y),
            0.0
            )

    def send_initial_pose(self, x, y, z):
        request = SetInitialPose.Request()

        # Set request header
        request.pose.header.frame_id = "map"
        request.pose.header.stamp = self.get_clock().now().to_msg()

        #set request pose
        request.pose.pose.pose.position.x = x
        request.pose.pose.pose.position.y = y
        request.pose.pose.pose.position.z = z
        request.pose.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'sending initial pose x:{x}, y:{y}, z:{z}')
        
        self.client.call_async(request)
    
    # navigate_to_pose goal sender
    def send_navigation_goal(self, x, y, w):
        self.get_logger().info(f'Sending {self.i}th navigation goal: x:{x}, y:{y}, w:{w}')
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = w

        self.i += 1

        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        
        self.get_logger().info('Waiting on feedback')
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