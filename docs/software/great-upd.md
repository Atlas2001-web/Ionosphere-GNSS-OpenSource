# GREAT-UPD · 武大多星座 UPD 估计操作手册

目录：[`PROJECTS.json` → `GREAT-UPD`](../../PROJECTS.json) · 上游 <https://github.com/GREAT-WHU/GREAT-UPD> · tip **`fe4bf6e`**（无 git tag；README 史 **v1.0→v1.2**）· **GPL-3.0** · ★**19** · C++/CMake · 本机验证（2026-09-24 06:35–06:38 EDT）：`g++ 14.2.0` + `cmake 3.31.6` → `build/Bin/GREAT-UPD` **59864** B + `Lib/liblib{Gnut,Mat,UPD}.so`；`-h` → **`GREAT/UPD [0.9.0]`**（`$Rev: 2448 $`，源码编于 **Sep 24 2026 10:36:47**）；样例 `UPD_2020001` GPS：**WL** exit **0**、`upd_wl_2020001_G` **1149** B/**33** 行=`result/`（`cmp`/`sha256₁₂=8ad401614212`）；**EWL** exit **0**、`upd_ewl_2020001_G` **1150** B/**33** 行=`result/`（`cmp`/`sha₁₂=095e18c6ac3e`）；**NL** exit **0**、**92162** 行/**3479073** B（**2880** 历元）——与仓内 `result/` **字节不同**（v1.1 NL 符号约定，首历元 G01 **0.113** ≡ (−ref **0.887**) mod 1，**31/31** 星同构）；stdout 多为历元戳 + `Normal End!`；XML 写 `LOGRT.log` **本机未生成**；批脚本拉 CDDIS **未跑**（旧域/Earthdata 门禁）

> 岗位：**多星座未校准相位延迟（UPD）估计**（WL / EWL / NL）→ 服务 PPP-AR 固定。冲突时：**本机 `GREAT-UPD -h` / `doc/UPD_config/*.xml` / `doc/GREAT-UPD_1.0.pdf` / 上游 ReadMe > 本文**。  
> 下游 PPP → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)；多 AC 钟差合成 → [clkcomb](./clkcomb.md)；产品门户 → [data-access](../data-access.md)「SP3 / CLK / bias」。**≠** [cube](./cube.md)（APM 钟差/PPP-AR fork）。

## 1. 用途与边界

**做：**

- 多 GNSS（GPS/GLO/GAL/BDS）**宽巷 WL / 超宽巷 EWL / 窄巷 NL**（及 `EWL_epoch`）UPD 估计
- XML 驱动 CLI：`GREAT-UPD -x CONFIG.xml`；仓内预编译 Linux/Win/Mac + CMake 源码
- 样例包 `sample data/UPD_2020001`（**18** 站、2020-001）；`util/batch_process/upd.py` 批跑；`util/PreEdit` 周跳旗标；`util/upd_analysis` 出图脚本
- ReadMe：v1.1 调整 NL 正负号对齐 iGMAS；v1.2 增 CAS DCB 读写（影响 WL）

**不做：**

- **不是** PPP/PPP-AR 解算引擎 → [great-pvt](./great-pvt.md)/[pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md)
- **不是** 多 AC 钟差合成 → [clkcomb](./clkcomb.md)；**不是** IFCB 专用工具（GREAT-IFCB 另仓，本目录暂无篇）
- **不** 自带 Earthdata/CDDIS 凭证；`download_*.py` 默认旧域 `cddis.gsfc.nasa.gov` 明文 FTP
- 本机**未**用新日网自产 ambupd/ambflag（样例已捆）；**未臆造** 生产级 UPD 产品名以外的 stdout

一句话：**GREAT-UPD = 武大 GREAT 开源多星座 UPD 估计器**（LibUPD + LibGnut + LibMat）。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** GREAT-UPD | UPD 估计 CLI | `GREAT-UPD -x …xml` |
| [great-pvt](./great-pvt.md) | 精密 PVT（消费 UPD） | `GREAT_PVT -x …` |
| [clkcomb](./clkcomb.md) | 多 AC 钟/偏差合成 | `clkcomb comb.ini` |
| [cube](./cube.md) | APM 钟差/PPP-AR | Win+MKL；Linux 难编 |
| 官方 IGS/CAS OSB | 分析中心偏差产品 | CDDIS/iGMAS；本工具自产 `upd_*` |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| `g++` + `cmake`≥3.0 + GNU `make` | 源码编译（本机采用） |
| 预编译 `bin/Linux/`（可选） | 旧 glibc 捆绑；**勿**把整目录塞进 `LD_LIBRARY_PATH` |
| `python3`（可选） | `util/batch_process/upd.py` |
| CDDIS/Earthdata 或 CODE FTP（可选） | 批脚本拉 OBS/NAV/DCB |

