# gnsspy · Python GNSS 读写/分析操作手册

目录：[`PROJECTS.json` → `gnsspy`](../../PROJECTS.json) · 上游 <https://github.com/GNSSpy-Project/gnsspy> · 许可 **MIT** · 本机验证 **3.0.1**（`pip`/`git` tip `e6879bf`，2026-09-24 04:37 EDT）· **PyPI 无发行**（`pip install gnsspy` → No matching distribution）

> 岗位：RINEX OBS/NAV + SP3/CLK/IONEX → **pandas**；RINEX 2↔3 转换；可选 CDDIS 下载 / 可视化 / BRDC–SP3 比对。冲突时：**上游 README / `python -m gnsspy.io.rinex.converter -h` > 本文**。对照读库 → [georinex](./georinex.md)。

## 1. 用途与边界

**做：**

- `read_obsFile` / `read_navFile` / `read_sp3File` / `read_clockFile` / `read_ionFile`（及 `read_*_file` 别名）
- 非交互 RINEX 2↔3：`python -m gnsspy.io.rinex.converter`
- 交互菜单：`gnsspy`（下载 / 可视化 / 轨道比对 / 转换）
- Hatanaka：捆 `CRX2RNX`；`gnsspy.io.manipulate.crx2rnx`
- 大气/SPP/多路径等命名空间（`atmosphere` / `positioning` / `quality`）— 深度不及专用引擎

**不做：**

- **不是** 生产级 RINEX→xarray / NetCDF 切片主力 → [georinex](./georinex.md)
- **不是** 校准 TEC → [pytecgg](./pytecgg.md)；粗相对 TEC → [gnss-tec](./gnss-tec.md)
- **不是** 发表级 PPP-AR → [pride-pppar](./pride-pppar.md)；工业 CLI → [rtklib](./rtklib.md)
- **不是** QC 报表 → [anubis](./anubis.md)；拼日/抽稀 → [gfzrnx](./gfzrnx.md)
- 官方交互下载需 **NASA Earthdata**；本页未跑下载登录

一句话：gnsspy = **pandas 取向的 GNSS I/O + 转换/教学流水线**；大规模读切片优先 georinex。

| 术语 | 含义 |
| --- | --- |
| `Observation` | `read_obsFile` 返回；`.observation` 为 MultiIndex DataFrame（`Epoch`,`SV`） |
| `Navigation` | `read_navFile` 返回；`.navigation` 为星历 DataFrame |
| `gnsspy-convert-rinex` | **交互**转换入口（无 `-h` 非交互路径） |
| `python -m gnsspy.io.rinex.converter` | **非交互**转换（本手册主力） |
| extras `products`/`workflows` | 可选装；会拉上 **georinex** 等 |

## 2. 安装

Python **≥3.10**。无 PyPI wheel，从 GitHub 装。

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
# 核 + 产品组（含 georinex，便于对照）
python -m pip install "gnsspy[products] @ git+https://github.com/GNSSpy-Project/gnsspy.git"
# 或 clone 可编辑：
# git clone --depth 1 https://github.com/GNSSpy-Project/gnsspy.git && cd gnsspy
# python -m pip install -e ".[products]"
python -c "import gnsspy; print(gnsspy.__version__, gnsspy.__file__)"
python -m gnsspy.io.rinex.converter -h
which gnsspy gnsspy-download gnsspy-visualize gnsspy-convert-rinex
```

本机期望：`3.0.1`；`-h` 见 §5；四个入口脚本均在 `PATH`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No matching distribution` for `gnsspy` | **不在 PyPI** | 用上文 `git+https://...` / `pip install -e` |
| `Requires-Python >=3.10` | 解释器过旧 | 换 3.10+ |
| macOS 无 `CRX2RNX` | 捆二进制偏 Linux/Win | 自装 CRX2RNX 进 `PATH`，或先 [hatanaka](./hatanaka.md)/[rnxcmp](./rnxcmp.md) |
| 可 import、无 `gnsspy` 命令 | 错 venv | `which python`；重新 `source .venv/bin/activate` |

## 3. 端到端：读样本 OBS + 2→3 转换（本机真跑）

样本与 [georinex](./georinex.md) 相同：上游 `demo.10o`（RINEX 2.11 mixed，2 历元）。

```bash
mkdir -p data out
curl -fsSL -o data/demo.10o \
  https://raw.githubusercontent.com/geospace-code/georinex/main/src/georinex/tests/data/demo.10o
head -n 1 data/demo.10o
# 期望：首行含 RINEX VERSION / TYPE；绝不是 <!DOCTYPE html
```

