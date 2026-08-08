from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    task_status_publisher = Node(
            package="campusbot_task_manager",
            executable="task_status_publisher",
            output="screen",
            parameters=[{"publish_period_ms":500}]
            )
    task_status_subscriber = Node(
            package = "campusbot_task_manager",
            executable = "task_status_subscriber",
            output = "screen",
            )
    launch_description = LaunchDescription([task_status_publisher,task_status_subscriber])
    return launch_description
