import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    demo_dir = os.path.dirname(os.path.abspath(__file__))
    world_launch = os.path.join(
        get_package_share_directory('my_tb3_world'),
        'launch', 'new_world.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(world_launch)
        ),
        ExecuteProcess(
            cmd=[sys.executable, '-u',
                 os.path.join(demo_dir, 'cleaning_detector.py')],
            cwd=demo_dir,
            output='screen'
        ),
        ExecuteProcess(
            cmd=[sys.executable, '-u',
                 os.path.join(demo_dir, 'pressure_sensor.py')],
            cwd=demo_dir,
            output='screen'
        ),
    ])
