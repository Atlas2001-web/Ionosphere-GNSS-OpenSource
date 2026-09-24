# ublox_driver · 港科大 ZED-F9P ROS1 驱动操作手册

目录：[`PROJECTS.json` → `ublox_driver`](../../PROJECTS.json) · 上游 <https://github.com/HKUST-Aerial-Robotics/ublox_driver> · **URL 已核**（HTTP 200）· 包名 **`ublox_driver`** · 版本 **1.0.0** · tip **`7961ab7`**（2024-05-14 01:31 EDT；修 GPS subframe 索引）· 许可 **GPLv3** · 可执行 **`ublox_driver`** / **`sync_system_time`** · 本机验证：clone + `package.xml` / `launch`×1 / `config`×2 / `CMakeLists` exec×2 / 源码 `advertise` 话题表；**无 `/opt/ros`、无 u-blox 串口接收机 → 未 `catkin_make`、未 `roslaunch`、无 `rostopic echo`** · 2026-09-24 05:43 EDT

> 岗位：把 **u-blox（主测 ZED-F9P）** 串口/文件 UBX 流接入 **ROS 1（catkin）**，发与 **gnss_comm / GVINS** 对齐的原始测量与 PVT 话题。冲突时：**上游 README / 仓内 `config/driver_config.yaml` / `launch/ublox_driver.launch` > 本文**。离线 UBX 编解码 → [pyubx2](./pyubx2.md)；ROS 2 USB-UBX（F9/X20P）→ [ublox-dgnss](./ublox-dgnss.md)。**不是** 电离层 TEC/闪烁流水线，也**不是** 测地级 PPP 引擎。

## 1. 用途与边界

**做：**

- ROS **1**（README 开发环境：**Kinetic**；`package.xml` 为 catkin，**无** ament/ROS 2）
- 输入：`online:=1` 串口（默认 `/dev/ttyACM0` @ **921600**）；或 `online:=0` 回放 `.ubx`（速度由 `serial_baud_rate` 控）
- 接收机侧至少开：`UBX-RXM-RAWX`、`UBX-RXM-SFRBX`、`UBX-NAV-PVT`（样例 u-center 配置：`config/ucenter_config_f9p_gvins.txt`）
- 输出（`to_ros:=1`）：私有命名空间话题（节点名 `ublox_driver` → 前缀 `/ublox_driver/`）；可选 `to_file` 落盘、`to_serial` 转发
- 可选 RTK：`input_rtcm:=1`，从本机 TCP **`rtcm_tcp_port`（默认 3503）** 把 RTCM 灌进接收机（README 用 [rtklib](./rtklib.md) `str2str` 做 NTRIP→TCP）

**不做：**

- **不是** ROS 2 / USB composition 驱动 → [ublox-dgnss](./ublox-dgnss.md)
- **不是** 纯 Python UBX 编解码 / 无 ROS CLI → [pyubx2](./pyubx2.md)（+ [pygnssutils](./pygnssutils.md) `gnssstreamer`）
- **不是** Septentrio / Swift 品牌驱动 → [septentrio-gnss-driver](./septentrio-gnss-driver.md) / [swiftnav-ros2](./swiftnav-ros2.md)
- **不是** UBX→RINEX 批转换 → [ubx2rinex](./ubx2rinex.md)
- **无 ROS1 / 无 Rx**：**禁止臆造** `rostopic echo` / bag / 实时 `/receiver_lla` stdout
- 启动时改接收机 CFG：`config_receiver_at_start` 在 yaml 存在，但 README Todo 与注释写明 **NOT SUPPORT YET**

一句话：ublox_driver = **港科大空中机器人组 ROS1 ZED-F9P→gnss_comm 话题桥**；协议真相可离线对照 [pyubx2](./pyubx2.md)。

