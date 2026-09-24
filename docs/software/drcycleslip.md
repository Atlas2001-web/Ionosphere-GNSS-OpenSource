# DRCycleSlip · 三频周跳探测/修复教学脚本操作手册

目录：[`PROJECTS.json` → `DRCycleSlip`](../../PROJECTS.json) · 上游 <https://github.com/Jin-Whu/DRCycleSlip> · **无 PyPI / 无 setup.py / 无 LICENSE** · tip **`f57d74d`**（tag 文案 `v1.0`，2017-02-23）· 本机 Python **3.13** + numpy/scipy/matplotlib 实跑（2026-09-24 EDT）

> 岗位：武汉大学相关教学脚本——对 **RINEX 3** 单颗 **GPS/BDS 三频** 弧段做几何无关组合二阶差分周跳探测，并用仓内 `{PRN}cycleslip.txt` **注入已知周跳**后验证能否解出 `(ΔN1,ΔN2,ΔN3)`。冲突时：**仓内源码 / 本机 stdout > 本文**。**不是** [cycle-slip-correction](./cycle-slip-correction.md)（EMBRACE rTEC 四阶差分 CLI）；生产 QC 优先 [anubis](./anubis.md)。

## 1. 用途与边界

**做：**

- `search.py`：按阈值搜 GPS(`g`)/BDS(`b`) 三频组合（波长、电离层系数、σ、检出概率）
- `find_cycleslip.py`：暴力枚举满足三组合整数条件的候选 `(i,j,k)`
- `process.py`：读 RINEX 3 OBS → 注入 `{PRN}cycleslip.txt` → 三组合二阶差分探测 → 解线性方程修复相位（内存）→ 出 `{PRN}.eps` / `{PRN}ion.eps`

**不做：**

- **不**写回改正后的 RINEX / 不产 XTR/XML QC → [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)
- **不是**双频 rTEC 四阶差分试验 CLI → [cycle-slip-correction](./cycle-slip-correction.md)（依赖 georinex；默认 G/R；出 PDF）
- **不**读 RINEX 2.x（历元行无 `>`）/ **不**处理 Galileo·QZSS·GLONASS
- **不**提供 pip 包或开箱 CLI（`process.py` 的 `argparse` 入口被注释，默认硬编码 Windows 路径）
- 仓内样例名 `jfng0760.13o` **未随仓分发**；须自备三频 R3

一句话：**DRCycleSlip = 2017 教学级三频周跳注入–探测–修复脚本**；接到 TEC 前请先确认是否真要「注入验证」而非生产清洗。

| 术语 | 含义 |
| --- | --- |
| 三频组合 | GPS 默认 `[-6,1,7]`/`[3,0,-4]`/`[4,-8,3]`；BDS static `[-4,1,4]`/`[-3,6,-2]`/`[4,-2,-3]` |
| `deltaN` | 组合值二阶差分；超 `threshold` 标周跳 |
| `{PRN}cycleslip.txt` | **注入**表：`epoch b1 b2 b3`；探测前写入相位 |
| `static`/`move` | BDS 动态档换另一组组合/门限；GPS 两档相同 |
| 与 CSC 差异 | 本工具自解析 R3 列偏移；CSC 走 [georinex](./georinex.md) + rTEC |

## 2. 安装

**无 PyPI。** clone 后装科学计算依赖即可（本机 2026-09-24 EDT）：

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/Jin-Whu/DRCycleSlip.git
cd DRCycleSlip
git rev-parse --short HEAD   # 期望：f57d74d

