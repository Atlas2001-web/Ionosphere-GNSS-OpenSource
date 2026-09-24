# MCOSB · 多 GNSS 多频码 OSB 估计（MATLAB）操作手册

目录：[`PROJECTS.json` → `MCOSB`](../../PROJECTS.json) · 上游 <https://github.com/GCCLib/MCOSB> · tip **`f9af2c0`**（2026-02-03；无语义化 tag）· ★**11** · license **see upstream README**（根目录无 `LICENSE`；User Manual Disclaimer）· MATLAB（开发标定 **2024b**；手册称「几乎全版本」）· ECUT/GCC · 本机验证（2026-09-24 06:56–06:59 EDT）：`which matlab` 空；**Octave 9.4.0** 可 `load` 仓内 `OSB/*.mat`；原脚本 `Path='E:\MCOSB'` + `\` 路径 → `fopen` **fid=−1**；把 `\`→`/`、`Year=2024`、`SYS='GPS'`、`DOYEnd=1` 后 Octave 重跑 GPS DOY001：`GPSC5Q` **155**/`GPSC5X` **60** 站进度行；冒烟 **G01 C1C=9.5833 / C5Q=11.7346** ≡ 仓内 `OSB/GPS/GPSSatOSBC5Q.mat`（|Δ|≈**5e−12**）≡ 预置 Bias-SINEX `ECU0MGXFIN_20240010000_01D_01D_OSB.BIA`（sha₁₂=`bd697064377f`，**648** 条 `OSB` 行）。**未臆造**新产品；生产级 OSB 仍看 IGS/AC。

> 岗位：MGEX 网 RINEX + SP3 + GIM → GFIF 提取 SPR **MCB** → 多频码 **OSB**（Bias-SINEX `.BIA`）→ 可用性/时序/STD 分析。冲突时：**仓内四脚本 + `MCOSB_UserManual.pdf` > 本文**。  
> 前置偏差链：[gkit-bias](./gkit-bias.md)（DCB/UPD/IFCB→OSB）· [great-upd](./great-upd.md)（UPD）· 产品门户 [data-access](../data-access.md)「SP3 / CLK / bias」。**≠** [clkcomb](./clkcomb.md)（多 AC 合成）· **≠** PPP 引擎。

## 1. 用途与边界

**做：**

- 四主脚本：`ReadOBS` → `ExtractMCB` → `EstimateCOSB` → `AnalyzeCOSB`
- GPS / Galileo / BDS-3（或 `SYS='ALL'`）多码型 OSB；写 **Bias-SINEX**（`SOFTWARE MCOSB 1.0`）
- 对照分析仓内/自备 `5_FilesAnalysis/{ECU,CAS}/*.BIA`（可用性、时序、STD、可选站分布图）
- 子库 `MCOSBToolbox/`（不含 `m_map` 共 **55** 个 `.m`；全树 **131** 含 m_map）读 RINEX/SP3/IONEX、组法方程、出图

**不做：**

- **不是** 无 MATLAB/Octave 的一键 CLI → [gkit-bias](./gkit-bias.md)
- **不是** 多分析中心轨道/钟差综合 → PROJECTS `SPOCC` / [clkcomb](./clkcomb.md)
- **不是** UPD/IFCB/相位偏差主链 → [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)
- **不是** PPP/PPP-AR → [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)
- 本机**无**商业 MATLAB → 未跑 GUI/`AnalyzeCOSB` 出图；Octave 仅冒烟估计（须改路径分隔符）

一句话：**MCOSB = ECUT 开源多 GNSS 多频码 OSB 估计/分析 MATLAB 工具（GFIF-MCB→Bias-SINEX）**。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** MCOSB | MATLAB 网解码 OSB | `EstimateCOSB.m` → `ECU0MGXFIN_*_OSB.BIA` |
| [gkit-bias](./gkit-bias.md) | C++ DCB/UPD/IFCB→OSB | `gkit_bias *.conf` |
| [great-upd](./great-upd.md) | 武大 UPD | `GREAT-UPD -x …xml` |
| [clkcomb](./clkcomb.md) | 多 AC 钟/偏差合成 | `clkcomb comb.ini` |
| CAS/IGS OSB | 分析中心产品 | `CAS0MGXRAP_*`；本仓对照用 |

## 2. 安装

### 前置

| 组件 | 用途 |
| --- | --- |
| **MATLAB**（标定 2024b；手册：几乎全版本） | **官方运行时** |
| Octave ≥9（可选冒烟） | 本机 **9.4.0** 已通 GPS 日解；**非**上游承诺 |
| 磁盘 | clone 含 zip ≈ **430 MB+**；解压 OBS/SP3/ION 更大 |
| Mapping / 绘图（可选） | `AnalyzeCOSB` + `m_map` 站分布 |

