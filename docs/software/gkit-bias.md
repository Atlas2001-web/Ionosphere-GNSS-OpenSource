# Gkit-Bias · 全频点 DCB/UPD/IFCB→OSB 操作手册

目录：[`PROJECTS.json` → `Gkit-Bias`](../../PROJECTS.json) · 上游 <https://github.com/LiZhengXiao99/Gkit-Bias> · tip **`b8b7dd8`**（tag 消息 **V1.0**；无语义化 git tag）· **GPL-3.0** · ★**8** · C++17/CMake/Eigen3 · 本机验证（2026-09-24 06:51–06:54 EDT）：`g++ 14.2.0` + `cmake 3.31.6` + `libeigen3-dev 3.4.0-5` → `build/bin/gkit_bias` **1357040** B + `build/libgkit_bias_core.a` **2259004** B；`-V`/`-h` → **`Gkit-Bias v1.0.0 (commit b8b7dd8), Zhengxiao Li (李郑骁)`** / **`GNSS bias product estimation: UPD / DCB / IFCB / OSB`**；无参 / 缺文件 exit **2**；仓内四份 `config/*aether*.conf` 缺数据 exit **1**（DCB/IFCB：`input folder does not exist: config/./data/2025091`；UPD：`aetheramb reader produced no valid observations…`）；空输入目录 DCB/IFCB：`[Read] … RINEX=0 SP3=0` → `no RINEX observations read`；空 `.amb` 目录：`no AETHER .amb files found`；`mode=3`：`CLK mode is not supported yet`。**仓内无样例观测/无预置 DCB·IFCB·OSB 产品**——**未臆造**任何 Bias-SINEX / `.DCB` / `.IFCB` / `.UPD` 数值行。

> 岗位：**全频点卫星端偏差估计**（DCB / UPD / IFCB）并可选折成 **OSB**，服务 AETHER/Pride 等 PPP-AR。冲突时：**本机 `gkit_bias -h|-V` / `config/*.conf` / 上游 README > 本文**。  
> 对照武大族：[great-upd](./great-upd.md)（UPD）· [great-ifcb](./great-ifcb.md)（IFCB）· [clkcomb](./clkcomb.md)（多 AC 钟/偏差合成）· [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)（消费端 PPP）· 产品门户 [data-access](../data-access.md)「SP3 / CLK / bias」。**≠** [cube](./cube.md)（APM 钟差/PPP-AR）。

## 1. 用途与边界

**做：**

- 统一 CLI `gkit_bias CONFIG`：`mode=0` UPD、`1` DCB、`2` IFCB；估计后可内存直出 Bias-SINEX **OSB**（`osb_output` / `osb_dcb` / `osb_ifcb`）
- **DCB**：RINEX+SP3 → 球谐 VTEC 与码偏差联立；模板注 ≥60 站
- **IFCB**：三频 IF 差 → `epodif`（历元差分）或 `lsq`；模板默认 GPS L5
- **UPD**：读 **AETHER-AMB 2.0** 浮点 `.amb`（须已加 DCB/IFCB）→ WL/EWL/NL；可 `realtime=true` 滑窗
- 仓内 `script/*.py`（9）：`compare_dcb` / `check_osb_consistency` / `plot_*` / `analyze_*`（本机仅 `ast.parse` 语法 OK；无产品未实跑图）

**不做：**

- **不是** PPP/PPP-AR 引擎 → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)
- **不是** 多 AC 钟差合成 → [clkcomb](./clkcomb.md)；**不是** 武大 GREAT-UPD/IFCB 同二进制（算法谱系相近、输入/XML 完全不同）
- **`mode=3` CLK 未实现**（本机：`CLK mode is not supported yet`，exit **1**）
- **不** 附带 RINEX/SP3/`.amb`/atx 算例；AETHER 树、`sat_antex_file` 指向的邻仓路径需自备
- 本机**未**拉 CDDIS/CAS DCB、**未**跑通 OSB 落盘——**禁止**把下文缺输入 stderr 当成产品 stdout

