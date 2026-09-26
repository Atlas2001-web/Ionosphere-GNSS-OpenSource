# EarthScope gnsstools · Go GNSS 格式编解码库 + CLI（gnss-convert / gnss-inspect）操作手册

> gitlab.com/earthscope/gnsstools：EarthScope（原 UNAVCO/GAGE）维护的 Go 库和一组命令行工具。它读 RINEX 2/3/4、CRINEX、BINEX、SBF、NovAtel、u-blox UBX、Javad JPS、SBP，写 RINEX 2.11/3.05/4.02、Parquet、CRINEX；RTCM3 **只能用 `gnss-inspect` 解码成 JSON，`gnss-convert` 不支持 RTCM3 输入**。
> **别混淆：** [gnsstools](./gnsstools.md) 是 arthurdjn 写的 Python 教学库（RINEX/SP3 → pandas），跟本篇**同名但无关**。EarthScope 的 Python 数据接口是 [earthscope-sdk](./earthscope-sdk.md)，也不是本库。
> 实测时间：2026-09-26 04:26–04:38 EDT。环境是 Debian box（系统 `/etc/localtime` 为 `Etc/UTC`），CLI 日志里的 `time=…Z` 是 UTC。

> **质检复跑通过（2026-09-26 04:48–05:03 EDT，go1.26.8 从源码构建 `b3efce5`，`version` 报 `v0.111.1-0.20260924003836-b3efce58c3e7`）**：冷缓存构建 98 s、`gnss-convert` 164978130 B / `gnss-inspect` 10567569 B；WTZR CRX 4131445 B、sha256 `81b6c958`；`info` 2880 历元；3.05 26333817 B、`--doppler` 34909851 B、2.11 7462110 B、Parquet 11 MB 447933 行 / 449 个 phase=0 / loss_of_lock 2704；3.05 头与首历元、2.11 类型行、PHASE SHIFT 清零逐字一致；hatanaka(RNXCMP) 对照 127653 行 / 1198 行前导零差异；自压 CRX 自解字节相同、RNXCMP 解出 2934 行（卫星行 2880 vs 124719）；GMSD7 `gnss-inspect` 1143 帧（pyrtcm 按类型计数全同）；JPS 130 历元、NovAtel 46 历元且 644 个 D≈+2²⁰、ubx `unexpected EOF`、rtcm3 输入 `unsupported`、`validate` not yet implemented；空文件 / 5.00 / `--rinex-version 9.9`→4.02 / 15 MB 截断 1410 历元 / `--site-log` 错路径均一致。**已修**：§4.1 解压输出名与后续命令不一致（`WTZR_es.rnx`→`WTZR.rnx`）；`info` 补 `File`/`File size` 两行及不带 `--detailed --metadata` 时缺接收机/天线/坐标；Parquet `satellite` 是 uint16 PRN（单列仅 43 值）。未复跑：convbin 逐值对照、georinex 读回、4.02 输入、RINEX 当 SBF/BINEX 读、gnss-inspect 坏 CRC/截断、`.crx.gz` 截断等其余错误用例。

## 1. 用途边界

| 能（已实测） | 不能 / 未测 |
| --- | --- |
| RINEX 3.04 → RINEX 3.05 / 4.02 / 2.11，Parquet；读 `.crx.gz` / `.rnx.gz` | `validate`：RINEX 报 `not yet implemented`，exit 1 |
| CRINEX 压缩和解压（`gnss-convert crinex`） | RTCM3 → RINEX：`convert` 报 `unsupported input format: rtcm3` |
| Javad JPS、NovAtel RANGECMP → RINEX（RTKLIB 真实样本） | SBF / BINEX 的整日真实文件：没有找到免账号样本，**未测** |
| `gnss-inspect rtcm3` 解码 MSM7、1004/1012 等消息，输出 JSON | `ntrip-client`、`gnss-stream`、`gnss-process`（SPP/PPP）：**未测**（未构建） |
| `info` 看头信息和历元数 | `download`（CDDIS 要 Earthdata 账号，GAGE 要 `es login`）：**未测** |
| — | 串口、TCP 实时流：**未在真接收机上测试** |

## 2. 版本事实（2026-09-26 核实）

