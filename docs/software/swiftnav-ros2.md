# swiftnav-ros2 · Swift Navigation 官方 ROS 2 SBP 驱动操作手册

目录：[`PROJECTS.json` → `swiftnav-ros2`](../../PROJECTS.json) · 上游 <https://github.com/swift-nav/swiftnav-ros2> · **URL 已核** · ROS 包名 **`swiftnav_ros2_driver`**（≠ 仓库名连字符）· 版本 **1.0.0** · tip **`c35c6ef`**（2024-07-22；**main tip，比 tag `v1.0.0`=`5c82573` 超前 4 commit**；`package.xml` 仍 **1.0.0**）· 许可 **MIT** · 可执行文件 **`sbp-to-ros`** · 本机验证：clone + `package.xml` / `launch/start.py` / `config/settings.yaml` / `msg/Baseline.msg` 清单；**无 `/opt/ros`、无 Swift 接收机 → 未 `colcon`、未 `ros2 launch`、无 topic echo** · 2026-09-24 05:32 EDT · **质检复跑** 2026-09-24 05:42 EDT（tip/`package.xml`/launch×1/config×1/msg×1/`sbp-to-ros`/`settings.yaml` 键一致；Docker 文档仍写 `params.yaml`；**NO_ROS**）

> 岗位：把 **Piksi Multi / Duro / PGM EVK / Starling** 等 Swift GNSS（及 INS）经 **SBP**（TCP / 串口 / `.sbp` 回放）接入 **ROS 2**，发导航与专有 baseline 话题。冲突时：**上游 README / 仓内 `config/settings.yaml` / 本机 `ros2 pkg` > 本文**。协议编解码 → [libsbp](./libsbp.md)；现场串口/刷机 → [piksi-tools](./piksi-tools.md)；Septentrio ROS 对照 → [septentrio-gnss-driver](./septentrio-gnss-driver.md)。**不是** 电离层 TEC/闪烁流水线。

## 1. 用途与边界

**做：**

- ROS 2（README：**Humble** 主测；亦称支持 Foxy / Galactic；Ubuntu 22.04 / 20.04）
- 输入：Swift **SBP** 流——`interface`：`1` TCP Client / `2` Serial / `3` File 回放
- 输出：标准话题 + 专有 `Baseline.msg`；可选把入流 SBP 落盘
- 依赖系统库：C 版 **libsbp**（README 钉 **v4.11.0**）+ **libserialport**

**不做：**

- **不是** SBP 协议库本体 → [libsbp](./libsbp.md)（PyPI `sbp` / `sbp2json`；本驱动链的是 **C libsbp**，版本与 PyPI tip 可不一致）
- **不是** 现场配置/刷机 CLI → [piksi-tools](./piksi-tools.md)
- **不是** 多品牌 / Septentrio ROS → [septentrio-gnss-driver](./septentrio-gnss-driver.md)；**不是** 精密 PPP/TEC
- **无 ROS / 无 Rx**：**禁止臆造** `ros2 topic echo` / bag / 实时 NED stdout

一句话：swiftnav-ros2 = **Swift 官方 ROS 2 SBP→话题桥**；协议真相在 libsbp，现场壳在 piksi_tools。

| 术语 | 含义 |
| --- | --- |
| 仓库名 | `swiftnav-ros2`（GitHub 连字符） |
| ROS 包名 | **`swiftnav_ros2_driver`**（`package.xml` / ament） |
| `sbp-to-ros` | `CMakeLists.txt` 可执行目标；launch 里 `executable` |
| SBP | Swift Binary Protocol；帧头 preamble=`0x55` |
| `interface` | `1` TCP / `2` 串口 / `3` 文件回放 |
| `enabled_publishers` | 话题开关列表；名即话题名（见 §4） |

## 2. 安装（有 ROS 的机器）

### 2.1 钉 C libsbp（README Step 2）

```bash
git clone https://github.com/swift-nav/libsbp.git && cd libsbp
git checkout v4.11.0
cd c && git submodule update --init --recursive
mkdir build && cd build
# 上游 README 写作 `cmake DCMAKE_...`（缺 -）；正确为：
cmake -DCMAKE_CXX_STANDARD=17 -DCMAKE_CXX_STANDARD_REQUIRED=ON \
  -DCMAKE_CXX_EXTENSIONS=OFF ..
make && sudo make install   # 默认进 /usr/local；驱动 CMake 链此路径
```

