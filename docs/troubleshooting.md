# 故障排查记录

## `ros2 --version` 报告未知参数

ROS 2 Humble 的命令行工具没有全局 `--version` 选项。可以改为检查 `ROS_DISTRO`、功能包前缀或系统已安装的软件包版本。

## GUI 检查在自动化终端中失败

沙箱可能没有暴露桌面显示服务或 GPU 设备节点。诊断显卡驱动前，应先在普通桌面终端中重新验证 RViz2 和 Gazebo GUI。

## CMake 报告 `Expected a command name`

CMake 注释以 `#` 开头，不能使用 C++ 的 `//`。没有 `#` 的普通说明文字也会被当成 CMake 命令，从而导致配置失败。

## colcon 警告所选功能包已经存在于 underlay

如果重新构建当前工作空间前已经 source 了它自己的 `install/setup.bash`，就可能出现该警告。应打开新终端，只 source `/opt/ros/humble/setup.bash`，构建成功后再 source 项目 overlay。不要习惯性使用 `--allow-overriding` 隐藏警告。
