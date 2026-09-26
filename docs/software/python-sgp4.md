# python-sgp4 · Python SGP4/SDP4 TLE/OMM 轨道传播操作手册

目录：`PROJECTS.json` **`python-sgp4`**（orbit-clock / SGP4传播）· 上游 <https://github.com/brandon-rhodes/python-sgp4> · PyPI **`sgp4` 2.27**（2026-07-03 发布；master **`8126f77`**，2026-09-24 08:58 EDT）· **MIT** · ★**472** · 本机 Python **3.13.5**，`sgp4.api.accelerated == True`（Vallado C++ 扩展 `vallado_cpp.abi3.so`）· 真跑 2026-09-26 02:09–02:30 EDT

> 岗位：把 **TLE / OMM 平均根数** 传播成某 UTC 时刻的 **TEME** 位置（km）/速度（km/s）。精度是 **km 级**（GPS 实测中位 ~1.7 km，见 §3.4），**不是**精密轨道。冲突时：**上游 README / `help(Satrec)` > 本文**。
> 姊妹篇：[satellite-js](./satellite-js.md)（同一 Vallado 算法的 JS/TS 版，§3.2 实测差 ≤ 1.7 cm）。精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [gnssanalysis](./gnssanalysis.md) / [sp3](./sp3.md)。数值积分外推：[gmat](./gmat.md)。

## 1. 用途与边界

**做：** `Satrec.twoline2rv(l1, l2)` / `sgp4.omm.initialize()` 读根数 → `sat.sgp4(jd, fr)` 或 `sat.sgp4_tsince(min)` 得 `(err, r, v)`；`SatrecArray` 多星×多时刻向量化；`sgp4.exporter` 回写 TLE/OMM；自带官方 `tcppver.out` 校验。

**不做：**

- **不做坐标转换**：输出只有 TEME（真赤道/平春分点）。要 ITRF/ECEF、经纬高、仰角 → astropy `TEME→ITRS` 或 skyfield（§3.4）
- **不拉 TLE**：自己从 CelesTrak GP API / Space-Track 下
- **不是精密星历**：GNSS 定位/PPP 用 SP3 或广播星历，勿用 TLE
- **不管 GPST/UTC**：输入一律 UTC；和 SP3（GPST）比时要 −18 s（§3.4 实测忘了 = 53 km）

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `sgp4`（PyPI） | 纯传播库，TEME 输出 | `from sgp4.api import Satrec` |
| skyfield `EarthSatellite` | 内部调用本库 + 帧转换/可见性 | `sat.at(t).frame_xyz(itrs)` |
| [satellite-js](./satellite-js.md) | JS 版，带 `eciToEcf`（仅 GMST 旋转） | `import * as satellite` |
| 广播星历 / SP3 | GNSS 精密/准精密轨道 | RINEX NAV / `*.SP3` |

## 2. 安装

```bash
python3 -m venv venv && . venv/bin/activate
pip install sgp4 astropy skyfield numpy     # 本机：sgp4 2.27 / astropy 8.0.1 / skyfield 1.55
python -c "import sgp4; from sgp4.api import accelerated; print(sgp4.__version__, accelerated)"
# 2.27 True        ← False 表示回落纯 Python（sgp4/model.py 的 Satrec/SatrecArray，接口相同但慢）
```

## 3. 真命令 + 实测输出（2026-09-26 EDT）

### 3.1 拉 TLE/OMM（记录抓取时刻）

```bash
date '+%F %T %Z'   # 2026-09-26 02:09:18 EDT
curl -s 'https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle'  -o gps-ops.tle   # 96 行 = 32 星
curl -s 'https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle'    -o iss.tle
curl -s 'https://celestrak.org/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=json' -o gps-ops.json  # OMM
```

| 星 | TLE 历元（字段） | = UTC | = ET |
| --- | --- | --- | --- |
| ISS (ZARYA) 25544 | `26268.43198945` | 2026-09-25 10:22:03.888 | 06:22:04 EDT |
| GPS BIIR-13 (PRN 02) 28474 | `26268.06454359` | 2026-09-25 01:32:56.566 | 09-24 21:32:57 EDT |

gps-ops 32 星历元跨度 `26260.32`（PRN 21）… `26268.90`（PRN 27）——**同一组 TLE 新旧差 8 天**，先看历元再用。

### 3.2 传播 + 与 satellite-js 交叉

```python
from sgp4.api import Satrec, jday
s = Satrec.twoline2rv(l1, l2)              # 默认 WGS72 + opsmode 'i'（与 CelesTrak/Space-Track 一致）
jd, fr = jday(2026, 9, 26, 0, 0, 0.0)      # UTC；返回整数 .5 日 + 日内分数
e, r, v = s.sgp4(jd, fr)                   # e=0 正常；r km（TEME）；v km/s
```

实测（`e` 全为 0；r km / v km/s，TEME）：

