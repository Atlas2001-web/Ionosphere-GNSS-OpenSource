# PyIRI · 纯 Python IRI 气候模型操作手册

目录：[`PROJECTS.json` → `PyIRI`](../../PROJECTS.json) · 上游 <https://github.com/victoriyaforsythe/PyIRI> · 许可 **MIT**（`LICENSE`；`pyproject` classifier 误写 BSD，以 LICENSE 为准）· PyPI **`PyIRI` 0.1.7** · 本机验证：`sh.IRI_density_1day` 单点 2020-04-01 / F10.7=100 → UT12 NmF2≈1.942e12、vTEC≈43.2 TECU（2026-09-24 EDT） · **质检复跑通过**（同 I/O）

> 岗位：不绑 Fortran，在 Python 里算 IRI 气候态 **Nm/hm/fo、EDP、近似 vTEC**，作 GNSS TEC/GIM 对照背景。冲突时：**仓内 `docs/tutorials/*.py` / ReadTheDocs > 本文**。

## 1. 用途与边界

**做：**

- `PyIRI.sh_library.IRI_density_1day`：球谐（SH）架构，一日全 UT × 网格 × 高度 → F2/F1/E/Es + EDP
- 坐标：`GEO` / `QD` / `MLT`；foF2 系数 `CCIR`/`URSI`；hmF2 `SHU2015`/`AMTB2013`/`BSE1979`
- 捆带 `coefficients/`（CCIR、URSI、SH、IGRF、Es、Apex）；`coeff_dir=None` 用包内默认
- 旧路径 `PyIRI.edp_update`（Fourier/经验；`coeff_dir` **必填位置参**）

**不做：**

- **不是** 当天实况 / 同化天气场 → 对照用 [ionex-gim](./ionex-gim.md) 读 GIM；概念见教程 [04](../tutorials/04-iri-nequick.md)
- **不是** Galileo 单频 NeQuick-G → [nequickg](./nequickg.md)
- **不是** 官方 IRI-2016/2020 Fortran 数值金标准封装 → 兄弟手册 **[iri2016](./iri2016.md)**（QA）；上层大气多模型包装 → **[pyglow](./pyglow.md)**（QA）。本文不重复其安装/旗标
- **不** 做闪烁/暴时物理；强扰动期只作气候下限，勿当真值

一句话：PyIRI = **纯 Python IRI 气候学实现**（SH 为主），便于嵌进科研脚本。

| 术语 | 含义 |
| --- | --- |
| `aUT` | 世界时数组（小时，可小数） |
| `alon` / `alat` | **一维**展平经/纬（度）；先 `ravel` |
| `aalt` | 高度网格（km） |
| `F107` | 日 F10.7（SFU）；`IRI_density_1day` 驱动 |
| `F2['Nm']`/`hm`/`fo` | F2 峰密度 (m⁻³)、峰高 (km)、临界频率 (MHz) |
| `EDP` | 电子密度廊线；本机形状 `(nUT, nalt, ngrid)` |
| `old_output` | `False`→7 元组含 `Es`；默认仍偏旧 6 元组（0.2+ 将改） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/victoriyaforsythe/PyIRI.git
cd PyIRI
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
# 或：pip install 'PyIRI==0.1.7'
python -c "import PyIRI; print(PyIRI.__version__)"
# 期望：0.1.7
```

依赖要点：`numpy`、`scipy>=1.15`、`pandas`、`matplotlib`、`netCDF4`、`fortranformat`、`opt_einsum`。Python **≥3.10**。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `scipy` 版本过旧 | 声明 ≥1.15 | `pip install 'scipy>=1.15'` |
| `ModuleNotFoundError: PyIRI` | 未进 venv / 未 editable | `source .venv && pip install -e .` |
| 缺系数文件 | 只拷了 `.py` | 用完整包/`pip install PyIRI`（含 `coefficients/`） |

## 3. 端到端：单点一日 EDP + vTEC（本机真跑）

场景对齐上游 `docs/tutorials/Single_location.py`（缩网格加速）：2020-04-01，10°E/20°N，F10.7=100，CCIR + SHU2015。

### 3.1 SH：`IRI_density_1day`

```bash
cd ~/iono_ops/PyIRI && source .venv/bin/activate
python - <<'PY'
import numpy as np
import PyIRI
import PyIRI.sh_library as sh

