# GREAT-IFCB · 武大多星座频间钟差（IFCB）估计操作手册

目录：[`PROJECTS.json` → `GREAT-IFCB`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-IFCB> · tip **`e245681`**（无 git tag；`init v1.0`）· **GPL-3.0** · ★**15** · C++/CMake · 本机验证（2026-09-24 06:42–06:44 EDT）：`g++ 14.2.0` + `cmake 3.31.6` → `build/Bin/GREAT-IFCB` **54568** B + `Lib/liblib{Gnut,IFCB,Mat}.so`；`-h`/`-V 1` → **`GREAT-IFCB [1.0]`**（`$Rev: 2448 $`，源码编于 **Sep 24 2026 10:43:04**）；预编译 `bin/Linux/GREAT-IFCB` **44904** B → **`GREAT-IFCB [1.0]`** compiled **Jul 29 2022 13:31:21**；缺 XML → `xconfig: not file read … File was not found` exit **1**；`doc/IFCB_CONFIG.xml` 无 OBS/NAV/DCB → 仍 **`Normal End!`** exit **0**，仅出空壳 `ifcb_2021003_GCE` **38** B（`% IFCB generated using GREAT-IFCB`+尾标记）+ `ifcb.log` **2220** B（**非** XML 写的 `LOGRT.log`）；GitHub tip **无** `sample_data/IFCB_2021003` / `util/PreEdit`（README/PDF 宣称有）→ **未臆造** 历元级 IFCB 数值；WHU `igs.gnsswhu.cn` NLST **425**；批下载脚本本机**未拉**新产品

> 岗位：**多星座频间钟差（IFCB）估计**（GPS/GAL/BDS 三频）→ 服务精密钟差与三频 PPP。冲突时：**本机 `GREAT-IFCB -h` / `doc/IFCB_CONFIG.xml` / `doc/GREAT-IFCB_1.0.pdf` / 上游 README > 本文**。  
> 同链 UPD → [great-upd](./great-upd.md)；多 AC 钟差合成 → [clkcomb](./clkcomb.md)；产品门户 → [data-access](../data-access.md)「SP3 / CLK / bias」。下游 PPP → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)。**≠** [cube](./cube.md)（APM 钟差/PPP-AR）。

## 1. 用途与边界

**做：**

- 多 GNSS（**GPS / Galileo / BeiDou**）**频间钟差 IFCB** 估计（三频相位几何无关组合）
- XML 驱动 CLI：`GREAT-IFCB -x CONFIG.xml`；仓内预编译 Linux/Win/Mac + CMake 源码（LibIFCB + LibGnut + LibMat）
- 内置 PreEdit 风格周跳检查（XML `<preedit>`：MW/GF/gap/short）；批脚本 `util/PythonScripts/ifcb.py` + `download_{obs,nav,dcb}.py` + `draw_ifcb.py`
- 论文/手册：GPS Solutions **27:84**（2023）；用户手册 `doc/GREAT-IFCB_1.0.pdf`

**不做：**

- **不是** UPD/WL/NL 估计 → [great-upd](./great-upd.md)；**不是** 精密钟差滤波主引擎（GREAT-PCE 另仓，本目录暂无篇）
- **不是** PPP/PPP-AR 解算 → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)
- **不是** 多 AC 钟/偏差合成 → [clkcomb](./clkcomb.md)
- GitHub tip **不带** `sample_data/`；NOAA GPS Toolbox 索引列论文但**本机未找到**可下的 `GREAT-IFCB_<ver>.zip` 直链 → **禁止**拿空壳产物当真 IFCB
- 本机**未**用新日网自产 OBS/NAV/DCB（WHU FTP **425**；CDDIS 需 Earthdata）