### Linux 源码（本机已通；推荐）

```bash
sudo apt install -y build-essential cmake   # 本机已有 g++ 14.2.0 / cmake 3.31.6
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GREAT-WHU/GREAT-UPD.git
cd GREAT-UPD
git rev-parse --short HEAD   # 本机：fe4bf6e
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)              # → Bin/GREAT-UPD、Lib/liblib*.so
ls -la Bin/GREAT-UPD         # 本机：59864 B
export LD_LIBRARY_PATH="$PWD/Lib:${LD_LIBRARY_PATH:-}"
./Bin/GREAT-UPD -h
```

**本机 `-h`：**

```text
GREAT/UPD [0.9.0] compiled: Sep 24 2026 10:36:47 ($Rev: 2448 $)

Usage: 

    -h|--help              .. this help                          
    -V int                 .. version                            
    -v int                 .. verbosity level                    
    -x file                .. configuration input file           
    --                     .. configuration from stdinp          
    -l file                .. log output file                    
    -X                     .. output default configuration in XML
```

### 预编译陷阱（本机踩过）

```bash
# 错误：把 bin/Linux 整目录加入 LD_LIBRARY_PATH
# → 捆绑的旧 libc.so.6 污染系统动态链接（Assertion / GLIBC_2.xx not found）
# 正确：只用 liblib*.so，或优先源码 build/Lib
mkdir -p /tmp/great-upd-libs
cp -a ~/iono_ops/GREAT-UPD/bin/Linux/liblib*.so /tmp/great-upd-libs/
export LD_LIBRARY_PATH=/tmp/great-upd-libs
~/iono_ops/GREAT-UPD/bin/Linux/GREAT-UPD -h
# → GREAT/UPD [0.9.0] compiled: Aug  5 2020 15:57:06 ($Rev: 2448 $)
```

预编译二进制自称 **0.9.0 / 2020-08-05**；源码 tip 含 v1.1/v1.2 修正——**以源码构建为准**。

### PreEdit（周跳旗标；本机仅 help）

```bash
chmod +x util/PreEdit/Linux/GREAT-PreEdit
# 同理勿加载该目录捆绑 libc
./util/PreEdit/Linux/GREAT-PreEdit -h
# → GREAT/TURBOEDIT [0.9.0] compiled: Aug  5 2020 16:13:12 ($Rev: 2448 $)
```

更完整开源见上游链 <https://github.com/GREAT-WHU/Great_TurboEdit_UPDFormat>（ReadMe 2026-03-05）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `GLIBC_2.xx not found` / ld.so Assertion | `LD_LIBRARY_PATH` 含捆绑 `libc.so.6` | 只链 `liblib*.so` 或用 `build/Lib` |
| 无参 exit **255** | 缺 XML / 无 `updmode` | 必须 `-x`；见下 |
| `-x` 缺文件 exit **1** | `xconfig: not file read … File was not found` | 改路径 |
| 路径含空格 | 目录名 `sample data` | 引用加引号或拷到无空格路径 |

## 3. 端到端（本机真跑；样例 2020-001 GPS）

```bash
export LD_LIBRARY_PATH=~/iono_ops/GREAT-UPD/build/Lib
BIN=~/iono_ops/GREAT-UPD/build/Bin/GREAT-UPD
cp -a ~/iono_ops/GREAT-UPD/"sample data"/UPD_2020001 /tmp/great-upd-smoke
cd /tmp/great-upd-smoke
# 输出写在 cwd（XML 的 <upd> 相对路径），勿依赖空 result/
```

### 3.1 WL（宽巷）

```bash
$BIN -x XML/upd_WL_Linux.xml
# stdout： Normal End!   ；exit 0  （约 26 s）
wc -l upd_wl_2020001_G          # 33
cmp upd_wl_2020001_G result/upd_wl_2020001_G && echo MATCH
```