year, month, day = 2020, 4, 1
F107 = 100.0
alon = np.array([10.0])          # 必须 1-D
alat = np.array([20.0])
aUT = np.arange(0, 24, 1.0)      # 小时
aalt = np.arange(90, 701, 10)    # km；本例 62 层

# old_output=False → 7 返回值（含 Es）；勿按 7 去解包默认旧行为
F2, F1, E, Es, sun, mag, EDP = sh.IRI_density_1day(
    year, month, day, aUT, alon, alat, aalt, F107,
    coeff_dir=None,
    foF2_coeff="CCIR",
    hmF2_model="SHU2015",
    coord="GEO",
    old_output=False,
)

iut = list(aUT).index(12)
prof = EDP[iut, :, 0]            # (nUT, nalt, ngrid)
tec = float(np.trapezoid(prof, aalt * 1e3) / 1e16)
print("version", PyIRI.__version__)
print("EDP_shape", EDP.shape)
print(f"UT12 NmF2={float(F2['Nm'][iut,0]):.6e} "
      f"hmF2_km={float(F2['hm'][iut,0]):.2f} "
      f"foF2_MHz={float(F2['fo'][iut,0]):.4f}")
print(f"UT12 NmE={float(E['Nm'][iut,0]):.4e} hmE_km={float(E['hm'][iut,0]):.2f}")
print(f"UT12 NmEs={float(Es['Nm'][iut,0]):.4e}")
print(f"UT12 Ne_min={prof.min():.4e} Ne_max={prof.max():.4e}")
print(f"vTEC_trapz_TECU={tec:.3f}")
print(f"NmF2_day_min={F2['Nm'][:,0].min():.4e} "
      f"NmF2_day_max={F2['Nm'][:,0].max():.4e}")
