# pymap3d · 纯 Python 三维坐标转换操作手册

目录：[`PROJECTS.json` → `pymap3d`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/pymap3d> · PyPI **`pymap3d` 3.2.0** · tip **`033895e`** · 许可 **BSD-2-Clause** · 本机验证（2026-09-24 06:04 EDT）：pytest **397 passed** / **11 skipped**；北京 geodetic→ECEF **(−2177813.332, 4388956.908, 4069858.556)** m 往返 OK；+0.001°N → ENU n≈**111.034** m；赤道 ECEF x=**6378137.0**；默认 ECI 为 Numpy 实现（无 Astropy → 精度警告）

> 岗位：**大地坐标 / ECEF / ENU·NED / AER / ECI** 等互转（对齐常见 MATLAB 习惯）。冲突时：**上游 README / docs / 本机 `help(pymap3d.geodetic2ecef)` > 本文**。磁坐标 → [apexpy](./apexpy.md)/[aacgmv2](./aacgmv2.md)；RINEX 站坐标读写 → [georinex](./georinex.md)；同组织还有 georinex。

## 1. 用途与边界

**做：**

- `geodetic2ecef` / `ecef2geodetic`（WGS84 等 `Ellipsoid`）
- `geodetic2enu` / `enu2geodetic`、`geodetic2ned`、`enu2aer` / `aer2enu`
- `geodetic2eci` / `eci2geodetic`（需时间；可选 Astropy 提精）
- 矢量 `numpy` 输入；无强制系统依赖（纯 Python + numpy）

**不做：**

- **不是** ITRF 历元框变换 / 板块运动产品（需 pyproj/ITRF 工具另接）
- **不是** 磁纬/MLT → [apexpy](./apexpy.md)/[aacgmv2](./aacgmv2.md)
- **不是** NMEA/RINEX 解析
- **不是** 重力/大地水准面精化（仅几何椭球高）

一句话：`pymap3d` = **日地/GNSS 脚本里的坐标胶水**；框变换与磁坐标另找专用库。

| 术语 | 含义 |
| --- | --- |
| geodetic | lat° / lon° / 椭球高 m |
| ECEF | 地心地固直角坐标 m |
| ENU / NED | 站心东北天 / 北东地 |
| AER | 方位角° / 仰角° / 斜距 m |
| ECI | 惯性系（本机默认 Numpy 路径） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
pip install 'pymap3d==3.2.0'
python -c "import pymap3d as pm; print(pm.__version__)"
# 期望：3.2.0

# 可选 tip + 单测
git clone --depth 1 https://github.com/geospace-code/pymap3d.git ~/iono_ops/pymap3d
cd ~/iono_ops/pymap3d && git rev-parse --short HEAD   # 033895e
pip install pytest
PYTHONPATH=src python -m pytest -q
# 397 passed, 11 skipped
```

可选：`pip install astropy` 后 ECI 走高精度路径（本机**未**装 Astropy）。

## 3. 端到端（本机真跑；2026-09-24 06:04 EDT）

### 3.1 北京：大地 ↔ ECEF 往返（对齐 [gpsd](./gpsd.md) 坐标）

```bash
python - <<'PY'
import pymap3d as pm
lat, lon, alt = 39.904187167, 116.390742667, 44.0
x, y, z = pm.geodetic2ecef(lat, lon, alt)
print(f"ECEF {x:.3f} {y:.3f} {z:.3f}")
lat2, lon2, alt2 = pm.ecef2geodetic(x, y, z)
print(lat2, lon2, alt2)
print(pm.geodetic2ecef(0.0, 0.0, 0.0))  # 赤道
ell = pm.Ellipsoid.from_name("wgs84")
print(ell.semimajor_axis, ell.semiminor_axis)
PY
```

**本机：** ECEF **−2177813.332** / **4388956.908** / **4069858.556** m；往返 lat/lon 一致、alt≈**44.0**；赤道 **(6378137.0, 0.0, 0.0)**；WGS84 a=**6378137.0** b=**6356752.31424518**。

### 3.2 站心 ENU / AER / NED

```bash
python - <<'PY'
import pymap3d as pm
lat0, lon0, h0 = 39.904187167, 116.390742667, 44.0
e, n, u = pm.geodetic2enu(lat0 + 0.001, lon0, h0, lat0, lon0, h0)
print("ENU", e, n, u)
print("AER", pm.enu2aer(e, n, u))
print("NED", pm.geodetic2ned(lat0 + 0.001, lon0, h0, lat0, lon0, h0))
PY
```

**本机：** ENU e≈**0**、n≈**111.033569** m、u≈**−0.001** m；AER az=**0** el=**0** range≈**111.034** m；NED n≈**111.034**、e≈**0**、d≈**+0.001** m。

### 3.3 对空中点的 AER（视线）

```bash
python - <<'PY'
import pymap3d as pm
lat0, lon0, h0 = 39.904187167, 116.390742667, 44.0
az, el, srange = pm.geodetic2aer(
    lat0, lon0 + 10.0, 500_000.0, lat0, lon0, h0
)
print(az, el, srange)
PY
```

**本机：** az≈**86.788°**、el≈**25.506°**、srange≈**1 018 065** m。

### 3.4 ECI（无 Astropy 边界）

```bash
python - <<'PY'
import pymap3d as pm
from datetime import datetime, timezone
t = datetime(2026, 9, 24, 10, 0, 0, tzinfo=timezone.utc)
xi, yi, zi = pm.geodetic2eci(39.904187167, 116.390742667, 44.0, t)
print(f"{xi:.3f} {yi:.3f} {zi:.3f}")
PY
```

**本机：** 日志警告 `Numpy implementation has much less accuracy than Astropy`；数值约 **−30400.903 / −4899478.486 / 4069858.556** m。需要更高 ECI 精度时再装 Astropy，**勿把本数当精密定轨输入**。

### 3.5 与磁坐标手册对照点（仅 ECEF）

```bash
python - <<'PY'
import pymap3d as pm
x, y, z = pm.geodetic2ecef(40.0, -80.0, 250_000.0)
print(f"{x:.3f} {y:.3f} {z:.3f}")
PY
```

**本机：** **882865.314 / −5006978.004 / 4238682.475** m（40°N 80°W 高 250 km）——磁坐标数值见 [apexpy](./apexpy.md)/[aacgmv2](./aacgmv2.md)，本文只给几何 ECEF。

## 4. I/O 与关键 API

| 函数 | 作用 |
| --- | --- |
| `geodetic2ecef(lat,lon,alt, ell=None)` | 大地 → ECEF |
| `ecef2geodetic(x,y,z, …)` | 逆变换 |
| `geodetic2enu` / `enu2geodetic` | 站心东北天 |
| `geodetic2ned` / `ned2geodetic` | 北东地 |
| `enu2aer` / `aer2enu` / `geodetic2aer` | 方位仰角斜距 |
| `geodetic2eci` / `eci2geodetic` | 惯性系（需 `datetime`） |
| `Ellipsoid.from_name("wgs84")` | 椭球参数 |

角度默认**度**；长度**米**。可传入 `numpy` 数组做批量。

## 5. 接到哪步

```text
测站 lat/lon/h 或 ECEF
  → pymap3d 转到 ENU/AER/ECI
  → 电离层穿刺点/射线几何脚本
  → 磁坐标另接 apexpy/aacgmv2
  → 观测文件坐标仍用 georinex/rinexmod
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | ECI 警告 / 精度差 | 未装 Astropy | `pip install astropy`；或只用 ECEF/ENU |
| 2 | 与 ITRF2020 差厘米级+ | 未做框/历元变换 | 另接 pyproj/官方框工具 |
| 3 | alt 当地水准高 | API 是**椭球高** | 勿混 geoid 高；差分先统一 |
| 4 | 角度当弧度传入 | 默认度 | 查 docstring；勿擅自 `/180*π` 两遍 |
| 5 | `skipped` 单测 | 可选依赖（pyproj 等） | 397 passed 即可；不必强装全 |
| 6 | 与 MATLAB 差符号 | NED/ENU 轴约定 | 用库内 `ned*`/`enu*` 成对函数 |
| 7 | 把 pymap3d 当磁坐标 | 产品边界 | → [apexpy](./apexpy.md) |
| 8 | 大数组慢 | 纯 Python 循环习惯 | 传 `ndarray` 走向量化 |
| 9 | 与 gpsd `altMSL` 比 ECEF | MSL≠椭球高 | 本手册北京例沿用 demo 数值作几何探针 |
| 10 | tip≠PyPI | 开发树超前 | 手册钉 **3.2.0**；tip `033895e` 同版号 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本内 ECEF/ENU/AER | **pymap3d（本文）** |
| 磁纬/MLT | [apexpy](./apexpy.md)/[aacgmv2](./aacgmv2.md) |
| RINEX 头/观测坐标 | [georinex](./georinex.md)/[rinexmod](./rinexmod.md) |
| CRS/投影/ITRF | pyproj（本目录未单列） |
| 轨道传播 TLE | catalog `python-sgp4`（无本手册时看上游） |

相关：[apexpy](./apexpy.md) · [aacgmv2](./aacgmv2.md) · [georinex](./georinex.md) · [geospacelab](./geospacelab.md) · [gpsd](./gpsd.md) · [msise00](./msise00.md)
