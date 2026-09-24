# septentrio_gnss_driver · Septentrio ROS1/ROS2 驱动（ROSaic）操作手册

目录：[`PROJECTS.json` → `septentrio_gnss_driver`](../../PROJECTS.json) · 上游 <https://github.com/septentrio-gnss/septentrio_gnss_driver> · 包名 **`septentrio_gnss_driver`** · 版本 **1.4.8** · tip **`5613af2`**（2026-08-01）· 许可 **BSD-3-Clause** · 本机验证：clone + `package.xml`/`launch`/`config`/`msg` 清单；**无 `/opt/ros`、无 Septentrio 接收机 → 未 `colcon`/`catkin` 编译、未 `ros2 launch`、无 bag 回放** · 2026-09-24 05:15 EDT

> 岗位：把 **mosaic / AsteRx** 等 Septentrio GNSS（及 INS）经串口/TCP/UDP/USB（RNDIS）接入 **ROS1/ROS2**，发布导航与观测话题。冲突时：**上游 README / 仓内 `config/*.yaml` / 本机 `ros2 pkg` > 本文**。离线 SBF 块 → [sbfparser](./sbfparser.md) / [pysbf2](./pysbf2.md)；HAS 页→SSR → [haslib](./haslib.md)。**不是** 电离层 TEC/闪烁流水线。

## 1. 用途与边界

**做：**

- 单天线 GNSS / 双天线姿态 / INS：读 SBF（及部分 NMEA），按 `publish.*` 开关发 ROS 话题
- 连接：`serial:/dev/...`、`tcp://host:port`（默认 RNDIS `tcp://192.168.3.1:28784`）、UDP 静态服、USB；可选 `file_name:*.sbf` / `*.pcap` 回放（需本机有日志文件，**仓内无样例 bag/pcap**）
- 可选：驱动侧配置接收机（`configure_rx: true`）、多路 RTK 改正（NTRIP / IP / 串口）、OSNMA/AIM+ 状态、NED↔ENU 轴约定

**不做：**

- **不是** 离线批解析 SBF / 编解码库 → [sbfparser](./sbfparser.md)（Cython）/ [pysbf2](./pysbf2.md)（纯 Python）
- **不是** Galileo HAS→RTCM/IGS SSR → [haslib](./haslib.md)；**不是** ISMR 下载 → [ismr-downloader](./ismr-downloader.md)
- **不是** 发表级 PPP/TEC；机器人联调为主
- 本机共享 Linux **无 ROS distro、无接收机硬件** → 下列「可测 / 不可测」须遵守；**禁止臆造** `ros2 topic echo` / bag 回放 stdout

一句话：ROSaic = **Septentrio 官方 ROS 驱动（C++17，一仓双 ROS）**；电离层事后仍落盘 SBF/RINEX 再走离线栈。

| 术语 | 含义 |
| --- | --- |
| ROSaic | ROS + mosaic；本包对外名 `septentrio_gnss_driver` |
| SBF | Septentrio Binary Format；驱动主输入 |
| `configure_rx` | `true` 时驱动按 yaml 改接收机（会覆盖旧设置） |
| `device` | 主连接串：`tcp://` / `serial:` / `file_name:` |
| `publish.*` | 话题开关；默认并非全开 |

## 2. 安装（ROS1 / ROS2）

### 2.1 apt 二进制（有对应 distro 时）

```bash
# $ROS_DISTRO 例：noetic / humble / jazzy / iron / rolling
sudo apt-get update
sudo apt-get install ros-$ROS_DISTRO-septentrio-gnss-driver
```

上游说明：Melodic/Foxy/Galactic 等 EOL 发行版的二进制**不再更新**；要跟 tip 请源码编。

### 2.2 源码 · ROS 2（colcon）

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
sudo apt install \
  ros-${ROS_DISTRO}-nmea-msgs ros-${ROS_DISTRO}-gps-msgs \
  ros-${ROS_DISTRO}-gtest-vendor \
  libboost-all-dev libpcap-dev \
  libgeographic-dev   # Ubuntu 24.04+ 常为 libgeographiclib-dev

