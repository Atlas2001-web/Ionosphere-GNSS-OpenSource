# ocbpy · 极盖边界（OCB）自适应磁坐标转换 操作手册

目录：[`PROJECTS.json` → `ocbpy`](../../PROJECTS.json) · 上游 <https://github.com/aburrell/ocbpy> · 文档 <https://ocbpy.readthedocs.io/> · PyPI **0.7.0**（main HEAD `3ced0de`）· 依赖 aacgmv2 2.7.1 + numpy · 许可 **BSD-3-Clause**（© 2017 Angeline G. Burrell、Gareth Chisham）· 本机实跑 2026-09-26 06:07–06:10 EDT（CPython 3.13.5，venv，numpy 2.2.6）

> **质检复跑通过（2026-09-26 06:20–06:30 EDT）**：ocbpy 0.7.0 + aacgmv2 2.7.1，numpy 2.4.6。§3.1–3.3 输出逐字一致，AMPERE 对象建立用时 40.5 s。`files.py` 里 AMPERE 结束时间写死为 2022-01-01，而 `amp_north/south_radii.ocb` 实际到 `20241031 23:58`（3514320 / 3646800 行），属实。坑 5、6、8 的修复命令实跑都有效：pickle 290 KB、读回瞬时；装上 zenodo-get 3.1.0 后提示消失；`circular` 让 `r_corr` 为 0、边界降约 2°。坑 8 原来写的 “AMPERE 与 IMAGE 同刻比” 不成立（两者没有重叠时段），已改写。坑 1 的提示文字、坑 7 的 54.378 出处按实测修正。
>
> 岗位：给定某一时刻的极盖边界圆（来自 IMAGE 紫外成像或 AMPERE 场向电流），把 AACGM 磁纬/MLT 换成"相对这条边界"的 OCB 纬度/MLT，并把速度、电场这类矢量按边界大小缩放。这样不同时刻、不同暴强度下的高纬观测可以叠在一起统计。冲突时：**本机 `ocbpy/_boundary.py`、`ocb_scaling.py` 文档串 > 本文**。

## 1. 它解决什么 / 不做什么

极盖（开放磁力线区）的大小一直在变：本页 §3.2 同一天的 AMPERE 边界，在午夜 MLT 从平静时的 AACGM 69.1° 退到暴时的 58.1°。固定 AACGM 纬度统计时，"75° 午夜"有时在极光椭圆里，有时在极盖深处，物理过程完全不同。ocbpy 把每个点映射到"边界永远在 OCB 纬度 74°"的坐标系里，消掉这种错位。

对 GNSS 电离层的意义：高纬相位闪烁、ROTI 增强主要出现在极光椭圆边缘、午后/日侧尖角区和从日侧漂进极盖的等离子体斑块（patch）里，位置都跟着边界走。按 OCB 坐标归档闪烁台站数据，比按地理或 AACGM 纬度分箱更容易看出"边界内/外"的差别。

**做：**

- `OCBoundary(filename, instrument, hemisphere, stime, etime)`：读 IMAGE（`*_circle.ocb`）、AMPERE（`amp_*_radii.ocb`）、DMSP-SSJ 边界文件；按 `fom`（优度）过滤
- `normal_coord(lat, mlt)` → `(ocb_lat, ocb_mlt, r_corr)`；`revert_coord` 反算回 AACGM
- `ocb_scaling.VectorData(...).set_ocb(ocb)`：矢量旋转 + 按 `scaled_r/unscaled_r` 缩放
- 包里自带边界文件：IMAGE 北半球 2000-05…2002-11，AMPERE 南北半球 2010-01…**2024-10-31**（本机 `tail` 看到的最后一行）

**不做：**

- 不算边界本身（边界来自 Chisham、Milan 等人发布的拟合）；不读 SuperDARN/GNSS 原始数据
- 不是 AACGM 库：地理→AACGM 由 [aacgmv2](./aacgmv2.md) 完成（`coords='geodetic'` 时内部调用）

