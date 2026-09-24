# pyglow · 上层大气气候态（IRI/HWM/IGRF/MSIS）操作手册

目录：[`PROJECTS.json` → `pyglow`](../../PROJECTS.json) · 上游 <https://github.com/timduly4/pyglow> · 许可 **MIT** · 本机 tip **`1988757`**（PR #152）· **Python 3.8** + `numpy==1.20.3` + gfortran 实装；IRI-2016/2012 剖面与 IGRF/HWM 已复跑（2026-09-24 EDT）

> 岗位：在 Python 里对给定 **时间/纬经/高度** 取 **IRI 电子密度与温度**、可选 HWM 风、IGRF 磁场、MSIS 中性大气；常与 GNSS TEC / GIM 做气候态对照。冲突时：**仓内 README / `examples/` > 本文**。上游 README 自陈维护滞后，安装路径以本机实踩为准。

## 1. 用途与边界

**做：**

- `pyglow.Point(dn, lat, lon, alt)` → `run_iri()` / `run_iri(version=2012)` 得 `ne`、`Te`/`Ti`/`Tn_iri`、`ni`、`NmF2`/`hmF2`
- `run_igrf()` → `B`/`Bx`/`By`/`Bz`/`dip`；`run_hwm(version=2014|1993|…)` → `u`/`v`
- 内置 AP/Kp/F10.7 等指数（`update_indices` 可续更）；IRI 系数包随模型目录

**不做：**

- **不是** 读 IONEX GIM 产品 → [ionex-gim](./ionex-gim.md)
- **不是** 从 RINEX 校准实测 sTEC/vTEC → [pytecgg](./pytecgg.md)（作者 viventriglia）
- **不是** 球谐 GIM 求解 → [sh-gim](./sh-gim.md)（求解器未开源，仅边界）
- **不是** Galileo 广播 NeQuick-G → [nequickg](./nequickg.md)
- **不是** 官方 IRI-2016 的现代 pip 封装 → 见计划中的 [iri2016](./iri2016.md)（`space-physics/iri2016`）；**勿与用法讲解正在写的 `PyIRI` 抢篇**
- 默认绑 **IRI-2012/2016**，与官网最新 IRI-2020/2026 可能不同步

一句话：pyglow = **irimodel 社区常用的 Python 气候态包装**（Fortran 模型 + `Point` API）。

| 术语 | 含义 |
| --- | --- |
| `Point` | 单点时空；成员经 `run_*` 填充 |
| `ne` / `ni` | 电子密度、离子密度字典（`O+`/`H+`/…），单位 **cm⁻³** |
| `NmF2` / `hmF2` | F2 峰值密度 / 峰高（km） |
| `version=` | IRI `2016`（默认）或 `2012` |
| 指数 | `f107`/`f107a`/`ap`/`kp`…；可用 `user_ind` 覆盖 |

## 2. 安装（本机实踩）

系统需 **gfortran**、**rsync**（Makefile 用）、**make**。上游声明难装于 Py≥3.10；本机用 **uv** 拉 **CPython 3.8.20**。

```bash
# 依赖工具
sudo apt-get install -y gfortran make rsync   # 缺啥补啥
# Python 3.8（示例用 uv；其它方式亦可）
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.8

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/timduly4/pyglow.git
cd pyglow
uv venv -p 3.8 .venv-py38 && source .venv-py38/bin/activate
uv pip install 'numpy==1.20.3' scipy matplotlib future charset_normalizer 'pandas==1.3.5'

# 官方站点下载常挂：用仓内 static/ 离线 HTTP + get_models_offline.py
( cd static && python -m http.server 8080 ) &
# 将 src/pyglow/models/Makefile 的 download 目标改为：
#   download:
#   	python get_models_offline.py
make -C src/pyglow/models source

# 现代 gcc 下 HWM07 可能报 incompatible-pointer-types → 编译期放宽：
export CFLAGS="-Wno-error=incompatible-pointer-types -Wno-incompatible-pointer-types"
make -C src/pyglow/models all
# 若 all 中途因 HWM 失败：对各 dl_models/<name>/ 单独 make compile && rsync <name>py*so <name>py.so
# 成功时应有 iri16py.so / iri12py.so / igrf12py.so 等

python setup.py install
python -c "import pyglow; print(pyglow.__file__)"
```

### 2.1 必补：IRI-2016 的 `igrf2015*.dat`

