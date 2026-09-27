cmake_minimum_required(VERSION 3.8)
project(navigation_pkg)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
# find_package(rclcpp REQUIRED)
# find_package(geometry_msgs REQUIRED)

add_executable(move_robot src/move_robot.cpp)
add_executable(stop_robot src/stop_robot.cpp)
add_executable(turn_left src/turn_left.cpp)
add_executable(turn_right src/turn_right.cpp)
add_executable(pid_controller src/pid_controller.cpp)

install(TARGETS
  move_robot
  stop_robot
  turn_left
  turn_right
  pid_controller
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
