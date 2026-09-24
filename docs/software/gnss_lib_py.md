# gnss_lib_py · Stanford NAV Lab GNSS 解析/分析操作手册

目录：[`PROJECTS.json` → `gnss_lib_py`](../../PROJECTS.json) · 上游 <https://github.com/Stanford-NavLab/gnss_lib_py> · 许可 **MIT** · PyPI **`gnss-lib-py` 1.1.0** · 本机验证：`RinexObs` 读仓内混合 OBS → **126** 测值 / **5** 历元；`RinexNav` + `AndroidDerived2023` 冒烟（2026-09-24 EDT） · **质检复跑通过**（同 I/O）

> 岗位：把 Android/原始测量、RINEX、SP3/CLK 等收进统一 **`NavData`**，再跑快照 WLS、残差、可视化。冲突时：**仓内 README / ReadTheDocs > 本文**。

## 1. 用途与边界

**做：**

- `NavData`：行=字段、列=单星单频测值；可读如 pandas、算如 ndarray
- 解析：`RinexObs` / `RinexNav` / `Clk` / `Sp3` / NMEA / Android raw / Google Decimeter 2021–2023
- 算法：`solve_wls` 快照加权最小二乘；残差、FDE、简易滤波
- 工具：时间转换、坐标、DOP、`add_sv_states_rinex` / 精密星历挂接
- 可视化：metric / skyplot / map（plotly；静态导出依赖 kaleido）

**不做：**

- **不是** 发表级 PPP-AR / 工业 CLI 事后定位 → [pride-pppar](./pride-pppar.md) / [rtklib](./rtklib.md)
- **不是** 开放 SSR/HAS PPP 试验箱 → [cssrlib](./cssrlib.md)；HAS 解码 → [haslib](./haslib.md)
- **不是** 校准 TEC / ROTI 产品 → [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md) / [oasis-roti](./oasis-roti.md)
- RINEX 底层读盘走 **georinex**（包装钉 `georinex<=1.16.1`）；只想 xarray 探活 → [georinex](./georinex.md)
- 另一条轻量「伪距+星历→自写估计」→ [laika](./laika.md)；手机 GnssLogger→RINEX → [android_rinex](./android_rinex.md)

一句话：gnss_lib_py = **Stanford NAV Lab 模块化 Python GNSS 测量/状态估计工具箱**（手机定位与算法课强）。

| 术语 | 含义 |
| --- | --- |
| `NavData` | 统一表；`shape=(n_rows, n_cols)`，**列=一条测值** |
| `gps_millis` | GPS 时标（ms）；`loop_time` 按此时分组 |
| `raw_pr_m` / `cn0_dbhz` | 原始伪距 (m) / 载噪比 (dB-Hz) |
| `gnss_sv_id` / `signal_type` | 如 `G02`；`l1`/`l5`/`e1`/`e5a`/`g1`… |
| `x_sv_m`… | 卫星 ECEF；**WLS 必需**（仅 OBS 没有） |
| `solve_wls` | 每历元 WLS → 接收机状态行 |

## 2. 安装

PyPI 包名是连字符 **`gnss-lib-py`**；`import gnss_lib_py`。Python **≥3.10,<3.15**（本机 3.13 可 import）。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/Stanford-NavLab/gnss_lib_py.git
cd gnss_lib_py
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
# 或：pip install 'gnss-lib-py==1.1.0'
python -c "import gnss_lib_py as glp; print(glp.__version__)"
# 期望：1.1.0
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'gnss_lib_py'` | 装了错名 / 未进 venv | `pip install gnss-lib-py`；`source .venv` |
| `georinex` 冲突 | 上游钉 `<=1.16.1` | 本 venv 专装；科学分析另开环境 |
| kaleido / plotly 写 PNG 失败 | 可选可视化链 | `pip install kaleido==0.2.1` |

## 3. 端到端：RINEX OBS → NavData（本机真跑）

样本：仓内 `data/unit_test/rinex/obs/rinex_obs_mixed_types.20o`（RINEX 3，多系统多频；2020-05-21）。

### 3.1 解析 + 首历元

把下面脚本存为 `/tmp/glp_e2e.py` 后执行（避免交互 heredoc 转义问题）：

```bash
cd ~/iono_ops/gnss_lib_py && source .venv/bin/activate
python /tmp/glp_e2e.py
```

`/tmp/glp_e2e.py` 内容：

```python
import gnss_lib_py as glp
from gnss_lib_py.parsers.rinex_obs import RinexObs
from gnss_lib_py.parsers.rinex_nav import RinexNav
from gnss_lib_py.parsers.google_decimeter import AndroidDerived2023
from gnss_lib_py.navdata.operations import loop_time
import numpy as np

