# pynmea2 · 高星标 Python NMEA 0183 解析库操作手册

目录：[`PROJECTS.json` → `pynmea2`](../../PROJECTS.json) · 上游 <https://github.com/Knio/pynmea2> · PyPI **`pynmea2` 1.19.0** · tip **`fcd90dc`** · 许可 **MIT** · Python 2.7 / 3.4+ · 本机验证（2026-09-24 06:04 EDT）：pytest **105 passed**；北京 `demo_beijing.nmea` 流 **36** 句；GGA lat=**39.90418716666667**/lon=**116.39074266666667**/qual=**1**/sats=**12**/alt=**44.0**；经典 RMC **48.1173**/11.516666666666667；坏校验和 → `ChecksumError` · **质检复跑**（2026-09-26 01:40 EDT，新 venv Python 3.13.5；PyPI 最新仍 1.19.0，tip `fcd90dc` 2026-04-21）：pytest **105 passed**（4 warnings）；§3.1–3.4 四段脚本从本页原样抽出跑，输出**逐字一致**（RMC 48.1173/11.516666666666667、构造句 `*47`、`ChecksumError … 00 != 47`、n=36=RMC/GGA/GSA 各 12）；`NMEAStreamReader` 逐行喂同得 36。改 1 处：坑 2 类型说法——`gps_qual` 在 GGA 类里声明为 `int`，**不带类型转换的是 `num_sats`、`horizontal_dil`、`geo_sep`**（字符串 `'06'`/`'3.86'`/`'-8.0'`）。注：§3.2/3.3 的 `demo_beijing.nmea` 是 [gpsd](./gpsd.md) 手册自写的 36 行文件（本机 `~/iono_ops/gpsd-demo/`，2424 B），换机器需按 gpsd §3 重建

> 岗位：纯 Python **NMEA 0183 句子解析/构造**（`parse` / `NMEAStreamReader` / 类型类如 `GGA`）。冲突时：**上游 README / `pynmea2` 源码 > 本文**。现代编解码+生成+流 CLI 生态 → [pynmeagps](./pynmeagps.md)；嵌入式 C → [minmea](./minmea.md)；系统守护 → [gpsd](./gpsd.md)。

## 1. 用途与边界

**做：**

- `pynmea2.parse(line)` → 类型化 `NMEASentence`（`GGA`/`RMC`/`GSA`/… + 多家 proprietary）
- `latitude`/`longitude` 十进制度辅助属性；`is_valid`；校验和检查
- `NMEAStreamReader(stream)` 按行增量解析
- 用类型类构造句子：`str(pynmea2.GGA(...))` 自动补 `*CS`

**不做：**

- **不是** 串口/NTRIP/多协议流 CLI → [pygnssutils](./pygnssutils.md)/[gpsd](./gpsd.md)
- **不是** UBX/RTCM/SBF → [pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)
- **不是** 定位/TEC 引擎
- **无官方 CLI**；脚本里 `import` 即可
- 与 [pynmeagps](./pynmeagps.md) **不是**同一作者栈：本库偏经典解析；semuconsulting 栈偏 GET/SET/POLL + 与 pyubx2/pyrtcm 同系

一句话：`pynmea2` = **星标高、依赖少的 NMEA 解析器**；新项目若已在 pygnssutils 生态，优先 pynmeagps。

| 术语 | 含义 |
| --- | --- |
| `talker` | `$GP`/`$GN`/… 两字母 |
| `sentence_type` | `GGA`/`RMC`/… |
| `latitude`/`longitude` | 十进制度 `float`（南/西为负） |
| `gps_qual` / `num_sats` | GGA 质量（`int`）与卫星数（**`str`**，如 `'06'`） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
pip install 'pynmea2==1.19.0'
python -c "import importlib.metadata as m, pynmea2; print(m.version('pynmea2'), pynmea2.__version__)"
# 期望：1.19.0 1.19.0

# 可选：对齐 tip 跑单测
git clone --depth 1 https://github.com/Knio/pynmea2.git ~/iono_ops/pynmea2
cd ~/iono_ops/pynmea2 && git rev-parse --short HEAD   # fcd90dc
pip install pytest
PYTHONPATH=. python -m pytest -q
# 105 passed
```

## 3. 端到端（本机真跑；2026-09-24 06:04 EDT）

### 3.1 经典样句（对齐 [minmea](./minmea.md)）

```bash
python - <<'PY'
import pynmea2
rmc = pynmea2.parse(
    "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
)
print(rmc.sentence_type, rmc.latitude, rmc.longitude, rmc.spd_over_grnd, rmc.true_course, rmc.datestamp)
gga = pynmea2.parse(
    "$GPGGA,123204.00,5106.94086,N,01701.51680,E,1,06,3.86,127.9,M,40.5,M,,*51"
)
print(gga.sentence_type, gga.latitude, gga.longitude, gga.gps_qual, gga.num_sats, gga.horizontal_dil, gga.altitude)
PY
```

**本机：** RMC **48.1173** / **11.516666666666667** / speed **22.4** / course **84.4** / date **1994-03-23**；GGA **51.115681** / **17.02528** / qual **1** / sats **06** / HDOP **3.86** / alt **127.9**。

### 3.2 北京样句（与 [gpsd](./gpsd.md)/[minmea](./minmea.md) 同源）

```bash
python - <<'PY'
import pynmea2
from pathlib import Path
path = Path.home() / "iono_ops/gpsd-demo/demo_beijing.nmea"
for line in path.read_text().splitlines()[:3]:
    m = pynmea2.parse(line)
    print(m.talker, m.sentence_type, getattr(m, "latitude", None),
          getattr(m, "longitude", None), getattr(m, "gps_qual", None),
          getattr(m, "num_sats", None), getattr(m, "altitude", None), m.is_valid)
