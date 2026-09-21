# georinex

目录：[`PROJECTS.json` → `georinex`](../../PROJECTS.json) · 上游 <https://github.com/geospace-code/georinex> · MIT · 依赖 xarray / numpy

> 操作手册。祈使句。参数冲突时以本机 `python -m georinex.read -h` 与上游 README 为准。

---

## 用途与边界

**用：**

- 把 RINEX OBS / NAV（含常见 `.gz`、Hatanaka `.crx`）读成 **xarray.Dataset**。
- 探活：时间覆盖、卫星列表、双频观测量是否成对、采样间隔。
- 过滤后落盘 NetCDF，给下游 Python 批处理加速。
- 电离层链的「读盘第一棒」：之后再接校准 TEC、ROTI、定位。

**不用 / 边界：**

- **不做** 校准 TEC / DCB 估计 → [pytecgg](./pytecgg.md)（作者 **viventriglia**，不是本仓维护者）。
- **不做** ROTI / AATR → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)。
- **不做** RTK / PPP 坐标 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)。
- **不做** QC PDF / XTR 报表 → [anubis](./anubis.md)。
- **不做** RINEX 拼接 / 抽稀 / 重命名 → 先 [gfzrnx](./gfzrnx.md)。
- **不做** 读 IONEX GIM → [ionex-gim](./ionex-gim.md)；球谐自建边界见 [sh-gim](./sh-gim.md)（求解器未开源）。

一句话：georinex = **读与切片**，不是科学产品引擎。

---

## 安装（多平台 + 报错）

### 共同要求

- Python **≥ 3.10**（以 PyPI 当前元数据为准；升级失败时先查 `Requires-Python`）。
- 建议独立 venv；不要用系统全局 pip。
- Hatanaka：`pip install hatanaka`，或系统装 `CRX2RNX` / `RNX2CRX`。

### Linux / macOS

```bash
cd ~/work
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install "georinex" "hatanaka" "netCDF4" "xarray" "numpy"
python -c "import georinex as gr, hatanaka, xarray; print(gr.__file__)"
python -m georinex.gtime -h 2>&1 | head -n 5 || true
python -m georinex.read -h 2>&1 | head -n 20
```

### Windows（PowerShell）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install georinex hatanaka netCDF4 xarray numpy
python -c "import georinex as gr; print(gr.__file__)"
```

若执行策略拦截：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`（仅本机策略，按单位 IT 规定执行）。

### Conda（可选）

```bash
conda create -n gnss python=3.11 -y
conda activate gnss
pip install georinex hatanaka netCDF4
```

### 安装期常见报错

| 现象 | 处理 |
|---|---|
| `No matching distribution` | Python 过旧；换 3.10+ |
| `error: Microsoft Visual C++`（Windows 编 netCDF4） | 先装预编译 wheel：`pip install netCDF4`；仍失败再装 VS Build Tools，或先不装 netCDF4、只读 RINEX |
| `ModuleNotFoundError: hatanaka` | `pip install hatanaka`；或系统 PATH 放 `CRX2RNX` |
| `libnetcdf.so` / DLL 找不到 | 重装 `netCDF4` wheel；Conda 用户用 `conda install -c conda-forge netcdf4` |
| 公司代理 SSL 失败 | 配置 `pip.conf` / `HTTPS_PROXY`；不要 `--trusted-host` 乱用到不明源 |
| 可 import 但 CLI 无模块 | 确认激活的是装包的那个 venv：`which python` |

### 安装验收（必须全过）

```bash
python -c "import georinex as gr; print('ok', gr.__version__ if hasattr(gr,'__version__') else 'no-ver')"
python -m georinex.gtime --help >/dev/null 2>&1 || python -m georinex.gtime 2>&1 | head -n 3
# 用任意本地最小 OBS 再验一次真实读盘（见下节）
```

---

## 快速冒烟（5 分钟）

路径为占位符。先准备一个非空 OBS（可用 [data-access](../data-access.md) 下载）。

