# 架构决策记录

## ADR-001：ROS 与仿真器基线

- 日期：2026-08-04
- 状态：已接受
- 决策：使用本机原生 ROS 2 Humble，通过 `ros_gz` 集成 Gazebo Fortress。
- 理由：所需软件栈已经安装；Humble 与 Fortress 是官方配套组合；原生图形环境可以避免容器在 8 GB 内存机器上的额外开销。
- 影响：Gazebo Classic 只保留为兼容性备用方案；GUI 行为需要在桌面环境中人工验证。

## ADR-002：机器人模型基线

- 日期：2026-08-04
- 状态：已接受
- 决策：创建简化的自定义差速 CampusBot 模型，不以 TurtleBot3 作为起点。
- 理由：在保持几何结构简单的同时，完整学习 URDF/Xacro、TF、传感器坐标系和仿真器插件。

## ADR-003：任务管理模块使用独立 C++ 功能包

- 日期：2026-08-05
- 状态：已接受
- 决策：使用 `campusbot_task_manager` 承载任务状态通信和后续 Nav2 Action Client，首先用最小 Publisher/Subscriber 验证 C++ 构建与回调模型。
- 理由：将任务调度与机器人描述、系统启动和导航配置分离，便于独立测试，也能逐步学习 Topic、Parameter、Service 和 Action。
- 影响：当前的 `std_msgs/msg/String` 只是通信学习载体；任务状态模型将在需求明确后再评估是否换成自定义消息。

## ADR-004：使用项目自有的传感器仿真世界

- 日期：2026-08-14
- 状态：已接受
- 决策：在 `campusbot_bringup/worlds` 中维护 `campus_world.sdf`，由顶层 Launch 通过 `FindPackageShare` 加载，不修改 Gazebo 安装目录中的 `empty.sdf`。
- 理由：系统 `empty.sdf` 没有加载 Sensors 系统；项目自有世界可以固定 Physics、渲染和传感器插件配置，也便于后续加入建图障碍物并由 Git 追踪。
- 影响：`campusbot_bringup` 必须安装 `worlds` 目录；GPU Lidar 依赖该世界中的 Sensors 系统和 Ogre2 渲染引擎。
