#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_tb3_world',
            executable='dashboard',
            name='db',
            output='screen',
            parameters=[],
        ),
        Node(
            package='my_tb3_world',
            executable='subscriber',
            name='sub',
            output='screen',
            parameters=[],
        )s
    ])