# aacgmv2 · AACGM-v2 地磁坐标操作手册

目录：[`PROJECTS.json` → `aacgmv2`](../../PROJECTS.json) · 上游 <https://github.com/aburrell/aacgmv2> · 许可 **MIT** · PyPI **`aacgmv2` 2.7.1** · tip **`5f85579`**（tag `v2.7.1`）· Python **3.13** 本机编译轮子（需 `python3-dev`）；`(40°N,80°W)` 2015-03-23 15:30 UT / 250 km 实跑（2026-09-24 EDT） · **质检复跑通过**（同 I/O，2026-09-24 04:45 EDT）

> 岗位：地理坐标 ↔ **Altitude-Adjusted Corrected Geomagnetic (AACGM-v2)**，并算 **MLT**。冲突时：**上游 README / `python -m aacgmv2 -h` > 本文**。与 [apexpy](./apexpy.md)（Apex/QD）互补；**不是** TEC / 电子密度模型。

## 1. 用途与边界

**做：**

- `get_aacgm_coord(glat, glon, height, dtime) → mlat, mlon, mlt`
- `convert_latlon` / `convert_latlon_arr`：`G2A` / `A2G`（第三返回值为 `out_r`，**不是** MLT）
- `convert_mlt(mlon|mlt, dtime, m2a=…)`：AACGM 经度 ↔ MLT
- CLI：`python -m aacgmv2 convert|convert_mlt …`

**不做：**