一句话：**GREAT-IFCB = 武大 GREAT 开源多星座 IFCB 估计器**（与 GREAT-UPD 同产品链、不同偏差量）。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** GREAT-IFCB | IFCB 估计 CLI | `GREAT-IFCB -x …xml` → `ifcb_*` |
| [great-upd](./great-upd.md) | UPD WL/EWL/NL | `GREAT-UPD -x …` → `upd_*` |
| [clkcomb](./clkcomb.md) | 多 AC 钟/偏差合成 | `clkcomb comb.ini` |
| [cube](./cube.md) | APM 钟差/PPP-AR | Win+MKL；Linux 难编 |
| Gkit-Bias（长安） | DCB/UPD/IFCB→OSB | 另仓；本目录暂无篇 |
| 官方 IGS/CAS 钟差 | 分析中心产品 | CDDIS；本工具自产 `ifcb_*` |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++` + `cmake`≥3.0 + GNU `make` | 源码编译（本机采用） |
| 预编译 `bin/Linux/`（可选） | 仅 `GREAT-IFCB`+`liblib*.so`（**无**捆绑 libc；仍须 `LD_LIBRARY_PATH`） |
| `python3` + `matplotlib`/`requests`（可选） | 批跑 / 拉数 / 出图 |
| CDDIS Earthdata 或 WHU（可选） | `download_*.py`；见 [data-access](../data-access.md) |

### Linux 源码（本机已通；推荐）

```bash
sudo apt install -y build-essential cmake   # 本机已有 g++ 14.2.0 / cmake 3.31.6
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GREAT-WHU/GREAT-IFCB.git
cd GREAT-IFCB
git rev-parse --short HEAD   # 本机：e245681
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)              # → Bin/GREAT-IFCB、Lib/liblib*.so
ls -la Bin/GREAT-IFCB         # 本机：54568 B
export LD_LIBRARY_PATH="$PWD/Lib:${LD_LIBRARY_PATH:-}"
./Bin/GREAT-IFCB -h
```

**本机 `-h`：**

```text
GREAT-IFCB [1.0] compiled: Sep 24 2026 10:43:04 ($Rev: 2448 $)

Usage: 

    -h|--help              .. this help                          
    -V int                 .. version                            
    -v int                 .. verbosity level                    
    -x file                .. configuration input file           
    --                     .. configuration from stdinp          
    -l file                .. log output file                    
    -X                     .. output default configuration in XML
```

### 预编译（本机）

```bash
chmod +x bin/Linux/GREAT-IFCB          # git 检出常无 +x → Permission denied
mkdir -p /tmp/great-ifcb-libs
cp -a bin/Linux/liblib*.so /tmp/great-ifcb-libs/
export LD_LIBRARY_PATH=/tmp/great-ifcb-libs
./bin/Linux/GREAT-IFCB -h
# → GREAT-IFCB [1.0] compiled: Jul 29 2022 13:31:21 ($Rev: 2448 $)
```

与 [great-upd](./great-upd.md) 对照：本仓 `bin/Linux/` **未**捆绑 `libc.so.6`，但仍须把 `liblib*.so` 放进 `LD_LIBRARY_PATH`（或用 `build/Lib`）。**勿**假设整目录塞进 `LD_LIBRARY_PATH` 在别的 GREAT 工具上安全。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Permission denied` | 预编译无执行位 | `chmod +x bin/Linux/GREAT-IFCB` |
| `error while loading shared libraries: liblibIFCB.so` | 未设 `LD_LIBRARY_PATH` | 指向 `build/Lib` 或仅含 `liblib*.so` 的目录 |
| `-x` 缺文件 exit **1** | `xconfig: not file read … File was not found` | 改路径 |
| 无真观测仍 `Normal End!` | 缺文件只打 Error，仍写空壳产物 | 见 §3.2；**查产物是否含 `EPOCH-TIME`** |

## 3. 端到端（本机真跑）

### 3.1 帮助 / 缺配置

```bash
export LD_LIBRARY_PATH=~/iono_ops/GREAT-IFCB/build/Lib
BIN=~/iono_ops/GREAT-IFCB/build/Bin/GREAT-IFCB
$BIN -h                 # GREAT-IFCB [1.0] …  ；exit 0
$BIN -V 1               # 同上版本行  ；exit 0
$BIN -x /tmp/no_such_ifcb.xml
# → xconfig: not file read /tmp/no_such_ifcb.xml File was not found  ；exit 1
$BIN -X | head           # 倾倒默认 XML 骨架（含 gen/inputs/gps…） ；exit 0
```

### 3.2 缺样例输入的空壳产物（**陷阱**；本机真跑）

GitHub tip **没有** `sample_data/IFCB_2021003`。用仓内 `doc/IFCB_CONFIG.xml`（指向 `brdm0030.21p` / `solo0030.21o` / CAS DCB，站 `SOLO`）在空目录跑：

