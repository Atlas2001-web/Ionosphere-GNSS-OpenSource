# gps-sdr-sim · GPS L1 基带信号仿真操作手册

目录：[`PROJECTS.json` → `gps-sdr-sim`](../../PROJECTS.json) · 上游 <https://github.com/osqzss/gps-sdr-sim> · tip **`28ca29a`** · ★**3466**（PROJECTS；写作 ★3468）· 许可 **MIT**（`LICENSE`，Copyright 2015–2025 Takuji Ebinuma）· 本机验证（**2026-09-24 06:53 EDT**；质检复跑 **06:58 EDT**）：`make` → `gps-sdr-sim` **64016** B；`-e brdc0010.22n -l 41.275,1.9876,100 -d 2 -s 2600000 -b 16` → **19760000** B；可见 **12** 星（G01/07/08/10/16/21/22/23/26/27/30/32）；`Process time = 0.2 [sec]`（写作 0.1）；东京 `-b 8` 1 s → **4680000** B / **11** 星（G05/10/12–15/18/20/23/24/28；`Process time = 0.1`）；同生成器已联调 [gnss-sdr](./gnss-sdr.md) 60 s PVT / [pocketsdr](./pocketsdr.md) `pocket_acq`；**无 SDR 发射、无天空天线**；**禁止户外放仿真 RF**

> 岗位：从 **RINEX NAV + 静态/动态轨迹**生成 GPS L1 C/A **I/Q 基带文件**，供文件回放接收机或 SDR 播放器。冲突时：**本机 `./gps-sdr-sim`（无参看 Usage）/ 仓内 README / `player/` > 本文**。  
> 完整接收机 → [gnss-sdr](./gnss-sdr.md)；口袋捕获 → [pocketsdr](./pocketsdr.md)；事后 RINEX → [rtklib](./rtklib.md)；数据礼仪 → [data-access](../data-access.md)。

## 1. 用途与边界

**做：**

- 静态 `-l`/`-c` 或动态 `-u`/`-x`/`-g`（运动采样 **10 Hz**）生成 GPS L1 IF/基带
- I/Q 位宽 `-b 1|8|16`；默认采样率 **2.6 Msps**（HackRF/bladeRF/Pluto 友好）
- `-v` 打印可见星方位/仰角/伪距；`-i` 关电离层；`-p` 恒定功率
- `player/`：bladeplayer / hackplayer / limeplayer / plutoplayer（需对应 lib）

**不做 / 本机限制：**

- **不是** 接收机 → [gnss-sdr](./gnss-sdr.md) / [pocketsdr](./pocketsdr.md) / [fgi-gsrx](./fgi-gsrx.md)
- **不是** 多星座仿真（仅 GPS L1 C/A；Galileo 另寻专用仿真器）
- **不是** RINEX 观测量生成器
- 仓内 `brdc0010.22n` 仅作冒烟；新产品需 CDDIS/Earthdata → [data-access](../data-access.md)
- 本机 **未** 编 `player/*`、**未** 接 HackRF/USRP → 只验证文件生成

一句话：gps-sdr-sim = **只出 GPS L1 I/Q 的信号源**；接接收机前先对齐采样率/位宽/交织。

| 术语 | 含义 |
| --- | --- |
| `-b 16` | 交织 int16 IQ（对 gnss-sdr `ishort` / PocketSDR `CS16`） |
| `-b 8` | 交织 int8 IQ（HackRF `hackrf_transfer` 常用） |
| `-b 1` | 1-bit 打包（需 bladeplayer 等） |
| `-s` | 采样率 Hz；默认 **2600000**；联调常改 **4000000** |
| `-d` | 时长 s；静态最大 **86400**；动态受 `USER_MOTION_SIZE` |
| `brdc*.YYn` | 日合并广播星历；时间须落在电文 TOC 有效窗 |

## 2. vs gnss-sdr / PocketSDR / FGI-GSRx

