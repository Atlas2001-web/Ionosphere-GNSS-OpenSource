# FGI-GSRx · 芬兰 FGI 多星座 MATLAB 软件接收机操作手册

目录：[`PROJECTS.json` → `FGI-GSRx`](../../PROJECTS.json) · 上游 <https://github.com/nlsfi/FGI-GSRx> · tip **`91a40a8`**（2026-07-10）· ★**192** · 文案版本 **v2.1.3**（`param` 内 `sys,versionNumber`）· 许可 **GPL-3.0**（`LICENSE`）· 本机验证（**2026-09-24 06:53 EDT**）：clone → **224** 个 `.m`；入口 `main/gsrx.m`；`param/*.txt` **16**；Chapter2 GPSL1：`samplingFreq=26e6` / `sampleSize=8` / `complexData=false` / `centerFrequency=1.56903e9`；ReleaseNotes PDF×**4** + User Manual **463173** B；样例 IF 门户返回 **Request Rejected**（246 B）；`which matlab` 空 → **未跑** acq/track/PVT；**禁止臆造** 坐标/固定率

> 岗位：对 **原始 IF 文件**做事后捕获→跟踪→电文→伪距→PVT（可出 RINEX 3.04）；服务干扰/欺骗、OSNMA、新信号算法实验。冲突时：**仓内 `User Manual FGI-GSRx_v2.1.0.pdf` / `param/default_param_*.txt` / `main/gsrx.m` > 本文**。  
> C++ 接收机 → [gnss-sdr](./gnss-sdr.md)；口袋 SDR → [pocketsdr](./pocketsdr.md)；基带源 → [gps-sdr-sim](./gps-sdr-sim.md)；事后 RINEX → [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 多星座：**GPS / Galileo / BeiDou / GLONASS / NavIC**（含 L1C、B1C、OSNMA 等模块）
- 模块目录：`acq` / `track` / `corr` / `nav` / `obs` / `lse` / `rinex` / `osnma` / `iono`…
- 文本 param：`sys,key,value`；并行跟踪：`parallelChannelTracking` + `PCTenabled`（需 MATLAB PCT）
- v2.1.2+：GPS C/A、Galileo E1B（及 GPS L1C 观测）→ **RINEX 3.04** NAV/OBS

**不做 / 本机限制：**

- **不是** 无 MATLAB 的 CLI → [gnss-sdr](./gnss-sdr.md) / [pocketsdr](./pocketsdr.md)
- **不是** 只生成基带 → [gps-sdr-sim](./gps-sdr-sim.md)
- **不是** RINEX 事后 PPP 引擎 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- Octave **≠** 官方运行时（PCT / 工具箱 / 对象语法）
- 本页 **无** 本机 PVT 数字——质检机无 MATLAB、样例 IF 未落盘

一句话：FGI-GSRx = **GPL 的 MATLAB 研究级软件接收机**（课本 *GNSS Software Receivers* 配套），强依赖商业 MATLAB + 匹配前端的 IF。

| 术语 | 含义 |
| --- | --- |
| `gsrx` | `main/gsrx.m`：主入口 `function [] = gsrx(varargin)` |
| `versionNumber` | 本机 param 标 **`v2.1.3`** |
| `PCTenabled` | 用 Parallel Computing Toolbox 并行跟踪通道 |
| `sampleSize` | **整样本**比特；I+Q 复数据时为二者合计 |
| `complexData` | Chapter2 默认 **false**（实采样）——与 gps-sdr-sim 交织 IQ **不同** |
| `snrMask` | 单位 **dB**（非 C/N0 dB-Hz；发行说明强调） |

## 2. vs gnss-sdr / PocketSDR / gps-sdr-sim / RTKLIB

| | **本文 FGI-GSRx** | [gnss-sdr](./gnss-sdr.md) | [pocketsdr](./pocketsdr.md) | [gps-sdr-sim](./gps-sdr-sim.md) | [rtklib](./rtklib.md) |
| --- | --- | --- | --- | --- | --- |
| 栈 | MATLAB `.m` | C++ / GNU Radio | C + libsdr | 单文件 C | C CLI |
| 输入 | IF + param | IF / SDR | IF / FE | NAV+轨迹 | RINEX |
| 输出 | `.mat` / 图 / RINEX3 | NMEA/KML/RINEX | acq/NMEA | `.bin` IQ | `.pos` |
| 本机 | 树+param 冒烟 | apt PVT | `pocket_acq` | `make`+IF | apt/自编 |

## 3. 安装（诚实：需要 MATLAB）

### 3.1 硬依赖

| 组件 | 说明 |
| --- | --- |
| **MATLAB** | **必需**；并行加速另需 **Parallel Computing Toolbox** |
| 匹配 IF | 采样率 / 中心频 / 实·复 / 位宽必须与 param 一致 |
| 用户手册 PDF | 仓内 `User Manual FGI-GSRx_v2.1.0.pdf`（**463173** B） |

本机：`which matlab` → 空；**未安装 Octave 作为替代**。

### 3.2 Clone（本机已做）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/nlsfi/FGI-GSRx.git
cd FGI-GSRx && git rev-parse --short HEAD   # 91a40a8
find . -name '*.m' | wc -l                  # 224
ls main/gsrx.m param/*.txt | wc -l
ls *.pdf
# FGI-GSRx_v2.1.{0,1,2,3}_*Release*.pdf + User Manual …
```

### 3.3 有 MATLAB 时的启动骨架

```matlab
cd('.../FGI-GSRx')                 % 仓库根进 path
addpath(genpath(pwd))
gsrx('param/default_param_GPSL1_Chapter2.txt')   % 或其它 default_param_*
```

先把 param 里 **Windows 盘符**（`D:\Raw IQ…`、`currentWorkingDirectoryForFGIGSRx`、`matlabpath`）改成你的 Linux/Windows 真路径；`rfFileName` 指向真实 IF。

## 4. 端到端

### 4.1 上游流程（有 MATLAB + IF；本机未解算）

1. 自 [FGI-GSRx-OS-DATAFILES](https://tiedostopalvelu.maanmittauslaitos.fi/tp/julkinen/lataus/tuotteet/FGI-GSRx-OS-DATAFILES) 或 [FGI-JSDR](https://www.maanmittauslaitos.fi/en/research/research/gnss-specialists/fgi-gnss-jamming-and-spoofing-dataset-repository-fgi-jsdr) 取 IF / `.mat`  
2. 复制最接近的 `param/default_param_*.txt`，改 `rfFileName` / `samplingFreq` / `centerFrequency` / `complexData` / `sampleSize`  
3. `gsrx('你的param.txt')` → 看谱/捕获/跟踪图；可选写 RINEX  
4. **坐标以你本机为准，禁止抄造。**

干扰/欺骗数据集、OSNMA 示例见 README 与 `osnma/`。

### 4.2 本机可复现：树 + param 冒烟（无 MATLAB）

```bash
cd ~/iono_ops/FGI-GSRx
test -f main/gsrx.m
rg -n "function \[\] = gsrx" main/gsrx.m
# 19:function [] = gsrx(varargin)

python3 - <<'PY'
from pathlib import Path
from collections import Counter
p=Path('param/default_param_GPSL1_Chapter2.txt')
kv=[]
for l in p.read_text(errors='replace').splitlines():
    s=l.strip()
    if not s or s.startswith('%'): continue
    a=s.split(','); kv.append((a[0].strip(),a[1].strip(),a[2].strip()))
print('kv',len(kv),'sections',dict(Counter(a for a,_,_ in kv)))
for k in ('versionNumber','samplingFreq','sampleSize','complexData',
          'centerFrequency','PCTenabled','elevationMask','snrMask'):
    for a,b,v in kv:
        if b==k: print(f'{a},{b},{v}')
PY
```

**本机结果（2026-09-24 06:53 EDT）：** `kv=80`；sections `sys=28` / `nav=7` / `osnma=4` / `gpsl1=41`；`versionNumber=v2.1.3`；`samplingFreq=26e6`；`sampleSize=8`；`complexData=false`；`centerFrequency=1569030000`；`PCTenabled=true`；`elevationMask=5`；`snrMask=5`。

样例下载探针：`curl` 门户 → **HTTP 200** 但体为 WAF **Request Rejected**（**246** B）→ **未落盘 IF**。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| IF / `.dat` | 由 `gpsl1,rfFileName`（或其它信号段）指定 |
| param `.txt` | `section,key,value`；注释行 `%` |
| 可选 IONEX | `ionomodel=ionex` 时填 `ionexFile` |

| 输出 | 说明 |
| --- | --- |
| `.mat` track/nav | `saveDataFile` / `dataFileOut` |
| 图 | `plotSpectra` / `plotAcquisition` / `plotTracking` |
| RINEX 3.04 | v2.1.2+；GPS/GAL 子集 |
| 不输出 | 无 MATLAB 时的本机 PVT stdout |

## 6. 关键 param 与数据源

| 文件 | 场景 |
| --- | --- |
| `default_param_GPSL1_Chapter2.txt` | 课本 Ch.2；26 Msps 实采样 |
| `default_param_GalileoE1_Chapter4.txt` | Galileo E1 |
| `default_param_MultiGNSS_Chapter7.txt` | 多星座 |
| `default_param_TEXBAT_GPSL1.txt` / `OAKBAT_*` / `FGISpoofRepo_*` / `JammerTest2023_*` | 欺骗/干扰公开集 |
| `default_param_GPSL1C.txt` / `BDSB1C.txt` | 新信号 |

公开数据入口（本机样例 IF **未**成功拉取）：

- OS datafiles：上文 tiedostopalvelu 链  
- Jamming/Spoofing：FGI-JSDR  
- GPS L1C：Fairdata `63f8b776-680b-4c98-ace7-d5e443f2b1c5`

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 立刻找不到文件 | param 仍是 `D:\…` | 改绝对路径；Linux 用正斜杠 |
| 2 | 捕获全失败 | 把 gps-sdr-sim IQ 当 Chapter2 实采样 | 对齐 `complexData`/`sampleSize`/`samplingFreq` |
| 3 | PCT 报错 | 无 Parallel Toolbox 却 `PCTenabled=true` | 改 `false` 或装 PCT |
| 4 | SNR 门限怪 | 把 `snrMask` 当 C/N0 | 按 **dB** 理解（发行说明） |
| 5 | 并行 bat 只在 Win | `runGNSSSingleSatelliteTracking.bat` | Linux 用 PCT 模式或串行 |
| 6 | 无 RINEX | 旧流程 / 非 GPS·GAL | 升 v2.1.2+；查信号支持表 |
| 7 | 样例下不来 | WAF / 地区门禁 | 换网络或邮件问 FGI；勿臆造 |
| 8 | Octave 跑挂 | 非支持运行时 | 用正版 MATLAB |
| 9 | 与 gnss-sdr 坐标比飞 | 前端/算法/历元不同 | 分表；同 IF 再比 |
| 10 | `msToProcess` 过大 | 磁盘/内存爆 | 先短 `msToProcess` 冒烟 |
| 11 | 忽略 `trackingMode` | 1 ms vs 20 ms 数据不匹配 | 与数据文件发行说明一致 |
| 12 | 无 MATLAB 却写“本机 PVT” | 臆造 | 只引用树/param 数字 |

## 8. 接到哪步

1. 无 MATLAB → [gnss-sdr](./gnss-sdr.md) + [gps-sdr-sim](./gps-sdr-sim.md) 文件链；或 [pocketsdr](./pocketsdr.md)  
2. 出 RINEX 后精密定位 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)  
3. 干扰/欺骗研究 → FGI-JSDR + 本文 param 族  
4. 数据礼仪 → [data-access](../data-access.md)

## 9. 选型

| 需求 | 选 |
| --- | --- |
| MATLAB 算法/教学/抗干扰实验 | **本文** |
| 生产向开源接收机（无 MATLAB） | [gnss-sdr](./gnss-sdr.md) |
| 轻量捕获 / Pocket FE | [pocketsdr](./pocketsdr.md) |
| 只生成 GPS L1 IQ | [gps-sdr-sim](./gps-sdr-sim.md) |
| RINEX→RTK/PPP | [rtklib](./rtklib.md) |

## 10. 相关

[gnss-sdr](./gnss-sdr.md) · [pocketsdr](./pocketsdr.md) · [gps-sdr-sim](./gps-sdr-sim.md) · [rtklib](./rtklib.md) · [gogps-matlab](./gogps-matlab.md) · [rapppid](./rapppid.md) · [georinex](./georinex.md) · [data-access](../data-access.md) · [README](./README.md)
