# gnss-tec · RINEX → 斜路径 TEC 操作手册

目录：[`PROJECTS.json` → `gnss-tec`](../../PROJECTS.json) · 上游 <https://github.com/gnss-lab/gnss-tec> · PyPI **`gnss-tec`** · MIT · SIMuRG / gnss-lab · 本机验证 **1.1.1** + georinex 样例 `14601736.18o` 实跑 · **质检复跑**（2026-09-26 01:30 EDT，新 venv Python 3.13.5；PyPI 最新仍 **1.1.1**，`requires_dist` 仅 test extra；上游 tip `3a12cf2` 2019-05-18）：§3.2 脚本从本页原样抽出跑，12 行 stdout + `total_tec_objects=23 with_phase=15 with_prange=12` **逐字一致**，stderr 为 slot 7–11 的 `UserWarning`；坑 1（`Unknown RINEX version: 4.02`）、4（type N）、7（E07 `phase[2]=0.0`）、8、12 复现。改 2 处：坑 5 的 `TecError` 只在**直接构造** `Tec(..., 'R07')` 不给频点号时抛，走 `rnx()` 时 `glo={}` 只告警并跳过 R 星（即坑 3）；坑 8 喂 HTML 报的是 `rnx: Unknown file type`（NAV 才是 `Not an observation file`）

> 岗位：从 RINEX **载波 + 伪距**重建**斜路径 TEC**（phase / pseudorange）。库 API，无独立 CLI。冲突时：**本机 `import gnss_tec` / 上游 README > 本文**。

## 1. 用途与边界

**做：**

- RINEX OBS **2.0–2.12** 与 **3.0–3.03** → 逐星历元 `Tec` 对象
- `phase_tec`（相位几何无关）与 `p_range_tec`（伪距几何无关），单位 TECU
- GPS / GLO / GAL / BDS / QZSS / SBAS / IRNSS（频点表见 `FREQUENCY`）；GLO 需导航文件给频点号

**不做：**

- **不是** DCB/弧段整平后的**校准绝对** sTEC/vTEC → [pytecgg](./pytecgg.md)（作者 viventriglia）
- **不是** ROTI / ΔTEC / AATR → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)
- **不是** 只读盘探活 → [georinex](./georinex.md)；**不是** IONEX GIM → [ionex-gim](./ionex-gim.md)
- **不支持 RINEX 4.x**（本机对 `4.02` 直接 `Unknown RINEX version`）
- 不产出穿刺点 IPP、映射 vTEC、DCB 产品

一句话：gnss-tec = **轻量相对/几何无关斜 TEC 迭代器**；要发表级校准绝对 TEC 用 PyTECGg。

| 术语 | 含义 |
| --- | --- |
| `phase_tec` | 双频相位 GF → TECU；缺任一频点则为 `None` |
| `p_range_tec` | 双频伪距 GF → TECU；噪声大、可估绝对量级 |
| `glo_freq_nums` | GLONASS 槽位→频点号（来自 `.g` / 混合 NAV） |
| `BAND_PRIORITY` | 各系统优先频对，如 GPS `(1,2)` 再 `(1,5)` |
| `validity` | 位标志：相位/伪距/LLI 是否可用 |

## 2. 安装

```bash
cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install gnss-tec
python -c "import gnss_tec; print(gnss_tec.__version__, gnss_tec.__file__)"
# 期望：1.1.1 .../site-packages/gnss_tec/...
```

零第三方运行时依赖（纯标准库 + 包内）。源码：`pip install -e git+https://github.com/gnss-lab/gnss-tec.git#egg=gnss-tec`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` | 极旧 pip/Python | `pip install -U pip`；用 3.8+ |
| `Unknown RINEX version: 4.xx` | 只认到 3.03 | 先降到 3.xx：`gfzrnx` 或换文件（见坑） |
| import 成功但无样例 | 包不附带大 OBS | 自备 RINEX 或按下节 curl |

## 3. 端到端：短 OBS → phase_tec / p_range_tec（本机真跑）

样本：georinex 测试文件（RINEX **2.11** Mixed，约 30 s / 3 历元）。**弧段极短，数值仅验证管线，不作日变化分析。**

### 3.1 取数

```bash
mkdir -p ~/iono_ops/data && cd ~/iono_ops/data
curl -fsSL -o 14601736.18o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18o
# 可选：同站 GPS NAV（探活用；**不能**喂给 collect_freq_nums——type N 不支持）
# curl -fsSL -o 14601736.18n \
#   https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/14601736.18n
head -n 3 14601736.18o
# 期望：RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
```

### 3.2 完整脚本与参数

```bash
cd ~/iono_ops/data
python - <<'PY'
from gnss_tec import rnx
from gnss_tec.glo import collect_freq_nums

