# PyIRTAM · 纯 Python IRTAM 同化电离层操作手册

目录：[`PROJECTS.json` → `PyIRTAM`](../../PROJECTS.json) · 上游 <https://github.com/victoriyaforsythe/PyIRTAM> · 许可 **MIT** · PyPI **`PyIRTAM` 0.0.7** · 本机验证：LGDC 下 2024-06-01 02:15 四系数 → `run_PyIRTAM` 20° 网格，0°E/10°N 处 IRTAM NmF2≈3.00e11、hmF2≈294 km（相对同点 PyIRI 气候态升高）（2026-09-24 EDT）

> 岗位：把 **GIRO/GAMBIT IRTAM 系数** 接到 Python，与气候态 **PyIRI** 同网格同日对照 foF2/hmF2/EDP。冲突时：**仓内 `docs/tutorials/*.ipynb` / ReadTheDocs > 本文**。

## 1. 用途与边界

**做：**

- `PyIRTAM.coeff.download_irtam_coeffs`：从 LGDC/GAMBIT 拉 `foF2`/`hmF2`/`B0`/`B1` 15 min 系数 ASC
- `PyIRTAM.run_PyIRTAM`：同一次调用里算 **PyIRI 气候态 + IRTAM 同化态** 的 F2/F1/E/Es 与 EDP
- 网格与 PyIRI 一致：`alon`/`alat` 一维展平；`aalt` 高度 km；`aUT`/`ahr` 十进制小时

**不做：**

- **不是** 气候态 IRI 本体 → 兄弟 **[pyiri](./pyiri.md)**（纯 Python）/ **[iri2016](./iri2016.md)**（QA，Fortran）/ **[pyglow](./pyglow.md)**（QA，多模型）
- **不是** 官方 `irirtam.for` 逐行移植；金标准对照请走 IRI-2020 包内 IRTAM 子程序
- **不** 替代当日 GIM TEC 产品 → [ionex-gim](./ionex-gim.md)；概念课 [04](../tutorials/04-iri-nequick.md)
- LGDC 接口有访问节奏；勿高频扫全日所有 15 min 槽

一句话：PyIRTAM = **IRTAM 系数 → 全球/区域网格电子密度**（纯 Python，对接 PyIRI）。

| 术语 | 含义 |
| --- | --- |
| IRTAM | IRI Real-Time Assimilative Mapping（GIRO 同化） |
| `irtam_dir` | 系数根目录；`''`→包内 `PyIRTAM/irtam_coeffs` |
| `use_subdirs` | `True`→`YYYY/MMDD/`；`False`→系数直接在 `irtam_dir` |
| `download` | `run_PyIRTAM(..., download=True)` 缺文件时现拉 |
| `f2_iri` / `f2_irtam` | 同网格气候态 vs 同化态 F2 字典 |
| `EDP` | 形状 `(nUT, nalt, ngrid)`，单位 m⁻³ |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv-pyirtam && source .venv-pyirtam/bin/activate
python -m pip install -U pip
# 依赖 PyIRI≥气候态接口；锁与本机一致更稳
python -m pip install 'PyIRI==0.1.7' 'PyIRTAM==0.0.7'
# 或：git clone https://github.com/victoriyaforsythe/PyIRTAM.git && pip install -e ./PyIRTAM
python -c "import PyIRTAM, PyIRI; print(PyIRTAM.__version__, PyIRI.__version__)"
# 期望：0.0.7 0.1.7
```

依赖要点：`numpy`、`PyIRI`、`requests`。Python **≥3.10**。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ModuleNotFoundError: PyIRI` | 未装气候态后端 | `pip install 'PyIRI==0.1.7'` |
| `scipy` 过旧 | PyIRI 声明 ≥1.15 | `pip install 'scipy>=1.15'` |
| 可写包内 `irtam_coeffs` 失败 | 系统 site-packages 只读 | 自建 `irtam_dir=~/iono_ops/irtam_coeffs` |

