# geospacelab · 日地空间数据管理与可视化操作手册

目录：[`PROJECTS.json` → `geospacelab`](../../PROJECTS.json) · 上游 <https://github.com/JouleCai/geospacelab> · 文档 <https://geospacelab.readthedocs.io/en/latest/> · 许可 **BSD-3-Clause** · PyPI **`geospacelab` 0.14.8** · 本机：OMNI/WDC/GFZ + Madrigal GNSS TEC map 实拉（2015-03-17 St. Patrick 暴）；**不是** TEC 解算引擎（2026-09-24 EDT）

> 岗位：用 **DataHub / Dataset / Variable** 统一拉 OMNI、地磁指数、Madrigal TEC/EISCAT/DMSP、Swarm 等并做时序/极区图。冲突时：**上游 README / readthedocs / 本机 `import geospacelab` > 本文**。校准实测 TEC → [pytecgg](./pytecgg.md)；读 IONEX → [ionex-gim](./ionex-gim.md)；气候态 IRI → [pyglow](./pyglow.md)。

## 1. 用途与边界

**做：**

- `DataHub.dock(datasource_contents=[…])` 拉取并缓存多源数据
- Express：`OMNIDashboard`（太阳风+IMF+AE/SYM/Kp）、EISCAT/DMSP 等 quicklook
- `GeoDashboard` + `add_polar_map` 叠 Madrigal **GNSS TEC map**（beta）
- 本地根目录默认 `~/Geospacelab/Data`（`~/.geospacelab/config.toml`）

**不做：**

- **不是** 从 RINEX 校准 sTEC/vTEC → [pytecgg](./pytecgg.md)（作者 viventriglia）
- **不是** 读分析中心 IONEX GIM → [ionex-gim](./ionex-gim.md) / 并排 [diffionmap](./diffionmap.md)
- **不是** IRI/NeQuick 气候态剖面 → [pyglow](./pyglow.md) / [iri2016](./iri2016.md) / [nequickg](./nequickg.md)
- **不是** 球谐 GIM 求解 → [sh-gim](./sh-gim.md)（边界）
- TEC map 为 **Madrigal 产品图**（约 1°×1°、5 min），**不是** 你自建 GIM

一句话：geospacelab = **空间天气观测/指数/产品的拉取与作图框架**；电离层「算 TEC」仍走 pytecgg / GIM 链。

| 术语 | 含义 |
| --- | --- |
| `DataHub` | 顶层；`dock` 多数据源 |
| `datasource_contents` | 模块路径列表，如 `['cdaweb','omni']`、`['madrigal','gnss','tecmap']` |
| `Variable.value` | `numpy.ndarray`；时间维在 axis 0 |
| `OMNIDashboard` | OMNI2 + WDC AE/ASYSYM + GFZ Kp 的 express |
| `config.toml` | `~/.geospacelab/config.toml`：数据根、Madrigal/WDC 身份 |

## 2. 安装

```bash
mkdir -p ~/iono_ops/geospacelab-demo && cd ~/iono_ops/geospacelab-demo
python3.11 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install geospacelab cartopy
python -c "import geospacelab, cartopy; print(geospacelab.__version__, cartopy.__version__)"
# 期望：0.14.8  0.26.0（或以本机 PyPI 为准）
```

首次 `import` 会问 **数据根目录**；写入 `~/.geospacelab/config.toml`。Madrigal / WDC 首次 dock 会要邮箱等，建议预先写好：

```toml
[datahub]
data_root_dir = "/home/YOU/Geospacelab/Data"

[datahub.madrigal]
user_fullname = "Your Name"
user_email = "you@example.com"
user_affiliation = "Your Lab"

[datahub.wdc]
user_email = "you@example.com"
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'cartopy'` | 极区/地图依赖未装 | `pip install cartopy`（或 conda-forge） |
| `User's full name:` / `User's email:` 后 EOF | 非交互环境未写 config | 按上表写 `config.toml` 再跑 |
| `cannot import name 'madrigal'` 连带失败 | 缺身份时 import 半截 | 先写 madrigal/wdc 块 |
| 极区图缺岸线 | cartopy 数据未下完 | 允许联网；或预置 cartopy 数据目录 |
| `get_variable('B_x_GSM')` 得 `None` | 默认查到了错 dataset | 传 `dataset_index=0`（OMNI）或 `dataset=` |

### 安装验收

```bash
python -c "import geospacelab; from geospacelab.datahub import DataHub; print(geospacelab.__version__, 'ok')"
```

## 3. 端到端（本机真跑）

样本日：**2015-03-17**（St. Patrick’s Day 磁暴）。

### 3.1 OMNI + AE/SYM + Kp（`OMNIDashboard`）

