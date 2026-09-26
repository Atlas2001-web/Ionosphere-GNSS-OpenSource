# Ionosonde-Data-Downloader · 公共测高仪参数下载操作手册

目录：[`PROJECTS.json` → `Ionosonde-Data-Downloader`](../../PROJECTS.json) · 上游 <https://github.com/bzossi/Ionosonde-Data-Downloader> · 许可 **MIT** · tip **`ea80896`**（★**2**）· **无 PyPI** · 本机验证（2026-09-24 07:22 EDT；**质检复跑 07:28 EDT**：`station=13` Townsville **2010**→**(8760, 5)**/fof2 **[5.3, 6.1, 7.8]**；`station=3` Kokubunji **2020** auto→**(35136, 4)**/fof2 **[2.86, 2.82, 2.82]**；manual **(8784, 4)**；Aus **15** 站）：克隆后 `import iono_data_downloader`；澳大利亚 Townsville **2010** → shape **(8760, 5)** / foF2 首值 **5.3**；日本 Kokubunji **2020** auto → **(35136, 4)** / foF2 首值 **2.86**；依赖 **pandas + lxml + openpyxl**；OMNI2 在 pandas≥2.2 触 `delim_whitespace` 坑（见下）

> **质检复跑通过（2026-09-26 05:03–05:06 EDT，tip `ea80896`，Python 3.13 + pandas 3.0.6）**：Townsville 2010 `(8760, 5)` / fof2 `[5.3, 6.1, 7.8]` / URL `…375504.10.gz` / `year` 返回 10、Kokubunji 2020 manual `(8784, 4)` auto `(35136, 4)` / fof2 `[2.86, 2.82, 2.82]` / TO536、Aus 站表 15 行、OMNI2 `delim_whitespace` TypeError 逐字一致。**已修**：GIRO 库函数实测 `HTTPError 404`（`common/DIDBGetValues` 下线，Tomcat 404 776 B）——§3.3 注明、新增 3.3.1 公开替代 `fastchar/getbest` 真实 curl + pandas 解析与输出（WP937 2016-01-01 286 行；2016-01 `(3306, 6)`），指出 `MUFD` 须写 `MUF(D)`；失败表加 3 行（含 429 限流）、本机记录更新。未复跑：`single_use.py` 交互、Aus 2014 后 auto 路径、proxy。

> 岗位：从 **澳大利亚 SWS / 日本 NICT / GIRO DIDBase** 拉一年份 foF2·hmF2(hpF2)·foE·hmE·M3000F2 等到 **pandas**。冲突时：**上游 README / 各库 Rules of the Road > 本文**。使用须致谢各数据源。

## 1. 用途与边界

**做：**

- `ionosondesAustralia` / `ionosondesJapan` / `GIRO`：交互或 `station=`+`year=` 非交互
- 可选 `proxy=`；日本同时返回 **manual** 与 **auto** 定标两表
- 附带 `OMNI2_indexes(year)`（NASA OMNI2 低分辨率指数；见坑）
- 交互入口：`python single_use.py`（选库→站→年→CSV/Excel）

**不做：**

- **不** 拉原始 ionogram 图 / SAO 全量 → 各门户另有路径
- **不** 做 IRI/NeQuick 模式 → [iri2016](./iri2016.md) / [nequickg](./nequickg.md)
- **不** 拉 Swarm TEC → [viresclient](./viresclient.md)
- **不** 闪烁 ISMR → [ismr-downloader](./ismr-downloader.md)

一句话：**测高仪特征参数（foF2 等）按站·年批量备数**。

