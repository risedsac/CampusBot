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
- [ ] 保存可移植的 RViz2 配置并接入 Launch。

## 当前里程碑：传感器、里程计与 TF

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
- [ ] 扩展可用于建图的静态障碍物场景。

## 后续任务

- [ ] 集成 slam_toolbox 与 Nav2。
- [ ] 实现任务管理、路径规划和自动化评测功能包。