> 与本目录 [libsbp](./libsbp.md) 的 **PyPI `sbp` 6.5.2** 是两条线：ROS 驱动按 README 钉 **C v4.11.0**；Python 离线解码用 pip 即可，不必混装进同一 prefix。

### 2.2 工作区 + 依赖 + colcon

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash   # 例：humble
mkdir -p ~/swiftnav_ws/src && cd ~/swiftnav_ws/src
git clone https://github.com/swift-nav/swiftnav-ros2.git
cd ~/swiftnav_ws
sudo apt-get update && sudo apt-get install -y libserialport-dev
rosdep install --from-paths src --ignore-src -r -y
# 先改 src/swiftnav-ros2/config/settings.yaml（§3）再编
colcon build
source install/setup.bash
```

可选 Docker：仓内 `docs/build-in-docker.md`（文中仍写 `config/params.yaml`——**实文件是 `settings.yaml`**，以 `ls config/` 为准）。

### 2.3 本机（文档仓）可做的核对 — **无 ROS / 无硬件**

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/swift-nav/swiftnav-ros2.git
cd swiftnav-ros2
git rev-parse --short HEAD          # 期望 c35c6ef
grep -E '<version>|<name>|<license>' package.xml
# name=swiftnav_ros2_driver  version=1.0.0  license=MIT
ls launch/ config/ msg/
# launch/start.py  config/settings.yaml  msg/Baseline.msg
grep -E 'package=|executable=' launch/start.py
# package='swiftnav_ros2_driver'  executable='sbp-to-ros'
test -d /opt/ros && echo HAS_ROS || echo NO_ROS
# 有 ROS 后再：
#   ros2 pkg list | grep swiftnav
#   ros2 launch swiftnav_ros2_driver start.py --show-args
```

**本机结果（tip `c35c6ef` / 1.0.0，写作 05:32 / **质检复跑** 05:42 EDT）：** clone OK；`package.xml` name=`swiftnav_ros2_driver` version=`1.0.0` license=MIT；launch×**1**（`start.py`）、config×**1**（`settings.yaml`）、msg×**1**（`Baseline.msg`）；可执行名 **`sbp-to-ros`**；`git rev-parse v1.0.0` → **`5c82573`**（tip 超前 4 commit：Galactic 编译修复等）。**`which ros2` / `/opt/ros` 不存在** → 未 `colcon`、未 launch、未连 `192.168.0.222:55556`、仓内**无** `.sbp`/`.bag` 样例 → **硬件/ROS 门禁**；下列话题表来自上游 README + `settings.yaml` + `publisher_factory.cpp`，**非本机 echo**。

## 3. 配置与启动

### 3.1 改 `config/settings.yaml`（必做）

默认（仓内实文件，节选）：

```yaml
swiftnav_ros2_driver:
  ros__parameters:
    interface: 1                 # 1 TCP / 2 Serial / 3 File
    host_ip: "192.168.0.222"
    host_port: 55556
    read_timeout: 2000           # ms
    write_timeout: 2000
    device_name: "/dev/ttyUSB0"
    connection_str: "115200|N|8|1|N"   # 波特|校验|数据位|停止位|流控
    sbp_file: "/home/swiftnav/ros2logs/sample-drive.sbp"  # interface=3；须绝对路径
    frame_name: "swiftnav-gnss"
    timestamp_source_gnss: True  # True=接收机 UTC；False=主机钟
    baseline_dir_offset_deg: 0.0
    baseline_dip_offset_deg: 0.0
    track_update_min_speed_mps: 0.2
    enabled_publishers:
      ["gpsfix", "navsatfix", "twistwithcovariancestamped",
       "baseline", "timereference", "imu"]
    log_sbp_messages: False
    log_sbp_filepath: "/home/swiftnav/ros2logs"
```

串口用户须在 `dialout`；`connection_str` 流控：`N`/`X`/`R`/`D`（见 README）。改源码树内 yaml 后需 **重新 `colcon build`**；或直接改 `install/swiftnav_ros2_driver/share/swiftnav_ros2_driver/config/settings.yaml`（免重编）。

### 3.2 启动（有 ROS + 已 source install）