```bash
cd ~/iono_ops/geospacelab-demo && source .venv/bin/activate
export MPLBACKEND=Agg
python - <<'PY'
import datetime, numpy as np
import geospacelab
import geospacelab.express.omni_dashboard as omni

print('geospacelab', geospacelab.__version__)
dt_fr = datetime.datetime(2015, 3, 17, 0, 0)
dt_to = datetime.datetime(2015, 3, 17, 23, 59)
dash = omni.OMNIDashboard(
    dt_fr, dt_to, omni_type='OMNI2', omni_res='1min', load_mode='AUTO')
print('n_datasets', len(dash.datasets))

def dump(name, i):
    v = dash.get_variable(name, dataset_index=i)
    a = np.asarray(v.value).astype(float).ravel()
    fin = a[np.isfinite(a)]
    print(name, 'shape', np.asarray(v.value).shape,
          'finite', fin.size,
          'min', float(fin.min()), 'max', float(fin.max()))

for n in ['B_z_GSM', 'v_sw', 'n_p', 'SYM_H', 'AE']:
    dump(n, 0)
dump('Kp', 3)
dash.quicklook()
dash.save_figure(file_name='out/omni_20150317')
print('saved')
PY
```

**本机 stdout（节选，2026-09-24 EDT，`geospacelab` 0.14.8；首次会下 CDF/NC）：**

```text
geospacelab 0.14.8
n_datasets 4
B_z_GSM shape (1440, 1) finite 1153 min -26.0 max 27.34…
v_sw shape (1440, 1) finite 1019 min 394.1 max 648.1…
n_p shape (1440, 1) finite 1019 min 3.58 max 53.81…
SYM_H shape (1440, 1) finite 1440 min -234.0 max 67.0
AE shape (1440, 1) finite 1440 min 26.0 max 2298.0
Kp shape (8, 1) finite 8 min 2.0 max 7.667…
saved
```

缓存示例：`~/Geospacelab/Data/CDAWeb/OMNI/.../omni_hro2_1min_20150301_v01.cdf`、`WDC/AE/2015/WDC_AE_201503.nc`、`GFZ/Indices/Kp_Ap/GFZ_Kp_Ap_2015.nc`。

### 3.2 F10.7 / SN（GFZ）

```python
from geospacelab.datahub import DataHub
dh = DataHub(dt_fr, dt_to)
ds = dh.dock(datasource_contents=['gfz', 'snf107'], load_mode='AUTO')
print(list(ds.keys()))
# 本机 2015-03-17：SN=38, F107_ADJ≈113.2, F107_OBS≈114.3
print(float(ds['SN'].value), float(ds['F107_OBS'].value))
```

**本机：** `SN 38.0` · `F107_OBS 114.3` · `F107_ADJ 113.2`（日值，窗口内 1 点）。

### 3.3 Madrigal GNSS TEC map（极区叠图）

需已写 `[datahub.madrigal]`。1 h 窗（5 min 一图）：

```bash
python - <<'PY'
import datetime, numpy as np, matplotlib.pyplot as plt
import geospacelab.visualization.mpl.geomap.geodashboards as geomap

dt_fr = datetime.datetime(2015, 3, 17, 6, 0)
dt_to = datetime.datetime(2015, 3, 17, 7, 0)
time_c = datetime.datetime(2015, 3, 17, 6, 30)
db = geomap.GeoDashboard(dt_fr=dt_fr, dt_to=dt_to, figure_config={'figsize': (6, 5)})
ds = db.dock(datasource_contents=['madrigal', 'gnss', 'tecmap'], load_mode='AUTO')
tec = np.asarray(ds['TEC_MAP'].value).astype(float)
dts = np.asarray(ds['DATETIME'].value).ravel()
glat = np.asarray(ds['GEO_LAT'].value)
glon = np.asarray(ds['GEO_LON'].value)
print('n_epochs', len(dts), 'shape', tec.shape, 'latlon', glat.shape)
ind = 6  # 06:30
fin = tec[ind][np.isfinite(tec[ind])]
print('t', dts[ind], 'finite', fin.size, 'min', float(fin.min()),
      'max', float(fin.max()), 'median', float(np.median(fin)))
db.set_layout(1, 1)
panel = db.add_polar_map(
    row_ind=0, col_ind=0, style='lon-fixed', cs='GEO', lon_c=0.,
    pole='N', ut=time_c, boundary_lat=30., mirror_south=False)
panel.overlay_coastlines(); panel.overlay_gridlines()
pcfg = dict(ds['TEC_MAP'].visual.plot_config.pcolormesh)
pcfg.update(c_lim=[5, 30], cmap='jet')
ipc = panel.overlay_pcolormesh(
    tec[ind], coords={'lat': glat, 'lon': glon, 'height': 250.}, cs='GEO', **pcfg)
panel.add_colorbar(ipc, c_label='TECU', c_scale='linear',
                   left=1.1, bottom=0.1, width=0.05, height=0.7)
plt.savefig('out/tec_20150317_0630.png', dpi=120, bbox_inches='tight')
print('saved_fig')
PY
```

