# CampusBot

CampusBot: ROS2 Autonomous Navigation and Benchmark System

CampusBot 是一个面向学习与工程实践的 ROS 2 移动机器人项目，计划完成差速机器人仿真、建图、定位导航、自定义路径规划、任务管理和自动化评测。

## 当前状态

- 阶段：第一阶段，差速机器人基础仿真与传感器链路
- 环境：Linux Mint 21.3（Ubuntu 22.04 Jammy 基础）、ROS 2 Humble、Gazebo Fortress
- 已完成：C++ Topic 通信、Parameter 与 Launch、差速机器人模型、Gazebo 物理仿真、速度控制、仿真时间、里程计、TF、Joint State 和二维激光雷达
- 当前能力：使用顶层 Launch 启动仿真，通过 ROS 2 `/cmd_vel` 控制机器人，并在 RViz2 中显示 RobotModel 与 `/scan`
- 尚未完成：可复用 RViz2 配置、完整建图场景、slam_toolbox、Nav2 集成、任务管理 Action、自定义规划器和自动化评测

## 构建

```bash
source /opt/ros/humble/setup.zsh
cd /home/wzt/work/CampusBot
colcon build --symlink-install
source install/setup.zsh
```

如果使用 Bash，应将上述两个 `.zsh` 换成对应的 `.bash`。

## 启动基础仿真

构建并加载工作空间后启动 Gazebo、机器人模型和 ROS–Gazebo Bridge：

```bash
ros2 launch campusbot_bringup simulation.launch.py
```

在另一个已经加载工作空间的终端启动 RViz2：

```bash
rviz2
```

当前已实际验证的主要 ROS 2 接口包括：

- `/cmd_vel`：ROS 2 向 Gazebo 发送速度指令。
- `/clock`：Gazebo 向 ROS 2 提供仿真时间。
- `/odom`：发布机器人在里程计坐标系中的位姿与速度。
- `/tf`、`/tf_static`：维护机器人动态与静态坐标变换。
- `/joint_states`：发布左右轮关节状态。
- `/scan`：以约 10 Hz 发布 360 点二维激光扫描。

## 功能包职责

- `campusbot_description`：机器人 Xacro/URDF、坐标系和 RViz 配置。
- `campusbot_bringup`：管理 Gazebo 世界、机器人生成、仿真插件和 Bridge 的组合启动。
- `campusbot_navigation`：预留 slam_toolbox、AMCL 与 Nav2 的参数和启动文件。
- `campusbot_task_manager`：包含已验证的 C++ Publisher/Subscriber，后续承载 Nav2 Action Client 与任务状态机。

## 文档导航

各 Markdown 文件的读者和用途见 [docs/README.md](docs/README.md)。除主要供协作代理读取的 `AGENTS.md` 外，项目文档以中文为主。

## 许可证

本项目使用 MIT License。
