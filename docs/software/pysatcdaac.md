# pysatCDAAC · CDAAC/COSMIC 掩星 → pysat Instrument 操作手册

目录：[`PROJECTS.json` → `pysatCDAAC`](../../PROJECTS.json) · 上游 <https://github.com/pysat/pysatCDAAC> · 文档 <https://pysatcdaac.readthedocs.io/> · 许可 **BSD-3-Clause** · PyPI **`pysatCDAAC` 0.0.5**（非 `pysat-cdaac`）· 本机验证：`ionprf` 2019-01-01 下载 **59** 文件 → `clean` 载入 **53** 时次；`ionphs` 同日下载 **144** 文件，`Instrument.load` **失败**（改 netCDF4 读 `exL1`/`exL2`）（2026-09-24 EDT）

> 岗位：把 UCAR **CDAAC** GNSS-RO（含 **ionPhs / ionPrf**）接到 **pysat** 数据框架。冲突时：**本机 Instrument 源码 / 上游 README / readthedocs > 本文**。

## 1. 用途与边界

**做：**

- COSMIC-1 RO：`pysatCDAAC.instruments.cosmic_gps`（`platform=cosmic` · `name=gps`）
- 标签（小写 tag → CDAAC 文件名）：
  - **电离层**：`ionprf`→`ionPrf`（Ne）· `ionphs`→`ionPhs`（excess phase）· `podtec`→`podTec` · `scnlv1`→`scnLv1`
  - **大气对照**：`wetprf` / `atmprf` / `eraprf` / `gfsprf`
- 从 `https://data.cosmic.ucar.edu/` 拉日包 tar.gz（先 **repro2013**，404 再 **postProc**）；解压到 `pysat.params['data_dirs']`
- COSMIC-2 **IVM**（非 RO）：`cosmic2_ivm`（`inst_id` e1…e6）— 本手册只点名，未实跑

**不做：**

- **不是** Abel 反演引擎；读的是 CDAAC 已发布产品
- **不是** AWS 三型门户 → [awsgnssroutils](./awsgnssroutils.md)（`calibratedPhase` 有 excessPhase，**无** Ne / 无 `ionPhs` 文件名）
- **不是** JPL GENESIS 大气 L2 ASCII 批量器 → [cosmic-crunch](./cosmic-crunch.md)
- **不是** 地基双频 TEC / ROTI / GIM → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md) / [ionex-gim](./ionex-gim.md)

一句话：pysatCDAAC = **CDAAC COSMIC RO（含 ionPhs/ionPrf）的 pysat 插件**；Ne 走 `ionprf`，excess phase 走 `ionphs`（当前 load 有坑，见下）。

| 术语 | 含义 |
| --- | --- |
| `ionprf` / `ionPrf` | Level-2 电离层电子密度剖面（`ELEC_dens` el/cm³） |
| `ionphs` / `ionPhs` | Level-1b 电离层 excess phase（`exL1`/`exL2`，单位 m） |
| `atmprf` / `wetprf` | 大气剖面（无 Ne）；对照 cosmic-crunch / AWS atm |
| `podtec` / `scnlv1` | 绝对 TEC 辅助 / S4 闪烁；本机未拉 |
| `repro2013` → `postProc` | 下载优先再处理，失败回落事后处理 |
| `altitude_bin` | 仅对含 `MSL_alt` 的剖面标签有效；`ionphs`/`podtec`/`scnlv1` 禁用 |
| `cosmic2_ivm` | COSMIC-2 离子速度计，**不是** RO ionPrf |

### 开放 vs 门禁（本机实测）

