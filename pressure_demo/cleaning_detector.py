import json
import math
import sqlite3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CleaningDetector(Node):
    def __init__(self):
        super().__init__('cleaning_detector')
        self.declare_parameter('reference_pressure_bar', 5.0)
        self.declare_parameter('tolerance_bar', 0.3)
        self.reference = float(
            self.get_parameter('reference_pressure_bar').value
        )
        self.tolerance = float(
            self.get_parameter('tolerance_bar').value
        )
        if not (
            math.isfinite(self.reference) and self.reference > 0
            and math.isfinite(self.tolerance) and self.tolerance >= 0
        ):
            raise ValueError('Invalid reference pressure or tolerance')

        self.last_time = None
        self.last_key = None
        self.count = 0
        self.declare_parameter('db_path', '/ws/pressure_demo/cleaning.db')
        self.db = sqlite3.connect(self.get_parameter('db_path').value)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS point_pressure_suspicions (
                section_id TEXT,
                frame_id TEXT,
                robot_x_m REAL,
                robot_y_m REAL,
                measured_pressure_bar REAL,
                reference_pressure_bar REAL,
                deviation_bar REAL,
                tolerance_bar REAL,
                sim_time_s REAL,
                status TEXT,
                PRIMARY KEY (section_id, frame_id)
            )
        """)
        self.db.commit()
        self.subscription = self.create_subscription(
            String, '/ro/point_pressure', self.on_sample, 10
        )
        self.get_logger().info(
            f'Waiting for pressure data | Reference={self.reference:.2f} '
            f'bar | Tolerance={self.tolerance:.2f} bar'
        )

    def on_sample(self, msg):
        try:
            s = json.loads(msg.data)
            section, frame = s['section_id'], s['frame_id']
            if not all(isinstance(v, str) and v for v in (section, frame)):
                raise ValueError('Invalid section or coordinate frame')
            t, x, y, pressure = [
                float(s[k]) for k in (
                    'sim_time_s', 'robot_x_m', 'robot_y_m', 'pressure_bar'
                )
            ]
            if not all(math.isfinite(v) for v in (t, x, y, pressure)):
                raise ValueError('Invalid numeric data')
            if t < 0 or pressure < 0:
                raise ValueError('Invalid time or pressure')
        except (ValueError, KeyError, TypeError) as error:
            self.count = 0
            self.get_logger().warning(f'Sample rejected: {error}')
            return

        key = (section, frame)
        if self.last_time is not None:
            if t == self.last_time:
                return
            if t < self.last_time or t - self.last_time > 5.0:
                self.count = 0
        if key != self.last_key:
            self.count = 0
        self.last_key, self.last_time = key, t

        deviation = pressure - self.reference
        exceeds = pressure > self.reference + self.tolerance
        self.count = min(self.count + 1, 3) if exceeds else 0

        if self.count < 3:
            self.get_logger().info(
                f'{section} | Pressure={pressure:.2f} bar | '
                f'Deviation={deviation:.2f} bar | '
                f'Consecutive exceedances={self.count}/3'
            )
            return

        with self.db:
            self.db.execute("""
                INSERT INTO point_pressure_suspicions
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(section_id, frame_id) DO UPDATE SET
                    robot_x_m=excluded.robot_x_m,
                    robot_y_m=excluded.robot_y_m,
                    measured_pressure_bar=excluded.measured_pressure_bar,
                    reference_pressure_bar=excluded.reference_pressure_bar,
                    deviation_bar=excluded.deviation_bar,
                    tolerance_bar=excluded.tolerance_bar,
                    sim_time_s=excluded.sim_time_s,
                    status=excluded.status
            """, (
                section, frame, x, y, pressure, self.reference,
                deviation, self.tolerance, t, 'suspected'
            ))

        self.get_logger().warning(
            f'SUSPECTED FOULING: {section} | '
            f'Pressure={pressure:.2f} bar | '
            f'Deviation={deviation:.2f} bar | Saved to database'
        )


def main():
    rclpy.init()
    node = CleaningDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.db.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