| 术语 | 含义 |
| --- | --- |
| foF2 / foE | F2 / E 层临界频率 (MHz) |
| hpF2 | 本仓列名（原 hmF2 / h′F2；tip `ea80896` 更名） |
| GIRO | Global Ionospheric Radio Observatory（UML DIDBase） |
| URSI / 站码 | GIRO `ursiCode`；日本如 `TO535`/`TO536` |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/bzossi/Ionosonde-Data-Downloader.git
cd Ionosonde-Data-Downloader
# tip 本机：ea80896
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install pandas lxml html5lib openpyxl
# 必须在仓根运行（相对读 Aus_stations.csv / Giro_stats.csv）
python -c "import iono_data_downloader as idd; print('import OK', idd)"
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Import lxml failed` | `pd.read_html` 要解析器 | `pip install lxml`（或 html5lib） |
| `FileNotFoundError: Aus_stations.csv` | 不在仓根 / 改了 cwd | `cd` 到克隆根再 `import` |
| `No module named 'Australia'` | 把单文件拷走 | 保留仓内同级 `.py`；或把仓根加 `PYTHONPATH` |
| 无 CLI 入口 | 设计如此 | 用 `single_use.py` 或 `import iono_data_downloader` |

## 3. 端到端（本机真跑；质检复跑 2026-09-24 07:28 EDT）

### 3.1 澳大利亚 SWS（Townsville 2010）

站索引以仓内 `Aus_stations.csv` 为准（本机 **15** 站；**townsville = 13**；README 旧表含 mawson 等已删站，勿硬抄序号）。

```bash
cd ~/iono_ops/Ionosonde-Data-Downloader
source .venv/bin/activate
python - <<'PY'
import iono_data_downloader as idd
df, station, year = idd.ionosondesAustralia(station=13, year=2010)
print(station, year, df.shape, list(df.columns))
print(df.head(3))
print("fof2 head", df["fof2"].dropna().head(3).tolist())
PY
```

**本机 stdout（节选）：**

```text
Searching available years...
Downloading data...
https://downloads.sws.bom.gov.au/wdc/iondata/au/townsville/3755.04/375504.10.gz
M3000F2 empty
townsville 10 (8760, 5) ['fof2', 'hpF2', 'foE', 'hmE', 'M3000F2']
                     fof2   hpF2   foE   hmE  M3000F2