离线 `static/00_iri.tar` **带** `igrf2015.dat` / `igrf2015s.dat`，但 `setup.py` 的 `iri16_data` 清单写成了不存在的 `igrf2020*` / `dgrf2015`，**安装后目录缺 2015 系数**。Fortran 会在 `iri_sub` **静默退出（exit 0、无 Python 异常）**。

```bash
SITE=$(python -c "import pyglow,os; print(os.path.dirname(pyglow.__file__))")
cp -v src/pyglow/models/dl_models/iri16/igrf2015.dat \
      src/pyglow/models/dl_models/iri16/igrf2015s.dat \
      "$SITE/iri16_data/"
ls "$SITE/iri16_data"/igrf2015*.dat
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pyglow'` / 无 `.so` | 未 `make` / 未 install | 按上表；确认 `find -name 'iri16py*.so'` |
| `run_iri()` 无返回、进程 exit 0 | 缺 `igrf2015*.dat` | §2.1 拷贝 |
| `Cannot open file 'ig_rz.dat'` | 在错误 cwd 调 `read_ig_rz` | 经 `Point.run_iri`（内部会 `chdir` 到 `iri16_data/`） |
| HWM07 `incompatible-pointer-types` | 新 gcc + 旧 f2py | `CFLAGS=…` 后重 `make compile` |
| `rsync: not found` | Makefile 依赖 | `apt install rsync` 或手写 `cp *py*.so namepy.so` |
| MSIS `ap` 维数 ValueError | 本机复现：`gtd7` 与 AP 向量长度不匹配 | 记为环境坑；IRI/IGRF/HWM 仍可用 |

## 3. 端到端：IRI-2016 vs 2012 剖面（本机真跑）

条件：2015-03-23 15:30 UT，**(40°N, 80°W)**，高度 100–500 km（9 点）。

```bash
cd ~/iono_ops/pyglow && source .venv-py38/bin/activate
python - <<'PY'
from datetime import datetime
import numpy as np
import pyglow

dn = datetime(2015, 3, 23, 15, 30)
lat, lon = 40.0, -80.0
alts = np.linspace(100., 500., 9)

pt = pyglow.Point(dn, lat, lon, 250.0)
pt.run_iri()  # default version=2016
print('iri2016_alt250_ne', pt.ne)
print('iri2016_Te', pt.Te, 'Ti', pt.Ti, 'Tn_iri', pt.Tn_iri)
print('iri2016_ni', dict(pt.ni))
print('iri2016_NmF2', pt.NmF2, 'hmF2', pt.hmF2)

pt.run_iri(version=2012)
print('iri2012_alt250_ne', pt.ne)

nes16, nes12 = [], []
for alt in alts:
    p = pyglow.Point(dn, lat, lon, float(alt))
    p.run_iri(); nes16.append(float(p.ne))
    p.run_iri(version=2012); nes12.append(float(p.ne))
print('alts_km', [round(float(a),1) for a in alts])
print('ne_iri2016', [round(x,3) for x in nes16])
print('ne_iri2012', [round(x,3) for x in nes12])
print('ne_max_2016', max(nes16), 'at_km', float(alts[int(np.argmax(nes16))]))

p2 = pyglow.Point(dn, lat, lon, 250.0)
p2.run_igrf()
print('igrf_B', p2.B, 'dip', p2.dip)
p2.run_hwm(version=2014)
print('hwm14_u', p2.u, 'v', p2.v)
print('f107', p2.f107, 'ap', p2.ap, 'kp', p2.kp)
PY
```

**本机 stdout（2026-09-24 EDT，补齐 `igrf2015*.dat` 后）：**

```text
iri2016_alt250_ne 854889.005056
iri2016_Te 1745.7712 Ti 1017.06 Tn_iri 1017.06
iri2016_ni {'O+': 821082.5216, 'H+': 0.0, 'HE+': 0.0, 'O2+': 8090.49856, 'NO+': 14461.804544}
iri2016_NmF2 893029.90848 hmF2 271.4751
iri2012_alt250_ne 1233322.115072
alts_km [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0]
ne_iri2016 [113656.652, 221394.092, 513472.496, 854889.005, 849509.482, 660797.719, 469427.421, 328157.79, 232918.761]
ne_iri2012 [110475.043, 239707.914, 653078.626, 1233322.115, 1352371.536, 1080474.73, 763789.705, 526013.956, 367389.999]
ne_max_2016 854889.005056 at_km 250.0
igrf_B 4.631570244603175e-05 dip 67.12284207430118
hwm14_u -88.41388 v 6.846781
f107 127.2 ap 15.0 kp 3.0
```

