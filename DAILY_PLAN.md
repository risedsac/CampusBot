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
- 知识检查：完成 Node、Executor、Topic、Parameter、Launch 和 Timer 状态关系的问答与纠正。
- 算法练习：完成两数之和的暴力法与哈希表法，能够解释时间和空间复杂度以及“先查找、后插入”的原因。
- 尚未完成：两数之和代码未编译和运行；按照本人选择，本次只完成代码审查并明确标记为尚未验证。
- 典型错误：误用 `--cmake-flags`，Launch 中将 `executable` 拼错，并曾写错 Subscriber 的包名。
- 根本原因：尚未完全熟悉 colcon 参数名称，以及 Launch 中包名、可执行程序名和节点名的对应关系。
- 已掌握：启动参数覆盖默认值、Timer 创建时机、Launch 文件安装位置和多节点统一启动。
- 仍需巩固：动态参数更新机制、QoS、Service、Action 和多种 Executor。

### 下一学习日方向

1. 创建最小 URDF/Xacro 机器人模型。
2. 理解 `base_link`、关节和 TF 父子关系。
3. 使用 `robot_state_publisher` 在 RViz2 中显示模型。

## 2026-08-09——第 4 天

### 今日目标

1. 理解 URDF/Xacro 中 Link、Joint、Visual 和 Origin 的关系。
2. 创建 `base_footprint → base_link` 最小底盘模型。
3. 使用 `robot_state_publisher`、TF 和 RViz2 完成显示；时间允许时加入最小 Launch。

### 今日成果

- 创建可被 Xacro 和 URDF 工具正确解析的蓝色长方体底盘。
- 发布 `base_footprint → base_link` 固定 TF，并在 RViz2 中显示模型。
- 使用 description 包自己的 Launch 启动 `robot_state_publisher`。

### 今日知识点

- C++ 语法：本日不新增 C++，集中学习 XML、Python Launch 和机器人坐标系。
- 数据结构与算法：树结构、唯一父节点和坐标变换链。
- ROS 2：URDF、Xacro、`robot_description`、`robot_state_publisher`、`/tf_static` 和 RViz2 RobotModel。
- Linux 与工具：`xacro`、`check_urdf`、`tf2_echo` 和 `FindPackageShare`。
- 面试知识：Frame、Transform 与 TF tree 的区别，以及 Joint Origin 与 Visual Origin 的区别。

### 验收结果

- [x] Xacro 成功生成普通 URDF。
- [x] `check_urdf` 确认根 Link 和固定关节树正确。
- [x] `tf2_echo` 确认固定关节高度为 0.10 m。
- [x] RViz2 成功显示蓝色底盘。
- [x] description Launch 成功启动 `robot_state_publisher`。

### 当日复盘

- 已完成：最小底盘模型、固定 TF、RViz2 显示、description Launch 和项目理解检查。
- 未完成：可移植 RViz2 配置尚未接入 Launch；碰撞、惯性和轮子留到下一学习日。
- 典型错误：XML 属性和向量误用逗号、`geometry` 拼写错误、遗漏根结束标签、把 Launch 变量写成带引号的普通字符串。
- 根本原因：首次接触 XML/URDF 语法，以及尚未完全区分字符串字面量、Launch Substitution 和运行期结果。
- 已掌握：TF 是带时间信息的坐标变换系统；模型描述与 TF 是 RViz2 显示 RobotModel 的两个独立输入。
- 仍需巩固：四元数、动态 TF、完整导航坐标系链和 RViz2 配置复用。

### 下一学习日方向

1. 为底盘添加 Collision 与 Inertial。
2. 添加左右驱动轮，并理解 Revolute/Continuous Joint。
3. 保存 RViz2 配置并完善显示 Launch。

## 2026-08-10——第 5 天

### 今日目标

