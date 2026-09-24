# cycle-slip-correction · 周跳探测改正 CLI 操作手册

目录：[`PROJECTS.json` → `cycle-slip-correction`](../../PROJECTS.json) · 上游 <https://github.com/embrace-inpe/cycle-slip-correction> · **无 PyPI 包**（`setup.py` 名 `cycleslip` 未发布）· MIT · EMBRACE/INPE · 本机验证 tip **`c465dd4`**（2019-04-26）+ 现代依赖 + BAKO RINEX **3.03** 40 历元实跑

> 岗位：对 **RINEX 3.01–3.03** 观测做 **相对 TEC（rTEC）四阶差分** 周跳探测，并在内存里尝试改正相位；常用于低纬活跃区前处理试验。**不是**定位引擎内置周跳策略，**也不写回改正后的 RINEX**（`-rinex_output` 已注释）。冲突时：**本机 `python main.py -h` / 上游 README > 本文**。

## 1. 用途与边界

**做：**

- 读目录内 RINEX OBS（经 **georinex**）→ 逐 PRN 算 rTEC / Melbourne–Wübbena 类组合
- 四阶差分 + `find_peaks` 标不连续点；匹配索引后改正 L1/L2（内存）
- 默认星座 **`G`/`R`**（`settings.CONSTELLATIONS`）；出 **`{PRN}_corrected.pdf`**（及 `plot_it=True` 时的检测图）
- 面向 EMBRACE 低纬 TEC 流水线的前处理试验

**不做：**

- **不**支持 RINEX **2.x**（本机对 `2.11` 直接跳过）/ **3.05+** / **4.x**（列名表无键或 georinex 拒读）
- **不**写改正 RINEX、不产出 QC 报告 → [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md) / [pinot](./pinot.md)
- **不是**校准绝对 sTEC/vTEC → [pytecgg](./pytecgg.md)；粗相对斜 TEC → [gnss-tec](./gnss-tec.md)
- **不是** ROTI/ΔTEC → [oasis-roti](./oasis-roti.md)；**不是** RTK/PPP 引擎周跳 → [rtklib](./rtklib.md)
- 不处理 Galileo/BDS/QZSS（除非你改 `CONSTELLATIONS` 与 `COLUMNS_IN_RINEX`）

一句话：EMBRACE **周跳探测/改正试验 CLI**；接到 TEC 链前先确认标志含义与引擎策略是否一致。

| 术语 | 含义 |
| --- | --- |
| rTEC | 相位几何无关相对 TEC（米级组合，非校准 TECU 产品） |
| 4th der | rTEC 四阶差分；超 `LIMIT_STD×σ` 标峰 |
| `DIFF_TEC_MAX` | 码-相一致性门限（默认 `0.05`） |
| `COLUMNS_IN_RINEX` | 按版本映射 L1/L2/C1/P2 观测码（3.01/3.02/3.03） |
| `plot_it` | 是否另存检测图 `{PRN}.pdf`；**改正对比图始终写** |

## 2. 安装

**无 PyPI。** 上游 README 写 `pip install -r requirements.txt`，仓内实际文件名是拼写错误的 **`requeriments.txt`**；官方钉死在 2019（`numpy==1.16.2` / `georinex==1.10.0` / `matplotlib==3.0.3`…），**在 Python 3.13 上会构建失败**（本机 `matplotlib` wheel 构建：`SafeConfigParser`）。

```bash
cd ~/iono_ops
git clone https://github.com/embrace-inpe/cycle-slip-correction.git
cd cycle-slip-correction
git rev-parse --short HEAD   # 期望：c465dd4
python3 -m venv ~/iono_ops/csc_venv && source ~/iono_ops/csc_venv/bin/activate
python -m pip install -U pip

# 官方钉（Py3.13 本机失败，仅作对照）
# pip install -r requeriments.txt

# 可工作钉（本机 2026-09-24 ET 实装）：
python -m pip install 'numpy>=1.26' 'pandas>=2.0' 'scipy>=1.11' \
  'matplotlib>=3.8' 'xarray>=2023.1' 'georinex>=1.16' 'dateparser>=1.1'
python - <<'PY'
import numpy,pandas,scipy,matplotlib,xarray,georinex,dateparser
print(numpy.__version__, pandas.__version__, scipy.__version__,
      matplotlib.__version__, xarray.__version__,
      georinex.__version__, dateparser.__version__)
PY
# 期望示例：2.5.3 3.0.6 1.18.1 3.11.2 2026.7.0 1.16.2 1.4.3
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No such file: requirements.txt` | 文件名拼写 | 用 **`requeriments.txt`** 或上面可工作钉 |
| `SafeConfigParser` / 旧 pin 构建失败 | 2019 pin × 新 Python | 用可工作钉；勿臆造已装成功 |
| `ModuleNotFoundError: georinex` | 未装依赖 | `pip install georinex dateparser matplotlib scipy pandas` |
| `pip install cycleslip` 404 | **未发布 PyPI** | 只 clone + `python main.py` |
| `setup.py` 的 `scripts=['cycle_slip']` | 仓内无该可执行文件 | **忽略 setup**；入口是 `main.py` |

