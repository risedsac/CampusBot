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

## 2026-08-09——URDF/Xacro、TF 与 RViz2

### 已完成

- 创建 `campusbot.urdf.xacro`，定义地面投影坐标系 `base_footprint` 和底盘坐标系 `base_link`。
- 使用固定关节连接两个 Link，并将底盘中心设置在地面上方 0.10 m。
- 为 `base_link` 添加尺寸为 0.50 m × 0.35 m × 0.20 m 的蓝色长方体外观。
- 使用 `xacro` 生成普通 URDF，使用 `check_urdf` 验证根 Link 和子 Link。
- 使用 `robot_state_publisher` 发布固定 TF，并在 RViz2 中显示模型。
- 创建 `display.launch.py`，通过 `FindPackageShare`、`PathJoinSubstitution` 和 `Command` 在启动时展开 Xacro。

### 验证证据

- `check_urdf` 输出 `Successfully Parsed XML`，根 Link 为 `base_footprint`，子 Link 为 `base_link`。
- `tf2_echo base_footprint base_link` 实测平移为 `[0, 0, 0.1]`，旋转为单位四元数。
- RViz2 以 `base_footprint` 为固定坐标系，成功显示蓝色底盘。
- `ros2 launch campusbot_description display.launch.py` 成功启动 `robot_state_publisher` 并解析两个 Segment。

### 排错与实验

- 修复 XML 属性之间误用逗号、`geometry` 拼写错误、三维数值误用逗号和缺少 `</robot>` 等问题。
- 发现当前 Humble 运行方式没有 `/robot_description` Topic，改由 RViz2 的 File 模式读取生成的 URDF。
- 主动将固定关节高度从 0.10 m 改为 0 m，观察底盘中心与地面重合的效果，之后恢复为 0.10 m。
- 理解 `got segment` 只能证明结构解析成功，不能证明坐标数值符合设计意图。

### 关键理解

- Joint 的 `origin` 描述 Child Link 相对 Parent Link 的位姿；Visual 的 `origin` 描述几何体相对所属 Link 的位姿。
- Frame 是坐标系，Transform 是两个 Frame 之间的平移和旋转，TF2 负责维护和查询这些变换。
- 固定关系发布到 `/tf_static`，运动过程中变化的关系通常发布到 `/tf`。
- `FindPackageShare` 从安装空间定位功能包资源，避免硬编码本机绝对路径。
- RViz2 显示 RobotModel 同时需要模型描述和 TF；两者缺一不可。

### 仍需继续巩固

- 四元数与 RPY 的转换和旋转方向。
- `map`、`odom`、`base_footprint`、`base_link` 的完整职责划分。
- 动态关节如何由 `/joint_states` 驱动 `robot_state_publisher` 发布 TF。

## 2026-08-10——机器人动力学、Gazebo 与差速驱动

### 已完成

- 使用 Xacro Property 统一管理底盘、车轮和后辅助轮的尺寸、质量与位置参数。
- 使用 Xacro Macro 生成左右驱动轮，避免重复维护两份 Link 和 Joint 定义。
- 为底盘、左右轮和球形辅助轮添加 Visual、Collision、Mass 与 Inertia。
- 使用长方体、圆柱体和实心球公式计算惯性张量，并通过 Xacro 展开结果核对数值。
- 创建后辅助轮和左右 Continuous Joint，完成 `base_footprint → base_link → wheels/caster` 结构。
- 创建 `simulation.launch.py`，统一启动 Gazebo Fortress、`robot_state_publisher` 和机器人生成节点。
- 在 Gazebo 空世界中成功生成 CampusBot，并验证机器人能够稳定落地。
- 添加 Gazebo DiffDrive 插件，通过 Gazebo Transport `/cmd_vel` 验证直行与停止。
- 将主动轮轴线前移至 `x=0.05 m`，并限制线加速度和角加速度，改善启停时的前倾问题。
- 手动验证 ROS–Gazebo Bridge 后，将 `/cmd_vel` Bridge 接入顶层 Launch。
- 最终使用 ROS 2 `geometry_msgs/msg/Twist` 成功控制 Gazebo 中的小车运动。