# GLO：须 .yyG 或混合 NAV（含 R）；GPS-only .yyN 会 NavMessageFileError: type N unsupported
# glo = collect_freq_nums('14601736.18g')
glo = {}

n = n_phase = n_pr = 0
with open('14601736.18o') as obs_file:
    for tec in rnx(obs_file, glo_freq_nums=glo):
        n += 1
        pt, pr = tec.phase_tec, tec.p_range_tec
        if pt is not None:
            n_phase += 1
        if pr is not None:
            n_pr += 1
        if n <= 12:
            print(f"{tec.timestamp} {tec.satellite}: "
                  f"phase_tec={pt} p_range_tec={pr} "
                  f"phase_code={tec.phase_code} p_range_code={tec.p_range_code}")
print(f"total_tec_objects={n} with_phase={n_phase} with_prange={n_pr}")
PY
```

| 参数 | 作用 |
| --- | --- |
| `obs_file` | 已打开的文本 OBS（`rnx` 会先 `next` 读版本行） |
| `glo_freq_nums` | `collect_freq_nums(glo_nav)`；要 **GLO/混合** NAV，不是 GPS `.yyN`；缺则告警并跳过 R 星 |
| `band_priority` | 默认 `BAND_PRIORITY`；改频对时传入自定义 dict |

**本机截断 stdout（gnss-tec 1.1.1，2026-09-24 ET；stderr 另见 GLO 警告）：**

```text
.../gnss_tec/rinex.py:331: UserWarning: Can't find slot 7 in the glo_freq_nums dict.
  warnings.warn(str(err))