print("F2_keys", sorted(F2.keys()))
print("mag_modip_deg", float(mag["modip"][0]))
PY
```

**本机 stdout（2026-09-24 EDT，`PyIRI` 0.1.7）：**

```text
version 0.1.7
EDP_shape (24, 62, 1)
UT12 NmF2=1.941519e+12 hmF2_km=364.62 foF2_MHz=12.5130
UT12 NmE=1.5508e+11 hmE_km=110.00
UT12 NmEs=1.7354e+11
UT12 Ne_min=1.0957e+10 Ne_max=1.9386e+12
vTEC_trapz_TECU=43.194
NmF2_day_min=1.7562e+11 NmF2_day_max=2.1762e+12
F2_keys ['B0', 'B1', 'B_bot', 'B_top', 'M3000', 'Nm', 'fo', 'hm']
mag_modip_deg 21.55441907468987
```

| 字段 | 含义 |
| --- | --- |
| `EDP_shape (24,62,1)` | 24 UT × 62 高度 × 1 网格点 |
| `NmF2` / `hmF2` / `foF2` | F2 峰；`fo` 单位 MHz |
| `vTEC_trapz_TECU` | ∫ Ne dh / 1e16；**粗积分**（取决于 `aalt` 步长），非 IONEX 产品 |
| `mag['modip']` | 修正磁倾角（度） |
| `Es` | 偶发 E；需 `old_output=False` |

### 3.2 旗标 / 关键参数

| 参数 | 作用 |
| --- | --- |
| `foF2_coeff` | `'CCIR'` 或 `'URSI'`（默认 URSI） |
| `hmF2_model` | `'SHU2015'`（默认）/ `'AMTB2013'` / `'BSE1979'` |
| `coord` | `'GEO'` / `'QD'` / `'MLT'` |
| `coeff_dir` | 系数根目录；`None`=包内 |
| `old_output` | `False` 返回 Es；默认 `None`≈旧 6 出参（有 FutureWarning） |
| `F107` | 仅 `IRI_density_1day`；月均接口是 `solidx`/`solmin`/`solmax`（见坑） |

### 3.3 与 GIM / NeQuick 对照口径

```text
PyIRI vTEC（气候、单点积分）  ≠  IONEX GIM 当日图  ≠  NeQuick-G 广播改正
```

读 GIM → [ionex-gim](./ionex-gim.md)；NeQuick-G → [nequickg](./nequickg.md)；机制课 → [04-iri-nequick](../tutorials/04-iri-nequick.md)。

## 4. 接到哪步

- 气候背景 / 论文「相对 IRI」→ 本文；要 **Fortran IRI-2016 接口** → [iri2016](./iri2016.md)（QA）；多模型 Python 上层 → [pyglow](./pyglow.md)（QA）
- 当日 TEC 图对照 → [ionex-gim](./ionex-gim.md)；Galileo 单频 → [nequickg](./nequickg.md)
- 教程 [04](../tutorials/04-iri-nequick.md)；GIM 课 [03](../tutorials/03-gim-ionex.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ValueError: not enough values to unpack (expected 7, got 6)` | 默认仍 6 出参 | `old_output=False` 再解包 7 元组 |
| 2 | `FutureWarning: old_output … will change` | 0.2+ 默认将翻 | 显式传 `old_output=False`（或 True） |
| 3 | `IndexError: too many indices for array`（1-D） | `alon`/`alat` 仍是 2-D | `alon = alon_2d.ravel()` |
| 4 | `EDP[iut,0,:]` 值几乎常数 / TEC≈0 | 轴序是 `(nUT,nalt,ngrid)` | 用 `EDP[iut, :, igrid]` |
| 5 | `IRI_monthly_mean_par(..., F107=100)` 或位置传 F107 | API 是 `solidx`/`solmin`/`solmax` | 读 `inspect.signature`；日廓线用 `IRI_density_1day` |
| 6 | `UnboundLocalError: F107min`（月均） | 0.1.7 月均路径缺陷 | 避开月均；用 `IRI_density_1day`；或升版本后重试 |
| 7 | `edp_update.IRI_density_1day() missing coeff_dir` | 旧模块 **位置参必填** | 传包内系数目录，或改走 `sh_library` |
| 8 | 把结果当「今天 TEC 真值」 | 气候态≠天气 | 并列 [ionex-gim](./ionex-gim.md) / 双频 TEC；暴期降权 |
| 9 | 与 pyglow/iri2016 数字对不齐 | 版本/系数/选项族不同 | 对照时锁同一 foF2/hmF2/F10.7；金标准见 QA 手册 |
| 10 | `vTEC` 随 `aalt` 步长漂 | 粗梯形积分 | 加密 `aalt`；报告时写明积分限与步长 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 纯 Python IRI 气候 / 脚本嵌入 | **本文 PyIRI** |
| Fortran IRI-2016 包装 | [iri2016](./iri2016.md)（QA） |
| 多模型上层大气 Python | [pyglow](./pyglow.md)（QA） |
| Galileo NeQuick-G | [nequickg](./nequickg.md) |
| 读 IONEX GIM | [ionex-gim](./ionex-gim.md) |

- 文档：<https://pyiri.readthedocs.io/>
- 教程脚本：<https://github.com/victoriyaforsythe/PyIRI/tree/main/docs/tutorials>
- DOI：<https://doi.org/10.5281/zenodo.8235172>
- 兄弟：[nequickg](./nequickg.md) · [ionex-gim](./ionex-gim.md) · [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · 教程 [04](../tutorials/04-iri-nequick.md)