### 验证证据

- `xacro` 成功生成普通 URDF，`check_urdf` 输出 `Successfully Parsed XML`。
- 生成模型包含左右驱动轮与后辅助轮，轮距展开为约 `0.40 m`，轮径为 `0.10 m`。
- Gazebo GUI 中机器人能够落到地面并保持稳定，没有持续下沉或飞走。
- Gazebo 原生 Twist 命令能够驱动小车，证明 DiffDrive 插件、关节名称和轮子参数有效。
- 手动运行 `parameter_bridge` 后，ROS 2 `/cmd_vel` 能够控制 Gazebo 小车。
- Bridge 写入 `simulation.launch.py` 后，只需启动顶层 Launch，ROS 2 `/cmd_vel` 即可直接控制小车。

### 排错与根本原因

- 后辅助轮最初存在 XML 闭合标签错误和非法惯性属性写法；通过先检查 XML 层级、再把球体惯性保存为 Xacro Property 修复。
- Continuous Joint 没有对应动态 TF 时，RViz2 报告无法从 Wheel Link 变换到 `base_footprint`；原因是运动关节需要 Joint State 才能计算动态变换。
- 初始主动轮位于 `x=0`，整车质心投影几乎落在主动轮支撑边界，突然停止时容易前倾；将主动轮前移并限制减速度后明显改善。
- `ign topic -l` 没有持续显示 `/cmd_vel`，但命令仍能驱动车辆；原因是 DiffDrive 是订阅端，而临时发布命令结束后不再存在长期发布端。
- 8 月 9 日曾记录“当前运行没有 `/robot_description` Topic”；今天重新启动并检查后确认该话题实际存在，因此此前结论属于检查时机或方式导致的误判。

### 关键理解

- Visual 决定显示外观，Collision 决定接触几何，Inertial 决定物体受到力和力矩后的运动响应。
- `F = ma` 描述平动，`τ = Iα` 描述转动；相同力矩下，转动惯量增大一倍会使角加速度减小为一半。
- Joint Origin 决定 Child Link 坐标系相对 Parent Link 的位置；各 Link 内部的 Visual、Collision 和 Inertial Origin 都相对该 Link 坐标系定义。
- 差速驱动根据目标线速度、角速度、轮距和轮径计算左右轮角速度。
- ROS 2 DDS 与 Gazebo Transport 是两套独立通信系统；同名 `/cmd_vel` 需要 Bridge 转换协议和消息类型。
- 仿真环境中的 Bridge 对应真机中的底层硬件驱动接口，上层 Nav2 可以继续使用标准 ROS 2 `/cmd_vel`。

### 仍需继续巩固

- 惯性张量的非对角项及惯性坐标系旋转后的含义。
- 球形固定辅助轮的摩擦简化与真实万向轮模型之间的差别。
- Gazebo 里程计、动态 TF、`/clock` 与 ROS 2 仿真时间的数据关系。
- Bridge 的单向与双向语法，以及为多个传感器使用 YAML 配置的方式。

## 2026-08-11——仿真时间、里程计与动态 TF

### 已完成