mkdir -p ~/septentrio/src && cd ~/septentrio/src
git clone https://github.com/septentrio-gnss/septentrio_gnss_driver.git
cd ~/septentrio
# tip master 已用 ament/catkin 双探测；旧 README 的 `git checkout ros2` 对统一仓可省略
colcon build --packages-up-to septentrio_gnss_driver
# 改 launch/config 热更：加 --symlink-install
source install/setup.bash   # 勿照抄旧 README 里的 devel/setup.bash（那是 ROS1）
```

### 2.3 源码 · ROS 1（catkin_tools）

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
sudo apt install ros-${ROS_DISTRO}-nmea-msgs ros-${ROS_DISTRO}-gps-common \
  libboost-all-dev libpcap-dev libgeographic-dev
# Melodic: python-catkin-tools；Noetic: python3-catkin-tools
mkdir -p ~/septentrio/src && cd ~/septentrio && catkin init
catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
cd src && git clone https://github.com/septentrio-gnss/septentrio_gnss_driver.git
cd ~/septentrio && rosdep install . --from-paths src -i -y
catkin build
source devel/setup.bash
```

依赖硬约束：**C++17**；`Boost`、`GeographicLib`、`libpcap`；消息包见上。

### 2.4 本机（文档仓）可做的核对 — **无 ROS / 无硬件**

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/septentrio-gnss/septentrio_gnss_driver.git
cd septentrio_gnss_driver
git rev-parse --short HEAD          # 期望 5613af2
grep -E '<version>|<name>|<license>' package.xml
ls launch/ config/ msg/ | sed 's/^/  /'
# launch: rover.launch  rover.launch.py  rover_node.launch.py
# config: gnss.yaml  ins.yaml  rover.yaml  rover_node.yaml
# msg: 26 个 .msg（PVT*/PosCov*/MeasEpoch/AIMPlusStatus…）

# 有 ROS 的机器上再冒烟：
#   source /opt/ros/$ROS_DISTRO/setup.bash
#   ros2 pkg list | grep septentrio
#   ros2 launch septentrio_gnss_driver rover.launch.py --show-args
#   # 或 ros2 pkg prefix septentrio_gnss_driver
```

**本机结果（tip `5613af2` / 1.4.8，2026-09-24 05:15 EDT）：** clone OK；`package.xml` name=`septentrio_gnss_driver` version=`1.4.8` license=BSD 3-Clause；launch×3、config×4、msg×26。**`which ros2` / `/opt/ros` 不存在** → 未编译、未 launch、未连 `192.168.3.1`、仓内无 `.sbf`/`.pcap`/`.bag` 样例 → **硬件/ROS 门禁，下列话题表来自上游 README + 默认 yaml，非本机 echo。**

## 3. 配置与启动

### 3.1 改 yaml（必做）

复制/改 `config/rover.yaml`（或 `gnss.yaml` / `ins.yaml` / `rover_node.yaml`）：

```yaml
device: tcp://192.168.3.1:28784   # 或 serial:/dev/serial/by-id/usb-Septentrio_...
# device: file_name:/path/to/log.sbf   # 回放时自动 use_gnss_time:=true
configure_rx: true                 # false → 须先在 Web UI 配好并保存
receiver_type: gnss                # INS 则改 ins + 杠杆臂
use_ros_axis_orientation: true     # Septentrio NED → ROS ENU
publish:
  gpsfix: true
  pvtgeodetic: true
  poscovgeodetic: true
  atteuler: true
  attcoveuler: true
  aimplusstatus: true
  navsatfix: false
  measepoch: false                 # 开则带宽陡增
```

串口用户须在 `dialout` 组；`hw_flow_control` / `ant_*_serial_nr` 等**必须是带引号的字符串**（见坑表）。

### 3.2 启动命令

```bash
# ROS 2 · composition（默认读 rover.yaml）
ros2 launch septentrio_gnss_driver rover.launch.py
ros2 launch septentrio_gnss_driver rover.launch.py file_name:=gnss.yaml
# ROS 2 · 普通 node（默认 rover_node.yaml）
ros2 launch septentrio_gnss_driver rover_node.launch.py file_name:=ins.yaml

