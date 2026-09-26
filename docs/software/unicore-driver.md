# UnicoreDriver · 和芯星通 UM982/UM980 二进制 BESTNAVXYZB → ROS Noetic 里程计 操作手册

目录：[`PROJECTS.json` → `UnicoreDriver`](../../PROJECTS.json) · 上游 <https://github.com/zltan-whu/UnicoreDriver>（与 PROJECTS `url` 一致，默认分支 **main**）· 唯一提交 **`240ae7d`**（2025-04-30 09:49 EDT，`initial commit`）· **无 tag / 无 release** · **GPL-3.0** · ★**11** / fork 2 · C++11 · catkin 包名 `unicore_driver` · 实测窗口 **2026-09-26 06:20–06:32 EDT**

规范依据：**Unicore Reference Commands Manual For N4 High Precision Products V2 EN R1.15**（371 页，en.unicore.com 公开 PDF，5581479 B）：表 7-48 二进制报文头、§7.5.23 BESTNAVXYZ（Message ID 240，表 7-72，第 189–190 页）、表 7-172 位置/速度类型、表 7-173 解状态、附录 CRC32 C 代码。

> 一句话：串口读 Unicore 二进制帧，校验 CRC32，**只把 `BESTNAVXYZB`（ID 240）变成 `nav_msgs/Odometry`**，话题 `~best_nav_ecef`，坐标系 **ECEF**；另带一个把固定 GGA 发给 NTRIP caster、把 RTCM 写回串口的客户端。
> **本机无接收机、未装 ROS**：用最小 ROS 桩（自写 `ros/ros.h` + `nav_msgs/Odometry.h`，stdout 模拟 `rostopic echo`）编译上游 4 个源文件原样，socat 虚拟串口回放。串口/接收机/roslaunch 路径均**「未在真接收机测试」**。

## 1. 用途边界

| 做 | 不做 |
| --- | --- |
| 二进制同步 `AA 44 B5` + 24 B 头 + CRC32 校验，解 **BESTNAVXYZB** | **不解 ASCII**（`#BESTNAVXYZA` 被当垃圾跳过），不解 NMEA |
| 位置 X/Y/Z、速度 VX/VY/VZ（ECEF）+ 各 σ² 放进协方差对角 | **不转 ENU / 大地坐标**，没有原点参数；要 ENU 自己算（§4） |
| `child_frame_id` 填位置类型字符串（`SINGLE`/`NARROW_INT`…） | 不看解状态 `P-sol status`，不输出卫星数、差分龄期、基站 ID |
| OBSVM(12)/BDSEPH(108)/BDSION(4) 帧：原样追加到当前目录 `obs_data.bin`/`ephem_data.bin`/`iono_data.bin` | 不发布观测/星历话题（README Todo：将来接 gnss_comm） |
| NTRIP v1 风格 GET + 每秒发一次**固定** GGA，收到的 RTCM 写回同一串口 | 不给接收机发配置命令（README 要你先用 UPrecise 配 `BESTNAVXYZB`） |
| launch 里多个 `<group ns=…>` = 多台接收机 | 无 ROS2 版本 |

## 2. 安装

上游方式（**未测**，本机无 ROS Noetic）：`catkin_ws/src` 下 clone → `catkin_make` → `roslaunch unicore_driver unicore_driver.launch`。依赖：roscpp、nav_msgs、sensor_msgs、std_msgs、rospy（package.xml），Boost（asio/thread，CMake 里没写 `find_package(Boost)`，靠 roscpp 传递），`find_package(Eigen3 REQUIRED)` 但源码**没有用到 Eigen**。

本机离线编译（真实命令，g++ 14.2 / Boost 1.83，Debian）：

```bash
unset TMPDIR PYTHONPATH ROS_PACKAGE_PATH CMAKE_PREFIX_PATH LD_LIBRARY_PATH
export TMPDIR=/tmp/unicoredrv-man/tmp; cd /tmp/unicoredrv-man
git clone https://github.com/zltan-whu/UnicoreDriver          # → 240ae7d
U=UnicoreDriver
g++ -std=c++11 -O3 -Wall -fPIC -Istub -I$U/include/unicore_driver \
  $U/src/{unicore_driver,serial_handler,unicore_message_processor,ntripclint_handler}.cpp \
  stub/ros_stub.cpp -o build/unicore_driver -lboost_thread -lpthread
# 只出 4 条 warning（-Wreorder ×3、-Wsign-compare ×1），0 error；二进制 417992 B
# 另编 -O1 -g -fsanitize=address,undefined 版本用于错误用例
```