```
ISS  2026-09-26T00:00Z   -949.485596  4511.500075 -5001.757253  -7.322557177 0.764630116  2.076133336
ISS  2026-09-27T00:00Z    688.165467 -4592.529188  4953.048799   7.228249664 -1.288068475 -2.198008435
PRN02 2026-09-26T00:00Z 18021.574980 -18486.667125 -4235.878206  2.017883433 1.198689134  3.155333530
PRN02 2026-09-26T06:00Z -18241.277918 19245.665147  4873.354746 -1.977397925 -1.143054481 -3.057086236
```

同时刻 satellite.js 7.1.0 `propagate(satrec, Date)`：ISS |dr| = **5.07–5.08 mm**、PRN02 |dr| = **16.6–17.1 mm**，|dv| ≤ **5.7e-6 m/s**。根因已查实：本库把历元拆成 `jdsatepoch=2461308.5` + `jdsatepochF=0.06454359`，JS 存单个 double `2461308.56454359`，tsince 差 **7.26e-8 min（4.4 µs）**；把本库 tsince `1347.0572304` 直接喂 `satellite.sgp4()` → 位置**逐位相同**。结论：两库算法一致，差异全在时间表示。

### 3.3 自带校验向量

```bash
python -m sgp4.tests            # Ran 45 tests in 0.087s  OK
python -m sgp4.tests -v 2>&1 | grep tcppver
# test_legacy_against_tcppver ... ok
# test_satrec_against_tcppver_using_julian_dates ... ok
# test_satrec_against_tcppver_using_tsince ... ok
```

包内带 `SGP4-VER.TLE`（33 组 TLE）+ `tcppver.out`（700 行，Vallado 官方 C++ 输出），三路比对全过。

### 3.4 对 IGS SP3 的精度（本人比对，非上游数字）

- 精密参考：BKG 公开镜像（免登录）`https://igs.bkg.bund.de/root_ftp/IGS/products/2437/`：`IGS0OPSULT_20262680000_02D_15M_ORB.SP3.gz`（2026-09-25 起 48 h，取前 24 h 观测段，96 历元）+ `IGS0OPSRAP_20262670000_01D_15M_ORB.SP3.gz`（09-24 快速）。CDDIS 需 Earthdata，未用。
- 流程：SP3 历元（GPST）**−18 s → UTC** → `SatrecArray.sgp4` 得 TEME → **astropy 8.0.1** `TEME(...).transform_to(ITRS(obstime))`（IERS-A 自动下载，含 UT1−UTC 与极移）→ 与 SP3（IGS20/ITRF，km）逐历元求 3D 差。

```
IGS ULT 2026-09-25 00:00 GPST +24h  epochs=96  PRN02 (TLE 26268.06454)
  3D km: mean=0.534 rms=0.551 min=0.316 max=0.828
  RMS R/T/N km: 0.212 / 0.413 / 0.298
  WRONG [no GPST->UTC (leap=0)]     : 3D mean=53.489  max=57.897 km
  WRONG [TEME used as ECEF]         : 3D mean=26974.176 max=52133.889 km
IGS RAP 2026-09-24（TLE 反推 ~1 d） PRN02: mean=0.456 rms=0.463 max=0.593 km
全星（ULT，31 星；G15 该 ULT 无记录）: mean3D 中位 1.658 km，最小 0.302（G03），常见 0.3–5 km
  异常：G13 GPS BIII-10（TLE 26264.30，已 4.7 d）mean=469.6 km；RAP 日 32 星中位 1.710 km、最大 420.9 km
```

G13 用全部 32 组 TLE 反查，最近的仍是 BIII-10（463 km），说明 PRN 对应无误、是该 TLE 本身不贴合（新星/机动的可能性未核实）。

帧转换交叉：同一 TEME 点（PRN02，2026-09-25 12:00 UTC），skyfield 默认 `load.timescale()` 与 astropy 差 **210 m**（skyfield 内置表外推 dUT1=+0.0956 s，astropy IERS-A −0.0142 s）；换 `timescale(builtin=False)` 拉 finals2000A 后差 **46.6 m**（skyfield `itrs` 未装极移）；再 `iers.install_polar_motion_table` 后差 **2.5 m**（两边 dUT1 差 1.4 ms）。对 km 级 SGP4 误差都可忽略，但做 m 级工作时必须知道。

## 4. I/O 字段

| 项 | 说明 |
| --- | --- |
| 输入 TLE | 69 列两行；`twoline2rv` **不校验 checksum**（改错末位仍解析，实测） |
| 输入 OMM | CelesTrak `FORMAT=json/xml/csv`；`sgp4.omm.initialize(Satrec(), dict)`；字段 `EPOCH` `MEAN_MOTION`(rev/d) `ECCENTRICITY` `INCLINATION`(deg) `BSTAR` … |
| 时间 | `jday(Y,M,D,h,m,s)` → `(jd, fr)` UTC；或 `sgp4_tsince(分钟)` 相对历元 |
| 输出 `e` | 0 正常；1 平均偏心率越界；2 平均运动<0；3 摄动偏心率越界；4 半通径<0；6 已衰减（mrt<1）。文本见 `sgp4.api.SGP4_ERRORS` |
| 输出 `r` / `v` | TEME，km / km/s（**不是** ECEF） |
| Satrec 属性 | 弧度与 rad/min：`inclo` 0.96117 rad、`no_kozai` 0.00875109 rad/min（PRN02 实测）；`a` 以地球半径计（4.1643 ER） |
| `SatrecArray.sgp4(jd[], fr[])` | 返回 `e (nsat,nt)`、`r (nsat,nt,3)`、`v (nsat,nt,3)` |

