# PocketSDR · Takasu 口袋式 GNSS 软件接收机操作手册

目录：[`PROJECTS.json` → `PocketSDR`](../../PROJECTS.json) · 上游 <https://github.com/tomojitakasu/PocketSDR> · tip **`03787da`** · 文案 **ver. 0.20**（2026-08-08）· 许可 **BSD-2-Clause**（`LICENSE.txt`）· 本机验证（**2026-09-24 06:50 EDT**；质检复跑 **06:53 EDT**）：`lib/build`+`app` `make USE_SOAPY=0` → `bin/pocket_acq` **3115320** B / `pocket_acq ver.0.20`；对 `gps-sdr-sim` CS16 2 s 切片：`C/N0≥40` 命中 **12** 星（G01/07/08/10/16/21–23/26/27/30/32；C/N0 与写作稿逐行对齐：G01=**47.2**/G08=**52.9**/G10=**51.3**/G27=**54.2**）；`TIME=1.851 s`（写作 **3.153 s**，墙时变）；`pocket_scan` 无 FE→`USB device list get error`；短 IF `pocket_trk`→`memory allocation error size=0`/**无** NMEA；**无 Pocket FE 硬件**；**未臆造**天空 PVT 坐标

> 岗位：用 **Pocket SDR FE**（或 Soapy 前端）+ C/Python AP 做多星座捕获/跟踪/PVT 实验。冲突时：**仓内 `doc/command_ref.md` / `pocket_* -h` / 本机冒烟 > 本文**。  
> 完整 GNU Radio 风格接收机 → [gnss-sdr](./gnss-sdr.md)；事后解算 → [rtklib](./rtklib.md)（本仓捆 `lib/RTKLIB`）；手机原始测量 → [gps-measurement-tools](./gps-measurement-tools.md)。

## 1. 用途与边界

**做：**

- 多星座多频：**GPS / GLO / GAL / QZSS / BDS / NavIC / SBAS**（信号 ID 见仓内 PDF）
- 工具：`pocket_acq` / `pocket_trk` / `pocket_dump` / `pocket_conf` / `pocket_scan` / `pocket_web`…
- 文件回放：`INT8` / `INT8X2` / `CS8` / `CS16` / FE `RAW*`；可选 `.tag` 旁路元数据
- Soapy：Lime / HackRF / Pluto / RTL 等（`USE_SOAPY=1` + 系统 Soapy 包）

**不做 / 本机限制：**

- **不是** 即插即用测绘接收机；FE 采样质量定上限
- **不是** [gnss-sdr](./gnss-sdr.md)（无 GNU Radio 流图；API/conf 完全不同）
- **不是** 只生成基带 → gps-sdr-sim
- 仓内 `sample/*.bin` 仅 **~100 ms**；长样本多在 `*.link` 外链 zip（需另下）
- 本机 **无** FE → `pocket_scan` 失败正常；用仿真 IF 做捕获冒烟

一句话：PocketSDR = **Takasu 系紧凑 SDR 接收机 + FE 生态**；教学/算法友好，生产监测站请自建标定。

| 术语 | 含义 |
| --- | --- |
| FE 2/4/8CH | 专用 USB 前端；VID `04B4`；udev 见 `driver/99-pocket-sdr.rules` |
| `.tag` | IF 旁路：格式/采样率/LO；无 tag 时必须手写 `-fmt/-f/-fi` |
| `CS16` | 交织 int16 IQ（对接 `gps-sdr-sim -b 16`） |
| `-f`（acq） | **MHz** 数值（源码 `*1e6`）；`-f 4` = 4 Msps |
| Soapy | 第三方 SDR 抽象；本机冒烟关 `USE_SOAPY=0` |

## 2. vs gnss-sdr / RTKLIB / gps-measurement-tools

| | **本文 PocketSDR** | [gnss-sdr](./gnss-sdr.md) | [rtklib](./rtklib.md) | [gps-measurement-tools](./gps-measurement-tools.md) |
| --- | --- | --- | --- | --- |
| 输入 | IF / FE / Soapy | IF / UHD/Osmo… | RINEX | 手机 Logger 文本 |
| 输出 | 捕获表 / NMEA / RTCM（trk） | PVT/KML/NMEA/RINEX | `.pos` | MATLAB / 经 android_rinex |
| 本机 | 源码 make + `pocket_acq` | apt 0.0.20 + 仿真 PVT | apt/自编 | demo→RINEX |
| 作者系 | Tomoji Takasu | CTTC | Takasu（同系捆进 lib） | Google |

