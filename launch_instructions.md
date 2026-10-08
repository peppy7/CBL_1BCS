For all the below, first open docker then for each new terminal open a WSL terminal

**launch initial simulation**
(assumes you have already setup everything)
docker run --rm -it --name turtlebot3_container --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/c2irr10/turtlebot3_ws:/ws --user $(id -u):$(id -g) turtlebot3_ws bash
cd /ws
source /opt/ros/jazzy/setup.bash
source /opt/install/setup.bash
colcon build
source install/setup.bash
export TURTLEBOT3_MODEL=burger

**run initial gazebo simulation**
ros2 launch my_tb3_world new_world.launch.py

now from here for any extra programs we attach a terminal and run or launch it

**attach second terminal**
docker exec -it turtlebot3_container bash
cd /ws
source install/setup.bash
export TURTLEBOT3_MODEL=burger

**list of important run/launch commands**
ros2 run rqt_graph rqt_graph
ros2 run turtlebot3_teleop teleop_keyboard
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
