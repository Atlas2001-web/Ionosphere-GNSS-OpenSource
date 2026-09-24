# CSSRlib · Python PPP / PPP-RTK 操作手册

目录：[`PROJECTS.json` → `cssrlib`](../../PROJECTS.json) · 上游 <https://github.com/hirokawa/cssrlib> · 样例仓 <https://github.com/hirokawa/cssrlib-data> · PyPI **`cssrlib`** · MIT · 本机验证 **1.2.1**（`2025.10.14` 包内版本戳）+ `cssrlib-data` `doy2025-046` SPP 实跑

> 岗位：开放增强服务（QZSS CLAS / Galileo HAS / BDS PPP / IGS SSR 等）的 **Python PPP/PPP-RTK/RTK 试验与教学**。思路贴近 RTKLIB。冲突时：**本机 `import cssrlib` / 上游 README / `cssrlib-data/samples` > 本文**。

## 1. 用途与边界

**做：**

- 解码 Compact SSR、RTCM/IGS SSR、HAS/BDS PPP 等改正；读 RINEX OBS/NAV、SP3
- 脚本级 **SPP / RTK / PPP / PPP-RTK**（`pntpos` / `rtk` / `ppp` / `ppprtk` / `pppssr`）
- Colab / Jupyter 教程（仓内 `tutorials/`）；配套数据在 **`cssrlib-data`**

**不做：**

- 发表级 PPP-AR 产线 → [pride-pppar](./pride-pppar.md)
- 轻量 CLI 事后定位主力 → [rtklib](./rtklib.md)（`rnx2rtkp`）
- 校准 sTEC/vTEC / ROTI → [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md) / [oasis-roti](./oasis-roti.md)
- 实时多用户播发 → [bkg-ntripcaster](./bkg-ntripcaster.md) / [bnc](./bnc.md)
- 电离层在此是 **改正/状态量**，不是 GIM/STEC 产品

一句话：CSSRlib = **可读的 Python 开放 PPP/PPP-RTK 试验箱**；要论文级坐标固定率用 PRIDE。

| 术语 | 含义 |
| --- | --- |
| Compact SSR / CLAS | QZSS 紧凑状态空间改正；PPP-RTK |
| HAS / BDS PPP | Galileo / 北斗卫星播发 PPP 改正 |
| `rSigRnx` | 信号选择，如 `GC1C`、`EL5Q` |
| `stdpos` / `ppprtkpos` | 单点 / PPP-RTK 处理入口 |
| `cssrlib-data` | 官方样例 OBS/NAV/L6 与 `test_*.py` |

## 2. 安装

```bash
cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate   # 需要 Python ≥3.10
python -m pip install -U pip
python -m pip install cssrlib pandas pysolid
# cartopy 失败时（Debian/Ubuntu）：
# sudo apt-get install -y libgeos++-dev && pip install cartopy
python -c "import cssrlib, importlib.metadata as m; print(m.version('cssrlib'), cssrlib.__file__)"
# 期望类似：1.2.1 .../site-packages/cssrlib/...

# 完整样例（强烈建议；含 OBS/NAV/改正）
git clone --depth 1 https://github.com/hirokawa/cssrlib-data.git
# 部分脚本还需 IGS 产品：
# cd cssrlib-data/samples && python igs_download.py
```

开发版：`pip install -U git+https://github.com/hirokawa/cssrlib.git@main`（与 `cssrlib-data` **同分支**）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | Python &lt;3.10 | `python3.12 -m venv .venv` |
| `ModuleNotFoundError: pandas` | PyPI 元数据未列、但 `ewss`/`pntpos` 链会 import | `pip install pandas` |
| `ModuleNotFoundError: pysolid` | 固体潮；PPP 样例常要 | `pip install pysolid` |
| cartopy / GEOS 编译失败 | 缺系统库 | `sudo apt-get install -y libgeos++-dev` 后重装 |
| leap second mild warning | `pysolid` 闰秒表过期 | `pip install -U pysolid` |

## 3. 端到端：样例站日 → SPP（本机真跑）

数据：`cssrlib-data/data/doy2025-046/`（`046r_rnx.obs` + `046r_rnx.nav`，RINEX 4 OBS）。入口等价于上游 `samples/test_pntpos.py`（dataset=3），此处截断到 **60 历元** 以便复现。

### 3.1 摆放与冒烟

```bash
cd ~/iono_ops/cssrlib-data/samples
export MPLBACKEND=Agg
ls ../data/doy2025-046/046r_rnx.{obs,nav}
python test_rnx.py 2>&1 | head -n 8
```

**本机截断 stdout（cssrlib 1.2.1，2026-09-24 ET）：**

```text
2025-02-15 17:00:01
G29 C1C  25531815.275  C2W         0.000  ...  L1C         0.000  ...
C60 C2I  39775928.006  C6I  39775914.179  ...  L2I 207123840.215  ...
G23 C1C  23919537.649  C2W  23919538.295  ...  L1C 125698028.321  L2W  97946535.729  ...
```

