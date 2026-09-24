# libsbp · Swift Binary Protocol 多语言客户端操作手册

目录：[`PROJECTS.json` → `libsbp`](../../PROJECTS.json) · 上游 <https://github.com/swift-nav/libsbp> · 文档 <https://swift-nav.github.io/libsbp/> · **URL 已核** · PyPI 包名 **`sbp`（不是 `libsbp`）** · 本机 **`sbp` 6.5.2** · tip **`2b883ad`**（2026-09-18；tag **`v6.5.2`**=`e283ec36`）· 许可 **MIT** · 本机验证：`pip install sbp` + `sbp2json` / `python -m sbp2json`；上游 `python/data/one_msg.bin`、`test_data/short.sbp`、`test_data/roundtrip.sbp` 真解码；**无 Swift 接收机硬件** · 2026-09-24 05:20 EDT

> 岗位：与 **Piksi / Swift** 机型交换 **SBP** 二进制（导航、观测、配置、心跳等）。冲突时：**上游 README / spec / 本机 `sbp2json -h` > 本文**。现场配置/刷机 CLI → 列表 `piksi_tools`（尚未短硬）；ROS 2 → 列表 `swiftnav-ros2`（尚未短硬）；数值例程（非通信）→ `libswiftnav`。厂商对照：Septentrio ROS → [septentrio-gnss-driver](./septentrio-gnss-driver.md)；其他编解码 → [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pysbf2](./pysbf2.md)。

## 1. 用途与边界

**做：**

- 多语言绑定：C/C++、**Python（`sbp`）**、Rust、Java、JS、Haskell…；规范 YAML/`jsonschema`/`kaitai`
- Python：流式 `Framer`/`Handler` + `dispatch`；构造 `MsgPosLLH` / `MsgHeartbeat` 等并 `to_binary()`
- CLI：`sbp2json`（pip 自带；亦可 `python -m sbp2json`）；Rust 仓另有更快的 `sbp2json` / `json2sbp` / `json2json`
- 离线解码仓内 `.sbp` / 串口日志；串口/TCP/UDP 示例见 `sbp.client.examples`

**不做：**

- **不是** 通用多品牌 RTK/PPP 引擎 → [rtklib](./rtklib.md) / [ginan](./ginan.md) / [pride-pppar](./pride-pppar.md)
- **不是** Septentrio SBF / u-blox UBX / RTCM3 编解码 → [pysbf2](./pysbf2.md)/[sbfparser](./sbfparser.md) / [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md)
- **不是** Septentrio ROS 驱动 → [septentrio-gnss-driver](./septentrio-gnss-driver.md)（对照：不同厂商、不同二进制）
- **无接收机**时：只验绑定/CLI/样例文件；**禁止臆造**串口 NED 流 stdout

一句话：libsbp = **Swift SBP 协议栈**；电离层/精密定位仍在观测落盘或差分链路之后。

| 符号 | 含义 |
| --- | --- |
| SBP | Swift Binary Protocol；帧头 preamble=`0x55` |
| `msg_type` | u16 消息号（例：522=`MsgPosLLH`，65535=`MsgHeartbeat`，21=`MsgAcqResultDepA`） |
| `sbp` | **PyPI 包名**；`import sbp`；**无** `pip install libsbp` |
| `sbp2json` | SBP 二进制 → NDJSON（一行一帧） |
| `Framer` | 从 `read()` 切帧并 `dispatch` 成强类型消息 |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip 'sbp==6.5.2'
python -c "import importlib.metadata as m; print(m.version('sbp'))"
# 期望：6.5.2
# 负例：pip install libsbp  → No matching distribution found
which sbp2json
sbp2json -h | head -5
# 亦可：python -m sbp2json -h
# 可选加速 JSON：pip install 'sbp[sbp2json]'（pybase64 + rapidjson）
```

源码开发绑定：

```bash
git clone https://github.com/swift-nav/libsbp.git && cd libsbp
pip install 'file:///path/to/libsbp#subdirectory=python'
# 或：pip install "git+https://github.com/swift-nav/libsbp@v6.5.2#egg=sbp&subdirectory=python"
```

C/Rust 等见上游 README（CMake / Cargo）；本手册以 **Python + sbp2json** 为可复现路径。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'sbp'` | 未激活 venv / 装错名 | `pip install sbp`（不是 libsbp） |
| `pip install libsbp` 失败 | PyPI **无**该名 | 用 `sbp` |
| 只有 `python -m sbp2json` 无 `sbp2json` | PATH/scripts 未进 PATH | 用模块入口或把 venv `bin` 加入 PATH |
| 与固件字段对不上 | SBP/固件版本漂移 | 对齐接收机固件与 libsbp tag；读 CHANGELOG |

## 3. 端到端（本机 `sbp` 6.5.2 真跑）

样例路径以 clone 上游为准（下文 `LIB=.../libsbp`）。

### 3.1 `one_msg.bin`：`sbp2json` + `dispatch` 往返