## 3. 安装（Linux，无 Soapy）

```bash
sudo apt-get install -y git build-essential libusb-1.0-0-dev libfftw3-dev
# 可选：python3-numpy python3-scipy python3-matplotlib python3-tk

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/tomojitakasu/PocketSDR.git
cd PocketSDR && git rev-parse --short HEAD   # 本机：03787da

cd lib/build
make clean && make USE_SOAPY=0 -j$(nproc) && make USE_SOAPY=0 install
# → ../linux/libsdr.so libsdr.a librtk.so …

cd ../../app
make clean && make USE_SOAPY=0 -j$(nproc) && make USE_SOAPY=0 install
# → ../bin/pocket_acq pocket_trk pocket_scan …

export PATH="$HOME/iono_ops/PocketSDR/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/iono_ops/PocketSDR/lib/linux:$LD_LIBRARY_PATH"
pocket_acq -v    # 期望：pocket_acq ver.0.20
```

**勿** `USE_FFTW=1` 却不装齐依赖：apps 仍链 `libpocketfft.a`；本机用默认 PocketFFT 最省事。

有 FE 时：

```bash
sudo cp driver/99-pocket-sdr.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -aG plugdev "$USER"   # 重新登录
pocket_scan                        # 应列出 04B4 设备
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No rule … libpocketfft.a` | `USE_FFTW=1` 跳过 pocketfft | `USE_SOAPY=0` 默认重编 |
| `USB device list get error` | 无 FE / 无权限 | 预期（无硬件）；或 udev+plugdev |
| Python `import numpy` 失败 | 未装系统/venv 包 | `apt install python3-numpy` 或 venv |

## 4. 端到端：仿真 CS16 → pocket_acq（本机真跑）

与 [gnss-sdr](./gnss-sdr.md) 同一生成器；切 2 s 即可捕获：

```bash
# 假定已有 gpssim_4M_16b.bin（4 Msps、int16 IQ）
dd if=~/iono_ops/gnss-sdr-smoke/gpssim_4M_16b.bin \
   of=~/iono_ops/gnss-sdr-smoke/gpssim_2s_cs16.bin bs=1M count=32

cd ~/iono_ops/PocketSDR
pocket_acq -fmt CS16 -f 4 -fi 0 -sig L1CA -prn 1-32 -tint 20 \
  ~/iono_ops/gnss-sdr-smoke/gpssim_2s_cs16.bin \
  2>~/iono_ops/gnss-sdr-smoke/pocket_acq_sim.err \
  | tee ~/iono_ops/gnss-sdr-smoke/pocket_acq_sim.log
```

**本机 stdout（节选，2026-09-24 06:50 EDT）：**

```text
SIG= L1CA, PRN=   1, COFF=  0.64175 ms, DOP=  3011 Hz, C/N0= 47.2 dB-Hz
SIG= L1CA, PRN=   8, COFF=  0.83650 ms, DOP=  1196 Hz, C/N0= 52.9 dB-Hz
SIG= L1CA, PRN=  10, COFF=  0.68125 ms, DOP= -1377 Hz, C/N0= 51.3 dB-Hz
SIG= L1CA, PRN=  27, COFF=  0.06500 ms, DOP=  -902 Hz, C/N0= 54.2 dB-Hz
...
TIME = 1.851 s
```

`C/N0≥40`：**12** 颗，与 `gps-sdr-sim` 可见表 / [gnss-sdr](./gnss-sdr.md) 跟踪集一致（质检复跑 C/N0 **逐行对齐**写作稿）。`TIME` 墙时本次 **1.851 s**（首跑曾记 **3.153 s**——勿当算法恒定耗时）。stderr 有 `tag file open error … .tag` **可忽略**（无旁路 tag 时的提示）。仓内 `sample/L1_*_12MHz_I.bin` 用 `-fmt INT8 -f 12 -fi 3`；仅 100 ms，虚警多，**勿**当灵敏度金标准。

跟踪/PVT（有更长 IF + 正确 `-fo`/`-IQ` 时）：