## 3. 端到端：RINEX 3.03 短切片 → 探测日志 + PDF（本机真跑）

样本：PRIDE 例程站 **BAKO** 全日 OBS 截断前 **40 历元**（约 20 min @ 30 s，RINEX **3.03**）。完整日文件亦可，但 PDF 会按 PRN 暴增。

### 3.1 取数与 settings 补丁

默认 `REQUIRED_VERSION = 3.01` 会让 `which_cols_to_load()` 按 **3.01 短名**选列；分析阶段又用 **头文件 version** 取 `COLUMNS_IN_RINEX`。对 **3.03** 文件请把两者对齐，并建议先关检测大图、只跑 GPS：

```bash
# 自备 3.03 OBS，或从已有 PRIDE 例程截断（文件名须过 setup_rinex_name）
mkdir -p ~/iono_ops/csc_rinx ~/iono_ops/csc_run
# 例：BAKO00IDN_R_20212200000_01D_30S_MO.rnx → 放入 csc_rinx/
# 长名 .rnx：年=字符[12:16]，DOY=[16:19]；短名 .YYo：四字母站+[4:7] DOY

cd ~/iono_ops/cycle-slip-correction
# 备份后改 settings.py（本机实跑补丁）：
#   plot_it = False
#   REQUIRED_VERSION = 3.03
#   CONSTELLATIONS = ['G']
```

### 3.2 命令

```bash
source ~/iono_ops/csc_venv/bin/activate
cd ~/iono_ops/csc_run          # PDF / cycle_slip.log 落在 cwd
python ~/iono_ops/cycle-slip-correction/main.py -h
# 期望：usage… -rinex_folder … -verbose …

python ~/iono_ops/cycle-slip-correction/main.py \
  -rinex_folder ~/iono_ops/csc_rinx -verbose True
```

**本机截断 stdout（tip `c465dd4` + georinex 1.16.2，2026-09-24 ET）：**

```text
[2026.09.24 08:20:53] {cycle_slip.py  :411 } INFO : >> Found 1 file(s)
[2026.09.24 08:20:53] {cycle_slip.py  :419 } INFO : >>>> Reading rinex: BAKO00IDN_R_20212200000_01D_30S_MO.rnx
[2026.09.24 08:20:53] {cycle_slip.py  :311 } INFO : >>>> Detecting peaks on the 4th order final differences in rTEC...
[2026.09.24 08:20:53] {cycle_slip.py  :215 } INFO : >>>>>> No discontinuities detected (by final differences) for PRN G02
[2026.09.24 08:20:53] {cycle_slip.py  :314 } INFO : >>>> Finding discontinuities and correcting cycle-slips (PRN G02)...
……（G03/G06/G07/G09/G14/G17/G19/G30 同结构）……
[2026.09.24 08:20:54] {cycle_slip.py  :435 } INFO : >> File BAKO00IDN_R_20212200000_01D_30S_MO.rnx checked! Time: 14721.6372 minutes
[2026.09.24 08:20:54] {cycle_slip.py  :438 } INFO : >> Processing done for 1 files in -14721.6372 minutes
```

cwd 产物：`G02_corrected.pdf` … `G30_corrected.pdf`、`cycle_slip.log`。短弧无周跳时日志为 **No discontinuities**；有跳时类似上游示例 `Discontinuities detected in [ … ]` / `Indexes match (…): correcting…`。

**计时数字不可信：** `start=time.perf_counter()` 与 `stop=time.process_time()` 混用，会出现上万分钟或负值——以墙钟为准。

## 4. I/O

| | 说明 |
| --- | --- |
| **输入** | 目录内全部文件；每个须通过 `setup_rinex_name`（四字母站名 + 合法 DOY + `.YYo` 或长名 `.rnx`） |
| **OBS 版本** | 头 `version >= REQUIRED_VERSION`（默认 3.01）；列名键仅 **`3.01`/`3.02`/`3.03`** |
| **观测码** | GPS 3.03 默认 `L1C/L2W/C1C/C1W/C2W`；缺码则该 PRN 序列大量 NaN，探测变「无跳」假阴性 |
| **输出 OBS** | **无**（改正只在内存；勿期望新 `.rnx`） |
| **输出图** | `{PRN}_corrected.pdf`（rTEC 原/改）；`plot_it=True` 另有 `{PRN}.pdf` |
| **日志** | stdout（`-verbose` 真值）+ 滚动 `cycle_slip.log`（cwd，5 MB×7） |