| 字段 | 含义 |
| --- | --- |
| `ne` | 电子密度 **cm⁻³**（内部从 m⁻³ `/100³`） |
| `Te`/`Ti`/`Tn_iri` | 电子/离子/中性温度 **K** |
| `ni['O+']`… | 离子密度 cm⁻³（`JF(22)=0` 路径） |
| `NmF2`/`hmF2` | 峰值密度与峰高；本机 hmF2≈**271.5 km** |
| `igrf_B` | 总场 **T**；`dip` 磁倾角 **°** |
| `hwm14_u`/`v` | 纬向/经向风 **m/s**（HWM14） |

### 3.1 关键 API

| 符号 | 作用 |
| --- | --- |
| `Point(dn, lat, lon, alt)` | `dn` 为 `datetime`（按 UT 理解） |
| `run_iri(version=2016, NmF2=…, hmF2=…, compute_Ne/Te_Ti/Ni=…)` | 跑 IRI；可灌峰值约束 |
| `run_igrf()` / `run_hwm(version=…)` / `run_msis()` | 磁场 / 风 / 中性（MSIS 本机 AP 维数失败） |
| `pyglow.update_indices(y0, y1)` | 续下载指数（需网） |
| `pyglow.check_stored_indices(d0, d1)` | 检查本地指数覆盖 |

## 4. 接到哪步

- 气候态 Ne/TEC 背景 ↔ 单站校准 TEC：[pytecgg](./pytecgg.md)；粗相对 TEC：[gnss-tec](./gnss-tec.md)
- 与分析中心 GIM 图对照：[ionex-gim](./ionex-gim.md)；球谐自建边界：[sh-gim](./sh-gim.md)
- 只要官方 IRI-2016 Fortran 的现代封装 → [iri2016](./iri2016.md)（撰写中）；纯 Python IRI → 用法讲解的 `PyIRI`（**勿抢写**）
- Galileo 单频模型对照 → [nequickg](./nequickg.md)
- 教程 [04 IRI/NeQuick](../tutorials/04-iri-nequick.md) · [01 基础](../tutorials/01-ionosphere-tec-basics.md) · [03 GIM](../tutorials/03-gim-ionex.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | Py3.10+ 装不上 / f2py 怪错 | 上游停更 | 用 **3.8** + `numpy==1.20.3` |
| 2 | `run_iri` 静默 exit 0 | 缺 `igrf2015*.dat` | §2.1 |
| 3 | 官方 URL 下模型失败 | 远端不稳 | `static/` + `get_models_offline.py` |
| 4 | `make all` 死在 `rsync` | 未装 rsync | `apt install rsync` |
| 5 | HWM07 编译 pointer 错误 | 新 gcc | `CFLAGS=-Wno-error=incompatible-pointer-types` |
| 6 | MSIS `ap` ValueError | f2py/AP 长度 | 本机未通；先只用 IRI/IGRF/HWM |
| 7 | 当实测 TEC 产品 | 气候态模型 | 实测链走 [pytecgg](./pytecgg.md) |
| 8 | 当 GIM 读取器 | 不读 IONEX | [ionex-gim](./ionex-gim.md) |
| 9 | 与 IRI-2020 论文对不上 | 绑的是 2012/2016 | 换官方新版或其它封装并核对版本 |
| 10 | `src` 出现在安装路径触发测试路径改写 | `iri.py` 对含 `src` 的路径特殊处理 | 正常 site-packages 路径无 `src` 子串即可；勿把包装进路径名含 `src` 的前缀 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| Python 里快速 IRI-2012/2016 + 风/磁 | **本文 pyglow** |
| 官方 IRI-2016 的 pip/Fortran 接口 | [iri2016](./iri2016.md) |
| 读 IONEX VTEC 图 | [ionex-gim](./ionex-gim.md) |
| 校准 GNSS TEC | [pytecgg](./pytecgg.md) |
| Galileo NeQuick-G | [nequickg](./nequickg.md) |

- 上游：<https://github.com/timduly4/pyglow>
- irimodel：<https://irimodel.org/>
- 兄弟：[ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [sh-gim](./sh-gim.md) · [nequickg](./nequickg.md) · [iri2016](./iri2016.md) · [data-access](../data-access.md)