- 对比 Gazebo Transport 与 ROS 2 Graph 中的 Clock、Odometry 和 TF Topic。
- 使用 `ros2 topic info --verbose` 证明 Topic 名称存在不等于存在 Publisher，也不等于有消息流动。
- 手动桥接 Gazebo `/clock`，验证 Gazebo 暂停时仿真时间停止、恢复后继续前进。
- 将 Clock Bridge 接入顶层 Launch，并为各 Bridge 设置唯一 Node 名称。
- 检查 Gazebo `/model/campusbot/odometry` 的消息类型，并桥接为 ROS 2 `nav_msgs/msg/Odometry`。
- 使用 ROS 2 Remapping 将模型作用域 Topic 映射为标准 `/odom`。
- 配置 DiffDrive 的 `frame_id=odom` 与 `child_frame_id=base_footprint`，统一 Odometry 和 URDF 的 Frame 名称。
- 桥接 Gazebo `/model/campusbot/tf` 到 ROS 2 `/tf`，使用 `tf2_echo` 验证 `odom → base_footprint` 动态变换。
- 使用一条 `simulation.launch.py` 同时启动 Gazebo、机器人、速度、时钟、里程计和 TF Bridge。

### 验证证据

- Bridge 启动前，ROS 2 `/clock` 的 Publisher 数量为 0，`robot_state_publisher` 是唯一 Subscriber。
- Clock Bridge 启动后，`clock_bridge` 成为唯一 Publisher，仿真时间能够读取并受 Gazebo 暂停状态控制。
- Gazebo Odometry 类型确认为 `ignition.msgs.Odometry`，ROS 2 `/odom` 类型确认为 `nav_msgs/msg/Odometry`。
- 小车直行后 `/odom` 的 `position.x` 累计到约 `1.83 m`，时间戳使用仿真时间。
- 修正 Frame 配置后，消息变为 `frame_id: odom`、`child_frame_id: base_footprint`。
- Gazebo TF 类型确认为 `ignition.msgs.Pose_V`，`tf2_echo odom base_footprint` 已实际运行验证成功。
- Clock、Odometry 和 TF Bridge 写入顶层 Launch 后均完成自动启动验证。

### 关键理解

- `use_sim_time=true` 会让具体 ROS 2 Node 订阅 `/clock`，并不意味着 ROS 2 自动产生仿真时钟。
- `/clock` Bridge 统一 Gazebo 与 ROS 2 的时间基准；Odometry Bridge 转换并传递运动状态，两者职责不同。
- `/odom` 同时包含 Pose、Twist 和 Covariance；TF 提供坐标系查询接口，收到 Odometry 不会自动写入 TF Buffer。
- Topic Remapping 只修改 ROS Graph 中的 Topic 名称，不会修改消息内部的 `frame_id` 和 `child_frame_id`。
- `parameters` 进入 ROS 2 参数系统，`arguments` 进入可执行程序命令行，`launch_arguments` 传给被包含的 Launch，`remappings` 修改 ROS 侧名称。
- `[` 表示 Gazebo → ROS 2，`]` 表示 ROS 2 → Gazebo，开口方向可以辅助记忆消息来源。
- 排错应沿 `ROS Publisher → Bridge → Gazebo Topic → DiffDrive → Joint/Physics` 数据流逐段验证。

### 算法练习：二维机器人返回原点

- 使用两个整数累计二维坐标的总体思路正确。
- 发现未初始化局部整数、自定义字符与题目输入不一致等问题。
- 理解 `int x, y = 0;` 只初始化 `y`，`x` 仍是未初始化状态。
- 最终修正版函数、复杂度分析和编译运行尚未完成，顺延到下一学习日，不记录为已验证。

### 仍需继续巩固

- Topic、Publisher、Subscriber 与具体 Node 的精确关系，避免使用“ROS 2 本身是订阅者”之类不准确表述。
- `/odom` 消息和 `odom → base_footprint` TF 的重复信息与不同消费者。
- Frame 前缀、ROS Namespace 和多机器人 Topic/TF 隔离策略。
- `/joint_states` 如何驱动 `robot_state_publisher` 补全运动关节 TF。

## 2026-08-14——Joint State、雷达坐标系与 Gazebo LaserScan

### 已完成