**本机产物摘录：**

```text
% UPD generated using upd_WL
 G01           0.861     0.000   18
 G02           0.413     0.023   18
 …
 G32           0.686     0.023   18
EOF
```

### 3.2 EWL（超宽巷）

```bash
$BIN -x XML/upd_EWL_Linux.xml
# stdout： Normal End!   ；exit 0
cmp upd_ewl_2020001_G result/upd_ewl_2020001_G && echo MATCH
# 本机头：G01 0.256 …；xG02 / xG05 为无效（sigma=10000）
```

### 3.3 NL（窄巷；注意 v1.1 符号）

```bash
$BIN -x XML/upd_NL_Linux.xml
# stdout：每 30 s 一行历元时间戳（2880 行）+ Normal End!  ；exit 0（约 44 s）
wc -l upd_nl_2020001_G          # 92162
# 与仓内 result/upd_nl_2020001_G：行数同、数值为 v1.1 符号约定 → 勿强求 cmp
```

**本机首历元：**

```text
% UPD generated using upd_NL
 EPOCH-TIME   58849       0.0
 G01             0.113     0.042    4
 G02             0.306     0.041    5
 G03             0.876     0.047    3
```

仓内预置 ref 同历元 G01=**0.887**（≈ (−0.113) mod 1）。ReadMe：**v1.1 NL 正负号已调至与 iGMAS 产品一致**——源码 tip 输出以后者为准。

### 3.4 用法 / 缺配置（真报错）

```bash
$BIN                 # 无 -x → 警告缺 gen/updmode → *** warning: not defined upd mode []  ；exit 255
$BIN -x /no/such.xml # xconfig: not file read /no/such.xml File was not found  ；exit 1
$BIN -V 1            # GREAT/UPD [0.9.0] compiled: …  ；exit 0
```

### 3.5 批处理脚本（本机仅 usage）

```bash
python3 ~/iono_ops/GREAT-UPD/util/batch_process/upd.py -h
# Purpose: UPD estimation script
# Usage: python  upd.py  -c  <config_file>  --config=<config_file>
# 样例：cd "sample data/UPD_2020001" && python3 …/upd.py -c upd_Linux.ini
# （ini 默认 satsys=C、upd_mode=WL+NL；需先设好 LD_LIBRARY_PATH 与 software= 路径）
```

拉数脚本默认 `cddis.gsfc.nasa.gov` FTP / CODE `ftp.aiub.unibe.ch`——**本机未执行真实下载**；现行 CDDIS 见 [data-access](../data-access.md)。

## 4. 输入 / 输出

| 方向 | 格式 | 说明 |
| --- | --- | --- |
| 入 | XML | `updmode`=`WL`/`EWL`/`EWL_epoch`/`NL`；`<gen>` 时窗/系统/测站/`sat_rm` |
| 入 | RINEX OBS/NAV | WL/EWL：`<rinexo>`+`<rinexn>`；NL 可不读 OBS |
| 入 | `.ambflag` / `ambflag23` | 周跳旗标（PreEdit）；EWL 用 L2/L5 等 |
| 入 | CODE/CAS DCB（`<biabern>`） | WL/EWL；v1.2 支持 CAS |
| 入 | `*_ambupd_*` | NL：浮点 IF+宽巷模糊度 |
| 入 | 已估 WL UPD | NL 的 `<upd>` |
| 入 | 可选 `<ifcb>` | EWL |
| 出 | `upd_{wl,ewl,nl}_YYYYDDD_S` | S=`G/R/E/C`；WL/EWL 日常数；NL 按历元块 |
| 出 | 声称 `LOGRT.log` | 本机样例跑**未落盘**（坑） |

样例规模（本机）：OBS≈**341** MB / ambupd≈**96** MB / gnss≈**10** MB；**18** 站。

## 5. 参数（XML / CLI）

