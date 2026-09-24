# rinex2bin · RINEX→BINEX 序列化 CLI 操作手册

目录：[`PROJECTS.json` 提及](../../PROJECTS.json) · crates.io **`rinex2bin` 0.1.0**（bin **`rinex2bin`**）· 上游 <https://github.com/rtk-rs/rinex2bin>（GitHub **301→** [nav-solutions/rinex2bin](https://github.com/nav-solutions/rinex2bin)）· tip **`cc74460`**（tag **`v0.1.0`**；仓内仍 **0.1.0**）· **MPL-2.0** · ★**1** · 依赖锁 **`rinex` 0.17.0** + **`binex` 0.4.2** · 本机验证 **rustc 1.98.1** + `cargo install rinex2bin --locked`（2026-09-24 07:01 EDT）：ESBC MN `--skip` → debug **MonumentGeo×3** + **EphemerisFrame×2640**（GLO **510**/SBAS **2130**）；落盘短名 **`ESBC1770.20N.bin`** **10821632 B**（=**2642×4096**；流尽后忙等须 `timeout`/`kill`）；GLO3 切片 R01 `clock_offset_s`=**6.355904042721×10⁻⁵**≡RINEX；无 `--skip` 大头注释 → **`NotEnoughBytes`**；OBS 仅头；`demo.10o` → **`datime parsing`**

> 岗位：把 RINEX（优先 **NAV**）序列化成 **BINEX** 二进制流/`.bin` 文件，便于紧凑分发或写 I/O。冲突时：**本机 `rinex2bin -h` / crates README > 本文**。  
> 上游 README 明确：**Observation RINEX is work in progress**。同生态解析库 → [rinex](./rinex.md)；QC/filegen → [rinex-cli](./rinex-cli.md)；Python 读盘 → [georinex](./georinex.md)；CRX→RNX → [crx2rnx](./crx2rnx.md)；UBX→RINEX → [ubx2rinex](./ubx2rinex.md)；RINEX→CGGTTS → [rnx2cggtts](./rnx2cggtts.md)。**BINEX 序列化 ≠ 定位/TEC。**

## 1. 用途与边界

**做：**

- CLI：`rinex2bin [OPTIONS] <filepath>` —— 读 RINEX（含 `.gz` 后缀）→ 默认写出自动命名 `.bin`；或 `-o` / `--stream`
- 编码元数据：默认 **big-endian**；`-l` little；`-c` enhanced CRC；`-r` reversed
- `--skip`：跳过 RINEX **Header 注释段**序列化（直接进 record）
- `-s`：自动文件名偏 **V2 短名**；`--gzip`：压缩写出（与 `-o …gz` 路径相关，见坑）

**不做：**

- **不是** 定位 / PPP / 共视时间比对 → [rtklib](./rtklib.md)/[rnx2cggtts](./rnx2cggtts.md)
- **不是** TEC / 电离层产品 → [georinex](./georinex.md)/[gnss-tec](./gnss-tec.md)/[pytecgg](./pytecgg.md)
- **不是** RINEX QC / filegen → [rinex-cli](./rinex-cli.md)
- **不是** 完整 OBS→BINEX 观测体（`rinex` **0.17** 流化器实质只挂 **Nav** 子流；OBS 本机仅 **MonumentGeo 头**）
- **不是** 可靠「跑完即退」的生产批处理：本机 crates **0.1.0** 在 iterator 穷尽后 **`None` 忙等不退出**（须外部 `timeout`/`kill`）；且每条消息 `write` **整页 4096 B**（大量尾零）

一句话：`rinex2bin` = **RINEX→BINEX 序列化小刀**；当前实用面偏 **NAV（GLO/SBAS 本机可出帧）**，OBS/GPS 等见 §3。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `rinex2bin` | Rust CLI | `rinex2bin -V` → `rinex2bin 0.1.0` |
| [rinex](./rinex.md) | 纯库 | `cargo add rinex`；无同名 bin |
| [rinex-cli](./rinex-cli.md) | QC/filegen | 不写 BINEX |
| crates `binex` | BINEX 编解码库 | 无本手册同名 CLI 承诺 |

