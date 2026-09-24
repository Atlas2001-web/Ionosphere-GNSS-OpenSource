# OASIS（pyOASIS）· ROTI / ΔTEC / SIDX 操作手册

目录：[`PROJECTS.json` → `OASIS`](../../PROJECTS.json) · 上游 <https://github.com/giorgiopicanco/OASIS> · PyPI **`pyOASIS`** · **CC BY-NC 4.0**（商业先读 LICENSE）· 本机验证 **pyOASIS 1.0.3** + 仓内样例 `BOAV` DOY 049/2023（SP3→RNX3→ROTI/ΔTEC 真跑）

> 岗位：RINEX OBS + **同日** MGEX SP3 → 电离层扰动指数。主产物 **ROTI、ΔTEC、SIDX**。不是硬件 S4/σφ，不是校准绝对 TEC，不是 GIM。入口以仓库 `main.py` 与包 API `pyOASIS.SP3intp` / `RNXclean` / `RNXlevelling` / `ROTIcalc` / `DTECcalc` / `SIDXcalc` 为准。

## 1. 用途与边界

**做：** 周跳/粗差 → 弧段 GF leveling → ROTI、ΔTEC、SIDX。RINEX 2/3；文档友好采样 **15/30 s**；GPS + GLONASS（Galileo/BeiDou 以上游为准）。**不依赖 DCB / GIM 产品。**

**不做：** 硬件闪烁 → ISMR；可控仿真 → [iono-scintillation](./iono-scintillation.md)；校准绝对 TEC → [pytecgg](./pytecgg.md)（作者 **viventriglia**）；全球球谐 GIM → 开源 GIM / [sh-gim](./sh-gim.md) 边界；C++ 批监测 → [ionomoni](./ionomoni.md)。

一句话：读盘后的 **Python 扰动指数链**；与 IonoMoni **只比趋势，不硬比绝对值**。

| 术语 | 含义 |
| --- | --- |
| ROTI | Rate of TEC Index（短窗 ROT 标准差） |
| ΔTEC | 长短窗 leveled GF 之差（**非**绝对 TEC） |
| SIDX | Sudden Ionospheric Disturbance Index |
| GF leveling | 相位几何无关组合按弧段对齐到码 |
| IPP | 穿刺点（需 SP3） |

## 2. 安装

```bash
cd ~/work
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install pyOASIS
python -c "import pyOASIS, importlib.metadata as m; print('pyOASIS', m.version('pyOASIS'))"

# 完整流水线（含 INPUT 样例）——推荐
git clone https://github.com/giorgiopicanco/OASIS.git
cd OASIS
python -m pip install -r requirements.txt
ls INPUT/
```

依赖要点（以 `requirements.txt` 为准）：numpy、pandas、matplotlib、scipy、astropy、**georinex**、pyproj。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python 过旧 | 用 3.8+ |
| `ModuleNotFoundError: georinex` | 依赖未装全 | `pip install -r requirements.txt` |
| 可 import、`main.py` 秒退 | 不在仓库根 / 无 INPUT | `cd OASIS`；`ls INPUT/` |
| 许可疑虑 | CC BY-NC | 商业先读 LICENSE |
| `pd.to_numeric(..., errors='ignore')` 炸 | **pandas 3** 已删 `errors='ignore'` | 临时改 `errors='coerce'`，或钉 `pandas<3` |
| leveling 在插值步无声退出 | 旧代码 `index.values.astype("datetime64[s]").astype("int64")` 与新 numpy/pandas 不兼容 | 升级上游；或插值改 `Series.interpolate(method="time")` |

## 3. 端到端：样例站日 → 指数文件

上游示例：`INPUT/boav0491.23o` + 同日 GFZ MGEX SP3（DOY 049 / 2023）。**当前 `main.py` 期望子目录：**

```text
INPUT/RINEX/*.yyo|*.rnx
INPUT/ORBITS/*SP3
OUTPUT/ORBITS/<YYYY>/<DOY>/
OUTPUT/RINEX/<YYYY>/<DOY>/<STA>/
```

### 3.1 摆放输入

```bash
cd ~/work/OASIS
mkdir -p INPUT/RINEX INPUT/ORBITS OUTPUT logs
# 若样例仍在 INPUT/ 根下：
test -f INPUT/boav0491.23o && cp -n INPUT/boav0491.23o INPUT/RINEX/
test -f INPUT/GFZ0MGXRAP_20230490000_01D_05M_ORB.SP3 \
  && cp -n INPUT/GFZ0MGXRAP_20230490000_01D_05M_ORB.SP3 INPUT/ORBITS/
head -n 3 INPUT/RINEX/boav0491.23o
# 期望：RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
ls -la INPUT/ORBITS/*SP3
```