```bash
pocket_trk -h | head
# 文件源示例（参数以 command_ref 为准；错 fo 会 memory allocation error）
# pocket_trk -fmt CS16 -f 4e6 -fo 1575.42e6 -IQ 2 -sig L1CA -prn 1,8,10,27 \
#   -nmea /tmp/pocket.nmea /path/to/long.cs16
```

本机短切片上 `pocket_trk` 报 `memory allocation error size=0`→**无** `/tmp/pocket_qc.nmea`（质检 06:53 复认；诚实边界）。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IF 文件 | 格式与 `-fmt` 一致；有 `.tag` 则覆盖 CLI 采样参数 |
| Pocket FE | `pocket_conf` 载入 `conf/pocket_*.conf` 后 `pocket_dump`/`pocket_trk` |
| Soapy 设备 | 需编译 Soapy；见 `doc/notes_soapy_dev.md` |

| 输出 | 说明 |
| --- | --- |
| `pocket_acq` | 每 PRN 一行 COFF/DOP/C/N0 |
| `pocket_trk` | 可选 `-nmea` / `-rtcm` / `-log` |
| 不输出 | IONEX / 校准 TEC；观测进 Python → 先落 RINEX 再 [georinex](./georinex.md) |

## 6. 硬件诚实边界

1. FE 要 **USB3 口 + 足够供电**；Pi 5 可用但 CPU/USB 路由有笔记（README）  
2. 第三方 SDR 的时钟稳定度 / 前端滤波往往差于 Pocket FE——比灵敏度前先统一前端  
3. 无 udev → 必须 `sudo`，或加入 `plugdev`  
4. 户外发射仿真信号涉无线电法规；实验室用屏蔽箱  
5. Windows 预编译在 `bin/*.exe`；Linux 以本机构建为准  

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `tag file open error` | 无 `.tag` | 可忽略；补 `-fmt/-f/-fi` |
| 2 | 捕获全是 ~35 dB-Hz | 门限噪声 / 错格式 | 查 `CS16`↔`-b 16`；看高 C/N0 子集 |
| 3 | `-f 4000000` 怪结果 | acq 的 `-f` 以 **MHz** 计 | 写 `-f 4` |
| 4 | `libpocketfft.a` missing | FFTW 开关与 apps 不一致 | `USE_SOAPY=0` 全量重装 |
| 5 | `USB device list get error` | 无 FE | 文件源冒烟；有 FE 查 udev |
| 6 | `memory allocation error size=0` | trk 参数/fo 不匹配 | 读 `command_ref`；加长 IF |
| 7 | 100 ms sample 当论文灵敏度 | 样本太短 | 下 `*.link` 长包或自采 |
| 8 | 与 gnss-sdr conf 混用 | 生态不同 | 各走各文档 |
| 9 | Python AP 缺 numpy | 系统包未装 | apt/venv |
| 10 | 把捕获 DOP 当用户速度 | 含义是载波多普勒 | 只报 C/N0/COFF |
| 11 | Soapy 未编却 `-driver` | `USE_SOAPY=0` | 重编开 Soapy 或换 FE |
| 12 | 无 FE 却写实时 PVT 坐标 | 臆造 | 本文只报 acq 表 |

## 8. 接到哪步

1. 生成 IF → gps-sdr-sim；对照完整 PVT → [gnss-sdr](./gnss-sdr.md)  
2. 落 RINEX / 精密解 → [rtklib](./rtklib.md) / [georinex](./georinex.md)  
3. 手机链路 → [gps-measurement-tools](./gps-measurement-tools.md)  
4. 算法改码：从 `src/sdr_*.c` / `python/sdr_*.py` 下手（模块小于 gnss-sdr）  
5. 数据与法规 → [data-access](../data-access.md)

## 9. 选型

| 需求 | 选 |
| --- | --- |
| Pocket FE / 轻量多星座实验 | **本文** |
| GNU Radio 风格完整站 | [gnss-sdr](./gnss-sdr.md) |
| RINEX 事后 RTK/PPP | [rtklib](./rtklib.md) |
| 手机原始测量 | [gps-measurement-tools](./gps-measurement-tools.md) |

## 10. 相关

[gnss-sdr](./gnss-sdr.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gps-measurement-tools](./gps-measurement-tools.md) · [android_rinex](./android_rinex.md) · [laika](./laika.md) · [data-access](../data-access.md) · [README](./README.md)
