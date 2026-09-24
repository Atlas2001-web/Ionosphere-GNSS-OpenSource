# FAST · GNSS 下载 / QC / SPP 操作手册

目录：[`PROJECTS.json` → `FAST`](../../PROJECTS.json) · 上游 <https://github.com/ChangChuntao/FAST> · 许可 **GPL-3.0**（`LICENSE`；README 徽章写 MIT **以 LICENSE 为准**）· 源码 tip **3.01.01**（`2026-08-03`）· 本机验证：`sample_data/abpo0010.25o` → satNum 全日 SYS + 首小时 SPP，MEAN XYZ 相对约坐标 Δ≈0.69 m（2026-09-24 EDT）· **质检复跑通过**（satNum+1h SPP 同 I/O）

> 岗位：日常 **IGS/分析中心产品拉取、观测 QC、广播星历 SPP、选站抽稀**。精密 PPP-AR → [pride-pppar](./pride-pppar.md)；读 RINEX 进 xarray → [georinex](./georinex.md)。冲突时：**仓内 `README`/`README_CN` / `manual/*.pdf` > 本文**。

## 1. 用途与边界

**做：**

- 下载：`python src/_fast.py -t <type> -y … -d/-s/-e …`（多线程、可解压）
- QC：`fast.qc.*` / `fast.plot.plotSatNum` 等（卫星数、CNR、周跳、MP、IOD、CMC…）
- SPP：`fast.spp.sppbybrdc.spp` 双频无电离层伪距 + 广播星历（G/C/E）
- 选站：`fast.site.thinning` 格网抽稀；GUI `src/_fastQt.py`（PyQt5）

**不做：**

- **不是** 发表级 PPP-AR / POD → [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md)
- **不是** 旧 TEQC 批壳替代品的唯一选择 → 批处理缺站日目录见 [pinot](./pinot.md)
- **不** 替代数据源说明总表 → [data-access](../data-access.md)
- CLI **无参**会进交互菜单并 `input()` 阻塞；自动化必须带 `-t/-y/…` 或直接调 Python API

一句话：FAST = **下载 + QC + 粗 SPP + 选站** 一体化工具箱（中文用户多）。

| 术语 | 含义 |
| --- | --- |
| `GPS_brdc` / `GCRE_MGEX_obs` … | `-t` 数据类型名（见 `-h` / `supportData`） |
| `doy` | 年积日；`-d` 单日，`-s/-e` 区间 |
| `bandChoose` | `getCode(obsHead, {'G':['1','2'],…})` 结果 |
| `writePosData` | 带头 `# PGM : FAST` 的标准 SPP 文本 |
| `sample_data/` | 仓内 ABPO 2025-001 OBS+NAV+分析样例 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/ChangChuntao/FAST.git
cd FAST
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
# 无头 QC/SPP 最小集；GUI 再加 PyQt5 qdarkstyle qbstyles cartopy
python -m pip install numpy matplotlib
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python -c "from fast.com.pub import lastVersion, lastVersionTime; print(lastVersion, lastVersionTime)"
# 期望：3.01.01 2026-08-03
python src/_fast.py -v
# 期望：2026-08-03 - 3.01.01
```

也可下 Release 预编译 CLI（Ubuntu/CentOS/Win/Mac）；本文以 **源码 + PYTHONPATH** 为准。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ModuleNotFoundError: fast` | 未把 `src` 入路径 | `export PYTHONPATH=$PWD/src` 或在仓库根跑 |
| GUI 起不来 | 缺 PyQt5 | `pip install PyQt5 qdarkstyle qbstyles` |
| `python src/_fast.py` 卡住 | 无参进交互 | 加 `-v`/`-t …` 或 API 调用 |

## 3. 端到端：样例 QC satNum + SPP（本机真跑）

数据：仓内 `sample_data/abpo0010.25o`（RINEX 3.04，2880 历元×30 s）+ `brdc0010.25p`。

### 3.1 卫星数统计（无 GUI）

> 注意：`plotSatNum(..., self=None)` 在 3.01.x 仍引用 GUI 时间窗变量会 `UnboundLocalError`。无头请自建 `satNumData` 再 `writeSatNum`（见下）。

