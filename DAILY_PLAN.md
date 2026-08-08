# 每日计划

## 2026-08-04——第 1 天

### 今日目标

1. 确定 ROS 2 与 Gazebo 技术基线。
2. 创建最小仓库与功能包骨架。
3. 构建工作空间并理解各生成目录。

### 验收标准

- `colcon build --symlink-install` 构建成功。
- source overlay 后，ROS 2 能发现三个 CampusBot 功能包。
- 能解释 `src/`、`build/`、`install/` 和 `log/` 的用途。

### 验证结果

- 构建通过：3 个功能包全部成功完成。
- 依赖检查通过：声明的系统依赖均已满足。
- Overlay 检查通过：所有功能包前缀都指向当前工作空间的 `install/` 目录。
- Git 验收通过：完成第一次人工提交，并通过 SSH 成功推送到 GitHub。

## 2026-08-05——第 2 天

### 今日目标

1. 理解 ROS 2 节点、Topic、消息类型与 Publisher 的数据关系。
2. 亲自实现并验证一个 C++ 任务状态 Publisher。
3. 在理解 Publisher 后，实现 Subscriber，再加入参数与 Launch。

### 今日步骤

1. 用伪代码描述 Publisher 的输入、处理和输出。
2. 创建 `campusbot_task_manager` C++ 功能包骨架。
3. 亲自补全 Publisher 的关键代码并编译。
4. 使用 `ros2 topic` 命令检查 Topic、消息类型、频率和内容。
5. 通过理解检查后，再实现 Subscriber、参数和 Launch。

### 今日验收标准

- Publisher 与 Subscriber 能通过一个 Topic 稳定通信。
- 能解释节点、Topic、消息、Publisher、Subscriber 和 QoS 的基本关系。
- 能解释构造函数、成员变量、智能指针、定时器与回调函数。
- 能预测修改发布周期和 Topic 名称后的运行结果。
- 构建、运行和检查命令均实际执行成功。

### 今日成果

- 创建 `campusbot_task_manager` C++ 功能包。
- 独立完成 `task_status_publisher`，以约 1 Hz 向 `/campusbot/task_status` 发布 `HELLO0`、`HELLO1` 等消息。
- 独立完成 `task_status_subscriber`，通过订阅回调逐条接收并输出消息。
- 使用 `ros2 topic info --verbose` 和 `ros2 topic echo --once` 验证消息类型、通信端点、QoS 与实际数据。
- 为 clangd 生成 `compile_commands.json`，验证 ROS 2 头文件可正确索引，检查结果为 0 个错误。
- Publisher 和 Subscriber 已分别创建 Git 提交并推送到 GitHub。

### 今日知识点

- C++ 语法：类继承、构造函数初始化列表、成员变量生命周期、`std::shared_ptr`、Lambda 的 `[this]` 捕获、`ConstSharedPtr`、`std::chrono::milliseconds`。
- 数据结构与算法：初步理解 QoS 队列深度与回调阻塞后的消息积压；未进入正式算法实现。
- ROS 2：Node、Topic、Message、Publisher、Subscriber、`spin()`、Executor、DDS 发现、`RELIABLE` 与 `VOLATILE` QoS。
- Linux 与工具：`colcon build --packages-select`、`compile_commands.json`、`clangd-15 --check`、`ros2 topic` 检查命令。
- 面试知识：节点与进程的区别、Publisher/Subscriber 数据流、单线程 Executor 中阻塞回调的影响。

### 验收结果

- [x] Publisher 与 Subscriber 在 `/campusbot/task_status` 上稳定通信。
- [x] 两个可执行程序都能从 `install/` 中被 `ros2 run` 发现。
- [x] 构建通过，已启用 `-Wall -Wextra -Wpedantic`。
- [x] clangd 能读取 ROS 2 依赖和 C++17 编译参数。
- [ ] 发布周期参数化。
- [ ] 使用 Launch 同时启动 Publisher 和 Subscriber。

### 当日复盘

- 已完成：C++ Publisher、Subscriber、运行验证、Topic/QoS 检查与 Git 提交。
- 未完成：Parameter 与 Launch，顺延到下一学习日。
- 典型错误：`SharedPtr`、`msg` 的拼写错误，`1000ms` 缺少字面量作用域，clangd 缺少编译数据库。
- 根本原因：对 ROS 2 API 名称不熟悉，以及尚未建立“CMake 目标生成真实编译参数”的工具链认识。
- 已纠正的误解：Subscriber 不使用 Publisher 的 Timer；它由消息到达事件使 Subscription 就绪，再由 Subscriber 的 Executor 执行回调。
- 仍需巩固：DDS 发现与单条消息数据流的区别、`ConstSharedPtr` 的精确语义、QoS 队列满后的行为。