| | **本文 gps-sdr-sim** | [gnss-sdr](./gnss-sdr.md) | [pocketsdr](./pocketsdr.md) | [fgi-gsrx](./fgi-gsrx.md) |
| --- | --- | --- | --- | --- |
| 角色 | **只生成** L1 基带 | IQ→PVT | 捕获/跟踪/FE | MATLAB IF→PVT |
| 输入 | NAV + 位置/轨迹 | IF / SDR | IF / FE / Soapy | IF + param |
| 输出 | `.bin` I/Q | NMEA/KML/RINEX | acq 表 / NMEA | `.mat` / RINEX3 |
| 本机 | `make` + 2 s IF | apt + 仿真 PVT | `pocket_acq` | clone；**无 MATLAB** |

混用后果：把仿真真值当天空标定、或把 `-b 8` 文件喂 `ishort`——捕获全灭。

## 3. 安装（Linux GCC）

```bash
sudo apt-get install -y build-essential git
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/osqzss/gps-sdr-sim.git
cd gps-sdr-sim && git rev-parse --short HEAD   # 本机：28ca29a
make clean && make -j$(nproc)
ls -la gps-sdr-sim    # 本机：64016 B
./gps-sdr-sim         # 打印 Usage（exit 非 0 正常）
```

等价直编：`gcc gpssim.c -lm -O3 -o gps-sdr-sim`。长轨迹：`make USER_MOTION_SIZE=4000`。

Windows：VS 建 Console，加 `gpssim.c` + `getopt.c`，Release 构建。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `brdc` 下载失败 | CDDIS 需 Earthdata | 用仓内样例或见 [data-access](../data-access.md) |
| 动态 >300 s 截断 | 默认 `USER_MOTION_SIZE` | 重编加大宏 |
| player 链失败 | 缺 libhackrf/bladeRF… | 先装驱动；本手册不依赖 player |

## 4. 端到端：生成 IF（本机真跑）

### 4.1 静态 2 s / 2.6 Msps / int16（默认率）

```bash
mkdir -p ~/iono_ops/gps-sdr-sim-smoke
cd ~/iono_ops/gps-sdr-sim
./gps-sdr-sim -e brdc0010.22n -l 41.275,1.9876,100 -d 2 -s 2600000 -b 16 \
  -o ~/iono_ops/gps-sdr-sim-smoke/gpssim_2s_2p6M_16b.bin \
  -t 2022/01/01,00:00:00 -v
```

**本机 stdout 要点（2026-09-24 06:53 EDT；质检复跑 06:58 EDT）：**

```text
xyz =   4797686.3,    166499.3,   4185490.2
llh =   41.275000,    1.987600,       100.0
Start time = 2022/01/01,00:00:00 (2190:518400)
Duration = 2.0 [sec]
01  258.3  17.2  23716813.6   3.5
08  320.4  66.6  20621541.5   1.6
27   89.7  72.9  20417433.1   1.5
...
Done!
Process time = 0.2 [sec]   # 质检复跑；写作 0.1
```

产物：**19760000** B ≈ `2 × 2.6e6 × 2 × 2`（秒×采样×I/Q×int16）。可见表 **12** 星与 gnss-sdr/PocketSDR 联调一致。

### 4.2 东京 1 s / int8（HackRF 位宽）

```bash
./gps-sdr-sim -e brdc0010.22n -l 35.681298,139.766247,10.0 -d 1 -s 2600000 -b 8 \
  -o ~/iono_ops/gps-sdr-sim-smoke/gpssim_1s_2p6M_8b.bin \
  -t 2022/01/01,00:00:00 -v
# → 4680000 B；可见 11 星（G05/10/12–15/18/20/23/24/28）
```

### 4.3 联调接收机（已在姊妹手册跑通；本页不重跑长片段）

| 下游 | 推荐旗标 | 文档 |
| --- | --- | --- |
| gnss-sdr | `-s 4000000 -b 16` → conf `item_type=ishort`，`PVT.positioning_mode=Single` | [gnss-sdr](./gnss-sdr.md) |
| PocketSDR | 同 CS16；`pocket_acq -fmt CS16 -f 4 -fi 0 -sig L1CA` | [pocketsdr](./pocketsdr.md) |

本机既有 60 s / 4 Msps / int16（约 **915 MB**）已出 gnss-sdr 首定 **41.275N / 1.98757E**。

### 4.4 发射（有硬件且合法时）

```bash
# 示例骨架——功率/天线/法规自负；本机未跑
# hackrf_transfer -t gpssim.bin -f 1575420000 -s 2600000 -a 1 -x 0
# 或 make -C player hackplayer && ./player/hackplayer …
```