| 项 | 值 |
| --- | --- |
| 仓库 | <https://gitlab.com/earthscope/gnsstools>，默认分支 `main` `b3efce5`（2026-09-23 20:38 EDT，提交信息 `changelog: release v0.111.0`） |
| 最新 tag | 根模块 `v0.111.0` → `30b776a`（2026-09-23 20:36 EDT）；另有 `cmd/v0.111.0` → `e6329bc`、`geodata/v0.111.0` → `b0821d0`，三个 tag 各管一个 Go 模块 |
| 许可 / 星 | Apache-2.0；GitLab ★6、fork 4（API `star_count`）；最近活动 2026-09-25 18:04 EDT |
| 模块路径 | 根模块 `gitlab.com/earthscope/gnsstools`（**无 CGo**）；`…/cmd`（CLI）；`…/geodata`（TileDB/Arrow/Iceberg） |
| Go 要求 | 三个 `go.mod` 都写 `go 1.26.0`。box 系统自带 go1.24.4 **不够**，本篇用官方 go1.26.8 |
| CLI | `cmd/` 下有 `gnss-convert`、`gnss-inspect`、`gnss-process`、`gnss-stream`、`gnss-catalog`、`ntrip-client`、`obs-table-rebuild`、`iceberg-table-props` |
| codecs | antex binex bottle fcn ionex javad met novatel orbex pos rinex rtcm sbf sbp sinex sitelog sp3 ublox vaisala |

## 3. 安装

```bash
# 用自己的缓存目录，避免继承别人的 GOPATH/TMPDIR
export GOPATH=$PWD/gopath GOCACHE=$PWD/gocache GOMODCACHE=$PWD/gopath/pkg/mod GOTOOLCHAIN=local
curl -sSL https://go.dev/dl/go1.26.8.linux-amd64.tar.gz | tar xz && export PATH=$PWD/go/bin:$PATH
# 方式 A：go install（cmd 模块的 tag 是 cmd/v0.111.0，但版本写 @v0.111.0 就能解析到）
GOBIN=$PWD/bin go install gitlab.com/earthscope/gnsstools/cmd/gnss-inspect@v0.111.0
# 方式 B：从源码构建
git clone https://gitlab.com/earthscope/gnsstools.git && cd gnsstools/cmd
go build -o ../../bin/gnss-convert ./gnss-convert && go build -o ../../bin/gnss-inspect ./gnss-inspect
```

实测数据：冷缓存下两个 CLI 一起构建用了 **1 min 40 s**（含下载依赖），build 缓存热了以后 `go install` 用 5 s。**`gnss-convert` 二进制 165 MB**（静态链入 AWS S3、Iceberg、Parquet、NATS），`gnss-inspect` 10.6 MB。共享盘空间紧张时先确认余量。只用库的话 `go get gitlab.com/earthscope/gnsstools@v0.111.0`，不会拉 geodata 那一套重依赖。

## 4. 命令与真实输出

`gnss-convert --help`（原文摘录）：

```
Available Commands:
  availability Compute availability metrics from any supported input format
  convert      Convert GNSS data between different formats
  crinex       Compress or decompress RINEX with Hatanaka (CRINEX)
  info         Show information about GNSS data files
  products     Convert GNSS product files to parquet
  qc           Compute per-satellite geometry and signal quality metrics
  validate     Validate GNSS data integrity
  version      Show version information
```

`convert --help` 里的格式清单（原文）：`rtcm3: RTCM3 files (.rtcm) [PLANNED]`、`sp3 … [PLANNED]`；输出 `rinex … [IMPLEMENTED]`、`rtcm3 … [PLANNED]`、`parquet … [IMPLEMENTED]`。实现层还支持 `jps`、`tps`（Javad/Topcon）、`parquet` 输入，这几种不在清单里，但出错提示会列出：`(supported: rinex, binex, jps, tps, nva, nvb, sbf, sbp, ubx, parquet)`。`--input`/`--output` 必须写成 `格式:路径`。

`gnss-inspect --help` 的子命令：`binex bottle fcn novatel-ascii novatel-binary orbex rnx rtcm3 sbf sitelog sp3 ublox ublox-serial`。每个子命令都只有 `--file`，输出是**多个 JSON 对象直接串接**，不是 JSON 数组，也不是 NDJSON。

### 4.1 路径 A：BKG WTZR 2026-258（RINEX 3.04 MO，30 s）

