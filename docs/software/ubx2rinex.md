# ubx2rinex · U-Blox UBX→RINEX 采集/反序列化操作手册

目录：[`PROJECTS.json` → `ubx2rinex`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/ubx2rinex> · crates.io **`ubx2rinex` 0.3.0** · tip **`3b67fd0`**（`v0.3.0-6-g3b67fd0`；仓内仍标 0.3.0）· **MPL-2.0** · 默认 feature **UBX V23** · 本机验证 **rustc 1.98.1** + `cargo install ubx2rinex --locked`（需 **libudev-dev**；2026-09-24 05:36 EDT）：被动 `-f` 上游 `F9T-L2-5min.ubx.gz` → OBS **298** 历元 G01 L1C/C1C/D1C；coldstart → OBS **561** + NAV **9** 星历；pyubx2 无 RAWX 样例 **0** 文件

> 岗位：nav-solutions **UBX 流/快照 → RINEX OBS（默认）/NAV（可选）** CLI。冲突时：**本机 `ubx2rinex -h` / 上游 README > 本文**。  
> UBX 编解码库（无 CLI）→ [pyubx2](./pyubx2.md)；串口/NTRIP/录流 CLI → [pygnssutils](./pygnssutils.md)；桌面 GUI → [pygpsclient](./pygpsclient.md)；手机 Logger→RINEX → [android_rinex](./android_rinex.md)/[gps-measurement-tools](./gps-measurement-tools.md)；读进 xarray → [georinex](./georinex.md)；同生态 Rust RINEX QC → [rinex-cli](./rinex-cli.md)。

## 1. 用途与边界

**做：**

- **被动模式** `-f/--file`：读 `.ubx` / `.ubx.gz`（可多次 `-f`），写出 RINEX3（默认）OBS；可选 `--nav` 出 NAV
- **主动模式** `-p/--port`：接 u-blox 串口实时采集（须至少一星座 + `--l1`/`--l2`/`--l5`）；本机**无接收机**，主动模式未实跑
- 星座过滤：`--gps/--galileo/--glonass/--bds/--qzss/--sbas/--irnss`；被动下作**数据滤镜**（不选则默认混星写出）
- 命名：短名（默认）/ `-l --long` + `-c` 三国码长名；`-n` 自定义 stem；`--prefix` 输出目录；`--gzip` / `--crx`
- 头定制：`-m` 接收机型号、`--agency/--observer/--operator`、`--rx-clock` 等

**不做：**

- **不是** UBX 协议百科 / 帧级编解码 API → [pyubx2](./pyubx2.md)
- **不是** 实时监视 GUI → [pygpsclient](./pygpsclient.md)
- **不是** NTRIP/多协议运维 CLI → [pygnssutils](./pygnssutils.md)
- **不是** 手机 GnssLogger→RINEX → [android_rinex](./android_rinex.md)
- **不是** 定位/TEC/PPP → 落盘后走 [georinex](./georinex.md)/[rtklib](./rtklib.md)/[pytecgg](./pytecgg.md)
- NAV 目前实质偏 **GPS（+QZSS）星历**；无 `RXM-RAWX` 的配置/NAV-PVT 日志**不会**出 OBS

一句话：`ubx2rinex` = **UBX→RINEX 采集器**；电离层产品在「OBS/NAV 落盘」之后。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `ubx2rinex` | Rust CLI，clap | `ubx2rinex -V` → `ubx2rinex 0.3.0` |
| [pyubx2](./pyubx2.md) | Python 编解码库 | 无 console script；`import pyubx2` |
| [pygpsclient](./pygpsclient.md) `pyrinexconv` | GUI 捆转换 | tkinter；非本 bin |
| [rinex-cli](./rinex-cli.md) | 已有 RINEX 的 QC/filegen | 不吃 UBX |

| 术语 | 含义 |
| --- | --- |
| 被动 / 主动 | `-f` 文件 vs `-p` 串口（互斥） |
| 默认修订 | RINEX **V3**（`--v2` / `--v4` 可改） |
| 默认快照 | `--period` 默认 **1 h**（文件名常带 `01H`；非日报） |
| `RXM-RAWX` | OBS 观测主源；无则被动常 **0** 文件 |
| `RXM-SFRBX` | NAV 星历主源；F9T 样例无 SFRBX → `--nav` 无 MN |

## 2. 安装

```bash
# rustup（本机 rustc 1.98.1）；串口依赖需系统 libudev
sudo apt-get install -y libudev-dev pkg-config   # Debian/Ubuntu；缺则 libudev-sys build 失败
. "$HOME/.cargo/env"
rustc --version

cargo install ubx2rinex --locked
which ubx2rinex
ubx2rinex -V
# 期望：…/.cargo/bin/ubx2rinex
#       ubx2rinex 0.3.0

ubx2rinex -h

# tip（可选；本机 clone 验证 commit，未强制覆盖 crates bin）
# mkdir -p ~/iono_ops && cd ~/iono_ops
# git clone https://github.com/nav-solutions/ubx2rinex.git
# # data 子模若是 git@…：改 .gitmodules 为 https://github.com/nav-solutions/data.git 再 submodule update
# cd ubx2rinex && git log -1 --oneline   # 3b67fd0 Update itertools…
# cargo install --path . --locked
```

**本机 `ubx2rinex -h`（2026-09-24 EDT，ANSI 已剥；节选）：**

```text
U-Blox stream to RINEX collecter

Usage: ubx2rinex [OPTIONS]

Options:
  -h, --help     Print help
  -V, --version  Print version

Serial port (Active device, GNSS module):
  -p, --port <PORT>            Define serial port. Example /dev/ttyUSB0 on Linux
  -b, --baud <Baudrate (u32)>  … By default we use 115_200

Constellation selection:
      --gps      Activate GPS constellation. …
      --galileo  …
      --bds / --qzss / --glonass / --sbas / --irnss

Signal selection:
      --l1 / --l2 / --l5     … Not required when operating from UBX files

File interface (Passive mode):
  -f, --file <FILENAME>  Load a single UBX file. … Gzip … must be terminated with '.gz'.

RINEX Collection:
  -n, --name <name>      … default "UBXR"
      --prefix <prefix>  …
      --period <period>  … default … 1 hour …
      --v2 / --v4 / -l, --long / --gzip / -c <country>
      --agency / --observer / --operator / --comment …

Observations collection:
      --no-obs / -s, --sampling <sampling> / --no-phase / --no-pr / --no-dop / --crx …

Navigation messages collection:
      --nav / --nav-period / --healthy / --unhealthy
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `libudev` / `pkg-config` build 失败 | 缺开发包 | `apt install libudev-dev pkg-config` |
| `package … requires rustc …` | toolchain 过旧 | rustup stable（本机 1.98.1） |
| 无 stdout 以为挂了 | 日志走 `RUST_LOG` | `export RUST_LOG=info` |
| 主动模式无星座/信号 | clap/运行期要求 | `-p … --gps --l1`（至少） |

## 3. 端到端（本机 0.3.0 真跑；2026-09-24 05:36 EDT）

样例：上游 submodule `data/UBX/`（HTTPS）+ pyubx2 仓内样例。工作目录：`~/iono_ops/ubx2rinex-demo`。

```bash
mkdir -p ~/iono_ops/ubx2rinex-demo/{data,out} && cd ~/iono_ops/ubx2rinex-demo
cp ~/iono_ops/ubx2rinex/data/UBX/F9T-L2-5min.ubx.gz data/          # 359615 B
cp ~/iono_ops/ubx2rinex/data/UBX/16dBatt_no_interference_coldstart.ubx.gz data/  # 1190026 B
cp ~/iono_ops/pyubx2-src/examples/{2023-4-17_82912_serial-COM3.ubx,mon_span.ubx} data/
cp ~/iono_ops/pyubx2-src/tests/pygpsdata-NAV.log data/
export RUST_LOG=info
```

### 3.1 上游 F9T：`--gps` → OBS（有 RAWX）

```bash
ubx2rinex -f data/F9T-L2-5min.ubx.gz --gps --prefix out/f9t \
  -m F9T -c USA -l --agency IonosphereGNSS --observer demo
ls -la out/f9t/
# UBXRUSA_R_20252230000_01H_30S_MO.rnx  658125 B
```

**本机日志（摘录）：**

```text
 INFO  ubx2rinex] … UTC - application deployed
 INFO  ubx2rinex] … UTC - Observation mode deployed
 INFO  ubx2rinex] 2025-08-11T21:36:11 UTC - consumed all content
