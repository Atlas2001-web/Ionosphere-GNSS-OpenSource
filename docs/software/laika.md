# laika · comma.ai Python GNSS 操作手册

目录：[`PROJECTS.json` → `laika`](../../PROJECTS.json) · 上游 <https://github.com/commaai/laika> · 许可 **MIT** · 包版本 **0.0.1**（仓内 `pyproject.toml`）· 本机验证：读 `examples/slac1700.18o` → 2880 历元 + DOP 烟测；`pytest` time/dop/prns **17 passed**；质检复跑 stdout 一致（2026-09-24 EDT，R11）。**完整星历/改正下载需 Earthdata `.netrc`**（本机未配账号，未跑 CORS 定位）

> 岗位：把原始 GNSS 观测整理成「伪距 + 卫星位置」供自写 WLS/卡尔曼；`AstroDog` 负责拉 CDDIS 等产品并缓存。冲突时：**仓内 README / `examples/Walkthrough.ipynb` > 本文**。

## 1. 用途与边界

**做：**

- `RINEXFile` + `raw.read_rinex_obs`：RINEX OBS → `GNSSMeasurement` 列表
- `AstroDog`：`get_sat_info` / `get_delay`（对流层+电离层+DCB；美东可用 DGPS）
- `raw.process_measurements` / `correct_measurements` + `opt.calc_pos_fix`：改正伪距与简易 WLS
- DOP 工具：`get_DOP` / `PDOP` / `HDOP` / `VDOP` / `TDOP`
- 示例笔记本：Walkthrough / CORS 站坐标 / Kalman

**不做：**

- **不是** 发表级 PPP-AR → [pride-pppar](./pride-pppar.md)
- **不是** 开放 SSR/HAS PPP 试验箱 → [cssrlib](./cssrlib.md)；HAS 解码 → [haslib](./haslib.md)
- **不是** 工业 CLI 事后定位主力 → [rtklib](./rtklib.md)
- **不是** 校准 TEC 产品 → [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md)
- 默认解算是教学级 WLS；量产融合定位需自接滤波器（见 `examples/Kalman.ipynb`）

一句话：laika = **可读的轻量 Python GNSS 观测处理库**（comma.ai）；下载链依赖 NASA Earthdata。

| 术语 | 含义 |
| --- | --- |
| `AstroDog` | 下载/缓存星历、IONEX、DCB 等并回答 `get_sat_info`/`get_delay` |
| `GNSSMeasurement` | 单星单历元；`observables`（C1C/L1C…）、`sat_pos`、`processed` |
| `GPSTime(week, tow)` | GPS 周 + 周内秒 |
| `pull_orbit` | 是否允许从网上下星历（默认 True；无账号会失败） |
| Earthdata `.netrc` | CDDIS 鉴权；无则只能做本地解析/DOP 等离线部分 |

## 2. 安装

上游写明偏 Ubuntu + Python 3.11；本机 **3.13** 可 import。`sympy` 被 `opt`/`dgps` 间接需要但未写入 `pyproject` 依赖表。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/commaai/laika.git
cd laika
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install numpy scipy certifi requests pycurl tqdm hatanaka pycapnp atomicwrites sympy
python -m pip install -e .
python -c "from laika import AstroDog; print('ok', AstroDog)"
# 可选：离线单测
python -m pip install pytest parameterized
python -m pytest tests/test_time.py tests/test_dop.py tests/test_prns.py -q
# 期望：17 passed
```

Earthdata（拉星历/CORS 必需）：

```bash
# https://urs.earthdata.nasa.gov/ 注册后，在仓根写 .netrc（勿提交 git）：
# machine urs.earthdata.nasa.gov login YOUR_USER password YOUR_PASS
chmod 600 .netrc
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'sympy'` | 未列入官方 deps | `pip install sympy` |
| `pycapnp` / `pycurl` 编译失败 | 缺系统头 | `sudo apt install libcurl4-openssl-dev` 后重装；或换 Py3.11 |
| 下载 401/空文件 | 无 Earthdata | 配 `.netrc`；勿把口令写入仓库 |

## 3. 端到端：本地 RINEX 解析 + DOP（本机真跑）

不依赖 Earthdata。样本：`examples/slac1700.18o`（RINEX 2 观测，仓内自带）。

### 3.1 读 OBS

```bash
cd ~/iono_ops/laika && source .venv/bin/activate
python - <<'PY'
from laika.rinex_file import RINEXFile
import laika.raw_gnss as raw
from laika.lib.coordinates import geodetic2ecef, ecef2geodetic
from laika.raw_gnss import get_PDOP
import numpy as np