| 相邻页面 | 关系 |
| --- | --- |
| [lompe](./lompe.md) | 极区局地电动力学反演；输出的对流速度可以再用本页转到 OCB 坐标做统计 |
| [pydarn](./pydarn.md) / [superdarn-data](./superdarn-data.md) | SuperDARN 视线速度来源；`ocbpy.instruments.vort` 读 SuperDARN 涡度文件（未实跑） |
| [aacgmv2](./aacgmv2.md) / [apexpy](./apexpy.md) | 底层磁坐标 |
| [pysatspaceweather](./pysatspaceweather.md) | 同一场 2024-05-10 暴的 Kp（15 UT 起 ≥ 7.67） |

## 2. 安装

```bash
python3 -m venv venv && . venv/bin/activate
pip install --no-cache-dir ocbpy        # 装上 ocbpy 0.7.0 + aacgmv2 2.7.1（aacgmv2 有 manylinux 轮子，免编译）
```

每次 `import ocbpy` 会打印 `unable to load \`zenodo_get\` module; avalable from PyPi.`，只影响 DMSP-SSJ 边界下载（坑 6），其余功能照常。

## 3. 端到端

脚本 `ocb1.py`，`HOME=$PWD/home python -u ocb1.py`，整脚本 41.5 s（大头是读 AMPERE 文件，坑 5）。

### 3.1 包内测试边界（IMAGE 格式）→ OCB 坐标

```python
import os, numpy as np, ocbpy
tfile = os.path.join(os.path.dirname(ocbpy.__file__), 'tests', 'test_data', 'test_north_ocb')
t = ocbpy.OCBoundary(filename=tfile, instrument='image', hemisphere=1)
print(t)
t.get_next_good_ocb_ind()            # 跳到第一条通过 fom 过滤的记录
olat, omlt, rc = t.normal_coord(np.array([75., 80., 70., 85.]), np.array([22., 12., 6., 0.]))
```

真实输出：

```
OCBoundary file: .../ocbpy/tests/test_data/test_north_ocb
Source instrument: IMAGE
Boundary reference latitude: 74.0 degrees

75 records from 2000-05-05 11:35:27 to 2000-05-09 11:33:22

YYYY-MM-DD HH:MM:SS Phi_Centre R_Centre R
-----------------------------------------------------------------------------
2000-05-05 11:35:27 356.93 8.74 9.69
2000-05-05 11:37:23 202.97 13.23 22.23
...
test file first good rec_ind = 27 dtime = 2000-05-05 13:40:30 phi_cent[deg] = 87.48 r_cent[deg] = 2.76 r[deg] = 14.09 fom = 4.0
AACGM_lat  MLT  ->  OCB_lat  OCB_MLT  r_corr
    75.00  22.0 ->   71.312   21.430    0.00
    80.00  12.0 ->   78.088   13.016    0.00
    70.00   6.0 ->   70.419    6.027    0.00
    85.00   0.0 ->   83.636   22.035    0.00
```

IMAGE 文件默认用 `ocb_correction.circular`，所以 `r_corr` 全是 0。前 27 条（0–26）的 `fom`（`R_MERIT`）超过默认上限 5.0，被跳过；第 27 条 `fom` = 4.0。

### 3.2 包内 AMPERE 边界：2024-05-10 平静早晨 vs 暴时

```python
afile = os.path.join(os.path.dirname(ocbpy.__file__), 'boundaries', 'amp_north_radii.ocb')
a = ocbpy.OCBoundary(filename=afile, instrument='ampere', hemisphere=1,
                     stime=dt.datetime(2024,5,10,5), etime=dt.datetime(2024,5,11,1))
for when in (dt.datetime(2024,5,10,6), dt.datetime(2024,5,10,22)):
    a.rec_ind = -1
    ocbpy.match_data_ocb(a, [when], idat=0, max_tol=600); j = a.rec_ind
    a.get_aacgm_boundary_lat(np.array([0., 6., 12., 18.]), rec_ind=j, overwrite=True)
    olat, omlt, rc = a.normal_coord(np.array([70., 75., 80.]), np.array([0., 0., 0.]))
    rl, rm = a.revert_coord(olat, omlt, rc)
```

