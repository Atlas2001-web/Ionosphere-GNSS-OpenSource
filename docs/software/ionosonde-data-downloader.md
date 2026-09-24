# Ionosonde-Data-Downloader · 公共测高仪参数下载操作手册

目录：[`PROJECTS.json` → `Ionosonde-Data-Downloader`](../../PROJECTS.json) · 上游 <https://github.com/bzossi/Ionosonde-Data-Downloader> · 许可 **MIT** · tip **`ea80896`**（★**2**）· **无 PyPI** · 本机验证（2026-09-24 07:22 EDT；**质检复跑 07:28 EDT**：`station=13` Townsville **2010**→**(8760, 5)**/fof2 **[5.3, 6.1, 7.8]**；`station=3` Kokubunji **2020** auto→**(35136, 4)**/fof2 **[2.86, 2.82, 2.82]**；manual **(8784, 4)**；Aus **15** 站）：克隆后 `import iono_data_downloader`；澳大利亚 Townsville **2010** → shape **(8760, 5)** / foF2 首值 **5.3**；日本 Kokubunji **2020** auto → **(35136, 4)** / foF2 首值 **2.86**；依赖 **pandas + lxml + openpyxl**；OMNI2 在 pandas≥2.2 触 `delim_whitespace` 坑（见下）

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
# GIRO：station 为 Giro_stats.csv 行号；全年请求可能较慢
# df, station, year = idd.GIRO(station=…, year=2016)

# OMNI2（pandas 2.2+ 本机失败示例）：
# idd.OMNI2_indexes(2000)
# TypeError: read_table() got an unexpected keyword argument 'delim_whitespace'
```

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
| GIRO 全年 | **未跑**（慢；接口已探） |