```bash
# 0) 文件自检：必须是 RINEX，不是 HTML 登录页
head -n 8 data/sample.obs
file data/sample.obs
# 期望：文本含 RINEX VERSION / TYPE；file 显示 ASCII/UTF-8 text 或 gzip

# 1) 只看时间（坏文件最先在这里暴露）
python -m georinex.gtime data/sample.obs
# 期望：打印起止时间与间隔；空/半截文件 → 报错或无有效历元

# 2) 读 OBS，看维与变量
python - <<'PY'
import georinex as gr
obs = gr.load("data/sample.obs")
print(obs)
print("dims:", dict(obs.sizes))
print("vars:", list(obs.data_vars)[:20])
print("sv sample:", list(obs.sv.values[:8]) if "sv" in obs.coords else "no sv")
PY
# 期望：time/sv 维 > 0；变量名随 RINEX2/3 变（L1 vs L1C）

# 3) 省内存过滤
python - <<'PY'
import georinex as gr
obs = gr.load("data/sample.obs", use="G", tlim=("2024-01-01", "2024-01-01T06:00"))
print(dict(obs.sizes))
print([v for v in obs.data_vars if v.startswith(("L","C","P","S")) ][:12])
PY
```

**冒烟失败判据：** `dims` 全 0、抛 `UnicodeDecodeError`/`ValueError`、或 `head` 看到 `<html` —— 先修数据文件，不要改 georinex。

---

## 完整工作流

### 工作流 A：一日站 OBS → NetCDF 缓存 → 交给 PyTECGg / 自写 TEC

对应教程 [02](../tutorials/02-gnss-dualfreq-tec.md)、[16](../tutorials/16-practice-one-day-tec.md)。

```bash
# A1 可选：GFZRNX 抽稀 / 拼日（大文件强烈建议）
# gfzrnx -finp data/SITE00XXX_R_*.rnx -fout data/SITE_30s.rnx -smp 30 -kv -f

# A2 时间探活
python -m georinex.gtime data/SITE_30s.rnx | tee logs/gtime_SITE.txt

# A3 只读 GPS + 双频相位/伪距，写出 nc
python - <<'PY'
import georinex as gr
from pathlib import Path
src = Path("data/SITE_30s.rnx")
out = Path("data/SITE_30s_G.nc")
obs = gr.load(
    src,
    use="G",
    meas=["L1C", "L2W", "C1C", "C2W"],  # 先 print(data_vars) 再改成你文件真实名
)
print(obs.sizes)
# 断言双频成对
need = {"L1C", "L2W"}
have = set(obs.data_vars)
missing = need - have
if missing:
    raise SystemExit(f"缺观测量 {missing}; 现有={sorted(have)[:40]}")
obs.to_netcdf(out)
print("wrote", out, out.stat().st_size)
PY

# A4 复查缓存
python - <<'PY'
import georinex as gr
obs = gr.load("data/SITE_30s_G.nc")
print(obs.sizes, list(obs.data_vars))
PY
```

**期望输出（示意）：**

```text
Dimensions: (time: 2880, sv: 12)
Data variables: L1C L2W C1C C2W
wrote data/SITE_30s_G.nc 12345678
```

下游：把**原始 RINEX**（不是 nc）交给 [pytecgg](./pytecgg.md) 做校准 TEC；nc 仅作探活/自写脚本缓存。PyTECGg 上游 = **viventriglia**。

### 工作流 B：NAV + OBS 联合探活（星历覆盖）

```bash
python - <<'PY'
import georinex as gr
nav = gr.load("data/BRDC00IGS_R_20240010000_01D_MN.rnx")
obs = gr.load("data/SITE.rnx", use="G")
print("NAV:", nav)
print("OBS time:", obs.time.values[0], "→", obs.time.values[-1])
# NAV 维名随版本变化：常见 sv / time；打印后人工确认覆盖 OBS 日
print("NAV coords:", list(nav.coords))
print("NAV data_vars sample:", list(nav.data_vars)[:15])
PY
```

**期望：** NAV 可读；OBS 日在广播星历有效窗内。覆盖不足时换当日 BRDC / 多日拼 NAV。

### 工作流 C：Hatanaka / gzip 批量探活

```bash
# C1 完整性
gunzip -t data/SITE.rnx.gz && echo gzip_ok
# 或 hatanaka 工具链：若直接 load .crx.gz 失败，先解压再转

# C2 直接读（georinex + hatanaka 正常时应可）
python -m georinex.gtime data/SITE.crx.gz

# C3 目录扫描时间覆盖
python - <<'PY'
from pathlib import Path
import georinex as gr
for p in sorted(Path("data").glob("*.rnx*"))[:20]:
    try:
        # gtime API：优先 CLI；库侧可用 gettimes（若本机版本提供）
        times = gr.gettimes(p)
        print(p.name, times[0], times[-1], len(times))
    except Exception as e:
        print("FAIL", p.name, type(e).__name__, e)
PY
```

