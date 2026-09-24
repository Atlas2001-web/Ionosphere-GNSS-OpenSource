# GNSS-MP · GNSS Multipath Analysis（gnssmultipath）操作手册

目录：[`PROJECTS.json` → `GNSS_Multipath_Analysis_Software`](../../PROJECTS.json) · 上游 <https://github.com/paarnes/GNSS_Multipath_Analysis_Software> · PyPI **`gnssmultipath` 2.2.0** · tip **`806c3d9`** · 许可 **MIT** · 要求 **Python ≥3.10** · 本机验证：NMBUS Samsung S20 OBS + 匹配 SP3 → GPS **C1C RMS MP≈1.273 m** / 加权 **≈1.093 m**；周跳 **47**；**293** 历元；写出 Report/CSV/pkl · 2026-09-24 05:03 EDT

> 岗位：从 **一份 RINEX OBS + 星历（广播 NAV 或 SP3）** 估计各系统各码的 **伪距多路径**、电离层延迟序列、周跳统计与 SNR/天空图，并可选伪距最小二乘粗定位。冲突时：**本机 `import gnssmultipath; help(GNSS_MultipathAnalysis)` / 上游 README > 本文**。读 RINEX → [georinex](./georinex.md)；改/抽稀 → [gfzrnx](./gfzrnx.md)；经典 MP 指标 → [teqc](./teqc.md)；定位引擎 → [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 读 RINEX OBS **2/3/4** + NAV **3/4**（含 RINEX4 多消息类型）或 **SP3-c/d**
- Estey–Meertens 型码多路径 + 几何无关相位电离层；弧段去均值
- 周跳：码–相位与几何无关相位变率 + LLI bit0；仰角截止与加权 RMS
- 报告 `.txt`、按系统 CSV、可选 pickle/zstd、极坐标/条形图（可关）
- 可选：伪距 LS 估计接收机位置 / DOP；内置 CDDIS 下载辅助

**不做：**

- **不是** 定位/PPP 引擎 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 周跳**写回** RINEX 的修复器 → [cycle-slip-correction](./cycle-slip-correction.md) / [drcycleslip](./drcycleslip.md)
- **不是** 仅 MP12 一行摘要的 TEQC → [teqc](./teqc.md)（可对照数量级）
- **不是** TEC 校准产线 → [pytecgg](./pytecgg.md)
- 广播 NAV 路径在部分 **NumPy 2.x + object 数组** 组合会踩 `unique(..., axis=0)`；本机冒烟优先 **SP3**（见坑）

一句话：GNSS-MP = **观测域多路径 / 周跳 / SNR 分析与出图的 Python 工具箱**。

| 术语 | 含义 |
| --- | --- |
| \(M_{P_1}\) | \(P_1-(1+\frac{2}{\alpha-1})L_1+\frac{2}{\alpha-1}L_2\)；弧内去均值 |
| `cutoff_elevation_angle` | 低于此仰角不进统计（README 示例常 10°；默认实现里可被置 0） |
| `phaseCodeLimit` / `ionLimit` | 周跳门限（m/s）；样例约 6.667 / 0.067 |
| `desiredGNSSsystems` | 如 `['GPS']`；过滤过严可能导致 SP3 插值空集 |
| Report / CSV / pkl | 文本总览、分系统表、可重载字典 |

## 2. 安装

```bash
python3 -m venv ~/iono_ops/venv-gnssmp
source ~/iono_ops/venv-gnssmp/bin/activate
pip install -U pip
pip install 'gnssmultipath==2.2.0'
python -c "import gnssmultipath; print(gnssmultipath.__version__)"
# 期望：2.2.0

cd ~/iono_ops
git clone --depth 1 https://github.com/paarnes/GNSS_Multipath_Analysis_Software.git
cd GNSS_Multipath_Analysis_Software && git rev-parse --short HEAD   # 本机 806c3d9
```

作图无 LaTeX 时会自动回退非 TeX 后端。Hatanaka `.crx.gz` 依赖已声明 `hatanaka`。

## 3. 端到端：NMBUS + SP3（本机真跑）

与上游 `tests/test_GNSS_MultipathAnalysis.py::test_GNSS_MultipathAnalysis_sp3_file` 同源数据。

```bash
cd ~/iono_ops/GNSS_Multipath_Analysis_Software/src
source ~/iono_ops/venv-gnssmp/bin/activate
python - <<'PY'
from gnssmultipath import GNSS_MultipathAnalysis
import os
out = '/tmp/gnssmp_nmbus'
os.makedirs(out, exist_ok=True)
res = GNSS_MultipathAnalysis(
    rinObsFilename='../TestData/ObservationFiles/v3/NMBUS_SAMSUNG_S20.20o',
    sp3NavFilename_1='../TestData/SP3/NMBUS_2020 10 30.SP3',  # 文件名含空格
    outputDir=out,
    plotEstimates=False,
    plot_polarplot=False,
    write_results_to_csv=True,
)
g = res['GPS']['Band_1']['C1C']
print('C1C RMS', round(g['rms_multipath_range1_averaged'], 3))
print('C1C wRMS', round(g['elevation_weighted_average_rms_multipath_range1'], 3))
print('slips', g['cycle_slip_distribution']['n_slips_Tot'])
print('nEpochs', res['ExtraOutputInfo']['nEpochs'])
PY
```

**本机结果（2.2.0 / tip `806c3d9`，2026-09-24 05:03 EDT）：**

```text
系统：GPS + GLONASS + Galileo + BeiDou
GPS C1C：RMS multipath ≈ 1.273 m；加权 RMS ≈ 1.093 m；周跳 Tot=47
nEpochs=293；tInterval=1 s；钟跳 2（间隔均值 121 s）
产出：
  /tmp/gnssmp_nmbus/NMBUS_SAMSUNG_S20_Report.txt
  /tmp/gnssmp_nmbus/Result_files_CSV/{GPS,GLONASS,Galileo,BeiDou}_results.csv
  /tmp/gnssmp_nmbus/analysisResults.pkl
```

| 输入 | 说明 |
| --- | --- |
| `NMBUS_SAMSUNG_S20.20o` | RINEX 3.03 混合；约 13:22–13:34 UTC（2020-10-30） |
| `NMBUS_2020 10 30.SP3` | 文件名含空格；与 OBS 同日 |
| `outputDir` | 报告/CSV/pkl 根目录 |

| 输出字段 | 含义 |
| --- | --- |
| `rms_multipath_range1_averaged` | 该码真 RMS（\(\sqrt{\overline{x^2}}\)） |
| `elevation_weighted_average_rms_multipath_range1` | \(w=\min(4\sin^2 E,1)\) 加权 |
| `cycle_slip_distribution` | 按仰角箱计数 + `n_slips_Tot` |
| Report 头 | 版本、文件名、近似坐标、门限、系统列表 |

广播 NAV：把 `sp3NavFilename_1` 换成 `broadcastNav1='…/BRDC….rnx'`。若遇 NumPy `unique`/`object` 报错，改走 SP3（见坑）。

## 4. 关键参数

| 参数 | 作用 |
| --- | --- |
| `rinObsFilename` | OBS 路径（必填） |
| `broadcastNav1..4` / `sp3NavFilename_1..3` | 二选一（可多文件跨日） |
| `outputDir` | 输出目录 |
| `cutoff_elevation_angle` | 仰角截止（度） |
| `desiredGNSSsystems` | 系统白名单；勿与空星座结果叠加 |
| `plotEstimates` / `plot_polarplot` | 关图加速批处理 |
| `write_results_to_csv` / `save_results_as_compressed_pickle` | CSV / zstd pickle |
| `nav_data_rate` | 广播星历抽稀（秒）；测试常用 120 |

API：`from gnssmultipath import GNSS_MultipathAnalysis`（函数入口）。

## 5. 接到哪步

- 读/探 OBS → [georinex](./georinex.md)；格式体检/拼接 → [gfzrnx](./gfzrnx.md)；经典 QC 一行 MP → [teqc](./teqc.md)
- 周跳专项修复试验 → [cycle-slip-correction](./cycle-slip-correction.md) / [drcycleslip](./drcycleslip.md)
- 固定解/PPP 质量对照 → [rtklib](./rtklib.md) / [anubis](./anubis.md)
- 工作流 **A** 前段 QC：RINEX → 本文（天线/多路径）→ [georinex](./georinex.md)/[pytecgg](./pytecgg.md)；概念 [data-access](../data-access.md) · 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ValueError: need at least one array to concatenate` | SP3 与 OBS 无交集，或 `desiredGNSSsystems` 滤空 | 去掉系统过滤；核对 SP3 日期/文件名 |
| 2 | `TypeError: unique … dtype object` | 广播 NAV→object 数组 + NumPy 2 | 改用匹配 **SP3**；或换测过的 NumPy/钉上游 issue |
| 3 | `FileNotFoundError` 含空格 SP3 | 路径未加引号/未用 API 字符串 | Python 字符串整路径；壳层加引号 |
| 4 | 无图/无 GUI | 无显示或未装 TeX | `plotEstimates=False`；库会回退非 TeX |
| 5 | 与 [teqc](./teqc.md) MP12 差一个数量级 | 组合/加权/弧段定义不同 | 只比相对站/天线；勿逐位相等 |
| 6 | `.crx.gz` 读失败 | 未装/坏掉 `hatanaka` | `pip install hatanaka`；或先 [rnxcmp](./rnxcmp.md) 解压 |
| 7 | 期望写回无周跳 OBS | 工具只分析 | 修复链 → [cycle-slip-correction](./cycle-slip-correction.md) |
| 8 | `cd` 到错目录相对路径失效 | 测试习惯在 `src/` 下跑 | 改绝对路径，或 `cd …/src` |
| 9 | 全日 1 Hz 内存大 | 全量进内存 | 先裁时段 OBS（[gfzrnx](./gfzrnx.md)）再分析 |
| 10 | CDDIS 下载 401/超时 | 需 Earthdata | 走 [data-access](../data-access.md)；或预置本地 NAV/SP3 |
| 11 | 把结果当精密坐标发表 | 伪距 LS 仅粗略 | 正式坐标 → [pride-pppar](./pride-pppar.md)/[rtklib](./rtklib.md) |
| 12 | PyPI 无 TestData | 轮子不含样例 | clone 上游仓再用 `TestData/` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 分信号码多路径 + 周跳报告/出图 | **本文 GNSS-MP** |
| 快速读 OBS 进 xarray | [georinex](./georinex.md) |
| 官方级 RINEX 编辑/抽稀 | [gfzrnx](./gfzrnx.md) |
| 经典一行 MP12（EOL） | [teqc](./teqc.md) |
| RTK/PPP 引擎 | [rtklib](./rtklib.md) |

## 8. 相关

[georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [teqc](./teqc.md) · [rtklib](./rtklib.md) · [anubis](./anubis.md) · [cycle-slip-correction](./cycle-slip-correction.md) · [drcycleslip](./drcycleslip.md) · [hatanaka](./hatanaka.md) · [data-access](../data-access.md) · [README](./README.md)

- 方法论摘要见上游 README「Methodology」
- 结果示例：仓内 `Results_example/`
