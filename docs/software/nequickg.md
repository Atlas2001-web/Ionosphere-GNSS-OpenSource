# NequickG · Galileo NeQuick-G（Python）操作手册

目录：[`PROJECTS.json` → `NequickG`](../../PROJECTS.json) · 上游 <https://github.com/tpl2go/NequickG>（本机 clone 可访问；末提交 `1d17834` 2017-12-01）· **无 SPDX 许可字段**（使用前自核 README/引用 Galileo ICD）· 本机验证：对源码做 **Python 3 最小语法移植** 后跑通 `vTEC` + ESA Medium 校验表第 1 行；**质检复跑**确认数值一致并补 Medium 全表 36 行统计（2026-09-24 ET）。上游原文为 **Python 2**（`print` 语句）

> 岗位：用 **Galileo 广播 ai0/ai1/ai2** 算本地电子密度廓线、垂直/斜 TEC，对照 ESA 校验表。冲突时：**仓内 `tasks/` / `Validation.py` > 本文**。生产接收机改正优先官方 C 实现（见 §6）。

## 1. 用途与边界

**做：**

- `NequickG_global(时间, 广播系数)` → 全球模型；`get_Nequick_local(Position)` → 单点 `NequickG`
- `vTEC(h1,h2)` / `vTEC_ratio()`：高度积分垂直 TEC、底/顶比
- `sTEC(Ray)` / `sTEC2(Ray)`：视线斜 TEC（校验表主路径）
- 内置 `CCIR_MoDIP/` 系数；`Validation/*_reference.dat` 对照 ESA 高/中/低太阳活动表

**不做：**

- **不是** ITU 气候态 NeQuick 2 → `Nequick-ITUR` / ICTP NeQuick2（见 PROJECTS）
- **不是** 读 RINEX/算实测 STEC → [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)
- **不是** 读 IONEX GIM → [ionex-gim](./ionex-gim.md)
- **未实现** 电离层扰动旗标（上游 README 明文）
- **不是** 官方认证实现：数值须用 ESA 表自核；嵌入产品用 GSC/JRC C 源码

一句话：NequickG = **社区 Python 版 Galileo 单频电离层改正模型**，便于脚本/教学；官方 C 另见 §6。

| 术语 | 含义 |
| --- | --- |
| `NEQTime(mth, UT)` | 月（1–12）与世界时（小时） |
| `Position(lat, lon)` | 地理纬/经（度） |
| `GalileoBroadcast(ai0, ai1, ai2)` | Galileo 电离层广播三系数 |
| `Ray(h1,lat1,lon1,h2,lat2,lon2)` | 直线传播路径；高程 **km** |
| `Az` / MODIP | 有效电离参数；修正磁倾角（模型内部） |

## 2. 安装

上游 **不提供** `setup.py` / PyPI；依赖 **numpy**（画图任务另需 matplotlib；Basemap 已过时，本手册 E2E 不依赖）。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/tpl2go/NequickG.git
cd NequickG
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip numpy
# 上游是 Python 2。本机仅有 Python 3.13 → 复制后做最小语法移植（勿改 origin 工作树也可）：
cp -a . ../NequickG_py3 && cd ../NequickG_py3
python - <<'PY'
import re, pathlib
for p in pathlib.Path(".").rglob("*.py"):
    if ".git" in p.parts: continue
    t = p.read_text(encoding="utf-8", errors="replace")
    t2 = re.sub(r"(?m)^([ \t]*)print(?!\s*\()([ \t]+.+)$",
                lambda m: m.group(1) + "print(" + m.group(2).strip() + ")", t)
    t2 = t2.replace("with file(", "with open(")
    t2 = re.sub(r"\bfile\(", "open(", t2)
    t2 = re.sub(r"\bxrange\(", "range(", t2)
    t2 = re.sub(r"except\s+(\w+)\s*,\s*(\w+)\s*:", r"except \1 as \2:", t2)
    # Py3: map 返回迭代器，Validation.py 的 row[0] 会 TypeError
    t2 = t2.replace("row = map(float, row)", "row = list(map(float, row))")
    if t2 != t: p.write_text(t2)
print("py3_patch_done")
PY
python -c "from NequickG import NEQTime; print('import_ok', NEQTime)"
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `SyntaxError: Missing parentheses in call to 'print'` | 源码是 Py2 | 按上表移植；或找仍带 Py2 的环境（不推荐） |
| `ModuleNotFoundError: numpy` | 未装 | `pip install numpy` |
| `No module named NequickG` | 不在仓根 | `cd` 到含 `NequickG.py` 的目录再跑 |
| `TypeError: 'map' object is not subscriptable` | 只改了 `print`，未改 `map` | §2 补丁含 `list(map(...))`；或手改 `Validation.py` |
| Basemap 安装失败 | 依赖已死 | 跳过 `tasks/parameter_maps.py` 绘图；算 TEC 不需要 |

