# 系统架构

项目最终规划的高层数据流：

```text
Gazebo Fortress 与机器人模型
              ↓
ROS 2 Topic、TF 与里程计
              ↓
slam_toolbox / 地图服务器 / AMCL
              ↓
Nav2 导航栈
              ↓
CampusBot 任务管理器与规划器
              ↓
自动化评测与结果分析
```

当前已实现的基础仿真数据流：

```text
ROS 2 /cmd_vel
       ↓ ros_gz_bridge
Gazebo DiffDrive → 机器人关节与物理运动
       ├── /clock ─────────────→ ROS 2 仿真时间
       ├── Odometry ───────────→ ROS 2 /odom
       ├── Pose_V ─────────────→ ROS 2 /tf（odom → base_footprint）
       ├── Joint State ────────→ ROS 2 /joint_states
       │                              ↓
       │                     robot_state_publisher
       │                              ↓
       │                       左右轮动态 TF
       └── LaserScan ─────────→ ROS 2 /scan
                                      ↓
                              TF 转换与 RViz2 显示
```

其中机器人描述包提供 `base_footprint → base_link → lidar_link` 等固定结构；Gazebo 提供物理运动和传感器数据；Bridge 负责在 Gazebo Transport 与 ROS 2 DDS 之间转换消息。

尚未接入的数据链从 slam_toolbox 开始，包括地图、AMCL、Nav2、自定义任务管理、规划器和自动化评测。