- 修正二维机器人返回原点函数中的局部变量初始化问题，明确 `int x, y = 0;` 只初始化 `y`；最终逻辑通过代码检查，时间复杂度为 `O(n)`、额外空间复杂度为 `O(1)`，本次未单独编译运行。
- 在 Gazebo 模型中添加 `JointStatePublisher`，只发布左右驱动轮关节状态。
- 使用 `ros_gz_bridge` 将 Gazebo `ignition.msgs.Model` 转换为 ROS 2 `sensor_msgs/msg/JointState`。
- 验证 `/joint_states` 的发布者为 `joint_states_bridge`、订阅者为 `robot_state_publisher`，并通过轮子旋转时变化的 TF 验证动态关节链路。
- 添加 `lidar_link`、圆柱体 Visual/Collision/Inertial 和固定关节，雷达中心相对 `base_footprint` 的高度为 `0.26 m`。
- 创建项目自有 `campus_world.sdf`，加载 Physics、UserCommands、SceneBroadcaster 和 Sensors 系统，并通过 `FindPackageShare` 从 Launch 中定位世界文件。
- 在 `lidar_link` 上添加二维 `gpu_lidar`，配置 360 个水平采样、约 360° 视场、10 Hz、0.12～12 m 量程和 0.01 m 距离分辨率。

### 验证证据

- `ros2 topic info /joint_states --verbose` 显示一个 Bridge Publisher 和一个 `robot_state_publisher` Subscriber。
- `ros2 topic echo --once /joint_states` 返回左右轮的名称、位置、速度与力矩数据。
- 完整仿真启动后，RViz2 中左右轮重新出现；`tf2_echo` 显示轮子旋转时 Rotation 持续变化。
- `xacro` 和 `check_urdf` 成功解析包含 `lidar_link` 的机器人树。
- `tf2_echo base_footprint lidar_link` 与生成 SDF 均确认雷达高度为 `0.26 m`。
- `ign sdf -k campus_world.sdf` 返回 `Valid`，新世界中机器人生成、控制和 `/clock` 均正常。
- URDF 转换后的 SDF 保留 `lidar_sensor`、`gpu_lidar`、`/scan` 和全部扫描参数。
- `ign topic -i -t /scan` 确认 Gazebo `/scan` 的消息类型为 `ignition.msgs.LaserScan`。

### 排错与根本原因

- 最初将 Joint State 插件参数写成 DiffDrive 的 `<left_joint>` 和 `<right_joint>`；根本原因是没有区分不同插件各自的配置接口，修正为可重复的 `<joint_name>`。
- 只运行 description Launch 时 RViz2 中轮子消失；原因是 Continuous Joint 需要 `/joint_states` 才能由 `robot_state_publisher` 生成动态 TF，而固定的雷达关节不需要实时状态。
- 雷达模型曾出现 `radius`、惯量属性和 Link 名称拼写错误；通过“XML 解析 → URDF 语义检查 → TF 数值检查”逐层修复。
- `launch_arguments` 中 `['-r', world_file]` 会直接拼接成 `-r/path`；原因是该列表表示同一参数值的替换片段，不是自动插入空格的终端参数列表。
- Sensor 配置曾混淆 `gazebo reference` 与 `sensor name`；前者必须引用已有 `lidar_link`，后者是 Gazebo 内部的 `lidar_sensor` 实体名称。

### 关键理解

- URDF 描述关节连接关系，`/joint_states` 描述活动关节当前状态，`robot_state_publisher` 将二者结合生成动态 TF。
- Gazebo GUI 本身不会让轮子 TF 出现；真正起作用的是 Joint State 插件、Bridge 和 `robot_state_publisher` 数据链。
- `lidar_link` 表示安装坐标系，`lidar_sensor` 表示传感器实体，`/scan` 表示数据通道，三者不能混为一谈。
- `samples × horizontal resolution` 决定返回距离数据点数量；距离分辨率表示线性测量粒度，不等同于测量精度。
- `-π` 到 `+π` 表示完整一圈，ROS 标准平面坐标中 0 rad 朝向 `+X`，正角方向朝向 `+Y`。
- 系统自带世界适合示例，但仓库自有世界更利于依赖固定、障碍物扩展和 GitHub 复现。