| 输出 | 含义 |
| --- | --- |
| 首行时间 | 首历元 `time2str(obs.t)` |
| `G23 C1C … L1C …` | 该星伪距/载波；`0.000` = 该信号无效或未选中 |

### 3.2 关键参数（API）

| 符号 / 调用 | 作用 |
| --- | --- |
| `rSigRnx("GC1C")` 等 | 限定系统+观测量；多系统就 `extend` |
| `rnxdec().setSignals(sigs)` | 注册信号表 |
| `decode_nav(navfile, Nav())` | 广播星历 → `nav.eph` / `nav.geph` |
| `decode_obsh` / `decode_obs` | 头 + 逐历元观测 |
| `autoSubstituteSignals()` | 缺测时自动替信号 |
| `stdpos(nav, rnx.pos, log)` | 单点定位滤波器；`nav.pmode=1` 动态 |
| `nav.t = obs.t`（首历元） | 对齐滤波器时间；**漏写则 ENU 千米级发散** |
| `nav.elmin` | 高度截止（弧度）；示例 `5°` |
| `ecef2enu(pos_ref, dx)` | ECEF 残差 → 站心 ENU（需真值） |

### 3.3 SPP 60 历元（完整可跑脚本）

```bash
cd ~/iono_ops/cssrlib-data/samples
export MPLBACKEND=Agg
python - <<'PY'
import numpy as np
from cssrlib.rinex import rnxdec
from cssrlib.gnss import Nav, rSigRnx, ecef2pos, ecef2enu, epoch2time, time2str
from cssrlib.pntpos import stdpos

ep = [2025, 2, 15, 17, 0, 0]
xyz_ref = [-3962108.6819, 3381309.5707, 3668678.6750]  # 样例真值
pos_ref = ecef2pos(xyz_ref)
t_start = epoch2time(ep)
navfile = '../data/doy2025-046/046r_rnx.nav'
obsfile = '../data/doy2025-046/046r_rnx.obs'
sigs = [rSigRnx(s) for s in
        ("GC1C","GL1C","GS1C","EC1C","EL1C","ES1C","JC1C","JL1C","JS1C")]
dec = rnxdec(); dec.setSignals(sigs)
nav = Nav(nf=1); nav.pmode = 1
nav = dec.decode_nav(navfile, nav)
assert dec.decode_obsh(obsfile) >= 0
dec.autoSubstituteSignals()
std = stdpos(nav, dec.pos, 'spp_smoke.log')
nav.elmin = np.deg2rad(5.0)
obs = dec.decode_obs()
while t_start > obs.t and obs.t.time != 0:
    obs = dec.decode_obs()
print('start', time2str(obs.t), 'eph', len(nav.eph), 'geph', len(nav.geph))
for ne in range(60):
    if ne == 0:
        nav.t = obs.t   # 必须：首历元对齐滤波器时间，否则 tt 巨大→发散
    std.process(obs, cs=None)
    enu = ecef2enu(pos_ref, nav.x[0:3] - xyz_ref)
    d2 = float(np.sqrt(enu[0]**2 + enu[1]**2))
    if ne < 5 or ne % 15 == 0 or ne == 59:
        print(f"{time2str(obs.t)} ENU {enu[0]:7.3f} {enu[1]:7.3f} {enu[2]:7.3f}, "
              f"2D {d2:6.3f}, mode {nav.smode}")
    obs = dec.decode_obs()
    if obs.t.time == 0:
        break
dec.fobs.close()
if nav.fout: nav.fout.close()
PY
```

**本机截断 stdout（cssrlib 1.2.1，含 `nav.t=obs.t`，60 历元，2026-09-24 ET）：**

```text
start 2025-02-15 17:00:01 eph 313 geph 36
2025-02-15 17:00:01 ENU   0.558   1.226   1.669, 2D  1.347, mode 1
2025-02-15 17:00:02 ENU   0.090   0.303   0.304, 2D  0.316, mode 1
2025-02-15 17:00:03 ENU  -0.063   0.145   0.315, 2D  0.158, mode 1
2025-02-15 17:00:04 ENU  -0.135   0.132   0.403, 2D  0.189, mode 1
2025-02-15 17:00:05 ENU  -0.208   0.129   0.300, 2D  0.245, mode 1
2025-02-15 17:00:16 ENU  -0.065  -0.091   0.758, 2D  0.112, mode 1
2025-02-15 17:00:31 ENU  -0.143  -0.024   0.898, 2D  0.145, mode 1
2025-02-15 17:00:46 ENU  -0.064   0.207   0.578, 2D  0.217, mode 1
2025-02-15 17:01:00 ENU   0.062   0.192   0.522, 2D  0.201, mode 1
```

日志头（`spp_smoke.log`）：

```text
2025-02-15 17:00:01  G11 - edit - low elevation   2.3 deg
2025-02-15 17:00:01  G29 - edit - low elevation   3.2 deg
2025-02-15 17:00:01  E11 - edit C1C  - invalid PR obs
```