| 路径 | 凭证 | 本机 |
| --- | --- | --- |
| `data.cosmic.ucar.edu/gnss-ro/...` 日包 | **无**（匿名 HTTPS） | `ionPrf_postProc_2019_001.tar.gz` 等 200 |
| `Instrument.download`（cosmic_gps） | **无** | 2019-01-01 `ionprf`/`ionphs` 均可下 |
| 旧 CDAAC 网页账号 | 门户表单 | **RO 直链可不登录**；见 [data-access RO](../data-access.md) |
| `cosmic2_ivm` | 同公开树 `cosmic2/postProc/.../ivmL2m_*.tar.gz` | 未实跑 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv-pysat && source .venv-pysat/bin/activate
python -m pip install -U pip
# 本机：pandas 3 / numpy 2 会踩 pysat 空文件列表 dtype='a'（见坑）
python -m pip install 'pysatCDAAC==0.0.5' 'pysat>=3.2.1' 'pandas==2.2.3'
python -c "import importlib.metadata as m; print(m.version('pysatCDAAC'), m.version('pysat'))"
# 期望：0.0.5 3.2.2（或相近 pysat 3.2.x）
```

首次使用须指定数据根（目录须已存在）：

```bash
mkdir -p ~/iono_ops/pysatData
python - <<'PY'
import pysat, os
pysat.params['data_dirs'] = os.path.expanduser('~/iono_ops/pysatData')
print(pysat.params['data_dirs'])
PY
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `pip install pysat-cdaac` 找不到 | 包名是 **`pysatCDAAC`** | 用正确 PyPI 名 |
| 启动提示要设 `data_dirs` | 未配置 | `pysat.params['data_dirs'] = '...'` |
| `TypeError: data type 'a' not understood` | pysat 3.2.2 × pandas3/numpy2 | 钉 `pandas==2.2.3`；或见坑 #2 补丁 |

## 3. 端到端：download → load ionprf（本机真跑）

### 3.1 构造 Instrument + 下 2019-01-01 ionPrf

```bash
source ~/iono_ops/.venv-pysat/bin/activate
python - <<'PY'
import pysat, datetime as dt, os
import pandas as pds
# 若仍遇 dtype='a'，取消下一补丁注释（本机 pandas 2.2.3 + numpy 2.5 仍需）
_orig = pds.Series.__init__
def _si(self, data=None, index=None, dtype=None, *a, **k):
    if dtype == 'a':
        dtype = object
    return _orig(self, data=data, index=index, dtype=dtype, *a, **k)
pds.Series.__init__ = _si

pysat.params['data_dirs'] = os.path.expanduser('~/iono_ops/pysatData')
from pysatCDAAC.instruments import cosmic_gps

inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionprf',
                        update_files=True, temporary_file_list=True)
print(inst)
start = dt.datetime(2019, 1, 1)
inst.download(start=start, stop=start)
inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionprf',
                        update_files=True, temporary_file_list=True)
print('nfiles', len(inst.files.files))
print(inst.files.files.head(2))
PY
```

**本机结果（2026-09-24 EDT，`pysatCDAAC` 0.0.5 / `pysat` 3.2.2）：**

```text
pysat.Instrument(platform='cosmic', name='gps', tag='ionprf', ...)
nfiles 59
2019-01-01 14:20:00.060200    2019/001/ionPrf_C006.2019.001.14.20.G02_2016.1...
2019-01-01 14:20:00.061200    2019/001/ionPrf_C006.2019.001.14.20.G12_2016.1...
```

下载 URL 逻辑（源码）：先试  
`.../repro2013/level2/2019/001/ionPrf_repro2013_2019_001.tar.gz`（本机 **404**）→ 替换为  
`.../postProc/level2/2019/001/ionPrf_postProc_2019_001.tar.gz`（本机 **200**，约 0.55 MB）。  
落地：`~/iono_ops/pysatData/cosmic/gps/ionprf/2019/001/ionPrf_C*.????_nc`。

### 3.2 load + 看 Ne

```bash
python - <<'PY'
import pysat, datetime as dt, os, numpy as np, pandas as pds
_orig = pds.Series.__init__
def _si(self, data=None, index=None, dtype=None, *a, **k):
    if dtype == 'a': dtype = object
    return _orig(self, data=data, index=index, dtype=dtype, *a, **k)
pds.Series.__init__ = _si
pysat.params['data_dirs'] = os.path.expanduser('~/iono_ops/pysatData')
from pysatCDAAC.instruments import cosmic_gps

inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionprf',
                        update_files=True, temporary_file_list=True,
                        clean_level='clean')
inst.load(date=dt.datetime(2019, 1, 1))
print(inst)
print('dims', dict(inst.data.sizes))
print('ELEC_dens', inst['ELEC_dens'].values.shape,
      float(np.nanmin(inst['ELEC_dens'])), float(np.nanmax(inst['ELEC_dens'])))
print('edmax[0]', float(inst['edmax'].values[0]),
      'edmaxalt[0]', float(inst['edmaxalt'].values[0]))
PY
```

**本机 stdout（截断）：**

```text
Platform: 'cosmic'
Name: 'gps'
Tag: 'ionprf'
Cleaning Level: 'clean'
Number of files: 59
Date: 01 January 2019
Time range: 01 January 2019 14:20:41 --- 01 January 2019 23:41:07
Number of Times: 53
Number of variables: 58
dims {'time': 53, 'RO': 502}
ELEC_dens (53, 502) 1131.7281494140625 817363.6875
edmax[0] 589629.7947462643 edmaxalt[0] 196.92424521491316
```