```

**本机头与首历元（可复现）：**

```text
     3.00           OBSERVATION DATA    GPS                 RINEX VERSION / TYPE
rs-rinex v0.21.1                                            PGM / RUN BY / DATE
                    IonosphereGNSS                          OBSERVER / AGENCY
G   15 L1C C1C D1C L2L L2S C2L C2S D2L D2S L5I L5Q C5I C5Q  SYS / # / OBS TYPES
       D5I D5Q                                              SYS / # / OBS TYPES
                    F9T                                     REC # / TYPE / VERS
                                                            END OF HEADER
> 2025 08 11 21 31 31.0010000  0  9
G01 112252116.071    21360867.696         804.339
…
```

注意头里观测类型顺序是 **L1C C1C D1C**（相位在前）；与常见「C1C L1C」列序不同，读字段勿错位。

| 字段 | 本机值 |
| --- | --- |
| 输入 | `F9T-L2-5min.ubx.gz` **359615** B；pyubx2 计 **3066** 帧 / **RXM-RAWX=299**（无 SFRBX） |
| 输出 | `UBXRUSA_R_20252230000_01H_30S_MO.rnx` **658125** B |
| 历元 | `grep -c '^>'` = **298**；时窗 **2025-08-11 21:31:31 → 21:36:28** |
| georinex 1.16.2 | `{'time': 298, 'sv': 12}`；SV G01…G32（12 颗） |
| G01 首历元 | **L1C=112252116.071** · **C1C=21360867.696** · **D1C=804.339**（georinex 与明文一致）；本切片 L2/L5 对该星为空 |

文件名里的 `0000_01H_30S` 是命名器合成（快照/采样标签），**不等于**体数据已抽稀到 30 s——本文件仍是约 **1 s** 历元。

### 3.2 混星座 / 短名+gzip / `-s` 被动无效

```bash
# 混星：--gps --galileo --glonass --bds --qzss
ubx2rinex -f data/F9T-L2-5min.ubx.gz --gps --galileo --glonass --bds --qzss \
  --prefix out/f9t_multi -m F9T -c USA -l
