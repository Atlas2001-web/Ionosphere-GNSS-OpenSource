# apexpy · Apex / 准偶极磁坐标操作手册

目录：[`PROJECTS.json` → `apexpy`](../../PROJECTS.json) · 上游 <https://github.com/aburrell/apexpy> · 许可 **MIT** · PyPI **`apexpy` 2.1.1** · 本机 tip **`eed96cf`** · Python **3.11** 轮子；`(40°N,80°W)` 2015-03-23 15:30 UT / 250 km 实跑（2026-09-24 EDT）

> 岗位：地理坐标 ↔ **Modified Apex / Quasi-Dipole (QD)**，算 **MLT**、沿磁力线映射、\|B\|。冲突时：**上游 README / `apexpy -h` > 本文**。常与 IRI 气候态、GIM/TEC 按磁纬分箱联用。

## 1. 用途与边界

**做：**

- `Apex(date, refh).geo2apex / apex2geo / geo2qd / qd2geo`
- `mlon2mlt` / `mlt2mlon`；`map_to_height` 沿场线映射；`get_babs` → \|B\|（**特斯拉**）
- CLI：`apexpy geo apex|qd|mlt YYYYMMDDHHMMSS`（stdin：`lat lon`）

**不做：**

- **不是** 电子密度 / TEC 模型 → [iri2016](./iri2016.md) · [pyglow](./pyglow.md) · [pyiri](./pyiri.md) · [pyirtam](./pyirtam.md)
- **不是** 读 IONEX GIM → [ionex-gim](./ionex-gim.md)
- **不是** RINEX→TEC → [pytecgg](./pytecgg.md)
- 时间外推依赖内置 IGRF 系数年代；远未来/远过去需自查系数

一句话：apexpy = **电离层磁坐标（Apex/QD/MLT）的 Python 标准轮子**。

| 术语 | 含义 |
| --- | --- |
| `refh` | Modified Apex 参考高度（km） |
| Apex lat/lon | `geo2apex(glat,glon,height)` |
| QD | Quasi-Dipole；与 Apex 共用磁经度、纬不同 |
| MLT | 磁地方时（小时）；需完整 `YYYYMMDDHHMMSS` |
| `get_babs` | \|B\|，单位 **T**（×1e9 → nT） |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv apexpy-demo/.venv
source apexpy-demo/.venv/bin/activate
pip install -U pip
pip install 'apexpy==2.1.1' numpy
python -c "import apexpy; print(apexpy.__version__)"
# 期望：2.1.1
apexpy -h | head
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `pip` 源码编译失败 | 无 gfortran / 缺 wheel | `apt install gfortran`；或换有 wheel 的平台 |
| CLI `full date/time … YYYYMMDDHHMMSS required for MLT` | 日期串不够 14 位 | 用 `20150323153000` |
| `ValueError: lat must be in [-90, 90]` | 纬经颠倒或越界 | stdin/`convert` 均为 **lat lon（度）** |

## 3. 端到端：地理 → Apex/QD/MLT（本机真跑）

与 [pyglow](./pyglow.md) / [iri2016](./iri2016.md) 同点：2015-03-23 15:30 UT，**(40°N, 80°W)**，250 km，`refh=0`。

```bash
cd ~/iono_ops/apexpy-demo && source .venv/bin/activate
python - <<'PY'
from datetime import datetime
import apexpy

dn = datetime(2015, 3, 23, 15, 30, 0)
A = apexpy.Apex(date=dn, refh=0)
print("apexpy", apexpy.__version__)
print("year", float(A.year), "refh", A.refh)

glat, glon, h = 40.0, -80.0, 250.0
alat, alon = A.geo2apex(glat, glon, h)
print("geo2apex", float(alat), float(alon))
qlat, qlon = A.geo2qd(glat, glon, h)
print("geo2qd", float(qlat), float(qlon))
g2, o2, err = A.apex2geo(float(alat), float(alon), h)
print("apex2geo", float(g2), float(o2), float(err))
print("mlon2mlt", float(A.mlon2mlt(float(alon), dn)))
b = float(A.get_babs(glat, glon, h))
print("babs_T", b, "babs_nT", b * 1e9)

mla, mlo, merr = A.map_to_height(glat, glon, 250.0, 110.0)
print("map_250_to_110", float(mla), float(mlo), float(merr))

a, o = A.geo2apex(0.0, 0.0, 300.0)
q, qo = A.geo2qd(0.0, 0.0, 300.0)
print("eq_apex", float(a), float(o), "qd", float(q), float(qo))
a, o = A.geo2apex(70.0, 0.0, 110.0)
q, qo = A.geo2qd(70.0, 0.0, 110.0)
print("pole_apex", float(a), float(o), "qd", float(q), float(qo))
PY
```

