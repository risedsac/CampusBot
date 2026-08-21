from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration,PathJoinSubstitution,Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
def generate_launch_description():
      use_sim_time = LaunchConfiguration('use_sim_time')
      declare_use_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation/Gazebo clock',
            )
      params_file = LaunchConfiguration('params_file')
      default_params_file = PathJoinSubstitution([FindPackageShare("campusbot_navigation"),"config","nav2_params.yaml"])
      declare_params_file = DeclareLaunchArgument(
              'params_file',
              default_value = default_params_file,
              description = 'Use na2 params_file yaml file',
              )
      nav2_launch_file = PathJoinSubstitution(
              [FindPackageShare("nav2_bringup"),
               "launch",
               "navigation_launch.py",
               ]
              )
      start_nav2 = IncludeLaunchDescription(
              PythonLaunchDescriptionSource(nav2_launch_file),
              launch_arguments = {
                  "use_sim_time": use_sim_time,
                  "params_file":  params_file,
                  "autostart": "true",
                }.items(),
              )
      return LaunchDescription([
          declare_use_sim_time,
          declare_params_file,
          start_nav2,
          ])


  
