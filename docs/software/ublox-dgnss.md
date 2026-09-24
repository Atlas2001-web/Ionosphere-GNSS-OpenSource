# ublox_dgnss · ROS 2 u-blox UBX DGNSS 驱动操作手册

目录：[`PROJECTS.json` → `ublox_dgnss`](../../PROJECTS.json) · 上游 <https://github.com/aussierobots/ublox_dgnss> · **URL 已核** · 元包 **`ublox_dgnss`** · 全栈版本 **0.7.6** · tip **`7ace9d5`**（2026-08-13 23:15 EDT；tag **`0.7.6`**）· 许可 **Apache-2.0** · 可执行 **`ublox_dgnss_node`** / **`ublox_nav_sat_fix_hp`** / **`ntrip_client_node`** · 本机验证：clone + 六包 `package.xml` / `launch`×11 / `config`×3 / `msg`×65 / `srv`×4 清单；**无 `/opt/ros`、无 u-blox USB 接收机 → 未 `colcon`、未 `ros2 launch`、无 topic echo** · 2026-09-24 05:40 EDT

> 岗位：把 **ZED-F9P / F9R / X20P** 经 **USB + UBX** 接入 **ROS 2**，发高精度导航话题；可选固定/移动基站、内置 NTRIP RTCM、初步 SPARTN。冲突时：**上游 README / 仓内 `launch/*.py` / `config/*.toml` / 本机 `ros2 pkg` > 本文**。离线 UBX 编解码 → [pyubx2](./pyubx2.md)；Septentrio / Swift ROS 对照 → [septentrio-gnss-driver](./septentrio-gnss-driver.md) / [swiftnav-ros2](./swiftnav-ros2.md)。**不是** 电离层 TEC/闪烁流水线，也**不是** 测地级 PPP 引擎。

## 1. 用途与边界

**做：**

- ROS 2（README：**Humble / Jazzy / Kilted / Rolling**；Ubuntu 22.04/24.04/26.04）
- 传输：**USB**（`libusb-1.0`）；F9 系 CDC-ACM `0x01a9`；X20P **仅主接口** `0x01ab`（UART1/2 `0x050c`/`0x050d` **不支持**）
- 输出：`ublox_ubx_msgs` 的 UBX 镜像话题（`CFG_MSGOUT_*`>0 才发）+ 可选 `sensor_msgs/NavSatFix`（`/fix`）
- 场景：单机 rover HP；固定基站+rover（`ublox_fb+r_*`）；F9P moving-base（`ublox_mb+r_*`，**F9R 不支持**）；X20P 25 Hz 专用 launch
- 改正：订 `/ntrip_client/rtcm`（默认开）或外源 RTCM；X20P 可选 PMP / QZSS L6 / SPARTN key 入流

**不做：**

- **不是** 纯 Python UBX 编解码 / 无 ROS CLI → [pyubx2](./pyubx2.md)（+ [pygnssutils](./pygnssutils.md) `gnssstreamer`）
- **不是** Septentrio / Swift 品牌驱动 → [septentrio-gnss-driver](./septentrio-gnss-driver.md) / [swiftnav-ros2](./swiftnav-ros2.md)
- **不是** 发表级 PPP/TEC；机器人/车载室外联调为主
- **无 ROS / 无 Rx**：**禁止臆造** `ros2 topic echo` / bag / 实时 `/fix` stdout

一句话：ublox_dgnss = **Aussie Robots ROS 2 USB-UBX 高精度桥**（composition）；协议真相可离线对照 [pyubx2](./pyubx2.md)。

| 术语 | 含义 |
| --- | --- |
| 元包 `ublox_dgnss` | 聚合 launch/config + 依赖五个实现包 |
| `ublox_dgnss_node` | 主驱动；plugin `ublox_dgnss::UbloxDGNSSNode`；exec 同名 |
| `DEVICE_FAMILY` | `F9P`（默认）/ `F9R` / `X20P` |
| `CFG_MSGOUT_*_USB` | >0 → 对应 `/ubx_*` 话题开启发 |
| `/fix` | `ublox_nav_sat_fix_hp_node` 合成 NavSatFix（依赖 hp_pos_llh+cov+status） |
| moving-base | 车载双 F9P 航向；launch `ublox_mb+r_*` |

## 2. 安装（有 ROS 的机器）

### 2.1 udev（USB 权限，必做一次）

```bash
sudo tee /etc/udev/rules.d/99-ublox-gnss.rules <<'RULE'
# F9P/F9R
ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a9", MODE="0666", GROUP="plugdev", ENV{ID_MM_DEVICE_IGNORE}="1"
# X20P 主接口（唯一受支持）
ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01ab", MODE="0666", GROUP="plugdev", ENV{ID_MM_DEVICE_IGNORE}="1"
RULE
sudo udevadm control --reload-rules && sudo udevadm trigger
# 用户加入 plugdev 后重登
```