数据来自 `https://igs.bkg.bund.de/root_ftp/IGS/obs/2026/258/WTZR00DEU_R_20262580000_01D_30S_MO.crx.gz`（4131445 B，sha256 `81b6c958…`，免账号）。

```bash
gnss-convert crinex decompress --input WTZR00DEU_R_20262580000_01D_30S_MO.crx.gz --output WTZR.rnx      # 1.06–1.50 s，exit 0，30169464 B
gnss-convert info --input rinex:WTZR.rnx --detailed --metadata                                            # 0.41 s
```
```
Format:     RINEX 3.04 / Observation / Mixed
File:       WTZR.rnx
File size:  28.8 MB
Station:    WTZR
Receiver:   1831551             LEICA GR50          4.50/7.710
Antenna:    10020031            LEIAR25.R3      LEIT
Position:   4075580.8863   931853.5784  4801567.9707
Time range: 2026-09-15T00:00:00Z — 2026-09-15T23:59:30Z
Epochs:     2880
```
`--statistics` 没有多输出任何内容，默认输出里也没有卫星数和观测值统计。不加 `--detailed --metadata` 时只有 Format/File/File size/Station/Time range/Epochs 六行，**没有 Receiver/Antenna/Position**。

```bash
gnss-convert convert --input rinex:WTZR.rnx --output rinex:WTZR_3.05.rnx --rinex-version 3.05            # 0.54 s，26333817 B
gnss-convert convert --input rinex:WTZR.rnx --output rinex:WTZR_d.rnx --rinex-version 3.05 --doppler      # 34909851 B
gnss-convert convert --input rinex:WTZR.rnx --output rinex:WTZR_4.02.rnx --rinex-version 4.02            # 0.56 s
gnss-convert convert --input rinex:WTZR.rnx --output rinex:WTZR_2.11.rnx --rinex-version 2.11            # 0.49 s，7462110 B
gnss-convert convert --input rinex:WTZR.rnx --output parquet:pq/                                         # 1.61 s，11 MB
```
3.05 输出的头和首历元（节选，行尾空格已去掉）：

```
     3.05           OBSERVATION DATA    M                   RINEX VERSION / TYPE
gnss-convert        gnss-convert        20260926 083100 UTC PGM / RUN BY / DATE
GNSS                                                        MARKER NAME
00000000            UNKNOWN             0.0.0               REC # / TYPE / VERS
        0.0000        0.0000        0.0000                  APPROX POSITION XYZ
G   12 L1C C1C S1C L2S C2S S2S L2W C2W S2W L5Q C5Q S5Q      SYS / # / OBS TYPES
G L2S  0.00000                                              SYS / PHASE SHIFT
> 2026 09 15 00 00  0.0000000  0 43
G05 127513684.211 7  24265041.597 7        47.500    99361311.583 7  …
```

对照原文件的首行：`G05  24265041.597   127513684.21107     -2784.078          47.500 …`。可以看到输出里观测顺序改成了 L-C-S(-D)，LLI 的 `0` 改成空格，C 观测补上了 SSI `7`。

2.11 输出的头只有这一行观测类型：`8    L1    L2    C1    P2    P1    S1    S2    C2      # / TYPES OF OBSERV`。

Parquet 按 Hive 分区写到 `pq/station_id=WTZR/year=2026/month=09/day=15/session_id=WTZR/data_*.parquet`，每个（历元, 卫星, 信号）一行，共 **447933 行**，覆盖 2880 历元、123 颗卫星（按 `constellation`+`satellite` 计；`satellite` 列是 uint16 PRN 号，单看它只有 43 个不同值，必须和 `constellation` 一起当键）。列有 `epoch`(ms, UTC) `constellation` `satellite` `signal` `code` `phase` `doppler` `snr` `loss_of_lock` `half_cycle_ambiguity` `lock_time` `fcn` 等。

### 4.2 路径 B：RTKLIB 仓库里的真实原始数据

样本来自 tomojitakasu/RTKLIB `rtklib_2.4.3` 分支 `180043e`（2020-12-29）的 `test/data/rcvraw/`：`GMSD7_20121014.rtcm3`、`testglo.rtcm3`、`javad_20110115.jps`、`oemv_200911218.gps`、`ubx_20080526.ubx`。

