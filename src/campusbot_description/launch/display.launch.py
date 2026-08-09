from launch import LaunchDescription, launch_description
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch_ros.actions import  Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command
def generate_launch_description():
    #找到xacro文件
    description_xacro_file = PathJoinSubstitution([FindPackageShare("campusbot_description"),
                                                   "urdf","campusbot.urdf.xacro"])
    
    xacro_output = Command(['xacro ',description_xacro_file])
    robot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output = "screen",
            parameters=[{"robot_description":xacro_output}]
            )
    launch_description=LaunchDescription([robot_state_publisher])
    return launch_description