| 字段 | 含义 | 误用 |
| --- | --- | --- |
| ENU E/N/U [m] | 相对样例真值的站心残差 | 当成 PPP 收敛曲线对外报价 |
| 2D | √(E²+N²) | 忽略 U 分量起伏 |
| `mode` | `nav.smode`（此处 SPP≈1） | 与 RTKLIB `Q=` 编号混比 |
| `edit low elevation` | 低于 `elmin` 被踢 | 以为无星 |

**未在本机跑完（诚实边界）：** `test_ppprtk.py`（CLAS L6）、`test_ppphas.py`（HAS）、`test_pppbds.py` 等需改正流 + 常要 `pysolid`/ANTEX（`igs_download.py`）。命令形态：`cd samples && python test_ppprtk.py`（先改 `config_ppprtk.yml` / `dataset`）。**禁止**把上文 SPP 的米级 2D 写成 PPP-RTK 厘米级结果。

### 3.4 接到下游

- 开放服务教学 / 改正接入试验 → 教程 [06](../tutorials/06-iono-positioning.md)
- 要发表级坐标/固定率 → [pride-pppar](./pride-pppar.md)；CLI 冒烟 → [rtklib](./rtklib.md)
- 磁暴日看定位是否抖 → 同站日 [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md) 对照高 ROTI 时段
- 拉实时改正流 → [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md)

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| RINEX OBS/NAV | 样例为 RINEX 4；自备数据时信号名与 `rSigRnx` 一致 |
| Compact SSR / HAS / BDS / RTCM SSR | 与观测**同时段**；CLAS 常需 L6 日志 |
| SP3 / ANTEX | IGS PPP 样例；先 `igs_download.py` |
| `config_ppp.yml` / `config_ppprtk.yml` | `elmin`、`iono_opt`、`armode` 等 |

| 输出 | 下游 |
| --- | --- |
| ECEF / ENU 时间序列、日志 | 教学图、与 RTKLIB/PRIDE 对照 |
| 解码后的 SSR/HAS 结构 | 自写滤波器；不是 IONEX |

**明确不输出：** 校准 STEC、ROTI、GIM。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 D 定位教学（开放 PPP） | §3 | [06](../tutorials/06-iono-positioning.md) · [rtklib](./rtklib.md) |
| CLAS/HAS 改正接入 | `cssrlib-data` `test_ppp*` | 官方 Colab · 各服务 ICD |
| 发表级 PPP-AR | — | [pride-pppar](./pride-pppar.md) |
| 高 ROTI↔固定率 | §3.4 | [oasis-roti](./oasis-roti.md) · [pride-pppar](./pride-pppar.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `import cssrlib.pntpos` 要 pandas | 传递依赖未声明全 | `pip install pandas` |
| 2 | 首历元后 ENU 千米级发散 / `too few satellites` | 未设 `nav.t = obs.t`，`timediff(obs.t, nav.t)` 巨大 | 循环首步：`if ne==0: nav.t = obs.t`（见 §3.3） |
| 3 | PPP 脚本固体潮警告/炸 | 缺或旧 `pysolid` | `pip install -U pysolid` |
| 4 | `test_eph.py` 找不到 brdc | 未下 IGS / 无 `data/brdc` | `cd samples && python igs_download.py` |
| 5 | cartopy 安装失败 | 缺 GEOS | `sudo apt-get install -y libgeos++-dev` |
| 6 | 几乎无星 / 全 `invalid PR` | `sigs` 与接收机观测量不匹配 | 对照 `test_rnx.py` 打印改 `rSigRnx` |
| 7 | ENU 几十米不收敛 | 当真值的坐标错日/错站 | 用样例 `xyz_ref`；或先 SPP 估近似 |
| 8 | CLAS 无解 | L6 通道/PRN/时段不对 | 核对 `config_ppprtk.yml` 与 `decode_msg` 的 `prn_ref` |
| 9 | cssrlib 与 data 行为不一致 | 主从分支漂移 | 两边都 pin `@main` 或同 tag |
| 10 | 无头机弹 GUI | matplotlib 默认后端 | `export MPLBACKEND=Agg` |
| 11 | 把 SPP 2D 写成 HAS/CLAS 精度 | 未跑改正链 | 只引用对应 `test_ppp*` 真日志 |
| 12 | RINEX 4 头读失败 | 旧 cssrlib | `pip install -U cssrlib` |
| 13 | `leap second table` mild warning | 闰秒表过期 | `pip install -U pysolid` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Python 学 CLAS/HAS/BDS PPP | **CSSRlib** + cssrlib-data |
| 发表级 PPP-AR / ZTD | **PRIDE-PPPAR** |
| 事后 CLI RTK/浮点 PPP | **RTKLIB** explorer |
| 只解码 NTRIP / 录盘 | [pygnssutils](./pygnssutils.md) / [bnc](./bnc.md) |
| STEC 重建 | [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) |

## 8. 相关

[rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [oasis-roti](./oasis-roti.md) · [gnss-tec](./gnss-tec.md) · [pytecgg](./pytecgg.md) · [README](./README.md)