缺 SP3：按 [data-access](../data-access.md) 取同日 MGEX（需 Earthdata）。**2018 前**常见 `JAX0MGXFIN_`；**2018 后**常见 `GFZ0MGXRAP_`（以上游 README 为准）。

### 3.2 配置 `main.py`

```bash
grep -nE 'sta |doy |year |INPUT|OUTPUT|SP3intp|RNXclean|ROTIcalc' main.py | head -n 40
# 确认：
#   sta="BOAV"; doy="049"; year="2023"
#   rinex_dir = .../INPUT/RINEX
#   orbit_input_dir = .../INPUT/ORBITS
```

无头机器：`export MPLBACKEND=Agg`，并把各 `show_plot=True` 改 `False`（或改调用参数）。

### 3.3 跑流水线（API ≡ `main.py` 步骤）

```bash
export MPLBACKEND=Agg
python3 main.py 2>&1 | tee logs/oasis_run.log
# 或逐步：
python3 - <<'PY'
import os; os.environ["MPLBACKEND"]="Agg"
import matplotlib; matplotlib.use("Agg")
from pathlib import Path
import pyOASIS
base = Path(".").resolve()
year, doy, sta = "2023", "049", "BOAV"
rinex_dir = base / "INPUT" / "RINEX"
orbit_in  = base / "INPUT" / "ORBITS"
orbit_out = base / "OUTPUT" / "ORBITS" / year / doy
sta_out   = base / "OUTPUT" / "RINEX" / year / doy / sta
orbit_out.mkdir(parents=True, exist_ok=True)
sta_out.mkdir(parents=True, exist_ok=True)
pyOASIS.SP3intp(year, doy, orbit_in, orbit_out)
pyOASIS.RNXclean(sta, doy, year, rinex_dir, orbit_out, sta_out)
pyOASIS.RNXlevelling(sta, sta_out, show_plot=False)
pyOASIS.ROTIcalc(sta, doy, year, sta_out, sta_out, show_plot=False)
pyOASIS.DTECcalc(sta, doy, year, sta_out, sta_out, show_plot=False)
# SIDX：部分环境 RNX3 的 mini_flag='N' 会导致 astype(float) 失败——见坑表
pyOASIS.SIDXcalc(sta, doy, year, sta_out, sta_out, show_plot=False)
PY
find OUTPUT -type f | head -n 40
```

| 步骤 | API | 作用 / 典型产出 |
| --- | --- | --- |
| 轨道 | `SP3intp` | SP3 → 观测历元表；`OUTPUT/ORBITS/.../ORBITS_YYYY_DOY.SP3` |
| 清洗 | `RNXclean`（内含 screening） | → `.RNX1` / `.RNX2` |
| 对齐 | `RNXlevelling` | 弧段 GF leveling → `.RNX3` |
| 指数 | `ROTIcalc` / `DTECcalc` / `SIDXcalc` | `*_G_ROTI.txt` / `*_DTEC.txt` / SIDX |

**本机真实产物摘要（pyOASIS 1.0.3，BOAV 2023/049，2026-09-24）：**

```text
# SP3 插值后
OUTPUT/ORBITS/2023/049/ORBITS_2023_049.SP3   # ~2.3 MB
Date	Time	Satellite	X	Y	Z
18-02-2023	00:00:00	PC01	-34367.691383	24409.268792	-558.824928

# 计数
53× .RNX1   53× .RNX2   53× .RNX3   + ROTI/DTEC .txt/.png

# ROTI 头 + 首行
MJD	Longitude	Latitude	Height	Elevation	ROTI	STA	SAT
59993.72300	  298.41695	   -3.05986	  450.00000	   30.22005	    0.08905	BOAV	G01

# ΔTEC 头 + 首行
date	time	MJD	Longitude	Latitude	Height	Elevation	DTEC	STA	SAT
2023-02-18	17:22:37	59993.72405	  298.46125	   -2.94429	  450.00000	   30.82391	   -5.08360	BOAV	G01
```

**期望：** 日志走完 leveling；`OUTPUT/RINEX/<Y>/<DOY>/<STA>/` 下有 `.RNX3` 与 `*_ROTI.txt`。缺 SP3 → 死在轨道步。SIDX 本机未稳定出文件（见坑 17）。

### 3.4 输出字段