```bash
source install/setup.bash
ros2 launch swiftnav_ros2_driver start.py
# 新终端 echo 专有消息前仍须 source install（Baseline 非标准库）
ros2 topic echo /baseline
# 有硬件时再：
# ros2 topic list | rg 'gpsfix|navsatfix|baseline|imu|timereference|twist'
# ros2 topic echo /gpsfix --once
# ros2 topic echo /navsatfix --once
```

> **门禁：** 上列 `echo`/`topic list` 为有 ROS/硬件时的操作模板；**本文档机未跑，无 stdout。**

接收机侧：专口只开驱动所需 SBP（降延迟）。README 列消息 ID：`97,258,259,520,524,529,530,545,2304,2305,65287`（MEASUREMENT STATE / GPS·UTC TIME / DOPS / BASELINE NED / POS·VEL LLH/NED COV / ORIENT EULER / IMU RAW·AUX / GNSS TIME OFFSET）。Piksi/Duro 用 Swift Console；Starling 在 yaml `enabled-messages` 里写同组 ID。

## 4. 期望话题（`enabled_publishers` 名 = 话题名）

| 话题 | 消息类型 | 关键 SBP（README） | 默认 |
| --- | --- | --- | --- |
| **`/gpsfix`** | `gps_msgs/msg/GPSFix` | GPS TIME 258、POS LLH COV 529、VEL NED COV 530；可选 UTC 259、ORIENT 545、DOPS 520 | **开** |
| **`/navsatfix`** | `sensor_msgs/msg/NavSatFix` | POS LLH COV 529；可选 UTC、MEASUREMENT STATE 97 | **开** |
| **`/twistwithcovariancestamped`** | `geometry_msgs/msg/TwistWithCovarianceStamped` | VEL NED COV 530（NED→ENU：`x=east,y=north,z=-down`） | **开** |
| **`/baseline`** | `swiftnav_ros2_driver/msg/Baseline`（专有） | BASELINE NED 524；mode：0 无效 / 3 Float / 4 Fixed | **开** |
| **`/timereference`** | `sensor_msgs/msg/TimeReference` | GPS TIME 258（+UTC） | **开** |
| **`/imu`** | `sensor_msgs/msg/Imu` | IMU RAW 2304、IMU AUX 2305（+时间偏置等） | **开** |

证据：`src/publishers/publisher_factory.cpp` 中 `topic = publisher.name`（`gpsfix`/`navsatfix`/…）；`msg/Baseline.msg` 字段含 `baseline_n_m`/`baseline_dir_deg`/`mode` 等。关某个 publisher：从 `enabled_publishers` **删行或注释**。DR 位置在 `gpsfix`/`navsatfix` 的 status 中按 README 报为 `STATUS_FIX`(0)。

## 5. 关键参数

| 参数 | 作用 | 冒烟注意 |
| --- | --- | --- |
| `interface` | 1/2/3 | 默认可 TCP；无网口改串口或文件 |
| `host_ip` / `host_port` | TCP | 默认 `192.168.0.222:55556` |
| `device_name` / `connection_str` | 串口 | `115200\|N\|8\|1\|N`；提 IMU/观测带宽须升波特率 |
| `sbp_file` | 回放 | **绝对路径**；按读文件速率，非实时 |
| `frame_name` | `header.frame_id` / TimeReference.source | 默认 `swiftnav-gnss` |
| `timestamp_source_gnss` | 头戳来源 | `True` 需 UTC TIME；否则退主机钟 |
| `track_update_min_speed_mps` | GPSFix.track 冻结阈 | 默认 `0.2`；低速航迹冻旧值 |
| `baseline_*_offset_deg` | RTK 方位/倾角偏置 | float；装车校准 |
| `enabled_publishers` | 话题开关 | 见 §4 |
| `log_sbp_messages` / `log_sbp_filepath` | 原始 SBP 录盘 | 目录绝对路径；文件名自动带时间戳 |

## 6. 接到哪步

```text
[Swift Rx / Starling live]
    │  SBP over TCP/serial
    ▼
swiftnav_ros2_driver (sbp-to-ros) ──ROS 话题──► 机器人 / robot_localization / 监控
    │
    ├─ 现场配置/刷机/串口日志 ──► [piksi-tools]
    ├─ 离线 .sbp / JSON 解码   ──► [libsbp]（sbp2json / Python）
    └─ 差分/NTRIP 侧（非本包）──► [ntripstreams]/[pygnssutils]/[bnc]/[rtkbase]
         落盘 RINEX 后再走路径 A/B（georinex / pytecgg / …）
```

