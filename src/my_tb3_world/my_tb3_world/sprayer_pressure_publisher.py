import rclpy
from rclpy.node import Node
from msg import SprayerPressure


class SprayerPressurePublisher(Node):
    def __init__(self):
        super().__init__('sprayer_pressure_publisher')

        self.publisher_ = self.create_publisher(
            SprayerPressure,
            '/sprayer_pressure',
            10
        )

        self.timer = self.create_timer(1.0, self.publish_pressure)

    def publish_pressure(self):
        msg = SprayerPressure()
        msg.time = self.get_clock().now().nanoseconds / 1e9
        msg.pressure = 1.0

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SprayerPressurePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()