# ROS 1（param 名无扩展名）
roslaunch septentrio_gnss_driver rover.launch param_file_name:=rover
roslaunch septentrio_gnss_driver rover.launch param_file_name:=gnss
```

> 上游 README 一处写成 `rover.py`，**仓内实文件是 `rover.launch.py`**；以 `ls launch/` 为准。

有硬件时核对：

```bash
ros2 topic list | rg 'pvtgeodetic|gpsfix|navsatfix|measepoch|aimplus'
ros2 topic echo /pvtgeodetic --once
# ROS1: rostopic echo /gpsfix
```

## 4. 期望话题 / 输出（默认 `rover.yaml` 为 true 者加粗）

| 话题 | 消息类型 | 对应 SBF/来源 | 默认 |
| --- | --- | --- | --- |
| **`/gpsfix`** | `gps_msgs/GPSFix`（ROS1: `gps_common`） | PVT+协方差+MeasEpoch+DOP+姿态等合成 | **开** |
| **`/pvtgeodetic`** | `…/PVTGeodetic` | `PVTGeodetic` | **开** |
| **`/poscovgeodetic`** | `…/PosCovGeodetic` | `PosCovGeodetic` | **开** |
| **`/velcovgeodetic`** | `…/VelCovGeodetic` | `VelCovGeodetic` | **开**（rover.yaml） |
| **`/atteuler`** `/attcoveuler` | AttEuler / AttCovEuler | 双天线/INS 姿态 | **开** |
| **`/aimplusstatus`** `/rfstatus` | AIM+/RF | AIM+ / `RFStatus` | **开** |
| `/navsatfix` | `sensor_msgs/NavSatFix` | PVT+PosCov（或 INSNavGeod） | 关 |
| `/measepoch` | `…/MeasEpoch` | 观测历元（带宽大） | 关 |
| `/gpgga` `/gprmc` `/gpgsa` `/gpgsv` | `nmea_msgs/*` | NMEA | 关 |
| `/localization` `/imu` `/tf` | Odometry / Imu / tf | **INS** 相关 | 关 |

组合消息（`gpsfix`/`navsatfix`）由**同历元最晚到达的块**触发；`publish_only_valid` 可滤无效 TOW。

## 5. 关键参数（嵌套：ROS2 用 `.`，ROS1 用 `/`）

| 参数 | 作用 | 冒烟默认 / 注意 |
| --- | --- | --- |
| `device` | 主链路 | `tcp://192.168.3.1:28784`；命令口常 **28784** |
| `serial.baudrate` | 串口波特率 | `921600`；开 MeasEpoch ≈需数百 kbit/s |
| `stream_device.tcp/udp` | 静态 IP server 收 SBF | 空则走 `device` |
| `configure_rx` | 是否改接收机 | `true` **会覆盖** 机内旧值 |
| `login.user/password` | 非匿名权限 | 默认可匿名全控 |
| `osnma.mode` | `off`/`loose`/`strict` | `strict` 要 NTP |
| `receiver_type` | `gnss` / `ins` | INS 须配杠杆臂或 tf |
| `use_ros_axis_orientation` | NED↔ENU | 接 `robot_localization` 时建议 `true` |
| `polling_period.pvt` / `.rest` | ms；`0`=OnChange | rover：`100` / `500` |
| `rtk_settings.ntrip_*` | 机内 NTRIP 客户 | id/caster/mount/user/pwd |
| `publish.*` | 话题开关 | 见 §4 |
| `leap_seconds` | 无 `ReceiverTime` 的文件回放 | README 示例 18；随 UTC 闰秒更新 |
| `activate_debug_log` | 调试日志 | `false` |

## 6. 接到哪步（离线对照）

```text
[接收机 live]
    │  SBF over TCP/serial
    ▼
septentrio_gnss_driver  ──ROS话题──►  机器人 / robot_localization / 监控
    │
    │  另：接收机 Web/SD 落盘 .sbf（或 PCAP）
    ▼
[sbfparser] / [pysbf2]  ──块 dict──►  质控 / 自研脚本
    │
    ├─ GALRawCNAV / HAS 相关块 ──► [haslib] → RTCM/IGS SSR → PPP
    └─ 转 RINEX（厂商工具 / autorino / teqc 等）──► 路径 A/B（georinex / pytecgg / ionomoni…）
```

- **只要 ROS 实时位姿/GPSFix**：停在本驱动。
- **要解析任意 SBF 字段、无 ROS**：直接 [sbfparser](./sbfparser.md) / [pysbf2](./pysbf2.md)，不必起驱动。
- **要 HAS 改正**：落盘含 C/NAV 的 SBF → [haslib](./haslib.md)（驱动默认话题**不含**完整 HAS 页管道）。
- 工作流 **C**：本驱动（车载/机载 Septentrio）↔ [rtkbase](./rtkbase.md)/[ntripstreams](./ntripstreams.md)/[bnc](./bnc.md) 差分侧。

## 7. 坑（≥8；现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 串口 Permission denied | 用户不在 `dialout` | `sudo adduser $USER dialout` 后重登 |
| 2 | `hw_flow_control` 读错 / 无效 | yaml 写成无引号 `off`（布尔） | 写成字符串 `"off"` 或 `"RTS\|CTS"` |
| 3 | 天线序列号告警 | 纯数字被当成 int | `ant_serial_nr: "12345"` 加引号 |
| 4 | 机内设置被清空/改乱 | `configure_rx: true` 会覆盖 | 预配置机：`configure_rx: false` + Web 保存；或接受驱动接管 |
| 5 | TCP 重连后无流 | 动态 `device: tcp://` 会话 id 变 | 预配置 + `stream_device.tcp.ip_server`/`port` 静态服 |
| 6 | `/gpsfix` 空或卡 | MeasEpoch 等块未开 / 波特率不够 | 开相关 `publish`；串口提速；查 `polling_period` |
| 7 | 航向与 Web GUI 差 90°/符号反 | NED vs ENU | 调 `use_ros_axis_orientation`；与 GUI 对照时用 `false` |
| 8 | ROS2 launch 找不到 `rover.py` | README 旧名 | 用 **`rover.launch.py`** / `rover_node.launch.py` |
| 9 | `git checkout ros2` 困惑 | 旧双分支文档；现 **master 统一仓** | tip 直接 clone；CMake 按 ament/catkin 分支 |
| 10 | 文件回放时间戳错乱 | 无 `ReceiverTime` 且未设闰秒 | 设 `leap_seconds`；或录块时包含 ReceiverTime |
| 11 | UDP/USB 块重复 | 旧固件已知问题 | GNSS≥4.14 / INS≥1.4.1；或改 TCP |
| 12 | 当 TEC/闪烁工具用 | 驱动只做 ROS 导航话题 | 落盘 SBF→[sbfparser](./sbfparser.md)/[pysbf2](./pysbf2.md)/[haslib](./haslib.md)/ISMR 链 |
| 13 | 多路 NTRIP `keep_open: false` 关不干净 | 关端口需数秒 | 加大 launch `sigterm_timeout`（例 10–20） |
| 14 | 本机无 ROS 却期待 `ros2 pkg` | 环境门禁 | 先装 distro；本文 §2.4 只验仓结构 |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| Septentrio **实时**进 ROS1/ROS2 | **本文 septentrio_gnss_driver** |
| 离线/脚本解析 SBF（快） | [sbfparser](./sbfparser.md) |
| 离线/纯 Python 编解码 SBF（同 pyubx2 栈） | [pysbf2](./pysbf2.md) |
| SBF/BINEX → HAS SSR | [haslib](./haslib.md) |
| Pi 基站 Web + NTRIP（可含 Mosaic） | [rtkbase](./rtkbase.md) |
| u-blox ROS2 | 列表 `ublox_dgnss`（尚未短硬） |
| Swift SBP ROS2 | 列表 `swiftnav-ros2` / `libsbp`（尚未短硬） |

## 9. 相关

[sbfparser](./sbfparser.md) · [pysbf2](./pysbf2.md) · [haslib](./haslib.md) · [rtkbase](./rtkbase.md) · [ntripstreams](./ntripstreams.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [autorino](./autorino.md) · [ismr-downloader](./ismr-downloader.md) · [README](./README.md)

- 上游：<https://github.com/septentrio-gnss/septentrio_gnss_driver>
- 支持：Septentrio Customer Support；固件建议 GNSS ≥4.10.0、INS ≥1.3.2（OSNMA/PTP 等见 README 版本表）
- 许可：BSD-3-Clause