PY
```

**本机（首条 RMC / 次条 GGA）：** talker **`GN`**；RMC lat=**39.90418716666667** lon=**116.39074266666667** spd=**0.1**；GGA qual=**1** sats=**12** alt=**44.0** geo_sep=**−8.0**；`is_valid=True`。

### 3.3 逐行读文件 + 构造回写

```bash
python - <<'PY'
import pynmea2
from pathlib import Path

path = Path.home() / "iono_ops/gpsd-demo/demo_beijing.nmea"
n, types = 0, []
for line in path.read_text().splitlines():
    if not line.startswith("$"):
        continue
    m = pynmea2.parse(line)
    n += 1
    types.append(m.sentence_type)
print("n", n, "unique", sorted(set(types)))

msg = pynmea2.GGA(
    "GP", "GGA",
    ("123519", "4807.038", "N", "01131.000", "E", "1", "08", "0.9", "545.4", "M", "46.9", "M", "", ""),
)
s = str(msg)
print(s)
print(pynmea2.parse(s).latitude, pynmea2.parse(s).longitude)
PY
```

**本机：** **n=36**（12×`RMC`+`GGA`+`GSA`）；构造句 **`$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47`**；回读 lat=**48.1173** lon=**11.516666666666667**。

流式也可用 `NMEAStreamReader`（本机同文件亦得 **36** 句）；逐行 `parse` 更直观。

### 3.4 坏校验和

```bash
python - <<'PY'
import pynmea2
try:
    pynmea2.parse("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*00")
except pynmea2.ChecksumError as e:
    print(type(e).__name__, e)
PY
```

**本机：** `ChecksumError ('checksum does not match: 00 != 47', …)`。

## 4. I/O 与关键参数

| 接口 | 作用 |
| --- | --- |
| `parse(data, check=True)` | 一句 → `NMEASentence`；可关校验 |
| `NMEAStreamReader(stream, errors='raise'\|'yield'\|'ignore')` | 流式 |
| `msg.latitude` / `.longitude` | 十进制度 |
| `str(msg)` / `msg.render()` | 序列化（补校验和） |
| 类型类 `pynmea2.GGA`/`RMC`/… | 构造；字段为 NMEA 原始元组 |

## 5. 接到哪步

```text
接收机/文件 NMEA
  → pynmea2.parse / NMEAStreamReader
  → 坐标/质检字段
  → 需要 UBX/RTCM 同栈 → 改 pynmeagps/pyubx2/pyrtcm
  → 系统多客户端 → gpsd
  → 嵌入式无 Python → minmea
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 与 pynmeagps API 混用 | 两套对象模型 | 选定一条栈；本目录新流优先 [pynmeagps](./pynmeagps.md) |
| 2 | `num_sats` / `horizontal_dil` / `geo_sep` 是 `str`（`'06'`、`'3.86'`、`'-8.0'`） | GGA 类只给 `gps_qual`(int)、`altitude`(float) 声明了类型 | `int(msg.num_sats)`、`float(msg.horizontal_dil)`；看 `pynmea2/types/talker.py` 的 `fields` |
| 3 | `ChecksumError` | `*CS` 错 | 修源数据；或 `parse(..., check=False)`（慎） |
| 4 | `NMEAStreamReader` EOF 难写 | `next()` 空列表≠一定结束 | 优先逐行 `parse`；流式自测 EOF |
| 5 | 无 CLI | 库项目 | 自己写 5 行脚本 |
| 6 | proprietary 句失败 | 未覆盖厂商方言 | 看 `types/proprietary/`；或换 pynmeagps `userdefined` |
| 7 | Py2 文档残留 | README 仍写 2.7 | 生产用 3.10+；本机 3.13 OK |
| 8 | `datetime.utcfromtimestamp` 警告 | 旧 proprietary 路径（Nor） | 单测 105 仍过；勿当解析失败 |
| 9 | 把 lat 字段当十进制度 | 原始 `msg.lat` 是 `ddmm.mmmm` 字符串 | 用 `.latitude` |
| 10 | 与 gpsd JSON 比字段名 | 两套命名 | GGA↔TPV 自行映射 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 少依赖、经典 NMEA 解析 | **pynmea2（本文）** |
| 与 pyubx2/pyrtcm/pygpsclient 同系 | [pynmeagps](./pynmeagps.md) |
| 嵌入式纯 C | [minmea](./minmea.md) |
| 多客户端守护 / JSON | [gpsd](./gpsd.md) |
| NTRIP+多协议 CLI | [pygnssutils](./pygnssutils.md) |

相关：[pynmeagps](./pynmeagps.md) · [minmea](./minmea.md) · [gpsd](./gpsd.md) · [pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · [pyubx2](./pyubx2.md)