### 工作流 D：只抽间隔（文件是 1 Hz，你只要 30 s）

优先用 [gfzrnx](./gfzrnx.md) `-smp 30` 写新文件；若坚持在读时抽稀：

```bash
python - <<'PY'
import georinex as gr
# interval 单位秒；以本机版本文档为准
obs = gr.load("data/SITE_1Hz.rnx", use="G", interval=30)
print(obs.sizes)
# 粗检间隔
import numpy as np
dt = np.diff(obs.time.values).astype("timedelta64[s]").astype(int)
print("dt unique sample:", sorted(set(dt.tolist()))[:10])
PY
```

**注意：** 读时 interval ≠ 官方抽稀工具对 LLI/头文件的处理；生产流水线用 gfzrnx。

### 工作流 E：接定位 / ROTI 前的字段核对

```bash
python - <<'PY'
import georinex as gr
obs = gr.load("data/SITE.rnx", use="G")
vars_ = list(obs.data_vars)
print(vars_)
# 双频 TEC 最低需求：两载波相位（或码）成对
phase = [v for v in vars_ if v.startswith("L")]
code  = [v for v in vars_ if v.startswith(("C","P"))]
print("phase", phase)
print("code", code)
assert len(phase) >= 2, "单频无法做几何无关 TEC"
PY
```

然后：

- 校准 TEC → [pytecgg](./pytecgg.md)
- ROTI → [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)（它们通常直接吃 RINEX，不必经 georinex）
- 坐标 → [rtklib](./rtklib.md)

---

## 输入 / 输出与字段表

### 输入

| 类型 | 扩展名 / 形态 | 备注 |
|---|---|---|
| OBS | `.obs` `.##o` `.rnx` `.rnx.gz` `.crx` `.crx.gz` | RINEX 2/3/4 |
| NAV | `.nav` `.##n` `.##p` 混合 NAV `.rnx` | 广播星历 |
| 缓存 | `.nc`（本工具写出） | 再 `gr.load` |
| 可选 | SP3（部分版本/路径） | 以本机能力为准；精密轨道主战场不在 georinex |

### 输出（OBS Dataset 常见坐标 / 维）

| 名 | 含义 | 操作注意 |
|---|---|---|
| `time` | 历元 | 默认与文件头时间系一致；对齐 IONEX/事件前先统一 GPST/UTC |
| `sv` | 卫星 ID 如 `G01` | 过滤后仍保留出现过的 sv |
| `interval`（属性/推断） | 采样 | 用 `gtime` 或 `diff(time)` 核实 |

### 输出（OBS 数据变量，示意）

| 变量模式 | 含义 | RINEX2 例 | RINEX3 例 |
|---|---|---|---|
| 载波相位 | cycles | `L1` `L2` | `L1C` `L2W` `L2X`… |
| 伪距 | meters | `C1` `P2` | `C1C` `C2W`… |
| 多普勒 | Hz | `D1` | `D1C`… |
| SNR | dB-Hz 等 | `S1` | `S1C`… |

SSI/LLI：默认常不加载；需要时用 `useindicators=True` 或 CLI `-useindicators`（以 `-h` 为准）。

### 输出（NAV）

| 内容 | 说明 |
|---|---|
| 轨道 / 钟差参数 | 按星座分字段；**先 `print(nav)`** 再取字段 |
| 不做 | 卫星 ECEF 连续轨迹（那是下游 `satellite_coordinates` 一类） |

### 明确不输出

IONEX、ROTI 序列、`.pos`、校准 `stec`/`vtec`、Anubis XTR。

---

## 常用参数

### Python `gr.load`

| 参数 | 作用 | 示例 |
|---|---|---|
| `use` | 系统过滤 | `"G"` / `"E"` / `"C"` / 集合 |
| `tlim` | 时间窗 | `("2024-01-01","2024-01-01T06:00")` 或 datetime 对 |
| `meas` | 观测量白名单 | `["L1C","L2W","C1C","C2W"]` |
| `interval` | 读时抽稀（秒） | `30` |
| `useindicators` | 载入 LLI/SSI | `True` |
| `fast` | RINEX2 快预分配 | 默认常 True；异常改 `False` |
| `verbose` | 日志 | `True` |

