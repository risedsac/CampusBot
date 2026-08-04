# ROS 2 学习笔记

## 工作空间

colcon 工作空间用于组织多个 ROS 2 功能包。源码功能包放在 `src/` 中，构建会生成 `build/`、`install/` 和 `log/`。

## 功能包元数据

- `package.xml` 声明功能包名称、许可证、维护者和依赖关系。
- `CMakeLists.txt` 描述如何构建 `ament_cmake` 功能包，以及安装哪些运行时资源。

## BEGIN

### 各个文件的解释

| 文件 | 谁看 | 作用 |
|---|---|---|
| `CampusBot/README.md` | 你、GitHub 访客、面试官 | 项目首页、功能介绍、构建和演示方法 |
| `CampusBot/TODO.md` | 你和我 | 当前任务与后续任务 |
| `CampusBot/DAILY_PLAN.md` | 你 | 每日目标、步骤和验收结果 |
| `CampusBot/LEARNING_LOG.md` | 你 | 学到的知识、错误和薄弱点 |
| `CampusBot/DECISIONS.md` | 你、协作者、面试官 | 记录技术选择及其理由 |
| `CampusBot/docs/architecture.md` | 你、GitHub 访客 | 系统模块、依赖关系和数据流 |
| `CampusBot/docs/ros2_notes.md` | 你 | 与项目相关的 ROS 2 知识笔记 |
| `CampusBot/docs/troubleshooting.md` | 你和协作者 | 记录真实错误、原因和解决方法 |
| `CampusBot/docs/interview_notes.md` | 你 | 项目介绍、面试问题和追问 |
| `CampusBot/AGENTS.md` | Codex/代理 | 约束代理如何修改和测试项目 |

### 1. 为什么源码明明在 `src/`，`ros2 pkg prefix` 却返回 `install/`？

```text
CMake install 规则
         ↓
colcon 设置每个 package 的安装前缀
         ↓
ament_package() 注册 package 索引
         ↓
文件和索引进入 install/
         ↓
source install/setup.bash 更新查找环境
         ↓
ros2 pkg prefix 查询 ament 索引
```

不是简单地“CMake 固定把所有东西放进 install”，而是：

- CMake 描述要安装什么；
- colcon 决定 workspace 的安装前缀；
- ament 建立 ROS 2 package 索引；
- source 让当前终端能够找到这个索引。

### 2. git 的部分操作

```bash
git add .
git diff --cached --stat
git diff --cached --check
```

解释：

- `git add .`：把未被 `.gitignore` 排除的文件放入暂存区，不会提交或上传。
- `git diff --cached --stat`：查看准备提交的文件及变更规模。
- `git diff --cached --check`：检查尾随空格等格式问题；成功时通常没有输出。
- 三条命令都不会修改源码内容。

如果误执行 `git add .`，首次提交前可以使用：

```bash
git rm --cached -r .
```
