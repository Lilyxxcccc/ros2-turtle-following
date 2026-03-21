# ROS2 Turtle Following (TF-based)

## 项目介绍

基于 ROS2 TF 坐标变换，实现一个乌龟自动跟随系统。
通过监听 turtle1 与 turtle2 的相对位姿，实时生成速度控制指令，使 turtle2 平滑跟随 turtle1。

---

## 功能特点

* 基于 TF 实现坐标系转换（world → turtle）
* 使用 TransformListener 获取相对位姿
* 基于比例控制（P控制）实现跟随
* 支持参数调节：

  * 跟随距离（stop_distance）
  * 线速度增益（linear_gain）
  * 角速度增益（angular_gain）
* 限制最大速度，提升稳定性（防抖）

---

## 技术点

* ROS2 节点通信
* TF2 坐标变换（TransformBroadcaster / Listener）
* 几何计算（atan2 / 距离计算）
* 简单控制算法（P控制）

---

## 运行方式

```bash
ros2 launch py05_exercise exer01_turtle_follow.launch.xml
```

```bash
ros2 run turtlesim turtle_teleop_key
```

---

## 效果展示

![demo](images/demo.gif)

---

## 项目结构

```
ros2-turtle-following/
├── py05_exercise/ # ROS2 功能包
├── images/ # 项目演示 GIF
└── README.md
```

---

## 环境依赖

-Ubuntu 22.04

-ROS2 Humble

-Python3

-turtlesim

-tf2_ros

-geometry_msgs

-tf_transformations

---

## 系统组成

本项目包含 3 个核心节点：

1. `exer01_tf_spawn_py`
   - 调用 `/spawn` 服务生成 `turtle2`

2. `exer02_tf_broadcaster_py`
   - 订阅 `/turtle1/pose` 或 `/turtle2/pose`
   - 将乌龟位姿转换为 `world -> turtleX` 的 TF 坐标变换

3. `exer03_tf_listener_py`
   - 查询 `turtle1` 相对于 `turtle2` 的坐标变换
   - 根据相对位置计算速度指令并发布到 `turtle2/cmd_vel`

---

## 核心参数说明

- `target_frame`：跟随者坐标系，默认 `turtle2`
- `source_frame`：目标坐标系，默认 `turtle1`
- `stop_distance`：停止跟随的最小距离
- `linear_gain`：线速度比例增益
- `angular_gain`：角速度比例增益
- `max_linear_speed`：最大线速度
- `max_angular_speed`：最大角速度

---

## 项目收获

通过这个项目，我系统练习了：

- ROS2 Python 功能包的组织方式
- service / topic / TF 三种机制的配合使用
- 使用 TF2 处理坐标系变换
- 使用相对位姿实现简单的 P 控制跟随
- 使用 launch 文件组织多节点系统

---

## 项目亮点

- 使用 ROS2 TF2 构建多坐标系关系，而不是直接使用全局坐标控制
- 将 turtlesim 位姿封装为 TF 变换，体现机器人坐标系建模思路
- 使用比例控制实现目标跟随，并加入停止距离和速度限幅提升稳定性
- 使用 launch 文件一键启动完整系统，具备基本工程组织能力

---

## 后续优化方向

* PID 控制优化
* 多目标跟随
* RViz 可视化
