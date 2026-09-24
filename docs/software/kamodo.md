# Kamodo · NASA CCMC 日地模式输出函数化操作手册

目录：[`PROJECTS.json` → `Kamodo`](../../PROJECTS.json) · 上游 <https://github.com/nasa/Kamodo> · core <https://github.com/nasa/Kamodo-core> · 文档 <https://nasa.github.io/Kamodo/> · 许可 **NASA-Open** · PyPI **`kamodo-ccmc` 26.9.2**（拉 **`kamodo-core-official` 26.8.7**）· 本机：core 组合 + CCMC 样例 **SWMF_IE** 实插（2026-09-24 04:45 EDT）

> 岗位：把 GITM / TIEGCM / IRI / **SWMF_IE** / NRLMSIS 等模式输出**函数化**（插值、单位、飞越）。冲突时：**上游 README / `Model_Variables` 本机打印 > 本文**。气候态 IRI → [iri2016](./iri2016.md) / [pyiri](./pyiri.md)；中性大气 → [msise00](./msise00.md)；**不是**从 GNSS 解算 TEC。

## 1. 用途与边界

**做：**

- `from kamodo import Kamodo`：任意场 → 可组合函数（core）
- `kamodo_ccmc.flythrough.model_wrapper`：`Model_Reader` / `Model_Variables` / `File_Times` / 飞越
- 本机 `Choose_Model("")` 含 IRI、NRLMSIS、GITM、TIEGCM、WACCMX、CTIPe、**SWMF_IE/GM**、Weimer、DTM、ADELPHI、AMGeO、SuperDARN、OpenGGCM、WAMIPE、VERB-3D、Ovation-Prime 等
- 样例包：<https://ccmc.gsfc.nasa.gov/publicData/KAMODO_TestData/>

**不做：**

- **不是** RINEX→TEC / GIM → [pytecgg](./pytecgg.md) / [ionex-gim](./ionex-gim.md) / [ionex-rs](./ionex-rs.md)
- **不是** 无文件 IRI/msis 一键气候态 → [iri2016](./iri2016.md) / [msise00](./msise00.md)（Kamodo reader 要**已写出的模式目录**）
- **勿** `pip install kamodo`（旧发行与 `kamodo-ccmc` / `kamodo-core-official` 冲突）

一句话：Kamodo = **CCMC 模式输出的统一函数化 API**。

| 术语 | 含义 |
| --- | --- |
| `kamodo-ccmc` | 读者生态（推荐 PyPI 入口） |
| `kamodo-core-official` | 核心：`from kamodo import Kamodo` |
| `*_ijk(time, lon, lat)` | 网格插值；`time` 多为文件日起的**小时** |
| `file_dir` | **目录**（建议末尾 `/`） |

## 2. 安装

建议 ≥16 GB RAM。独立 venv：