```bash
gnss-inspect rtcm3 --file GMSD7_20121014.rtcm3 > gmsd.json      # 0.07 s，2.4 MB，exit 0
gnss-convert convert --input jps:javad_20110115.jps --output rinex:jps_es.obs --rinex-version 3.05 --doppler --reference-date 2011-01-15   # 0.25 s
gnss-convert convert --input nvb:oemv_200911218.gps --output rinex:nov_es.obs --rinex-version 3.05 --doppler                             # 0.24 s，46 历元
gnss-convert convert --input ubx:ubx_20080526.ubx --output rinex:ubx_es.obs    # exit 1: conversion failed: unexpected EOF
```
GMSD7 的 JSON 首个对象：`"MessageNumber": 1077, "ReferenceStationId": 611, "Epoch": 604784000, … "Ranges": [135, 900, …]`，字段都是原始整数（DF 值），**不换算成米**。ubx 样本是 2008 年的 RXM-RAW，不是 RAWX，gnss-convert 不认，报错内容看不出原因。

## 5. 交叉检查（独立工具）

| 对象 | 独立工具 | 结果 |
| --- | --- | --- |
| CRX 解压 | RNXCMP crx2rnx 4.1.0（PyPI `hatanaka` 2.8.1 自带） | 行数都是 127653；1198 行文本不同，**全部是前导零写法**（`.880` 和 `0.880`、`-.xxx` 和 `-0.xxx`），数值、LLI、SSI 0 处不一致 |
| CRX 压缩 | RNXCMP crx2rnx 4.1.0；Rust `crx2rnx` 2.7.0 | gnss-convert 自己压、自己解，字节完全相同；**RNXCMP 解它压出来的 CRX 时 exit 0 但输出错乱**（只剩 2934 行，卫星行 2880 条，原文件是 124719 条）；Rust crx2rnx 能解出 124719 条卫星行。原因是空白 flag 没有写 `&` |
| RINEX 3.04→3.05 `--doppler` | 自写列宽解析 + georinex 1.16.2 | 2880/2880 历元，123/123 颗卫星，1791283/1791283 个值，max\|Δ\|=**0**，LLI 0 处不同；georinex 读前 1 h：120 历元 × 55 颗卫星 × 64 个变量，76803 个值 max\|Δ\|=0，NaN 分布一致 |
| 默认 3.05 / 4.02（不加 `--doppler`） | 同上 | 值一样，但 **D 观测全部丢失（447933 个）**；原本没有 SSI 的 C 观测被补上了 SSI（447933 个）。georinex 不认 4.02（`unknown RINEX … 4.02`） |
| 3.04→2.11 | 自写解析，按数值反查信号来源 | 只剩 G、R 两个系统（54/123 颗卫星），8 种观测 `L1 L2 C1 P2 P1 S1 S2 C2`，P1 列全空；G L2 大部分取 L2W（30845），有 **225 个取的是 L2S**；R L2 取 L2C（20595）和 L2P（62）混用；E/C/S/I 全部丢掉 |
| RTCM3 GMSD7（1143 帧） | pyrtcm 1.2.0 | 两边帧数都是 1143，按类型计数全同：1007/1008/1033 各 28，1019 15，1020 16，1077/1087/1117/1127 各 257；MSM 19558 个 cell 的精细伪距和相位 max\|Δ\|=**0** |
| RTCM3 testglo（429 帧） | pyrtcm 1.2.0 | 计数全同；1004 的 2046 条卫星记录 L1 伪距、相位差 0 处不一致 |
| JPS → RINEX | RTKLIB convbin 2.4.3 b34 | 130/130 历元；共有 31316 个值，C、S 全同；D 只差最后一位 ±0.001 Hz；**GL1W、RL1P 差 +0.25 周，GL2X、RL2C 差 −0.25 周**（两边头部 PHASE SHIFT 都写 0，1/4 周对齐的约定不同）；convbin 在首历元置 LLI=1（65 处）；gnss-convert 多出一颗 E01，只有 D1X、S1X |
| NovAtel RANGECMP → RINEX | RTKLIB convbin 2.4.3 b34 | 46/46 历元、16/16 颗卫星，C、S 全同；**负多普勒错成 +2²⁰ Hz**（−1140.227 → 1047435.773，G/R 的 D 共 644 个值）；L 差约 2²³ 周的整数倍（例如 100663296 = 12×2²³；R L2P 另外还差 −0.25 周），说明没有按伪距解算 ADR 翻转 |