## 3. 端到端：vTEC + Medium 校验第 1 行（本机真跑）

在 **已移植** 的 `~/iono_ops/NequickG_py3` 下执行（等同 `tasks/vTEC.py` + 截取 `Validation.py`）。

### 3.1 垂直 TEC（高 Az 广播系数）

```bash
cd ~/iono_ops/NequickG_py3
python -W ignore - <<'PY'
from NequickG import NEQTime, Position, GalileoBroadcast
from NequickG_global import NequickG_global

TX = NEQTime(4, 12)                 # April, 12 UT
RX = Position(40, 0)                # 40N, 0E
BX = GalileoBroadcast(236.831, 0, 0)
NEQ, Para = NequickG_global(TX, BX).get_Nequick_local(RX)
v_raw = NEQ.vTEC(100, 2000)         # 积分高度 km
print(f"vTEC_raw={v_raw}")
print(f"vTEC_TECU_with_x1000={v_raw * 1000 / 1e16:.4f}")  # 见字段说明
print(f"vTEC_ratio={NEQ.vTEC_ratio():.4f}")
print(f"foF2_MHz={Para.foF2:.4f} hmF2_km={Para.hmF2:.2f} "
      f"NmF2={Para.NmF2:.4f} modip_deg={Para.modip:.2f}")
PY
```

**本机 stdout（2026-09-24 ET）：**

```text
vTEC_raw=796397393584444.4
vTEC_TECU_with_x1000=79.6397
vTEC_ratio=1.7527
foF2_MHz=14.5999 hmF2_km=388.27 NmF2=26.4315 modip_deg=47.55
```

### 3.2 斜 TEC ↔ ESA Medium 表一行

`Validation/Medium_reference.dat` 列：`mth UT lon1 lat1 h1_m lon2 lat2 h2_m stec_TECU`（高程文件里是 **米**，`Ray` 要 **公里**）。广播系数见上游 `Validation.py`。

```bash
python -W ignore - <<'PY'
from NequickG import NEQTime, GalileoBroadcast
from NequickG_global import NequickG_global, Ray

row = open("Validation/Medium_reference.dat").readline().split()
BX = GalileoBroadcast(121.129893, 0.351254133, 0.0134635348)
mth, UT = int(float(row[0])), int(float(row[1]))
lon1, lat1, h1 = float(row[2]), float(row[3]), float(row[4]) / 1000.0
lon2, lat2, h2 = float(row[5]), float(row[6]), float(row[7]) / 1000.0
exp = float(row[8])
ray = Ray(h1, lat1, lon1, h2, lat2, lon2)
got = NequickG_global(NEQTime(mth, UT), BX).sTEC(ray) / 1e16
print("row0", row)
print(f"expected_TECU={exp} got_TECU={got:.4f} rel_err_pct={abs(got-exp)/exp*100:.2f}")
PY
```

**本机：**

```text
row0 ['4', '0', '40.19', '-3.00', '-23.32', '76.65', '-41.43', '20157673.93', '18.26']
expected_TECU=18.26 got_TECU=19.0635 rel_err_pct=4.40
```

**Medium 全表 36 行（同系数循环，本机质检复跑）：** `max_rel%=9.45` · `mean_rel%=1.59`（前三行 rel% ≈ 4.40 / 1.32 / 3.60）。

勿指望最小 `print` 移植后直接 `python Validation.py`：即便加了 `list(map(...))`，脚本末尾默认跑 **Low** 表并 `plt.show()`（要 matplotlib，且会阻塞）。产品验收用上面的行循环，或改脚本只 `run('Medium')` 并去掉绘图。高/低活动 `GalileoBroadcast` 系数见仓内 `Validation.py`。

### 3.3 API / 旗标（类参数）

| 符号 | 作用 |
| --- | --- |
| `NEQTime(mth, universal_time)` | 驱动 CCIR 月份与地方时相关项 |
| `Position(latitude, longitude)` | 度；东经为正 |
| `GalileoBroadcast(ai0, ai1, ai2)` | 与 Galileo OS 电离层 ICD 广播一致 |
| `Ray(h1, lat1, lon1, h2, lat2, lon2)` | 观测端→卫星端；`h*` 为 **km** |
| `get_Nequick_local(pos)` | 返回 `(NequickG, parameters)` |
| `vTEC(h1, h2, tolerance=None)` | 垂直积分；`tolerance` 默认低轨 0.001 / 高 0.01 |
| `sTEC(ray, tolerance=None)` | 斜积分；末尾 `*1000`（km→m 尺度）；竖直近距时回退 `vTEC` |
| `sTEC2(ray)` | 另一套斜积分实现（`tasks/sTEC.py` 对比用） |