```bash
LIB=/path/to/libsbp
od -An -tx1 $LIB/python/data/one_msg.bin | head -2
# 本机前 16 字节：55 15 00 da 05 0d 9a 99 81 41 00 40 bb 43 51 89 …
sbp2json $LIB/python/data/one_msg.bin
# 或：python -m sbp2json $LIB/python/data/one_msg.bin
```

**本机 stdout：**

```text
unconsumed: 33
{"preamble":85,"msg_type":21,"sender":1498,"length":13,"payload":"mpmBQQBAu0NRidpEDg==","crc":20459,"snr":16.200000762939453,"cp":374.5,"cf":1748.2911376953125,"prn":14}
```

说明：文件 54 B；完整第一帧 21 B = `MsgAcqResultDepA`（`msg_type=21`）；余 33 B 为截断的第二帧头（`msg_type=22`），故 `unconsumed: 33`——**属夹具设计，非解码器坏**。

```bash
python - <<'PY'
from sbp.msg import SBP
from sbp.table import dispatch
import struct
raw = open("python/data/one_msg.bin", "rb").read()  # cwd=LIB
msg_type, sender, length = struct.unpack_from("<HHB", raw, 1)
payload, crc = raw[6:6+length], struct.unpack_from("<H", raw, 6+length)[0]
msg = dispatch(SBP(msg_type, sender, length, payload, crc))
print(type(msg).__name__, f"snr={msg.snr} cp={msg.cp} cf={msg.cf} prn={msg.prn}")
assert msg.to_binary() == raw[:21]
print("roundtrip OK", msg.to_binary().hex())
PY
```

**本机：**

```text
MsgAcqResultDepA snr=16.200000762939453 cp=374.5 cf=1748.2911376953125 prn=14
roundtrip OK 551500da050d9a9981410040bb435189da440eeb4f
```

### 3.2 `roundtrip.sbp`：导航帧（非零 LLH）

```bash
# --include 后请加 --，否则路径会被当成又一个 include
sbp2json --include 522 -- $LIB/test_data/roundtrip.sbp | head -1
```

**本机（截断美化）：**

```text
msg_type=522 sender=22963 tow=271497800
lat=37.831235254413826 lon=-122.28650677009367 height=-17.215181577283488
n_sats=15 flags=6 h_accuracy=513 v_accuracy=1115
```

Python `Framer`（**勿**在 `Handler` 里 `break` 后依赖上下文清理——本机曾挂起；直接迭代 `Framer`）：

```bash
python - <<'PY'
from sbp.client.drivers.file_driver import FileDriver
from sbp.client.framer import Framer
from collections import Counter
c, n = Counter(), 0
with open("test_data/roundtrip.sbp", "rb") as fh:
    for msg, _ in Framer(FileDriver(fh).read, None, verbose=False):
        n += 1
        c[type(msg).__name__] += 1
        if type(msg).__name__ == "MsgPosLLH" and msg.n_sats:
            print(f"PosLLH tow={msg.tow} lat={msg.lat:.8f} lon={msg.lon:.8f} h={msg.height:.4f} n_sats={msg.n_sats} flags={msg.flags}")
            break
print("scanned", n, "top", c.most_common(5))
PY
```

**本机：**

```text
PosLLH tow=271497800 lat=37.83123525 lon=-122.28650677 h=-17.2152 n_sats=15 flags=6
```

整文件（本机 `sbp2json` 无 CRC 报错）：**5000** 帧；Top 含 `MsgGPSTime`/`MsgUtcTime`/`MsgPosLLH`/`MsgVelNED`/`MsgDops`/`MsgBaselineNED`/`MsgAgeCorrections`/`MsgDgnssStatus` 各 **466**。伴生：`GPSTime wn=2098 tow=271497800 ns_residual=0 flags=1`；本段 `MsgBaselineNED` 样例 `n=e=d=0`（无基线解时为零，属数据内容非解析失败）。

### 3.3 `short.sbp`：帧计数

```bash
python - <<'PY'
from sbp.client.drivers.file_driver import FileDriver
from sbp.client.framer import Framer
from collections import Counter
c = Counter(); n = 0
with open("test_data/short.sbp", "rb") as fh:
    for msg, _ in Framer(FileDriver(fh).read, None, verbose=False):
        n += 1; c[type(msg).__name__] += 1
print("total", n); print("top", c.most_common(8))
PY
```

**本机：** `total 2382`；Top 含 `MsgGPSTime`/`MsgUtcTime`/`MsgPosLLH`/`MsgPosECEF`/`MsgVelNED`/`MsgVelECEF`/`MsgDops`/`MsgBaselineNED` 各 **188**（该文件前几帧导航字段可为 0，计数仍有效）。对照仓内 `test_data/short.sbp.json` NDJSON **2382** 行。

### 3.4 构造 `MsgPosLLH` / `MsgHeartbeat` 往返