```bash
mkdir -p ~/iono_ops/kamodo-demo && cd ~/iono_ops/kamodo-demo
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip setuptools wheel
pip install 'kamodo-ccmc==26.9.2'
python -c "import importlib.metadata as m; from kamodo import Kamodo; print(m.version('kamodo-ccmc'), m.version('kamodo-core-official'), float(Kamodo(rho='x**2').rho(3)))"
# 期望：26.9.2 26.8.7 9.0
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 与旧 `kamodo` 23.x 打架 | 错入口 | 新建 venv，只装 `kamodo-ccmc` |
| `N is a reserved name` | 保留符号 | 换名（如 `n`） |
| IRI `.tgz` 太大 | 测试包数百 MB–GB | 先用 **SWMF_IE.tgz**（~60 MB） |

## 3. 端到端 A：core 组合（本机真跑）

```bash
cd ~/iono_ops/kamodo-demo && source .venv/bin/activate
python - <<'PY'
from kamodo import Kamodo
k = Kamodo(rho='x**2')
k['n'] = '3*rho'
print('rho(3)', float(k.rho(3)))
print('n(3)', float(k.n(3)))
print('keys', list(k))
PY
```

**本机 stdout（2026-09-24 04:45 EDT，core 26.8.7）：**

```text
rho(3) 9.0
n(3) 27.0
keys [rho(x), rho, n(x), n]
```

## 4. 端到端 B：SWMF_IE 插值（本机真跑）

```bash
cd ~/iono_ops/kamodo-demo && source .venv/bin/activate
mkdir -p TestData && cd TestData
curl -fL -o SWMF_IE.tgz https://ccmc.gsfc.nasa.gov/publicData/KAMODO_TestData/SWMF_IE.tgz
tar -xzf SWMF_IE.tgz && find SWMF_IE -name '._*' -delete && cd ..
python - <<'PY'
import numpy as np
from pathlib import Path
import importlib.metadata as m
import kamodo_ccmc.flythrough.model_wrapper as MW
d = str(Path('TestData/SWMF_IE').resolve()) + '/'
print('ccmc', m.version('kamodo-ccmc'), 'core', m.version('kamodo-core-official'))
MW.File_Times('SWMF_IE', d)
kam = MW.Model_Reader('SWMF_IE')(d, variables_requested=['Sigma_H','Sigma_P','phi','Phi_E'])
print('model', kam.modelname, 'filedate', kam.filedate)
print('Sigma_H', float(kam.Sigma_H_ijk(12.0, 0.0, 70.0)))
print('Sigma_P', float(kam.Sigma_P_ijk(12.0, 0.0, 70.0)))
print('phi_kV', float(kam.phi_ijk(12.0, 0.0, 70.0)))
print('Phi_E', float(kam.Phi_E_ijk(12.0, 0.0, 70.0)))
g = kam.Sigma_H_ijk(np.array([0.,12.,23.]), np.array([0.]), np.array([70.]))
print('Sigma_H_grid', [float(x) for x in np.asarray(g).ravel()])
PY
```

**本机 stdout（节选）：**

```text
ccmc 26.9.2 core 26.8.7
UTC time ranges
------------------------------------------
Start Date: 2008-05-02  Time: 00:00:00
End Date: 2008-05-02  Time: 23:00:00
model SWMF_IE filedate 2008-05-02 00:00:00+00:00
Sigma_H 9.1183
Sigma_P 7.6589
phi_kV -1.7879
Phi_E 1e-17
Sigma_H_grid [8.1299, 9.1183, 8.3571]
```

`Model_Variables('SWMF_IE')` 另有 `j_*`/`E_*`/`v_*`/`W_JouleH`；`IRI` → `N_e`/`TEC`/`NmF2`；`NRLMSIS` → `T_n`/`rho`（均需对应输出目录）。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| 模式输出目录 | SWMF_IE：`i_eYYYYMMDD-HHMMSS-*.nc` |
| `variables_requested` | 标准化名；空则更耗内存 |
| 坐标 | `time`（hr）、`lon`/`lat`（deg） |

| 输出 | 说明 |
| --- | --- |
| Kamodo 函数 | 标量/数组插值 |
| 不输出 | 观测 TEC、发表级 GIM、无文件气候态 |

## 6. 接到哪一步

| 场景 | 链接 |
| --- | --- |
| 无文件 NRLMSISE-00 | [msise00](./msise00.md) |
| 无文件 IRI | [iri2016](./iri2016.md) / [pyiri](./pyiri.md) / [pyglow](./pyglow.md) |
| 观测 TEC / IONEX | [pytecgg](./pytecgg.md) · [ionex-gim](./ionex-gim.md) · [ionex-rs](./ionex-rs.md) |
| 多源观测作图 | [geospacelab](./geospacelab.md) |
| 磁坐标 | [apexpy](./apexpy.md) · [aacgmv2](./aacgmv2.md) |

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 旧 `kamodo` 冲突 | 错包 | 只用 `kamodo-ccmc` |
| 2 | `file_dir` 指向单文件 | API 要目录 | 传目录 + `/` |
| 3 | `._*` 干扰 | macOS xattr | `find -name '._*' -delete` |
| 4 | OOM | 变量太多 | 缩 `variables_requested` |
| 5 | `time` 单位错 | 多为当日小时 | 先 `File_Times` |
| 6 | 当无数据 IRI | reader≠内置求解 | 下 IRI 输出或改 [iri2016](./iri2016.md) |
| 7 | 保留名注册失败 | core 保留字 | 换符号 |
| 8 | SWMF-GM 不可用 | 缺 C 扩展 | 装 gcc 或先用 SWMF_IE |
| 9 | tar 太大 | IRI/WACCMX | 先 SWMF_IE ~60M |
| 10 | `Phi_E≈1e-17` | 该点近零 | 换纬/时 |
| 11 | 坐标系错 | SM/GDZ/GSE | 看 `Model_Variables` |
| 12 | 当 GNSS TEC 产品 | 边界错 | 模式场≠观测解算 |

## 8. 选型

| 需求 | 选 |
| --- | --- |
| CCMC 模式场统一插值/飞越 | **Kamodo（本页）** |
| 无文件 msis/IRI | [msise00](./msise00.md) / [iri2016](./iri2016.md) |
| 观测 TEC/GIM | [pytecgg](./pytecgg.md) / [ionex-gim](./ionex-gim.md) |

## 9. 相关

[iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [msise00](./msise00.md) · [geospacelab](./geospacelab.md) · [ionex-gim](./ionex-gim.md) · [aacgmv2](./aacgmv2.md) · [apexpy](./apexpy.md) · [README](./README.md)