对照：`clean_level='none'` 本机 **59** 时次；`clean` 后 **53**。原始 nc：`ELEC_dens` units=`el/cm3`。

### 3.3 ionphs：下载成功，全日 load 失败（诚实记录）

```bash
python - <<'PY'
import pysat, datetime as dt, os, pandas as pds
_orig = pds.Series.__init__
def _si(self, data=None, index=None, dtype=None, *a, **k):
    if dtype == 'a': dtype = object
    return _orig(self, data=data, index=index, dtype=dtype, *a, **k)
pds.Series.__init__ = _si
pysat.params['data_dirs'] = os.path.expanduser('~/iono_ops/pysatData')
from pysatCDAAC.instruments import cosmic_gps
from netCDF4 import Dataset
from pathlib import Path
import numpy as np

inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionphs',
                        update_files=True, temporary_file_list=True,
                        clean_level='none')
inst.download(start=dt.datetime(2019,1,1), stop=dt.datetime(2019,1,1))
inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionphs',
                        update_files=True, temporary_file_list=True)
print('nfiles', len(inst.files.files))
# 全日 load 本机报错（勿指望）：
# ValueError: conflicting sizes for dimension 'RO': length 7 on 'qc_heights' ...
root = Path(os.path.expanduser('~/iono_ops/pysatData/cosmic/gps/ionphs'))
p = sorted(root.rglob('*_nc'))[0]
ds = Dataset(p)
print(p.name, 'size', p.stat().st_size)
print('vars', list(ds.variables.keys()))
for k in ['exL1', 'exL2', 'caL1Snr', 'pL2Snr']:
    v = ds.variables[k][:]
    print(k, 'len', len(v), 'min', float(np.nanmin(v)), 'max', float(np.nanmax(v)),
          'units', getattr(ds.variables[k], 'units', None))
ds.close()
PY
```

**本机：**

```text
nfiles 144
ionPhs_C006.2019.001.14.20.G02_2016.1120_nc size 231032
vars ['time', 'caL1Snr', 'pL1Snr', 'pL2Snr', 'xLeo', ..., 'exL1', 'exL2', 'exLC',
      'occheight', 'qc_heights', 'nspikes', 'maxspike']
exL1 len 1565 min 0.0 max 11092.410616762936 units m
exL2 len 1565 min 0.0 max 11092.13374889642 units m
caL1Snr len 1565 min 270.0 max 682.0 units None
pL2Snr len 1565 min 48.0 max 299.0 units None
```

要点：`qc_heights` 等短数组与 `exL1` 长时序被 `load_files` 强行塞进同一维 `RO` → **即使单文件 `cosmic_gps.load([path])` 也炸**。excess phase 分析请 **netCDF4/xarray 直接读**；或等上游修。

### 3.4 可选：`altitude_bin`（仅 ionprf 等）

```python
inst = pysat.Instrument(inst_module=cosmic_gps, tag='ionprf',
                        update_files=True, temporary_file_list=True,
                        clean_level='none', altitude_bin=10)
inst.load(date=dt.datetime(2019, 1, 1))
# 本机：dims time=59, RO=300；新增坐标 MSL_bin_alt（例 30,40,...,100 km）
```

## 4. I/O 字段

| 路径 / 字段 | 含义 |
| --- | --- |
| `pysatData/cosmic/gps/ionprf/YYYY/DDD/*.????_nc` | 解压后的 ionPrf 单掩星文件 |
| `pysatData/cosmic/gps/ionphs/YYYY/DDD/*.????_nc` | ionPhs 单掩星文件 |
| `ELEC_dens` | 电子密度 **el/cm³**（非 m⁻³） |
| `MSL_alt` | 近地点海拔 km |
| `TEC_cal` | 校准掩星 TEC（TECU）；沿剖面 |
| `edmax` / `edmaxalt` | 峰值 Ne / 峰值高度（全局属性→列） |
| `GEO_lat` / `GEO_lon` / `OCC_azi` | 切点地理坐标 / 方位 |
| `exL1` / `exL2` / `exLC` | L1/L2/组合 excess phase（m） |
| `caL1Snr` / `pL1Snr` / `pL2Snr` | SNR |
| `qc_heights` / `nspikes` / `maxspike` | ionPhs QC 短数组（触发 load 冲突） |

