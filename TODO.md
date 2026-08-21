# 待办事项

## 已完成里程碑：ROS 2 基本通信

- [x] 检查主机开发环境。
- [x] 确定使用 ROS 2 Humble 与 Gazebo Fortress。
- [x] 使用 `colcon build` 验证项目骨架。
- [x] 替换功能包中的临时维护者邮箱。
- [x] 完成首次 Git 提交并通过 SSH 推送到 GitHub。
- [x] 创建 `campusbot_task_manager` C++ 功能包。
- [x] 实现并验证任务状态 Publisher。
- [x] 实现并验证任务状态 Subscriber。
- [x] 生成 clangd 所需的 `compile_commands.json`。
- [x] 清理 Subscriber 的冗余头文件和日志拼写。
- [x] 将 Publisher 发布周期改为 ROS 2 Parameter。
- [x] 使用 Launch 同时启动 Publisher 和 Subscriber。

## 已完成里程碑：机器人模型、TF 与基础仿真驱动

- [x] 创建包含 `base_footprint` 和 `base_link` 的最小 Xacro 模型。
- [x] 使用 `xacro` 和 `check_urdf` 验证模型语法与树结构。
- [x] 使用 `robot_state_publisher` 发布固定 TF。
- [x] 在 RViz2 中显示底盘外观。
- [x] 使用 description 包的 Launch 启动 `robot_state_publisher`。
- [x] 添加底盘的碰撞模型与惯性参数。
- [x] 添加左右驱动轮和后辅助轮。
- [x] 使用 Xacro Property 和 Macro 复用左右轮模型。
- [x] 使用 Gazebo Fortress 加载差速机器人并验证物理稳定性。
- [x] 添加 Gazebo DiffDrive 插件并验证原生速度控制。
- [x] 使用 `ros_gz_bridge` 将 ROS 2 `/cmd_vel` 桥接到 Gazebo。
- [x] 使用顶层 Launch 同时启动 Gazebo、机器人模型与速度桥接节点。
- [x] 保存可移植的 RViz2 配置并接入 Launch。

## 已完成里程碑：传感器、里程计与 TF

- [x] 桥接 Gazebo `/clock` 并统一使用仿真时间。
- [x] 输出并桥接差速驱动里程计 `/odom`。
- [x] 验证 `odom → base_footprint` 动态 TF。
- [x] 发布并桥接驱动轮 `/joint_states`，补全 Wheel Link 动态 TF。
- [x] 添加 `lidar_link`、固定 TF 和 GPU Lidar 传感器模型。
- [x] 创建带 Sensors 系统的项目自有世界，并验证 Gazebo `/scan`。
- [x] 将 Gazebo `/scan` 桥接为 ROS 2 `sensor_msgs/msg/LaserScan`。
- [x] 检查 ROS 2 `/scan` 的消息内容、频率、QoS 和 `frame_id`。
- [x] 使用 `override_frame_id` 将扫描坐标系统一为 `lidar_link`，并验证 TF 可查询。
- [x] 在 RViz2 中显示 LaserScan，加入测试障碍物并验证约 1.75 m 的正前方测距。
- [x] 扩展可用于建图的静态障碍物场景。

## 已完成里程碑：建图、定位与单目标导航

- [x] 使用 slam_toolbox 建立二维占据栅格地图。
- [x] 保存地图 PGM 与 YAML 文件，并理解主要字段。
- [x] 使用 Map Server 加载静态地图。
- [x] 使用 Lifecycle Manager 自动配置并激活 Nav2 Lifecycle Node。
- [x] 使用 AMCL 发布 `map → odom`，建立完整定位 TF 链。
- [x] 配置并启动 Nav2 Planner、Controller、BT Navigator 和恢复行为。
- [x] 在 RViz2 中发送目标并完成单目标自主导航。

## 后续任务

- [ ] 创建一键启动仿真、定位和导航的顶层 Launch。
- [ ] 使用 C++ 实现 Nav2 `NavigateToPose` Action Client。
- [ ] 实现多目标任务状态机、超时、取消和重试。
- [ ] 独立实现 BFS、Dijkstra 与 A* 栅格路径规划。
- [ ] 接入 `OccupancyGrid`，发布并可视化 `nav_msgs/Path`。
- [ ] 实现导航自动化评测、CSV 记录与结果可视化。
- [ ] 持续完善 README、架构说明、测试和面试材料。
