# spinifex · 用 GIM + IGRF 算射电天文视线 TEC / 法拉第旋转量（RM）操作手册

目录：上游 <https://git.astron.nl/RD/spinifex>（ASTRON + CSIRO；GitHub 镜像 lofar-astron/spinifex）· PyPI **`spinifex` 2.0**（2026-08-13 上传，= tag `v2.0` `3788d3d`；main tip `e2ca48c` 2026-09-09）· **Apache-2.0** · RMextract 的后继 · 本机验证 **2026-09-26 03:38–03:45 EDT**：CPython 3.11.16 venv，astropy 8.0.1 / ppigrf 2.1.0（IGRF-14）/ PyIRI 0.1.7 / numpy 2.4.6；LOFAR 核心看 Cas A，2024-08-22（DOY 235），CODE 终版 GIM（AIUB 下载）与 UPC UQRG（Chapman 自动下载）两套。

> **质检复跑通过**（2026-09-26 03:43–03:47 EDT）。
> - 环境：独立 uv venv，spinifex 2.0（无 casacore）；PyPI 2.0 上传 2026-08-13 13:46 UTC、`v2.0`=`3788d3d`、main `e2ca48c`（`git ls-remote`）、Apache License 均核对无误。
> - 逐字复现：AIUB CODE DOY 235/236 字节数（355254/354652）；§3 CODE 8 行表逐位一致（00:00 RM 1.1773±0.1067，12:00 1.6112）；UQRG 变体 8 行与节选 4 行一致，自动下载 `uqrg2350.24i.Z` 1230257 B，15:00 1.5332 vs CODE 1.3676，CODE−UQRG 差 0.003–0.17；§4 `check_vtec.py` 三行一致，`apply_earth_rotation=0` 时最大差实测 2.9e−10 TECU（即“逐位一致”成立），开旋转 0.552/+0.162；`rm_iri.py` 9 行逐位一致（100 层 50–20000 km，12:00 比值 0.821）。坑 1（ImportError 原文）、4（代码默认 `server=chapman, prefix=uqr`）、5（只放当天文件报 netrc 错；`remove_midnight_jumps=False` 时 12:00 RM 1.61117527）、6（`height=350` 仍为 1.61117527；改 `DEFAULT_IONO_HEIGHT` 后为 1.44861521）、8、9 都已复现。
> - 修正：耗时本次 4.4 s（原 2.1 s，冷启动 import 的差），§8 改为 2–5 s；其余无改动。
> - 未复跑：casacore/CLI、MS→H5Parm、FITS 改正、`tomion`，也没和 RMextract 对比（与原文局限一致）。

> 岗位：给“测站 + 时间 + 视线方向（天体坐标或高度角/方位角）”，从 **IONEX GIM** 插出穿刺点 TEC，乘 **IGRF** 地磁场视线分量，输出视线 TEC 与电离层 **RM**（rad/m²）；也能直接给 MeasurementSet 写 H5Parm、给 FITS 立方做 RM 改正。  
> 冲突时：本机 `site-packages/spinifex/*.py` > 上游 docs（部分默认值已过时，见坑 4）> 本文。

## 1. 它解决什么（术语）

| 术语 | 一句话 | 在 spinifex 里 |
| --- | --- | --- |
| **VTEC / GIM / IONEX** | GNSS 反演的全球垂直 TEC 格网（CODE 1 h、UQRG 15 min…），IONEX 是交换格式 | 唯一的电子含量来源（`ionex`/`ionex_iri` 模型）；自己不做 GNSS 处理 |
| **IPP**（穿刺点） | 视线与高度 h 薄壳的交点 | `get_ipp_from_skycoord/altaz`；单层默认 **450 km** |
| **STEC** 与 **映射函数** | 视线 TEC = VTEC × airmass（单层映射 1/cos z′） | `DTEC.electron_density`（每层 TECU）× `DTEC.airmass` |
| **法拉第旋转 / RM** | 线偏振电磁波穿过磁化等离子体，偏振角转 `Δχ = RM·λ²`；RM ∝ ∫ nₑ B∥ dl | `RM.rm = −2.62e−6 · Σ(nₑ[TECU] · B∥[nT] · airmass)` |
| **B∥ / IGRF** | 国际地磁参考场；取 IPP 处场矢量在视线上的投影 | `ppigrf.igrf_gc`（ppigrf 2.1.0 默认 `IGRF14.shc`），逐日一次 |
| 等离子体层修正 | 单层把电子全放在 450 km，高空（B 更弱）的电子被高估 → RM 偏大 | `ionex_iri`：用 **PyIRI** 归一化剖面把 GIM 的 TEC 分到 100 层（50–20000 km） |
| **dTEC** | 视线 TEC（或相对值），射电干涉仪做相位改正用 | `get_dtec_from_skycoord/altaz`，CLI `get_tec_h5parm_from_ms` |