写出：`obs.to_netcdf("out.nc")`。读回：`gr.load("out.nc")`。

### CLI

| 命令 | 作用 |
|---|---|
| `python -m georinex.gtime FILE` | 起止与间隔 |
| `python -m georinex.read …` | 读/转/可选画图；看 `-h` 要 `-use`/`--tlim`/`--meas` |

```bash
python -m georinex.read data/sample.obs -use G --tlim 2024-01-01T00:00 2024-01-01T03:00 --meas L1C L2W -o data/out.nc
# 精确旗标以本机 -h 为准；上行为常见形态示意
```

---

## 接到 tutorials / 工作流哪一步

| 场景 | 本手册位置 | 教程 / 下游 |
|---|---|---|
| 双频 TEC 入门 | 工作流 A | [02](../tutorials/02-gnss-dualfreq-tec.md) → [pytecgg](./pytecgg.md) |
| 一日 TEC 练习 | A + 字段核对 | [16](../tutorials/16-practice-one-day-tec.md) |
| 与 GIM 对照前探活 | A3 确认双频 | [03](../tutorials/03-gim-ionex.md) · [ionex-gim](./ionex-gim.md) · [18](../tutorials/18-lab-compare-gims.md) |
| DCB / 偏差概念 | 读盘后不要自己「估绝对值」糊弄 | [09](../tutorials/09-dcb-biases-deep.md) + pytecgg |
| 闪烁 / ROTI | 仅确认高采样文件可读 | [05](../tutorials/05-scintillation-roti.md) → oasis-roti / ionomoni |
| 定位受电离层影响 | 确认 OBS 可读后换 RTKLIB | [06](../tutorials/06-iono-positioning.md) |
| 索引路径 A | data-access → **georinex** → 可选 gfzrnx/anubis → pytecgg | [software README](./README.md) |

SH-GIM：仅当讨论「自建球谐 GIM」边界时打开 [sh-gim](./sh-gim.md)；**不要**把 georinex 读盘结果指望成全球 GIM。

---

## 可操作坑（≥12）

1. **变量名照抄教程导致 KeyError**  
   先 `print(list(obs.data_vars))`。RINEX3 是 `L1C/L2W`，不是 `L1/L2`。

2. **把相对 TEC 当绝对产品**  
   georinex 只给你相位/伪距。绝对值走 [pytecgg](./pytecgg.md)（viventriglia）。

3. **1 Hz 全日进内存 OOM**  
   立刻加 `use`/`tlim`/`meas`，或 gfzrnx `-smp`。

4. **`.crx` 失败却怪 georinex**  
   `pip show hatanaka`；或先 `CRX2RNX` 转成普通 RINEX。

5. **坏 NetCDF 缓存**  
   源文件更新后删 `.nc` 重读。缓存与源 SHA/mtime 不一致就不要用。

6. **半截 gzip / 下载成 HTML**  
   `gunzip -t`；`head` 见 `<!DOCTYPE` → 重新走 Earthdata/CDDIS 鉴权下载。

7. **GPST / UTC 混用**  
   对 IONEX、磁暴时刻、闪烁事件前，写明时间系再减。

8. **`tlim` 顺序反了或越界**  
   得到空维。先 `gtime` 看真实覆盖再设窗。

9. **`use='G'` 写成 `use='GPS'`**  
   系统码是单字母（G/E/C/R/J/I…），以文档为准。

10. **LLI 未加载却做周跳分析**  
    开 `useindicators`；或把周跳交给专用链。

11. **多路径站硬跑 TEC**  
    先 [anubis](./anubis.md) QC；坏站别在 georinex「读成功」就当科学可用。

12. **NAV 日界 / 混合星座缺星**  
    OBS 有 `C`/`E` 而 NAV 只有 GPS → 下游算坐标失败。换混合 BRDC。

13. **Windows 路径反斜杠进字符串**  
    用 `pathlib.Path` 或原始字符串。

14. **把 `interval=` 当正式抽稀产品**  
    对外分发 RINEX 用 gfzrnx；读时抽稀仅自用探活。

15. **并行多进程各自 load 巨型文件打爆磁盘缓存**  
    控制并发；先切小窗。

16. **混淆 georinex 与 PyTECGg 作者**  
    georinex = geospace-code；PyTECGg = viventriglia；SH-GIM = 本仓维护者且求解未开源。