## 3. 端到端：下载系数 + 重建（本机真跑）

场景对齐上游 `docs/tutorials/PyIRTAM_with_download.ipynb`（缩网格加速）：2024-06-01 02:15 UT，F10.7=90.8，20°×20° 全球网格。

### 3.1 拉四个参数系数

```bash
source ~/iono_ops/.venv-pyirtam/bin/activate
mkdir -p ~/iono_ops/pyirtam_e2e/irtam_coeffs
python - <<'PY'
import datetime as dt
from PyIRTAM import coeff

dtime = dt.datetime(2024, 6, 1, 2, 15, 0)
irtam_dir = "irtam_coeffs"  # 相对 cwd；或绝对路径
for param in ["foF2", "hmF2", "B0", "B1"]:
    dstat, fstat, msg = coeff.download_irtam_coeffs(
        dtime, param, irtam_dir=irtam_dir, use_subdirs=True, overwrite=True)
    print(param, "downloaded=", dstat, "exists=", fstat, "msg=", repr(msg))
PY
# 期望文件约 18 KB×4：
# irtam_coeffs/2024/0601/IRTAM_{foF2,hmF2,B0in,B1in}_COEFFS_20240601_021500.ASC
```

**本机（2026-09-24 EDT）：** 四参数 `downloaded=True exists=True`；源 `https://lgdc.uml.edu/rix/gambit-coeffs`。

### 3.2 `run_PyIRTAM`：IRI vs IRTAM

```bash
python - <<'PY'
import numpy as np
import PyIRI.main_library as ml
import PyIRTAM

year, month, day = 2024, 6, 1
ahr = np.array([2 + 15 / 60.0])   # 十进制小时
f107 = 90.8
alon, alat, _, _ = ml.set_geo_grid(20, 20)   # 展平 1-D
aalt = np.arange(90, 501, 20)
irtam_dir = "irtam_coeffs"

(f2_iri, f1_iri, e_iri, es_iri, sun, mag, edp_iri,
 f2_irtam, f1_irtam, e_irtam, es_irtam, edp_irtam) = PyIRTAM.run_PyIRTAM(
    year, month, day, ahr, alon, alat, aalt, f107,
    irtam_dir=irtam_dir, use_subdirs=True, download=False)

idx = int(np.argmin((alon - 0.0) ** 2 + (alat - 20.0) ** 2))
Nm_i, hm_i = float(f2_iri["Nm"][0, idx]), float(f2_iri["hm"][0, idx])
Nm_t, hm_t = float(f2_irtam["Nm"][0, idx]), float(f2_irtam["hm"][0, idx])
fo_i = float(f2_iri["fo"][0, idx])
fo_t = (Nm_t / 1.24e10) ** 0.5          # IRTAM 字典无 fo，自算
tec_i = float(np.trapezoid(edp_iri[0, :, idx], aalt * 1e3) / 1e16)
tec_t = float(np.trapezoid(edp_irtam[0, :, idx], aalt * 1e3) / 1e16)
print("version", PyIRTAM.__version__)
print("point lon,lat", float(alon[idx]), float(alat[idx]))
print(f"IRI   foF2={fo_i:.4f} hmF2={hm_i:.2f} NmF2={Nm_i:.6e} vTEC={tec_i:.3f}")
print(f"IRTAM foF2~={fo_t:.4f} hmF2={hm_t:.2f} NmF2={Nm_t:.6e} vTEC={tec_t:.3f}")
print("EDP_shapes", edp_iri.shape, edp_irtam.shape)
print("IRTAM_F2_keys", sorted(f2_irtam.keys()))
PY
```

**本机 stdout（2026-09-24 EDT，`PyIRTAM` 0.0.7 / `PyIRI` 0.1.7）：**

```text
version 0.0.7
point lon,lat 0.0 10.0
IRI   foF2=3.9284 hmF2=276.66 NmF2=1.913591e+11 vTEC=2.665
IRTAM foF2~=4.9219 hmF2=294.22 NmF2=3.003884e+11 vTEC=5.063
EDP_shapes (1, 21, 190) (1, 21, 190)
IRTAM_F2_keys ['B0', 'B1', 'B_top', 'Nm', 'hm']
```