- **不是** Apex / Quasi-Dipole → [apexpy](./apexpy.md)（同作者生态，定义不同，数字勿直接混用）
- **不是** 电子密度 / TEC → [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [pyiri](./pyiri.md)
- **不是** 中性大气 → [msise00](./msise00.md)
- **不是** 读 IONEX / RINEX→TEC → [ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md)
- 系数默认高度上限 **2000 km**（`high_alt_coeff`）；更高需 `TRACE` / `ALLOWTRACE` / `BADIDEA`

一句话：aacgmv2 = **AACGM-v2（Shepherd 2014）的 Python 标准轮子**，极光/高纬电离层磁坐标常用。

| 术语 | 含义 |
| --- | --- |
| AACGM-v2 | 高度调整校正地磁坐标；纬度/经度单位度 |
| `mlt` | 磁地方时（小时）；需完整 `datetime`（含时分） |
| `out_r`（`convert_latlon`） | G2A：地心径向距离（以 R_E 计）；A2G：高度 km |
| `TRACE` | 沿磁力线追踪，不用多项式系数 |
| `ALLOWTRACE` | `get_aacgm_coord` 默认；>2000 km 自动追踪 |
| 引用 | 包 DOI **与** Shepherd (2014) JGR 论文 |

## 2. 安装

PyPI **无预编译 manylinux wheel**（本机 3.13）：源码编 C 扩展，需 **`python3-dev`**（`Python.h`）+ gcc。

```bash
sudo apt-get install -y python3-dev   # 缺则 fatal error: Python.h
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv aacgmv2-demo/.venv
source aacgmv2-demo/.venv/bin/activate
pip install -U pip
pip install 'aacgmv2==2.7.1' numpy
python -c "import aacgmv2; print(aacgmv2.__version__)"
# 期望：2.7.1
python -m aacgmv2 -h
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `fatal error: Python.h` | 未装头文件 | `apt install python3-dev` |
| 编译很慢 / 刷 C | 源码扩展 | 等一次编完；勿 `--break-system-packages` |
| CLI `convert -d` 帮助写 1900–2020 | 帮助文案偏旧 | 包内系数到 **2030**；以实跑为准 |

## 3. 端到端：地理 → AACGM / MLT（本机真跑）

与 [msise00](./msise00.md) / [iri2016](./iri2016.md) / [apexpy](./apexpy.md) 同点：2015-03-23 **15:30 UT**，**(40°N, 80°W)**，250 km。

```bash
cd ~/iono_ops/aacgmv2-demo && source .venv/bin/activate
python - <<'PY'
import datetime as dt
import numpy as np
import aacgmv2

dn = dt.datetime(2015, 3, 23, 15, 30, 0)
print("aacgmv2", aacgmv2.__version__)

glat, glon, h = 40.0, -80.0, 250.0
mlat, mlon, mlt = aacgmv2.get_aacgm_coord(glat, glon, h, dn)
print("get_aacgm_coord", float(mlat), float(mlon), float(mlt))

g2a = aacgmv2.convert_latlon(glat, glon, h, dn)  # method_code 默认 G2A
print("convert_latlon_G2A", float(g2a[0]), float(g2a[1]), float(g2a[2]))

a2g = aacgmv2.convert_latlon(float(mlat), float(mlon), h, dn, method_code="A2G")
print("convert_latlon_A2G", float(a2g[0]), float(a2g[1]), float(a2g[2]))

mlt2 = float(np.asarray(aacgmv2.convert_mlt([float(mlon)], dn, m2a=False)).ravel()[0])
mlon2 = float(np.asarray(aacgmv2.convert_mlt([float(mlt)], dn, m2a=True)).ravel()[0])
print("convert_mlt_A2M", mlt2)
print("convert_mlt_M2A", mlon2)

arr = aacgmv2.convert_latlon_arr(
    [40.0, 0.0, 70.0], [-80.0, 0.0, 0.0], [250.0, 300.0, 110.0], dn)
print("arr_mlat", [float(x) for x in arr[0]])
print("arr_mlon", [float(x) for x in arr[1]])
print("arr_r", [float(x) for x in arr[2]])

mlat_t, mlon_t, mlt_t = aacgmv2.get_aacgm_coord(glat, glon, h, dn, method="TRACE")
print("get_aacgm_TRACE", float(mlat_t), float(mlon_t), float(mlt_t))

dn0 = dt.datetime(2015, 3, 23)  # 00:00 UT → MLT 大变
print("get_aacgm_dateonly", *[float(x) for x in aacgmv2.get_aacgm_coord(glat, glon, h, dn0)])
PY
```

**本机 stdout（2026-09-24 EDT，`aacgmv2` 2.7.1）：**

```text
aacgmv2 2.7.1
get_aacgm_coord 50.53175925707385 -4.091903907285906 10.090683439588037
convert_latlon_G2A 50.53175925707385 -4.091903907285906 1.03894769416398
convert_latlon_A2G 40.00372038734848 -79.99356242319746 251.85782587500563
convert_mlt_A2M 10.090683439588037
convert_mlt_M2A -4.091903907285911
arr_mlat [50.53175925707385, -7.24216947222024, 68.4691798381246]
arr_mlon [-4.091903907285906, 72.71156263448808, 87.01436383076438]
arr_r [1.03894769416398, 1.048175696885987, 1.015393050349527]
get_aacgm_TRACE 50.529276253080454 -4.096604805518098 10.09037004637256
get_aacgm_dateonly 50.531912979223954 -4.092019189684674 18.766986896242074
```

| 字段 | 本机值 | 含义 |
| --- | --- | --- |
| `mlat` | ≈ **50.532°** | AACGM 磁纬 |
| `mlon` | ≈ **-4.092°** | AACGM 磁经 |
| `mlt` | ≈ **10.091 h** | 磁地方时（15:30 UT） |
| `G2A` 第三列 | ≈ 1.039 | `out_r`（R_E），**不是** MLT |
| `A2G` 往返 | ≈ 40.004°, −79.994°, 251.86 km | 近似闭合；高度略偏 |
| `TRACE` | mlat≈50.529 | 与系数法差 ~0.002° |
| `dateonly` MLT | ≈ 18.767 h | 缺时分 → 按 00:00 UT |

对照同点 [apexpy](./apexpy.md)：Apex alat≈**50.70**、alon≈**−4.07**、MLT≈**10.25**——系统不同，勿当同一坐标。

### 3.1 CLI

`convert` 的 `-d` **只有日期**（无时分）；要 MLT 用 `convert_mlt` + **14 位** `YYYYMMDDHHMMSS`。

```bash
printf '40.0 -80.0 250.0\n' | python -m aacgmv2 convert -d 20150323
printf '40.0 -80.0 250.0\n' | python -m aacgmv2 convert -d 20150323 -t
printf -- '-4.091903907285906\n' | python -m aacgmv2 convert_mlt 20150323153000
```

**本机 stdout：**

```text
50.53191298 -4.09201919 1.03894769
50.52942882 -4.09671825 1.03894769
10.09068344
```

（第一行 = 日期 00:00 的 G2A；第二行加 `-t` = TRACE；第三行 = 该 `mlon` 在 15:30 UT 的 MLT。）

### 3.2 关键参数 / method

| 入口 | 关键参数 |
| --- | --- |
| `get_aacgm_coord` | `method`：`ALLOWTRACE`（默认）/`TRACE`/`BADIDEA`/`GEOCENTRIC` |
| `convert_latlon` | `method_code`：`G2A`/`A2G`，可 `|` 叠 `TRACE` 等 |
| CLI `convert` | `-d YYYYMMDD`、`-v`（A2G）、`-t`（trace）、`-a`/`-b`/`-g` |
| CLI `convert_mlt` | 位置参 `YYYYMMDDHHMMSS`；`-v` = MLT→mlon |

```bash
python -m aacgmv2 convert -h
python -m aacgmv2 convert_mlt -h
```

## 4. I/O 字段

| API | 输入 | 输出 |
| --- | --- | --- |
| `get_aacgm_coord` | glat, glon(°E), height(km), `datetime` | **mlat, mlon, mlt** |
| `convert_latlon` | lat, lon, height, `datetime`, `method_code` | lat, lon, **out_r** |
| `convert_latlon_arr` | 数组 lat/lon/height | 三元组数组 |
| `convert_mlt` | mlon 或 mlt 数组, `datetime`, `m2a` | 对应 mlt 或 mlon |
| CLI `convert` 行 | `LAT LON ALT` | `mlat mlon out_r` |
| CLI `convert_mlt` 行 | 单列数字 | MLT 或 mlon |

## 5. 接到哪步

- IRI/气候态按**磁纬**分箱 → 本文或 [apexpy](./apexpy.md)（先选定一种体系）+ [iri2016](./iri2016.md) / [pyglow](./pyglow.md) / [pyiri](./pyiri.md)
- GIM/TEC 按 AACGM 纬统计 → [ionex-gim](./ionex-gim.md) + 本文
- 中性背景同点对照 → [msise00](./msise00.md)
- 教程 → [04](../tutorials/04-iri-nequick.md) / [03](../tutorials/03-gim-ionex.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `fatal error: Python.h` | 无开发头 | `apt install python3-dev` |
| 2 | 把 `convert_latlon` 第三列当 MLT | 那是 **out_r** | 要 MLT 用 `get_aacgm_coord` / `convert_mlt` |
| 3 | MLT 差 ~8 h | `datetime` 只有日期 / CLI `convert -d` 无时 | 锁 **15:30**；MLT 走 `convert_mlt` 14 位 |
| 4 | 与 apexpy 差 0.1°+ | AACGM ≠ Apex/QD | 全文固定一种；对照写清体系 |
| 5 | `>2000 km` RuntimeError | 系数上限 | `method="TRACE"` 或 `ALLOWTRACE` |
| 6 | A2G 往返 lat/height 不完全重合 | 近似变换 | 允许小残差；勿强制逐点相等 |
| 7 | `convert_mlt` → `TypeError: only 0-dimensional…` | 返回数组 | `np.asarray(…).ravel()[0]` |
| 8 | CLI `-d` 帮助写到 2020 | 文案旧 | 系数到 2030；以本机实跑为准 |
| 9 | 当 TEC/IRI 用 | 只做坐标 | 接 [iri2016](./iri2016.md) / [pyiri](./pyiri.md) |
| 10 | 引用只写包名 | 上游要求双引 | DOI + Shepherd 2014 |
| 11 | 数组与标量 shape 炸 | 未对齐长度 | `convert_latlon_arr` 三路同长 |
| 12 | 经度东/西搞反 | 约定 **°E**（西经为负） | 80°W → `-80` |

## 7. 选型与链接

| 你要… | 用 |
| --- | --- |
| AACGM-v2 / MLT | **本文 aacgmv2** |
| Apex / QD / MLT | [apexpy](./apexpy.md) |
| IRI 气候态 | [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [pyiri](./pyiri.md) |
| NRLMSISE-00 | [msise00](./msise00.md) |
| 读 GIM | [ionex-gim](./ionex-gim.md) |

- 文档：<https://aacgmv2.readthedocs.io/>
- 论文：Shepherd, S. G. (2014), *JGR Space Physics*, doi:10.1002/2014JA020264
- 兄弟：[apexpy](./apexpy.md) · [msise00](./msise00.md) · [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [pyiri](./pyiri.md) · [ionex-gim](./ionex-gim.md)
