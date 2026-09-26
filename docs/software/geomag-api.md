# 地磁台数据 API（USGS Geomag · INTERMAGNET/BGS GIN · NRCan FDSN · MACCS · THEMIS GMAG）· 下载侧 操作手册

入口：[USGS Geomag Web Service](https://geomag.usgs.gov/ws/docs/) · [BGS GIN（INTERMAGNET 节点）](https://imag-data.bgs.ac.uk/GIN_V1/GINServices) · [Earthquakes Canada FDSN](https://www.earthquakescanada.nrcan.gc.ca/fdsnws/) · [MACCS](http://space.augsburg.edu/maccs/) · [THEMIS GMAG](https://themis.ssl.berkeley.edu/gmag/) · 本机验证 **2026-09-26 03:22–03:40 EDT**。只用 curl + 系统 Python 3.13（`json` / `numpy`）；样例是 BOU（Boulder）在 **2024-05-10 18:00–18:59 UT**（Gannon 超级磁暴当天）的数据，全部下到 `/tmp` 级的小文件，用完即删。

> 岗位：把**地磁台分钟 / 秒值**拉到本地，给 TEC / ROTI 事件配磁场时间轴（dB/dt、H 扰动）。本文**不讲**指数（Kp / Dst / SYM-H 用 [pyspedas](./pyspedas.md)）、不讲 SuperMAG，也不做基线处理或 GIC 建模。  
> 门槛总表见 [data-access 决策表](../data-access.md#电离层与地磁门户决策表)：[E8 USGS](../data-access.md#dp-e8) · [E9 NRCan](../data-access.md#dp-e9) · [E10 BGS](../data-access.md#dp-e10) · [E11 MACCS](../data-access.md#dp-e11) · [E12 THEMIS](../data-access.md#dp-e12)。  
> 冲突时：**服务端返回的 422 错误文本 / 官方文档 > 本文**。

## 1. 它解决什么，边界在哪

| 路线 | 覆盖 | 输出 | 账号 | 本文定位 |
| --- | --- | --- | --- | --- |
| **USGS Geomag ws** `geomag.usgs.gov/ws/data/` | USGS 台站（`/ws/observatories/` 列出 43 个，含 BOU / FRD / HON …） | IAGA-2002 / JSON | 无 | 主路线：实时到准定值 |
| **BGS GIN** `imag-data.bgs.ac.uk/GIN_V1/GINServices` | 全部 INTERMAGNET 台（含 USGS 的 BOU） | IAGA-2002 / JSON | 无 | 主路线：**definitive** 定值与跨国台站 |
| NRCan FDSN（网络码 C2） | 加拿大台（OTT / MEA / BLC …） | miniSEED | 无 | 备选：高纬加拿大 |
| MACCS | 加拿大北极 9 个站 | IAGA-2002，0.5 s | 无 | 备选：极隙区 |
| THEMIS GMAG | 北美众多合作台网 | CDF L2，1 s | 无 | 备选：亚暴 / 北美链；**用 PySPEDAS 读的方法见 [pyspedas](./pyspedas.md)** |

**术语**
- **元素**：X 北、Y 东、Z 下；H 水平强度；D 偏角；F 总强度（标量仪）；G = ΔF。
- **数据类型**，从快到准：`variation`（实时、无基线）→ `adjusted` / provisional → `quasi-definitive` → `definitive`。

## 2. 安装

```bash
curl --version | head -1          # 只要 curl
python3 -c "import numpy; print(numpy.__version__)"    # 可选：算 H/D、统计
```

miniSEED 需要 ObsPy（`pip install obspy`）解码；CDF 需要 `cdflib`。本轮这两个都**没装**，只核了文件头（坑 11）。

## 3. 真实命令与输出

### 3.1 USGS：一站一小时，1 min / 1 s × IAGA-2002 / JSON

```bash
U="https://geomag.usgs.gov/ws/data/"
curl -s "$U?id=BOU&starttime=2024-05-10T18:00:00Z&endtime=2024-05-10T18:59:00Z&sampling_period=60&format=iaga2002"
```

```text
 Reported               XYZF                                         |
 Sensor Orientation     HDZ                                          |
 Data Interval Type     1-minute                                     |
 Data Type              adjusted                                     |
DATE       TIME         DOY     BOUX      BOUY      BOUZ      BOUF   |
2024-05-10 18:00:00.000 131     20366.87   2988.88  99999.00  51208.70
2024-05-10 18:01:00.000 131     20371.56   3000.16  99999.00  51209.30
```

不带 `type` / `elements` 时，**默认是 `adjusted` + `XYZF`**；这一小时 adjusted 的 Z **整段缺测**（99999）。文件共 79 行 = 19 行头 + 60 行数据。

| 请求（BOU 18:00–18:59，`type=variation`，`elements=H,Z,F`） | HTTP | 大小 | 用时 | 行 / 点 |
| --- | --- | --- | --- | --- |
| `sampling_period=60&format=json` | 200 | 4057 B | ~1–2 s | 60 |
| `sampling_period=1&format=iaga2002`（`endtime=…18:59:59Z`） | 200 | 257091 B | 3.8 s | 3600 |
| `sampling_period=1&format=json` | 200 | 203809 B | 11.6 s | 3600，无 null |

1 s IAGA 的前两行：

```text
DATE       TIME         DOY     BOUH      BOUZ      BOUF      BOUNUL |
2024-05-10 18:00:00.000 131     20652.14  46325.30  51229.78  99999.00
2024-05-10 18:00:01.000 131     20653.69  46325.08  51230.13  99999.00
```

只要了 3 个元素，IAGA 仍固定输出 4 列，第 4 列叫 **`BOUNUL`**，全填 99999（坑 4）。

JSON 结构（1 min）：`times[]` 是 ISO 时间串，`values[]` 每个元素一条 `{"id":"H","metadata":{…,"location":"R0"},"values":[20654.194, 20660.482, …]}`；缺测是 **`null`**。

### 3.2 数据类型可用性：variation / adjusted / quasi-definitive / definitive

同一时刻，`elements=X,Y,Z,F,H,D`，JSON（IAGA 最多 4 个元素，要 6 个只能用 JSON，坑 3）：

```text
variation         X [20382.46, 20386.99]   Y [3339.487, 3350.829]  Z [46325.272, 46323.244]  F [51230.696, 51231.304]  H [20654.194, 20660.482]  D [5.584, 7.324]
adjusted          X [20366.872, 20371.562] Y [2988.884, 3000.161]  Z [None, None]            F [51208.696, 51209.304]  H [20585.016, 20591.297]  D [500.921, 502.670]
quasi-definitive  X [20363.3, 20368.0]     Y [2989.7, 3000.9]      Z [None, None]            F [None, None]            H [20581.601, 20587.881]  D [501.143, 502.879]
definitive        X [None, None] …（全部 null，location D0）
```

`location` 码对应：`R0` variation、`A0` adjusted、`Q0` quasi-definitive、`D0` definitive。

**USGS ws 上 BOU 的 definitive 可用性**（每天取 00:00 的 X）：

| 日期 | definitive | quasi-definitive |
| --- | --- | --- |
| 2010-06-01 | `[20611.9, 20611.4]` | — |
| 2018-06-01 / 2020-06-01 / 2022-06-01 / 2023-06-01 / 2024-01-01 | `[None, None]` | 2022 起都有，例如 `[20522.1, 20522.8]` |

同一台同一天的 **definitive 在 GIN 上有**（3.3 节，Publication Date 2025-08-01）。要定值，就走 GIN。

### 3.3 INTERMAGNET via BGS GIN：同台 BOU 对照

```bash
G="https://imag-data.bgs.ac.uk/GIN_V1/GINServices?Request=GetData&testObsys=0&observatoryIagaCode=BOU&orientation=native"
curl -s -OJ "$G&format=IAGA2002&samplesPerDay=minute&dataStartDate=2024-05-10&dataDuration=1&publicationState=definitive"
# 200，104157 B，1.3 s；Content-Disposition: filename=bou20240510dmin.min（-J 按它落盘）
```

```text
 Reported               XYZG                                         |
 Sensor Orientation     HDZF                                         |
 Data Type              Definitive                                   |
 Publication Date       2025-08-01                                   |
 # D-conversion factor 10000                                         |
DATE       TIME         DOY     BOUX      BOUY      BOUZ      BOUG   |
2024-05-10 18:00:00.000 131     20366.30   2988.20  46888.80  51208.65
```

- GIN 上 `publicationState=best-avail` 在这一天返回的也是 Definitive。
- `samplesPerDay=second` 一天：200，6135820 B，7.8 s，`Data Type Provisional`；18:00:00 那一行为 `20365.06 2987.14 46888.76 51207.78`（**有 Z**）。
- `format=json`（1 天分钟）：200，86188 B，键为 `datetime, @info, G, X, Y, Z`；18:00 那一点为 `[20366.3, 2988.2, 46888.8, -0.5]`，缺测为 `None`。
- 列名的坑：IAGA 表头写 `XYZG`，第 4 列却是 **F 标量值**（51208.65）；JSON 的 `G` 才是真正的 ΔF（−0.5）（坑 6）。

### 3.4 算 H / D，比较两条路线（`cmp.py`）

```python
import json, urllib.request, numpy as np
U = ("https://geomag.usgs.gov/ws/data/?id=BOU&starttime=2024-05-10T18:00:00Z"
     "&endtime=2024-05-10T18:59:00Z&sampling_period=60&type=adjusted&elements=X,Y,Z,F&format=json")
d = json.load(urllib.request.urlopen(U, timeout=60))
usgs = {v["id"]: np.array([np.nan if x is None else x for x in v["values"]]) for v in d["values"]}   # null → NaN
rows = [l.split() for l in open("bou20240510dmin.min") if l.startswith("2024-05-10 18:")]
gin = np.array([[float(x) for x in r[3:7]] for r in rows]); gin[gin >= 99999] = np.nan              # 99999 → NaN
X, Y, Z, G = gin.T
H_gin = np.hypot(X, Y); D_gin = np.degrees(np.arctan2(Y, X)) * 60        # D 用角分
H_usgs = np.hypot(usgs["X"], usgs["Y"])
print("n", len(rows), "usgs Z null:", int(np.isnan(usgs["Z"]).sum()), "gin Z NaN:", int(np.isnan(Z).sum()))
print("18:00 H usgs %.2f gin %.2f  D gin %.2f arcmin" % (H_usgs[0], H_gin[0], D_gin[0]))
for k, a, b in [("X", usgs["X"], X), ("Y", usgs["Y"], Y), ("H", H_usgs, H_gin)]:
    diff = a - b; print(k, "adjusted-definitive: mean %.2f  std %.2f  max|%.2f|" % (np.nanmean(diff), np.nanstd(diff), np.nanmax(abs(diff))))
Fv = np.sqrt(X**2 + Y**2 + Z**2); print("gin col4 - |XYZ| at 18:00: %.2f" % (G[0] - Fv[0]))
```

```text
n 60 usgs Z null: 60 gin Z NaN: 0
18:00 H usgs 20585.02 gin 20584.35  D gin 500.82 arcmin
X adjusted-definitive: mean 0.73  std 0.14  max|1.07|
Y adjusted-definitive: mean 0.77  std 0.14  max|1.19|
H adjusted-definitive: mean 0.83  std 0.15  max|1.21|
gin col4 - |XYZ| at 18:00: 0.50
```

怎么读：
- USGS adjusted 比 GIN definitive 系统性偏高约 0.8 nT，但抖动只有 0.15 nT。**做 dB/dt、扰动形态，两者都行；做绝对值或长期趋势，用 definitive。**
- 用 X / Y 算出来的 H 与 USGS 自带的 H 完全一致（adjusted：差 0.0 nT）。D 为 500.92′ ≈ 8.35°，与 `atan2(Y,X)` 相符。

**variation 的 D 不是偏角**：variation 的 D = 5.584，而 `atan2(Y,X)` = 558.28′。`/ws/observatories/` 给 BOU 的 `declination_base` 为 **5527**（单位 0.1′），552.7 + 5.584 = 558.28′。所以 variation 的 D 是相对基准偏角的**增量（角分）**（坑 5）。

### 3.5 缺测：99999 与 null

- **USGS**：IAGA 里是 `99999.00`（3.1 节整列 Z），JSON 里是 `null`。
- **GIN**：同一天的 IAGA 有 9 行带 99999，例如：
  ```text
  2024-05-10 21:06:00.000 131     20457.80   2714.10  99999.00  51353.00      # 21:06–21:11 缺 Z
  2024-05-10 21:40:00.000 131     99999.00  99999.00  47211.80  51630.00      # 缺 X/Y
  ```
  JSON 里对应位置是 `None`（21:06 → `[20457.8, 2714.1, None, None]`，G 也跟着为空）。
- 读入时统一 `>= 99999 → NaN`、`None → NaN`（见 `cmp.py`）。**别对 99999 直接插值或求差分**。

### 3.6 上限与限速（实测，非官方承诺）

| 请求（BOU，`elements=H`，`type=variation`） | 结果 |
| --- | --- |
| 1 s × 1 天（86400 点），IAGA | 200，6135891 B，**29.4 s** |
| 1 s × 2 天 | **404**，721 B HTML "The specified URL cannot be found."，30.4 s |
| 1 min × 1 天 / 7 天 / 14 天 | 200：103731 B 6.8 s / 717171 B 20.3 s / 1432851 B 20.5 s |
| 1 min × 30 天、× 90 天 | **404**（同上 HTML），30.4 s |
| 1 min × 2020–2025（JSON） | **422**：`Request exceeds output sample limit (3156479 > 1296000)` |

- 硬上限：**1,296,000 个输出样本**，超了立刻回 422 并说明原因。
- 实际更早撞上的是约 **30 s 网关超时**：伪装成 **404 HTML**，不是 JSON 错误（坑 7）。**1 s 数据按 ≤1 天切，1 min 数据按 ≤14 天切。**
- 限速：连续 6 次小请求全部 200（1.1–11.2 s），响应头里**没有**任何 `RateLimit` / `Retry-After`。仍请串行、加间隔。
- GIN：连续 3 次 200（约 1.3 s）；分钟数据 `dataDuration=31` 为 200，3171357 B，6.1 s；`=100` 为 200，10225917 B，14.6 s。

### 3.7 备选路线（一条命令一个结果）

```bash
# NRCan FDSN：OTT 18:00–19:00；UFX = 1 min X，LFX = 1 s X
F="https://www.earthquakescanada.nrcan.gc.ca/fdsnws/dataselect/1/query?net=C2&sta=OTT&loc=R0&starttime=2024-05-10T18:00:00&endtime=2024-05-10T19:00:00"
curl -s -o ott_ufx.mseed "$F&cha=UFX"   # 200，1024 B = 2 条 512 B 记录，起点 17:06 与 19:00，各 114 点
curl -s -o ott_lfx.mseed "$F&cha=LFX"   # 200，16896 B = 33 条记录，首条从 17:58:38 开始
curl -s -o ott_uf.mseed  "$F&cha=UF%3F" # 200，4096 B（X/Y/Z/F 四个通道）；未编码的 "?" → 404
curl -s "https://www.earthquakescanada.nrcan.gc.ca/fdsnws/station/1/query?net=C2&sta=OTT&loc=R0&cha=UFX&level=channel&format=text"
# …|Scale|ScaleFreq|ScaleUnits|SampleRate|… → 1.0|1.0|n/a|0.016666666666666666|

# MACCS：表单返回直链，再下 IAGA-2002（0.5 s，约 12 MB/天）
curl -s "http://space.augsburg.edu/maccs/retrieveiaga2002.jsp?stations=IG&startYear=2024&month=5&dayOfMonth=10&startDay=131&GetData=Get+Data" | grep -oE 'IAGA2002/[^"]+'
# IAGA2002/IGL/2024/igl20240510v_l1_half_sec.sec
curl -s -r 0-1900 "http://space.augsburg.edu/maccs/IAGA2002/IGL/2024/igl20240510v_l1_half_sec.sec" | grep -E '^2024' | head -1
# 2024-05-10 00:00:00.250 131      6304.20   1270.48  80601.53  88888.88

# THEMIS GMAG：日文件 CDF（读法见 pyspedas 手册）
curl -s -I "https://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/fykn/2024/thg_l2_mag_fykn_20240510_v01.cdf" | grep -i content-length
# Content-Length: 1770138    （版本号猜错，例如 _v02 → 404）
```

## 4. 输入与输出

| 路线 | 必填输入 | 输出单位 / 字段 |
| --- | --- | --- |
| USGS | `id`、`starttime` / `endtime`（ISO，带 Z） | nT；D 为角分（variation 为相对 `declination_base` 的增量）；JSON 的 `times` / `values[].values`；IAGA 固定 4 列 |
| GIN | `observatoryIagaCode`、`dataStartDate`、`dataDuration`（天）、`samplesPerDay`、`publicationState` | IAGA 文件名为 `<iaga><yyyymmdd><d/p/v…><min/sec>`；JSON 的 `datetime` + 元素数组 + `@info` |
| NRCan | `net=C2&sta&loc&cha&starttime&endtime` | miniSEED 整条记录（会超出请求时段），需自己裁剪 |
| MACCS | 站码（IG → IGL）、年 / 月 / 日 | 本地地磁坐标 XYZ，F 填 88888.88 |
| THEMIS | 站名小写 + 日期 | CDF：`thg_mag_<stn>`、`thg_mag_<stn>_time` |

## 5. 参数

| 服务 | 参数 | 取值 / 说明 |
| --- | --- | --- |
| USGS | `elements` | 逗号分隔；IAGA ≤4 个，JSON 可以更多 |
| | `sampling_period` | `1` / `60`（本文实测这两个） |
| | `type` | `variation` / `adjusted` / `quasi-definitive` / `definitive` |
| | `format` | `iaga2002` / `json` |
| | 站表 | `https://geomag.usgs.gov/ws/observatories/`（GeoJSON，43 个；站号写错会 422 并列出合法站号） |
| GIN | `samplesPerDay` | `minute` / `second` |
| | `publicationState` | `best-avail` / `definitive`（`best-avail` 会给当时能拿到的最好一级） |
| | `format` | `IAGA2002` / `json` |
| | `orientation` | `native`（本文只用过 native） |
| | `testObsys=0` | 固定写上 |
| NRCan | `cha` | `UF?` = 1 min，`LF?` = 1 s；`?` 要写成 `%3F`，或用 `*` |

## 6. 在工作流里接哪一步

- **路径 B · 不规则体 / 磁暴**（[README](./README.md#b--不规则体--磁暴)）：用 H 扰动和 dB/dt 标出主相、亚暴时刻，再与 ROTI / TEC 对照；指数层面（SYM-H、Kp）交给 [pyspedas](./pyspedas.md)。
- 高纬 TEC / 闪烁事件：MACCS、THEMIS GMAG、NRCan 补北美极区链；ISR 剖面见 [madrigal](./madrigal.md)。

## 7. 坑（现象 → 原因 → 修复）

1. **默认拿到的不是你以为的数据** → USGS 不写 `type` 就是 `adjusted`，不写 `elements` 就是 `XYZF` → 永远显式写 `type=` 和 `elements=`。
2. **adjusted 的 Z 整段缺测** → BOU 2024-05-10 18 时 adjusted 与 quasi-definitive 的 Z 全是 null，variation 和 GIN definitive 都有 Z → 缺哪个元素就换一种 type 或换 GIN 再查。
3. **422 `No more than four elements allowed for iaga2002 format`** → IAGA-2002 格式固定 4 列 → 超过 4 个元素改用 `format=json`，或者分两次请求。
4. **多出一列 `BOUNUL`** → 只请求 3 个元素时，IAGA 用 NUL 列补到 4 列，全填 99999 → 按列名取列，别按位置取。
5. **variation 的 D 只有 5.58** → 它是相对 `declination_base`（5527 × 0.1′）的增量；adjusted / definitive 的 D 才是绝对角分 → 要偏角就用 adjusted+，或者 `atan2(Y,X)`。
6. **GIN IAGA 表头写 G，数值却是 F** → 表头 `XYZG`，第 4 列 51208.65 ≈ F；JSON 的 `G` 才是 ΔF（−0.5） → 需要 ΔF 就取 JSON，或者自己算 `F_s − |XYZ|`（本例为 +0.50）。GIN JSON 的 `@info` 里 reported / sensor orientation 也写反了，`data_interval_type` 标成 "filtered 1-day"：元数据以 IAGA 头为准。
7. **大请求回 404 HTML，不是错误 JSON** → 约 30 s 网关超时（1 s×2 天、1 min×30 天都会撞上）；只有超过 1,296,000 样本才回真正的 422 → 切片：1 s ≤1 天，1 min ≤14 天；遇到 404 先缩短时段，别当成站号错了。
8. **USGS 上找不到 definitive** → BOU 2018–2024 的 `type=definitive` 全部为 null（2010 年有）→ 定值走 GIN `publicationState=definitive`（2024-05-10 已在 2025-08-01 发布）。
9. **两条路线差约 0.8 nT** → adjusted 与 definitive 基线不同（X 平均偏 0.73，H 平均偏 0.83，std 0.15）→ 同一分析里别混用两种 type；拼接时只能用 definitive。
10. **99999 / 88888 / null 混进统计** → IAGA 缺测为 99999，MACCS 的 F 填 88888.88，JSON 为 null / None → 读入即转 NaN，再做 dB/dt。
11. **FDSN 返回的时段比请求的长** → miniSEED 按整条记录返回（UFX 首条从 17:06 开始），通道比例写 `Scale 1.0 n/a` → ObsPy `trim()` 到请求时段；本轮没解码，数值单位请用 ObsPy 读出后，与 USGS / GIN 同类台对比确认。
12. **USGS 门户页 403，Web 服务却 200** → `www.usgs.gov` 挡无 UA 的脚本，`geomag.usgs.gov/ws` 不挡 → 脚本只打 `/ws/`。
13. **首个请求很慢** → USGS 冷请求 7–11 s，之后 1–2 s；1 s JSON 比 IAGA 慢三倍（11.6 s 对 3.8 s） → 批量拉 1 s 数据用 IAGA，timeout 设 ≥60 s。

## 8. 选型对比

| 需求 | 选 | 理由 |
| --- | --- | --- |
| USGS 台的实时 / 近实时（延迟约 3 min） | **USGS ws**，`type=variation` 或 `adjusted` | 最新；JSON 好解析 |
| 发表用的定值、跨国 INTERMAGNET 台 | **BGS GIN** `publicationState=definitive` | USGS ws 缺 definitive；GIN 一个接口覆盖全网 |
| 一次要 >4 个元素 | USGS `format=json` | IAGA 限 4 列 |
| 加拿大高纬 1 s | NRCan FDSN（`LF?`） | 需 ObsPy 解码 |
| 极隙区 0.5 s | MACCS | 只有 HTTP；F 为占位值 |
| 北美亚暴链 / 多台网 1 s | THEMIS GMAG CDF | 读法见 [pyspedas](./pyspedas.md) |
| Kp / Dst / SYM-H 指数 | [pyspedas](./pyspedas.md) | 不必从台站自己算 |
| 全球台站统一基线的扰动场 | SuperMAG（需注册，本文不含） | — |