### 2.2 源码 · colcon

```bash
source /opt/ros/${ROS_DISTRO}/setup.bash   # humble|jazzy|kilted|rolling
sudo apt-get update
sudo apt-get install -y libusb-1.0-0-dev libcurl4-openssl-dev pkg-config
# rtcm_msgs 等：rosdep 一般能拉；缺则 apt install ros-${ROS_DISTRO}-rtcm-msgs

mkdir -p ~/ublox_ws/src && cd ~/ublox_ws/src
git clone https://github.com/aussierobots/ublox_dgnss.git
cd ~/ublox_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-up-to ublox_dgnss
source install/setup.bash
```

依赖硬约束：C++、`libusb-1.0`、`rclcpp_components`、`rtcm_msgs`、`sensor_msgs`；NTRIP 节点另需 `libcurl`。

### 2.3 本机（文档仓）可做的核对 — **无 ROS / 无硬件**

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/aussierobots/ublox_dgnss.git
cd ublox_dgnss
git rev-parse --short HEAD          # 期望 7ace9d5
for d in ublox_dgnss ublox_dgnss_node ublox_nav_sat_fix_hp_node \
         ntrip_client_node ublox_ubx_msgs ublox_ubx_interfaces; do
  echo "== $d"; grep -E '<name>|<version>|<license>' $d/package.xml