（`print(a)` 的记录表与每条一行的 scaling 列表已节选）

```
601 records from 2024-05-10 05:00:00 to 2024-05-11 01:00:00
Uses scaling function(s):
ocbpy.ocb_correction.elliptical(**{})
attrs: ['dtime', 'r', 'x', 'y', 'phi_cent', 'r_cent', 'fom']
== 2024-05-10 06:00:00 matched rec_ind=30 dtime=2024-05-10 06:00:00 r[deg]=19.0 phi_cent[deg]=345.96 r_cent[deg]=4.12 fom(j_mag uA/m)=0.32
   aacgm_boundary_mlt = [ 0.  6. 12. 18.]
   aacgm_boundary_lat = [69.128 77.556 79.228 72.421]
   AACGM_lat MLT -> OCB_lat OCB_MLT r_corr
      70.00  0.0 ->   74.824   0.238 -2.10
      75.00  0.0 ->   79.544   0.346 -2.10
      80.00  0.0 ->   84.242   0.631 -2.10
   revert_coord -> [70. 75. 80.] [0. 0. 0.]
== 2024-05-10 22:00:00 matched rec_ind=510 dtime=2024-05-10 22:00:00 r[deg]=34.0 phi_cent[deg]=270.00 r_cent[deg]=1.00 fom(j_mag uA/m)=1.46
   aacgm_boundary_mlt = [ 0.  6. 12. 18.]
   aacgm_boundary_lat = [58.114 61.973 60.211 56.946]
   AACGM_lat MLT -> OCB_lat OCB_MLT r_corr
      70.00  0.0 ->   79.957   0.191 -2.10
      75.00  0.0 ->   82.460   0.254 -2.10
      80.00  0.0 ->   84.960   0.381 -2.10
   revert_coord -> [70. 75. 80.] [0. 0. 0.]
```

AMPERE 文件的 `fom` 就是 `J_MAG`（µA/m，R1/R2 电流跃变）；默认 `ocb_correction.elliptical`（Burrell et al. 2019 把 R1/R2 边界修正到 OCB），午夜 MLT 处 `r_corr` = −2.10°。

### 3.3 矢量缩放（暴时 22 UT，AACGM 75°、MLT 0 处一个 500 m/s 北向 + 100 m/s 东向流速）

```python
v = ocbpy.ocb_scaling.VectorData(0, j, 75.0, 0.0, vect_n=500.0, vect_e=100.0, vect_z=0.0,
                                 dat_name='Vi', dat_units='m/s', scale_func=ocbpy.ocb_scaling.normal_evar)
v.set_ocb(a)
```

```
VectorData Vi [m/s] at AACGM lat 75, MLT 0:
   ocb_lat    = 82.46027569882807
   ocb_mlt    = 0.25427165561935694
   r_corr     = -2.097939334919742
   unscaled_r = 31.902060665080256
   scaled_r   = 16.0
   vect_n     = 500.0
   vect_e     = 100.0
   vect_mag   = 509.9019513592785
   ocb_n      = 996.939395783758
   ocb_e      = 199.3878791567516
   ocb_z      = 0.0
   ocb_mag    = 1016.6826865941564
   ocb_quad   = 2
   vec_quad   = 1
   pole_angle = 3.858253231780013
```

`normal_evar` 按 `unscaled_r / scaled_r` = 31.902 / 16.0 ≈ 1.994 放大：`ocb_n` 996.94 = 500 × 1.994。意思是：暴时极盖半径约为参考极盖（90° − 74° = 16°）的两倍，同样的电势差摊在更大的面积上，"归一化"后的流速要乘回这个比例才能和平静时比较。`ocb_z` 为 0 是因为 `normal_evar` 只缩放水平分量；纵向分量要不要缩放取决于物理量（`normal_curl_evar` 是另一个选项）。

## 4. 参数 / 字段

