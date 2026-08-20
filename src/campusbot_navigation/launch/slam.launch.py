from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import  PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation/Gazebo clock',
        )
    slam_config_file = PathJoinSubstitution([FindPackageShare("campusbot_navigation"),"config","slam_params.yaml"])
    start_slam_box = Node(
            parameters=[
               slam_config_file,
               {"use_sim_time": use_sim_time}],

            package = "slam_toolbox",
            executable = "async_slam_toolbox_node",
            name = "slam_toolbox",
            output = "screen",

            )
    return LaunchDescription([declare_use_sim_time,start_slam_box])



