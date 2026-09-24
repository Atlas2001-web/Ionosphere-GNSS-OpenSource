# CLASLIB · QZSS CLAS 厘米级增强（Compact SSR）操作手册

目录：[`PROJECTS.json` → `CLASLIB`](../../PROJECTS.json) · 上游 <https://github.com/QZSS-Strategy-Office/claslib> · 官方门户 <https://qzss.go.jp/en/technical/dod/clas/clas_test-library.html> · tip **`1e3a75d`** / tag **`084`**（README 记 **0.8.4**，2026-09-10）· 源自 RTKLIB 2.4.2p13 + GSILIB · 许可 **BSD-2-Clause + 附加条款**（≤0.6.0 明确；其后见仓内 LICENSE）· 本机验证：Linux `ssr2osr`（无 LAPACK）· `-dump` → Compact SSR 分型 CSV（header **3601** 行）· `make test1` → **3580** `$GPGGA` · ≈36.1036°N 140.0863°E · 2026-09-24 04:54 EDT

> 岗位：日本内阁府 QZSS **CLAS**（Centimeter-Level Augmentation Service）参考实现——解码 **Compact SSR（RTCM MT4073）**，做 **SSR→OSR / SSR→虚拟观测**，以及事后 **PPP-RTK / VRS-RTK**（`rnx2rtkp`）。冲突时：**仓内 README / `doc/` 手册 / `./ssr2osr -?` > 本文**。Python 试验 → [cssrlib](./cssrlib.md)；QZSS **MADOCA-PPP**（另一服务）→ [madocalib](./madocalib.md)；通用 CLI → [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 读 RINEX OBS/NAV + **QZSS L6** 归档（`.l6`），解码 Compact SSR 子类型（含 SubType12 / 双通道，视版本）
- **`ssr2osr`**：Compact SSR → 观测空间改正（OSR）；可 `-dump` 只解析分型
- **`ssr2obs`**：Compact SSR → 虚拟观测（RINEX3 / RTCM3 MSM），供 VRS-RTK
- **`rnx2rtkp`**（`-P`/`-PS` 发行）：事后 PPP-RTK / VRS-RTK（NMEA-GGA）
- 仓内 `data/` 样例 OBS/NAV/L6 + 网格 `clas_grid.def`

**不做：**

- **不是** 运营级完好性保证——官方免责：不保证有效性/可靠性
- **不是** QZSS **MADOCA-PPP** → [madocalib](./madocalib.md)（服务、ICD、L6 产品均不同）
- **不是** 通用未改 RTKLIB → [rtklib](./rtklib.md)；勿把两套 `rnx2rtkp` 混进同一 `PATH`
- **不是** Galileo HAS 页解码 → [haslib](./haslib.md)；Python CLAS/HAS 教学 → [cssrlib](./cssrlib.md)
- **不是** 校准 sTEC/GIM 产线 → [pytecgg](./pytecgg.md) / [ionex-gim](./ionex-gim.md)（此处电离层是 CLAS 网格改正）
- 预编译 `*.exe` 面向 **Windows 10 x64**；Linux 须自编译（上游推荐 MinGW/CYGWIN，本机 gcc 已通）

一句话：CLASLIB = **QZSS CLAS 官方测试库**（Compact SSR 解码 + OSR/VRS/PPP-RTK 参考链）。

| 术语 | 含义 |
| --- | --- |
| CLAS / Compact SSR | QZSS 厘米级增强；RTCM MT4073 紧凑状态空间改正 |
| L6 / `.l6` | QZSS L6 消息归档；IS-QZSS-L6 定义 |
| SSR2OSR / OSR | 状态空间 → 观测空间改正；本页主验证入口 |
| SSR2OBS / VRS | 生成虚拟参考站观测，供 RTK 模式 |
| SubType12 / 双通道 | IS-QZSS-L6-002+ / -007 起的扩展；`test1_*ST12` / `*_2CH` |
| `clas_grid.def` | CLAS 网格定义；`file-cssrgridfile` 必填 |

## 2. 安装（Linux 自编译 `ssr2osr`）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/QZSS-Strategy-Office/claslib.git
cd claslib && git rev-parse --short HEAD   # 本机 1e3a75d / tag 084

# 可选：sudo apt-get install -y liblapack-dev libblas-dev
# 无 LAPACK 时去掉 -DLAPACK / -llapack -lblas（见下）
cd util/ssr2osr
make clean
make -j"$(nproc)" \
  CFLAGS='-Wall -O3 -ansi -pedantic -I../../src -DTRACE -DENAGAL -DENAQZS -DNFREQ=3 -DENA_SSR2OSR' \
  LDLIBS='-lm'
./ssr2osr -? | head -5
# 期望：usage: ssr2osr [option]... file file [...]

# 同理：cd ../ssr2obs && make …；cd ../rnx2rtkp && make …（-PS 源码发行）
```

**关键：把 `sample.conf` 里的 Windows 反斜杠改成 Linux 正斜杠**（否则必报 `grid file error`）：

```bash
cp sample.conf sample.conf.bak
sed -i 's|\\.\\.|../..|g; s|\\|/|g' sample.conf
rg 'file-cssrgridfile' sample.conf
# 期望：file-cssrgridfile  =../../data/clas_grid.def
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `cannot find -llapack` | 默认 makefile 链 LAPACK | 用上文无 LAPACK 的 `CFLAGS`/`LDLIBS`，或装 `liblapack-dev` |
| 直接跑 `ssr2osr.exe` | Linux 不认 PE | 走 `util/*/makefile` 的 `make` |
| `error : no input file` | 无参启动 | 正常；`-?` 看帮助 |

## 3. 端到端 A：`-dump` 解析 L6（本机真跑）

数据：`data/2019349B.l6`（ST12 样例，~879 KB）。只解析、不产 OSR。

```bash
cd ~/iono_ops/claslib/util/ssr2osr
./ssr2osr -k sample.conf -dump ../../data/2019349B.l6
wc -l parse_cssr_header.csv parse_cssr_type1.csv
head -2 parse_cssr_header.csv
```

**本机结果（tip `1e3a75d`，2026-09-24 04:54 EDT）：**

```text
CSSR frame first recieve: tow=377538.7
start CSSR decoding: week=2437, tow=377538.7

parse_cssr_header.csv     3601
parse_cssr_type1.csv      1859
parse_cssr_type2.csv      2099
parse_cssr_type3.csv     12625
parse_cssr_type4.csv      4401
parse_cssr_type6.csv     42612
parse_cssr_type11.csv     9553
parse_cssr_type12_stec.csv  18212
parse_cssr_type12_grid.csv 320693
```

| 输出 | 含义 |
| --- | --- |
| `week` / `tow` | 首帧 GPS 周 / 周内秒 |
| `parse_cssr_header.csv` | L6 帧头（Preamble/PRN/消息类型等） |
| `type1`…`type12_*` | Compact SSR 各子类型展开；MT **4073** |
| type5/8/9 仅 1 行 | 该样例时段无对应子类型有效载荷（正常） |

## 4. 端到端 B：`test1` SSR→OSR + NMEA（本机真跑）

等价 `make test1`（OBS `0627239Q.obs` + NAV `sept_2019239.nav` + L6 `2019239Q.l6`，2019-08-27 16:00–16:59）：

```bash
cd ~/iono_ops/claslib/util/ssr2osr
./ssr2osr -ti 1 -ts 2019/08/27 16:00:00 -te 2019/08/27 16:59:59 -x 2 \
  -k sample.conf \
  ../../data/0627239Q.obs ../../data/sept_2019239.nav ../../data/2019239Q.l6 \
  -o 0627239Q.nmea
rg -c '^\$GPGGA' 0627239Q.nmea
rg '^\$GPGGA' 0627239Q.nmea | head -1
rg '^\$GPGGA' 0627239Q.nmea | tail -1
```

**本机结果：**

```text
3580 条 $GPGGA；质量位均为 1；nsat 峰值 17
首：160002.00  3606.2185695,N  14005.1804310,E  → ≈36.103643°N 140.086340°E  alt≈32.5 m
末：165941.00  3606.2182657,N  14005.1792138,E  → ≈36.103638°N 140.086320°E  alt≈32.5 m
旁路产物：0627239Q.nmea.osr（~8.6 MB）、.stat、.trace（-x 2）
```

| 旗标 | 作用 |
| --- | --- |
| `-k conf` | 读 `pos1-posmode=ssr2osr`、网格/天线/BLQ 等 |
| `-dump` | 只解析 Compact SSR → CSV；仍要可读的 `file-cssrgridfile` |
| `-ti` / `-ts` / `-te` | 采样间隔与时段 |
| `-l6w week` | L6 文件起始 GPS 周（跨周边界时） |
| `-o` | 输出；默认 NMEA-GGA 风格 |
| `-x level` | trace；`2` 时旁路 `.trace` 很大 |

`ssr2obs`：`cd ../ssr2obs && make && make test1r`（RINEX 虚拟观测）/ `make test1m`（MSM）。`rnx2rtkp`：`make test_L6` / `test_VRS` / `test_ST12`（见上游 README §3.3）。

## 5. 接到哪步

- CLAS Compact SSR / OSR 理解 → Python 对照 [cssrlib](./cssrlib.md)（`cssrlib-data`）
- 事后通用 RTK/PPP → [rtklib](./rtklib.md)；发表级 PPP-AR → [pride-pppar](./pride-pppar.md)
- 同属 QZSS 但 **MADOCA** 链路 → [madocalib](./madocalib.md)
- L6/CLAS 归档入口：官方 <https://sys.qzss.go.jp/dod/archives/clas.html>；概念 [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)
- 工作流 **D**（开放服务教学）：QC → [cssrlib](./cssrlib.md)/本文 → [madocalib](./madocalib.md)/[pride-pppar](./pride-pppar.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `grid file error: ..\..\data\clas_grid.def` | conf 里 Windows 路径 | `sed -i 's\|\\\\.\\\\.\|../..\|g; s\|\\\\\|/\|\|g' sample.conf` |
| 2 | `cannot find -llapack` | 默认链 LAPACK | 无库时用 §2 的 `LDLIBS='-lm'` 重编 |
| 3 | `-dump` 仍报 Grid file read error | dump 路径也读 `file-cssrgridfile` | 先修 conf 路径；网格文件须存在 |
| 4 | 跑 `bin/*.exe` / `ssr2osr.exe` | 预编译是 Windows PE | Linux：`cd util/ssr2osr && make` |
| 5 | 与系统 `rnx2rtkp` 结果对不上 | CLAS 分支改过定位核 | `which rnx2rtkp`；只用 `claslib/util/rnx2rtkp/` |
| 6 | 跨周 L6 时间错乱 | 周号未指定 | 加 `-l6w <GPS周>`（见 `make test_L6_week`） |
| 7 | 当 MADOCA 教程跑 CLAS 样例 | 两套 QZSS 服务/ICD 不同 | MADOCA → [madocalib](./madocalib.md) |
| 8 | 期望 cm 级固定解却只有 NMEA q=1 | `ssr2osr` 主责 OSR；PPP-RTK 在 `rnx2rtkp` | 编/跑 `util/rnx2rtkp` 的 `test_L6` |
| 9 | `.trace` 数 GB | `-x` 过高 | 日常 `-x 0`；调试再 `-x 2` |
| 10 | 业务区在日本境外无改正 | CLAS 服务区/网格有限 | 换服务区数据或改用 [cssrlib](./cssrlib.md)/IGS SSR |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| QZSS CLAS 官方 Compact SSR→OSR/VRS/PPP-RTK | **本文 CLASLIB** |
| Python CLAS/HAS/BDS 教学 PPP | [cssrlib](./cssrlib.md) |
| QZSS MADOCA-PPP 官方参考 | [madocalib](./madocalib.md) |
| 通用事后 RTK/PPP CLI | [rtklib](./rtklib.md) |
| Galileo HAS 页→SSR | [haslib](./haslib.md) |

## 8. 相关

[cssrlib](./cssrlib.md) · [madocalib](./madocalib.md) · [rtklib](./rtklib.md) · [haslib](./haslib.md) · [pride-pppar](./pride-pppar.md) · [data-access](../data-access.md) · [README](./README.md)

- IS-QZSS-L6：<https://qzss.go.jp/en/technical/ps-is-qzss/ps-is-qzss.html>
- CLAS 归档：<https://sys.qzss.go.jp/dod/archives/clas.html>