# → …MO.rnx 1507711 B；头 TYPE=M (MIXED)；历元仍 298；首历元 29 SV（G9+C11+E9）

# 短名 + gzip（-n DEMO）
ubx2rinex -f data/F9T-L2-5min.ubx.gz --gps --prefix out/f9t2 -n DEMO --gzip
# → DEMO223.25O.gz 65321 B；解压后历元仍 298

# 被动下 -s "30 s" 本机仍 298 历元（抽稀不生效；见坑）
ubx2rinex -f data/F9T-L2-5min.ubx.gz --gps -s "30 s" --prefix /tmp/ubx_samp -m F9T
```

不带任何 `--gps`… 时：本机仍写出 **MIXED** 短名（cwd 下 `UBXR223.25O`，约 **1.55 MB**，历元 298，含 G/C/E/S）；帮助文案写「须选星座」，以**实测**为准——要单星座请显式 `--gps` 等。

### 3.3 coldstart：OBS + `--nav`（有 SFRBX）

```bash
ubx2rinex -f data/16dBatt_no_interference_coldstart.ubx.gz --gps --nav \
  --prefix out/cold_nav -m M8 -c USA -l
ls -la out/cold_nav/
# UBXRUSA_R_20251150000_01H_30S_MO.rnx  1252627 B
# UBXRUSA_R_20251100000_01H_30S_MN.rnx     5662 B
```

**OBS：** 历元 **561**；georinex `{'time': 561, 'sv': 9}`；时窗 **2025-04-25 06:38:07 → 06:47:27**；首历元 G06 **L1C=121660195.355** · **C1C=23151165.526** · **D1C=−1815.442**。日志有 `clock reset!` / `phase cycle slip not correctly managed`（见坑）。

**NAV（节选）：**

```text
     3.00           NAVIGATION DATA     GPS                 RINEX VERSION / TYPE