**本机 stdout（2026-09-24 EDT，`apexpy` 2.1.1）：**

```text
apexpy 2.1.1
year 2015.2236872146118 refh 0
geo2apex 50.69572448730469 -4.0730390548706055
geo2qd 49.77827835083008 -4.0730390548706055
apex2geo 40.0 -80.0 0.0
mlon2mlt 10.252084795633952
babs_T 4.6287867666761836e-05 babs_nT 46287.867666761835
map_250_to_110 40.486270904541016 -80.10050201416016 5.122642050991999e-06
eq_apex -17.326662063598633 73.6803970336914 qd -12.355287551879883 73.6803970336914
pole_apex 68.44007110595703 87.1010513305664 qd 68.2453384399414 87.1010513305664
```

### 3.1 CLI（同点）

日期必须 **14 位** `YYYYMMDDHHMMSS`（MLT 强制）。

```bash
printf '40.0 -80.0\n' | apexpy geo apex 20150323153000 --height 250 --refh 0
printf '40.0 -80.0\n' | apexpy geo qd   20150323153000 --height 250
printf '40.0 -80.0\n' | apexpy geo mlt  20150323153000 --height 250
```

**本机 stdout：**

```text
50.69572449 -4.07303905
49.77827835 -4.07303905
50.69572449 10.25208480
```

（`geo mlt` 第二列是 **MLT**，不是磁经。）

### 3.2 `refh` 与高度

```bash
python - <<'PY'
from datetime import datetime
import apexpy
A = apexpy.Apex(date=datetime(2015,3,23), refh=300)
print("h250_refh300", [float(x) for x in A.geo2apex(40, -80, 250)])
print("h400_refh300", [float(x) for x in A.geo2apex(40, -80, 400)])
PY
```

**本机：**

```text
h250_refh300 [49.59557342529297, -4.073162078857422]
h400_refh300 [50.100948333740234, -4.188036918640137]
```

## 4. 接到哪步

- IRI/气候态按**磁纬**分箱 → 本文 + [pyglow](./pyglow.md) / [iri2016](./iri2016.md) / [pyiri](./pyiri.md) / [pyirtam](./pyirtam.md)
- GIM/TEC 按 QD 纬统计 → [ionex-gim](./ionex-gim.md) + 本文
- 教程 → [04](../tutorials/04-iri-nequick.md) / [03](../tutorials/03-gim-ionex.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | CLI `YYYYMMDDHHMMSS required for MLT` | 日期只有 8/12 位 | 写满 14 位 |
| 2 | `lat must be in [-90, 90]` | 纬经顺序反了 | **lat lon（度）** |
| 3 | `get_babs`≈4.6e-5 当 nT 用 | 返回值是 **T** | ×1e9 → nT |
| 4 | `geo mlt` 第二列当磁经 | CLI 第二列是 **MLT** | 要磁经用 `geo apex`/`qd` |
| 5 | 换 `refh` 后 Apex 纬跳变 | 定义面高度变了 | 全文固定同一 `refh` |
| 6 | 与旧论文差 1°+ | IGRF 年代 / `date` 不同 | 锁同一 `datetime` |
| 7 | 源码安装失败 | 无 Fortran 编译器 | 优先 PyPI wheel |
| 8 | 当电子密度模型 | 只做坐标 | 接 [iri2016](./iri2016.md) / [pyiri](./pyiri.md) |
| 9 | `map_to_height` 残差大 | 近磁赤道/共轭分支 | 查 `conjugate`；换足迹高度 |
| 10 | 数组与标量 shape 炸 | 未广播 | 纬经高同标量或同长数组 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| Apex / QD / MLT 坐标 | **本文 apexpy** |
| IRI 气候态（Fortran 包装） | [iri2016](./iri2016.md) · [pyglow](./pyglow.md) |
| 纯 Python IRI / IRTAM | [pyiri](./pyiri.md) · [pyirtam](./pyirtam.md) |
| 读 GIM | [ionex-gim](./ionex-gim.md) |

- 文档：<https://apexpy.readthedocs.io/>
- 兄弟：[pyglow](./pyglow.md) · [iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [pyirtam](./pyirtam.md) · [ionex-gim](./ionex-gim.md) · [nequickg](./nequickg.md)
