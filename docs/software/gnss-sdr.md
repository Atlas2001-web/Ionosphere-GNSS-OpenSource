# gnss-sdr · CTTC 开源 GNSS 软件定义接收机操作手册

目录：[`PROJECTS.json` → `gnss-sdr`](../../PROJECTS.json) · 上游 <https://github.com/gnss-sdr/gnss-sdr> · 站点 <https://gnss-sdr.org> · tip **`0f4dba1`** · 本机冒烟：**Debian `gnss-sdr` 0.0.20-1** · **GPL-3.0-or-later** · 本机验证（**2026-09-24 06:50 EDT**）：`gps-sdr-sim` 60 s IF（4 Msps/`ishort`）→ `PVT.positioning_mode=Single` → 首定 **41.275N / 1.98757E / H≈89.4 m**（真值 **41.275 / 1.9876 / 100**）；跟踪 **12** PRN；NMEA **870** 行；**无 RF 前端、无天空天线**；**未臆造**未跑通的天空 PVT

> 岗位：从 **IQ/IF 文件或 SDR 前端**跑捕获→跟踪→电文→观测→PVT。冲突时：**本机 `gnss-sdr --help` / 仓内 `conf/` / [gnss-sdr.org docs](https://gnss-sdr.org) > 本文**。  
> 仿真源 → [gps-sdr-sim](https://github.com/osqzss/gps-sdr-sim)（本机联调）；轻量口袋接收机 → [pocketsdr](./pocketsdr.md)；事后 RINEX 解算 → [rtklib](./rtklib.md)；RINEX 探活 → [georinex](./georinex.md)。

## 1. 用途与边界

**做：**

- 多星座软件接收机：捕获 / DLL-PLL 跟踪 / 导航电文 / 观测量 / PVT（RTKLIB 解算块）
- `File_Signal_Source` 回放 IF；UHD / OsmoSDR / Lime / Pluto 等实时前端（需对应驱动与编译开关）
- 写出 KML/GPX/GeoJSON/NMEA；可选 RINEX、观测 dump

**不做 / 本机限制：**

- **不是** RINEX 事后 PPP/RTK 引擎 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 手机 Logger 套件 → [gps-measurement-tools](./gps-measurement-tools.md)
- **不是** 仅捕获教学脚本 → [pocketsdr](./pocketsdr.md)（同属 SDR，栈更轻）
- 本机 **无** HackRF/USRP/天线 → 用仿真 IF；**禁止把仿真坐标写成“天空实测”**
- 默认样例 conf 里的 CTTC `.dat` **不在包内**——须自备文件或仿真

一句话：gnss-sdr = **GNU Radio 风格的完整 SDR 接收机**；算力与前端门槛高，无硬件时先走文件源。

| 术语 | 含义 |
| --- | --- |
| `internal_fs_sps` | 调理后内部采样率（常低于前端 `sampling_frequency`） |
| `item_type=ishort` | 交织 int16 IQ（与 `gps-sdr-sim -b 16` 对齐） |
| `Channels_1C` | GPS L1 C/A 通道数 / 并行捕获数 |
| `RTKLIB_PVT` | 观测进 RTKLIB 解；`Single` vs `PPP_Static` 门槛差很大 |
| volk_gnsssdr | SIMD 核；首次可跑 `volk_gnsssdr_profile`（可选） |

## 2. vs PocketSDR / gps-sdr-sim / RTKLIB

| | **本文 gnss-sdr** | [pocketsdr](./pocketsdr.md) | gps-sdr-sim | [rtklib](./rtklib.md) |
| --- | --- | --- | --- | --- |
| 角色 | IQ→PVT 接收机 | 口袋 FE + 捕获/跟踪 AP | **只生成** L1 基带 | RINEX→定位 |
| 栈 | C++ / GNU Radio 依赖 | C + 自带 libsdr | 单文件 C | C CLI |
| 本机冒烟 | apt **0.0.20** + 仿真 IF | 源码 `make` + `pocket_acq` | `make` 出 `gps-sdr-sim` | apt/自编 `rnx2rtkp` |
| 前端 | UHD/OsmoSDR/… | Pocket FE / Soapy | 无（发射另接 SDR） | 无射频 |

混用后果：把 gps-sdr-sim 真值坐标当天空标定、或把 gnss-sdr 当 RINEX PPP——报告与产品都会错。

## 3. 安装（Debian 二进制最快）

```bash
# 本机（Debian trixie）：
sudo apt-get install -y gnss-sdr
gnss-sdr --version    # 期望：gnss-sdr version 0.0.20
which gnss-sdr        # /usr/bin/gnss-sdr
ls /usr/share/gnss-sdr/conf/File_input/GPS/ | head
```

从源码（重、依赖 GNU Radio 等；无硬件时不必）：

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/gnss-sdr/gnss-sdr.git
cd gnss-sdr && git rev-parse --short HEAD   # 本机对照：0f4dba1
# mkdir build && cd build && cmake .. && make -j$(nproc)
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `apt` 拉依赖巨大 | GNU Radio / UHD / Qt 链 | 接受；或 Docker 镜像 `carlesfernandez/docker-gnsssdr` |
| conf 指向不存在的 `.dat` | 仓内占位路径 | 改 `SignalSource.filename` |
| 进程卡住等键盘 | 默认 keyboard listener | `--keyboard=false` 或 EOF 后退 |

## 4. 端到端：gps-sdr-sim IF → Single PVT（本机真跑）

**前置：** 另仓编译 `gps-sdr-sim`（MIT；<https://github.com/osqzss/gps-sdr-sim>），用自带 `brdc0010.22n`。

```bash
mkdir -p ~/iono_ops/gnss-sdr-smoke && cd ~/iono_ops/gps-sdr-sim
./gps-sdr-sim -e brdc0010.22n -l 41.275,1.9876,100 -d 60 -s 4000000 -b 16 \
  -o ~/iono_ops/gnss-sdr-smoke/gpssim_4M_16b_60s.bin -t 2022/01/01,00:00:00
# → ~956 MB；可见星含 G01/07/08/10/16/21/22/23/26/27/30/32

cp /usr/share/gnss-sdr/conf/File_input/GPS/gnss-sdr_GPS_L1_ishort.conf \
   ~/iono_ops/gnss-sdr-smoke/gps_l1_sim_single.conf
# 编辑要点：
#   SignalSource.filename=.../gpssim_4M_16b_60s.bin
#   SignalSource.item_type=ishort
#   SignalSource.sampling_frequency=4000000
#   Channels_1C.count=12 ; Channels.in_acquisition=4
#   PVT.positioning_mode=Single   # 勿用默认 PPP_Static 短片段
#   PVT.dump=true

cd ~/iono_ops/gnss-sdr-smoke
gnss-sdr --config_file=./gps_l1_sim_single.conf --log_dir=./logs2 -keyboard=false
```

**本机 stdout / 日志要点（0.0.20，2026-09-24 06:50 EDT）：**

```text
Tracking of GPS L1 C/A ... PRN 01,07,08,10,16,21,22,23,26,27,30,32
First position fix at 2022-Jan-01 00:00:24.160000 UTC is Lat = 41.275 [deg], Long = 1.98757 [deg], Height= 89.3569 [m]
Position at 2022-Jan-01 00:00:24.500000 UTC using 7 observations is Lat = 41.275011 [deg], Long = 1.987619 [deg], Height = 96.24 [m]
Total GNSS-SDR run time: 7.274530 [seconds]
```

产物：`PVT_*.kml` / `.gpx` / `.geojson`、`gnss_sdr_pvt.nmea`（本机 **870** 行；首 `$GPGGA` 高度≈**87** m）、`observables.mat`。墙时 ≈7 s 吃完 60 s 仿真。

**坑对照：** 同 conf 默认 `PPP_Static` + 仅 30 s IF → 跟踪/电文有、**无**稳态 PVT（日志反复 `position solver error`）——不是仿真坏了，是模式门槛。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IF 文件 | `item_type` 与字宽/交织必须匹配（`ishort`↔int16 IQ） |
| 采样率 | 前端 `sampling_frequency` 与仿真 `-s` 一致；再配 `Resampler` |
| 实时 SDR | 换 `RealTime_input` conf；**先** `lsusb`/Soapy 通再开接收机 |

| 输出 | 说明 |
| --- | --- |
| NMEA / KML / GPX / GeoJSON | `PVT.*` 开关；短片段高度抖动正常 |
| RINEX | 视 conf `flag_rinex_*`；落盘后再 [georinex](./georinex.md) |
| 不输出 | 校准 TEC / GIM；电离层产品链走 [pytecgg](./pytecgg.md) |

## 6. 硬件 / SDR 诚实边界

1. **无天线 = 无天空 PVT**；实验室请屏蔽箱或持证发射，勿户外放 gps-sdr-sim  
2. HackRF/RTL 等 NF、带宽、前端滤波远差专业 GNSS FE；捕获门限与 C/N0 预期要降  
3. USB 供电不足 → 掉样 → 假周跳；优先供电集线器  
4. 本机冒烟路径：**文件源**；实时路径自行加驱动与 udev  
5. Docker 镜像便于课程，但版本常滞后 Debian/上游 tip——写报告标版本串  

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 有跟踪无位置 | `PPP_Static` + 片段太短 | 改 `Single` 或加长 IF |
| 2 | 立刻退出 / 空跑 | `filename` 仍是占位路径 | `ls -l` 文件；改绝对路径 |
| 3 | 捕获全失败 | `item_type`/采样率与 IF 不一致 | `-b 16`↔`ishort`；核对 Msps |
| 4 | 卡在 “press q” | keyboard 开着 | `-keyboard=false` |
| 5 | 高度漂十几米 | 仿真+单频+短弧 | 报告标仿真；勿当测地精度 |
| 6 | 与 RTKLIB 坐标比飞 | 对象不同（SDR PVT vs RINEX PPP） | 分表写；同观测再比 |
| 7 | apt 与 tip 功能差 | 发行版滞后 | 报告写 **0.0.20**；新特性自编 tip `0f4dba1` |
| 8 | 把仿真当真天空 | 流程误解 | 文中标明 `gps-sdr-sim` 真值 |
| 9 | OsmoSDR 编译未开 | CMake 默认 OFF | `-DENABLE_OSMOSDR=ON` 重编 |
| 10 | 多星座 conf 套 GPS-only IF | 通道空转 | 先 L1CA 单系统跑通 |
| 11 | volk 首次极慢 | 未 profile | 可选 `volk_gnsssdr_profile` |
| 12 | 无 RF 却写“实测精度 cm” | 臆造 | 只引用本机日志数字 |

## 8. 接到哪步

1. 要 IF → gps-sdr-sim / 自采；捕获对照 → [pocketsdr](./pocketsdr.md)  
2. 出 RINEX → [georinex](./georinex.md) / [rinexmod](./rinexmod.md)  
3. 精密定位 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)（**换观测文件**，别硬扛 SDR PVT）  
4. 手机原始测量 → [gps-measurement-tools](./gps-measurement-tools.md) + [android_rinex](./android_rinex.md)  
5. 法规 / 数据礼仪 → [data-access](../data-access.md)

## 9. 选型

| 需求 | 选 |
| --- | --- |
| 完整 SDR 接收机 / 教学监控站 | **本文** |
| 轻量捕获 + Pocket FE | [pocketsdr](./pocketsdr.md) |
| 只生成 L1 基带 | gps-sdr-sim（上游） |
| RINEX 事后 RTK/PPP | [rtklib](./rtklib.md) |
| 读观测进 Python | [georinex](./georinex.md) |

## 10. 相关

[pocketsdr](./pocketsdr.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gps-measurement-tools](./gps-measurement-tools.md) · [android_rinex](./android_rinex.md) · [laika](./laika.md) · [data-access](../data-access.md) · [README](./README.md)
