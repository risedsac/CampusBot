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
- 待完成：第一次人工 Git 提交。