| 术语 | 含义 |
| --- | --- |
| 包名 / 节点名 | 均为 `ublox_driver`；`ros::NodeHandle nh("~")` → 话题在 `/ublox_driver/...` |
| `gnss_comm` | 兄弟仓消息定义（`GnssPVTSolnMsg`/`GnssMeasMsg`/…）；**本包无 `.msg`** |
| `online` | `1` 串口实时 / `0` 文件回放 |
| `input_rtcm` | `1` 时连 `localhost:rtcm_tcp_port` 取 RTCM 写入串口 |
| `carr_soln` | `/receiver_pvt` 字段；README：`2` = RTK fix |
| `sync_system_time` | 另可执行；订 `/ublox_driver/receiver_lla` 粗同步系统钟（需 root + 改 `UTC_OFFSET`） |

## 2. 安装（有 ROS 1 的机器）

### 2.1 依赖

```bash
# ROS Kinetic（或兼容 catkin 发行版）已 source
sudo apt-get install -y libboost-all-dev libgoogle-glog-dev libeigen3-dev
# 串口权限（一次）
sudo usermod -aG dialout $USER   # 重登生效
```

另需先编 **[gnss_comm](https://github.com/HKUST-Aerial-Robotics/gnss_comm)**（同工作区 `src/`）。CMake 还 `find_package(Glog REQUIRED)` + Eigen3（README 钉 Eigen **3.3.3** 习惯值；本机 apt Eigen 通常可用）。

### 2.2 catkin

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash   # 例：kinetic / noetic
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/HKUST-Aerial-Robotics/gnss_comm.git
git clone https://github.com/HKUST-Aerial-Robotics/ublox_driver.git
cd ~/catkin_ws && catkin_make
source devel/setup.bash
```

### 2.3 本机（文档仓）可做的核对 — **无 ROS / 无硬件**

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/HKUST-Aerial-Robotics/ublox_driver.git
cd ublox_driver
git rev-parse --short HEAD          # 期望 7961ab7
grep -E '<name>|<version>|<license>' package.xml
# name=ublox_driver  version=1.0.0  license=GPLv3
ls launch/ config/
# launch/ublox_driver.launch
# config/driver_config.yaml  ucenter_config_f9p_gvins.txt
rg -n 'add_executable' CMakeLists.txt
# ublox_driver · sync_system_time
rg -n 'advertise<' src/ublox_message_processor.cpp
rg -n 'NodeHandle' src/ublox_driver.cpp   # nh("~")
test -d /opt/ros && echo HAS_ROS || echo NO_ROS
find . -name '*.msg' -o -name '*.ubx' -o -name '*.bag' | wc -l   # 0
# 有 ROS1 后再：
#   rospack find ublox_driver
#   roslaunch ublox_driver ublox_driver.launch
#   rostopic echo /ublox_driver/receiver_lla
```

**本机结果（tip `7961ab7` / 1.0.0，2026-09-24 05:43 EDT）：** clone OK；`package.xml` name=`ublox_driver` version=`1.0.0` license=GPLv3；launch×**1**、config×**2**（yaml+u-center txt）、本包 **msg×0**（消息在 gnss_comm）；exec **`ublox_driver`** + **`sync_system_time`**；`advertise`×**7**（见 §4）。**`which ros2`/`roslaunch` / `/opt/ros` 不存在** → 未 `catkin_make`、未 launch、未插 `/dev/ttyACM0`、仓内**无** `.ubx`/`.bag` → **硬件/ROS 门禁**；下列话题表来自源码 `advertise` + README，**非本机 echo**。

## 3. 配置与启动

### 3.1 改 `config/driver_config.yaml`（必做）

仓内默认（节选）：

```yaml
online: 1
input_serial_port: "/dev/ttyACM0"
serial_baud_rate: 921600
input_rtcm: 0
rtcm_tcp_port: 3503
config_receiver_at_start: 0     # NOT SUPPORT YET
ubx_filepath: "~/tmp/ublox_driver_test/2020_11_30_7_14_33.ubx"
rtk_correction_ecef:
    rows: 3
    cols: 1
    dt: d
    data: [ 0, 0, 0 ]
to_ros: 1
to_file: 0
dump_dir: "~/tmp/ublox_driver_test/"
to_serial: 0
output_serial_port: "/dev/ttyACM0"
```

### 3.2 在线接收机（有 ROS1 + 已 u-center 配好）

```bash
# 先确认串口与 dialout
ls -l /dev/ttyACM0
roslaunch ublox_driver ublox_driver.launch
# 可选换配置：
# roslaunch ublox_driver ublox_driver.launch config_path:=/path/to/my.yaml
```

### 3.3 可选 RTCM（内部 RTK 引擎，如 F9P）

```bash
# 另终端：NTRIP → 本机 TCP 3503（例；凭据自备）
# ./str2str -in ntrip://USER:PASS@host:port/MOUNT -out tcpsvr://:3503
# yaml: input_rtcm: 1 后 relaunch
# README：/ublox_driver/receiver_pvt 的 carr_soln==2 → RTK fix
```

### 3.4 回放 `.ubx`

```bash
# yaml: online: 0 ; ubx_filepath: "/path/to/log.ubx"
roslaunch ublox_driver ublox_driver.launch
# 回放速率受 serial_baud_rate 控制
```

### 3.5 粗同步系统时间（可选）

```bash
# 先改 src/sync_system_time.cpp 的 constexpr UTC_OFFSET（默认 8）并重编
sudo su
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/catkin_ws/devel/setup.bash
rosrun ublox_driver sync_system_time
# 订 /ublox_driver/receiver_lla；有效 PVT 后写 CLOCK_REALTIME
```

## 4. 话题（源码 `advertise`；**非本机 echo**）

节点 `ublox_driver` + `NodeHandle("~")` → 全名带 `/ublox_driver/` 前缀。消息类型来自 **gnss_comm**（除 `NavSatFix`）。

| 相对名 | 全名 | 类型（仓内符号） | 来源 UBX（README） |
| --- | --- | --- | --- |
| `receiver_pvt` | `/ublox_driver/receiver_pvt` | `GnssPVTSolnMsg` | NAV-PVT（含 `carr_soln`） |
| `receiver_lla` | `/ublox_driver/receiver_lla` | `sensor_msgs/NavSatFix` | 由 PVT 合成 |
| `time_pulse_info` | `/ublox_driver/time_pulse_info` | `GnssTimePulseInfoMsg` | 时间脉冲相关 |
| `range_meas` | `/ublox_driver/range_meas` | `GnssMeasMsg` | RXM-RAWX |
| `ephem` | `/ublox_driver/ephem` | `GnssEphemMsg` | RXM-SFRBX→GPS/Gal/… |
| `glo_ephem` | `/ublox_driver/glo_ephem` | `GnssGloEphemMsg` | RXM-SFRBX→GLO |
| `iono_params` | `/ublox_driver/iono_params` | `StampedFloat64Array` | 电离层参数（子帧） |

冒烟模板（有硬件 + ROS1）：`rostopic echo /ublox_driver/receiver_lla` · `/ublox_driver/receiver_pvt` · `/ublox_driver/range_meas`。部分话题在无 GNSS 锁定前可能静默（README 明示）。

## 5. 关键参数

| 参数 | 作用 | 冒烟注意 |
| --- | --- | --- |
| `online` | 串口 / 文件 | 回放务必 `0` + 有效 `ubx_filepath` |
| `input_serial_port` / `serial_baud_rate` | 串口与波特 | 须与 u-center 一致；回放时 baud 控速度 |
| `input_rtcm` / `rtcm_tcp_port` | RTCM TCP 入 | 默认 3503；无 `str2str` 时保持 `0` |
| `rtk_correction_ecef` | 基站 ECEF 偏置改正 | 3×1；RTCM 基站坐标偏时用 |
| `to_ros` / `to_file` / `to_serial` | 三路输出开关 | 可同时开 |
| `dump_dir` / `ubx_filepath` | 落盘 / 回放路径 | `~` 展开依赖参数解析；路径不存在则起不来 |
| `config_receiver_at_start` | 启动写 CFG | **尚未支持**；继续用 u-center |

## 6. 接到哪步

```text
[u-blox ZED-F9P 串口 / .ubx 文件]
    │  UBX (RAWX/SFRBX/PVT)  (+ 可选 RTCM@TCP)
    ▼
ublox_driver ──/ublox_driver/*──► gnss_comm / GVINS / 监控
    ├─ 离线 UBX 编解码 ──► [pyubx2] / [pygnssutils]
    ├─ UBX→RINEX 落盘 ──► [ubx2rinex]
    ├─ 要 ROS 2 USB 驱动 ──► [ublox-dgnss]（换栈，勿混 catkin/colcon）
    ├─ Septentrio / Swift ──► 换品牌 ROS 驱动
    └─ 测地 PPP/TEC ──► 落盘 RINEX 后再走 [georinex] / [rtklib] / …
```

- **只要 ROS1 + GVINS/gnss_comm 原始量**：停在本驱动。
- **只要协议/无 ROS**：直接 [pyubx2](./pyubx2.md)。
- **要 ROS2 USB HP/NTRIP 节点**：用 [ublox-dgnss](./ublox-dgnss.md)，不要硬把本包当 ROS2。

## 7. 坑（≥8；现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 打不开 `/dev/ttyACM*` | 无 `dialout` | `usermod -aG dialout` 后重登 |
| 2 | `roslaunch` 找不到包 | 未 source / 未编 gnss_comm | 同 ws 先编 gnss_comm，再 `source devel` |
| 3 | 话题全空 | 接收机未开 RAWX/SFRBX/PVT | 用 u-center 灌 `ucenter_config_f9p_gvins.txt` 同类配置 |
| 4 | 仅 LLA/PVT 有、无 `range_meas` | 无 RAW 或未锁定 | 查天线/天空；确认 RAWX 输出 |
| 5 | `carr_soln` 永非 2 | 无 RTCM / 错 mount | `input_rtcm:1` + `str2str`→3503；核 NTRIP |
| 6 | 当 ROS2 包 `colcon` | 本包是 **catkin ROS1** | 换 [ublox-dgnss](./ublox-dgnss.md) 或装 ROS1 |
| 7 | `config_receiver_at_start:1` 无效 | 功能未实现 | 保持 0；CFG 用 u-center |
| 8 | 回放极慢/极快 | `serial_baud_rate` 控速 | 调 yaml 波特（非真实串口时） |
| 9 | `sync_system_time` 时区错 | `UTC_OFFSET` 硬编码 | 改宏重编；需 root |
| 10 | 缺 Glog/Eigen 链接失败 | CMake `REQUIRED` | 装 `libgoogle-glog-dev` + Eigen3 |
| 11 | 本机无 ROS 却期待 `rostopic` | 环境门禁 | 先装 ROS1；本文 §2.3 只验仓结构 |
| 12 | 当 TEC/PPP 引擎用 | 只是实时驱动 | 落盘再走离线栈；协议试验用 [pyubx2](./pyubx2.md) |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| ZED-F9P **ROS1** + gnss_comm/GVINS | **本文 ublox_driver** |
| F9/X20P **ROS2** USB-UBX / NTRIP 节点 | [ublox-dgnss](./ublox-dgnss.md) |
| UBX 编解码 / 无 ROS | [pyubx2](./pyubx2.md) |
| UBX→RINEX CLI | [ubx2rinex](./ubx2rinex.md) |
| Septentrio / Swift 实时 ROS | [septentrio-gnss-driver](./septentrio-gnss-driver.md) / [swiftnav-ros2](./swiftnav-ros2.md) |
| 系统级 NMEA/JSON 守护 | [gpsd](./gpsd.md) |

## 9. 相关

[ublox-dgnss](./ublox-dgnss.md) · [pyubx2](./pyubx2.md) · [ubx2rinex](./ubx2rinex.md) · [septentrio-gnss-driver](./septentrio-gnss-driver.md) · [swiftnav-ros2](./swiftnav-ros2.md) · [gpsd](./gpsd.md) · [rtklib](./rtklib.md) · [pygnssutils](./pygnssutils.md) · [README](./README.md)

- 上游：<https://github.com/HKUST-Aerial-Robotics/ublox_driver>
- 消息仓：<https://github.com/HKUST-Aerial-Robotics/gnss_comm>
- 接口说明：README 链 UBX-18010854（ZED-F9P）
- 许可：GPLv3（星历解析多处改编自 RTKLIB，见源码头注释 BSD-2）
