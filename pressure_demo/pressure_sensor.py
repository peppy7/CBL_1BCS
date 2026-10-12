import json
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from nav_msgs.msg import Odometry
from std_msgs.msg import String


class PressureSensor(Node):
    def __init__(self):
        super().__init__('demo_pressure_sensor')
        self.last_time = None
        self.publisher = self.create_publisher(
            String, '/ro/point_pressure', 10
        )
        self.subscription = self.create_subscription(
            Odometry, '/odom', self.on_position,
            qos_profile_sensor_data
        )
        self.get_logger().info('Waiting for robot position data...')

    def on_position(self, msg):
        t = msg.header.stamp.sec + msg.header.stamp.nanosec / 1e9
        if self.last_time is not None and 0 <= t - self.last_time < 1.0:
            return
        self.last_time = t

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        if not math.isfinite(x) or not math.isfinite(y):
            return

        cell_x = math.floor(x + 0.5)
        cell_y = math.floor(y + 0.5)
        section = f'section_{cell_x}_{cell_y}'

        # Synthetic test model: elevated pressure in section (1, 0).
        pressure = 5.5 if (cell_x, cell_y) == (1, 0) else 5.0

        sample = {
            'source': 'synthetic_demo',
            'section_id': section,
            'frame_id': msg.header.frame_id,
            'sim_time_s': t,
            'robot_x_m': x,
            'robot_y_m': y,
            'pressure_bar': pressure
        }

        output = String()
        output.data = json.dumps(sample)
        self.publisher.publish(output)
        self.get_logger().info(
            f'{section} | x={x:.2f}, y={y:.2f} m | '
            f'Pressure={pressure:.2f} bar'
        )


def main():
    rclpy.init()
    node = PressureSensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