## 5. 参数

| 参数 | 默认 | 说明 |
| --- | --- | --- |
| `whichconst` | `WGS72` | 与 TLE 生成方一致；换 `WGS84` 会引入额外误差 |
| `opsmode` | `'i'` | 改进模式；`'a'` 为 AFSPC 兼容（校验用例用） |
| `jd, fr` 拆分 | — | 传 `(jd, fr)` 而非 `jd+fr`：12:34:56.789 时刻合并后 PRN02 差 **4.3 cm**（实测） |
| `exporter.export_tle / export_omm` | — | ISS 回写 TLE 与原文仅 checksum/`00000-0` 格式差，OMM `EPOCH 2026-09-25T10:22:03.888479` |

## 6. 接到哪步

CelesTrak/Space-Track 根数 →（本库）TEME → astropy/skyfield 转 ITRS → 仰角/可见窗口、LEO 掩星/IPP 粗几何、GNSS 星空图、TLE 质量监控 → 需要 m/cm 级改走 [data-access](../data-access.md#sp3--clk--bias) 下 SP3 → [gnssanalysis](./gnssanalysis.md) 比较、[sp3](./sp3.md) 插值；需力学模型外推 → [gmat](./gmat.md)。前端展示 → [satellite-js](./satellite-js.md)。

## 7. 坑（均实测）

1. **TEME ≠ ECEF**：把 TEME 当 ECEF 与 SP3 比，PRN02 平均差 **26974 km**。必须 `TEME→ITRS`。
2. **GPST vs UTC**：SP3 历元是 GPST，不减 18 s 直接当 UTC → **53.5 km**（GPS 3.9 km/s × 18 s ≈ 70 km 量级）。
3. **错误不抛异常**：截断 TLE → `Satrec` 静默给 `error=2`、`no_kozai=0`，`sgp4()` 返回 `(2, (nan,nan,nan), …)`；老接口 `sgp4.io.twoline2rv` 才 `ValueError: TLE format error`。**每次检查 `e`**。
4. **衰减码 6 仍给出坐标**：ISS TLE 外推 +5 年 → `e=6 "mrt is less than 1.0 … decayed"`，但 `r=[4619.1,-2794.5,3262.1]` 不是 NaN；+3 年仍 `e=0`（结果已无物理意义）。按 `e` 过滤，别按 NaN 过滤。
5. **jd/fr 精度**：`sgp4(jd+fr, 0)` 丢精度（实测 4.3 cm）；TLE 历元本身只有 8 位小数（≈0.86 ms）。
6. **OMM ≠ TLE 逐位**：PRN02 JSON `ECCENTRICITY 0.01725844` 比 TLE 多一位 → 同时刻差 **1.39 m**（satellite.js 1.91 m）。混用两种源做差分会看到伪信号。
7. **单位**：内部角度全是弧度、平均运动 rad/min；TLE 里是度与 rev/day。自己改 `Satrec` 字段必须换算。
8. **TLE 老化/机动**：同组 GPS TLE 历元差 8 天；G13 实测 470 km、G21（TLE 已 7.7 d）5.1 km。先看 `epochdays` 和年龄。
9. **skyfield 默认 IERS 表过期**：`load.timescale()` 内置 dUT1 外推 → 210 m；要 `builtin=False` + 装极移表。astropy 在 cwd 发现 `finals2000A.all` 会优先读并告警 `AstropyDeprecationWarning`——把 skyfield 数据放子目录（`Loader('skydata')`）。
10. **SatrecArray 只有 C 扩展才快**：`accelerated=False` 时回落 `sgp4/model.py` 纯 Python 版（接口同、无向量化加速）；本机 C 版 32 星×10080 分钟 = 322560 状态 **181 ms**（逐个循环 245 ms），收益随规模增长。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| Python 批量 TLE 传播、可见性 | **本库** + astropy/skyfield |
| 要现成仰角/过境/星下点 | skyfield（内部即本库） |
| 浏览器 / Node 可视化 | [satellite-js](./satellite-js.md) |
| Rust 服务 / no_std | [sgp4-rs](./sgp4-rs.md)（WGS72 配置下与本库差 ≤ 9 µm） |
| m/cm 级 GNSS 轨道 | SP3 → [gnssanalysis](./gnssanalysis.md) / [sp3](./sp3.md) |
| 带摄动力模型的定轨/外推 | [gmat](./gmat.md)（或 Orekit） |
| 可微分/ML 管线 | dSGP4（`PROJECTS.json` 有登记，本库无梯度） |