### 3.1 `read_obsFile` → pandas

```bash
python - <<'PY'
from gnsspy.io.rinex.observation import read_obsFile
obs = read_obsFile("data/demo.10o")
df = obs.observation
print(obs.version, obs.interval, obs.approx_position)
print(df.index.names, df.shape, list(df.columns))
print("epochs", df.index.get_level_values(0).nunique(),
      "svs", df.index.get_level_values(1).nunique())
r = df.xs("G07", level="SV").iloc[0]
print("G07 L1", float(r["L1"]))
print("G07 C1", float(r["C1"]))
PY
```

**真实输出（本机 3.0.1，节选）：**

```text
Observation file  data/demo.10o  is read in 0.00 seconds.
2.11 30 [4789028.4701, 176610.0133, 4195017.031]
['Epoch', 'SV'] (22, 9) ['L1', 'L2', 'P1', 'P2', 'C1', 'S1', 'S2', 'epoch', 'SYSTEM']
epochs 2 svs 14
G07 L1 118767195.326
G07 C1 22227666.76
```

| 字段 | 含义 |
| --- | --- |
| 首行 `Observation file … is read in …` | 读入横幅（副作用打印，非返回值） |
| `version` / `interval` | `2.11` / `30`（秒） |
| `approx_position` | 头 `APPROX POSITION XYZ` |
| `observation` | MultiIndex 长表；本文件 **22 行 = 2 历元 × 有观测的星**（非满笛卡尔积） |
| `observation_types`（v2） | 含计数串，如 `['7','L1',…,'S2']` |

同文件 georinex：`L1 G07 t0 = 118767195.326`，`C1 = 22227666.76`（**与 gnsspy 数值一致**）；结构为 xarray `(time:2, sv:14)`，见 [georinex](./georinex.md)。

### 3.2 非交互 RINEX 2 → 3.04

```bash
python -m gnsspy.io.rinex.converter data/demo.10o out/demo_r3.rnx --target 3.04
head -n 16 out/demo_r3.rnx
```

**真实 stdout：**

```text
OK: data/demo.10o -> out/demo_r3.rnx
```

头节选（本机）：`3.04` / `M: MIXED`；`G 7 L1W L2W C1W C2W C1C S1W S2W`；`INTERVAL 30.000`。再 `read_obsFile("out/demo_r3.rnx")` → `version 3.04`，列变为 `C1C/C1W/L1W/…`，shape `(22, 13)`。

**注意：** 本 `demo.10o` 头里 XYZ 列宽非标准；转换后本机曾见  
`APPROX POSITION XYZ` → `4789028.4700  0.0000  0.0000`（Y/Z 丢失）。`mini` 类标准 14.4 头则 XYZ 保持。转换后务必核对近似坐标。

### 3.3 对照：同一文件 + georinex 探活

```bash
python -m georinex.time data/demo.10o
```

```text
filename: start, stop, number of times, interval
demo.10o: 2010-03-05T00:00:00 2010-03-05T00:00:30 2 30.0
['2010-03-05T00:00:00.000' '2010-03-05T00:00:30.000']
```

| | **gnsspy 3.0.1** | **georinex 1.16.2** |
| --- | --- | --- |
| 返回 | `Observation` + **pandas** MultiIndex | **xarray.Dataset** `(time,sv)` |
| 过滤/写 NetCDF | 自写 pandas | CLI `-u/-m/-o` 成熟 |
| RINEX 2↔3 写出 | **有**（converter） | **无**（只读为主） |
| `.gz` 直读 OBS | **否**（见坑） | **是**（常见） |
| 依赖取向 | pandas / 交互工作流 | xarray / 科研切片 |

## 4. I/O 速查

| 方向 | 路径 | 说明 |
| --- | --- | --- |
| 入 | `.o` / `.rnx` / `.*n` 等**已解压**文本 | `read_obsFile` / `read_navFile` |
| 入 | `.gz` / `.Z` OBS | **转换器**可吃 `.gz`/`.Z`；**读函数**要求先解压 |
| 入 | `.crx` / `.d` | 先 `crx2rnx` / [hatanaka](./hatanaka.md) |
| 出 | converter `--target 3.04` / `2.11` | 写新 OBS；`--keep` 仅影响写 v2 时保留系统 |
| 出 | 可视化 HTML | 交互 `gnsspy-visualize` → `<out>/analyses/` |
| 出 | 轨道比对 xlsx/png | 交互菜单 3/4；需产品文件 / Earthdata |

