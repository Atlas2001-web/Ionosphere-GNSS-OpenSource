# pysbf2 · Septentrio SBF 纯 Python 编解码操作手册

目录：[`PROJECTS.json` → `pysbf2`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pysbf2> · 文档 <https://www.semuconsulting.com/pysbf2/> · PyPI **`pysbf2` 1.0.5** · tip **`a68fe44`** · BSD-3-Clause · Python ≥3.10 · 本机验证 1.0.5（构造 `PVTCartesian` 往返；上游 `tests/pygpsdata_x5_*.log` / `examples/sbfdata.log`；混流 NMEA+RTCM；`SBF_MSGIDS`=**125**；**无 ISM***）· 2026-09-24 05:10 EDT

> 岗位：纯 Python **解析/生成 Septentrio SBF**（并可经依赖拆混流中的 NMEA / RTCM3）。冲突时：**上游 README / Sphinx / 本机 `help(SBFReader)` > 本文**。官方 Cython 快路径 → [sbfparser](./sbfparser.md)；HAS 页→SSR → [haslib](./haslib.md)；u-blox 对照 → [pyubx2](./pyubx2.md)。**本包无 CLI entry point**（流 CLI → [pygnssutils](./pygnssutils.md) `gnssstreamer`）。

## 1. 用途与边界

**做：**

- 流式读文件/串口/套接字中的 `$@`（`24 40`）SBF 帧；迭代 `SBFReader`
- 单帧 `SBFReader.parse(bytes)` → `SBFMessage`；`serialize()` 写回带 CRC 的完整帧
- 构造消息：`SBFMessage("PVTCartesian", TOW=…, WNc=…, …)`（测试注入 / 假接收机）
- `protfilter` 混读 NMEA / RTCM3（底层 [pynmeagps](./pynmeagps.md) / [pyrtcm](./pyrtcm.md)）
- 码表：`SBF_MSGIDS`（本机 **125**）；属性译码 `sbftypes_decodes.PVT_TYPE` / `SIGNAL_TYPE` 等
- 同作者栈：与 [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pynmeagps](./pynmeagps.md) / [pyspartn](./pyspartn.md) API 同型

**不做：**

- **不是** 官方 Cython 高性能块表 → [sbfparser](./sbfparser.md)（对比：pysbf2 = **纯 Python 同栈编解码**；sbf-parser = **官方生态、仓内大样例**）
- **不是** Galileo HAS 拼页/SSR → [haslib](./haslib.md)（本库只拆出 `GALRawCNAV` 等）
- **不是** ISMR/S4/σφ 产品；`SBF_MSGIDS` **无 `ISM*`**（与 sbfparser tip 同缺口）
- **不是** NTRIP/串口运维 CLI → [pygnssutils](./pygnssutils.md)；**不是** RINEX/PPP/TEC

一句话：pysbf2 = **SBF 二进制的结构化读写（semuconsulting 栈）**；电离层产品在抽块 / 转观测之后。

| 符号 | 含义 |
| --- | --- |
| `SBFReader` | 流包装：`read()` 或 `for raw, msg in reader` |
| `SBFMessage` | 一帧属性包；`identity` 如 `PVTCartesian`、`ReceiverStatus`、`GALRawCNAV` |
| `TOW` / `WNc` | 周内 **ms**（`int`；`str(msg)` 常印成 `HH:MM:SS`）/ GPS 连续周 |
| `Type`（PVT） | PVT 模式码；`PVT_TYPE[6]=='SBAS aided PVT'` |
| `protfilter` | `NMEA_PROTOCOL` (1) \| `SBF_PROTOCOL` (2) \| `RTCM3_PROTOCOL` (4)；默认 7 |
| `VALCKSUM` | CRC 校验（默认开） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip 'pysbf2>=1.0.5'
python - <<'PY'
import importlib.metadata as m
print(m.version('pysbf2'), m.version('pynmeagps'), m.version('pyrtcm'))
print(list(m.distribution('pysbf2').entry_points))
PY
# 期望：
# 1.0.5 1.1.7 1.2.0
# []
```

源码（样例日志在仓内 `tests/` / `examples/`）：

```bash
git clone --depth 1 https://github.com/semuconsulting/pysbf2.git
cd pysbf2 && git rev-parse --short HEAD   # 期望：a68fe44
```

conda：`conda install -c conda-forge pysbf2`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pysbf2'` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| `python -m pysbf2` 失败 | 无 `__main__` / 无 console script | 用库 API；CLI 用 `gnssstreamer` |
| 与文档 API 不符 | 钉死了旧版 | `pip install -U 'pysbf2>=1.0.5'` |

## 3. 端到端（本机 1.0.5 真跑）

**本机无 Septentrio 接收机**：下列全部用构造字节 + 上游仓内 `tests/`、`examples/` 真跑，**禁止**臆造 stdout。有串口时见 §3.5。路径相对克隆根（如 `~/iono_ops/pysbf2`）。

### 3.1 构造 → parse 往返（`PVTCartesian`）

```bash
python - <<'PY'
from pysbf2 import SBFMessage, SBFReader
from pysbf2.sbftypes_decodes import PVT_TYPE
from pysbf2.sbftypes_core import SBF_MSGIDS

msg = SBFMessage(
    "PVTCartesian",
    TOW=208903000, WNc=2367, Type=4, Error=0,
    X=3803640.1823747293, Y=-148797.3625715144, Z=5100642.783697508,
    Undulation=48.466453552246094, NrSV=16,
    Latency=43, HAccuracy=122, VAccuracy=136,
)
raw = msg.serialize()
back = SBFReader.parse(raw)
print(msg.identity, msg.TOW, msg.WNc, msg.Type, PVT_TYPE[msg.Type])
print(round(msg.X, 4), msg.NrSV, len(raw), raw[:8].hex())
print("roundtrip", back.serialize() == raw)
print("SBF_MSGIDS", len(SBF_MSGIDS))
PY
```

期望（本机）：

```
PVTCartesian 208903000 2367 4 RTK with fixed ambiguities
3803640.1824 16 96 24400686a60f6000
roundtrip True
SBF_MSGIDS 125
```

### 3.2 读上游 PVT 样例

```bash
python - <<'PY'
from pysbf2 import SBFReader
from pysbf2.sbfreader import SBF_PROTOCOL
from pysbf2.sbftypes_decodes import PVT_TYPE

with open("tests/pygpsdata_x5_pvtcart.log", "rb") as stream:
    ids = []
    pvt = None
    for raw, parsed in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if parsed is None:
            continue
        ids.append(parsed.identity)
        if pvt is None and parsed.identity == "PVTCartesian":
            pvt = parsed
print(ids)
print(pvt.TOW, pvt.WNc, pvt.Type, PVT_TYPE[pvt.Type])
print(pvt.X, pvt.Y, pvt.Z, pvt.NrSV, pvt.Latency)
PY
```

期望：

```
['PVTCartesian', 'PosCovCartesian', 'VelCovCartesian', 'BaseVectorCart']
482621000 2367 6 SBAS aided PVT
3813176.3935078024 -149599.1631026641 5093600.012439784 36 61
```

`str(pvt)` 里 `TOW=14:03:23` 只是打印格式；属性 `pvt.TOW` 仍是 **ms** 整数。

### 3.3 `ReceiverStatus` / 大地坐标 / 原始导航

```bash
python - <<'PY'
from collections import Counter
from math import degrees
from pysbf2 import SBFReader
from pysbf2.sbfreader import SBF_PROTOCOL

with open("tests/pygpsdata_x5_status.log", "rb") as stream:
    c = Counter(); rs = None
    for raw, p in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if p is None:
            continue
        c[p.identity] += 1
        if p.identity == "ReceiverStatus":
            rs = p
print(dict(c))
print(rs.TOW, rs.WNc, rs.CPULoad, rs.UpTime, rs.Temperature, rs.N)

with open("tests/pygpsdata_x5_pvtgeod.log", "rb") as stream:
    for raw, p in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if p and p.identity == "PVTGeodetic":
            print(p.TOW, p.Type, degrees(p.Latitude), degrees(p.Longitude), p.Height, p.NrSV)
            break

with open("tests/pygpsdata_x5_rawnav.log", "rb") as stream:
    c = Counter(); gal = None
    for raw, p in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if p is None:
            continue
        c[p.identity] += 1
        if p.identity == "GALRawCNAV":
            gal = (p.TOW, p.SVID, p.CRCPassed, p.SigIdx, len(raw))
print(dict(c))
print("GALRawCNAV", gal)

with open("tests/pygpsdata_x5_measurements.log", "rb") as stream:
    for raw, p in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if p and p.identity == "MeasEpoch":
            print("MeasEpoch", p.TOW, p.WNc, p.N1)
            break
PY
```

期望（摘要）：

```
{'ChannelStatus': 1, 'SatVisibility': 1, 'InputLink': 1, 'OutputLink': 1, 'ReceiverStatus': 1, 'QualityInd': 1, 'NTRIPClientStatus': 1, 'NTRIPServerStatus': 1, 'DiskStatus': 1, 'RFStatus': 1, 'DynDNSStatus': 1, 'P2PPStatus': 1, 'GALAuthStatus': 1}
483170000 2367 28 1365 154 8
482847000 6 53.34405249154133 -2.246685985695232 131.18596542546626 36
{'GALRawINAV': 1, 'GEORawL1': 1, 'BDSRaw': 1, 'GLORawCA': 1, 'GPSRawCA': 1, 'GALRawFNAV': 1, 'NAVICRaw': 1, 'GPSRawL2C': 1, 'GALRawCNAV': 1}
GALRawCNAV (136900000, 128, 1, 24, 52)
MeasEpoch 482321000 2367 44
```

`Latitude`/`Longitude` 为 **弧度**（上表已 `degrees()`）。

### 3.4 混流 + `examples/sbfdata.log`

```bash
python - <<'PY'
from collections import Counter
from pysbf2 import SBFReader
from pysbf2.sbfreader import SBF_PROTOCOL, NMEA_PROTOCOL, RTCM3_PROTOCOL

with open("tests/pygpsdata_mixed.log", "rb") as stream:
    r = SBFReader(stream, protfilter=SBF_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL)
    print([(type(p).__name__, p.identity) for _, p in r if p])

c = Counter(); n = 0; first = None
with open("examples/sbfdata.log", "rb") as stream:
    for raw, p in SBFReader(stream, protfilter=SBF_PROTOCOL):
        if p is None:
            continue
        n += 1
        c[p.identity] += 1
        if first is None:
            first = p
print(n, dict(c))
print(first.TOW, first.Type, first.X, first.NrSV)
PY
```

期望：

```
[('NMEAMessage', 'GNGLL'), ('RTCMMessage', '1005'), ('RTCMMessage', '1230'), ('NMEAMessage', 'GNRMC'), ('SBFMessage', 'PVTGeodetic'), ('SBFMessage', 'PosLocal')]
232 {'PVTCartesian': 58, 'PosCovCartesian': 58, 'VelCovCartesian': 58, 'BaseVectorCart': 58}
218303000 1 3803640.7362816357 15
```

### 3.5 有串口时（本机未跑）

```python
from serial import Serial
from pysbf2 import SBFReader, SBF_PROTOCOL, NMEA_PROTOCOL
with Serial("/dev/ttyACM0", 115200, timeout=3) as stream:
    for raw, parsed in SBFReader(stream, protfilter=SBF_PROTOCOL | NMEA_PROTOCOL):
        print(parsed)
```

## 4. I/O 与关键参数

| API | 输入 | 输出 |
| --- | --- | --- |
| `SBFReader(stream, …)` | 支持 `read(n)` 的流 | 迭代 `(raw:bytes, parsed)` |
| `SBFReader.parse(data)` | 完整一帧 `bytes` | `SBFMessage` / NMEA / RTCM |
| `SBFMessage(identity, **fields)` | 块名 + 字段 | 对象；`.serialize()` → 帧 |
| `SBF_MSGIDS` | — | `{块号: (名, 说明)}`，本机 **125** |
| `PVT_TYPE[n]` | PVT `Type` | 人话模式串 |

| kwargs | 含义 |
| --- | --- |
| `protfilter` | 协议位掩码；只要 SBF 用 `SBF_PROTOCOL` |
| `validate` | `VALCKSUM`(默认) / `VALNONE` |
| `quitonerror` | `ERR_IGNORE` / `ERR_LOG`(默认) / `ERR_RAISE` |
| `parsebitfield` | 1=拆 bit 标志（默认）；0=保留字节序列 |

## 5. 接到哪步

| 上下游 | 接法 |
| --- | --- |
| [sbfparser](./sbfparser.md) | 官方 Cython / 仓内大 `.sbf`；本库偏 **同栈脚本与生成** |
| [haslib](./haslib.md) | 本库确认 `GALRawCNAV` → haslib → [cssrlib](./cssrlib.md)/[rtklib](./rtklib.md) |
| [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pynmeagps](./pynmeagps.md) | 同作者 API；**勿把 UBX 字节丢进 SBFReader** |
| [pygnssutils](./pygnssutils.md) | 录流/NTRIP CLI；解码仍可用本库 |
| 闪烁 / TEC | [ismr-downloader](./ismr-downloader.md) / [oasis-roti](./oasis-roti.md) / [pytecgg](./pytecgg.md)（本库不产指数） |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `python -m pysbf2` / `pysbf2:` not found | **无 CLI** | 库 API；流用 `gnssstreamer` |
| 2 | `Mode=1` 构造后无 `.Mode` | PVT 字段是 **`Type`**（及 bit 拆出的 `AutoSet`/`2D`） | 用 `Type=`；译码 `PVT_TYPE` |
| 3 | `str(msg)` 的 `TOW=14:03:23` 当秒用 | 仅显示格式 | 用 `msg.TOW`（ms `int`） |
| 4 | `Lat`/`Lon` AttributeError | 字段名 **`Latitude`/`Longitude`** | 且单位是 **rad** |
| 5 | 文件帧 `parse` 后再 `serialize` ≠ 原字节 | ID 字 **revision nibble** 重写（本机 `4f→0f`） | 保原 `raw`；构造帧往返仍 OK |
| 6 | 指望 `ISM*` / 4086 | `SBF_MSGIDS` **无 ISM** | 同 [sbfparser](./sbfparser.md)；ISMR 走下载器 |
| 7 | 混流只见 SBF | `protfilter` 未 OR NMEA/RTCM | `SBF_PROTOCOL \| NMEA_PROTOCOL \| RTCM3_PROTOCOL` |
| 8 | 与 sbf-parser 字典键不一致 | 两套模型（属性 vs dict） | 选一栈；对照块名/`TOW` |
| 9 | `COG=-20000000000.0` | SBF Do-Not-Use 哨兵 | 按手册过滤无效值 |
| 10 | 依赖版本飘 | 未钉 `pynmeagps`/`pyrtcm` | 本机：pysbf2 1.0.5 + pynmeagps 1.1.7 + pyrtcm 1.2.0 |

## 7. 选型与链接

| 你要… | 用 |
| --- | --- |
| 纯 Python、与 pyubx2/pyrtcm 同栈、可生成 | **本文 pysbf2** |
| 官方 Cython、大样例、偏只读解析 | [sbfparser](./sbfparser.md)（`sbf-parser`） |
| 老 GPL SBF 模块 | `pysbf`（维护/许可自审） |
| SBF → HAS SSR | [haslib](./haslib.md) |
| UBX / RTCM3 / NMEA | [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pynmeagps](./pynmeagps.md) |
| 录流 CLI | [pygnssutils](./pygnssutils.md) |

- 上游：<https://github.com/semuconsulting/pysbf2>
- PyPI：<https://pypi.org/project/pysbf2/>
- Sphinx：<https://www.semuconsulting.com/pysbf2/>
- 兄弟：[sbfparser](./sbfparser.md) · [haslib](./haslib.md) · [pyubx2](./pyubx2.md) · [pyrtcm](./pyrtcm.md) · [pynmeagps](./pynmeagps.md) · [pygnssutils](./pygnssutils.md)