```bash
rm -rf /tmp/great-ifcb-smoke && mkdir -p /tmp/great-ifcb-smoke && cd /tmp/great-ifcb-smoke
cp ~/iono_ops/GREAT-IFCB/doc/IFCB_CONFIG.xml .
$BIN -x IFCB_CONFIG.xml
# stderr/stdout 含：
#   Error: Exception opening file brdm0030.21p: std::exception
#   … Incomplete header identified. .. brdm0030.21p
#   （OBS/DCB 同理）
#   processing started [ IFCB Estimation ]
#   … recover absolute IFCB finish!
#   Normal End!
# exit 0
wc -c ifcb_2021003_GCE ifcb.log    # 38  2220
cat ifcb_2021003_GCE
```

**本机空壳产物（全文）：**

```text
% IFCB generated using GREAT-IFCB
EOF
```

**判据：** 有效产品应有 `EPOCH-TIME` 块与 `PRN value sigma npoint` 行（源码 `t_ifcb::encode_data`）；**仅头+尾标记且 duration 0.000 s = 失败**，尽管 exit 0 / `Normal End!`。XML 写 `<log> LOGRT.log </log>`，本机实际落盘 **`ifcb.log`**（相对 cwd）。

### 3.3 官方样例路径（PDF；本机未跑）

手册要求 NOAA/`sample_data/IFCB_2021003/`（OBS+`gnss/` NAV/DCB + `site_list` + `IFCB_linux.xml` + `result/ifcb_*_ref`）：

```bash
# 预期（有样例包时；本机无包未执行）：
cd …/sample_data/IFCB_2021003
export LD_LIBRARY_PATH=…/build/Lib
…/build/Bin/GREAT-IFCB -x IFCB_linux.xml
# 期望：ifcb_2021003_GCE 含 EPOCH-TIME，应与 result/*_ref 一致
# python3 …/draw_ifcb.py 2021 3 1 GCE ifcb_2021003_GCE
```

### 3.4 批脚本（本机仅 usage）

```bash
python3 ~/iono_ops/GREAT-IFCB/util/PythonScripts/ifcb.py -h
# → IFCB estimation batch-process script / configfile
python3 …/download_obs.py -h
# → year doy length dst sitelist ；源序 gdc.cddis.eosdis.nasa.gov → igs.gnsswhu.cn
python3 …/draw_ifcb.py -h
# → beg_year beg_doy days system data_dir
```

本机对 `igs.gnsswhu.cn` 匿名 FTP **NLST 425**；CDDIS TLS 需 Earthdata——**未拉** 2021-003 新产品。拉数见 [data-access](../data-access.md)。

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | XML | `<gen>` 时窗/`sys`/`rec`/`int`/`sat_rm`；`<gps|bds|gal>` 的 `<band>`/`<freq>`；`<preedit>`；`<outputs><ifcb>` |
| 入 | RINEX OBS | `<rinexo>`；RINEX 2.10–3.04（PDF） |
| 入 | RINEX NAV | `<rinexn>`（样例 `brdm*.21p`） |
| 入 | CAS/IGG DCB | `<biabern>`（样例 `CAS0MGXRAP_*_DCB.BSX`） |
| 出 | `ifcb_YYYYDDD_S` | S 如 `GCE`；头 `% IFCB generated using GREAT-IFCB`；历元 `EPOCH-TIME mjd sod`；行 `PRN value sigma npoint`（无效前缀 `x`）；尾结束标记 |
| 出 | 日志 | 本机为 cwd **`ifcb.log`**（≠ XML `LOGRT.log` 字面） |

产品数值单位/符号约定以 PDF Appendix A.2 + 源码为准；**无样例时禁止抄写臆造历元值**。

## 5. 参数（XML / CLI）