NAV 冒烟（georinex 测试 `14601736.18n`）：`read_navFile` → `Navigation.version='2.11'`，`.navigation` shape `(7, 33)`（本机）。

## 5. 参数与入口

```text
python -m gnsspy.io.rinex.converter [-h] [--target TARGET] [--keep KEEP] input output
```

| 参数 | 本机含义 |
| --- | --- |
| `input` / `output` | 源 / 目标 OBS 路径 |
| `--target` | 如 `2.11` / `3.04`；省略则取「对面」主版本 |
| `--keep` | 写 RINEX 2 时保留系统，默认 `GR`；可 `GRES` / `GRECJIS` |

入口脚本：`gnsspy`（菜单 1–6）、`gnsspy-download`、`gnsspy-visualize`、`gnsspy-convert-rinex`（后三者偏交互；**不要**对 `gnsspy-convert-rinex` 指望 argparse `-h`）。

可选 extras：`.[visualization]` / `.[products]` / `.[workflows]` / `.[all]`（见 `pyproject.toml`）。

## 6. 接到哪一步

```text
data-access / 可选 fast·gdds 下载
        ↓
  [.crx → hatanaka/rnxcmp/crx2rnx]
        ↓
  需要 2↔3 规范化？ → gnsspy converter
        ↓
  科研切片 / NetCDF / 时间探活？ → georinex   ← 默认读路径
  教学 pandas / SNR·天空图 / BRDC–SP3？ → gnsspy API/菜单
        ↓
  TEC → gnss-tec / pytecgg；定位 → rtklib / pride-pppar / cssrlib
```

路径 A（一日 TEC）：下载 →（可选 gnsspy 转换）→ **georinex 探活** → pytecgg。不要把 gnsspy SPP/插值残差当 STEC 产品。

## 7. 坑（≥8）

1. **`pip install gnsspy` 失败**：包不在 PyPI；必须 git URL / 本地 editable。
2. **`read_obsFile("….Z")`**：`ValueError: All I/O functions take uncompressed files…`（文案仍写 Next release）。
3. **`read_obsFile("….gz")`**：扩展名未拦 `.gz` 时可能直接 `IndexError`；先 `gzip -d` 或只交给 **converter**。
4. **`gnsspy-convert-rinex` 无非交互 `-h`**：会进交互菜单；脚本化用 `python -m gnsspy.io.rinex.converter`。
5. **转换后 XYZ 可能被写烂**：非标准列宽头（如本 `demo.10o`）→ Y/Z=0；转换后重读 `approx_position`。
6. **`obs.epoch` 只是 `datetime.date`**：完整时间在 MultiIndex `Epoch` 层，不要当历元列表。
7. **v2 `observation_types[0]` 是计数 `'7'`**：不是观测量名；过滤列用 `L1`/`C1` 等。
8. **Hatanaka**：converter **拒绝** `.crx/.d`；先 `CRX2RNX` / `crx2rnx()` / [hatanaka](./hatanaka.md)。
9. **CDDIS 下载 / 轨道比对**：要 Earthdata；`credentials.txt` 勿提交 git。
10. **`[products]`/`[workflows]` 依赖 georinex**：装了不等于读路径变成 xarray；两套 API 并存，别混返回类型。
11. **写 RINEX 2 `--keep` 默认 `GR`**：BDS/QZSS/IRNSS 会被丢掉；需要时显式 `GRECJIS`（仍受 R2 体系限制）。
12. **轨道比对范围**：菜单工作流当前主比 GPS/Galileo/BDS；别默认「全星座 SP3 已覆盖」。

## 8. 选型

| 你要… | 选 |
| --- | --- |
| RINEX → xarray / NetCDF / CLI 探活 | **[georinex](./georinex.md)** |
| RINEX → pandas + 2↔3 转换 + 教学图 | **gnsspy（本页）** |
| 轻量观测→自写 WLS | [laika](./laika.md) |
| NavData / 教学 WLS / Android | [gnss_lib_py](./gnss_lib_py.md) |
| 仅 Hatanaka | [hatanaka](./hatanaka.md) / [rnxcmp](./rnxcmp.md) |
| 校准 TEC | [pytecgg](./pytecgg.md) |

---

相关：[georinex](./georinex.md) · [hatanaka](./hatanaka.md) · [data-access](../data-access.md) · [`PROJECTS.json`](../../PROJECTS.json)