| `OCBoundary` 参数 | 默认 | 说明 |
| --- | --- | --- |
| `filename` | `'default'` | 边界文件路径；`'default'` 按 `instrument`+时间挑包内文件（AMPERE 2022 年后挑不到，坑 1） |
| `instrument` | `''` | `'image'` `'si12'` `'si13'` `'wic'` `'ampere'`/`'amp'` `'dmsp-ssj'` |
| `hemisphere` | `1` | 1 北、−1 南；必须和文件、数据纬度符号一致 |
| `boundary_lat` | `74.0` | OCB 坐标里边界所在纬度 |
| `stime` / `etime` | `None` | 只保留该时间段记录（AMPERE 文件仍要整个读一遍） |
| `rfunc` | IMAGE `circular`，AMPERE `elliptical` | 边界修正函数，决定 `r_corr` |

| 属性 / 返回 | 单位 | 含义 |
| --- | --- | --- |
| `dtime[i]` | UT | 第 i 条边界时刻 |
| `phi_cent` | deg | 拟合圆心方位（从午夜起算，≈ MLT×15） |
| `r_cent` | deg | 圆心离 AACGM 极点的余纬 |
| `r` | deg | 圆半径（余纬） |
| `fom` | IMAGE：`R_MERIT`（deg）；AMPERE：`J_MAG`（µA/m） | 质量指标；源码默认 IMAGE `max_fom=5.0`、AMPERE `min_fom=0.15`，`get_next_good_ocb_ind(min_merit, max_merit)` 可改 |
| `rec_ind` | — | 当前使用的记录号；初值 −1 |
| `normal_coord` → `ocb_lat, ocb_mlt, r_corr` | deg, h, deg | OCB 纬度 / MLT / 修正量 |
| `aacgm_boundary_lat[j]` | deg | `get_aacgm_boundary_lat` 写入的边界 AACGM 纬度（不作为返回值） |
| `VectorData.ocb_n/ocb_e/ocb_z/ocb_mag` | 同输入 | OCB 坐标下缩放后的分量 |
| `unscaled_r` / `scaled_r` | deg | 该 MLT 处实际极盖半径 / 参考半径 `90 − boundary_lat` |

## 5. 怎么读结果

- `ocb_lat` > 74：在极盖（开放磁力线）里；< 74：在边界赤道侧（闭合磁力线、极光椭圆或更低）。
- 同一个 AACGM 70° 午夜点：06 UT `ocb_lat` 74.824（刚过边界，贴着椭圆极侧），22 UT 79.957（深入极盖）。如果用 AACGM 纬度分箱，这两个时刻会落进同一格。
- 边界纬度随 MLT 变：06 UT 日侧（12 MLT）79.2°、夜侧（0 MLT）69.1°，圆心偏向夜侧是正常形态；22 UT 四个 MLT 都在 57–62°，说明整个椭圆大幅赤道向扩张。
- `revert_coord` 精确回到输入值，可用来自检。