**本机（缓存后）：**

```text
n_epochs 13 shape (13, 180, 360) latlon (180, 360)
t 2015-03-17 06:30:00 finite 11777 min 0.0 max 114.0 median 11.3
saved_fig
```

首次会从 Madrigal 拉 `gps150317g.004.hdf5`（约数十 MB）到 `…/Madrigal/GNSS/TEC/2015/20150317/`。产品状态上游标 **beta**。

对照：自建绝对 TEC → [pytecgg](./pytecgg.md)；IGS/CODE IONEX → [ionex-gim](./ionex-gim.md)；气候态背景 → [pyglow](./pyglow.md)。

## 4. I/O 字段

| 侧 | 路径/字段 | 说明 |
| --- | --- | --- |
| 配 | `~/.geospacelab/config.toml` | 数据根、Madrigal/WDC |
| 缓存 | `~/Geospacelab/Data/…` | CDF / netCDF / HDF5 |
| 入 | CDAWeb OMNI、WDC AE/ASYSYM、GFZ Kp/F107、Madrigal TEC… | `load_mode='AUTO'` 自动下 |
| 出 | `Variable.value` | ndarray；TEC_MAP `(t,lat,lon)` |
| 出 | `save_figure` / `plt.savefig` | quicklook / 极区图 |

常用 `datasource_contents`：

| 列表 | 产品 |
| --- | --- |
| `['cdaweb','omni']` | OMNI2（express 里再拆分辨率） |
| `['wdc','ae']` / `['wdc','asysym']` | AE / SYM-H |
| `['gfz','kpap']` / `['gfz','snf107']` | Kp·Ap / SN·F10.7 |
| `['madrigal','gnss','tecmap']` | 全球 GNSS TEC 图（beta） |

## 5. 接到哪步

```text
磁暴背景（OMNI/AE/SYM/Kp/F107）
  → 本文 OMNIDashboard / GFZ
  → 对照 ROTI：oasis-roti / ionomoni
  → 对照 GIM：ionex-gim / diffionmap
Madrigal TEC map（本文）
  → 肉眼/极区结构；非校准单站 TEC
单站校准 TEC
  → pytecgg ← RINEX
气候态 Ne
  → pyglow / iri2016
```

路径 B（暴时）可把本文指数层叠在 ROTI/TEC 时间轴上；教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 交互询问姓名/邮箱后挂死 | 无 TTY | 预写 `config.toml` |
| 2 | `No module named 'cartopy'` | 地图未装 | `pip install cartopy` |
| 3 | `get_variable` 全 `None` | 查错 dataset | `dataset_index=` / `dataset=` |
| 4 | TEC dock 很慢/很大 | 整日 HDF5 | 缩 `dt_fr`/`dt_to`；复用缓存 |
| 5 | 把 TEC_MAP 当自建 GIM | 实为 Madrigal 产品 | 发表写明来源；自建走 GIM 链 |
| 6 | 与 IONEX 数值差一截 | 壳高/算法/网格不同 | 只做形态对照；定量用 [ionex-gim](./ionex-gim.md) |
| 7 | `OMNIDashboard` 缺 Kp | GFZ/WDC 块失败 | 查 config 与网络；单 dock `gfz/kpap` |
| 8 | 岸线/字体告警 | cartopy/字体数据 | 可忽略或装字体；加 `MPLBACKEND=Agg` |
| 9 | 无头环境弹窗 | 默认 GUI 后端 | `export MPLBACKEND=Agg` |
| 10 | 当 RINEX→TEC 引擎 | 无解算 | 改 [pytecgg](./pytecgg.md) |
| 11 | Madrigal 拒连 | 身份/站点策略 | 换邮箱、查 OpenMadrigal 状态 |
| 12 | 标签显示 `wdc \| kpap` 却有 F107 | DataHub 索引复用观感 | 以 `list(ds.keys())` 与文件路径为准 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| OMNI/指数/TEC 产品拉图 | **geospacelab（本文）** |
| RINEX→校准 TEC | [pytecgg](./pytecgg.md) |
| 读 IONEX GIM | [ionex-gim](./ionex-gim.md) |
| 两幅 IONEX 并排 | [diffionmap](./diffionmap.md) |
| IRI 气候态 | [pyglow](./pyglow.md) · [iri2016](./iri2016.md) |
| 模式场函数化飞越 | Kamodo（缺篇时见 `lists/01-ionosphere.md`） |

相关：上游 README · readthedocs · [pytecgg](./pytecgg.md) · [ionex-gim](./ionex-gim.md) · [pyglow](./pyglow.md) · [oasis-roti](./oasis-roti.md) · 教程 [05](../tutorials/05-scintillation-roti.md)/[20](../tutorials/20-storm-tec-analysis.md)