NovAtel 这个问题查了源码：`codecs/novatel/novatel_binary/message_140.go` 里 `DopplerFreq` 按无符号 28 位读（`extractBitsUint64(n1, 0, 27)`），`Phase` 也用 `uint64(r.Le32())` 读，两处都没有做符号扩展。

JPS 路径的系统和观测类型（gnss-convert 与 convbin 各自的头）：

```
gnss-convert: G 16 L1C C1C S1C D1C L1W … L2X C2X S2X D2X | R 16 | S 4 | E 4 L1X C1X S1X D1X | J 20
convbin:      G 15 C1C L1C D1C S1C C1W L1W S1W C2W …      | R 15 | J 19 | S 4（无 E）
```

复现交叉检查的做法：用 Python 按 RINEX 3 列宽（3+16k）切出 (历元, 卫星, 类型) → (值, LLI, SSI)，历元键按数值解析，因为 convbin 写 `00.0000000`，gnss-convert 写 ` 0.0000000`。两个文件取键的交集逐值做差。2.11 文件则对每个 (历元, 卫星) 在原 3.04 文件里按数值反查，看它来自哪个信号。

## 6. 错误用例

输入都是**合成**的：从真实文件截断或改坏，只有 `wrongfmt` 是把真实 RTCM 文件改了扩展名。

| 用例 | 结果 |
| --- | --- |
| 空 `.rnx` | exit 1，`failed to create RINEX scanner: no header` |
| RINEX 在 15 MB 处截断（切在行中间） | **exit 0 不报错**，输出 1410 历元；最后一个历元仍写满 44 颗卫星，截断处的 C56 行只剩一部分值 |
| 观测值改成 `ABCDEFGHIJ` | exit 1，`strconv.ParseFloat: parsing "ABCDEFGHIJ97"` |
| 历元改成 `2026 13 45 99` | **exit 0 不报错**，被归一化成 `2027 02 18 03:00`，头里 TIME OF FIRST OBS 变成 2027 年 |
| 版本号改成 5.00 | exit 1，`version not supported: 5.00` |
| RINEX 4.02 输入 / 2.11 截断输入 | exit 0 / exit 0（后者是 1165 历元，同样不报错） |
| `.crx.gz`、`.rnx.gz` | exit 0，都是 2880 历元 |
| `.crx.gz` 截断 | exit 1，`unexpected EOF`，**但已写出 678 历元的半截文件** |
| RTCM 文件当 RINEX 读 | exit 1，`END OF HEADER not found` |
| RINEX 文件当 SBF / BINEX 读；空文件当 NVB、JPS 读 | **exit 0，输出 0 字节**；当 SBF 读时空转了 17 s |
| `gnss-inspect rtcm3`：空文件 / RINEX 文本 / 截断到 100 kB / 改坏首帧 CRC | 全部 exit 0：前两种不输出，截断的输出 437 帧，坏 CRC 那帧**被丢掉且没有提示**（剩 1142 帧） |
| `--rinex-version 3.04` 或 `9.9` | **exit 0，输出 4.02 且不提示** |
| `--site-log /nonexist` | exit 1，`failed to open site log` |
| `validate --input rinex:…` | exit 1，`RINEX validation not yet implemented` |

全部用例 **0 次 panic**。

## 7. I/O 要点

- 输入：`rinex:` 能自动识别 `.gz`、CRINEX。二进制格式要写对前缀（`binex`/`sbf`/`nvb`/`nva`/`ubx`/`jps`/`tps`/`sbp`）。格式写错不会报错，只会得到空文件。
- RINEX 输出：只写 2.11、3.05、4.02。`PGM / RUN BY` 固定为 `gnss-convert`、`EarthScope`。**Doppler 要加 `--doppler` 才输出**。
- 头部元数据：优先级是 flags > `--station-config` YAML > `--site-log`（按首历元选设备）> 内置默认。**RINEX→RINEX 转换也不会继承输入文件的头**。
- Parquet：缺失的相位存成 **0**（不是 null，WTZR 有 449 个）；`loss_of_lock` 只对应 LLI bit0（2704 个）。
- 日志：INFO 写到 stderr，带 UTC 时间戳；用 `GNSSTOOLS_LOG_LEVEL=warn` 可以压掉（gnss-inspect）。