obs = RinexObs("data/unit_test/rinex/obs/rinex_obs_mixed_types.20o")
print("version", glp.__version__)
print("obs_shape", obs.shape)
print("rows", obs.rows)
print("n_meas", len(obs), "n_epochs",
      len(np.unique(np.atleast_1d(obs["gps_millis"]))))
print("gnss", sorted({str(x) for x in np.atleast_1d(obs["gnss_id"])}))
print("signals", sorted({str(x) for x in np.atleast_1d(obs["signal_type"])}))

for timestamp, delta_t, epoch in loop_time(obs, "gps_millis", delta_t_decimals=-2):
    pr = np.atleast_1d(epoch["raw_pr_m"])
    cn0 = np.atleast_1d(epoch["cn0_dbhz"])
    svs = sorted({str(x) for x in np.atleast_1d(epoch["gnss_sv_id"])})
    print(f"first_epoch_gps_millis={int(timestamp)} delta_t={delta_t}")
    print(f"first_epoch_n_meas={len(epoch)} "
          f"pr_min_m={float(np.nanmin(pr)):.3f} "
          f"pr_max_m={float(np.nanmax(pr)):.3f}")
    print(f"first_epoch_cn0_median_dbhz={float(np.nanmedian(cn0)):.2f}")
    print(f"first_epoch_svs={svs}")
    break

pdf = obs.pandas_df()
row = pdf[(pdf.gnss_sv_id == "G02") & (pdf.signal_type == "l1")].iloc[0]
print(f"G02_l1_raw_pr_m={row.raw_pr_m:.5f}")

nav = RinexNav("data/unit_test/rinex/nav/brdc1370.20n")
print("nav_shape", nav.shape, "n_eph", len(nav))

d = AndroidDerived2023(
    "data/unit_test/google_decimeter_2023/"
    "2023-09-07-18-59-us-ca/pixel7pro/device_gnss.csv")