| 术语 | 含义 |
| --- | --- |
| MonumentGeo | BINEX 地标/注释帧；工具用其宣布流开始、软件名、接收机/机构、头注释 |
| EphemerisFrame | NAV 体：本机见 **GLO** / **SBAS**（GPS/GAL/BDS/QZSS forge 常失败） |
| `--skip` | 跳过把全部 Header COMMENT 打成一条超大 MonumentGeo |
| 4096 B 页 | `main` 固定缓冲；`encode` 返回长度**未**用于截断 `write` |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1

cargo install rinex2bin --locked
which rinex2bin
rinex2bin -V
# 期望：…/.cargo/bin/rinex2bin
#       rinex2bin 0.1.0

rinex2bin -h

# tip（可选；本机 clone 验证，未强制覆盖 crates bin）
# mkdir -p ~/iono_ops && cd ~/iono_ops
# git clone https://github.com/nav-solutions/rinex2bin.git   # rtk-rs 仓 301→此处
# cd rinex2bin && git log -1 --oneline   # cc74460 release (#3)
# cargo install --path . --locked
```

**锁文件关键依赖（crates 0.1.0 `Cargo.lock`）：** `rinex` **0.17.0**（feature `flate2`/`binex`）· `binex` **0.4.2** · `clap` **4.x** · `flate2` · `env_logger`。本机 **`cargo install rinex2bin --locked` 在 rustc 1.98.1 下一次通过**（无需降 toolchain）。

**本机 `rinex2bin -h`（2026-09-24 EDT，ANSI 已剥）：**

```text
RINEX to BINEX

Usage: rinex2bin [OPTIONS] <filepath>

Options:
  -h, --help     Print help (see more with '--help')
  -V, --version  Print version

Input:
  <filepath>  Input RINEX file

BINEX (forging):
  -l, --little  Encoded stream uses Little endianness. Big endiannes is the default
  -c, --crc     Encode stream uses enhanced CRC technique (for very robust messaging).
  -r, --rev     Forge a Reversed BINEX Stream.
      --skip    Skip RINEX Header section serialization.

Output File:
  -o, --output <filepath>  Define output BIN file name. Otherwise, BIN file name is guessed fron RINEX content.
  -s, --short              Prefer V2 (short) file name when auto guessing the BIN file name.

Streaming:
      --stream <writable interface>  Stream on custom I/O interface, instead of forging a BIN file.
      --gzip                         Gzip compress the BINEX stream.
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 进程不退、CPU 空转 | iterator `None` 后 `loop` 未 `break` | 一律 `timeout … rinex2bin …`；测完 `pkill -x rinex2bin` |
| `BINEX encoding error: NotEnoughBytes` | 大头 COMMENT 单帧 > **4096 B** | 加 **`--skip`**；或先裁头注释 |
| `datime parsing` / `open error` | 拒识短名/缺文件 | 换 RINEX3 样例；检查路径 |
| OBS 无观测体 | WIP；流化器只挂 Nav | 勿期望 OBS→MSM；只取头 MonumentGeo |

## 3. 端到端（本机 0.1.0 真跑；2026-09-24 07:01 EDT）

样例：与 [rinex-cli](./rinex-cli.md)/[rnx2cggtts](./rnx2cggtts.md) 同源 ESBC MN；ACOR OBS；[ubx2rinex](./ubx2rinex.md) coldstart NAV；`demo.10o`。工作目录：`~/iono_ops/rinex2bin-demo`。

```bash
mkdir -p ~/iono_ops/rinex2bin-demo/{data,out,logs} && cd ~/iono_ops/rinex2bin-demo
cp ~/iono_ops/rnx2cggtts-demo/data/ESBC00DNK_R_20201770000_01D_MN.rnx data/
cp ~/iono_ops/rinex-cli-demo/data/{ACOR00ESP_R_20213550000_01D_30S_MO.rnx,demo.10o,ESBC00DNK_R_20201770000_01D_MN.rnx.gz} data/
cp ~/iono_ops/ubx2rinex-demo/out/cold_nav/UBXRUSA_R_20251100000_01H_30S_MN.rnx data/
export RUST_LOG=debug
```

### 3.1 ESBC MIXED NAV + `--skip`（有 EphemerisFrame）