Time
2010-01-01 00:00:00   5.3  446.0   NaN  91.0      NaN
2010-01-01 01:00:00   6.1  349.0   NaN  91.0      NaN
2010-01-01 02:00:00   7.8  287.0  3.59  91.0      NaN
fof2 head [5.3, 6.1, 7.8]
```

要点：

- 返回的 `year` 可能是两位 **`10`**（不是 `2010`）
- **2014 前** 走 `…/iondata/au/<stat>/…/*.gz` 小时值；**2014 后** 走 `wdc_ion_auto` 自动定标（分辨率 5/10 min）
- 部分站/年 `M3000F2 empty` 属正常

### 3.2 日本 NICT（Kokubunji 2020）

交互菜单站号 **1…5**（Wakkanai…Okinawa）；**3 = Kokubunji**。

```bash
python - <<'PY'
import iono_data_downloader as idd
df_m, df_a, station, year = idd.ionosondesJapan(station=3, year=2020)
print(station, year, "manual", df_m.shape, "auto", df_a.shape)
print(df_a.head(2))
print("fof2 head", df_a["fof2"].dropna().head(3).tolist())
PY
```

**本机 stdout（节选）：**

```text
https://wdc.nict.go.jp/Ionosphere/archive/observation-history/factor-manual-TO536-2020H.sjis.txt
Downloading data...
https://wdc.nict.go.jp/Ionosphere/archive/observation-history/factor-auto-TO536-2020.sjis.txt
Kokubunji 2020 manual (8784, 4) auto (35136, 4)
                     fof2  foE    hmE  hpF2
time
2020-01-01 00:00:00  2.86  NaN  106.0   NaN
2020-01-01 00:15:00  2.82  NaN  108.0   NaN
fof2 head [2.86, 2.82, 2.82]
```

站码会随年切换（例 Kokubunji `TO535`→`TO536`）；以实际请求 URL 为准。

### 3.3 GIRO / OMNI2

```python
import iono_data_downloader as idd
# GIRO：station 为 Giro_stats.csv 的 0 起行号（WP937 Wallops = 92）
# 2026-09 起**必失败**：Giro.py 两处都拼 lgdc.uml.edu/common/DIDBGetValues，该接口已下线
# idd.GIRO(station=92, year=2016)
# Downloading (time depends on GIRO servers status ...)
# HTTPError: HTTP Error 404:           ← 替代见 §5 与 3.3.1

# OMNI2（pandas 2.2+ 本机失败示例）：
# idd.OMNI2_indexes(2000)
# TypeError: read_table() got an unexpected keyword argument 'delim_whitespace'
```

#### 3.3.1 GIRO 替代：fastchar/getbest（匿名，本机真跑 2026-09-26 05:05 EDT）

旧接口实测（与库里 URL 同形）：

```bash
curl -s -o /dev/null -w 'HTTP %{http_code} %{size_download} B\n' \
 'https://lgdc.uml.edu/common/DIDBGetValues?ursiCode=WP937&charName=foF2,foE,hmF2,hmE,MUFD&DMUF=3000&fromDate=2016%2F01%2F01+00%3A00%3A00&toDate=2016%2F01%2F01+23%3A59%3A00'
# HTTP 404 776 B   （Tomcat：The requested resource [/common/DIDBGetValues] is not available）
```

公开替代 `fastchar/getbest`（参数同名；**`MUFD` 要写成 `MUF(D)`**，否则头里 `# STATUS: WARNING (Unknown characteristic name: MUFD)` 且该列缺失）：

```bash
curl -s -w '# HTTP %{http_code} %{size_download} B\n' \
 'https://lgdc.uml.edu/fastchar/getbest?ursiCode=WP937&charName=foF2,foE,hmF2,hmE,MUF(D)&DMUF=3000&fromDate=2016%2F01%2F01+00%3A00%3A00&toDate=2016%2F01%2F01+23%3A59%3A00' \
 > wp937_20160101.txt
grep -E '^# Time|^20' wp937_20160101.txt | head -3; tail -1 wp937_20160101.txt
```

```text
# Time                    CS   foF2 QD   foE QD   hmF2 QD    hmE QD MUF(D) QD
2016-01-01T00:00:08.000Z 100  3.000 //   --- __  422.2 //  110.0 //  7.096 //
2016-01-01T00:05:08.000Z 100  3.000 //   --- __  372.7 //  110.0 //  7.921 //
# HTTP 200 23478 B
```

全天 286 行数据、23478 B（HTTP 200）；头部 25 行 `#` 注释，列名行是 `# Time`（中间有空格），缺测为 `---`，每个特征后跟一列 `QD`。库里的 `read_table(url, skiprows=57, sep='\\s+')` 与 `df['#Time']` 都对不上这个格式，**只换 URL 不够**。直接读成 pandas（与本库返回列相近）：

```python
import io, urllib.request, pandas as pd
code, year = "WP937", 2016
url = ("https://lgdc.uml.edu/fastchar/getbest?ursiCode=%s&charName=foF2,foE,hmF2,hmE,MUF(D)&DMUF=3000"
       "&fromDate=%d%%2F01%%2F01+00%%3A00%%3A00&toDate=%d%%2F01%%2F31+23%%3A59%%3A00") % (code, year, year)
txt = urllib.request.urlopen(url, timeout=120).read().decode()
raw = [l for l in txt.splitlines() if l.startswith("# Time")][0][1:].split()
cols = [c if c != "QD" else raw[i-1] + "_QD" for i, c in enumerate(raw)]   # QD 列重名 → foF2_QD 等
df = pd.read_csv(io.StringIO(txt), comment="#", sep=r"\s+", names=cols, na_values=["---"])
df.index = pd.to_datetime(df.pop("Time")); df = df.drop(columns=[c for c in df if c.endswith("_QD")])
print(df.shape, list(df.columns)); print(df.head(3)); print("foF2 median", df.foF2.median())
```

```text
(3306, 6) ['CS', 'foF2', 'foE', 'hmF2', 'hmE', 'MUF(D)']
                            CS  foF2  foE   hmF2    hmE  MUF(D)
Time
2016-01-01 00:00:08+00:00  100  3.00  NaN  422.2  110.0   7.096
2016-01-01 00:05:08+00:00  100  3.00  NaN  372.7  110.0   7.921
2016-01-01 00:10:10+00:00  100  3.15  NaN  379.2  110.0   8.100
foF2 median 4.65
```

（WP937 2016-01 一个月 1.6 s。长时段请按月分段、别并发：本机连续 4 次请求后第 5 次即 **`HTTPError: HTTP Error 429: Too Many Requests`**，隔约 1 min 恢复，循环里要 `sleep`/重试；CS=999 为人工判读。参数/置信度细节见 [giro-ionosonde](./giro-ionosonde.md)。）

OMNI2 修复方向（勿改上游也可本地 monkeypatch）：把 `delim_whitespace=True` 换成 `sep=r'\s+'`（或降级 `pandas<2.2`）。指数备选 → [geospacelab](./geospacelab.md)。

### 3.4 交互壳

```bash
python single_use.py
# 1 Australian / 2 Japanese / 3 GIRO → 选站 → 选年 → 1 CSV / 2 Excel
```

## 4. 字段说明

| 返回 | 含义 |
| --- | --- |
| `df` | `DatetimeIndex`；列 `fof2, hpF2, foE, hmE, M3000F2`（库而异） |
| `station` | 站名字符串 |
| `year` | 传入年或两位年（Aus 旧路径） |
| Japan `df_manual`, `df_auto` | 人工 / 自动定标；分辨率不同 |

数据使用条件：

- <https://sws.bom.gov.au/World_Data_Centre>
- <https://wdc.nict.go.jp/IONO/HP2009/contact_us_e.html>
- <https://giro.uml.edu/didbase/RulesOfTheRoad.html>

## 5. 失败排查

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Import lxml failed` | 缺 HTML 解析器 | `pip install lxml` |
| `HTTPError` / 空表 | 站年无数据或门户改版 | 换年；浏览器打开同一 URL 核对 |
| `M3000F2 empty` | 源文件无该特征 | 忽略或换站/年 |
| 站号对不上 README | CSV 已更新 | `print(pd.read_csv('Aus_stations.csv', header=None))` |
| `OMNI2` `delim_whitespace` | 新 pandas 删参数 | `sep=r'\s+'` 或降级 pandas |
| `GIRO()` → `HTTPError: HTTP Error 404` | `Giro.py` L75/L95 用的 `lgdc.uml.edu/common/DIDBGetValues` 已下线（Tomcat 404，2026-09-26 实测） | 改用 `https://lgdc.uml.edu/fastchar/getbest?…`，`MUFD`→`MUF(D)`，并按 3.3.1 自己解析（库的 skiprows=57 解析不适配） |
| `year=None` 的「Data available」探测也报 404 | 同上（同一旧接口） | 直接传 `year=`；可用区间看 `Giro_stats.csv`（其 LATEST DATA 停在 2023-04-03，已过时）或 giro-ionosonde 站表 |
| fastchar `HTTP Error 429: Too Many Requests` | 短时间连发请求被限流（本机第 5 次触发） | 每请求间 `sleep` 数秒；429 后等约 1 min 重试 |
| SSL 错（GIRO） | 源码已 `ssl._create_unverified_context` | 仍失败则查代理 `proxy=` |
| 想画图 | — | `df.fof2.plot()`；需自备后端 |

## 6. 交叉

- Swarm/Aeolus 切片：[viresclient](./viresclient.md)
- 空间天气指数/TEC 图：[geospacelab](./geospacelab.md)
- IRI 气候态对照：[iri2016](./iri2016.md) / [pyiri](./pyiri.md) / [pyglow](./pyglow.md)
- GNSS 衍生 TEC：[gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md)
- [data-access](../data-access.md) · 教程 [04](../tutorials/04-iri-nequick.md) / [05](../tutorials/05-scintillation-roti.md)

## 7. 本机记录

| 项 | 值 |
| --- | --- |
| tip | **`ea80896`** |
| Aus stations CSV | **15** 行；townsville **13** |
| Aus 2010 Townsville | **(8760, 5)**；fof2 **5.3/6.1/7.8**；URL `…/375504.10.gz`；`year` 返回 **10** |
| Japan 2020 Kokubunji | manual **(8784, 4)** / auto **(35136, 4)**；fof2 **2.86**；码 **TO536** |
| OMNI2 2000 | **TypeError** `delim_whitespace`（pandas 本机 2.x） |
| GIRO（库函数） | **HTTPError 404**（DIDBGetValues 下线）；替代 fastchar WP937 2016-01 → **(3306, 6)**，foF2 首值 **3.00** |
