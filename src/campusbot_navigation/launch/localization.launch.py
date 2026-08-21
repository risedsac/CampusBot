from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration,PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation/Gazebo clock',
            )
    map_file = LaunchConfiguration('map')
    default_map_file = PathJoinSubstitution([FindPackageShare("campusbot_navigation"),"maps","campus_map.yaml"])
    declare_map = DeclareLaunchArgument(
            'map',
            default_value=default_map_file,
            description='Use map yaml file',
            )
    amcl_params_file = LaunchConfiguration('params_file')
    default_amcl_params_file = PathJoinSubstitution([FindPackageShare("campusbot_navigation"),"config","amcl_params.yaml"])
    declare_amcl_params_file = DeclareLaunchArgument(
            'params_file',
            default_value =default_amcl_params_file,
            description='Use amcl params file',
            )
    map_server = Node(
            parameters=[
                {
                    "yaml_filename": map_file,
                    "use_sim_time": use_sim_time
                },
                ],
            package = "nav2_map_server",
            executable="map_server",
            name="map_server",
            output = "screen",
            )
    lifecycle_manager = Node(
            package = "nav2_lifecycle_manager",
            executable= "lifecycle_manager",
            name="lifecycle_manager_localization",
            output="screen",
            parameters = [
                {
                    "use_sim_time": use_sim_time,
                    "autostart": True,
                    "node_names": ["map_server","amcl"],


                    }
                ]
            )
    amcl = Node(
            package = "nav2_amcl",
            executable = "amcl",
            name="amcl",
            output="screen",
            parameters = [
                amcl_params_file,
                {"use_sim_time": use_sim_time},
                ]

            )
    return LaunchDescription(
            [declare_use_sim_time,
             declare_map,
             declare_amcl_params_file,
             map_server,
             amcl,
             lifecycle_manager]


            )