```bash
# 无 --skip：大 B_STK 头注释 → panic NotEnoughBytes（见 §3.4）
timeout --signal=KILL 20s rinex2bin --skip -o out/esbc_skip.bin \
  data/ESBC00DNK_R_20201770000_01D_MN.rnx > logs/esbc_skip.log 2>&1
# exit 137（KILL）；勿等自然退出
```

**本机 debug 计数（`rg`）：**

| 量 | 值 |
| --- | --- |
| `Streaming: Message` | **2643** |
| MonumentGeo | **3**（announce / 空机构帧 / `RINEX Record starting!`） |
| EphemerisFrame | **2640** = GLO **510** + SBAS **2130** |
| 输入 NAV 头行（对照） | C **357** / E **1602** / G **257** / J **15** / R **510** / S **2130** |
| GPS/GAL/BDS/QZSS 帧 | **0**（`forge_*` 返回 `None`；遇失败可截断后续星座） |
| 落盘（KILL 前） | **10821632 B** = **2642×4096**（末消息可能未刷满；尾零占比极高） |

宣布串（真实）：`rtk-rs/rinex2bin v0.1.0 from V3 MIXED NAVIGATION DATA`；底层标 `rtk-rs/rinex v0.17.0`。

**自动命名 / gzip 输入 / 短名（cwd=`out/`）：**

```bash
cd out
timeout --signal=KILL 12s rinex2bin --skip ../data/ESBC00DNK_R_20201770000_01D_MN.rnx.gz
# → ESBC00DNK_R_20201771950_01D_MN.rnx.bin（TOC 取自首历元约 19:50）
timeout --signal=KILL 12s rinex2bin --skip -s ../data/ESBC00DNK_R_20201770000_01D_MN.rnx.gz
# → ESBC1770.20N.bin  10821632 B
```

### 3.2 GLO 三星历切片（字段对应）

自 ESBC 抽出 3 条 `R*` 写入 `data/ESBC_GLO3.rnx` 后：

```bash
timeout --signal=KILL 5s rinex2bin --skip -o out/glo3.bin data/ESBC_GLO3.rnx > logs/glo3.log 2>&1
```

**本机：** MonumentGeo **3** + EphemerisFrame(GLO) **3**；`glo3.bin` **16384 B**（**4×4096**，刷盘不全）。首帧：

```text
EphemerisFrame(GLO(GLOEphemeris { … clock_offset_s: 6.355904042721e-5, … x_km: 10908.94238281, … }))
```

对照 RINEX 行：`R01 2020 06 24 23 15 00 6.355904042721e-05 …` —— **钟差一致**。

### 3.3 OBS / ubx2rinex NAV / ACOR 头字段

```bash
# ACOR OBS（25 历元）——仅头，无观测体
timeout --signal=KILL 8s rinex2bin -o out/acor2.bin \
  data/ACOR00ESP_R_20213550000_01D_30S_MO.rnx > logs/acor2.log 2>&1
# MonumentGeo×5：announce「V3 MIXED OBS DATA」；ObserverName=IGNE；
# ReceiverType=LEICA GR50 / Number=1833574 / FW=4.50/7.710；头注释；Record starting
# 体：无 EphemerisFrame / 无观测 BINEX（WIP）

# ubx2rinex coldstart GPS NAV（9 星历）——头后无 GPS EphemerisFrame
timeout --signal=KILL 8s rinex2bin --skip -o out/cold_skip.bin \
  data/UBXRUSA_R_20251100000_01H_30S_MN.rnx
# announce：from V3 GPS NAVIGATION DATA；其后 forge_gps 失败 → 仅 MonumentGeo
```

### 3.4 失败边界（如实）

