# pynmeagps · NMEA 0183 编解码库操作手册

目录：[`PROJECTS.json` → `pynmeagps`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pynmeagps> · 文档 <https://www.semuconsulting.com/pynmeagps/> · PyPI **`pynmeagps` 1.1.7** · tip **`4322c38`** · BSD-3-Clause · Python ≥3.9 · 本机验证 1.1.7（生成 GGA → `NMEAReader.parse` 回读；坏校验和 / 未知专有句）· 2026-09-24 04:31 EDT · **质检复跑通过**（1.1.7/`4322c38`；`$GNGGA…*5D` 往返；文件流 3×GNGGA q=1,1,2）

> 岗位：纯 Python **解析/生成 NMEA 0183**（GET/SET/POLL）。冲突时：**上游 README / Sphinx / 本机 `help(NMEAReader)` > 本文**。串口/NTRIP 流 CLI → [pygnssutils](./pygnssutils.md)；桌面 GUI → [pygpsclient](./pygpsclient.md)。同系还有 `pyubx2` / `pyrtcm`（本目录未单列时见上游）。

## 1. 用途与边界

**做：**

- 流式读串口/文件/套接字中的 `$GNxxx,*CS` 句；迭代 `NMEAReader`
- 构造 `NMEAMessage` 并 `serialize()` 生成标准/常见专有句
- 校验和验证、未知 msgId 策略、用户自定义 payload 字典
- 给 [pygpsclient](./pygpsclient.md) / [pygnssutils](./pygnssutils.md) 当 NMEA 底层（后两者 `pip` 时常已拉上本库）

**不做：**

- **不是** UBX/RTCM 编解码 → `pyubx2` / `pyrtcm`（或捆在 pygnssutils 流里）
- **不是** 定位滤波 / PPP / TEC → [rtklib](./rtklib.md) / [pytecgg](./pytecgg.md)
- **不是** 多流运维 GUI → [bnc](./bnc.md)
- **不是** 保证吃下所有厂商私有方言；缺定义时要自己补 `userdefined`

一句话：pynmeagps = **NMEA 句子的结构化读写**；电离层产品在「录流 → RINEX/观测」之后。

| 符号 | 含义 |
| --- | --- |
| `GET` / `SET` / `POLL` | 接收机输出 / 主机下发 / 查询（`msgmode` 0/1/2） |
| `NMEAReader` | 流包装：`read()` 或 `for raw, msg in reader` |
| `NMEAMessage` | 一句的属性包；`identity` 如 `GNGGA` |
| `VALCKSUM` / `VALMSGID` | 校验和 / 已知 msgId 校验位标志 |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip pynmeagps
python -c "import importlib.metadata as m; print(m.version('pynmeagps'))"
# 期望：1.1.7
# 若已装 PyGPSClient / pygnssutils，多半已有本库：
python -c "import pynmeagps, pygnssutils; print(pynmeagps.__file__)"
```

conda：`conda install -c conda-forge pynmeagps`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pynmeagps'` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| 与文档 API 不符 | 钉死了旧版 | `pip install -U 'pynmeagps>=1.1.7'` |
| 只有 `pyubx2` 想读 NMEA | 栈分层 | `pip install pynmeagps`（或直接装 pygnssutils） |

## 3. 端到端（本机 1.1.7 真跑）

### 3.1 生成 → 回读

```bash
python - <<'PY'
from pynmeagps import NMEAMessage, NMEAReader, GET

gga = NMEAMessage(
    "GN", "GGA", GET,
    time="12:35:19", lat=39.9041871667, NS="N",
    lon=116.3907426667, EW="E", quality=1, numSV=12,
    HDOP=0.9, alt=44.0, altUnit="M", sep=-18.0, sepUnit="M",
)
raw = gga.serialize()
print(raw.decode().rstrip())
msg = NMEAReader.parse(raw)          # 注意：1.1.x 直接返回 NMEAMessage
print(msg.identity, msg.lat, msg.lon, msg.quality, msg.numSV, msg.alt)
assert msg.lat == 39.9041871667 and msg.quality == 1
print("roundtrip OK", NMEAReader.parse(msg.serialize()).lat == msg.lat)
PY
```

**本机 stdout：**

```text
$GNGGA,123519,3954.25123,N,11623.44456,E,1,12,0.9,44.0,M,-18.0,M,0.0,0*5D
GNGGA 39.9041871667 116.3907426667 1 12 44.0
roundtrip OK True
```

### 3.2 文件流迭代

```bash
python - <<'PY'
from pynmeagps import NMEAMessage, NMEAReader, GET
from pathlib import Path

lines = []
for t, lat, lon, q in [
    ("12:35:19", 39.9041871667, 116.3907426667, 1),
    ("12:35:20", 39.9041873333, 116.3907428333, 1),
    ("12:35:21", 39.9041875, 116.390743, 2),
]:
    m = NMEAMessage("GN", "GGA", GET, time=t, lat=lat, NS="N", lon=lon, EW="E",
                    quality=q, numSV=12, HDOP=0.9, alt=44.0, altUnit="M",
                    sep=-18.0, sepUnit="M")
    lines.append(m.serialize())
path = Path.home() / "iono_ops/pynmea_e2e/demo.nmea"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(b"".join(lines))

with path.open("rb") as fh:
    for i, (raw, msg) in enumerate(NMEAReader(fh), 1):
        print(i, msg.identity, msg.lat, msg.quality)
PY
```

**期望：** 三行 `GNGGA`，`quality` 为 1,1,2。接 CLI 回放：`gnssstreamer --filename ~/iono_ops/pynmea_e2e/demo.nmea --verbosity 2`（见 [pygnssutils](./pygnssutils.md)）。

### 3.3 校验和与未知专有句

```bash
python - <<'PY'
from pynmeagps import NMEAReader, NMEAParseError
from pynmeagps.nmeatypes_core import VALCKSUM, VALMSGID
from pynmeagps.nmeahelpers import calc_checksum

bad = b"$GNGGA,123519,3954.2513,N,11623.4446,E,1,12,0.9,44.0,M,-18.0,M,,*00\r\n"
try:
    NMEAReader.parse(bad)
except NMEAParseError as e:
    print("badck", e)

body = "PXYZ,1,2,3"
prop = f"${body}*{calc_checksum(body)}\r\n".encode()
try:
    NMEAReader.parse(prop, validate=VALCKSUM | VALMSGID)
except NMEAParseError as e:
    print("unknown", e)
print("nocheckid", NMEAReader.parse(prop, validate=VALCKSUM))
PY
```

**本机：**

```text
badck Message GNGGA invalid checksum 00 - should be 44.
unknown Unknown msgID PXYZ, msgmode GET.
nocheckid <NMEA(PXYZ, NOMINAL, field_01=1, field_02=2, field_03=3)>
```

长期专有句：用上游「user-defined payload」字典注册，而不是永远 `VALCKSUM` only。

### 3.4 串口（有硬件时）

```python
from serial import Serial
from pynmeagps import NMEAReader
with Serial("/dev/ttyACM0", 9600, timeout=3) as stream:
    nmr = NMEAReader(stream)
    raw, parsed = nmr.read()
    print(parsed)
```

无头自动化优先 [pygnssutils](./pygnssutils.md) `gnssstreamer`；本库适合嵌进自有脚本。

## 4. I/O 与关键参数

| API | 作用 |
| --- | --- |
| `NMEAReader(stream, msgmode=0, validate=VALCKSUM, nmeaonly=False, …)` | 包装二进制流 |
| `NMEAReader.parse(bytes)` | 单句解析 → `NMEAMessage` |
| `NMEAMessage(talker, msgID, msgmode, **payload)` | 构造 |
| `msg.serialize()` | → `bytes`（含 `$`/`*`/校验和/`\r\n`） |
| `calc_checksum(body)` | 对 `$` 与 `*` 之间文本算异或校验 |

| `validate` 位 | 含义 |
| --- | --- |
| `VALCKSUM` (1) | 校验和错误 → `NMEAParseError` |
| `VALMSGID` (2) | 未知 msgId → `NMEAParseError` |

经纬度属性在库内用**十进制度**；序列化时自动写成 NMEA `ddmm.mmmm`。

## 5. 接到哪步

```text
接收机 UART/TCP
  →（库）pynmeagps 解析 NMEA
  →（CLI）pygnssutils gnssstreamer 录流/过滤
  →（GUI）pygpsclient 监视
  → 要 RINEX/UBX RAW → pyrinexconv / 厂商工具 → georinex / pytecgg
```

同系交叉：[pygpsclient](./pygpsclient.md) · [pygnssutils](./pygnssutils.md)。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `TypeError: cannot unpack non-iterable NMEAMessage` | 1.1.x `parse` 不再返回 `(raw,msg)` | `msg = NMEAReader.parse(b)` 单返回值 |
| 2 | `NMEAParseError: … invalid checksum` | 截断行/日志被改过 | 保留 `\r\n`；或先修源再降 `validate` |
| 3 | `Unknown msgID …` | 厂商专有句未登记且开了 `VALMSGID` | `validate=VALCKSUM` 临时放行；或加 `userdefined` |
| 4 | `lat`/`lon` 为 `None` | 该句无位置字段（如纯 `GSA`） | `getattr(msg,"lat",None)`；按 `identity` 分支 |
| 5 | 生成的 RMC 含字面 `None` | 可选字段传了 Python `None` | 空字段用 `""` 或省略 kwargs |
| 6 | 串口迭代卡死 | 波特率/口错；二进制 UBX 当 NMEA | 对一下波特率；`nmeaonly=False` 或改 pyubx2 |
| 7 | 与 PyGPSClient 版本漂移 | 传递依赖未升级 | `pip install -U pynmeagps PyGPSClient pygnssutils` |
| 8 | 把 NMEA `quality` 当固定解置信度 | quality 语义因固件而异 | 仍以接收机 UBX/厂商状态为准 |
| 9 | 多句粘连解析失败 | 按行拆时丢了 `*` 后校验 | 整帧交给 `NMEAReader` 流式读 |
| 10 | 期望本库算 TEC/PPP | 职责仅编解码 | 观测落盘后走 [georinex](./georinex.md)/[rtklib](./rtklib.md) |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本里读写 NMEA | **pynmeagps（本文）** |
| 同栈 CLI 拉流/NTRIP | [pygnssutils](./pygnssutils.md) |
| 桌面监视/配置板卡 | [pygpsclient](./pygpsclient.md) |
| UBX 二进制 | `pyubx2`（上游同作者） |
| RTCM3 | `pyrtcm` |
| 多流录盘 | [bnc](./bnc.md) |

相关：上游 README · Sphinx · [pygpsclient](./pygpsclient.md) · [pygnssutils](./pygnssutils.md) · [android_rinex](./android_rinex.md) · 教程 [06](../tutorials/06-iono-positioning.md)
