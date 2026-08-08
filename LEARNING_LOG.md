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

## 2026-08-08——Parameter 与 Launch

### 已完成

- 将 Publisher 的发布周期声明为整数类型 ROS 2 Parameter，默认值为 1000 ms。
- 使用命令行把周期覆盖为 200 ms，并通过日志和 Topic 频率验证约为 5 Hz。
- 对 0 ms 和负数周期进行输入检查，节点输出明确错误并以非零状态退出。
- 编写 `task_status.launch.py`，一次启动 Publisher 和 Subscriber，并在 Launch 中传入 500 ms 周期。
- 在 CMake 中安装 Launch 目录，在 `package.xml` 中声明 `launch` 和 `launch_ros` 运行依赖。

### 验证证据

- `campusbot_task_manager` 使用 `-Wall -Wextra -Wpedantic` 构建通过。
- 默认 1000 ms、命令行覆盖 200 ms、非法的 0 ms 和负数输入均完成实际运行验证。
- `ros2 launch campusbot_task_manager task_status.launch.py` 成功启动两个进程。
- Launch 日志显示发布周期为 500 ms，Publisher 和 Subscriber 的消息一一对应。
- 使用 `Ctrl+C` 后两个节点均正常退出。

### 关键理解

- Parameter 的存储值、构造函数中读取出的局部变量和已经创建的 Timer 是三个不同层次的状态。
- 运行期间修改 Parameter 不会自动重建 Timer；动态生效需要参数回调和明确的 Timer 更新逻辑。
- Launch 中传入的参数会覆盖节点声明 Parameter 时使用的默认值。
- Launch 文件需要安装到功能包的 `share` 目录，ROS 2 才能通过包索引定位它。
- Launch 中的包名、可执行程序名和节点名来源不同，不能混为一谈。

### 算法练习：两数之和

- 写出双层循环暴力解法，理解 `j` 从 `i + 1` 开始可以避免重复使用同一个元素。
- 理解 `std::vector<int> answer(2, 0)` 会直接创建两个元素，而不是只预留容量。
- 暴力解法最坏检查 `n(n - 1) / 2` 对元素，时间复杂度为 `O(n²)`，额外空间复杂度为 `O(1)`。
- 写出基于 `std::unordered_map` 的一次遍历解法，理解映射关系为“元素值 → 旧下标”。
- 理解哈希表必须先查找补数、再插入当前元素，否则可能错误地重复使用当前下标。
- 哈希表解法平均时间复杂度为 `O(n)`，额外空间复杂度为 `O(n)`。
- 两份算法代码已经完成逻辑检查；按照本人选择，本次未进行编译和运行，因此仍属尚未实际验证。

### 仍需继续巩固

- ROS 2 动态参数回调的注册、校验和线程安全问题。
- Launch 参数、节点重命名、命名空间和条件启动。
- QoS 策略以及 Service、Action 与 Topic 的适用场景。