一句话：**Gkit-Bias = 长安大学相关开源全频点偏差估计器（DCB/UPD/IFCB→OSB）**。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** Gkit-Bias | 统一 conf 驱动 DCB/UPD/IFCB→OSB | `gkit_bias config/*.conf` |
| [great-upd](./great-upd.md) | 武大 UPD（XML） | `GREAT-UPD -x …xml` |
| [great-ifcb](./great-ifcb.md) | 武大 IFCB | `GREAT-IFCB -x …` |
| [clkcomb](./clkcomb.md) | 多 AC 钟/偏差合成 | `clkcomb comb.ini` |
| CAS/IGS OSB 产品 | 分析中心偏差文件 | CDDIS/iGMAS；本工具自产 `GKT*` |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++`≥7（C++17）+ `cmake`≥3.16 + GNU `make` | 源码编译（本机采用） |
| Eigen3（`libeigen3-dev` 或 `-DEIGEN3_INCLUDE_DIR=`） | 线性代数；CMake 找不到即 **FATAL** |
| `python3`（可选） | `script/*.py` 质检/出图 |
| AETHER PPP + igs20.atx + 网数据（可选） | 模板写死的邻仓路径与 ≥60 站 RINEX |

### Linux 源码（本机已通）

```bash
sudo apt install -y build-essential cmake libeigen3-dev
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/LiZhengXiao99/Gkit-Bias.git
cd Gkit-Bias
git rev-parse --short HEAD          # 本机：b8b7dd8
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j"$(nproc)"    # → bin/gkit_bias、libgkit_bias_core.a
ls -la build/bin/gkit_bias          # 本机：1357040 B
./build/bin/gkit_bias -V
./build/bin/gkit_bias -h
```

**本机 `-V`：**

```text
Gkit-Bias v1.0.0 (commit b8b7dd8), Zhengxiao Li (李郑骁)
GNSS bias product estimation: UPD / DCB / IFCB / OSB
```

**本机 `-h`：**

```text
Gkit-Bias v1.0.0 (commit b8b7dd8), Zhengxiao Li (李郑骁)
GNSS bias product estimation: UPD / DCB / IFCB / OSB
Usage:
  gkit_bias CONFIG_FILE

Examples:
  gkit_bias config/gkit_bias_upd_ambconf
  gkit_bias config/gkit_bias_dcb.conf
  gkit_bias config/gkit_bias_ifcb.conf
  gkit_bias config/gkit_bias_clk.conf

Gkit-Bias reads all options from a configuration file.
See config/ for example configs matching the supported products.
```

> **坑：** `-h` 示例文件名（`gkit_bias_dcb.conf` 等）**仓内不存在**。实装四份：`config/gkit_bias_dcb_aether.conf`、`gkit_bias_ifcb_aether.conf`、`gkit_bias_aether_upd_batch.conf`、`gkit_bias_aether_upd_rt.conf`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| CMake `Eigen3 was not found` | 无头文件 | `apt install libeigen3-dev` 或 `-DEIGEN3_INCLUDE_DIR=/usr/include/eigen3` |
| 无参 exit **2** | `missing config file` | 必须给 conf 路径 |
| 缺文件 exit **2** | `failed to open config file: …` | 改路径 |
| `mode=3` exit **1** | CLK 未实现 | 只用 0/1/2 |

## 3. 端到端（本机真跑；仅缺输入/空输入冒烟）

```bash
BIN=~/iono_ops/Gkit-Bias/build/bin/gkit_bias
cd ~/iono_ops/Gkit-Bias
```

### 3.1 无参 / 缺 conf（exit 2）

```bash
$BIN            # → missing config file + Usage；exit 2
$BIN /tmp/no_such_gkit.conf
# → failed to open config file: /tmp/no_such_gkit.conf；exit 2
```

### 3.2 仓内模板、数据未就绪（exit 1）

```bash
$BIN config/gkit_bias_dcb_aether.conf
# → input folder does not exist: config/./data/2025091

$BIN config/gkit_bias_ifcb_aether.conf
# → input folder does not exist: config/./data/2025091

$BIN config/gkit_bias_aether_upd_batch.conf
# → aetheramb reader produced no valid observations (check min-epochs, systems, combos, sigma)
```

> **`input` 相对路径相对 conf 所在目录解析**（`src/common/config.cpp`：`resolve_path(value, config_dir)`），**不是** cwd。故报错前缀是 `config/./data/…`，不是 `./data/…`。

### 3.3 空输入目录（exit 1；仍无产品）

```bash
mkdir -p /tmp/gkit-smoke/data/2025091 /tmp/gkit-smoke/amb_empty
# 将 conf 内 input/output 改成绝对路径后：
$BIN /tmp/gkit-smoke/dcb2.conf
# → [Read] input=/tmp/gkit-smoke/data/2025091 RINEX=0 SP3=0 orbit=sp3
# → no RINEX observations read

$BIN /tmp/gkit-smoke/ifcb2.conf   # 同上 RINEX=0

$BIN /tmp/gkit-smoke/upd.conf
# → no AETHER .amb files found: /tmp/gkit-smoke/amb_empty
```

### 3.4 CLK 占位

```bash
printf 'mode = 3\ninput = /tmp/x\noutput = /tmp/y\n' > /tmp/gkit-smoke/clk.conf
$BIN /tmp/gkit-smoke/clk.conf
# → CLK mode is not supported yet；exit 1
```

### 3.5 有数据时（流程；本机未跑通产品）

1. **DCB**（`mode=1`）：≥60 站 RINEX + 多日 SP3 → `output/` 下 `GKT_*_G/E/C.DCB`；可选 `osb_output=*.BIA`
2. **IFCB**（`mode=2`）：同目录三频观测；`ifcb_method=epodif|lsq` → `GKT0MGXRAP_*_IFCB.IFCB`
3. **AETHER 浮点解**（外链）写 `.amb`
4. **UPD**（默认 `mode=0`）：`input` 指向 `.amb` 目录；`combos=WL12,WL23,…,NL`；`osb_dcb`/`osb_ifcb`/`osb_output` 折 OSB
5. 下游 PPP-AR：[pride-pppar](./pride-pppar.md) / AETHER；偏差对照 CAS/IGS → [data-access](../data-access.md)

## 4. I/O

| 方向 | 形态 | 说明 |
| --- | --- | --- |
| 入·DCB/IFCB | 目录 | RINEX 观测 + SP3（`orbit_type=sp3`）；相对路径锚 conf 目录 |
| 入·UPD | 目录 | AETHER-AMB **2.0** `.amb`；非 RINEX |
| 入·可选 | atx / 既有 DCB·IFCB / CAS BSX | `sat_antex_file`；`osb_dcb`/`osb_ifcb` 供 OSB 折叠 |
| 出·DCB | 文本 `.DCB` | 模板：`GKT_YYYYMMDD_{G,E,C}.DCB` |
| 出·IFCB | `.IFCB` | 模板：`GKT0MGXRAP_*_IFCB.IFCB` |
| 出·UPD | UPD 块 + 可选 `.BIA` | `osb_output` Bias-SINEX；`osb_nl_daily`/`osb_wl_daily` 建议 true |
| 出·日志 | stdout | `verbose=true` 时 `[Read] …`；失败英文短句 |

本机**无**落盘产品字节可读——上表仅为 conf/README 声明的命名约定。

## 5. 参数（conf 键；摘自模板 + `config.cpp`）

| 键 | 含义 | 本机模板/默认 |
| --- | --- | --- |
| `mode` | 0 UPD / 1 DCB / 2 IFCB / 3 CLK(未实现) | DCB=1，IFCB=2，UPD 省略→0 |
| `input` / `output` | 输入目录 / 输出目录 | 相对路径：`input` 相对 **conf 目录** |
| `systems` | 系统掩码 | DCB `GEC`；IFCB `G`；UPD `GEC` |
| `elmask` / `wlelmask` / `nlelmask` | 高度角 | 常 15 / 10 / 12 |
| `orbit_type` | `sp3`（DCB/IFCB） | 模板 `sp3` |
| `dcb_*_types` | 码组合编号串 | 见 conf 注释 ↔ `signal.cpp` |
| `dcb_iono_order` / `dcb_local_time_blocks` | 球谐阶 / 地方时块 | 4 / 12 |
| `ifcb_method` | `epodif` / `lsq` | 模板 `epodif` |
| `ifcb_sample` / `ifcb_min_arc_ep` / `ifcb_jump_threshold` | 采样与弧段 | 30 / 31 / 0.1 |
| `combos` | UPD 组合 | `WL12,WL23,WL24,WL25,NL` |
| `sample` / `session` | 采样与 NL 会话 | 30 / 3600 |
| `datum` / `robust` / `bds_mode` | 基准 / 抗差 / BDS | `all-sat` / `none` / `split` |
| `realtime` / `realtime_step` / `osb_hold` | 仿实时 UPD | rt 模板 true / 300 / 300 |
| `osb_output` / `osb_dcb` / `osb_ifcb` | OSB 直出 | 路径自备；无则仅差分产品 |
| `ac` | 产品机构码 | 模板 `GKT`/`GKI`（注意混用） |
| `verbose` | 读数摘要 | `true` |

完整键以 `src/common/config.cpp` 的 `apply_config_entry` 为准。

## 6. 接到哪步

```text
RINEX+SP3 ──► Gkit-Bias DCB/IFCB ──► AETHER 浮点 .amb
                                      │
                                      ▼
                               Gkit-Bias UPD (+ osb_*)
                                      │
                                      ▼
                         OSB/BIA ──► Pride/AETHER PPP-AR
                                      │
              对照 CAS/IGS OSB / GREAT-UPD·IFCB / clkcomb 多 AC
```

- 只要武大 XML 样例 UPD → [great-upd](./great-upd.md)（自带 `sample data`）
- 只要 IFCB、已有 GREAT 生态 → [great-ifcb](./great-ifcb.md)
- 多分析中心钟差合并 → [clkcomb](./clkcomb.md)
- 偏差产品下载 → [data-access](../data-access.md)

## 7. 坑（≥8）

1. **`-h` 示例 conf 文件名与仓内不一致**——用 `*aether*.conf` 四份，勿抄 Usage 字面量。  
2. **`input` 相对路径锚 conf 目录**——cwd 改了也仍拼成 `config/./data/…`；本机 DCB/IFCB 即此报错。  
3. **无官方 sample_data**——空目录只会 `RINEX=0` / `no AETHER .amb`；**不要**伪造 `.DCB/.BIA` 当“期望输出”。  
4. **UPD 只吃 AETHER-AMB 2.0**——给普通 RINEX 或空目录不会默默成功；错误文案与 DCB 不同。  
5. **`mode=3` CLK 未实现**——exit 1；勿当钟差估计器。  
6. **邻仓路径写死**——`sat_antex_file=../AETHER/tbl/igs20_*.atx`、UPD `input=../AETHER/data/...`；无 AETHER 树必改绝对路径。  
7. **OSB 折叠依赖前置产品**——`osb_dcb`/`osb_ifcb` 指向的文件不存在时，估 UPD 也可能中途失败；先 DCB/IFCB 再 UPD。  
8. **`osb_nl_daily=true` 几乎必开**——模板注释：历元 NL 噪声大，须折叠日均值。  
9. **`ac` 码混用**——DCB/IFCB 模板 `GKI`，UPD/OSB `GKT`；下游文件名/机构码别混。  
10. **IFCB 模板 `systems=G`**——只估 GPS L5 频间；开 E/C 须自改并自备三频。  
11. **Eigen 缺失直接 FATAL**——与 GREAT 族（自带 LibMat）不同，须系统 Eigen。  
12. **script 无产品可跑**——`compare_dcb.py`/`check_osb_consistency.py` 要已有 `.DCB`/`.OSB`；本机未跑数值对照。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 一条工具链 DCB+IFCB+UPD→OSB（AETHER 生态） | **Gkit-Bias** | 统一 conf；OSB 内存直出 |
| 只要 UPD，要仓内 GPS 样例可对拍 | [great-upd](./great-upd.md) | `sample data` + WL/EWL 字节可 `cmp` |
| 只要 IFCB，GREAT XML 流程 | [great-ifcb](./great-ifcb.md) | 与 GREAT-PVT 同族 |
| 多 AC 钟/偏差合成 | [clkcomb](./clkcomb.md) | 输入是各家 CLK/OSB，不是 RINEX |
| 下游 PPP-AR | [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md) | 消费 OSB/UPD，不估计 DCB 网解 |
| Win+MKL 钟差/PPP-AR 一体 | [cube](./cube.md) | 与 Gkit 输入输出均不同；Linux 难编 |

**底线：** 没有 RINEX/SP3/`.amb` 就只会得到上文这些 **exit 1/2** 英文句；把它们当产品、或编造 OSB 行，都会污染偏差链路。
