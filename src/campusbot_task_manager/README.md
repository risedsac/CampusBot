# CampusBot 任务管理功能包

该功能包将逐步实现任务状态发布、多目标导航调度、超时、重试、取消和结果记录。

当前已实现两个用于学习 ROS 2 基本通信的 C++ 节点：

- `task_status_publisher`：以约 1 Hz 向 `/campusbot/task_status` 发布 `std_msgs/msg/String` 消息。
- `task_status_subscriber`：订阅同一 Topic 并在回调中输出收到的消息。

这两个节点是任务管理功能的学习基础，尚不是完整的多目标导航任务管理器。

## 当前验证方式

在工作空间根目录构建并加载环境后，分别运行：

```bash
ros2 run campusbot_task_manager task_status_publisher
ros2 run campusbot_task_manager task_status_subscriber
```

也可以直接检查 Topic：

```bash
ros2 topic info /campusbot/task_status --verbose
ros2 topic echo /campusbot/task_status --once
```
