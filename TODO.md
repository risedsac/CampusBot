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

## 当前里程碑：机器人模型与 TF

- [x] 创建包含 `base_footprint` 和 `base_link` 的最小 Xacro 模型。
- [x] 使用 `xacro` 和 `check_urdf` 验证模型语法与树结构。
- [x] 使用 `robot_state_publisher` 发布固定 TF。
- [x] 在 RViz2 中显示底盘外观。
- [x] 使用 description 包的 Launch 启动 `robot_state_publisher`。
- [ ] 添加底盘的碰撞模型与惯性参数。
- [ ] 添加左右驱动轮和辅助轮。
- [ ] 保存可移植的 RViz2 配置并接入 Launch。

## 后续任务

- [ ] 完成差速机器人描述。
- [ ] 接入 Gazebo 传感器与差速驱动。
- [ ] 集成 slam_toolbox 与 Nav2。
- [ ] 实现任务管理、路径规划和自动化评测功能包。