（同理 slot 8–11；有 R 星且 glo={} 时出现，可忽略或补 GLO NAV）
2018-06-22 06:17:30 E07: phase_tec=None p_range_tec=None phase_code={1: 'L1', 2: 'L8'} p_range_code={1: 'C1', 2: 'C8'}
2018-06-22 06:17:30 E19: phase_tec=None p_range_tec=None phase_code={1: 'L1', 2: 'L8'} p_range_code={1: 'C1', 2: 'C8'}
2018-06-22 06:17:30 G03: phase_tec=3.2993148613398913 p_range_tec=24.755677912400678 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:30 G07: phase_tec=-21.21545247449915 p_range_tec=1.2277902603563675 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:30 G09: phase_tec=-2.227435204140415 p_range_tec=26.097681238372537 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:30 G23: phase_tec=11.835532364343285 p_range_tec=None phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:30 G30: phase_tec=64.67108634940517 p_range_tec=21.300733227106164 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:45 E07: phase_tec=None p_range_tec=None phase_code={1: 'L1', 2: 'L8'} p_range_code={1: 'C1', 2: 'C8'}
2018-06-22 06:17:45 E19: phase_tec=None p_range_tec=None phase_code={1: 'L1', 2: 'L8'} p_range_code={1: 'C1', 2: 'C8'}
2018-06-22 06:17:45 G03: phase_tec=3.1958065072429647 p_range_tec=37.14779351066705 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:45 G07: phase_tec=-21.36236842813084 p_range_tec=3.9784211119348014 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
2018-06-22 06:17:45 G09: phase_tec=-2.2415321354618234 p_range_tec=26.354660582822802 phase_code={1: 'L1', 2: 'L2'} p_range_code={1: 'C1', 2: 'C2'}
total_tec_objects=23 with_phase=15 with_prange=12
```

### 3.3 输出字段

| 字段 | 含义 | 误用 |
| --- | --- | --- |
| `timestamp` / `satellite` | 历元、星号（`G03`） | — |
| `phase_tec` | 相位 GF TECU；相对、含模糊度跳 | **当绝对 VTEC 发表** |
| `p_range_tec` | 伪距 GF TECU；含 DCB/多路径 | 与 GIM 像素硬比而不做偏差处理 |
| `phase_code` / `p_range_code` | 实际选用的观测类型 | 忽略频对导致跨文献不可比 |
| `None` | 该频点值为 0 / 未读到双频 | 当成“TEC=0” |
| GLO `UserWarning` | 槽位不在 `glo_freq_nums` | 强行算 GLO 而不补 NAV |

公式要点（库内）：`factor(f1,f2)=(1/40.308)·(f1²f2²)/(f1²−f2²)·1e−16`，相位用 `c·(φ1/f1−φ2/f2)`。**无 DCB、无弧段 leveling、无 IPP。**

### 3.4 接到下游

- 路径 A 一日 TEC：本页粗相对 TEC → [pytecgg](./pytecgg.md) 校准 → [ionex-gim](./ionex-gim.md) 对照；教程 [02](../tutorials/02-gnss-dualfreq-tec.md) / [09](../tutorials/09-dcb-biases-deep.md) / [16](../tutorials/16-practice-one-day-tec.md)
- 数据入口：[data-access](../data-access.md)；读盘探活 [georinex](./georinex.md)；QC [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)
- 扰动指数：把 leveled 序列交给 [oasis-roti](./oasis-roti.md)（本库不产 ROTI）

## 4. 输入 / 输出速查

| 输入 | 要求 |
| --- | --- |
| RINEX OBS 2.x / 3.0–3.03 | 文本；双频相位或伪距 |
| GLO / 混合 NAV（可选） | `collect_freq_nums`；**不要**喂 GPS-only `.yyN`（type N） |
| RINEX 4 | **不支持** → 先转 3.xx |

| 输出 | 下游 |
| --- | --- |
| 迭代 `Tec`（TECU） | 自写 CSV/绘图；再交 PyTECGg/OASIS |
| 无文件产物 | 需自行落盘 |

**明确不输出：** `veq`、DCB parquet、IONEX、ROTI、IPP。

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 A 粗 TEC 冒烟 | §3 | [pytecgg](./pytecgg.md) · [02](../tutorials/02-gnss-dualfreq-tec.md) |
| 批站网相对 STEC | §3 | 自写循环；DCB→[09](../tutorials/09-dcb-biases-deep.md) |
| RINEX 4 / 清洗 | — | [gfzrnx](./gfzrnx.md) 再回本页 |
| GIM 对比 | — | [ionex-gim](./ionex-gim.md) · [18](../tutorials/18-lab-compare-gims.md) |

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `Unknown RINEX version: 4.02` | 版本表只到 3.03 | `gfzrnx` 转 RINEX 3 后再跑 |
| 2 | `phase_tec is None` | 第二频相位为 0 / 未读到 | `print(tec.phase, tec.phase_code)`；换双频站或改 `BAND_PRIORITY` |
| 3 | GLO `Can't find slot N` | 未传频点号 | `glo=collect_freq_nums('site.yyg'); rnx(f, glo_freq_nums=glo)` |
| 4 | `NavMessageFileError: type N is unsupported` | 把 GPS `.yyN` 喂给 `collect_freq_nums` | 换 `.yyG` / 混合 NAV（含 R 星历） |
| 5 | `TecError: GLO frequency number must be provided to compute TEC values.` | 绕过 `rnx()` **直接构造** `Tec(ts, 'GPS', 'R07')` 且不给 `glo_freq_num`（经 `rnx()` 时只告警跳过，见坑 3） | 给第 4 个参数频点号，或走 `rnx(f, glo_freq_nums=collect_freq_nums(...))` |
| 6 | 把 `phase_tec` 当绝对 TEC | 无 DCB/leveling | 转 [pytecgg](./pytecgg.md) `calculate_tec` |
| 7 | Galileo `None` 而 GPS 有值 | 选中的 Lx 列空（本样 E07 `phase[2]==0`） | 查 OBS 该星双频是否非空；或调频对优先级 |
| 8 | `rnx: Not an observation file` / `rnx: Unknown file type` | 前者喂了 NAV，后者喂了 HTML 等非 RINEX | `head` 确认 `OBSERVATION DATA` |
| 9 | 伪距 TEC 跳几十 TECU | 多路径/DCB，属预期 | 相位做相对；绝对走校准链 |
| 10 | EOF 时 `RuntimeError: generator raised StopIteration` | 旧迭代器 + 新 Python 边界 | 用 `for tec in rnx(f):`；升级到 ≥1.1.1（已修 PEP-479） |
| 11 | 与 PyTECGg 数值差巨大 | 定义不同（相对 GF vs 校准） | **只比形态**；笔记写清产品 |
| 12 | 空文件 `rnx: Empty input file` | 0 字节 / 下成登录页 | 重下；`wc -c` / `head` |
| 13 | 1 Hz 全日内存涨 | 全进 list | 流式写 CSV：`for tec in rnx(f): ...` |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 轻量 Python 相对 STEC | **gnss-tec** |
| 校准 sTEC/vTEC / bias | **PyTECGg** |
| ROTI / ΔTEC | **OASIS** / **IonoMoni** |
| 读 RINEX→xarray | **georinex** |
| 读 IONEX GIM | [ionex-gim](./ionex-gim.md) |

## 8. 相关

[pytecgg](./pytecgg.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [ionex-gim](./ionex-gim.md) · [cssrlib](./cssrlib.md) · [README](./README.md)