一句话：spinifex = **GIM 插值（含日固系旋转、跨午夜去跳）+ 几何（IPP/airmass）+ IGRF 投影**。它是 GNSS 电离层产品的**下游消费者**：GIM 的误差（2.5°×5° 平滑、DCB、映射高度）原样传进 RM。

与 GNSS 的关系：GNSS 用双频求 STEC → 建 GIM；spinifex 反过来用 GIM 给任意视线“预报” STEC。把视线换成某颗 GNSS 卫星的高度角/方位角（`get_dtec_from_altaz`），就得到 GIM 模型 STEC，可与 [ionotec](./ionotec.md)/[tec-suite](./tec-suite.md) 的实测 STEC 对比（本文未做）。

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3.11 -m venv spx-venv && . spx-venv/bin/activate
pip install --no-cache-dir spinifex                 # 2.0；拉 astropy、ppigrf、PyIRI、h5py、fitscube…（本机 venv 597 MB）
pip install --no-cache-dir python-casacore          # 只有要用 CLI / MeasurementSet 时才需要（本机 venv 597→712 MB）
spinifex -h                                         # 子命令：get_rm_h5parm_from_ms / get_tec_h5parm_from_ms / correct_fits_images
```

CLI 只面向 MS / FITS；“给站点和时间算 RM”要走 Python API（下面全部是 API）。

## 3. 端到端 A：LOFAR 核心 → Cas A，一天 8 个时刻（本机真跑）

数据：CDDIS 需要 Earthdata 登录且本机被挡（425），所以把 CODE 终版 GIM 从 AIUB 先下到 `output_directory`；spinifex 发现同名文件就**跳过下载**。默认 `remove_midnight_jumps=True` 会同时读 **当天和次日**。

```bash
mkdir -p ~/iono_ops/spx-demo/ionex_files && cd ~/iono_ops/spx-demo
for d in 235 236; do curl -sfL -O --output-dir ionex_files https://www.aiub.unibe.ch/download/CODE/2024/COD0OPSFIN_2024${d}0000_01D_01H_GIM.INX.gz; done   # 355254 / 354652 B
```

`rm_lofar.py`（站点坐标为 CS002 附近的近似值）：

```python
# rm_lofar.py — LOFAR 核心看 Cas A，2024-08-22 每 3 小时 TEC/RM（CODE 终版 GIM + IGRF14）
import time as _t; t0 = _t.time()
import sys, numpy as np, astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from spinifex import get_rm, get_dtec
lofar = EarthLocation(lon=6.8698 * u.deg, lat=52.9151 * u.deg, height=50 * u.m)   # CS002 附近（近似）
casa = SkyCoord(ra=350.85 * u.deg, dec=58.815 * u.deg)
times = Time("2024-08-22T00:00:00") + np.arange(0, 24, 3) * u.hour
pre, srv = (sys.argv[1:3] if len(sys.argv) > 2 else ("cod", "cddis"))              # 默认: CODE 终版，本地已有 → 跳过下载
opt = dict(prefix=pre, server=srv, output_directory="ionex_files")
rm = get_rm.get_rm_from_skycoord(loc=lofar, times=times, source=casa, **opt)
dt = get_dtec.get_dtec_from_skycoord(loc=lofar, times=times, source=casa, **opt)
vtec = dt.electron_density.sum(axis=1); stec = (dt.electron_density * dt.airmass).sum(axis=1)
print(f"height={rm.height[0]} km  shapes rm={rm.rm.shape} ne={rm.electron_density.shape}")
print(" UTC    el(deg) az(deg)  VTEC  STEC  B_par(nT)   RM(rad/m^2)")
for i, t in enumerate(times):
    print(f"{t.iso[11:16]}  {rm.elevation[i]:6.2f} {rm.azimuth[i]:7.2f} {vtec[i]:5.2f} {stec[i]:5.2f} "
          f"{rm.b_parallel[i,0]:9.1f}  {rm.rm[i]:.4f} ± {rm.rm_error[i]:.4f}")