桩只替换 ROS：`ros::NodeHandle::param` 读 `_name:=value` 命令行（同 rosrun 私有参数），`Publisher::publish` 打印成 `rostopic echo` 样式。消息解析、串口、NTRIP 代码是上游原文件，未改一行。

接收机侧（按手册 §8 命令语法整理，**未在真接收机测试**；上游 README 只说"用 UPrecise 配出 BESTNAVXYZB"）：

```text
UNLOG COM1                 # 先清掉该口所有输出，避免 ASCII/NMEA 挤占带宽
CONFIG COM1 921600         # 与 launch 的 baud_rate 一致
BESTNAVXYZB COM1 0.2       # 周期 0.2 s = 5 Hz；可选 1/0.5/0.2/0.1/0.05
SAVECONFIG
```

## 3. 例子与真实输出

### 3.1 数据来源

| 输入 | 来源 | 性质 |
| --- | --- | --- |
| `real_um980.bin`：32 帧 × 140 B = 4480 B | jclark/satpulse `gps/testdata/packets/unicore/UM980/bestnavxyz-dual.jsonl`（MIT，`c6ab0d6` 2026-04-04 07:43 EDT 入库；UM980 固件 Build17548）中 `UNCB` 行的 hex | **真实二进制**，含同历元 `#BESTNAVXYZA` |
| `real_synth.bin`：622 帧 = 87080 B | JHua07/Hardware-Projects `RTK_Trans/all.log`（无 license，仅本地使用）中 622 行 `#BESTNAVXYZA` 数值，自写编码器按表 7-72 封装 | **合成（源自真实观测值）**；ASCII CRC 622/622 通过后才封装 |

编码器先对真实二进制做过对拍：从同历元 ASCII 重编码的 32 帧，与真帧只在 double/float 低位（ASCII 4 位小数舍入，≤4.9×10⁻⁵）、`DelayMs` 字节和 CRC 上不同；头部 `TimeStatus` 真帧是 **160（0xA0）** 而非 1，`Version`（偏移 16）=17548 与固件号一致。

### 3.2 socat 回放（06:24:45 EDT）

```bash
socat pty,raw,echo=0,link=pty/ttyV0 pty,raw,echo=0,link=pty/ttyV1 &
./build/unicore_driver _port:=pty/ttyV0 _baud_rate:=921600 > out_real.yaml &
cat real_um980.bin > pty/ttyV1
# stderr: [ INFO] open port: .../pty/ttyV0        → 发布 32/32 条
```

第 1 条（真实 UM980 帧，GPS 周 2412、周内 543125000 ms，即 2026-04-04 02:51:47 EDT）：

```text
header:
  stamp: {secs: 1775285506, nsecs: 982000113}   # = 02:51:46.982 EDT，比历元早 18 ms
  frame_id: "ecef"
child_frame_id: "SINGLE"
pose.position: {x: -1144697.5421, y: 6090341.6446, z: 1504168.3606}
pose.covariance[0,7,14]: [13.5018768, 31.5853367, 55.8088188]   # = σ²，σ=3.6745/5.6201/7.4705 m
twist.linear: {x: -0.0213, y: -0.0664, z: 0.0325}               # ECEF m/s
twist.covariance[0,7,14]: [0.000870599761, 0.00310548465, 0.00128961226]
```

合成 622 帧（2025-05-28 05:01:48–05:12:09 EDT，全 `NARROW_INT`）：发布 622/622，首条 x=-1326002.8133、σ²=[0.000184960008, 0.000761759991, 0.00039999999]。

### 3.3 吞吐（pty，无波特率限制，桩发布=printf 到文件）

| 输入 | 帧数 | 写完耗时 | 发布 |
| --- | ---: | ---: | ---: |
| 合成 ×20（1741600 B） | 12440 | 0.077–0.100 s | 12440 |
| 合成 ×100（8708000 B），3 次 | 62200 | 0.381 / 0.389 / 0.385 s | 62200 |

