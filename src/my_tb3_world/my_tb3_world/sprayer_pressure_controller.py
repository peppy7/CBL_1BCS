import rclpy
from rclpy.node import Node
from msg import SprayerPressure
from msg import Measurement

class SprayerPressureController(Node):
    def __init__(self):
        super().__init__('sprayer_pressure_controller')
        self.latest_measurement = None

        self.target_publisher = self.create_publisher(
            SprayerPressure,
            '/target_sprayer_pressure',
            10
        )

        self.pressure_subscription = self.create_subscription(
            SprayerPressure,
            '/sprayer_pressure',
            self.pressure_callback,
            10
        )

        self.measurement_subscription = self.create_subscription(
            Measurement,
            '/measurement',
            self.measurement_callback,
            10
        )

    def pressure_callback(self, msg):
        self.get_logger().info(
            f'Received pressure: {msg.pressure}, time: {msg.time}'
        )

    def measurement_callback(self, msg):
        if not 0.0 <= msg.pressure <= 1.0:
            self.get_logger().warning(
                'Ignoring cell pressure outside [0, 1]'
            )
            return

        self.latest_measurement = msg

        target = SprayerPressure()
        target.time = msg.time
        target.pressure = 2.0 * (1.0 - msg.pressure)

        self.target_publisher.publish(target)

        self.get_logger().info(
            f'Cell ({msg.cell_x}, {msg.cell_y}), '
            f'cell pressure: {msg.pressure:.2f}, '
            f'target sprayer pressure: {target.pressure:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = SprayerPressureController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()