print(f"elapsed {_t.time()-t0:.1f} s")
```

```bash
python -u rm_lofar.py 2>&1 | grep -v '^INFO'
```

真实 stdout：

```text
height=[450.] km  shapes rm=(8,) ne=(8, 1)
 UTC    el(deg) az(deg)  VTEC  STEC  B_par(nT)   RM(rad/m^2)
00:00   80.37   45.90 12.47 12.63  -35585.4  1.1773 ± 0.1067
03:00   71.48  301.57  8.88  9.30  -33873.3  0.8258 ± 0.1116
06:00   48.99  310.08 15.80 20.01  -24914.5  1.3063 ± 0.1225
09:00   31.27  329.18 23.40 38.91  -14876.9  1.5166 ± 0.1008
12:00   22.36  352.80 31.17 61.94   -9928.7  1.6112 ± 0.0841
15:00   24.84   17.60 24.71 46.62  -11196.0  1.3676 ± 0.0822
18:00   37.94   39.64 24.77 36.66  -18647.0  1.7910 ± 0.0997
21:00   58.22   55.78 17.83 20.49  -29112.2  1.5627 ± 0.1032
elapsed 2.1 s
```

stderr 的 INFO 行会写明用了哪个文件：`File ionex_files/COD0OPSFIN_20242350000_01D_01H_GIM.INX.gz already exists. Skipping download.`（次日同理；DOY 234 没被读）。

手算核对 00:00：`2.62e-6 × 12.63 × 35585.4 = 1.1776`，与 1.1773 一致（差在四舍五入）；B∥ 为负 → 按公式 RM 为正。Cas A 在 52.9°N 是拱极源，12:00 UTC 下中天仰角 22°，airmass ≈ 2，STEC 是 VTEC 的 2 倍，但 B∥ 只有 −9.9 μT，RM 反而没翻倍。

同一脚本改用 UPC 15 min 的 UQRG（`python -u rm_lofar.py uqr chapman`，自动下载 `uqrg2350.24i.Z` 1230257 B + `uqrg2360.24i.Z`）：

```text
00:00   80.37   45.90 12.44 12.59  -35585.4  1.1742 ± 0.0983
06:00   48.99  310.08 17.44 22.09  -24914.5  1.4418 ± 0.0874
12:00   22.36  352.80 31.88 63.34   -9928.7  1.6476 ± 0.0568
18:00   37.94   39.64 26.93 39.86  -18647.0  1.9474 ± 0.0786
elapsed 8.5 s
```

（节选 4 行，几何与 B∥ 完全相同，只差 VTEC）。8 个时刻里 CODE 与 UQRG 的 RM 差 0.003–0.17 rad/m²（15:00 最大：1.3676 vs 1.5332），**GIM 的选择本身就是 ~10% 量级的不确定度**。

## 4. 端到端 B：VTEC 插值独立核对 + 单层 vs IRI 剖面（本机真跑）

`check_vtec.py`：拿 spinifex 算的 IPP，用自己的“时间线性 + 空间双线性”插 CODE 图，对比 spinifex 的 VTEC；取**半点**（两幅图之间）：

```python
# check_vtec.py — 用 spinifex 的 IPP，自己双线性插 CODE IONEX，对照 spinifex 的 VTEC
import gzip, datetime as dtm, numpy as np, astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from spinifex import get_dtec
from spinifex.geometry.get_ipp import get_ipp_from_skycoord
lofar = EarthLocation(lon=6.8698 * u.deg, lat=52.9151 * u.deg, height=50 * u.m)
casa = SkyCoord(ra=350.85 * u.deg, dec=58.815 * u.deg)
times = Time("2024-08-22T00:30:00") + np.arange(0, 24, 3) * u.hour   # 半点：两幅图之间
L = gzip.open("ionex_files/COD0OPSFIN_20242350000_01D_01H_GIM.INX.gz", "rt").read().splitlines(); M, ep = [], []
for i, s in enumerate(L):
    lab = s[60:].strip()
    if lab == "START OF TEC MAP":
        ep.append(dtm.datetime(*map(int, L[i+1][:36].split()))); g, j = [], i + 2
        while len(g) < 71:
            v = "".join(L[j+1:j+6]); g.append([int(v[k:k+5]) * 0.1 for k in range(0, 365, 5)]); j += 6
        M.append(np.array(g))
    elif lab == "START OF RMS MAP": break
