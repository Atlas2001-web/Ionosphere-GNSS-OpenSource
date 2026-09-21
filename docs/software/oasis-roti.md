# OASIS（pyOASIS）· ROTI / ΔTEC / SIDX 操作手册

目录：[`PROJECTS.json` → `OASIS`](../../PROJECTS.json) · 上游 <https://github.com/giorgiopicanco/OASIS> · PyPI **`pyOASIS`** · **CC BY-NC 4.0**（商业先读 LICENSE）

> 岗位：RINEX OBS + **同日** MGEX SP3 → 电离层扰动指数。主产物 **ROTI、ΔTEC、SIDX**。不是硬件 S4/σφ，不是校准绝对 TEC，不是 GIM。以仓库 `main.py` / `*_CALC.py` 与 README 为准。

## 1. 用途与边界

**做：** 周跳/粗差 → 弧段 GF leveling → ROTI（常见 **1 min** 窗 TEC 变化率标准差）、ΔTEC（约 **15 vs 60 min** 平滑差）、SIDX（1 min 内 \|ROT\| 均值类）。RINEX 2/3；文档友好采样 **15/30 s**；GPS + GLONASS（Galileo/BeiDou 以上游为准）。**不依赖 DCB / GIM 产品。**

**不做：** 硬件闪烁 → ISMR；可控仿真 → [iono-scintillation](./iono-scintillation.md)；校准绝对 TEC → [pytecgg](./pytecgg.md)（作者 **viventriglia**）；全球球谐 GIM → 开源 GIM / [sh-gim](./sh-gim.md) 边界说明；C++ 批监测 → [ionomoni](./ionomoni.md)。

一句话：读盘后的 **Python 扰动指数链**；与 IonoMoni **只比趋势，不硬比绝对值**。

| 术语 | 含义 |
| --- | --- |
| ROTI | Rate of TEC Index |
| ΔTEC | 长短窗 leveled GF 之差（非绝对 TEC） |
| SIDX | Sudden Ionospheric Disturbance Index |
| GF leveling | 相位几何无关组合按弧段对齐到码 |
| IPP | 穿刺点（需 SP3） |

## 2. 安装