## 8. 坑

1. **RINEX→RINEX 会丢头信息**：WTZR 转出来 MARKER NAME 变成 `GNSS`，接收机和天线变成 `UNKNOWN`，APPROX POSITION 和天线偏移变成 0；INTERVAL、LEAP SECONDS、SIGNAL STRENGTH UNIT、COMMENT 都没了。要用 `--marker/--receiver/--antenna-type/--position` 或 `--site-log` 补回来。
2. **PHASE SHIFT 被清零、数据却没改**：原文件 `G L2S -0.25000`、`E L1C 0.50000` 等，输出里都变成 `0.00000`，GLONASS COD/PHS/BIS 也从 −71.940 变成 0.000。按头信息做 1/4 周改正的下游程序会出错。
3. 默认不输出 D。3.05 输出比原文件小 13%，就是因为少了 D。
4. 2.11 输出只保留 GPS 和 GLONASS，同一列里会混用不同信号（例如 G L2 有 225 个取的是 L2S）。
5. `--rinex-version` 写了不支持的值，会不提示地退回 4.02。
6. 自己压出来的 CRX 不能交给 RNXCMP 解，会得到**不报错的错误输出**。要交换文件就用 RNXCMP `rnx2crx` 压。
7. NovAtel RANGECMP 的负多普勒会被写错（+2²⁰ Hz），相位也没有做翻转修正。v0.111.0 下 NovAtel 数据先用 convbin 或 [novatel-edie](./novatel-edie.md)。
8. JPS 转出的相位跟 convbin 差 ±1/4 周，两个文件不能混着用。
9. 输入截断或历元非法时 exit 0 且不报错。在流水线里要自己核对历元数和时间范围。
10. RTCM3 只能看 JSON，没有 RTCM→RINEX 转换；而且坏 CRC 的帧会被悄悄丢掉。
11. Go ≥1.26 是硬门槛；`GOTOOLCHAIN=local` 加旧版 Go 会直接编译失败。

## 9. 接到哪步 / 未测清单

- **上游**：BKG/IGS 公开 CRX（本篇），或 EarthScope GAGE 归档（要 `es login`，见 [earthscope-sdk](./earthscope-sdk.md)，未测）。
- **下游**：Parquet 可以直接进 DuckDB/pandas；RINEX 3.05 加 `--doppler` 的输出可以交给 [georinex](./georinex.md)、RTKLIB，但要先补头信息（坑 1、2）。
- **未测**：`qc`（需要 NAV）、`availability`、`products`、`download`；`gnss-process` SPP/TDCP/PPP；`gnss-stream`（NATS/Iceberg）；`ntrip-client` 和库里的 `ntrip`（没有连任何需要账号的 caster）；BINEX/SBF/SBP/TPS/NovAtel ASCII 的整日真实文件；RINEX NAV/MET 的读写；Windows/macOS。
- **未在真接收机上测试**：`gnss-inspect ublox-serial`、`binex --host` TCP 流。

## 10. 选型

| 需求 | 选 |
| --- | --- |
| 在 Go 服务里嵌入 RINEX/BINEX/SBF 编解码，并写 Parquet/Iceberg | **本库**（根模块无 CGo） |
| 原始数据 → RINEX 的通用转换，格式覆盖最广 | [rtklib](./rtklib.md) `convbin`（NovAtel、JPS 结果更可靠） |
| RINEX 检查、拼接、版本转换，头信息要保真 | [gfzrnx](./gfzrnx.md)（登记受限）/ [teqc](./teqc.md)（旧） |
| Rust 生态的 RINEX 读写 | [rinex](./rinex.md) / [rinex-cli](./rinex-cli.md) |
| 只在 Go 里解析 RTCM3 | [go-gnss-rtcm](./go-gnss-rtcm.md)（更轻）；Python 用 [pyrtcm](./pyrtcm.md) |
| BINEX 专用 | [binex](./binex.md)（Rust） |
| CRINEX 互换 | [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md) / [crx2rnx](./crx2rnx.md) |
| 用 Python 从 EarthScope 拉数据（带账号） | [earthscope-sdk](./earthscope-sdk.md) |
| Python 教学：RINEX/SP3 → pandas | [gnsstools](./gnsstools.md)（**同名不同项目**） |