M = np.array(M)
def gim(t, la, lo):
    x = (t - ep[0]).total_seconds() / 3600; k = min(int(x), 23); w = x - k
    fi, fj = (87.5 - la) / 2.5, ((lo + 180) % 360) / 5; i0, j0 = int(fi), int(fj); a, b = fi - i0, fj - j0
    g = (1 - w) * M[k] + w * M[k + 1]
    return (1-a)*(1-b)*g[i0, j0] + (1-a)*b*g[i0, j0+1] + a*(1-b)*g[i0+1, j0] + a*b*g[i0+1, j0+1]
ipp = get_ipp_from_skycoord(loc=lofar, times=times, source=casa, height_array=[450.0] * u.km)
for rot in (1, 0):
    d = get_dtec.get_dtec_from_skycoord(loc=lofar, times=times, source=casa, prefix="cod", server="cddis",
                                        output_directory="ionex_files", apply_earth_rotation=rot)
    mine = np.array([gim(t.to_datetime(), la, lo) for t, la, lo in zip(times, ipp.lat.to_value(u.deg)[:, 0], ipp.lon.to_value(u.deg)[:, 0])])
    dv = d.electron_density[:, 0] - mine
    print(f"apply_earth_rotation={rot}: max|spinifex-mine|={np.abs(dv).max():.3f} TECU  mean={dv.mean():+.3f}")
print("IPP lat/lon 00:30:", round(ipp.lat.to_value(u.deg)[0, 0], 3), round(ipp.lon.to_value(u.deg)[0, 0], 3), " 12:30:", round(ipp.lat.to_value(u.deg)[4, 0], 3), round(ipp.lon.to_value(u.deg)[4, 0], 3))
```

```text
apply_earth_rotation=1: max|spinifex-mine|=0.552 TECU  mean=+0.162
apply_earth_rotation=0: max|spinifex-mine|=0.000 TECU  mean=-0.000
IPP lat/lon 00:30: 53.156 7.214  12:30: 60.887 5.985
```

读法：关掉日固系旋转时与朴素插值逐位一致，说明 IONEX 读取/网格方向没问题；默认开旋转（相邻两图按地球自转对齐经度再插）带来 ≤0.55 TECU 的差。整点时刻两者都为 0（落在图历元上，旋转不起作用）。

`rm_iri.py`：同一几何比较 `ionex` 与 `ionex_iri`（历史 F10.7 用包内快照，本机无下载）：

```python
# rm_iri.py — 同一几何，ionex（单层 450 km）vs ionex_iri（IRI 归一化剖面 × GIM 总量）
import numpy as np, astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.time import Time
from spinifex import get_rm
lofar = EarthLocation(lon=6.8698 * u.deg, lat=52.9151 * u.deg, height=50 * u.m)
casa = SkyCoord(ra=350.85 * u.deg, dec=58.815 * u.deg)
times = Time("2024-08-22T00:00:00") + np.arange(0, 24, 3) * u.hour
opt = dict(prefix="cod", server="cddis", output_directory="ionex_files")
a = get_rm.get_rm_from_skycoord(loc=lofar, times=times, source=casa, iono_model_name="ionex", **opt)
b = get_rm.get_rm_from_skycoord(loc=lofar, times=times, source=casa, iono_model_name="ionex_iri", **opt)
print("ionex_iri heights:", b.height.shape, b.height[0, 0], "...", b.height[0, -1], "km")
for i, t in enumerate(times):
    print(f"{t.iso[11:16]}  ionex RM={a.rm[i]:.4f}  ionex_iri RM={b.rm[i]:.4f}  ratio={b.rm[i]/a.rm[i]:.3f}")