---

## 同类选型

| 需求 | 选 | 理由 |
|---|---|---|
| Python 读 RINEX → xarray | **georinex** | 本手册默认 |
| 拼日 / 抽稀 / 改版本 / 筛观测 | **gfzrnx** | 工业向 CLI |
| QC 报告 | **anubis** | XTR/XML |
| 校准 TEC | **pytecgg** | viventriglia |
| 只想看头/时间，极简 | `gtime` / `head` / gfzrnx `-meta` | 不必全量 load |
| C++/高性能自研读盘 | 自写或其它库 | 超本索引范围 |

不要用 georinex 替代 TEQC（已停更）的全部批处理职责——批处理清洗归 gfzrnx。

---

## 操作检查清单

1. venv 内 `import georinex` 成功。  
2. `hatanaka` 或 `CRX2RNX` 对 `.crx` 可用。  
3. `gtime` 给出非空时间范围。  
4. `load` 后 `time`/`sv` > 0。  
5. 双频任务：相位（或码）成对，名字已打印核对。  
6. 大文件先过滤再全量。  
7. `.nc` 与源一致；源变则删缓存。  
8. 下游工具吃的是**它们要求的格式**（多数要 RINEX，不是 nc）。  
9. 日志保留；失败只改一个变量重试。  
10. 参数以本机 `-h` 覆盖本文过期示例。

---

## 附录 A · 期望 I/O 样例

```text
$ python -m georinex.gtime data/sample.obs
2024-01-01T00:00:00.000  2024-01-01T23:59:30.000  interval≈30.0

$ python -c "import georinex as gr; print(gr.load('data/sample.obs'))"
<xarray.Dataset>
Dimensions:  (time: 2880, sv: 32)
Coordinates:
  * time     (time) datetime64[ns] ...
  * sv       (sv) <U3 'G01' 'G02' ...
Data variables:
    L1C      (time, sv) float64 ...
    L2W      (time, sv) float64 ...
    C1C      (time, sv) float64 ...
    C2W      (time, sv) float64 ...
Attributes: ...
```

失败样例：

```text
UnicodeDecodeError / ValueError: ...
# 或
Dimensions: (time: 0, sv: 0)
```

→ 停。查文件完整性与 `tlim`/`use`。

---

## 附录 B · 最小回归脚本

```bash
#!/usr/bin/env bash
set -euo pipefail
test -f "${1:?用法: $0 file.obs}"
python -m georinex.gtime "$1" | tee /tmp/gtime.out
python - <<PY
import georinex as gr, sys
obs = gr.load(sys.argv[1], use="G")
assert obs.sizes.get("time", 0) > 0
print("PASS", dict(obs.sizes), list(obs.data_vars)[:8])
PY
"$1"
```

---

## 附录 C · 与相邻工具的接口契约

| 上游产出 | georinex 动作 | 下游 |
|---|---|---|
| CDDIS/本地 RINEX | `load` / `gtime` | 人工判定 |
| gfzrnx 清洗后 RINEX | `load(meas=…)` | pytecgg / 自写 |
| BNC 落盘 RINEX | 同左 | 同左 |
| Anubis 仅报告 | 不读 XTR | 用报告决定是否丢站 |

---

## 附录 D · 版本与上游跟踪

- 升级：`pip install -U georinex hatanaka`。  
- 破坏性变更：读 `-h` 与 GitHub Releases。  
- 本文示例旗标落后时：**删示例，信本机帮助**。  
- 许可：MIT；依赖库各自许可另算。

---

## 相关工具

[gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [ionex-gim](./ionex-gim.md) · [rtklib](./rtklib.md) · [sh-gim](./sh-gim.md)


---

## 附录 E · 分系统过滤与多星座核对

```bash
python - <<'PY'
import georinex as gr
from collections import Counter
obs = gr.load("data/SITE.rnx")  # 先全量或 use=None
# 从 sv 坐标统计星座
svs = [str(s) for s in obs.sv.values]
c = Counter(s[0] for s in svs)
print("systems:", dict(c))
for sys in sorted(c):
    sub = gr.load("data/SITE.rnx", use=sys)
    print(sys, dict(sub.sizes), [v for v in sub.data_vars if v[0] in "LC"][:6])
PY
```

**操作要求：** 做 GPS-only TEC 就 `use="G"`；做多星座校准前确认每系统都有成对频率与对应 NAV。

---

## 附录 F · 与 Anubis / GFZRNX 的推荐顺序

```text
下载 RINEX
  → (可选) gfzrnx -chk / -smp / 拼日
  → (可选) anubis 出 QC
  → georinex gtime + load 探活
  → pytecgg 或 ROTI 或 rnx2rtkp
```

禁止顺序：先全量 georinex 读 1 Hz 再发现站是坏站。先 QC / 抽稀。

---

## 附录 G · NetCDF 字段抽查

```bash
python - <<'PY'
import xarray as xr
ds = xr.open_dataset("data/SITE_30s_G.nc")
print(ds)
print(ds.attrs)
# 随机抽一颗星非 NaN 比例
import numpy as np
v = ds["L1C"].isel(sv=0).values
print("finite ratio", np.isfinite(v).mean())
ds.close()
PY
```

有限值比例接近 0 → 观测量名滤错或时间窗错。

---

## 附录 H · 常见异常栈对照

| 栈 / 消息关键词 | 动作 |
|---|---|
| `No such file` | 改路径；检查 symlink |
| `not a gzip` | 扩展名是 `.gz` 但内容是纯 RINEX → 改名或换 opener |
| `CRX` / `hatanaka` | 装 hatanaka 或预转换 |
| `NetCDF: Not a valid ID` | 删坏 nc |
| `memoryerror` / OOM kill | 过滤；分块 `tlim` |
| `KeyError: 'L1'` | 打印 data_vars |

---

## 附录 I · 批处理模板（按日）

```bash
#!/usr/bin/env bash
set -euo pipefail
IN_DIR=data/obs
OUT_DIR=data/nc
mkdir -p "$OUT_DIR" logs
for f in "$IN_DIR"/*.rnx; do
  b=$(basename "$f" .rnx)
  python -m georinex.gtime "$f" | tee "logs/${b}_gtime.txt"
  python - <<PY
import georinex as gr
from pathlib import Path
f = Path("$f")
obs = gr.load(f, use="G")
out = Path("$OUT_DIR") / f"{f.stem}_G.nc"
obs.to_netcdf(out)
print("wrote", out)
PY
done
```

---

## 附录 J · 不要做的事（再强调）

- 不要在未核对 `data_vars` 时复制粘贴他人 `meas=` 列表。  
- 不要把 georinex Dataset 直接当成已校准 TEC 表发布。  
- 不要假设所有站都有 `L2W`；本地跟踪码以接收机为准。  
- 不要忽略许可与数据提供方条款（工具 MIT ≠ 数据可任意再分发）。

---

## 附录 K · 与 data-access 的衔接命令

```bash
# 示例：确认下载文件后再读（具体下载命令见 data-access.md）
ls -lh data/raw/
head -n 5 data/raw/SOME00XXX_R_*.rnx
python -m georinex.gtime data/raw/SOME00XXX_R_*.rnx
```

文件名 RINEX3 很长：始终用 tab 补全或 `pathlib` glob，避免手打截断。

---

## 附录 L · 性能笔记（可操作）

1. 第一次全量读建立直觉；之后默认 `use`+`meas`。  
2. 需要重复实验：写 nc，后续只读 nc。  
3. HDD 上大文件：先复制到 SSD 工作区再 load。  
4. NFS 家目录：临时文件与 nc 写本地盘。  
5. 分析完删中间 nc，保留原始 RINEX 与脚本。

---

## 附录 M · 验收表（交付给同事）

| 项 | 命令 / 证据 | 通过标准 |
|---|---|---|
| 安装 | `import georinex` | 无异常 |
| 时间 | `gtime` 输出 | 覆盖任务日 |
| 维 | `print(obs.sizes)` | time>0,sv>0 |
| 双频 | data_vars 列表截图/日志 | 成对 L/C |
| 缓存 | `ls -l *.nc` | 非 0 字节 |
| 下游 | 下一工具试读 RINEX | 退出码 0 |

---

## 相关工具（复述）

读盘 [georinex](./georinex.md) → 清洗 [gfzrnx](./gfzrnx.md) → QC [anubis](./anubis.md) → TEC [pytecgg](./pytecgg.md) → GIM 对照 [ionex-gim](./ionex-gim.md) → 定位 [rtklib](./rtklib.md)。