| 键 / 旗标 | 本机样例（`doc/IFCB_CONFIG.xml`） | 含义 |
| --- | --- | --- |
| `-x file` | `IFCB_CONFIG.xml` | 配置（缺文件 exit 1） |
| `-h` / `-V` / `-X` | — | 帮助 / 版本 / 默认 XML 骨架 |
| `-v` / `-l` | — | 详细度；`-l` 本机空跑未改落盘名（仍见 `ifcb.log`） |
| `<beg>`/`<end>`/`<int>` | 2021-01-03 全日 / 30 s | 时窗与采样 |
| `<sys>` | `GPS BDS GAL` | 多系统（PDF App.A 写「仅一个」与样例/README 多系统矛盾——以能跑的 XML 与 README 为准） |
| `<rec>` | `SOLO` | 测站；正式样例用 `site_list` 多站 |
| `<band>`/`<freq>` | GPS `1 2 5` / `1 2 3`；BDS `2 7 6`；GAL `1 5 7` | 三频顺序 |
| `<preedit>` | elev 7°；MW 3 cyc；GF 0.1 m；gap 20；short 10 | 周跳/短弧 |
| `<outputs><ifcb>` | `ifcb_2021003_GCE` | 相对 **cwd** 的产物名 |

`ifcb_example.ini`（批脚本）：`satsys`、`gps_band`/`gal_band`/`bds_band`、`sitelist`、`software=` 指向二进制。

## 6. 接到哪一步

```text
[data-access] 拉三频 OBS + 混合 NAV + CAS/IGG DCB
        ↓
  GREAT-IFCB  →  ifcb_YYYYDDD_*
        ↓
  （三频 PPP / 钟差产品改正 / 与 UPD 并行）
        ↓
  great-pvt / pride-pppar / ginan / ppp-wizard
```

同链相位偏差 → [great-upd](./great-upd.md)；多 AC 钟差综合 → [clkcomb](./clkcomb.md)。IFCB **不**替代 TEC/GIM。

## 7. 坑（≥8）

1. **GitHub tip 无 sample_data / PreEdit**：README 目录树有，`e245681` 树无——须 NOAA 完整包或自备三频网。
2. **空输入仍 `Normal End!` exit 0**：只出 38 B 头+结束标记；必须以 `EPOCH-TIME` / 非零 duration / 对照 ref 验收。
3. **`LOGRT.log` 名不实**：XML 写了，本机落 **`ifcb.log`**。
4. **预编译无 +x**：`Permission denied` → `chmod +x`。
5. **`LD_LIBRARY_PATH`**：必须能找到 `liblibIFCB.so` 等；与 UPD 一样优先 `build/Lib`；别的 GREAT 仓可能捆旧 libc——勿混用整目录。
6. **输出在 cwd**：`<ifcb>` 相对运行目录。
7. **批下载门禁**：脚本源序 CDDIS TLS → WHU；本机 WHU **425**；Earthdata 见 [data-access](../data-access.md)。
8. **PDF「单系统」vs 多系统 XML**：样例/`<sys> GPS BDS GAL` 与 App.A「only one system」冲突——跟 README 多星座能力与可跑配置。
9. **`doc/IFCB_CONFIG.xml` 注释写反**：`<rinexn>` 旁写 “obs”、`<rinexo>` 旁写 “nav”——以标签名为准。
10. **≠ UPD ≠ PCE ≠ clkcomb**：IFCB 是频间钟差；UPD 是相位延迟；钟差合成另工具。
11. **`-X` 默认骨架不含 `<ifcb>`/`<preedit>`/`<biabern>`**：勿当生产模板；用 `doc/IFCB_CONFIG.xml` 或批脚本生成。
12. **Cube / Gkit-Bias**：Cube 已有篇；Gkit-Bias（DCB/UPD/IFCB→OSB）另仓暂无手册。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 自建多星座 **IFCB** | **GREAT-IFCB** | 专用；有 PDF/预编译 |
| 自建 **UPD**（WL/EWL/NL） | [great-upd](./great-upd.md) | 同 GREAT 链；样例可复现 |
| 多 AC 钟/偏差合成 | [clkcomb](./clkcomb.md) | CLK/BIA 综合 |
| 武大 GREAT PPP | [great-pvt](./great-pvt.md) | 消费偏差/钟差 |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) | 消费 OSB/UPD |
| DCB/UPD/IFCB→OSB 一体 | Gkit-Bias（待手册） | 长安实现；对照用 |
| 只要分析中心产品 | [data-access](../data-access.md) | 不必自估 |
| APM 钟差/DCK | [cube](./cube.md) | Win+MKL |

**下一步候选（目录仍缺短硬）：** `GREAT-PCE`（精密钟差估计）或 `Gkit-Bias`（DCB/UPD/IFCB→OSB）；**Cube / great-upd / 本文已有**——勿重复；勿抢 `galileo-nequick-g` / `ionex` WIP。