python3 -m venv ~/iono_ops/drcs_demo/.venv
source ~/iono_ops/drcs_demo/.venv/bin/activate
python -m pip install -U pip
python -m pip install 'numpy>=1.26' 'scipy>=1.11' 'matplotlib>=3.8'
python - <<'PY'
import numpy, scipy, matplotlib
print(numpy.__version__, scipy.__version__, matplotlib.__version__)
PY
# 期望示例：2.5.3 1.18.1 3.11.2
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ModuleNotFoundError: scipy` | 未装 | `pip install scipy numpy matplotlib` |
| `Not find C:\Users\jin\...` | `__main__` 硬编码 Windows OBS | 改路径或按下节 `process(...)` 调用 |
| `FileNotFoundError` 写 eps | `savefig` 硬编码 `C:\Users\jin\OneDrive\...` | 改 `plotcycleslip`/`plotiond` 落盘目录；`MPLBACKEND=Agg` |
| `pip install DRCycleSlip` 404 | **未发布** | 只 clone |

## 3. 端到端：组合搜索 → BAKO G24 注入探测（本机真跑）

上游 README 仅两行；样例 OBS `jfng0760.13o` 不在仓内。本机用 PRIDE 例程 **BAKO** RINEX **3.03**（GPS：`C1C L1C … C5Q L5Q`），对 **G24** 注入仓内 `G24cycleslip.txt` 的历元 **700** 跳 `(23,18,17)`。

### 3.1 组合搜索 / 候选枚举（无需 RINEX）

```bash
source ~/iono_ops/drcs_demo/.venv/bin/activate
cd ~/iono_ops/DRCycleSlip

python find_cycleslip.py | head -20
# 期望片段：
# BDS:
# 1 1 1
# …
# GPS
# 4 3 3
# 23 18 17

python search.py g 1.0 | head -8
# 期望含：-6 1 7 29.305 … 与 Group: … -6 1 7 3 0 -4 4 -8 3 …
python search.py   # 无参
# 期望：
# Args:
# 	system
# 	threshold
```

**本机截断（tip `f57d74d`，2026-09-24 EDT）：**

```text
BDS:
1 1 1
4 3 3
5 4 4
…
GPS
4 3 3
23 18 17
…

-6 1 7 29.305 24.525 0.186 0.187 0.220
-3 1 3 9.768 12.242 0.094 0.112 0.365
3 0 -4 14.653 -12.283 0.103 0.111 0.257
4 -8 3 29.305 -11.770 0.189 0.190 0.223

Group:
-6 1 7 3 0 -4 4 -8 3 99.18% 99.14% 94.86%
```

### 3.2 探测/修复（须改路径；BAKO + G24）

```bash
# 自备三频 R3，或链到已有 BAKO：
#   BAKO00IDN_R_20212200000_01D_30S_MO.rnx
export MPLBACKEND=Agg
source ~/iono_ops/drcs_demo/.venv/bin/activate
cd ~/iono_ops/DRCycleSlip

# 先把 process.py 内两处 savefig 的 Windows 路径改成本机目录（否则写盘失败）
# 再调用（CLI 被注释，推荐直接调 process）：
python - <<'PY'
import process as P
P.iond=[]; P.cycleslip=[]; P.deltaN_lst=[]; P.precycleslip=[]
# G24cycleslip.txt 含 200/450/700；BAKO 上 G24 仅约历元 602–800 有弧
P.process('/path/to/BAKO00IDN_R_20212200000_01D_30S_MO.rnx', 'G24', 1, 800, 'static')
PY
```

**本机 stdout（注入表含 `700 23 18 17`；G24 弧内仅该跳可触发）：**

```text
700 23.00000000000024 18.000000000000192 17.00000000000018 -1.23 1.13 -1.10
```

含义：历元 **700** 解出周跳向量 **≈(23, 18, 17)**（与注入一致）；末三列为三组合 `deltaN`。空注入表（仅表头）时同窗 **n_detected=0**。产物：`G24.eps`、`G24ion.eps`（改路径后）。

## 4. I/O

| | 说明 |
| --- | --- |
| **输入 OBS** | RINEX **3.x**（历元行含 `>`）；头 `SYS / # / OBS TYPES` **单行**（续行不解析） |
| **GPS 观测** | 映射 `C1/L1/C2/L2/C5/L5`（取码前两字符；同名前缀后写覆盖，如 C2W 盖 C2S） |
| **BDS 观测** | `C2`/`C7`/`C6`（及 L*）；缺三频则 `setvalue` 抛错被裸 `except` 跳过 |
| **注入表** | 与脚本同目录 `{PRN}cycleslip.txt`；无文件则 `readcycleslip` 直接异常 |
| **输出 OBS** | **无**（修复只在内存；`repair` 供探测链使用） |
| **输出图** | `{PRN}.eps`（三组合 deltaN）+ `{PRN}ion.eps`（ΔI / ΔΔI）；默认 Windows 绝对路径 |
| **stdout** | 每条：`epochnum N1 N2 N3 deltaN0 deltaN1 deltaN2` |

