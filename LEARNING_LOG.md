# 学习日志

## 2026-08-04——开发环境与工作空间

- 确认已经安装 ROS 2 Humble、Nav2、slam_toolbox、RViz2 和 Gazebo Fortress。
- 确定三周项目采用本机原生 Humble + Fortress 技术路线。
- 理解 colcon 工作空间将源码功能包放在 `src/`，构建时生成 `build/`、`install/` 和 `log/`。

仍需复习的问题：

- underlay 与 overlay 工作空间有什么区别？
- `ament_package()` 如何让 ROS 2 发现功能包？

### 排错练习

- 修复了 CMake 注释误用 `//` 而不是 `#` 导致的解析错误。
- 观察到构建前 source 当前工作空间可能触发 underlay 同名功能包覆盖警告。
- 在 `AMENT_PREFIX_PATH` 只包含 `/opt/ros/humble` 的环境中成功完成重新构建。

### Git 与 GitHub

- 完成首次本地提交，并理解工作区、暂存区和提交之间的关系。
- 生成 Ed25519 SSH 密钥，将公钥添加到 GitHub，并通过 `ssh -T git@github.com` 验证身份。
- 将远程地址从 HTTPS 切换为 SSH，成功把本地 `main` 推送到 `origin/main`。
- 理解私钥必须保留在本机，只有 `.pub` 公钥可以上传。

## 2026-08-05——C++ Publisher 与 Subscriber

### 已完成

- 创建 `campusbot_task_manager` C++ 功能包。
- 使用 `rclcpp::Publisher<std_msgs::msg::String>` 定时发布任务状态消息。
- 使用 `rclcpp::Subscription<std_msgs::msg::String>` 接收消息并执行回调。
- 将 Publisher、Timer 和 Subscription 的智能指针保存为类成员，使其生命周期与 Node 一致。
- 在 CMake 中为两个节点添加可执行目标、ament 依赖和安装规则。

### 验证证据

- `colcon build --packages-select campusbot_task_manager` 构建通过。
- clangd 成功读取 `compile_commands.json`，Publisher 与 Subscriber 都完成检查且为 0 个错误。
- `/campusbot/task_status` 的消息类型为 `std_msgs/msg/String`，实测 Publisher 数量为 1。
- Publisher 输出 `HELLO0` 至 `HELLO17` 时，Subscriber 逐条收到了对应消息。
- 后启动的临时 Subscriber 收到 `HELLO118`，验证默认 `VOLATILE` QoS 不补发早期历史消息。

### 关键理解

- `spin()` 让 Executor 等待定时器、Topic、Service 和 Action 等就绪事件，它不是在 `main()` 中直接循环调用业务函数。
- Publisher 的 Timer 只负责产生发布事件；Subscriber 由 DDS 消息到达后的 Subscription 就绪事件驱动。
- DDS 发现和端点匹配属于通信准备过程，不是每条消息的业务数据流。
- `ConstSharedPtr` 为回调提供指向只读消息对象的共享智能指针，这是编译期代码约束，不是网络安全机制。
- 单线程 Executor 中的长时间回调会延迟同一 Executor 内的其他回调。

### 仍需继续巩固

- 不看提示画出“Publisher Executor → DDS/RMW → Subscriber Executor”数据流。
- 深入理解 QoS 的 History、Depth、Reliability 和 Durability。
- 理解参数声明、默认值、启动覆盖与运行期动态更新的区别。