print("android2023_shape", d.shape, "n", len(d))
```

**本机 stdout（2026-09-24 EDT，`gnss-lib-py` 1.1.0）：**

```text
version 1.1.0
obs_shape (10, 126)
rows ['gps_millis', 'gnss_sv_id', 'sv_id', 'gnss_id', 'raw_pr_m', 'carrier_phase', 'raw_doppler_hz', 'cn0_dbhz', 'signal_type', 'observation_code']
n_meas 126 n_epochs 5
gnss ['galileo', 'glonass', 'gps']
signals ['e1', 'e5a', 'g1', 'l1', 'l5']
first_epoch_gps_millis=1274131358443 delta_t=0
first_epoch_n_meas=25 pr_min_m=19233432.043 pr_max_m=25211384.493
first_epoch_cn0_median_dbhz=28.50
first_epoch_svs=['E13', 'E15', 'E21', 'E27', 'E30', 'G02', 'G05', 'G06', 'G12', 'G19', 'G24', 'G25', 'G29', 'R10', 'R11', 'R12', 'R21', 'R22']
G02_l1_raw_pr_m=20832141.28000
nav_shape (36, 6) n_eph 6
android2023_shape (60, 180) n 180
```

| 字段 | 含义 |
| --- | --- |
| `obs_shape (10, 126)` | 10 行字段 × 126 列测值 |
| `n_epochs` | 唯一 `gps_millis`（本文件 5） |
| `first_epoch_n_meas` | 首历元列数（多频→同星多列） |
| `G02_l1_raw_pr_m` | 单测参考 ≈20832141.28024（打印 5 位） |
| `nav_shape (36, 6)` | 广播星历 6 条 × 36 参数行 |
| `android2023_shape` | Decimeter 2023 derived → NavData |

### 3.2 定位链提示（本机未出解）

直接 `solve_wls(obs)` → `KeyError: 'x_sv_m', 'y_sv_m', 'z_sv_m' row(s) are missing`。需先挂星历：

```bash
# ephemeris_path 必须是「目录」；NAV 日期须覆盖 OBS
# glp.add_sv_states_rinex(obs, ephemeris_path='path/to/nav_dir')
# glp.solve_wls(obs_with_sv)
```

本机对混合 OBS（2020-05-21 / doy 142）配仓内 `brdc1370.20n`（doy 137）→ 星历覆盖失败。把**文件**路径当 `ephemeris_path` → `NotADirectoryError: .../brdc1370.20n/rinex`。换同日 BRDC **目录**后再跑 WLS。

### 3.3 关键 API

| 符号 | 作用 |
| --- | --- |
| `RinexObs(path)` | RINEX OBS → NavData（内经 georinex） |
| `RinexNav(path)` | 广播星历 → NavData |
| `AndroidDerived2021/22/23(csv)` | Google 挑战 derived |
| `loop_time(nd, "gps_millis")` | yield `(t, Δt, epoch)` |
| `add_sv_states_rinex(nd, ephemeris_path=dir)` | 挂广播卫星位置 |
| `solve_wls(nd)` | 历元 WLS |
| `nd.pandas_df()` / `nd.rows` / `len(nd)` | 导出与尺寸 |

## 4. 接到哪步

- 手机 / 算法课原型 → 本文；要 RTK/PPP 产品 → [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md) / [pride-pppar](./pride-pppar.md)
- 仅 RINEX→xarray → [georinex](./georinex.md)；Hatanaka → [hatanaka](./hatanaka.md) / [rnxcmp](./rnxcmp.md)
- 另一条轻量 Python 观测链 → [laika](./laika.md)；GnssLogger CSV → [android_rinex](./android_rinex.md)
- 教程 [06](../tutorials/06-iono-positioning.md)；数据 [data-access](../data-access.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `pip install gnss_lib_py` 找不到 | PyPI 名是连字符 | `pip install gnss-lib-py` |
| 2 | `ValueError: too many values to unpack (expected 2)` | `loop_time` 产 **3** 元组 | `for t, dt, epoch in loop_time(...)` |
| 3 | `KeyError: 'x_sv_m', 'y_sv_m', 'z_sv_m' … missing` | OBS 无卫星位置 | `add_sv_states_rinex` 后再 `solve_wls` |
| 4 | `NotADirectoryError: .../brdc….20n/rinex` | `ephemeris_path` 给了**文件** | 传 **目录**；把 NAV 放进该目录 |
| 5 | 星历覆盖失败 / 缺星 | NAV 日期或星不覆盖 OBS | 换同日 BRDC；或多文件放同一目录 |
| 6 | 当 PPP/RTK 引擎 | 能力是快照 WLS + 教具滤波 | 换 [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) |
| 7 | `georinex` API/结果怪 | 被钉在 ≤1.16.1 | 另开 venv 用新版做科学分析 |
| 8 | plotly 写 PNG 失败 | kaleido 未装或版本漂 | `pip install kaleido==0.2.1` |
| 9 | `len(obs)` 与「历元数」混淆 | `len`=列数=测值数 | 历元用 `unique(gps_millis)` / `loop_time` |
| 10 | Android 2021/22 CSV 用错类 | 年别 schema 不同 | 2023 用 `AndroidDerived2023` |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 模块化 NavData + 手机/RINEX 算法原型 | **本文 gnss_lib_py** |
| RINEX→xarray | [georinex](./georinex.md) |
| 轻量伪距处理 / Earthdata 星历狗 | [laika](./laika.md) |
| CLI RTK/PPP | [rtklib](./rtklib.md) |
| 手机 GnssLogger→RINEX | [android_rinex](./android_rinex.md) |

- 文档：<https://gnss-lib-py.readthedocs.io/>
- 笔记本：<https://github.com/Stanford-NavLab/gnss_lib_py/tree/main/notebooks/tutorials>
- 兄弟：[georinex](./georinex.md) · [laika](./laika.md) · [android_rinex](./android_rinex.md) · [rtklib](./rtklib.md) · [cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [hatanaka](./hatanaka.md) · [data-access](../data-access.md)