| 键 / 旗标 | 本机样例 | 含义 |
| --- | --- | --- |
| `-x file` | `XML/upd_*_Linux.xml` | 配置（必需） |
| `-h` / `-V` / `-X` | — | 帮助 / 版本串 / 倾倒默认 XML 骨架 |
| `-v` / `-l` | — | 详细度 / 日志路径（与 XML `<log>` 并存时以实跑为准） |
| `<beg>`/`<end>`/`<int>` | 2020-01-01 全日 / 30 s | 时窗与采样 |
| `<sys>` | `GPS`（可改 GLO/GAL/BDS） | 单次估计一个系统字母名 |
| `<rec>` | 18 站四字符 | 测站表 |
| `<sat_rm>` | `G04` | 排除星 |
| `updmode` | `WL` / `EWL` / `NL` | 估计模式 |
| `bds_code_bias_corr` | `true` | BDS 码偏差改正（WL/EWL） |
| `<band>`/`<freq>` | GPS `1 2 5` / `1 2 3` | 频点选择 |
| `<outputs verb>` | `2` | 详细度；NL 会刷历元时间戳到 stdout |

`upd_Linux.ini`（批脚本）：`upd_mode=WL+NL`、`satsys`、`sitelist`、`software=` 指向二进制。

## 6. 接到哪一步

```text
[data-access] 拉 OBS/NAV/DCB（+可选精密钟轨）
        ↓
  PreEdit / ambflag  →  ambflag*
        ↓
  GREAT-UPD  WL(/EWL)  →  upd_wl_* / upd_ewl_*
        ↓
  （浮点 PPP 或网解）→ ambupd*
        ↓
  GREAT-UPD  NL        →  upd_nl_*
        ↓
  great-pvt / pride-pppar / ginan / ppp-wizard  PPP-AR
```

钟差综合可并行 [clkcomb](./clkcomb.md)。电离层：UPD 改善固定率，**不**替代 TEC/GIM 产品。

## 7. 坑（≥8）

1. **捆绑 libc**：`export LD_LIBRARY_PATH=…/bin/Linux` 会拖入旧 `libc.so.6` → 系统命令全面崩；只链 `liblib*.so` 或 `build/Lib`。
2. **预编译 vs tip**：bin 自称 2020-08-05 **0.9.0**；NL 符号/CAS DCB 修正在源码 tip——优先 `cmake && make`。
3. **NL ≠ 仓内 result cmp**：v1.1 后本机 NL ≡ (−旧值) mod 1；WL/EWL 仍可与 `result/` 逐字节一致。
4. **`LOGRT.log` 未出**：样例 XML 写了 `<log>`，本机三次跑均无该文件——勿当失败判据；看 `upd_*` 与 `Normal End!`。
5. **输出在 cwd**：`<upd> upd_wl_…` 相对运行目录，不是自动进 `result/`。
6. **目录名空格**：`sample data/` 必须加引号。
7. **无 `-x` → exit 255**：不是 usage；多参/`-h` 才给帮助。
8. **NL 依赖 ambupd + 先验 WL**：缺文件会在解码阶段失败；样例已捆 18×`*_ambupd_2020001`。
9. **EWL 用 `ambflag23/`**：与 WL 的 `ambflag/` 不是同一套旗标。
10. **批下载门禁**：`download_obs/nav.py` → 旧 CDDIS 主机；现行 Earthdata 见 [data-access](../data-access.md)；本机**未拉**新日。
11. **单系统一次**：`<sys> GPS </sys>`；多系统需多次或改批脚本 `satsys`。
12. **≠ Cube / ≠ clkcomb**：UPD 估计器；钟差合成与 APM PPP-AR 是别的仓。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| 自建多星座 **UPD**（WL/EWL/NL） | **GREAT-UPD** | 专用；样例可复现 |
| 武大 GREAT **PPP/RTK** 消费 UPD | [great-pvt](./great-pvt.md) | XML PVT；本工具上游产品 |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) | 消费 OSB/UPD；不估 UPD |
| 多 AC 钟/偏差合成 | [clkcomb](./clkcomb.md) | CLK/BIA 综合，非 UPD LSQ |
| APM 钟差/DCK + PPP-AR | [cube](./cube.md) | Win+MKL；Linux 难编 |
| 只要分析中心 OSB/UPD | [data-access](../data-access.md) | 直接下产品，不必自估 |
| GA YAML PPP/POD | [ginan](./ginan.md) | 自管偏差模型 |

**下一步候选（目录仍缺短硬）：** `GREAT-IFCB`（同链频间钟差）或 `GREAT-PCE`（精密钟差估计）或 `Gkit-Bias`（DCB/UPD/IFCB→OSB）；**Cube 已有篇**——勿重复。