### 仍需继续巩固

- 将 Gazebo LaserScan 转换为 ROS 2 `sensor_msgs/msg/LaserScan` 的 Bridge 类型与方向。
- `/scan` 的实际 `angle_increment`、发布频率、QoS 和 `header.frame_id`。
- RViz2 LaserScan 显示以及 `lidar_link` TF 对齐检查。
- 在世界中加入可用于建图的障碍物，并理解仿真分辨率、噪声和真实雷达误差的区别。

## 2026-08-19——ROS 2 LaserScan、Frame 对齐与障碍物测距

### 已完成

- 使用 `ros_gz_bridge` 将 Gazebo `ignition.msgs.LaserScan` 转换为 ROS 2 `sensor_msgs/msg/LaserScan`。
- 将 Scan Bridge 接入顶层 `simulation.launch.py`，不再需要手动启动桥接进程。
- 检查 `/scan` 的发布端点、QoS、频率、角度范围、距离范围和数组长度。
- 发现 Gazebo 默认生成的作用域 Frame 名称不属于机器人 TF 树，使用 Bridge 的 `override_frame_id` 将消息统一为 `lidar_link`。
- 使用 `tf2_echo base_link lidar_link` 验证固定变换为 Z 方向 `0.12 m`。
- 在项目世界中加入橙色静态长方体，同时定义一致的 Visual 与 Collision。
- 在 Gazebo 中观察障碍物，在 RViz2 中观察红色扫描线，并读取 `/scan` 数组验证实际测距。

### 验证证据

- `/scan` 的 Publisher 为 `scan_bridge`，消息类型为 `sensor_msgs/msg/LaserScan`。
- 实测发布频率约为 `9.91～9.92 Hz`，与传感器配置的 10 Hz 一致。
- 一帧消息包含 360 个 `ranges`，角度范围约为 `-π～+π`，量程为 `0.12～12 m`。
- `ros2 param get /scan_bridge override_frame_id` 返回 `lidar_link`，消息头中的 `frame_id` 同样为 `lidar_link`。
- RViz2 LaserScan 状态为 `OK`，能够显示测试障碍物形成的红色扫描线。
- 障碍物正面理论位置为 `2.0 - 0.5 / 2 = 1.75 m`，实测最近扫描距离约为 `1.7501 m`。

### 排错与根本原因

- `/scan` 最初有数据但 Frame 为 `campusbot/base_footprint/lidar_sensor`；该名称不在 TF 树中，因此 RViz2 无法可靠完成坐标变换。
- 没有添加虚假的静态 TF，而是把传感器消息的 Frame 统一为已有的安装坐标系 `lidar_link`，使消息语义与 URDF 保持一致。
- `tf2_echo` 启动瞬间曾报告 Frame 不存在，随后持续输出正确变换；这是节点发现和 TF 数据到达前的短暂状态，不是最终连接失败。
- 当前 ROS 2 CLI 将 `ranges` 输出为单行 `array('f', [...])`，因此按输出行号截取中间元素的方法不适用。

### 关键理解

- LaserScan 的每个距离值都必须结合对应角度和 `header.frame_id` 才有空间意义；Topic 有数据并不代表 RViz2 一定能显示。
- `inf` 表示该方向在有效量程内没有获得碰撞返回，不代表 Bridge 或传感器报错。
- 平面障碍物正前方距离最短，越靠两侧射线越倾斜，测得斜距越长。
- 360 是偶数，最接近零度的是两束对称射线，因此数组中央出现两个几乎相同的最小距离。
- SDF 中 Visual 决定可见外观，Collision 决定射线和物理碰撞；两者不一致会造成“看到的位置”和“测到的位置”不同。

### 仍需继续巩固