**户外发射 GPS L1 在多数司法辖区违法。** 实验室用屏蔽箱 / 有线耦合；报告写清仿真。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| `-e` NAV | RINEX 2/3 GPS 导航；须覆盖 `-t` |
| `-l` / `-c` | 静：lat,lon,h 或 ECEF |
| `-u` / `-x` / `-g` | 动：ECEF CSV / LLH CSV / NMEA GGA；**10 Hz** |
| `-t` / `-T` | 情景时刻；`-T` 改写 TOC/TOE |

| 输出 | 说明 |
| --- | --- |
| `.bin` | 交织 I/Q；无文件头——元数据靠命令行约定 |
| stdout `-v` | PRN / az / el / range / iono delay |
| 不输出 | 多星座、观测量 RINEX、TEC 图 |

体积粗算：`duration × fs × 2 × (bits/8)`（`-b 1` 另计打包）。

## 6. 参数速查

| 旗标 | 本机常用 | 备注 |
| --- | --- | --- |
| `-s` | `2600000` / `4000000` | 必须与下游一致 |
| `-b` | `16`（接收机文件）/`8`（HackRF） | 错位宽=噪声 |
| `-d` | 冒烟 `2`；PVT `≥60` | 磁盘先算再跑 |
| `-i` | 航天场景 | 关电离层延迟 |
| `-p` | 近场/恒定 CN0 | 可选固定增益 |

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 接收机零捕获 | `-b`/`-s` 与 conf 不一致 | 16↔`ishort`/`CS16`；核对 Msps |
| 2 | 可见星空表 | `-t` 超出 NAV 有效期 | 换当日 brdc 或改 `-t` |
| 3 | 文件差 2× | 把 int16 当 int8 估大小 | 用 §4 公式 |
| 4 | 动态轨迹跳变 | CSV 非 10 Hz / 缺样本 | 重采样；加大 `USER_MOTION_SIZE` |
| 5 | gnss-sdr 无 PVT | 短 IF + `PPP_Static` | 见 [gnss-sdr](./gnss-sdr.md) 改 `Single` |
| 6 | 高度差十几米 | 单频仿真+短弧 | 报告标仿真真值；勿当测地 |
| 7 | 把仿真当真天空 | 流程误解 | 文中写 `-l` 真值 |
| 8 | 户外 `hackrf_transfer` | 违法/干扰 | 屏蔽箱或停 |
| 9 | FGI 默认 26 Msps 8-bit **实数** 对不上 | 前端模型不同 | 勿直接喂 FGI 样例 conf |
| 10 | Makefile `wget` brdc 失败 | 旧 FTP / 需登录 | 手动下 NAV |
| 11 | `-b 1` 用普通播放器 | 需专用 player | 改 `-b 8/16` 或编 bladeplayer |
| 12 | 多星座 conf 套 GPS-only IF | 通道空转 | 先 L1CA 单系统 |

## 8. 接到哪步

1. 出 IF → 本文；捕获 → [pocketsdr](./pocketsdr.md)；完整 PVT → [gnss-sdr](./gnss-sdr.md)  
2. MATLAB 教学接收机 → [fgi-gsrx](./fgi-gsrx.md)（IF 格式另配）  
3. 事后精密定位 → [rtklib](./rtklib.md)（换真实/仿真 RINEX，别硬扛 SDR PVT）  
4. 法规与数据 → [data-access](../data-access.md)

## 9. 选型

| 需求 | 选 |
| --- | --- |
| GPS L1 基带文件 / SDR 源 | **本文** |
| IQ→PVT 完整接收机 | [gnss-sdr](./gnss-sdr.md) |
| 轻量捕获 + Pocket FE | [pocketsdr](./pocketsdr.md) |
| MATLAB 算法实验（多星座 IF） | [fgi-gsrx](./fgi-gsrx.md) |
| RINEX 事后 RTK/PPP | [rtklib](./rtklib.md) |

## 10. 相关

[gnss-sdr](./gnss-sdr.md) · [pocketsdr](./pocketsdr.md) · [fgi-gsrx](./fgi-gsrx.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gps-measurement-tools](./gps-measurement-tools.md) · [data-access](../data-access.md) · [README](./README.md)
