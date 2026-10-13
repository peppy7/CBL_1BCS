This repo contains the /src folder

<h1>Launch instructions</h1>
For all the below, first open docker then for each new terminal open a WSL terminal OR use a linux enviroment and open terminals there.

**launch initial simulation**
(we assume you are already have gazebo and ros2 jazzy setup)
``` bash
cd /ws
source /opt/ros/jazzy/setup.bash
source /opt/install/setup.bash
colcon build
source install/setup.bash
export TURTLEBOT3_MODEL=burger
```

**run initial gazebo simulation**
``` bash
ros2 launch my_tb3_world new_world.launch.py
```
now from here for any extra programs we attach a terminal and run or launch it

**attach second terminal**
open a second terminal and attach to the docker container if needed
``` bash
cd /ws
source install/setup.bash
export TURTLEBOT3_MODEL=burger
```
Now we are in the ros2 enviroment

**list of important run/launch commands**
runs rqt_graph, visualizes nodes and topics.
```
ros2 run rqt_graph rqt_graph
```

runs teleop for keyboard control of the robot
```
ros2 run turtlebot3_teleop teleop_keyboard
```

launches nav2, required for navigation
```
ros2 launch nav2_bringup bringup_launch.py map:=map.yaml use_sim_time:=True
```

launches rviz
```
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```