rs-rinex v0.21.1                                            PGM / RUN BY / DATE
                                                            END OF HEADER
G12 2025 04 20 00 00 00-5.816104821861E-04-1.705302565824E-12 0.000000000000E+00
…
```

| 字段 | 本机值 |
| --- | --- |
| MN 大小 / 行 | **5662** B / **75** 行 |
| 星历条数 | **9**（G06 G11 G12 G24 G25 G28 G29 G31 G32） |
| G12 af0 | **−5.816104821861×10⁻⁴**（文件首行） |
| SFRBX | 输入含大量 `RXM-SFRBX`；日志大量 `SFRBX interpretation issue`（本机 cold_nav 约 **336** 条）仍写出上表 9 条 |

F9T 同加 `--nav`：**仅**出 MO（无 MN）——该 gz **无 SFRBX**。`--nav --no-obs` 可只出 MN，但无 OBS 时文件名 TOC 可能怪异（本机曾见 `…3280943292250000…_MN.rnx`）。

### 3.4 边界：pyubx2 样例无 RAWX → 0 文件

```bash
# COM3：仅 CFG-VALGET/ACK（133 帧，0 RAWX）
ubx2rinex -f data/2023-4-17_82912_serial-COM3.ubx --gps --galileo --glonass --bds \
  --prefix out/com3 -n COM3
# mon_span：MON-SPAN/HNR-PVT/…（109 帧，0 RAWX）
ubx2rinex -f data/mon_span.ubx --gps --prefix out/mon -n MONS
# pygpsdata-NAV.log：NAV-PVT 等（28 帧，0 RAWX）
ubx2rinex -f data/pygpsdata-NAV.log --gps --prefix out/navlog -n NAVL
```

**本机：** 均 `Observation mode deployed` → `1900-01-01T00:00:00 UTC - consumed all content`；**对应 out 目录空**（无 `.rnx`）。工具吃的是 **RAWX/SFRBX 二进制 UBX**，不是「任意 UBX/NAV 日志」。录观测请开 `RXM-RAWX`（及需要的 NAV 开 `RXM-SFRBX`）；编解码验收仍用 [pyubx2](./pyubx2.md)。

### 3.5 主动模式（有硬件时；本机未跑）

```bash
# 示例（上游 README）；须 -p + 星座 + 信号
RUST_LOG=info ubx2rinex -p /dev/ttyACM0 -b 115200 --gps --l1 -m M8T --rx-clock
```

本机无 `/dev/ttyACM*` / USB GNSS，**未**捕获主动模式 stdout。

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `-f FILE`（可重复） | 被动读 UBX；`.gz` 后缀须为 `.ubx.gz` |
| `-p PORT` / `-b` | 主动串口；默认波特率 **115200** |
| `--gps`… | 星座；被动=滤镜；主动=配置意图 |
| `--l1/--l2/--l5` | 主动信号；被动**不需要** |
| （默认）/ `--no-obs` / `--nav` | OBS 开 / 关 OBS / 开 NAV |
| `-n` / `-l -c` / `--prefix` / `-m` | 名 / 长名+国码 / 目录 / 接收机标签 |
| `--period` / `-s` | 快照时长（默认 1 h）/ 采样（**主动**语境；被动本机未抽稀） |
| `--gzip` / `--crx` / `--v2`/`--v4` | 压缩 / CRINEX / 修订 |

| 本机产物 | 大小 / 要点 |
| --- | --- |
| F9T `--gps` MO | **658125** B；**298** 历元；G01 C1C=**21360867.696** |
| F9T 混星 MO | **1507711** B；**298** 历元；首历元 **29** SV |
| F9T `--gzip` 短名 | `DEMO223.25O.gz` **65321** B |
| coldstart MO / MN | **1252627** / **5662** B；OBS **561**；NAV **9** eph |
| pyubx2 无 RAWX 三样例 | **0** 输出文件 |

## 5. 接到哪步

```text
u-blox .ubx / .ubx.gz（含 RXM-RAWX）
  → ubx2rinex（本文）→ OBS[/NAV] RINEX
  →（可选）rinex-cli QC / rinexmod 改头
  → georinex / gnsspy → gnss-tec / pytecgg / rtklib