```

```text
ionex_iri heights: (8, 100) 50.0 ... 20000.000000000004 km
00:00  ionex RM=1.1773  ionex_iri RM=1.1344  ratio=0.964
03:00  ionex RM=0.8258  ionex_iri RM=0.8023  ratio=0.972
06:00  ionex RM=1.3063  ionex_iri RM=1.3340  ratio=1.021
09:00  ionex RM=1.5166  ionex_iri RM=1.4486  ratio=0.955
12:00  ionex RM=1.6112  ionex_iri RM=1.3228  ratio=0.821
15:00  ionex RM=1.3676  ionex_iri RM=1.1814  ratio=0.864
18:00  ionex RM=1.7910  ionex_iri RM=1.7533  ratio=0.979
21:00  ionex RM=1.5627  ionex_iri RM=1.5423  ratio=0.987
```

低仰角（12:00、15:00）时差最大（−18%/−14%）：斜视线穿过的高空电子处在更弱的磁场里，单层模型把它们都算在 450 km 就高估了 RM。这符合上游文档对 `ionex_iri` 的说法；没有偏振观测做真值，**本文不判断哪个更准**。

## 5. 参数与字段

API：`get_rm.get_rm_from_skycoord(loc, times, source, iono_model_name="ionex", magnetic_model_name="ppigrf", **iono_kwargs)`；`get_rm_from_altaz(loc, altaz, …)`（`altaz` 要一维）；`get_dtec.get_dtec_from_skycoord/altaz` 同参。

| `iono_kwargs`（ionex / ionex_iri） | 代码默认（2.0） | 说明 |
| --- | --- | --- |
| `server` | **`chapman`**（文档写 cddis） | `cddis`（要 `~/.netrc`）、`chapman`（UPC http）、`igsiono`（ftp） |
| `prefix` | **`uqr`**（文档写 cod） | `cod esa igs jpl upc irt uqr` |
| `url_stem` | None | 覆盖服务器根地址 |
| `time_resolution` | None → cod 1 h、uqr 15 min、其余 2 h | 只影响拼文件名 |
| `solution` | `final` | `final` / `rapid` |
| `output_directory` | `./ionex_files` | 同名文件存在即跳过下载 |
| `height` | 450 km（日志显示） | 只在 `height_array` 多层时选最近层；单层时**无效**（坑 6） |
| `remove_midnight_jumps` | True | 读当天 + 次日文件以去掉日界跳变 |
| `apply_earth_rotation` | 1 | 相邻图间经度按自转对齐；0 关，可小数 |
| `correct_uqrg_rms` | True | 缩小 UQRG 偏大的 RMS |

| `RM` 字段 | 形状（本例） | 单位 / 含义 |
| --- | --- | --- |
| `rm`, `rm_error` | (8,) | rad/m²；误差 = GIM RMS 与 IGRF RMS 的相对误差之和 × |rm| |
| `b_parallel`, `b_parallel_error` | (8, n层) | nT，视线方向投影（带符号） |
| `electron_density`, `…_error` | (8, n层) | **每层 VTEC 份额**（TECU），不是 STEC |
| `height` | (8, n层) | IPP 离地高度 km |
| `azimuth`, `elevation` | (8,) | 度 |
| `times`, `loc` | — | astropy `Time` / `EarthLocation` |

`DTEC` 多一个 `airmass`（8, n层）：STEC = Σ `electron_density × airmass`。模型：`ionex`、`ionex_iri`、`tomion`（UPC 两层层析，70 层 110–1400 km）、`tomion_dual`（实验）；磁场模型只有 `ppigrf`。

## 6. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `spinifex -h` 报 `ImportError: casacore is not installed! To operate on MeasurementSets, install spinifex[casacore].` | CLI 在 import 时就要 casacore | `pip install --no-cache-dir "spinifex[casacore]"`（或只用 Python API） |
| 2 | 找不到“按站点+时间算 RM”的命令行 | CLI 只有 MS→H5Parm 与 FITS 改正 | 用 API：`python -u rm_lofar.py` |
| 3 | `server='cddis'` 报 `FileNotFoundError: Please add your NASA Earthdata login credentials to ~/.netrc` | CDDIS 需登录；本机还被挡 | 先从 AIUB 下同名文件到 `output_directory`：`curl -sfL -O --output-dir ionex_files https://www.aiub.unibe.ch/download/CODE/2024/COD0OPSFIN_20242350000_01D_01H_GIM.INX.gz` |
| 4 | 不传参数时实际下载的是 `uqrg…i.Z`（UPC），与文档“默认 cddis/cod”不符 | 2.0 代码默认 `server=chapman, prefix=uqr` | 显式写：`get_rm_from_skycoord(..., prefix="cod", server="cddis", output_directory="ionex_files")` |
| 5 | 只放了当天文件，仍去 CDDIS 要次日文件并报 netrc 错 | `remove_midnight_jumps=True` 要读次日 | 下次日文件，或加 `remove_midnight_jumps=False`（本机只放 DOY 235 时 12:00 RM=1.61117527，与 §3 有次日文件时的 1.6112 一致；日界附近才会有差） |
| 6 | 改 `height=350*u.km` 结果不变（12:00 仍 1.61117527） | 公开函数用模块常量 `DEFAULT_IONO_HEIGHT=[450] km` 作为唯一层，`height` 只在多层里挑最近 | 调用前改常量：`get_rm.DEFAULT_IONO_HEIGHT = np.array([350.]) * u.km`（本机 12:00 RM 变 1.44861521） |
| 7 | 把 `electron_density` 当视线 TEC，低仰角差一倍（12:00：31.17 vs 61.94） | 它是每层 VTEC 份额 | `stec = (d.electron_density * d.airmass).sum(axis=1)` |
| 8 | `ipp.lat.deg` 报 `AttributeError: 'Quantity' object has no 'deg' member` | IPP 的 lat/lon 是 `Quantity` 不是 `Latitude` | `ipp.lat.to_value(u.deg)` |
| 9 | 参数拼错直接 `TypeError: Incorrect arguments {… 'heigth': 400} for ionospheric model …` | kwargs 严格校验（pydantic） | 对照 §5 表：`python -c "from spinifex.ionospheric.models import *; print(parse_iono_kwargs(parse_iono_model('ionex')))"` |
| 10 | 低仰角 RM 看起来偏大 | 单层把高空电子放在 450 km 的强磁场处 | 换剖面模型：`iono_model_name="ionex_iri"`（本例 12:00 RM −18%） |