≈1.6×10⁵ 帧/s，远高于物理上限：921600 波特 8N1 ≈ 92160 B/s ≈ **658 帧/s**（仅 BESTNAVXYZB）。真 roscpp 序列化开销**未测**。

### 3.4 自己补 ENU（驱动不做；§4 已用同法验证）

```python
from pyproj import Transformer          # pyproj 3.8.0
import numpy as np
X0 = np.array([-1326002.8133, 5323044.2383, 3243889.2912])   # 原点：首历元或已知站坐标
enu = Transformer.from_pipeline(
    f"+proj=topocentric +ellps=WGS84 +X_0={X0[0]} +Y_0={X0[1]} +Z_0={X0[2]}")
e, n, u = enu.transform(-1326002.8157, 5323044.2338, 3243889.2896)   # 第 2 历元
print(round(e, 4), round(n, 4), round(u, 4))
# → 0.0034 0.0006 -0.0041      ← 本机输出（m）
```

原点怎么选由你决定：固定基准站坐标（可复现）、首个 `NARROW_INT` 历元（随每次启动漂移）、或地图坐标原点。速度同理用同一旋转矩阵从 ECEF 转到 ENU；协方差要 `R Σ Rᵀ`，驱动只给对角，交叉项已丢。

## 4. 交叉检查（06:26 EDT）

独立解析器：Python，按表 7-48/7-72 用 `struct` 写（`<3sBHHBBHIIBBH` 头 + 112 B 体），CRC 用 `zlib.crc32(b, 0xFFFFFFFF) ^ 0xFFFFFFFF`（= 手册 `CalculateCRC32`：反射 0xEDB88320、初值 0、无终异或），与驱动的 CRC 表实现无共享代码。

| 对照 | n | 结果 |
| --- | ---: | --- |
| 驱动 vs 独立解析：位置/速度（驱动输出按 4 位小数打印） | 32 真 / 622 合成 | max\|Δ\| 4.85×10⁻⁵ m / 0 |
| 驱动 vs 独立解析：√协方差 − σ（float32 平方往返） | 同上 | 位置 ≤1.5×10⁻⁷ m，速度 ≤1.4×10⁻⁸ m/s |
| `child_frame_id` vs 位置类型 | 654 | 0 不符（仅测到 SINGLE、NARROW_INT） |
| `stamp` − (周, ms, 头部闰秒) 历元 | 654 | **−0.016 … −0.020 s**，恰为各帧 `DelayMs`（16–20 ms） |
| pyproj 3.8.0（EPSG:4978→4979）大地坐标 vs 同历元 `#BESTNAVA`（纬/经/海拔+高程异常） | 622 | 水平 max 7.5×10⁻⁵ m，椭球高 max 1.1×10⁻⁴ m |
| 同上 vs 同历元 `$GNGGA`（MSL+N） | 622 | 水平 max 8.4×10⁻⁵ m，高 max 1.4×10⁻⁴ m |
| ENU：以首历元为原点（30.76613182°N, 103.98802962°E, h=484.6560 m），手写旋转 vs pyproj `topocentric` | 622 | 差 1.4×10⁻¹⁷ m；静态 NARROW_INT 散布 σ_E/σ_N/σ_U = 0.0137/0.0112/0.0364 m |

与手册不符 / 可疑处（源码核对）：

1. **时间戳减了 `DelayMs`**：手册定义 DelayMs = 数据输出时刻 − 信号接收时刻，`Ms` 本身就是解算历元；驱动 `stamp = (Ms − DelayMs)/1000`，于是比历元早 16–20 ms（按手册语义推断，非实测接收机）。
2. 闰秒写死 18 s，头部 `Leap sec` 字段不用；`TimeRef` 不看（若接收机配成 BDST，会差 14 s）。
3. 头部注释把偏移 16 叫 Reserved、20 叫 Version，手册相反（该字段未被使用，无影响）。
4. `parse_bestnav_ecef_msg` 的 `msg_len < 112` 比的是整帧长（140），不是体长；实际靠 `len == L+28` 兜底。
5. 类型名表只列 12 个，手册表 7-172 有 23 个：`IONOFREE_FLOAT`、`WIDE_INT`、`INS*`、`PPP_CONVERGING`、`PPP_AR`、`PPP_RTK` 等都变 `"UNKNOWN"`（合成 68/70 已复现）。