## 5. 参数与 settings

| 项 | 作用 |
| --- | --- |
| `-rinex_folder` | OBS 目录（**不是**单文件路径） |
| `-verbose` | 任意非空即开日志；**`-verbose False` 仍为真**（字符串） |
| `REQUIRED_VERSION` | 版本下限 + **`which_cols_to_load` 用的键**（常被忽略却致命） |
| `CONSTELLATIONS` | `gr.load(..., use=…)`；默认 `G`,`R` |
| `DIFF_TEC_MAX` / `LIMIT_STD` | 码相门限 / 四阶差分峰阈值倍率 |
| `plot_it` | 检测图开关；**不**关闭 `_corrected.pdf` |
| GLONASS | 头有 `GLONASS SLOT / FRQ #` 则解析头；否则 `downloads.py` 拉 IAC，且默认落盘路径硬编码 `/home/lotte/embrace/tec/glonasschannel/` |

## 6. 接到哪步

```text
[data-access] 取 RINEX 3.01–3.03
    →（可选 gfzrnx/hatanaka 解压·改版；R2→R3 另工具）
    → georinex 探活列名/星座
    → cycle-slip-correction（本手册：试验改正 / 出 PDF）
    → 再进 TEC：[gnss-tec] 粗相对 / [pytecgg] 校准
    → 或定位：[rtklib] / [pride-pppar]（引擎自带周跳，策略可能不一致）
    → QC 对照：[anubis] / [oasis-roti]
```

低纬气泡/闪烁日：先本工具或 oasis-roti 看弧段连续性，再跑 TEC；**不要**把 PDF 峰当硬件 S4。

## 7. 坑（≥8）

1. **无 PyPI / 入口是 `main.py`** — `pip install cycleslip` 404；`setup.py` scripts 指向不存在的 `cycle_slip`。
2. **`requeriments.txt` 拼写** — README 的 `requirements.txt` 不存在。
3. **2019 官方 pin 在 Py3.13 装失败** — 记录失败原因；改用 §2 可工作版本，勿假装 pin 成功。
4. **只认 3.01–3.03** — 本机 R2.11：`Rinex version 2.11. This code comprises the 3.01+…` 并 skip；R3.05：`KeyError: '3.05'`；R4.01：georinex `unknown RINEX`。
5. **`REQUIRED_VERSION` 与文件 version 不一致** — `which_cols_to_load` 死盯该常量；3.03 站请改成 `3.03`。
6. **不写回 RINEX** — `-rinex_output` 已注释；下游 TEC 仍读原文件则「改正」未生效。
7. **计时日志荒谬** — `perf_counter`−`process_time`；忽略分钟数。
8. **`-verbose False` 仍开日志** — `if args.verbose` 对非空字符串为真；关日志请省略该参数。
9. **GLONASS 下载路径** — 无头槽位表时写死 `/home/lotte/...`；无该目录即失败。优先用含 `GLONASS SLOT / FRQ #` 的 R3，或只跑 `['G']`。
10. **文件名校验严** — 非四字母站、坏 DOY、怪扩展直接 `sys.exit`；目录里杂文件会一起扫到。
11. **`_prepare_factor(hdr, year, month, doy)` 形参顺序** — 定义是 `(hdr, year, day, month)`，调用把 month/doy 对调；缺头表走下载时日期易错。
12. **与 RTKLIB/Anubis 标志不一致** — 四阶 rTEC 峰 ≠ LLI ≠ MW 检验；流水线需统一「何谓一周跳」。

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 低纬/EMBRACE 风格 rTEC 周跳试验 CLI | **本手册 cycle-slip-correction** |
| 读 RINEX 进 Python / 探列名 | [georinex](./georinex.md) |
| 生产 QC 报告（完好率/MP/CSR） | [anubis](./anubis.md) / [pinot](./pinot.md) |
| 改版/拼接/抽稀 | [gfzrnx](./gfzrnx.md) |
| ROTI / ΔTEC | [oasis-roti](./oasis-roti.md) |
| 校准 TEC 产品 | [pytecgg](./pytecgg.md) |
| 定位引擎内周跳 | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) |

**对照：** 目录另有 `DRCycleSlip`（教学脚本，本手册未覆盖）。选本工具 = 接受 **2019 仓 + 自备现代依赖 + 无 RINEX 回写**。