```bash
cd ~/iono_ops/FAST && source .venv/bin/activate
export PYTHONPATH="$PWD/src"
mkdir -p /tmp/fast_e2e
python - <<'PY'
import os
from fast.com.readObs import readObsHead, readObs
from fast.qc.satNum import writeSatNum

obs = "sample_data/abpo0010.25o"
obsHead = readObsHead(obs, needSatList=True)
obsData = readObs(obs, obsHead=obsHead)
epochs = list(obsData)
gnss = ["G", "C", "R", "E", "J", "ALL"]
satNumData = {"stat": {g: {"AVE": 0, "MIN": 0, "MAX": 0} for g in gnss}, "data": {}}
for ep in epochs:
    satNumData["data"][ep] = {g: 0 for g in gnss}
    for sat in obsData[ep]:
        satNumData["data"][ep]["ALL"] += 1
        if sat[0] in satNumData["data"][ep]:
            satNumData["data"][ep][sat[0]] += 1
for g in gnss:
    vals = [satNumData["data"][ep][g] for ep in epochs]
    satNumData["stat"][g] = {"AVE": sum(vals) / len(vals), "MIN": min(vals), "MAX": max(vals)}
out = "/tmp/fast_e2e/abpo_SatNum.txt"
writeSatNum(satNumData, out)
print("epochs", len(epochs), "Approx", obsHead["Approx Position"])
print("SYS", {g: {k: (round(v, 1) if k == "AVE" else v) for k, v in satNumData["stat"][g].items()} for g in gnss})
print("wrote", out)
PY
```

**本机 stdout（节选）：**

```text
epochs 2880 Approx [4097216.5539, 4429119.1897, -2065771.1988]
SYS {'G': {'AVE': 11.3, 'MIN': 8, 'MAX': 14}, 'C': {'AVE': 22.9, 'MIN': 18, 'MAX': 28},
     'R': {'AVE': 8.0, 'MIN': 6, 'MAX': 11}, 'E': {'AVE': 10.5, 'MIN': 6, 'MAX': 14},
     'J': {'AVE': 0.7, 'MIN': 0, 'MAX': 2}, 'ALL': {'AVE': 53.4, 'MIN': 46, 'MAX': 62}}
```

与仓内 `sample_data/analyze/abpo_SatNum.txt` 头统计一致。

### 3.2 广播星历 SPP（首小时）

```bash
python - <<'PY'
import os
from fast.com.readObs import readObsHead, readObs
from fast.com.readNav import readNav
from fast.com.gnssParameter import getCode
from fast.spp.sppbybrdc import spp, writePosData

obs, nav = "sample_data/abpo0010.25o", "sample_data/brdc0010.25p"
obsHead = readObsHead(obs, needSatList=True)
full = readObs(obs, obsHead=obsHead)
epochs = list(full)[:120]                       # 1 h
obsData = {ep: full[ep] for ep in epochs}
navData = readNav(nav)
bandChoose = getCode(obsHead, {"G": ["1", "2"], "C": ["2", "6"], "E": ["1", "5"]})
print("bandChoose keys", {k: list(v) for k, v in bandChoose.items()})
posData, X, Y, Z = spp(obsHead, obsData, navData, bandChoose,
                       epochs[0], epochs[-1], cutoff=7, self=None, posFile=None)
out = "/tmp/fast_e2e/abpo_spp_1h.pos"
writePosData(posData, out)                      # 带标准头；勿只靠 posFile= 裸写
ax, ay, az = obsHead["Approx Position"]
d = ((X - ax) ** 2 + (Y - ay) ** 2 + (Z - az) ** 2) ** 0.5
print(f"MEAN XYZ = {X:.3f} {Y:.3f} {Z:.3f}")
print(f"dXYZ_vs_approx_m = {d:.3f}")
print("n_epochs", len(posData))
print(open(out).read().splitlines()[6:9])
PY
```

**本机 stdout（2026-09-24 EDT）：**