```bash
python - <<'PY'
from sbp.navigation import MsgPosLLH
from sbp.system import MsgHeartbeat
from sbp.client.framer import Framer
import io
pos = MsgPosLLH(tow=407250000, lat=37.38656789, lon=-122.08345678,
                height=25.125, h_accuracy=150, v_accuracy=300, n_sats=14, flags=4)
blob = pos.to_binary()
for m, _ in Framer(io.BytesIO(blob).read, None, verbose=False):
    print(f"roundtrip PosLLH tow={m.tow} lat={m.lat:.8f} lon={m.lon:.8f} h={m.height} n_sats={m.n_sats} flags={m.flags}")
    break
hb = MsgHeartbeat(flags=0x1)
print("HB", hb.to_binary().hex(), "msg_type", hb.msg_type)
PY
```

**本机：**

```text
roundtrip PosLLH tow=407250000 lat=37.38656789 lon=-122.08345678 h=25.125 n_sats=14 flags=4
HB 55ffff42000401000000cf5a msg_type 65535
```

### 3.5 串口示例（需硬件；本机未跑）

```bash
# 默认 1 Mbaud；无设备会失败——勿当本手册已测 stdout
python -m sbp.client.examples.simple -p /dev/ttyUSB0
```

## 4. 接到哪步

```text
Swift 接收机 UART/TCP/.sbp 日志
  → sbp2json / Framer 解码（本文）
  →（现场）piksi_tools 配置/刷机（列表；尚未短硬）
  →（ROS2）swiftnav-ros2（列表；尚未短硬）
  → 观测/位置落盘 → georinex / rtklib / 电离层链
```

厂商二进制对照：[septentrio-gnss-driver](./septentrio-gnss-driver.md)（SBF/ROS）· [pysbf2](./pysbf2.md)/[sbfparser](./sbfparser.md) · [pyubx2](./pyubx2.md)（UBX）· [pyrtcm](./pyrtcm.md)（RTCM3）。

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `pip install libsbp` 失败 | PyPI 名是 **`sbp`** | `pip install sbp` |
| 2 | `sbp2json --include 522 file.sbp` 报 `invalid int value: '…/file.sbp'` | `nargs` 把路径吃进 `--include` | `sbp2json --include 522 -- file.sbp` |
| 3 | `unconsumed: 33` @ `one_msg.bin` | 夹具含截断第二帧 | 只信第一帧；或换 `roundtrip.sbp` |
| 4 | `Handler`+`break` 后进程挂起 | 读线程阻塞在 `read` | 直接迭代 `Framer`；或读到 EOF 不提前 `break` 清上下文 |
| 5 | `short.sbp` 上 `sbp2json` 刷 `CRC error` | 流中夹杂/旧帧与校验策略 | 用 `Framer` 统计或换 `roundtrip.sbp`（本机 0 CRC 错） |
| 6 | `MsgBaselineNED` 全 0 | 日志无固定基线 | 看 `MsgPosLLH`/`flags`；有基线解再滤 `n\|e\|d≠0` |
| 7 | 串口无数据 / Permission denied | 无硬件或未入 `dialout` | 无 Rx 只跑文件；有 Rx：`adduser $USER dialout` |
| 8 | 字段与固件 GUI 不一致 | SBP 版本/废弃消息（`*Dep*`） | 钉 tag；优先非 Dep 消息号 |
| 9 | 当 TEC/PPP 引擎用 | 只是协议库 | 落盘后走 [georinex](./georinex.md)/[rtklib](./rtklib.md) |
| 10 | 与 Septentrio 驱动混用 API | 不同厂商二进制 | SBF→[pysbf2](./pysbf2.md)；SBP→本文 |

## 6. 选型

| 你要… | 用 |
| --- | --- |
| Swift SBP 编解码 / `sbp2json` | **本文 libsbp（`pip install sbp`）** |
| Septentrio 实时进 ROS | [septentrio-gnss-driver](./septentrio-gnss-driver.md) |
| Septentrio 离线 SBF | [pysbf2](./pysbf2.md) / [sbfparser](./sbfparser.md) |
| u-blox UBX | [pyubx2](./pyubx2.md) |
| RTCM3 | [pyrtcm](./pyrtcm.md) |
| RTCM3→RINEX 小工具 | 列表 **`rtcm3torinex`**（高优先缺篇） |
| 定位/PPP | [rtklib](./rtklib.md) / [ginan](./ginan.md) / [pride-pppar](./pride-pppar.md) |

## 7. 相关

[septentrio-gnss-driver](./septentrio-gnss-driver.md) · [pysbf2](./pysbf2.md) · [sbfparser](./sbfparser.md) · [pyubx2](./pyubx2.md) · [pyrtcm](./pyrtcm.md) · [pygnssutils](./pygnssutils.md) · [rtkbase](./rtkbase.md) · [README](./README.md)

- 上游：<https://github.com/swift-nav/libsbp>
- PyPI：<https://pypi.org/project/sbp/>
- 规范/生成：仓内 `spec/`、`generator/`
- 许可：MIT