```bash
cd ~/work
python3 -m venv .venv && source .venv/bin/activate
# Windows: py -3.11 -m venv .venv && .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install pyOASIS
python -c "import pyOASIS; print('pyOASIS ok')"

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

## 3. 端到端：样例站日 → 指数文件

上游示例：`INPUT/boav0491.23o` + 同日 GFZ MGEX SP3（DOY 049 / 2023）。

### 3.1 检查输入

```bash
cd ~/work/OASIS
mkdir -p OUTPUT logs
ls -la INPUT/
head -n 3 INPUT/boav0491.23o
# 期望：RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
# SP3：同日；命名例 GFZ0MGXRAP_20230490000_01D_05M_ORB.SP3
ls INPUT/*SP3 INPUT/*.sp3 2>/dev/null
file INPUT/*SP3 2>/dev/null
```

缺 SP3：按 [data-access](../data-access.md) 从 CDDIS MGEX 取同日轨道（需 Earthdata）。日历换 DOY：可用 gnsscalendar 一类工具。**2018 前**常见前缀 `JAX0MGXFIN_`；**2018 后**常见 `GFZ0MGXRAP_`（以上游 README 为准）。

### 3.2 配置 `main.py`

```bash
grep -nE 'station|year|doy|doy|INPUT|OUTPUT|path|boav' main.py | head -n 40
# 编辑：站码、年、DOY、INPUT/OUTPUT——示例绝对路径不可照抄
```

### 3.3 跑流水线（步骤 × 脚本 × 产物）

```bash
python3 main.py 2>&1 | tee logs/oasis_run.log
echo EXIT:$?
find OUTPUT -type f | head -n 50
```

| 步骤 | 脚本 | 作用 / 典型产出 |
| --- | --- | --- |
| 轨道 | `SP3_INTERPOLATE.py` | SP3 → 观测历元；`ORBITS_YYYY_DOY.SP3` 类 |
| 清洗 | `RNX_CLEAN.py` | 读 RINEX、IPP、初标缺口/周跳 → `STAT_SAT_DOY_YYYY.RNX1` |
| 精筛 | `RNX_SCREENING.py` | ΔMW 残差 / 小弧段 → `.RNX2` |
| 对齐 | `RNX_LEVELLING.py` | 弧段 GF leveling（GPS L1–L2/L1–L5；GLO L1–L2/L2–L3）→ `.RNX3` |
| 指数 | `ROTI_CALC.py` | 对 `.RNX3` 算 ROTI |
| 指数 | `DTEC_CALC.py` | ΔTEC |
| 指数 | `SIDX_CALC.py` | SIDX |

**期望：** 日志走完 leveling；`OUTPUT` 下有按站/星组织的 leveled GF 与 ROTI/ΔTEC/SIDX（及示例图）。缺 SP3 → 死在轨道步。

### 3.4 输出字段（操作向）

| 产物 | 含义 | 误用 |
| --- | --- | --- |
| leveled GF | 弧段对齐后的几何无关组合 | 未 leveling 就算 ROTI → 假峰 |
| ROTI | 短窗 ROT 标准差（文档默认 1 min） | 改窗后与文献硬比数值 |
| ΔTEC | 15 vs 60 min 平滑差 | 当成绝对 TEC 发表 |
| SIDX | 短时 \|ROT\| 均值 | 与硬件 S4 混称 |
| IPP | 穿刺点 | SP3 日错 → 几何全错 |

### 3.5 接到下游

```bash
# 高 ROTI 时段 → 定位固定率（同窗）
# 绝对 TEC 形态 → pytecgg（不要用本页 ΔTEC 代替）
# 同站日可再跑 ionomoni，只比高值时段是否同向
```

教程：[05](../tutorials/05-scintillation-roti.md) · [20](../tutorials/20-storm-tec-analysis.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md)。

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| RINEX OBS 2/3 | 双频；15/30 s |
| MGEX SP3 | **同日**；放 `INPUT/` |
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
| 2 | 无 `.RNX3` | 单频或弧段被杀光 | 换双频站日；先 Anubis |
| 3 | ROTI 全空/NaN | 未 leveling 或采样不符 | 确认 `RNX_LEVELLING`；用 15/30 s |
| 4 | 1 Hz OOM / 窗义乱 | 非推荐采样 | `gfzrnx -smp 30` 后再跑 |
| 5 | 与 IonoMoni 差一个量级 | 窗口/周跳策略不同 | **比趋势**；笔记写定义 |
| 6 | 把 ROTI 写成 S4 | 物理量不同 | 改称 ROTI；S4 用 ISMR |
| 7 | 把 ΔTEC 当绝对 TEC | 误解产物 | → [pytecgg](./pytecgg.md) |
| 8 | SP3 用错天 | IPP 全错 | GPS week/DOY 日历核对 |
| 9 | cron 相对路径失效 | cwd 不同 | INPUT/OUTPUT 改绝对路径 |
| 10 | 夜峰全算赤道泡 | 多路径站 | 先 Anubis MP |
| 11 | 商业部署踩许可 | CC BY-NC | 读 LICENSE 或换工具 |
| 12 | 只跑到 RNX2 | 未跑 `*_CALC` | `find OUTPUT` 查指数文件 |
| 13 | GLONASS 怪值 | 频分通道 | 读 `glonass_channels.dat` / README |
| 14 | 与 GIM 像素比 ROTI | 对象不同 | GIM→[ionex-gim](./ionex-gim.md) |
| 15 | `head` 见 HTML | 下载成登录页 | 重走 Earthdata |
| 16 | 改窗后硬比文献 | 定义变了 | 报告声明窗口秒数 |

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