| 字段 | 含义 |
| --- | --- |
| `point … 0.0 10.0` | 20° 网格上距 (0°E,20°N) 最近格点落在 10°N |
| `IRTAM_F2_keys` | **无 `fo`/`M3000`**；`fo≈sqrt(Nm/1.24e10)` |
| `vTEC_*` | 粗梯形积分（取决于 `aalt`），非 IONEX |
| 返回 12 元组 | 前 7 个偏 IRI/太阳磁；后 5 个为 IRTAM F2/F1/E/Es/EDP |

### 3.3 常用参数

| 参数 | 作用 |
| --- | --- |
| `irtam_dir` | 系数根；空串=包内目录 |
| `use_subdirs` | 是否 `YYYY/MMDD`；与下载时一致 |
| `download` | 缺文件时自动 `download_irtam_coeffs` |
| `F107` / `f107` | 当日 F10.7（SFU），驱动气候态支路 |
| `aUT`/`ahr` | UT 小时数组；须覆盖已下载的 15 min 槽 |

## 4. 接到哪步

- 只要气候态背景 → [pyiri](./pyiri.md)；要 Fortran IRI-2016 → [iri2016](./iri2016.md)（QA）；多模型上层 → [pyglow](./pyglow.md)（QA）
- 同化 vs 气候对照 → **本文**；当日 TEC 图 → [ionex-gim](./ionex-gim.md)
- 教程 [04](../tutorials/04-iri-nequick.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `KeyError: 'fo'` 读 `f2_irtam` | IRTAM F2 只有 `Nm/hm/B0/B1/B_top` | `fo = (Nm/1.24e10)**0.5` |
| 2 | `IOError: unknown IRTAM coefficient file` | 路径/`use_subdirs` 与落盘不一致 | 下载与 `run_PyIRTAM` 用同一 `irtam_dir`+`use_subdirs` |
| 3 | `download=True` 极慢 / 被拒 | 全日 96 槽×4 参数打 LGDC | 先只拉需要的 `dtime`；遵守站点节奏 |
| 4 | `alon`/`alat` 维数错 | 未展平 | `ml.set_geo_grid` 或 `.ravel()` |
| 5 | 与 pyiri 单点手册数字不同 | 日期/F10.7/网格不同 | 锁同一 `year/month/day/F107/alon/alat` |
| 6 | `VTEC`/`MUF3000` 下载失败 | LGDC 声称支持但实测挂 | 只用 `foF2/hmF2/B0/B1` |
| 7 | 把 IRTAM 当「全球真值 TEC」 | 同化仍依赖测高仪覆盖 | 并列 [ionex-gim](./ionex-gim.md)/双频 TEC |
| 8 | 与官方 irirtam 差一截 | 非逐行移植 + EDP 跟 PyIRI 架构 | 论文对比写明软件版本；金标准走 Fortran |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| IRTAM 系数 + 同化 EDP（纯 Python） | **本文 PyIRTAM** |
| 纯 Python 气候 IRI | [pyiri](./pyiri.md) |
| Fortran IRI-2016 → xarray | [iri2016](./iri2016.md)（QA） |
| 多模型上层大气 | [pyglow](./pyglow.md)（QA） |
| 读 IONEX GIM | [ionex-gim](./ionex-gim.md) |

- 文档：<https://pyirtam.readthedocs.io/>
- 教程：<https://github.com/victoriyaforsythe/PyIRTAM/tree/main/docs/tutorials>
- DOI：<https://doi.org/10.5281/zenodo.10844521>
- LGDC：<https://lgdc.uml.edu/rix/gambit-coeffs>
- 兄弟：[pyiri](./pyiri.md) · [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [ionex-gim](./ionex-gim.md) · 教程 [04](../tutorials/04-iri-nequick.md)