- LaserScan QoS 的请求与提供兼容关系，以及 slam_toolbox 的订阅要求。
- 仿真雷达分辨率、噪声模型和真实传感器精度之间的区别。
- 构建具有足够几何特征的建图世界，并验证机器人运动时扫描与 TF 的连续对齐。

## 2026-08-21——静态地图定位与 Nav2 单目标导航

### 已完成

- 使用 slam_toolbox 完成项目场景建图，并保存 `campus_map.pgm` 与 `campus_map.yaml`。
- 将地图资源安装到 `campusbot_navigation`，使用 Map Server 发布 `/map`。
- 先手动执行 `configure` 和 `activate` 观察 Lifecycle 状态变化，再使用 Lifecycle Manager 自动管理 Map Server。
- 配置 AMCL 并通过 RViz2 发布 `/initialpose`，成功获得 `/amcl_pose` 和 `map → odom`。
- 配置并启动 Nav2 Planner、Controller、BT Navigator、Behavior Server 和 Velocity Smoother。
- 在 RViz2 中发送 Nav2 Goal，完成多次单目标自主导航验证。
- 将仿真、建图和导航 RViz2 配置分开，并通过 Launch Argument 选择配置文件。

### 验证证据

- 保存地图的分辨率为 `0.05 m`，宽高均为 `118` 个栅格，对应约 `5.9 m × 5.9 m`。
- Map Server 激活后，`/map` Publisher 数量为 1，QoS 为 `RELIABLE + TRANSIENT_LOCAL`。
- `map_server` 与 `amcl` 的 Lifecycle 状态均为 `active [3]`。
- `/amcl_pose` 输出地图坐标系中的估计位姿和协方差。
- `tf2_echo map odom` 与 `tf2_echo map base_footprint` 均持续返回有效变换。
- Nav2 五个主要运行节点均处于 Active 状态，RViz2 点击目标后机器人能够自主到达。

### 排错与根本原因

- Map Server 最初为 `unconfigured`，因此 ROS Graph 中不存在 `/map`；Lifecycle Node 只有配置并激活后才执行主要功能。
- RViz2 使用 `map` 作为 Fixed Frame 时机器人最初无法正常显示；原因是只有 `odom → base_footprint`，缺少定位模块提供的 `map → odom`。
- 雷达扫描与旧地图存在少量平行偏差；地图栅格分辨率、建图误差、里程计误差和 AMCL 估计误差都会共同影响重合程度。
- 目标点太靠近柱子时导航无法完成；机器人中心可达不等于机器人整个轮廓安全，Costmap 会结合机器人半径和障碍膨胀判断目标是否合法。

### 关键理解

- slam_toolbox 用于边运动边估计轨迹并建立地图；Map Server 用于加载和发布已经保存的静态地图。
- `odom → base_footprint` 提供连续、短期平滑的局部运动；AMCL 用地图和激光观测修正累计误差，并发布 `map → odom`。
- Planner Server 计算从当前位置到目标的全局路径；Controller Server 根据路径与局部环境持续输出速度控制指令。
- BT Navigator 组织导航任务流程；Behavior Server 承担旋转、后退等恢复行为；Lifecycle Manager 统一管理节点状态。
- `TRANSIENT_LOCAL` 使后加入的地图订阅者也能收到发布端保存的最后一份地图。
- 当前 Gazebo 仍然存在物理接触和摩擦，但模型、传感器、里程计和环境比真机理想；真机会受到轮胎打滑、标定误差、噪声、延迟和动态障碍影响。

### 仍需继续巩固

- AMCL 粒子滤波、协方差和初始位姿不确定性的含义。
- Global Costmap、Local Costmap、机器人半径与 Inflation Layer 的具体参数关系。
- Nav2 行为树的数据流和失败恢复流程。
- `NavigateToPose` Action 的目标、反馈、结果、取消、超时和重试机制。