## 5. 参数（常用）

| API / 旗标 | 作用 | 本机注意 |
| --- | --- | --- |
| `tag='ionprf'\|'ionphs'\|...` | 产品类型 | 必须小写；文件名驼峰由翻译表生成 |
| `clean_level='clean'\|'none'` | ionprf 质控 | clean 会丢剖面（59→53） |
| `altitude_bin=N` | 高度分箱 km | ionphs 等会 `ValueError` |
| `download(start, stop)` | 拉日包 | 窗勿过大；优先小日冒烟 |
| `update_files=True` | 重扫本地文件 | 下载后重建 Instrument |
| `temporary_file_list=True` | 不写持久文件列表 | 调试方便 |
| `pysat.utils.registry.register(...)` | 注册后用 `Instrument('cosmic','gps',tag=...)` | 可选 |

完整标签表：源码 `cosmic_gps.tags` / `tag_translation`。

## 6. 接到哪步

1. **电离层 Ne 剖面（CDAAC）**：本手册 `tag='ionprf'` → 气候态/暴时统计；单位注意 **cm⁻³** ↔ 模型 **m⁻³**（×1e6）。
2. **电离层 excess phase（CDAAC 文件名）**：下载用本包；**读字段用 netCDF4**（见 3.3）。AWS 同物理量近似入口 → [awsgnssroutils](./awsgnssroutils.md) `calibratedPhase.excessPhase`（无 Ne）。
3. **大气 RO**：本包 `atmprf`/`wetprf` 或 [cosmic-crunch](./cosmic-crunch.md) / AWS `atmosphericRetrieval` — **勿与 ionPrf 混 QC**。
4. **门户与直链说明**：[data-access 掩星 RO](../data-access.md)。
5. **地基 TEC 主链**：与本包无关 → 路径 A。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 当 Abel / 自研反演 | 包只读产品 | 要算法另找；本包=阅读器 |
| 2 | `dtype 'a' not understood` | pysat 空 Series × 新 numpy | 钉 pandas 2.2.x 或 Series 补丁把 `'a'`→`object` |
| 3 | `ionphs` `Instrument.load` / 单文件 `load` 炸 | `qc_heights` 与 `exL1` 维长冲突 | netCDF4 直读；勿硬堆全日 |
| 4 | 2014-05-01 等测试日落空 | repro2013 某 DOY 404 | 换有货日（本机用 2019-01-01 postProc） |
| 5 | 以为必须 CDAAC 登录 | 旧文档 | `data.cosmic` 匿名；见 data-access |
| 6 | `ELEC_dens` 和 IRI m⁻³ 差 10⁶ | 单位 el/cm³ | 换算后再比 [pyiri](./pyiri.md)/[iri2016](./iri2016.md) |
| 7 | `altitude_bin` + ionphs | 无 `MSL_alt` | 只对 ionprf/atm/wet 等开 |
| 8 | 与 AWS `calibratedPhase` 文件名混用 | 产品树不同 | CDAAC=`ionPhs`；AWS=三型 API 名 |
| 9 | 与 cosmic-crunch L2 硬拼 Ne | GENESIS 是大气 | 看 `ParameterName`；Ne 只用 ionPrf |
| 10 | `clean` 后 edmax 仍有 NaN | 质控只丢部分坏廓线 | 统计前再掩膜；或 `clean_level='none'` 自滤 |
| 11 | 把 `cosmic2_ivm` 当 RO | IVM≠掩星 | 电离层 RO 仍用 cosmic_gps 标签 |
| 12 | 预 1.0 行为变 | 包标注 pre-1.0.0 | 锁版本 `==0.0.5`；升级后重跑冒烟 |

## 8. 选型

| 你要… | 打开 |
| --- | --- |
| CDAAC **ionPrf Ne** /（下载）**ionPhs** 进 pysat | **本手册 pysatCDAAC** |
| AWS 批量查/下 **calibratedPhase**（无 Ne） | [awsgnssroutils](./awsgnssroutils.md) |
| GENESIS COSMIC-1 **大气** L2→netCDF | [cosmic-crunch](./cosmic-crunch.md) |
| 门户 / 直链说明 | [data-access RO](../data-access.md) |
| 地基校准 TEC | [pytecgg](./pytecgg.md) |

相关：[data-access](../data-access.md) · [awsgnssroutils](./awsgnssroutils.md) · [cosmic-crunch](./cosmic-crunch.md) · [README](./README.md) · [`PROJECTS.json`](../../PROJECTS.json)