本机：`which matlab` → 空；`octave --eval 'disp(version)'` → **9.4.0**。

### Clone（本机已做）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/GCCLib/MCOSB.git
cd MCOSB && git rev-parse --short HEAD   # 本机：f9af2c0
find . -name '*.m' | wc -l               # 131
find MCOSBToolbox -name '*.m' ! -path '*/m_map/*' | wc -l   # 55
ls *.m
# AnalyzeCOSB.m  EstimateCOSB.m  ExtractMCB.m  ReadOBS.m
ls -lh MCOSB_UserManual.pdf              # 本机：1725979 B
```

| 路径 | 内容（本机） |
| --- | --- |
| `1_FilesOBS/001.zip` | DOY001 RINEX3 样例块（zip 内 **14** 站 `.rnx`，解压约 **403 MB**） |
| `2_FilesSP3/2_FilesSP3.zip` | SP3 **102** 文件 |
| `3_FilesION/3_FilesION.zip` | GIM **100** 文件 |
| `MCB/{GPS,GAL,BDS3}.zip` | 已提取 SPR MCB（可直接估） |
| `OSB/{GPS,GAL,BDS3}/*.mat` | 预估 OSB（各系 **100** 日结构体） |
| `4_FilesOSB/` | `FileHead.BIA` + `4_FilesOSB.zip`（ECU 产品，与 `5_FilesAnalysis/ECU` **逐字节相同**） |
| `5_FilesAnalysis/{CAS,ECU}.zip` | 对照分析：CAS **365** / ECU **100** 日 `.BIA` |
| `STA/{GPS,GAL,BDS3}/001…100/` | 站信息 `.mat`（每系 **100** 日） |

README：**自备网数据才能重跑 `ReadOBS`/`ExtractMCB`**；**可直接**用 `MCB` + `5_FilesAnalysis` 跑 `EstimateCOSB`/`AnalyzeCOSB`。

### 启动（有 MATLAB）

```matlab
cd('.../MCOSB')                 % 仓库根，勿停在子目录
edit EstimateCOSB.m             % 改 Path / Year / DOY* / SYS
% Path = 'D:\iono_ops\MCOSB';  % Linux 用正斜杠：'/home/.../MCOSB'
```

## 3. 端到端（真命令 + 期望）

### 3.1 环境门（本机）

```bash
which matlab          # 空 → 无商业 MATLAB
octave --eval 'disp(version)'
# 9.4.0
```

### 3.2 预置 Bias-SINEX（无需 MATLAB）

```bash
cd ~/iono_ops/MCOSB
unzip -qo 5_FilesAnalysis/ECU.zip -d /tmp/mcosb_bia
head -12 /tmp/mcosb_bia/ECU/ECU0MGXFIN_20240010000_01D_01D_OSB.BIA
rg '^ OSB  .... G01' /tmp/mcosb_bia/ECU/ECU0MGXFIN_20240010000_01D_01D_OSB.BIA | head -3
rg -c '^ OSB' /tmp/mcosb_bia/ECU/ECU0MGXFIN_20240010000_01D_01D_OSB.BIA
```

**本机摘录：**

```text
  SOFTWARE          MCOSB 1.0
  HARDWARE          Matlab 2024b
 OSB  G000 G01           C1C       2024:001:00000 2024:002:00000 ns                  9.5833      0.0000
 OSB  G000 G01           C1W       2024:001:00000 2024:002:00000 ns                 10.4957      0.0000
 OSB  G000 G01           C5Q       2024:001:00000 2024:002:00000 ns                 11.7346      0.0000
 OSB  E000 E02           C1C       2024:001:00000 2024:002:00000 ns                 -1.3323      0.0000
 OSB  C000 C19           C1P       2024:001:00000 2024:002:00000 ns                -23.3042      0.0000
# OSB 行数：648（G182+E250+C216）
```

CAS 对照日：`CAS0MGXRAP_20240010000_01D_01D_OSB.BIA` **816** 条 `OSB`；G01 C1C=**10.1245**（与 ECU **不同系统/方法**，勿强行逐星相等）。

### 3.3 Octave `load` 仓内 `.mat`（本机）

```bash
cd ~/iono_ops/MCOSB
octave --quiet --eval "
addpath('MCOSBToolbox');
load('OSB/GPS/GPSSatOSBC5Q.mat');
disp(size(GPSSatOSBC5Q));          % 1 100
s = GPSSatOSBC5Q(1).OSB;
disp(s(1));                        % C1C≈9.5833 …
"
```

**本机：** `GPSSatOSBC5Q` **100** 日；第 1 日首星字段 `C1C C1W C2W C2L C5Q`，`C1C=9.5833`（与上节 `.BIA` 对齐）。

### 3.4 Octave 重跑 GPS DOY001 估计（本机冒烟；须改路径）

原脚本硬编码 `Path='E:\MCOSB'` 且大量 `MCB\GPS\`：

```bash
octave --quiet --eval "
Path='/workspace/MCOSB';
fid=fopen([Path '/4_FilesOSB/FileHead.BIA'],'r'); disp(['posix=' num2str(fid)]);
fid2=fopen([Path '\4_FilesOSB\FileHead.BIA'],'r'); disp(['win=' num2str(fid2)]);
"
# posix=正整数；win=-1
```

本机做法：解压 `MCB/GPS.zip` → `MCB/GPS/`；临时改写 `EstimateCOSB.m`（**勿提交**）：`Path` 绝对路径、`Year=2024`、`DOYEnd=1`、`SYS='GPS'`、把该文件内路径 `\`→`/`；跳过文末 SINEX 写（GAL/BDS 未估）。

**本机 stdout（节选）：**

```text
Step three: estimate multi-GNSS and multi-frequency code OSB products !
------------> [1] [1/155]   % GPSC5Q has been solved!!
------------> [1] [155/155]   % GPSC5Q has been solved!!
------------> [1] [1/60]   % GPSC5X has been solved!
------------> [1] [60/60]   % GPSC5X has been solved!
SMOKE G01 C1C=9.5833
SMOKE G01 C5Q=11.7346
Step three: completing !
```

与仓内预置 mat / ECU `.BIA` **数值一致**（|Δ C1C|≈5×10⁻¹²）。

### 3.5 MATLAB 官方四步（上游；有许可证时）

按 `MCOSB_UserManual.pdf` §4：

1. 数据入 `1_FilesOBS` / `2_FilesSP3` / `3_FilesION`（或解压仓内 zip）
2. `ReadOBS`：设 `Path`、`SYS`
3. `ExtractMCB`：`Lim=15`、`Year`/`DOY*`、`SYS`（BDS/GAL 各两套码型对）
4. `EstimateCOSB` → `OSB/*.mat` + `4_FilesOSB/ECU0MGXFIN_*_OSB.BIA`
5. `AnalyzeCOSB`：`Center='ECU'|'CAS'`，`Staion`（拼写如此）/`DOY`

期望控制台：`Step one/two/three/four: … completing !`；SINEX 行：`>----- YYYYDOY % SINEX file has been written！`。

## 4. I/O

| 阶段 | 输入 | 输出 |
| --- | --- | --- |
| ReadOBS | `1_FilesOBS/<DOY>/*.rnx` | `OBS/{GPS,GAL,BDS3}/` · `STA/.../STAInformation*.mat` |
| ExtractMCB | OBS + `2_FilesSP3`（**5 min** SP3）+ `3_FilesION` | `MCB/<SYS>/<DOY>/<码型>/*MCB.mat` |
| EstimateCOSB | `MCB/…` + `4_FilesOSB/FileHead.BIA` | `OSB/*.mat` · `4_FilesOSB/ECU0MGXFIN_*_OSB.BIA` |
| AnalyzeCOSB | `5_FilesAnalysis/<Center>/*.BIA`（+ 可选 STA） | 图：可用性 / 时序 / 值 / STD（+ 站图） |

**本机已核对的产品事实：**

| 文件 | 事实 |
| --- | --- |
| ECU DOY001 `.BIA` | **702** 行文件 / **648** 条 `OSB`；G01 C1C=**9.5833** ns |
| CAS DOY001 `.BIA` | **880** 行 / **816** 条 `OSB`；G01 C1C=**10.1245** ns |
| `MCB` GPS DOY001 | `GPSC5Q` **155** 站 · `GPSC5X` **60** 站 |
| GAL/BDS3 DOY001 | `GALC1C` **170** · `GALC1X` **79** · `BDSC1P` **76** · `BDSC1X` **35** |
| `OSB/GPS/GPSSatOSBC5Q.mat` | **100** 日 × **32** 星；字段对齐 C5Q 支路 |

## 5. 参数（四脚本顶栏）

| 符号 | 脚本 | 含义 | 仓内默认 |
| --- | --- | --- | --- |
| `Path` | 全部 | 软件根目录 | `'E:\MCOSB'` ← **必改** |
| `SYS` | Read/Extract/Estimate | `'GPS'`/`'BDS3'`/`'GAL'`/`'ALL'` | `'ALL'` |
| `Lim` | ExtractMCB | 截止高度角 ° | `15` |
| `Year` `DOYStart` `DOYEnd` | Extract/Estimate | 年积日窗 | **`2025`**，1…5 ← 样例数据实为 **2024** DOY001… |
| `NumFre` | EstimateCOSB | BDS/GAL 频点数 | `5` |
| `Center` | AnalyzeCOSB | `'ECU'` / `'CAS'` | `'CAS'` |
| `Staion` | AnalyzeCOSB | 是否画站网（拼写缺 i） | `0` |
| `DOY` | AnalyzeCOSB | 画哪一日 | `1` |

BDS 两套：`C1X/C2I/C5X/C6I/C7Z` 与 `C1P/…/C5P/C7D`；GAL 两套：`C1C/C6C/C7Q/C8Q/C5Q` 与 `C1X/…/C5X`。GPS：`C5Q` 与 `C5X` 两支路。

## 6. 接到哪步

```text
MGEX RINEX + SP3(5min) + GIM
        │
        ▼
   MCOSB ReadOBS → ExtractMCB → EstimateCOSB → ECU*.BIA
        │                              │
        │                              ├──► Pride / PPP 消费 OSB
        │                              └──► AnalyzeCOSB ↔ CAS*.BIA
        │
   旁路：Gkit-Bias / GREAT-UPD·IFCB（相位/DCB 链）· clkcomb（多 AC）
        │
   数据入口：[data-access](../data-access.md)
```

- 已有 AETHER 浮点、要 UPD/IFCB 一体 → [gkit-bias](./gkit-bias.md)
- 只要武大 UPD 样例对拍 → [great-upd](./great-upd.md)
- 只要下发 CAS/CODE OSB → [data-access](../data-access.md)，不必自估

## 7. 坑（≥8）

1. **`Path='E:\MCOSB'` 写死**——Linux/本机必改；`\` 拼接 `fopen` → **fid=−1**（本机已证）。  
2. **脚本 `Year=2025` vs 样例/产品 `2024`**——文件名与 SP3/ION 年错位会空读或错匹配。  
3. **SP3 须 5 min**——`ExtractMCB` 注释；30 s/15 min 产品勿直接塞。  
4. **`ReadOBS`/`ExtractMCB` 需自备解压数据**——仅 `*.zip` 时脚本 `dir` 不到日目录。  
5. **`MCB/*.zip` 解压锚点**——`unzip MCB/GPS.zip` 得到 `GPS/`，应落到 `MCB/GPS/`。  
6. **Octave ≠ 官方**——本机仅 GPS 日解冒烟；`AnalyzeCOSB`/`m_map`/完整 SINEX 写未宣称兼容。  
7. **`Staion` 拼写**——缺字母 i；改名无效。  
8. **CAS vs ECU 数值本就不同**——G01 C1C 10.12 vs 9.58；分析是对照不是回归相等。  
9. **GAL 预置 mat 首星可为 0**——零均值约束下基准星；勿当“空产品”。  
10. **无根目录 LICENSE**——发表/再分发读 PDF Disclaimer + 作者邮箱；m_map 等第三方另有许可。  
11. **SINEX 写依赖三系统 mat**——`SYS='GPS'` 单独估完仍调用 `WriteOSBGAL/BDS` 会未定义——先 `ALL` 或改写尾部。  
12. **生产仍用 IGS/AC**——本工具偏算法复现；PROJECTS 亦写明。

## 8. 选型

| 需求 | 选 | 理由 |
| --- | --- | --- |
| MATLAB 网解多频码 OSB + Bias-SINEX + 论文方法复现 | **MCOSB** | 仓内 MCB/OSB/BIA 可对拍；GFIF 方法 |
| C++/conf、接 AETHER UPD | [gkit-bias](./gkit-bias.md) | 无 MATLAB；本机缺样例数据 |
| 武大 UPD 样例可 `cmp` | [great-upd](./great-upd.md) | 相位延迟，不是码 OSB 网解 |
| 多 AC 轨道钟差综合 | PROJECTS **SPOCC** / [clkcomb](./clkcomb.md) | 输入是各家 SP3/CLK，不是 RINEX→OSB |
| 只消费 CAS/CODE OSB | [data-access](../data-access.md) | 不必自建网 |

**底线：** 没有 MATLAB（或未改路径的 Octave）就用 §3.2–3.3 的 **预置 `.BIA`/`.mat` 事实**；把缺路径的 `fid=−1` 或空 `dir` 当成“估出的 OSB”，会污染偏差链路。