## 5. 参数

| 项 | 作用 |
| --- | --- |
| `search.py system` | `g`=GPS L1/L2/L5；`b`=BDS B1/B2/B3 频率 |
| `search.py threshold` | 组合 σ 过滤上限（本机示例 `1.0`） |
| `process(filepath, prn, start, end, state)` | OBS 路径；PRN 如 `G24`/`C03`；历元窗；`static`/`move` |
| `G24cycleslip.txt` 等 | 注入时刻与 `(b1,b2,b3)`；上游默认四星：C03/C09/C12/G24 |

## 6. 接到哪步

```text
[data-access] 取 RINEX 3 三频 OBS
    → georinex 探活列名/是否缺 L5·B3
    → DRCycleSlip（本手册：教学注入–探测；或 dig 算法）
    → 生产清洗/QC：[anubis] / 试验对照：[cycle-slip-correction]
    → TEC：[gnss-tec] / [pytecgg]
```

路径 A 一日 TEC：在 [georinex](./georinex.md) 之后可选本工具做**方法对照**，不要替代 Anubis 完好率报告。

## 7. 坑（≥8）

1. **无 PyPI / 无 setup / 无许可证文件** — 只能 clone；商用前自行评估版权。
2. **`__main__` CLI 整段注释** — 默认跑死 Windows 路径 `C:\Users\jin\Downloads\jfng0760.13o`；须改源码或 `import process`。
3. **`savefig` 硬编码 OneDrive** — Linux 必改；否则探测成功也因写图失败。
4. **必须三频** — GPS 要 L1+L2+L5；BDS 要 B1/B2/B3 映射列；双频站全程 `continue` 静默空结果。
5. **`{PRN}cycleslip.txt` 是注入不是输出** — 缺文件即崩；空表=不注入；勿当成「探测结果日志」。
6. **OBS TYPES 续行不读** — 类型落在第二行（如部分 R3.05/R4）则 C5/L5 未映射，浮点切片错乱。
7. **历元号=文件全局计数** — 与卫星可见弧无关；注入 `200` 而该 PRN 从 602 才出现 → 该跳永不触发（BAKO G24 实况）。
8. **裸 `except:`** — `setvalue` 失败静默跳过；缺测被当成「无此历元」。
9. **不写回 RINEX** — 与 [cycle-slip-correction](./cycle-slip-correction.md) 一样，下游仍读原文件则「修复」未落地。
10. **shebang 拼写** — `find_cycleslip.py` 首行 `#!usr/bin/env pyhton`；用 `python find_cycleslip.py`。
11. **上游样例 OBS 缺失** — `jfng0760.13o` 不在仓；CDDIS 匿名拉易得 HTML（本机 10 KB 伪 gz）；改用公开三频 R3。
12. **与 CSC / Anubis 标志不可混用** — 三频组合整数解 ≠ rTEC 四阶峰 ≠ LLI/MW；流水线须统一定义。

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 三频组合搜索 / 注入验证教学 | **本手册 DRCycleSlip** |
| 双频 rTEC 周跳试验 CLI（出 PDF） | [cycle-slip-correction](./cycle-slip-correction.md) |
| 读 RINEX / 探三频列 | [georinex](./georinex.md) |
| 生产 QC（完好率/MP/CSR） | [anubis](./anubis.md) |
| 改版/拼接 | [gfzrnx](./gfzrnx.md) |
| 定位引擎内周跳 | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) |

**对照 cycle-slip-correction：** 彼=EMBRACE **双频 rTEC** + georinex + 目录批处理；此=**三频几何无关组合** + 自写 R3 解析 + **先注入再探测**。二者都**不写回 OBS**；生产请 Anubis。