## 5. 错误用例（全部「合成」，由 real_synth.bin 前 100 帧改写）

| 用例 | 结果 | 分类 |
| --- | --- | --- |
| 坏 CRC（每 10 帧翻 1 字节） | 发布 90，stderr `Invalid CRC checksum!` ×10，之后正常 | 丢帧有提示 |
| 截断帧（第 50 帧只留 70 B） | 发布 98：连带吃掉下一帧，只报 1 次 CRC 错，然后重同步 | 静默多丢 1 帧 |
| 长度字段 = 300（CRC 不可能对） | 发布 97：按 300+4 字节读，吞掉后面 2 帧 | 静默多丢 |
| 长度字段 = 65535 | 普通版 **SIGSEGV（rc=139）**；ASan：`heap-buffer-overflow … WRITE`（缓冲区只有 8192 B） | **崩溃** |
| 未知 ID 999（CRC 合法） | stdout `Message ID not match...` ×10，发布 90 | 有提示 |
| ID 12 OBSVM（CRC 合法） | 当前目录冒出 `obs_data.bin`（本地时间戳 + 原始字节 + `\n`，165 B） | 副作用 |
| 每帧后混 NMEA GGA + RTCM3 字节 | 发布 100/100，无任何输出 | 正确跳过 |
| `SOL_COMPUTED`→`INSUFFICIENT_OBS`，坐标非零 | **照样发布**（仍标 `NARROW_INT`） | 静默错误 |
| X=Y=Z=0 | `[ WARN] Invalid best_nav_ecef_msg, not publishing.` | 有提示 |
| 空输入 | 0 条，无任何提示，进程常驻 | 静默 |
| 串口断开（发 50 帧 + 半帧后杀 socat） | stderr 1 行 `Not received enough bytes: 36 while expecting 116`，进程存活、CPU 0%、**不重连**；同路径重建 pty 后 0 条新消息 | **卡死（静默停读）** |
| 端口不存在 / 未设 port | `[ERROR] Exception when opening serial port: open: No such file…` / 提示 `~port1`（实际参数叫 `port`），**退出码都是 0** | 退出码误导 |
| 正常退出（SIGINT） | 31 次 SIGINT 退出中 1 次 SIGSEGV（x20 用例），其余 rc=0；疑为分离的 io 线程与析构竞态，桩环境下所见 | 偶发崩溃 |

UBSan 另报：速度字段在 H+52，`reinterpret_cast<const double*>` 是**非对齐读**；x86 无碍，严格对齐的 ARM 上属未定义行为（未在 ARM 测）。

NTRIP 路径（本地假 caster，非真 CORS）：请求 `GET /TEST HTTP/1.1` + Basic 认证；回 `ICY 200 OK` 后 1000 B 负载**逐字节一致**写到串口另一端；7 s 收到 8 条 GGA（≈1 Hz），GGA 内容恒定、**不追加 CRLF**。stderr 以 INFO 级**明文打印用户名、密码与 Base64**。真 caster、重连、VRS **未测**。

## 6. I/O：字段与单位

输入帧（手册表 7-48/7-72，小端）：

| 偏移 | 字段 | 类型 | 驱动用途 |
| --- | --- | --- | --- |
| 0–2 | 同步 `AA 44 B5` | uchar×3 | 重同步 |
| 4 / 6 | Message ID / 体长 L | ushort | 分派；读 L+4 字节 |
| 10 / 12 | 周 / 周内毫秒 | ushort / ulong | 时间戳 |
| 22 | DelayMs | ushort | **被减去** |
| H+4 | pos type | enum | → `child_frame_id` |
| H+8/16/24 | P-X/Y/Z | double，m | → `pose.pose.position` |
| H+32/36/40 | σ | float，m | 平方 → `pose.covariance[0,7,14]`（m²） |
| H+52/60/68 | V-X/Y/Z | double，m/s | → `twist.twist.linear` |
| H+76/80/84 | σ | float，m/s | 平方 → `twist.covariance[0,7,14]`（m²/s²） |
| H+112 | CRC32 | ulong | 覆盖 0…H+111 |

H = 24；整帧 140 B。**不用**：P-sol/V-sol status、vel type、stn ID、V-latency、diff_age、sol_age、卫星数、扩展状态、信号掩码。

