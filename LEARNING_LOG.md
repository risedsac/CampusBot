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