| 产物 | 含义 | 误用 |
| --- | --- | --- |
| leveled GF / `.RNX3` | 弧段对齐后的几何无关组合 | 未 leveling 就算 ROTI → 假峰 |
| ROTI | 短窗 ROT 标准差 | 改窗后与文献硬比数值 |
| ΔTEC | 长短窗平滑差 | 当成绝对 TEC 发表 |
| SIDX | 短时 \|ROT\| 类指数 | 与硬件 S4 混称 |
| IPP Lon/Lat/Height | 穿刺点 | SP3 日错 → 几何全错 |

### 3.5 接到下游

高 ROTI 时段 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) 固定率；绝对 TEC → [pytecgg](./pytecgg.md)；同站日可再跑 [ionomoni](./ionomoni.md) **只比高值时段是否同向**。

教程：[05](../tutorials/05-scintillation-roti.md) · [20](../tutorials/20-storm-tec-analysis.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md)。

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| RINEX OBS 2/3 | 双频；15/30 s；放 `INPUT/RINEX/` |
| MGEX SP3 | **同日**；放 `INPUT/ORBITS/` |
| `main.py` 元数据 | 站码/年/DOY 与文件一致 |

| 输出 | 下游 |
| --- | --- |
| ROTI / ΔTEC / SIDX | 路径 B 分析 |
| leveled GF / 图 | 自检弧段 |

**明确不输出：** DCB 产品、IONEX、硬件 S4、校准 `veq`。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 B 不规则体 | §3 | [05](../tutorials/05-scintillation-roti.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 磁暴扰动 | §3 | [20](../tutorials/20-storm-tec-analysis.md) · [ionomoni](./ionomoni.md) |
| QC 前门禁 | — | [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md) |
| 绝对 TEC | — | [pytecgg](./pytecgg.md) |
| 高 ROTI→定位 | §3.5 | [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 轨道步失败 | 缺 SP3 / 日错 | 下同日 MGEX；核对 DOY |
| 2 | 无 `.RNX3` | 单频或弧段被杀光 / leveling 崩 | 换双频站日；先 Anubis；见坑 16 |
| 3 | ROTI 全空/NaN | 未 leveling 或采样不符 | 确认有 `.RNX3`；用 15/30 s |
| 4 | 1 Hz OOM / 窗义乱 | 非推荐采样 | `gfzrnx -smp 30` 后再跑 |
| 5 | 与 IonoMoni 差一个量级 | 窗口/周跳策略不同 | **比趋势**；笔记写定义 |
| 6 | 把 ROTI 写成 S4 | 物理量不同 | 改称 ROTI；S4 用 ISMR |
| 7 | 把 ΔTEC 当绝对 TEC | 误解产物 | → [pytecgg](./pytecgg.md) |
| 8 | SP3 用错天 | IPP 全错 | GPS week/DOY 日历核对 |
| 9 | cron 相对路径失效 | cwd 不同 | INPUT/OUTPUT 改绝对路径 |
| 10 | 夜峰全算赤道泡 | 多路径站 | 先 Anubis MP |
| 11 | 商业部署踩许可 | CC BY-NC | 读 LICENSE 或换工具 |
| 12 | 只跑到 RNX2 | 未跑 `*_calc` / leveling 失败 | `find OUTPUT -name '*.RNX3'` |
| 13 | GLONASS 怪值 | 频分通道 | 读上游 README / 通道表 |
| 14 | 与 GIM 像素比 ROTI | 对象不同 | GIM→[ionex-gim](./ionex-gim.md) |
| 15 | `head` 见 HTML | 下载成登录页 | 重走 Earthdata |
| 16 | RNXclean / leveling 无声失败 | pandas3 `errors='ignore'`；datetime64 强转 | `errors='coerce'`；time 插值；或钉旧 pandas |
| 17 | SIDX `astype(float)` 遇 `'N'` | RNX3 `mini_flag` 等列为字串 | 升上游或筛列/`to_numeric`；先交付 ROTI/ΔTEC |
| 18 | 样例在 `INPUT/` 根而脚本读子目录 | 布局过时 | 拷入 `INPUT/RINEX` 与 `INPUT/ORBITS` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Python 链 ROTI/ΔTEC/SIDX | **OASIS** |
| C++/XML 批监测 STEC+ROTI+AATR | **IonoMoni** |
| 校准 sTEC/vTEC | **pytecgg**（viventriglia） |
| 硬件 S4/σφ | ISMR |
| 仿真闪烁场 | [iono-scintillation](./iono-scintillation.md) |

## 8. 相关

[ionomoni](./ionomoni.md) · [pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [iono-scintillation](./iono-scintillation.md) · [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [ionex-gim](./ionex-gim.md) · [README](./README.md)