```bash
# ESBC 无 --skip
rinex2bin -o out/esbc_mn.bin data/ESBC00DNK_R_20201770000_01D_MN.rnx
# → panic: BINEX encoding error: NotEnoughBytes

# demo.10o
rinex2bin -o out/demo.bin data/demo.10o
# → panic: RINEX parsing error: datime parsing

# 缺文件
rinex2bin /no/such.rnx
# → panic: from_file: open error: … NotFound …；exit **101**
```

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `<filepath>` | 必填；明文或名以 `.gz` 结尾的 gzip RINEX |
| `-o` / （默认） | 自定义名 / 按内容猜名（R3 常带 `…MN.rnx.bin`） |
| `-s` | 短名（本机 ESBC → `ESBC1770.20N.bin`） |
| `--skip` | 跳过超大头注释序列化 |
| `-l`/`-c`/`-r` | 字节序 / 增强 CRC / reversed |
| `--stream` | 写到已有可写接口（本机未接真串口） |
| `--gzip` | 压缩意图（与自动名/`-o` 后缀组合；以实测落盘为准） |

| 本机产物 | 大小 / 要点 |
| --- | --- |
| `ESBC1770.20N.bin`（`--skip -s` + gz 入） | **10821632 B**；debug 帧 **2643**；GLO+SBAS |
| `glo3.bin` | **16384 B**；GLO×**3**；R01 钟差对齐 |
| ACOR OBS `.bin` | 头 MonumentGeo 仅；**25** 历元未进体 |
| `demo.10o` | **无**产物（panic） |

## 5. 接到哪步

```text
RINEX NAV（最好先裁掉巨型 COMMENT / 或 --skip）
  → rinex2bin（本文）→ .bin / I/O 流
  → 下游 BINEX 消费者（接收机/自研；本仓无专用反序列化手册）
OBS 归档 → 仍用 rinex-cli / georinex / crx2rnx；勿指望本文出观测体
需要共视 / TEC / 定位 → rnx2cggtts / gnss-tec / rtklib（本工具不替代）
```

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 命令「跑完」仍挂 | `None => {}` 忙等 | `timeout`/`kill`；测完确认无 `rinex2bin` 进程 |
| 2 | `.bin` 远大于有效载荷 | 每消息 `write` 整 **4096 B** | 知晓尾零；勿当「紧凑比」宣传值 |
| 3 | ESBC 无 `--skip` panic | 头 COMMENT 单帧过大 | **`--skip`** 或删 B_STK 类注释 |
| 4 | GPS NAV 无 EphemerisFrame | `forge_gps` 轨道键/类型失败 | 本机仅 GLO/SBAS 稳定出帧；勿臆造 GPS 帧数 |
| 5 | OBS 只有 MonumentGeo | OBS 流未实现 | 上游 WIP；观测走别的工具 |
| 6 | `demo.10o` panic | R2/短名 datime | 用 RINEX3 长名样例 |
| 7 | 成功路径几乎无「has been generated」 | README 示例有、crates **0.1.0** `main` **无**该打印 | 以 `RUST_LOG=debug` 帧计数 + 落盘为准 |
| 8 | `--gzip` 与自动名 | 实现分支绕 | 显式 `-o file.bin.gz` 并核对体积 |
| 9 | 仓库字段 `rtk-rs/…` | 已迁 **nav-solutions** | clone 用新 URL；版本仍以 crates **0.1.0** 为准 |
| 10 | 当定位/TEC 工具 | 只做序列化 | 见边界表 |
| 11 | 并行残留进程占盘 | 忘杀 | `pkill -x rinex2bin` |
| 12 | 与 [rinex-cli](./rinex-cli.md) tip `cbin` 混淆 | 另一入口/版本 | 以本机 `rinex2bin -h` 为准 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| RINEX→BINEX CLI（NAV 试验/紧凑流） | **本文 rinex2bin** |
| RINEX QC / 滤星座写回 | [rinex-cli](./rinex-cli.md) |
| 纯库解析/写回 | [rinex](./rinex.md) |
| Python→xarray | [georinex](./georinex.md) |
| CRX→RNX | [crx2rnx](./crx2rnx.md) |
| UBX→RINEX | [ubx2rinex](./ubx2rinex.md) |
| RINEX→CGGTTS | [rnx2cggtts](./rnx2cggtts.md) |

## 8. 相关

[rinex](./rinex.md) · [rinex-cli](./rinex-cli.md) · [georinex](./georinex.md) · [crx2rnx](./crx2rnx.md) · [ubx2rinex](./ubx2rinex.md) · [rnx2cggtts](./rnx2cggtts.md) · [haslib](./haslib.md)（SBF/BINEX→SSR 另一语境）· [README](./README.md)
