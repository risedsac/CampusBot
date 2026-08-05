cmake_minimum_required(VERSION 3.8)
project(campusbot_task_manager)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(task_status_publisher
    src/task_status_publisher.cpp
  )

  ament_target_dependencies(task_status_publisher
    rclcpp
    std_msgs
  )

  install(TARGETS
    task_status_publisher
    DESTINATION lib/${PROJECT_NAME}
  )
ament_package()