1. 为底盘、驱动轮和后辅助轮补全碰撞与惯性属性。
2. 在 Gazebo Fortress 中生成并稳定运行差速机器人。
3. 打通 ROS 2 `/cmd_vel` 到 Gazebo DiffDrive 的控制链。

### 今日成果

- 完成具有底盘、两个驱动轮和后辅助轮的差速机器人第一版物理模型。
- 使用 Xacro Property 和 Macro 管理重复参数与左右轮结构。
- 完成 Gazebo 顶层 Launch、DiffDrive 插件与 ROS–Gazebo Bridge。
- 使用一条 Launch 命令启动完整仿真，并通过 ROS 2 Twist 消息控制小车前进和停止。
- 根据支撑点和质心关系定位启停前倾问题，通过前移主动轮与限制加速度改善稳定性。

### 今日知识点

- C++ 语法：本日不新增 C++，重点学习 XML/Xacro、Python Launch 和动力学概念。
- 数据结构与算法：使用树结构理解 Link/Joint 层级，使用支撑三角形分析静态稳定性。
- ROS 2：`robot_description`、仿真时间、`geometry_msgs/msg/Twist`、ROS–Gazebo Bridge。
- Linux 与工具：`xacro`、`check_urdf`、`ign topic`、`ros2 topic pub`、多终端分层验证。
- 面试知识：Visual/Collision/Inertial 的区别、差速运动模型、仿真与真机底层接口替换。

### 验收结果

- [x] 底盘、车轮和后辅助轮均具有 Visual、Collision 与 Inertial。
- [x] Xacro 与 URDF 结构检查通过。
- [x] Gazebo 能够生成机器人并进行物理仿真。
- [x] Gazebo 原生 `/cmd_vel` 能够驱动小车。
- [x] ROS 2 `/cmd_vel` 通过 Bridge 驱动小车。
- [x] Bridge 已接入顶层 Launch，不再需要手动单独启动。
- [x] 小车连续启停后保持基本稳定。

### 当日复盘

- 已完成：机器人动力学属性、车轮 Macro、辅助轮、Gazebo 生成、差速驱动、稳定性修正和 ROS–Gazebo Bridge。
- 未完成：可移植 RViz2 配置、`/clock`、里程计、动态 TF 和激光雷达，顺延到下一学习日。
- 典型错误：XML 标签闭合错误、惯性属性引用方式错误、Python Launch 缩进错误、包名漏写引号、未使用路径拼接工具。
- 根本原因：首次同时处理 XML 层级、Xacro 表达式和 Python Launch，尚未形成“语法检查 → 展开检查 → 运行检查”的固定流程。
- 已掌握：Visual/Collision/Inertial 的职责、惯性张量基本意义、差速驱动参数、Bridge 的协议转换作用和顶层 Launch 的工程价值。
- 仍需巩固：完整动力学参数、真实脚轮建模、仿真时钟、里程计和移动关节 TF。

### 当日面试题（待回答）

1. RViz2 和 Gazebo 的核心区别是什么？
2. URDF 中 Visual、Collision 和 Inertial 分别解决什么问题？
3. `mass`、惯性张量和 Inertial Origin 会分别影响哪些物理现象？
4. 差速小车如何根据线速度和角速度计算左右轮速度？
5. 为什么 ROS 2 `/cmd_vel` 和 Gazebo `/cmd_vel` 同名却不能直接通信？
6. 仿真机器人突然停止时前倾，你会从哪些物理参数和结构关系排查？
7. 如果从 Gazebo 换成真机，哪些上层模块可以保留，哪些底层模块需要替换？

### 当日算法题

- 暂不新增算法题；今天集中完成机器人动力学和仿真控制链，下一学习日恢复算法练习。

### 下一学习日方向

1. 桥接 `/clock`，理解真实时间与仿真时间。
2. 输出 `/odom` 并建立 `odom → base_footprint` 动态 TF。
3. 添加激光雷达并验证 `/scan` 的消息类型、频率和 QoS。
