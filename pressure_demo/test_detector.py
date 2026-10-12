import json
import tempfile
from pathlib import Path

import rclpy
from std_msgs.msg import String
from cleaning_detector import CleaningDetector

with tempfile.TemporaryDirectory() as folder:
    db_path = str(Path(folder) / "test.db")
    rclpy.init(args=["--ros-args", "-p", f"db_path:={db_path}"])
    node = CleaningDetector()

    def sample(t, pressure):
        msg = String()
        msg.data = json.dumps({
            "section_id": "section_1_0",
            "frame_id": "odom",
            "sim_time_s": t,
            "robot_x_m": 0.7,
            "robot_y_m": 0.0,
            "pressure_bar": pressure
        })
        node.on_sample(msg)

    def count():
        return node.db.execute(
            "SELECT COUNT(*) FROM point_pressure_suspicions"
        ).fetchone()[0]

    try:
        for t in (1, 2, 3):
            sample(t, 5.0)
        assert count() == 0, "Temiz durumda kayıt oluştu"
        print("PASS: Temiz durumda kayıt yok")

        sample(4, 5.5)
        sample(5, 5.5)
        assert count() == 0, "Üç ölçüm tamamlanmadan kayıt oluştu"
        print("PASS: İlk iki aşımda kayıt yok")

        sample(6, 5.5)
        row = node.db.execute(
            "SELECT section_id, measured_pressure_bar, status "
            "FROM point_pressure_suspicions"
        ).fetchall()
        assert row == [("section_1_0", 5.5, "suspected")], row
        print("PASS: Üçüncü aşımda doğru SQLite kaydı oluştu")

        sample(7, 5.5)
        assert count() == 1, "Aynı bölge için mükerrer kayıt oluştu"
        print("PASS: Aynı bölge için mükerrer kayıt yok")
        print("TUM TESTLER GECTI")
    finally:
        node.db.close()
        node.destroy_node()
        rclpy.shutdown()