无 RAWX 的配置流 / NAV-PVT 日志 → pyubx2 解析；或改接收机输出再录
实时串口运维 / NTRIP → pygnssutils / pygpsclient
手机 Logger → android_rinex / gps-measurement-tools
```

路径 C 可在 [pyubx2](./pyubx2.md) 旁并列本文做「板卡 RAW→RINEX」落盘。

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `cargo install` 报 libudev | 缺 `libudev-dev` | `apt install libudev-dev pkg-config` |
| 2 | COM3 / mon_span / NAV.log → 空目录 | 无 `RXM-RAWX` | 用含 RAWX 的快照（上游 `data/UBX`）；配置流改走 pyubx2 |
| 3 | F9T `--nav` 无 MN | 该文件无 SFRBX | 换含 `RXM-SFRBX` 的录制（如 coldstart） |
| 4 | 大量 `SFRBX interpretation issue` | 解码不完整 | 仍可能写出部分 NAV；核对星数/af0；勿当完美星历源 |
| 5 | `clock reset` / cycle slip 警告 | coldstart 时钟跳 | 当前版声明未妥善管周跳；后处理自检 |
| 6 | 被动 `-s "30 s"` 仍 1 s 历元 | 采样旗标对文件流本机无效 | 事后用 [rinex-cli](./rinex-cli.md)/[gfzrnx](./gfzrnx.md) 抽稀 |
| 7 | 文件名 `01H_30S` 与体不一致 | 命名标签≠实际采样 | 以历元行/`georinex` 为准 |
| 8 | OBS 列序 L1C→C1C→D1C | 头 SYS/#/OBS TYPES 如此 | 按类型名读，勿按「码相位多普勒」习惯硬猜列号 |
| 9 | `--no-obs --nav` 文件名 TOC 怪异 | 无观测时时间锚异常 | 尽量 OBS+NAV 同跑；或事后 [rinexmod](./rinexmod.md) 改名 |
| 10 | 无 `RUST_LOG` 几乎静默 | tracing 默认安静 | `RUST_LOG=info` |
| 11 | data 子模 `git@…` clone 失败 | SSH 未配 | `.gitmodules` 改 HTTPS 再 `submodule update` |
| 12 | `--all-features` | 上游：UBX 协议 feature 互斥 | 只选 `ubx23`（默认）或其一 |
| 13 | 当 UBX 百科 / GUI | 职责仅转 RINEX | pyubx2 / pygpsclient |
| 14 | 混星时 `no available capacity` / `channel closed` | 内部通道背压 | 用 `--gps` 收窄；检查是否仍写出完整历元 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| UBX 文件/串口 → RINEX OBS/NAV | **本文 ubx2rinex** |
| 脚本解析/构造 UBX 帧 | [pyubx2](./pyubx2.md) |
| 录流/NTRIP/过滤 CLI | [pygnssutils](./pygnssutils.md) |
| 桌面联调 | [pygpsclient](./pygpsclient.md) |
| 手机 Logger → RINEX | [android_rinex](./android_rinex.md) / [gps-measurement-tools](./gps-measurement-tools.md) |
| 已有 RINEX 的 QC/滤星座 | [rinex-cli](./rinex-cli.md) / [georinex](./georinex.md) |
| RTCM3 → RINEX | [rtcm3torinex](./rtcm3torinex.md) / [bnc](./bnc.md) |

## 8. 相关

[pyubx2](./pyubx2.md) · [pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · [android_rinex](./android_rinex.md) · [gps-measurement-tools](./gps-measurement-tools.md) · [georinex](./georinex.md) · [rinex-cli](./rinex-cli.md) · [rinexmod](./rinexmod.md) · [rtcm3torinex](./rtcm3torinex.md) · [rtklib](./rtklib.md) · [README](./README.md)