### 当日面试题（待回答）

1. ROS 2 Node、可执行文件和进程有什么区别？
2. `rclcpp::spin()` 和 Executor 分别做什么？
3. 没有 Subscriber 时，Publisher 还会执行 `publish()` 吗？
4. `ConstSharedPtr` 约束的是智能指针还是消息对象？
5. 单线程 Executor 中一个回调阻塞会有什么影响？
6. 为什么后启动的 Subscriber 没有收到 `HELLO0` 开始的历史消息？

### 当日算法题（顺延到下一学习日）

- LeetCode 1：两数之和。目标是对比两层循环与哈希表方案的时间复杂度。

### 下一学习日计划

1. 清理 Subscriber 的内部实现头文件与日志拼写。
2. 将 Publisher 的发布周期改为可校验的 ROS 2 Parameter。
3. 如果参数化已充分理解，再创建最小 Launch 文件。

## 2026-08-08——第 3 天

### 今日目标

1. 清理 Subscriber 的头文件和日志，恢复 Publisher/Subscriber 数据流知识。
2. 将 Publisher 的发布周期改为可校验的 ROS 2 Parameter。
3. 如果 Parameter 已充分理解，再创建最小 Launch 文件；不为赶进度强行完成。

### 今日成果

- Subscriber 只依赖必要的公开头文件，并能通过无警告构建。
- Publisher 默认以 1000 ms 周期运行，也能用命令行参数改为 200 ms。
- 对 0 或负数周期明确报错，不用隐式回退值掩盖错误输入。
- 能解释参数的声明、默认值、启动覆盖和运行期动态修改之间的区别。

### 今日知识点

- C++ 语法：`const auto`、整数类型、参数检查与异常、显式头文件依赖。
- 数据结构与算法：复习哈希表，对比两数之和的暴力方案与哈希表方案。
- ROS 2：Parameter 声明与读取、CLI 覆盖、参数类型、Timer 的创建时机。
- Linux 与工具：在 zsh 中加载 `setup.zsh`，使用 `ros2 param` 和 `ros2 topic hz` 验证运行参数。
- 面试知识：为什么参数优于硬编码，以及为什么修改参数不一定会自动重建 Timer。

### 今日步骤

1. 20 分钟：清理 Subscriber，重新构建并运行 Publisher/Subscriber。
2. 20～40 分钟：理解 Parameter 的输入、输出、类型与启动覆盖。
3. 30～60 分钟：亲自实现发布周期参数化和非法输入检查。
4. 20～40 分钟：编译、运行，并对 1000 ms、200 ms、0 ms 和负数输入分别验证。
5. 20～40 分钟：视理解情况完成 Launch 或进行知识复盘。

### 今日验收标准

- `campusbot_task_manager` 构建成功且无编译警告。
- 默认启动时测得发布频率约为 1 Hz。
- 传入 `publish_period_ms:=200` 时测得发布频率约为 5 Hz。
- 传入非法周期时节点明确报错并退出。
- 能不看代码说出 Parameter 数据如何变成 Timer 周期。

### 验收结果

- [x] Subscriber 使用必要的公开头文件，功能包构建成功。
- [x] 默认 1000 ms 和覆盖为 200 ms 的发布周期均通过运行验证。
- [x] 0 ms 和负数输入会输出明确错误并以非零状态退出。
- [x] Launch 文件成功安装，并以 500 ms 参数同时启动 Publisher 和 Subscriber。
- [x] 能解释 Parameter 存储值、局部变量和 Timer 周期之间的区别。

### 当日复盘

- 已完成：Subscriber 清理、发布周期参数化、非法输入处理、最小 Launch、构建和运行验证。
- 尚未完成：两数之和算法题和本日面试题，保留为本次学习的最后两个环节。
- 典型错误：误用 `--cmake-flags`，Launch 中将 `executable` 拼错，并曾写错 Subscriber 的包名。
- 根本原因：尚未完全熟悉 colcon 参数名称，以及 Launch 中包名、可执行程序名和节点名的对应关系。
- 已掌握：启动参数覆盖默认值、Timer 创建时机、Launch 文件安装位置和多节点统一启动。
- 仍需巩固：动态参数更新机制、QoS、Service、Action 和多种 Executor。

### 下一学习日方向

1. 创建最小 URDF/Xacro 机器人模型。
2. 理解 `base_link`、关节和 TF 父子关系。
3. 使用 `robot_state_publisher` 在 RViz2 中显示模型。