```text
bandChoose keys {'G': ['C1C', 'C2W'], 'C': ['C2I', 'C6I'], 'E': ['C1C', 'C5Q']}
[…]: REF. COORD -> 4097216.106  4429118.678  -2065771.070
MEAN XYZ = 4097216.106 4429118.678 -2065771.070
dXYZ_vs_approx_m = 0.692
n_epochs 120
    mjd       sod                 X[m] …
  60676      0.00          4097216.063         4429119.790        -2065771.536 …
```

| 字段 | 含义 |
| --- | --- |
| `MEAN XYZ` | 窗口内平均站心直角坐标 (m) |
| `dXYZ_vs_approx_m` | 相对 RINEX `Approx Position`；广播 SPP 米级正常 |
| `HDOP/VDOP/PDOP/GDOP` | `writePosData` 行尾四列 |

### 3.3 下载 CLI（可失败，记坑）

```bash
# 版本 / 帮助（-h 末尾会再问是否列出数据类型，管道请准备输入）
python src/_fast.py -v
# 例：GPS 广播星历（源站 FTP 可能拒连）
python src/_fast.py -t GPS_brdc -y 2025 -d 1 -l /tmp/fast_dl -p 4 -u y
```

本机 2026-09-24 对 `igs.gnsswhu.cn` / `nfs.kasi.re.kr` FTP 均失败 → `***No files were downloaded!`。数据备援见 [data-access](../data-access.md)；本地已有 RINEX 时直接走 3.1/3.2。

### 3.4 常用旗标

| 旗标 | 作用 |
| --- | --- |
| `-t/-type` | 数据类型，逗号多选 |
| `-y/-d` 或 `-s/-e` | 年 + doy / 起止 doy |
| `-i/-site` / `-f` | 测站列表或站点文件 |
| `-l/-loc` | 下载目录 |
| `-p` | 并行线程 |
| `-u y/n` | 是否解压 |
| `-r` | 产品三字符重命名 |

## 4. 接到哪步

- 拉观测/星历后探活 → [georinex](./georinex.md)；旧批壳/缺站日 → [pinot](./pinot.md)
- 数据源与镜像 → [data-access](../data-access.md)
- 粗 SPP 冒烟后精密解 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- 路径 A（一日 TEC）仍走 georinex→pytecgg；FAST 只负责备数/粗检

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 进程挂起等输入 | 无参进交互菜单 | 始终带 `-t/-y/…` 或 `-v` |
| 2 | `-h` 末尾再 `input()` | `arg_options` 问是否列类型 | `printf 'n\n' \| python src/_fast.py -h` |
| 3 | `UnboundLocalError: startdatetime` | `plotSatNum` 无 `self` 仍滤时间窗 | 自建 `satNumData`+`writeSatNum`；或走 GUI |
| 4 | `***No files were downloaded!` | 上游 FTP PASV/拒连 | 换镜像/HTTP 源；见 [data-access](../data-access.md) |
| 5 | `posFile=` 行格式怪 / 无头 | 内部 `posCoord='ALL'` 写 ENU+XYZ | 用 `writePosData(posData, path)` |
| 6 | `ModuleNotFoundError: fast` | 未设 `PYTHONPATH=src` | `export PYTHONPATH=$PWD/src` |
| 7 | SPP 少星 / 跳历元 | `bandChoose` 与 OBS TYPES 不匹配 | `getCode(obsHead, {'G':['1','2'],…})` 先 `print` |
| 8 | 以为 MIT 可闭源嵌 | README 徽章误导 | 按 **GPL-3.0** 合规 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 下载+QC+粗 SPP 一体 | **本文 FAST** |
| RINEX→xarray | [georinex](./georinex.md) |
| 旧 CORS 批壳 / 缺站日 | [pinot](./pinot.md) |
| 数据中心与产品入口 | [data-access](../data-access.md) |
| 精密 PPP-AR | [pride-pppar](./pride-pppar.md) |

- 仓库：<https://github.com/ChangChuntao/FAST>
- 中文说明：<https://github.com/ChangChuntao/FAST/blob/main/README_CN.md>
- 手册 PDF：仓内 `manual/FAST_manual-V3.00.pdf`
- Release：<https://github.com/ChangChuntao/FAST/releases>
- 兄弟：[georinex](./georinex.md) · [pinot](./pinot.md) · [data-access](../data-access.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md)
