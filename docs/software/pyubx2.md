# pyubx2 · u-blox UBX 编解码库操作手册

目录：[`PROJECTS.json` → `pyubx2`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pyubx2> · 文档 <https://www.semuconsulting.com/pyubx2/> · PyPI **`pyubx2` 1.3.6** · tip **`4abbfa6`** · BSD-3-Clause · Python ≥3.10 · 本机验证 1.3.6（CFG-MSG / NAV-PVT POLL / ACK-ACK 往返；上游 `tests/pygpsdata-NAV.log` NAV-PVT；`examples/mon_span.ubx` 109 帧）· 2026-09-24 04:45 EDT

> 岗位：纯 Python **解析/生成 UBX**（GET/SET/POLL + Gen9 `CFG-VAL*`）。冲突时：**上游 README / Sphinx / 本机 `help(UBXReader)` > 本文**。串口/NTRIP/录流 CLI → [pygnssutils](./pygnssutils.md)；桌面 GUI → [pygpsclient](./pygpsclient.md)；NMEA 姐妹库 → [pynmeagps](./pynmeagps.md)。**本包无 CLI entry point**（上游 README 的 “CLI” 指向 pygnssutils，旧名 `gnssdump` → 现 `gnssstreamer`）。

## 1. 用途与边界

**做：**

- 流式读串口/文件/套接字中的 `b5 62 …` UBX 帧；迭代 `UBXReader`
- 构造 `UBXMessage` 并 `serialize()`（POLL 查询、SET 配置、GET 模拟接收机输出）
- Gen9 配置库：`UBXMessage.config_set` / `config_del` / `config_poll`（`CFG-VALSET/VALDEL/VALGET`）
- 同作者栈底层：被 [pygpsclient](./pygpsclient.md) / [pygnssutils](./pygnssutils.md) 依赖；`pip` 装后两者时常已拉上本库
- 可选：同一 `UBXReader` 经依赖解析混流中的 NMEA / RTCM3（`protfilter`）

**不做：**

- **不是** NTRIP/串口运维 CLI → [pygnssutils](./pygnssutils.md)（对比：pyubx2 = **编解码**；pygnssutils = **拉流/录盘/小 caster**）
- **不是** 桌面监视/改板卡 GUI → [pygpsclient](./pygpsclient.md)
- **不是** RTCM3 专职库 → `pyrtcm`（本目录未单列时见上游；本库可透传混流）
- **不是** 定位滤波 / PPP / TEC → [rtklib](./rtklib.md) / [pytecgg](./pytecgg.md)；原始量测落盘后另转 RINEX

一句话：pyubx2 = **UBX 二进制的结构化读写**；电离层产品在「录 RAW → RINEX/观测」之后。

| 符号 | 含义 |
| --- | --- |
| `GET` / `SET` / `POLL` | 接收机输出 / 主机下发 / 查询（`msgmode` 0/1/2）；`SETPOLL`(3) 按载荷自动判 SET/POLL |
| `UBXReader` | 流包装：`read()` 或 `for raw, msg in reader` |
| `UBXMessage` | 一帧属性包；`identity` 如 `NAV-PVT`、`CFG-MSG` |
| `VALCKSUM` | 校验和校验（默认开） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip 'pyubx2>=1.3.6'
python -c "import importlib.metadata as m; print(m.version('pyubx2'))"
# 期望：1.3.6
# 依赖会装 pynmeagps、pyrtcm；本包 entry_points 为空（无 pyubx2 命令）
python -c "import importlib.metadata as m; print(list(m.distribution('pyubx2').entry_points))"
# 期望：[]
# 流 CLI 另装：pip install pygnssutils  → gnssstreamer（见 pygnssutils.md）
```

conda：`conda install -c conda-forge pyubx2`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pyubx2'` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| `python -m pyubx2` 失败 | 无 `__main__` / 无 console script | 用库 API；CLI 用 `gnssstreamer` |
| 与文档 API 不符 | 钉死了旧版 | `pip install -U 'pyubx2>=1.3.6'` |

## 3. 端到端（本机 1.3.6 真跑）

### 3.1 构造 → 回读（SET / POLL / ACK）

```bash
python - <<'PY'
from pyubx2 import UBXMessage, UBXReader, GET, SET, POLL

cfg = UBXMessage(
    "CFG", "CFG-MSG", SET,
    msgClass=0x01, msgID=0x07,  # NAV-PVT
    rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0,
)
raw = cfg.serialize()
print(cfg)
print(raw.hex())
back = UBXReader.parse(raw, msgmode=SET)
assert back.serialize() == raw and back.rateUART1 == 1
print("set_roundtrip OK", back.identity, back.rateUART1)

poll = UBXMessage("NAV", "NAV-PVT", POLL)
print(poll, poll.serialize().hex())
assert UBXReader.parse(poll.serialize(), msgmode=POLL).serialize() == poll.serialize()
print("poll_roundtrip OK")

ack = UBXMessage("ACK", "ACK-ACK", GET, clsID=0x06, msgID=0x01)
print(ack, ack.serialize().hex())
a2 = UBXReader.parse(ack.serialize())
print("ack", a2.identity, a2.clsID, a2.msgID)
PY
```

**本机 stdout：**

```text
<UBX(CFG-MSG, msgClass=NAV, msgID=NAV-PVT, rateDDC=0, rateUART1=1, rateUART2=0, rateUSB=0, rateSPI=0, reserved=0)>
b56206010800010700010000000018e1
set_roundtrip OK CFG-MSG 1
<UBX(NAV-PVT)> b562010700000819
poll_roundtrip OK
<UBX(ACK-ACK, clsID=CFG, msgID=CFG-MSG)> b5620501020006010f38
ack ACK-ACK 6 1
```

注意：`UBXMessage("NAV", "PVT", …)` 会报 `Undefined message`——第二参要用字典里的完整 id 名 **`NAV-PVT`**（或直接传 `bytes` class/id）。

### 3.2 上游测试日志：读 NAV-PVT

取自仓内 `tests/pygpsdata-NAV.log`（本机另存后）：

```bash
# 若已 clone 上游：TESTS=.../pyubx2/tests/pygpsdata-NAV.log
python - <<'PY'
from pyubx2 import UBXReader, UBX_PROTOCOL
path = "pygpsdata-NAV.log"  # 换成你的路径
with open(path, "rb") as fh:
    raw, msg = next(iter(UBXReader(fh, protfilter=UBX_PROTOCOL)))
print(msg.identity, msg.lat, msg.lon, msg.numSV, msg.fixType,
      f"{msg.year:04d}-{msg.month:02d}-{msg.day:02d}",
      f"{msg.hour:02d}:{msg.min:02d}:{msg.second:02d}", len(raw))
PY
```

**本机（该样例第一帧）：**

```text
NAV-PVT 53.4507228 -2.2402855 26 3 2021-12-04 11:34:59 100
```

`lat`/`lon` 已是十进制度（库内缩放）；`height`/`hMSL` 为毫米整型。

### 3.3 上游示例二进制：整文件统计

`examples/mon_span.ubx`（本机 11639 B）：

```bash
python - <<'PY'
from collections import Counter
from pyubx2 import UBXReader, UBX_PROTOCOL
with open("mon_span.ubx", "rb") as fh:
    ids = Counter(p.identity for _, p in UBXReader(fh, protfilter=UBX_PROTOCOL))
print(sum(ids.values()), len(ids), ids["MON-SPAN"], ids["NAV-PVT"], ids["HNR-PVT"])
PY
```

**本机：** `109` 帧、多类 CFG/NAV/MON；其中 `MON-SPAN=7`，`NAV-PVT=1`，`HNR-PVT=13`。接 CLI 回放：`gnssstreamer --filename mon_span.ubx --protfilter 2 --verbosity 2`（见 [pygnssutils](./pygnssutils.md)）。

### 3.4 Gen9 CFG-VALSET + 坏校验和

```bash
python - <<'PY'
from pyubx2 import UBXMessage, UBXReader, SET

msg = UBXMessage.config_set(1, 0, [("CFG_MSGOUT_UBX_NAV_PVT_USB", 1)])  # layers=1 → RAM
print(msg)
print(msg.serialize().hex())
print(UBXReader.parse(msg.serialize(), msgmode=SET).CFG_MSGOUT_UBX_NAV_PVT_USB)

ack = UBXMessage("ACK", "ACK-ACK", 0, clsID=0x06, msgID=0x01)
bad = bytearray(ack.serialize()); bad[-1] ^= 0xFF
try:
    UBXReader.parse(bytes(bad))
except Exception as e:
    print("badck", e)
PY
```

**本机：**

```text
<UBX(CFG-VALSET, version=0, ram=1, bbr=0, flash=0, action=0, reserved0=0, CFG_MSGOUT_UBX_NAV_PVT_USB=1)>
b562068a09000001000009009120015552
1
badck Message checksum b'\x0f\xc7' invalid - should be b'\x0f8'
```

`layers=0` 时 `ram/bbr/flash` 全 0，接收机常忽略——写配置务必显式置层。

### 3.5 串口（有硬件时）

```python
from serial import Serial
from pyubx2 import UBXReader, UBX_PROTOCOL, NMEA_PROTOCOL
with Serial("/dev/ttyACM0", 38400, timeout=3) as stream:
    ubr = UBXReader(stream, protfilter=UBX_PROTOCOL | NMEA_PROTOCOL)
    raw, parsed = ubr.read()
    print(parsed)
```

无头自动化优先 [pygnssutils](./pygnssutils.md) `gnssstreamer`；本库适合嵌进自有脚本与单元测试桩。

## 4. I/O 与关键参数

| API | 作用 |
| --- | --- |
| `UBXReader(stream, protfilter=7, msgmode=GET, validate=VALCKSUM, …)` | 包装二进制流 |
| `UBXReader.parse(bytes, msgmode=GET)` | 单帧解析 → `UBXMessage` |
| `UBXMessage(cls, id, mode, **payload)` | 构造；`cls`/`id` 可为名或 `bytes` |
| `msg.serialize()` | → `bytes`（含同步字 `b5 62`、长度、校验） |
| `UBXMessage.config_set(layers, transaction, cfgData)` | → `CFG-VALSET` |
| `config_del` / `config_poll` | 删键 / 读键 |

| `protfilter` 位 | 协议 |
| --- | --- |
| 1 | NMEA（依赖 pynmeagps） |
| 2 | UBX |
| 4 | RTCM3（依赖 pyrtcm） |

经纬度在 NAV-PVT 等消息上已是浮点度；毫米高度勿当米用。

## 5. 接到哪步

```text
u-blox UART/TCP/.ubx 日志
  →（库）pyubx2 解析/下发 UBX
  →（CLI）pygnssutils gnssstreamer 录流/过滤
  →（GUI）pygpsclient 监视/改配置
  → RAW→RINEX（pyrinexconv / 厂商工具）→ georinex / pytecgg / rtklib
```

同系交叉：[pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · [pynmeagps](./pynmeagps.md)。RTCM 专职见上游 `pyrtcm`。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Undefined message, class NAV, id PVT` | id 字符串要用 `NAV-PVT` 全名 | `UBXMessage("NAV","NAV-PVT",…)` 或传 `b"\x01\x07"` |
| 2 | `Unknown message type … mode SET` | 用错 `msgmode` 读 GET 流 | 读接收机输出用默认 `GET`；仅解析主机命令时用 `SET`/`POLL`/`SETPOLL` |
| 3 | `Message checksum … invalid` | 截断/改写/粘包 | 整帧交给 `UBXReader`；临时 `validate=0` 仅调试 |
| 4 | `CFG-VALSET` 无效果 | `layers=0` 未选 RAM/BBR/Flash | `config_set(1,0,[…])` 至少置 RAM |
| 5 | `lat` 为 `None` | 该 identity 无位置字段 | `getattr(msg,"lat",None)`；按 `identity` 分支 |
| 6 | 串口全是 NMEA 解不出 UBX | 未开 UBX 输出或波特率错 | 先发 `CFG-MSG`/`CFG-VALSET`；对波特率；`protfilter` 含 NMEA |
| 7 | 期望 `python -m pyubx2` / `ubxdump` | 本包无 CLI | `pip install pygnssutils` → `gnssstreamer` |
| 8 | 与 PyGPSClient 字段漂移 | 传递依赖未升级 | `pip install -U pyubx2 PyGPSClient pygnssutils` |
| 9 | `height=91184` 当 91 km | 单位是 mm | `/1000` 得米；对照 `hMSL` |
| 10 | 把本库当 TEC/PPP 引擎 | 职责仅编解码 | 观测落盘后走 [georinex](./georinex.md)/[rtklib](./rtklib.md) |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本里读写 UBX | **pyubx2（本文）** |
| 同栈 CLI 拉流/NTRIP/录盘 | [pygnssutils](./pygnssutils.md) |
| 桌面监视/配置板卡 | [pygpsclient](./pygpsclient.md) |
| NMEA 句子 | [pynmeagps](./pynmeagps.md) |
| RTCM3 报文 | `pyrtcm`（上游同作者） |
| 多流录盘 / 生产 caster | [bnc](./bnc.md) / [bkg-ntripcaster](./bkg-ntripcaster.md) |

相关：上游 README · Sphinx · [pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · [pynmeagps](./pynmeagps.md) · 教程 [06](../tutorials/06-iono-positioning.md)