| 输出字段 | 含义 |
| --- | --- |
| `sTEC(...) / 1e16` | **TECU**（与 ESA 校验表同量纲；本机 Medium 行用此） |
| `vTEC(...)` 原始返回值 | **未**乘 `sTEC` 里的 `*1000`；要与 TECU 对齐需 `*1000/1e16`（本机坑） |
| `vTEC_ratio()` | `vTEC(hmF2→20000) / vTEC(0→hmF2)`，无量纲 |
| `Para.foF2` / `hmF2` / `NmF2` / `modip` | 临界频率 (MHz)、峰高 (km)、峰密度、修正磁倾角 |

## 4. 接到哪步

- 概念：教程 [02](../tutorials/02-gnss-dualfreq-tec.md) / [03](../tutorials/03-gim-ionex.md)；单频改正对照实测 → [pytecgg](./pytecgg.md) + [ionex-gim](./ionex-gim.md)
- 广播系数来源：Galileo NAV / ICD；不要与 NeQuick2 太阳黑子数入口混用
- 数据入口：[data-access](../data-access.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `SyntaxError` on `print "..."` | Py2 源码 | 用 §2 移植脚本；或 `2to3` |
| 2 | `vTEC/1e16` 只有 ~0.08 TECU，不合理 | `vTEC` 缺 `sTEC` 的 `*1000` | `tecu = vTEC(h1,h2)*1000/1e16` |
| 3 | `calulcating vTEC instead` | `Ray` 水平距过近（`p_radius<0.1`） | 用校验表异地两端；竖直场景直接调 `vTEC` |
| 4 | 与 ESA 表差几 percent | 社区实现/已知数值问题（README：低活动 foF1 可能为负） | 跑 `Validation.py` 定量；产品链改官方 C |
| 5 | `h1` 传了米导致路径荒谬 | 文件是米、`Ray` 要 km | `/1000.0` 再进 `Ray` |
| 6 | `import CCIR_MoDIP...` 失败 | 工作目录不对 | 在仓根运行；`PYTHONPATH=.` |
| 7 | `overflow` / `invalid value` RuntimeWarning | 廓线指数溢出 | `python -W ignore`；检查 Az 与纬度是否极端 |
| 8 | 当接收机认证模型 | 非 JRC/GSC 发布 | 改用 §6 官方源码并按其测试向量验收 |
| 9 | `Validation.py` → `map` TypeError | Py2 `map`→list，Py3 是迭代器 | §2 补丁；或 `row = list(map(float, row))` |
| 10 | `Validation.py` 卡住 / 要 GUI | 末尾 `compare`→`plt.show()` | 注释绘图；或只用 §3.2 行循环（本机 Medium 36 行 ~1 min） |

## 6. 官方 C 回退（登记下载）

若 Python 仓不可用或要入产品：

| 条目 | URL | 说明 |
| --- | --- | --- |
| **Galileo-NeQuick-G**（GSC） | 手册 [galileo-nequick-g](./galileo-nequick-g.md) · <https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code> | 官方 C11 + 测试；**注册/接受 EUPL-1.2** 后下加密包。本机**未**跑（无账号）；细节/门禁以专页为准，**勿在此复制** |
| ESA ESSR | <https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model> | 登记页；许可 ESA Community License |
| NeQuickJRC 镜像 | <https://github.com/mgfernan/NeQuickJRC> | 社区整理；非权威托管 |

安装极限（诚实）：官方包不经公开直链；无法在无注册环境下给出可复现 `cmake && ./test` 日志。拿到包后按其 `README`/测试驱动验收，**不要**假设与本 Python 仓 bit 级一致。

## 7. 选型与链接

| 你要… | 用 |
| --- | --- |
| 脚本/教学快速 sTEC | **本文 NequickG** |
| 认证/嵌入接收机 | GSC **Galileo-NeQuick-G** C |
| 气候态 NeQuick2 | ICTP / `Nequick-ITUR`（非 Galileo 广播入口） |
| 实测双频 TEC | [pytecgg](./pytecgg.md) / [gnss-tec](./gnss-tec.md) |

- ICD：<https://www.gsc-europa.eu/system/files/galileo_documents/Galileo_Ionospheric_Model.pdf>
- 兄弟：[galileo-nequick-g](./galileo-nequick-g.md)（官方 C 门禁）· [ionex-gim](./ionex-gim.md) · [pytecgg](./pytecgg.md) · [gnss-tec](./gnss-tec.md) · [sh-gim](./sh-gim.md) · [data-access](../data-access.md)
