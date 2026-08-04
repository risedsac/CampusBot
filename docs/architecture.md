# 系统架构

规划中的高层数据流：

```text
Gazebo Fortress 与机器人模型
              ↓
ROS 2 Topic、TF 与里程计
              ↓
slam_toolbox / 地图服务器 / AMCL
              ↓
Nav2 导航栈
              ↓
CampusBot 任务管理器与规划器
              ↓
自动化评测与结果分析
```

当前里程碑只建立了仓库与功能包边界，图中的功能尚未实现。
