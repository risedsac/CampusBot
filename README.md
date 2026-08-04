# CampusBot

CampusBot: ROS2 Autonomous Navigation and Benchmark System

CampusBot 是一个面向学习与工程实践的 ROS 2 移动机器人项目，计划完成差速机器人仿真、建图、定位导航、自定义路径规划、任务管理和自动化评测。

## 当前状态

- 阶段：第 1 天，项目骨架
- 环境：Linux Mint 21.3（Ubuntu 22.04 Jammy 基础）、ROS 2 Humble、Gazebo Fortress
- 已完成：环境审计、技术路线选择、ROS 2 package 骨架
- 尚未完成：机器人模型、仿真、SLAM、Nav2 集成及自定义算法

## 构建

```bash
source /opt/ros/humble/setup.bash
cd /home/wzt/work/CampusBot
colcon build --symlink-install
source install/setup.bash
```

首次构建只验证 package 结构和依赖声明，不代表机器人功能已经实现。

## 功能包职责

- `campusbot_description`：机器人 Xacro/URDF、坐标系和 RViz 配置。
- `campusbot_bringup`：组合启动仿真、机器人描述和导航模块。
- `campusbot_navigation`：slam_toolbox、AMCL 与 Nav2 的参数和启动文件。

## 文档导航

各 Markdown 文件的读者和用途见 [docs/README.md](docs/README.md)。除主要供协作代理读取的 `AGENTS.md` 外，项目文档以中文为主。

## 许可证

本项目使用 MIT License。