done
ls ublox_dgnss/launch/*.py | wc -l   # 11
ls ublox_dgnss/config/*.toml         # f9p / f9r / x20p
find ublox_ubx_msgs/msg -name '*.msg' | wc -l    # 65
ls ublox_ubx_interfaces/srv/         # ColdStart HotStart WarmStart ResetODO
rg -n 'EXECUTABLE|PLUGIN' ublox_dgnss_node/CMakeLists.txt \
  ublox_nav_sat_fix_hp_node/CMakeLists.txt ntrip_client_node/CMakeLists.txt
test -d /opt/ros && echo HAS_ROS || echo NO_ROS
# 有 ROS 后再：
#   ros2 pkg list | rg 'ublox_dgnss|ublox_ubx'
#   ros2 launch ublox_dgnss ublox_rover_hpposllh.launch.py --show-args
```

**本机结果（tip `7ace9d5` / 0.7.6，2026-09-24 05:40 EDT）：** clone OK；六包 name/version/license 均为 **0.7.6** / Apache License Version 2.0；launch×**11**、config toml×**3**、msg×**65**、srv×**4**；exec **`ublox_dgnss_node`** / **`ublox_nav_sat_fix_hp`** / **`ntrip_client_node`**；plugin 分别为 `ublox_dgnss::UbloxDGNSSNode` / `ublox_nav_sat_fix_hp::UbloxNavSatHpFixNode` / `ublox_dgnss::NTRIPClientNode`。**`which ros2` / `/opt/ros` 不存在** → 未 `colcon`、未 launch、未插 USB、仓内**无** `.bag`/样例 UBX → **硬件/ROS 门禁**；下列话题表来自上游 README + launch 参数，**非本机 echo**。

## 3. 配置与启动

### 3.1 常用 launch（有 ROS + 已 source）

```bash
# 默认 F9P · HP Lon/Lat
ros2 launch ublox_dgnss ublox_rover_hpposllh.launch.py
# 同上 + NavSatFix（另起 ublox_nav_sat_fix_hp）
ros2 launch ublox_dgnss ublox_rover_hpposllh_navsatfix.launch.py
# X20P 主接口（DEVICE_FAMILY 默认 X20P；CFG_RATE_MEAS:=40 → 25 Hz）
ros2 launch ublox_dgnss ublox_x20p_rover_hpposllh.launch.py
# 任意 launch 切家族：
ros2 launch ublox_dgnss ublox_rover_hpposllh.launch.py device_family:=X20P
# 固定基站 / rover；移动基站 / rover（需两台 F9P + 串号）
ros2 launch ublox_dgnss ublox_fb+r_base.launch.py
ros2 launch ublox_dgnss ublox_fb+r_rover.launch.py
ros2 launch ublox_dgnss ublox_mb+r_base.launch.py
ros2 launch ublox_dgnss ublox_mb+r_rover.launch.py
# NTRIP（凭据宜用环境变量，勿写进仓库）
export NTRIP_USERNAME=... NTRIP_PASSWORD=...
ros2 launch ublox_dgnss ntrip_client.launch.py \
  use_https:=true host:=ntrip.data.gnss.ga.gov.au port:=443 \
  mountpoint:=MBCH00AUS0
```

或单节点：

```bash
ros2 run ublox_dgnss_node ublox_dgnss_node --ros-args \
  -p CFG_USBOUTPROT_NMEA:=False -p DEVICE_FAMILY:=F9P
```

多机同族：设 `DEVICE_SERIAL_STRING`（F9 用 u-center 写 CFG-USB-SERIAL；X20P 用出厂 iSerial）与 `FRAME_ID`。

### 3.2 服务（有硬件时）

```bash
ros2 service call /ublox_dgnss/reset_odo ublox_ubx_interfaces/srv/ResetODO
ros2 service call /ublox_dgnss/cold_start ublox_ubx_interfaces/srv/ColdStart '{reset_type: 1}'
ros2 service call /ublox_dgnss/warm_start ublox_ubx_interfaces/srv/WarmStart '{reset_type: 1}'
ros2 service call /ublox_dgnss/hot_start  ublox_ubx_interfaces/srv/HotStart  '{reset_type: 1}'
```

> **门禁：** 上列 `launch`/`echo`/`service call` 为有 ROS/硬件时的操作模板；**本文档机未跑，无 stdout。**

CFG 只写 **RAM**：热插拔/冷热启动后驱动会把当前参数再下发；持久化请用 u-center 写闪存。`config/*.toml` 供批量键集（`generate_toml_from_existing.py`），与 launch 内联 `parameters=` 互补。

## 4. 期望话题（来自 README；非本机 echo）

**发布（`CFG_MSGOUT_*`>0 才有）：**

| 话题 | 说明 |
| --- | --- |
| `/ubx_nav_hp_pos_llh` `/ubx_nav_hp_pos_ecef` | 高精度位置 |
| `/ubx_nav_pvt` `/ubx_nav_status` `/ubx_nav_cov` | PVT / 解状态 / 协方差 |
| `/ubx_nav_rel_pos_ned` | 相对定位 / moving-base 航向 |
| `/ubx_rxm_rtcm` `/ubx_rxm_cor` | RTCM 使用状态；X20P 倾向 `cor`（`rtcm` 在设备侧渐弃） |
| `/ubx_rxm_rawx` `/ubx_rxm_measx` `/ubx_rxm_sfrbx` | 原始观测/星历块（开 MSGOUT 后） |
| `/ubx_esf_*` `/ubx_sec_*` `/ubx_mon_comms` | F9R 融合 / 抗干扰 / 通讯监视 |
| **`/fix`** | `sensor_msgs/NavSatFix`（需 hp_llh+cov+status 三路已开） |

**订阅（按 bool 门控）：**

| 参数（默认） | 话题 | 用途 |
| --- | --- | --- |
| `RTCM_INPUT_ENABLED`=`true` | `/ntrip_client/rtcm` | RTCM3 → USB |
| `ESF_MEAS_INPUT_ENABLED`=`true` | `/ubx_esf_meas_to_device` | **F9R** 传感器 |
| `RXM_PMP_INPUT_ENABLED`=`false` | `/ubx_rxm_pmp_to_device` | **X20P** L-band |
| `RXM_QZSSL6_INPUT_ENABLED`=`false` | `/ubx_rxm_qzssl6_to_device` | **X20P** QZSS L6/CLAS |
| `RXM_SPARTNKEY_INPUT_ENABLED`=`false` | `/ubx_rxm_spartnkey_to_device` | **X20P** SPARTN 密钥 |

冒烟模板（有硬件）：`ros2 topic echo /ubx_rxm_rtcm`（`msg_used==2` 表示已用改正）· `/ubx_nav_status` · `/ubx_nav_hp_pos_llh` · `/fix`。

## 5. 关键参数

| 参数 | 作用 | 冒烟注意 |
| --- | --- | --- |
| `DEVICE_FAMILY` | F9P/F9R/X20P | 错族 → 找不到 USB 或禁用不该有的订阅 |
| `DEVICE_SERIAL_STRING` | 多机选设备 | 空=同族第一台 |
| `FRAME_ID` | `header.frame_id` | 默认常 `ubx` / base / rover |
| `CFG_USBOUTPROT_NMEA` | USB 出 NMEA | launch 例常 `False` 减带宽 |
| `CFG_RATE_MEAS` / `CFG_RATE_NAV` | 测量/导航率 | 单位按 UBX 手册（未缩放）；X20P 例 MEAS=`40`≈25 Hz |
| `CFG_MSGOUT_UBX_*_USB` | 话题开关 | `0` 关；`1` 每历元；更大=降采样 |
| `CFG_TMODE_*` | 基站 survey-in / 固定坐标 | 见 `ublox_fb+r_base` |
| `RTCM_INPUT_ENABLED` 等 | 入流订阅门 | 见 §4；错族只打 warn 不订 |
| `CFG_SPARTN_USE_SOURCE` | SPARTN 源 | 初步支持；需配套 key/入流 |

运行时：`ros2 param set /ublox_dgnss CFG_RATE_NAV 2`（节点名以 launch 为准）。

## 6. 接到哪步

```text
[u-blox F9P/F9R/X20P USB]
    │  UBX (+ 可选 RTCM/SPARTN)
    ▼
ublox_dgnss_node ──/ubx_*──► 机器人 / robot_localization / 监控
    │                └─(+ nav_sat_fix_hp)── /fix
    ├─ NTRIP RTCM ──► ntrip_client_node 或外源 /ntrip_client/rtcm
    ├─ 离线 UBX 编解码 ──► [pyubx2] / [pygnssutils]
    ├─ Septentrio / Swift 机 ──► 换品牌 ROS 驱动，勿硬套
    └─ 落盘 RINEX 后再走路径 A/B（georinex / pytecgg / …）
```

- **只要 ROS 实时 HP / NavSatFix / 航向**：停在本驱动。
- **只要协议/无 ROS**：直接 [pyubx2](./pyubx2.md)，不必起驱动。
- **要测地 PPP/TEC**：落盘后走 [rtklib](./rtklib.md)/[georinex](./georinex.md) 等，不要指望本包。

## 7. 坑（≥8；现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 打不开 USB / Permission denied | 无 udev 或不在 `plugdev` | 装 §2.1 规则并重登 |
| 2 | X20P 完全无数据 | 插了 UART1/2 口 `0x050c/050d` | **只用主接口 `0x01ab`**；`DEVICE_FAMILY:=X20P` |
| 3 | `/fix` 永不出 | 未开 hp_llh+cov+status 三路 | 用 `*_navsatfix` launch，或手动把三路 `CFG_MSGOUT_*`>0 |
| 4 | 多机抢同一接收机 | 未设串号 | `DEVICE_SERIAL_STRING`；F9 先 u-center 写序列 |
| 5 | 改 CFG 重启丢失 | 只写 RAM | 预期行为；要持久化用 u-center 写闪存 |
| 6 | RTCM 订了仍是单点 | 改正未用 / 错 mount | `echo /ubx_rxm_rtcm` 看 `msg_used`；核 NTRIP 用户与 mount |
| 7 | moving-base 无航向 | 用了 F9R 或 UART2 线未接 | **仅 F9P**；按 app note 接 UART2；看 `/ubx_nav_rel_pos_ned` |
| 8 | `ros2 launch` 找不到包 | 未 source / 只编了子包 | `colcon build --packages-up-to ublox_dgnss` 后 `source install` |
| 9 | ModemManager 抢 CDC | 未 `ID_MM_DEVICE_IGNORE` | 用 §2.1 规则含该 ENV |
| 10 | 当 TEC/PPP 引擎用 | 只是实时驱动 | 落盘再走离线栈；协议试验用 [pyubx2](./pyubx2.md) |
| 11 | 本机无 ROS 却期待 `ros2 pkg` | 环境门禁 | 先装 Humble+；本文 §2.3 只验仓结构 |
| 12 | X20P 仍 echo `/ubx_rxm_rtcm` 为空 | 设备侧倾向 `/ubx_rxm_cor` | 开 `CFG_MSGOUT_UBX_RXM_COR_USB`；对照 README |

## 8. 选型

| 你要… | 用 |
| --- | --- |
| u-blox **F9/X20P 实时**进 ROS 2（USB UBX） | **本文 ublox_dgnss** |
| UBX 编解码 / 无 ROS | [pyubx2](./pyubx2.md) |
| Septentrio 实时进 ROS1/ROS2 | [septentrio-gnss-driver](./septentrio-gnss-driver.md) |
| Swift SBP 实时进 ROS 2 | [swiftnav-ros2](./swiftnav-ros2.md) |
| NTRIP/RTCM 通用工具（非本包节点） | [ntripstreams](./ntripstreams.md) / [pygnssutils](./pygnssutils.md) / [pyrtcm](./pyrtcm.md) |

## 9. 相关

[pyubx2](./pyubx2.md) · [septentrio-gnss-driver](./septentrio-gnss-driver.md) · [swiftnav-ros2](./swiftnav-ros2.md) · [ntripstreams](./ntripstreams.md) · [pygnssutils](./pygnssutils.md) · [pyrtcm](./pyrtcm.md) · [rtkbase](./rtkbase.md) · [README](./README.md)

- 上游：<https://github.com/aussierobots/ublox_dgnss>
- u-blox 接口手册：README 链 X20P Integration Manual / Interface Description；Moving-base app note UBX-19009093
- 许可：Apache-2.0
