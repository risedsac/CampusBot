cmake_minimum_required(VERSION 3.8)
project(campusbot_bringup)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch worlds rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