- **只要 ROS 实时位姿 / GPSFix / baseline**：停在本驱动。
- **只要协议/无 ROS**：直接 [libsbp](./libsbp.md) / [piksi-tools](./piksi-tools.md)，不必起驱动。
- **Septentrio 机**：换 [septentrio-gnss-driver](./septentrio-gnss-driver.md)，不要硬套本包。

## 7. 坑（≥8；现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ros2 launch` 找不到包 | 包名是下划线 | 用 **`swiftnav_ros2_driver`**，不是仓库名 `swiftnav-ros2` |
| 2 | `sbp-to-ros` / 链接失败找不到 `sbp` | 未装 C libsbp 或前缀不对 | 按 §2.1 装 **v4.11.0** 到 `/usr/local`；查 `ldconfig -p \| rg sbp` |
| 3 | README `cmake DCMAKE_...` 失败 | 缺 `-D` | 写成 **`cmake -DCMAKE_CXX_STANDARD=17 ...`** |
| 4 | 串口 Permission denied | 不在 `dialout` | `sudo adduser $USER dialout` 后重登 |
| 5 | 改了 yaml 不生效 | 跑的是 install 份 | 改 `install/.../config/settings.yaml` 或改源后重 `colcon build` |
| 6 | Docker 文档找不到 `params.yaml` | 文档旧名 | 用 **`config/settings.yaml`** |
| 7 | `/baseline` echo 报未知类型 | 新 shell 未 source | 每个终端先 `source install/setup.bash` |
| 8 | `interface: 3` 立刻退出/无流 | `sbp_file` 相对路径或文件不存在 | 绝对路径；仓内**无**样例 `.sbp`——自备或用 [piksi-tools](./piksi-tools.md)/[libsbp](./libsbp.md) 录 |
| 9 | GPSFix.track 卡住 | 水平速 < `track_update_min_speed_mps` | 降阈值或接受冻结；有 ORIENT 时优先 yaw |
| 10 | 时间戳乱跳 | `timestamp_source_gnss: True` 但无 UTC TIME | 开接收机 UTC 输出，或改 `False` 用主机钟 |
| 11 | 当 TEC/多品牌驱动用 | 只服务 Swift SBP | 换品牌驱动或离线栈；电离层走落盘 RINEX |
| 12 | 本机无 ROS 却期待 `ros2 pkg` | 环境门禁 | 先装 Humble 等；本文 §2.3 只验仓结构 |
| 13 | 与 PyPI `sbp 6.5.2` API 混用期望 | C 钉 v4 vs Python tip | ROS 构建跟 README；Python 离线跟 [libsbp](./libsbp.md) |
| 14 | Starling/Piksi 口上消息过多 | 未裁 `enabled-messages` | 只开 §3 所列 ID；专口给 ROS |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| Swift **实时**进 ROS 2 | **本文 swiftnav-ros2** |
| SBP 编解码 / `sbp2json`（无 ROS） | [libsbp](./libsbp.md) |
| Piksi 现场日志·配置·刷机 | [piksi-tools](./piksi-tools.md) |
| Septentrio 实时进 ROS1/ROS2 | [septentrio-gnss-driver](./septentrio-gnss-driver.md) |
| u-blox ROS2 | [ublox-dgnss](./ublox-dgnss.md) |
| Swift 数值例程（非通信） | [libswiftnav](./libswiftnav.md) |

## 9. 相关

[libsbp](./libsbp.md) · [piksi-tools](./piksi-tools.md) · [libswiftnav](./libswiftnav.md) · [septentrio-gnss-driver](./septentrio-gnss-driver.md) · [ublox-dgnss](./ublox-dgnss.md) · [ntripstreams](./ntripstreams.md) · [pygnssutils](./pygnssutils.md) · [rtkbase](./rtkbase.md) · [bnc](./bnc.md) · [README](./README.md)

- 上游：<https://github.com/swift-nav/swiftnav-ros2>
- 支持：<https://support.swiftnav.com/>（需登录提单）
- SBP 规范与机型配置：README「GNSS Receiver Configuration」链（Piksi Multi / Duro / PGM EVK / Starling）
- 许可：MIT