输出 `nav_msgs/Odometry`，话题 `/<ns>/unicore_driver/best_nav_ecef`，队列 100：`header.frame_id="ecef"`；`pose.pose.orientation` 全 0（**w=0，不是合法四元数**）；其余协方差 0；`twist.angular` 0。

launch 参数（`~` 私有）：`port`（默认空→退出）、`baud_rate`（921600）、`enable_rtk`（false）、`gga_sentence`、`ntrip_host`、`ntrip_port`（8002）、`ntrip_mountpoint`、`ntrip_user`、`ntrip_pass`。

## 7. 坑

1. **速度放在 ECEF、`child_frame_id` 放解类型字符串**：Odometry 约定 twist 在 child 坐标系，robot_localization/TF 会误读；接 EKF 前自己转 ENU 并改 frame。
2. **不过滤解状态**：`INSUFFICIENT_OBS` 等非零坐标照发，下游只能靠 `child_frame_id` 和协方差判断。
3. 长度字段 > 8164 → 堆溢出崩溃；串口线一抖/USB 重枚举 → 静默停读且不重连。生产上至少套 `respawn="true"` + 话题看门狗。
4. 退出码失败也是 0，`respawn` 以外的监控拿不到失败信号。
5. 时间戳早 DelayMs（16–20 ms），闰秒写死 18，不认 BDST。
6. OBSVM/星历/电离层帧若也开了，会在节点工作目录（roslaunch 下通常是 `~/.ros`）无限追加 `.bin` 文件。
7. 仓库 launch 默认值里有一组真实 NTRIP 主机/账号明文，且节点把密码打到日志：**换成你自己的并别把日志外发**。
8. launch 里写的 `\r\n` 在 XML 中是 4 个普通字符，而代码不补 CRLF；严格的 caster 可能不认这条 GGA（按源码推断，未在真 roslaunch/caster 验证）。GGA 固定不变，移动场景下 VRS 基准会越来越远。
9. 位置类型表缺 11 个（PPP_AR、WIDE_INT、INS* 等 → `UNKNOWN`）。
10. 非对齐 double 读取；32 位 ARM 板上先用 `-fsanitize=alignment` 跑一遍。
11. README 说依赖 Eigen 3.3.7，实际没用；缺的是显式 Boost 依赖。

## 8. 未测

真 UM982/UM980 接收机与 UPrecise 配置；真 ROS Noetic（catkin_make、roslaunch、rostopic、多 `<group>` 并行）；真 NTRIP caster 与 RTK 固定；物理串口 921600 波特下的丢字节行为；ARM 平台；ASCII 与 NMEA 输出（驱动本就不解）。

## 9. GPL-3.0 分发影响（简述，非法律意见）

源码 GPL-3.0，且 `serial_handler` 改自同为 GPL-3.0 的 HKUST ublox_driver。把本节点（或改过的版本）编进机器人镜像**对外分发**时，需同时提供对应源码与许可文本；把它的源文件并进你自己的闭源可执行文件，通常会让整体受 GPL 约束。只在内部使用、不分发，则无源码提供义务。通过 ROS 话题通信的独立节点一般被视为独立程序，但请以你的法务意见为准。

## 10. 选型

| 需求 | 选 |
| --- | --- |
| ROS1 下拿 UM98x ECEF 位置/速度，能接受 §7 的坑 | 本篇 UnicoreDriver（先加解状态过滤与重连） |
| Python、只要 ASCII `#PVTSLNA`/`#BESTNAVA`/航向 | [um982-driver](./um982-driver.md) |
| UM980 混合日志 → RINEX / RTKLIB 事后 PPK | [um980-rtklib-pipeline](./um980-rtklib-pipeline.md) |
| NovAtel 风格 OEM 二进制的成熟解码库（Unicore 头与之同源但 ID 不同） | [novatel-edie](./novatel-edie.md) |
| Unicore/u-blox 接收机做授时，含 UM980 实采测试数据 | [satpulse](./satpulse.md) |
| 同类 ROS 驱动参照（更完整的状态/话题） | [septentrio-gnss-driver](./septentrio-gnss-driver.md)、[ublox-driver](./ublox-driver.md)、[swiftnav-ros2](./swiftnav-ros2.md) |
| ECEF → 大地 / ENU 的独立换算 | [pymap3d](./pymap3d.md) 或 pyproj（§4 做法） |