rf = RINEXFile('examples/slac1700.18o')
print('version', rf.version, 'marker', rf.marker_name)
print('obs_types', rf.obs_types)
mg = raw.read_rinex_obs(rf)
print('epochs', len(mg), 'nsats_e0', len(mg[0]))
m = mg[0][0]
print('prn', m.prn, 'recv_time', m.recv_time)
print('obs_keys', sorted(m.observables.keys()))
print('C1C', float(m.observables['C1C']), 'sat_pos', m.sat_pos)

# DOP 烟测（与 tests/test_dop 同构几何）
recv = geodetic2ecef((37.4, -122.15, 60.0))
sats = np.array([
    [18935913, -3082759, -18366964],
    [7469795, 22355916, -12240619],
    [11083784, -18179141, 15877221],
    [22862911, 13420911, 1607501],
])
print('PDOP', get_PDOP(recv, sats))
print('recv_llh', ecef2geodetic(recv))
PY
```

**本机 stdout（2026-09-24 EDT）：**

```text
version 2.11 marker SLAC
obs_types ['L1', 'L2', 'C1', 'P2', 'P1', 'S1', 'S2']
epochs 2880 nsats_e0 15
prn G02 recv_time GPSTime(week=2006, tow=172800.0)
obs_keys ['C1C', 'C2P', 'L1C', 'L2C', 'P1C', 'S1C', 'S2C']
C1C 23545113.203 sat_pos [nan nan nan]
PDOP 3.2983697583505136
recv_llh [  37.4        -122.15         60.00009007]
```

| 字段 | 含义 |
| --- | --- |
| `epochs` / `nsats_e0` | 历元数；首历元可见星数 |
| `prn` / `recv_time` | 卫星 PRN；接收时刻 `GPSTime` |
| `observables['C1C']` | 伪距 (m)；RINEX2 `C1` 被映射为 `C1C` 等 |
| `sat_pos == nan` | **尚未** `process_measurements`；无星历前正常 |
| `PDOP` | 位置精度因子（几何；与定位解无关）。**同组卫星**在 `tests/test_dop` 用接收机 `(0,0,0)` → PDOP≈**2.196**；本文用 SLAC 近似坐标 → **3.298…**（勿混） |

### 3.2 AstroDog 冒烟 + 定位链（需账号）

```bash
python - <<'PY'
from laika import AstroDog
from laika.helpers import ConstellationId
dog = AstroDog(valid_const=[ConstellationId.GPS, ConstellationId.GLONASS])
print('cache_dir', dog.cache_dir)   # 默认 /tmp/gnss/
print('pull_orbit', dog.pull_orbit)
PY
# 有 .netrc 后（摘自 tests/test_positioning.py 思路）：
#   dog = AstroDog()
#   meas = raw.read_rinex_obs(RINEXFile(path))
#   proc = raw.process_measurements(meas[i], dog=dog)
#   corr = raw.correct_measurements(proc, approx_ecef, dog=dog)
#   fix, _, _ = opt.calc_pos_fix(corr)[0]
```

本机**未**配置 Earthdata：未跑 `get_sat_info` / CORS 下载；`dog=None` 调 `process_measurements` 会 `AttributeError`（见坑表）。

### 3.3 关键 API

| 符号 | 作用 |
| --- | --- |
| `RINEXFile(path)` | 解析 OBS 头与数据块 |
| `raw.read_rinex_obs(rf)` | → `List[List[GNSSMeasurement]]`（历元→星） |
| `AstroDog(pull_orbit=True, valid_const=…)` | 产品狗；`cache_dir` 默认 `/tmp/gnss/` |
| `raw.process_measurements(meas, dog=)` | 填 `sat_pos` / 钟差；**必须**有效 `dog` |
| `raw.correct_measurements(proc, pos, dog=)` | 对流层/电离层/DCB 改正伪距 |
| `opt.calc_pos_fix(corr)` | WLS；返回 `(fix, residual, …)` 列表 |
| `GPSTime.from_datetime` / `.as_datetime()` | 时间互转 |
| `helpers.get_constellation(prn)` | `G/R/E/C/J…` → `ConstellationId` |

## 4. 接到哪步

- 快速脚本定位 / 融合原型 → 本文；要 RTK/PPP 产品链 → [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md) / [pride-pppar](./pride-pppar.md)
- HAS/SSR 改正入口 → [haslib](./haslib.md) + [cssrlib](./cssrlib.md)（laika 不吃 HAS 页）
- RINEX 进 xarray / 科学分析 → [georinex](./georinex.md)；Hatanaka → [rnxcmp](./rnxcmp.md) / [hatanaka](./hatanaka.md)（laika 依赖里已列 `hatanaka`）
- 教程 [06](../tutorials/06-iono-positioning.md)；数据 [data-access](../data-access.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `No module named 'sympy'` | 间接依赖未声明 | `pip install sympy` |
| 2 | `sat_pos` 全 `nan` | 只读了 OBS，未 process | 配 Earthdata 后 `process_measurements(..., dog=dog)` |
| 3 | `AttributeError: 'NoneType' … get_sat_info` | `dog=None` | 传入 `AstroDog()`；无网则勿调 process |
| 4 | CDDIS/CORS 401 或空文件 | 无 `.netrc` | 按 §2 写 `urs.earthdata.nasa.gov` 凭证 |
| 5 | `pip install .` 后仍 `import laika` 失败 | 不在 venv / editable 未装 | `source .venv && pip install -e .` |
| 6 | 定位偏差大 / 仅 WLS | 未用动态滤波器 | 跟 `examples/Kalman.ipynb`；或换 [rtklib](./rtklib.md) |
| 7 | `hatanaka` 解压失败 | 旧 CRX / 缺二进制 | 官方工具见 [rnxcmp](./rnxcmp.md) |
| 8 | 当 HAS/SSR 解码器 | 能力不在此 | [haslib](./haslib.md) + [cssrlib](./cssrlib.md) |
| 9 | PDOP 与 `tests/test_dop` 对不上 | 接收机坐标不同（测试用 `(0,0,0)`） | 对照时同步 `geodetic2ecef` 参数；本文 SLAC 近似得 3.298… |
| 10 | `pyproject` 写 `target-version=py311`，本机 3.13 可 import | 上游声明偏 3.11 | 冒烟可用 3.13；遇编译型依赖失败再换 3.11 |

## 6. 选型与链接

| 你要… | 用 |
| --- | --- |
| 可读 Python 观测处理 / 自写估计器 | **本文 laika** |
| CLI RTK/PPP | [rtklib](./rtklib.md) |
| 开放 SSR/HAS PPP | [cssrlib](./cssrlib.md)（解码 [haslib](./haslib.md)） |
| 发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| RINEX→xarray | [georinex](./georinex.md) |

- Earthdata：<https://urs.earthdata.nasa.gov/>
- 笔记本：<https://github.com/commaai/laika/tree/master/examples>
- 兄弟：[rtklib](./rtklib.md) · [cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [georinex](./georinex.md) · [pygnssutils](./pygnssutils.md) · [pride-pppar](./pride-pppar.md) · [data-access](../data-access.md)