## 6. 坑（现象 → 原因 → 一条修复命令）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `OCBoundary(instrument='amp', stime=2024-…)` `print(ocb)` 只有一行 `No OCBoundary file specified`，`filename`/`dtime`/`r`/`fom` 全是 `None`，`records` 为 0。只有开了 INFO 日志才看得到 `no boundary file available for amp northern hemisphere, …` | `boundaries/files.py` 把 AMPERE 文件结束时间写死为 2022-01-01，而文件实际到 2024-10-31 | `OCBoundary(filename=os.path.join(os.path.dirname(ocbpy.__file__),'boundaries','amp_north_radii.ocb'), instrument='ampere', ...)` |
| 2 | `normal_coord` 返回 `(nan, nan, nan)` | 刚建对象时 `rec_ind = -1`，还没选记录 | `ocb.get_next_good_ocb_ind()`（或 `ocbpy.match_data_ocb(ocb, [时间], idat=0)`） |
| 3 | 南半球纬度（如 −75°）返回 NaN | `hemisphere=1` 的对象只接受北半球点 | `OCBoundary(filename=.../amp_south_radii.ocb, instrument='ampere', hemisphere=-1)` |
| 4 | `a.get_aacgm_boundary_lat(0.0, rec_ind=j)` 得到 `None`，格式化时报 `TypeError: unsupported format string passed to NoneType.__format__` | 该方法只把结果写进属性，不返回 | `a.get_aacgm_boundary_lat(mlts, rec_ind=j, overwrite=True); print(a.aacgm_boundary_lat[j])` |
| 5 | 建 AMPERE 对象要等约 40 s | `amp_north_radii.ocb` 有 3,514,320 行，源码对每一行做时间转换后才按 `stime/etime` 筛 | 一次建好对象反复用：`pickle.dump(a, open('amp_20240510.pkl','wb'))`（质检复跑：pickle 文件 290011 B，`pickle.load` 不到 0.01 s；读回后 06 UT 仍匹配 rec 30，70° 午夜 → 74.824，与新建对象相同） |
| 6 | `import ocbpy` 打印 `unable to load \`zenodo_get\` module` | DMSP-SSJ 边界要从 Zenodo 下载，依赖可选包 | `pip install --no-cache-dir zenodo_get`（质检复跑：装上 zenodo-get 3.1.0 后 `import ocbpy` 不再打印这条；DMSP-SSJ 下载本身没试） |
| 7 | 60° 这样远在边界外的点也给出 `ocb_lat` 54.378，不是 NaN（§3.1 IMAGE 测试记录 27，MLT 22）。反过来，AMPERE 暴时 22 UT 边界已经退到 58°，60° 落在极盖内，给出 74.946 | 映射对边界外的点照样线性外推 | 统计时自己筛：`mask = ocb_lat >= ocb.boundary_lat`（或按研究需要保留边界外 N 度） |
| 8 | AMPERE 对象给出的边界纬度比文件里的 R1/R2 圆（`r`、`r_cent`）高 2° 左右 | AMPERE 是 R1/R2 电流边界，默认用 `elliptical` 修正推到 OCB（本例 `r_corr` −2.10°）；IMAGE 用 `circular`（`r_corr` 0）。包内 IMAGE（2000–2002）和 AMPERE（2010–2024）没有重叠时段，没法同一时刻直接对比 | 需要原始 R1/R2 时：`OCBoundary(..., rfunc=ocbpy.ocb_correction.circular)`。质检复跑 22 UT：`r_corr` 全为 0；0/6/12/18 MLT 的边界 AACGM 纬度是 56.015/57.0/56.015/55.0（`elliptical` 是 58.114/61.973/60.211/56.946）；70° 午夜 → 80.576（`elliptical` 是 79.957） |

## 7. 许可与诚实边界

- ocbpy：BSD-3-Clause。包内边界数据要单独引用：IMAGE 引 Chisham (2017)、Chisham et al. (2022)；AMPERE 引 Milan (2023)、Milan et al. (2015) 并致谢 AMPERE 团队，用了修正还要引 Burrell et al. (2019)（`boundaries/README.md` 原文要求）。
- **实跑**：§3.1–3.3 全部输出；坑 1–8 复现过（5、6、8 的修复命令由质检复跑验证）。
- **未实跑**：`EABoundary` / `DualBoundary`（赤道侧边界 + 双边界坐标）、`cycle_boundary`、`instruments.vort`/`supermag`/`pysat_instruments`、DMSP-SSJ、`coords='geodetic'` 输入、南半球实际转换。
- ocbpy 只能在"有边界拟合"的时刻用；AMPERE 为 2 分钟一条，但 `fom` 低的记录会被跳过，暴时也可能出现空档。

## 8. 链接

- 教程：[05 闪烁与 ROTI](../tutorials/05-scintillation-roti.md) · [13 闪烁建模](../tutorials/13-scintillation-modeling.md) · [20 磁暴 TEC 分析](../tutorials/20-storm-tec-analysis.md)
- 兄弟：[lompe](./lompe.md) · [pydarn](./pydarn.md) · [superdarn-data](./superdarn-data.md) · [aacgmv2](./aacgmv2.md) · [apexpy](./apexpy.md) · [pysatspaceweather](./pysatspaceweather.md)
