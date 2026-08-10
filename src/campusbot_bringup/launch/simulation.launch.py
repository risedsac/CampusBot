from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
def generate_launch_description():
    #找到xacro文件
    description_xacro_file = PathJoinSubstitution([FindPackageShare("campusbot_description"),
                                                   "urdf","campusbot.urdf.xacro"])

    robot_description = Command(['xacro ',description_xacro_file])

# 下面gazebo_launch_file->gazebo_sim相当于下边终端命令
# ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r empty.sdf"
#
#   但 IncludeLaunchDescription 并不是真的再开一个终端，而是把另一个 Launch 的内容加入当前 Launch 系统统一管理。
#
    gazebo_launch_file = PathJoinSubstitution([
          FindPackageShare("ros_gz_sim"),
          "launch",
          "gz_sim.launch.py",
      ])

    gazebo_sim = IncludeLaunchDescription(
          PythonLaunchDescriptionSource(gazebo_launch_file),
          launch_arguments={
              "gz_args": "-r empty.sdf",
          }.items(),
      )

    robot_state_publisher = Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output = "screen",
            #use_sim_time表示Node使用gazebo仿真时间，而不是电脑时间，防止时间不同步
            parameters=[{"robot_description":robot_description,"use_sim_time": True}]
            )
    spawn_robot = Node(
          package="ros_gz_sim",
          executable="create",
          output="screen",
          arguments=[
              "-name", "campusbot",
              "-topic", "robot_description",
              "-z", "0.02",
          ],
      )
    cmd_vel_bridge= Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            output="screen",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist"
                ]

             )
    return LaunchDescription([gazebo_sim,robot_state_publisher,spawn_robot,cmd_vel_bridge])



