cmake_minimum_required(VERSION 3.8)
project(sprayer_gazebo)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sprayer_interfaces REQUIRED)

find_package(gz_sim_vendor REQUIRED)
find_package(gz-sim8 REQUIRED)

find_package(gz_plugin_vendor REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)

add_library(SprayerSystem SHARED
  src/SprayerSystem.cpp
)

target_compile_features(SprayerSystem PUBLIC cxx_std_17)

ament_target_dependencies(SprayerSystem
  rclcpp
  sprayer_interfaces
)

target_link_libraries(SprayerSystem
  gz-sim8::gz-sim8
  gz-plugin2::register
)

install(
  TARGETS SprayerSystem
  LIBRARY DESTINATION lib
)

ament_package()