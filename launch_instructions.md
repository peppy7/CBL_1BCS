For all the below, first open docker then for each new terminal open a WSL terminal

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
```
ros2 run rqt_graph rqt_graph
ros2 run turtlebot3_teleop teleop_keyboard
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```
