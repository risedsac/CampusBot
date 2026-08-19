# 故障排查记录

## `ros2 --version` 报告未知参数

ROS 2 Humble 的命令行工具没有全局 `--version` 选项。可以改为检查 `ROS_DISTRO`、功能包前缀或系统已安装的软件包版本。

## GUI 检查在自动化终端中失败

沙箱可能没有暴露桌面显示服务或 GPU 设备节点。诊断显卡驱动前，应先在普通桌面终端中重新验证 RViz2 和 Gazebo GUI。

## CMake 报告 `Expected a command name`

CMake 注释以 `#` 开头，不能使用 C++ 的 `//`。没有 `#` 的普通说明文字也会被当成 CMake 命令，从而导致配置失败。

## colcon 警告所选功能包已经存在于 underlay

如果重新构建当前工作空间前已经 source 了它自己的 `install/setup.bash`，就可能出现该警告。应打开新终端，只 source `/opt/ros/humble/setup.bash`，构建成功后再 source 项目 overlay。不要习惯性使用 `--allow-overriding` 隐藏警告。

## clangd 无法识别 ROS 2 头文件

原因是 clangd 不会因为系统已安装 ROS 2 就自动获得 CMake 目标的头文件搜索路径。源文件还必须先被 `add_executable()` 注册为构建目标。

构建时生成编译数据库：

```bash
colcon build --symlink-install \
  --packages-select campusbot_task_manager \
  --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

当前数据库位于 `build/campusbot_task_manager/compile_commands.json`，项目根目录的同名符号链接供 clangd 发现它。该链接已被 Git 忽略。

本机安装的可执行文件名为 `clangd-15`，如果编辑器配置使用 `clangd`，还需确认 LSP 实际启动命令。

## `/scan` 有数据但 RViz2 无法显示

先检查消息头和 TF：

```bash
ros2 topic echo /scan --once --field header
ros2 run tf2_ros tf2_echo base_link lidar_link
```

本项目中，Gazebo 最初输出的 Frame 为 `campusbot/base_footprint/lidar_sensor`，但 URDF/TF 树中的雷达安装坐标系是 `lidar_link`。Topic 虽然持续有数据，RViz2 却无法把该数据转换到 Fixed Frame。

已验证的解决方案是在 `scan_bridge` 中设置：

```python
parameters=[{"override_frame_id": "lidar_link"}]
```

不要为了消除报错随意添加一条虚假的静态 TF。必须先确认消息数据实际相对于哪个物理坐标系产生，再让消息 Frame 与机器人模型保持一致。

`tf2_echo` 刚启动时短暂报告 Frame 不存在、随后持续输出正确变换，通常是 ROS 2 发现和 TF 数据尚未到达导致的瞬时现象；应根据后续是否稳定输出判断，而不是只看第一行。