## 7. 怎么读结果

- 符号按 spinifex 自己的约定：`rm = −2.62e−6·Σ(nₑ·B∥·airmass)`，本例 B∥ 全为负、RM 全为正（0.83–1.79 rad/m²）。和 RMextract 或其他软件比数之前，先核对 B∥ 视线方向与 RM 的符号约定。
- 偏振角改正：`Δχ = RM·λ²`；150 MHz（λ=2 m）时 RM=1.6 rad/m² 相当于 6.4 rad，已经转了一圈多，所以低频偏振必须改正。
- `rm_error` 只含 GIM RMS 与 IGRF 标称 RMS，不含 GIM 系统误差与单层模型误差；§3 的 CODE vs UQRG 差（最大 0.17）和 §4 的单层 vs IRI 差（最大 0.29）都比它大，写论文时应把模型间差当误差下限。
- 精度链条：RM 的 TEC 部分完全来自 GIM → GIM 如何生成与比较见 [ionex](./ionex.md)、[ionex-gim](./ionex-gim.md)、教程 [03 GIM/IONEX](../tutorials/03-gim-ionex.md)、[18 GIM 对比实验](../tutorials/18-lab-compare-gims.md)；IRI 剖面见 [pyiri](./pyiri.md)。
- 本仓库**没有** `igrf.md`；IGRF 由 ppigrf 自带系数文件（`IGRF14.shc`，另附 `IGRF13.shc`）提供，逐日计算，不需要网络。

## 8. 许可与诚实局限

- Apache-2.0（Copyright 2025 ASTRON & CSIRO）；pyproject 标 “Development Status :: 3 - Alpha”。
- 只测了 1 个站（近似坐标）、1 个源、1 天、`ionex`/`ionex_iri` 两个模型、CODE/UQRG 两套 GIM；`tomion`、MS/FITS CLI、H5Parm 输出未测。没有偏振观测真值，RM 绝对精度未验证。
- 与 RMextract 的数值对比（上游有 notebook）未复跑。
- CDDIS（上游最推荐的归档）本机不可达，只能手工放文件；`chapman` 走明文 http。
- 本机速度：8 个时刻单层 RM + dTEC 共 2–5 s（本地文件；两次实测 2.1 / 4.4 s），UQRG 需下载时 8.5 s。
