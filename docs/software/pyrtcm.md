# pyrtcm · RTCM3 编解码库操作手册

目录：[`PROJECTS.json` → `pyrtcm`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pyrtcm> · 文档 <https://www.semuconsulting.com/pyrtcm/> · PyPI **`pyrtcm` 1.2.0** · tip **`5d66c7a`** · BSD-3-Clause · Python ≥3.10 · 本机验证 1.2.0（README 1005 帧往返；上游 `tests/pygpsdata-RTCM3.log` 11 帧；`pygpsdata-RTCMMSM3.log` MSM `parse_msm`；`msgfilter`/`PARSE_META`）· 2026-09-24 04:48 EDT · **质检复跑通过**（同 I/O，2026-09-24 04:50 EDT）

> 岗位：纯 Python **解析/生成 RTCM3**（含 MSM / 常见 SSR）。冲突时：**上游 README / Sphinx / 本机 `help(RTCMReader)` > 本文**。NTRIP/串口/录流 CLI → [pygnssutils](./pygnssutils.md)；桌面 GUI → [pygpsclient](./pygpsclient.md)；NMEA / UBX 姐妹库 → [pynmeagps](./pynmeagps.md) / [pyubx2](./pyubx2.md)。实时源注册与挂载点 → [data-access NTRIP](../data-access.md#实时-rtcm--ssr--ntrip)。**本包无 CLI entry point**（上游 “CLI” 指向 pygnssutils `gnssstreamer`）。

## 1. 用途与边界

**做：**

- 流式读文件/串口/套接字中的 `d3 …` RTCM3 帧；迭代 `RTCMReader`
- 单帧 `RTCMReader.parse(bytes)` → `RTCMMessage`；`serialize()` 写回带 CRC 的完整帧
- 拆 MSM（107x–112x）为可迭代数组：`parse_msm`；`labelmsm` 切换 RINEX 码 / 频段名
- 过滤：`msgfilter=(1005,1077)`；轻量：`parsed=PARSE_META` / `PARSE_NONE`
- 同作者栈底层：被 [pygpsclient](./pygpsclient.md) / [pygnssutils](./pygnssutils.md) / [pyubx2](./pyubx2.md)（`protfilter` 含 RTCM）依赖

**不做：**

- **不是** NTRIP 握手/订流/录盘 CLI → [pygnssutils](./pygnssutils.md)（对比：pyrtcm = **电文编解码**；pygnssutils = **拉流/录盘/小 caster**）
- **不是** 多流运维 GUI / 生产 caster → [bnc](./bnc.md) / [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** 定位滤波 / PPP / TEC → [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md) / [pytecgg](./pytecgg.md)
- **不是** SPARTN 改正 → 上游同系 `pyspartn`（本目录未单列时见 GitHub）

一句话：pyrtcm = **RTCM3 二进制的结构化读写**；电离层产品仍在「改正/观测落盘 → RINEX」之后。

| 符号 | 含义 |
| --- | --- |
| `RTCMReader` | 流包装：`read()` 或 `for raw, msg in reader` |
| `RTCMMessage` | 一帧属性包；`identity` 如 `1005`、`1077`、`4076_201` |
| `DF00n` | RTCM 数据字段名（见 `RTCM_DATA_FIELDS` / `datadesc`） |
| `VALCKSUM` / `VALNONE` | CRC 校验开/关（`validate` 默认 1） |
| `PARSE_NONE`/`FULL`/`META` | 0 仅原始 / 1 全解析（默认）/ 2 仅元数据字符串 |
| `labelmsm` | 1=RINEX 码（`2C`）；2=频段（`L2`） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip 'pyrtcm>=1.2.0'
python -c "import importlib.metadata as m; print(m.version('pyrtcm'))"
# 期望：1.2.0
# 依赖：pynmeagps>=1.1.4；本包 entry_points 为空（无 pyrtcm 命令）
python -c "import importlib.metadata as m; print(list(m.distribution('pyrtcm').entry_points))"
# 期望：[]
# 流 CLI 另装：pip install pygnssutils  → gnssstreamer / gnssntripclient
```

conda：`conda install -c conda-forge pyrtcm`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pyrtcm'` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| `python -m pyrtcm` 失败 | 无 `__main__` / 无 console script | 用库 API；CLI 用 `gnssstreamer` |
| 与文档 API 不符（无 `msgfilter`） | 钉死了 &lt;1.2 | `pip install -U 'pyrtcm>=1.2.0'` |

## 3. 端到端（本机 1.2.0 真跑）

### 3.1 最小 1005 帧：parse → serialize 往返

上游 README 样例字节（Station ARP ECEF）：

```bash
python - <<'PY'
from pyrtcm import RTCMReader, RTCMMessage, ecef2llh

raw = b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
msg = RTCMReader.parse(raw)
print(msg)
print(msg.identity, msg.DF003, msg.DF025, msg.DF026, msg.DF027)
print(msg.serialize().hex())
lat, lon, h = ecef2llh(msg.DF025, msg.DF026, msg.DF027)
print(f"llh {lat:.8f} {lon:.8f} {h:.4f}")
assert msg.serialize() == raw
# 亦可只喂 payload（无头/CRC），库会补全
msg2 = RTCMMessage(payload=b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
assert msg2.serialize() == raw
print("roundtrip OK")
PY
```

**本机 stdout：**

```text
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.802800001, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>
1005 0 4444030.802800001 3085671.2349 3366658.256
d300133ed000038a58d9493c872f34109d07d6af48205ad7f7
llh 32.06583254 34.77381904 72.1342
roundtrip OK
```

`DF025` 浮点尾数以本机为准（与上游 README 打印的 `4444030.8028` 等价）。

### 3.2 上游测试日志：整文件迭代

取自仓内 `tests/pygpsdata-RTCM3.log`：

```bash
# 若已 clone 上游：LOG=.../pyrtcm/tests/pygpsdata-RTCM3.log
python - <<'PY'
from collections import Counter
from pyrtcm import RTCMReader
path = "pygpsdata-RTCM3.log"  # 换成你的路径
with open(path, "rb") as fh:
    ids = Counter()
    for i, (raw, msg) in enumerate(RTCMReader(fh), 1):
        ids[msg.identity] += 1
        if i <= 3:
            print(i, msg.identity, len(raw))
print("total", sum(ids.values()), sorted(ids))
PY
```

**本机：**

```text
1 1005 25
2 4072 68
3 1077 275
total 11 ['1005', '1007', '1059', '1060', '1077', '1087', '1097', '1117', '1127', '1230', '4072']
```

接 CLI 回放：`gnssstreamer --filename pygpsdata-RTCM3.log --protfilter 4 --verbosity 2`（见 [pygnssutils](./pygnssutils.md)）。

### 3.3 MSM：`parse_msm` + `labelmsm`

`tests/pygpsdata-RTCMMSM3.log`（本机 3 帧：`1073`/`1083`/`1093`）：

```bash
python - <<'PY'
from pyrtcm import RTCMReader, parse_msm
path = "pygpsdata-RTCMMSM3.log"
with open(path, "rb") as fh:
    raw, msg = next(iter(RTCMReader(fh)))  # 默认 labelmsm=1 → RINEX 码
print(msg.identity, msg.NSat, msg.NSig, msg.NCell, msg.PRN_01, msg.CELLSIG_01)
meta, sats, cells = parse_msm(msg)
print(sorted(meta), len(sats), len(cells))
print(sats[0])
print(cells[0])
with open(path, "rb") as fh:
    _, m2 = next(iter(RTCMReader(fh, labelmsm=2)))
print("labelmsm2", m2.CELLSIG_01, m2.CELLSIG_02)
PY
```

**本机：**

```text
1073 8 4 20 006 1C
['cells', 'epoch', 'gnss', 'identity', 'sats', 'station'] 8 20
{'PRN': '006', 'DF398': 0.5908203125}
{'CELLPRN': '006', 'CELLSIG': '1C', 'DF400': -0.00019592046737670898, 'DF401': -2.4491921067237854e-05, 'DF402': 15, 'DF420': 0}
labelmsm2 L1 L2
```

手写循环也可用 `getattr(msg, f"CELLPRN_{i:02d}")`（后缀两位、从 01）。

### 3.4 `msgfilter` + `PARSE_META` + 坏 CRC

```bash
python - <<'PY'
from pyrtcm import RTCMReader, PARSE_META, RTCMParseError

path = "pygpsdata-RTCM3.log"
with open(path, "rb") as fh:
    hit = none = 0
    for raw, msg in RTCMReader(fh, msgfilter=(1005, 1077)):
        if msg is None:
            none += 1
        else:
            hit += 1
            print("hit", msg.identity, len(raw))
print("parsed", hit, "none", none)

with open(path, "rb") as fh:
    for raw, meta in RTCMReader(fh, msgfilter=(1005,), parsed=PARSE_META):
        if meta is not None:
            print(meta)
            break

good = b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
bad = bytearray(good); bad[-1] ^= 0xFF
try:
    RTCMReader.parse(bytes(bad))
except RTCMParseError as e:
    print("badck", e)
print("validate0", RTCMReader.parse(bytes(bad), validate=0).identity)
PY
```

**本机：**

```text
hit 1005 25
hit 1077 275
parsed 2 none 9
<RTCM(1005, length=25, data=b'\xd3\x00\x13\x3e\xd0\x00\x03\x8a\x58\xd9\x49\x3c\x87\x2f\x34\x10\x9d\x07\xd6\xaf\x48\x20\x5a\xd7\xf7')>
badck RTCM3 message invalid - failed CRC: b'Z\xd7\x08'
validate0 1005
```

过滤未命中时 **`parsed is None`（raw 仍可能非空）**——迭代里务必判空。

### 3.5 NTRIP 落盘 → pyrtcm（接到 pygnssutils）

有账号时先按 [pygnssutils](./pygnssutils.md) / [data-access](../data-access.md) 订流并录二进制，再解析：

```bash
# 示例：公开 IGS RTS（口令用环境变量；勿进 git）
# gnssntripclient --server products.igs-ip.net --port 2101 --https 0 \
#   --mountpoint SSRA02IGS0 --ntripuser "$NTRIP_USER" --ntrippassword "$NTRIP_PASS" \
#   --datatype RTCM --ntripversion 2.0 --verbosity 2
# 或 gnssstreamer --cliinput 1 --input "ntrip://..." --format 2 --clioutput 1 --output rtcm.bin

python - <<'PY'
from collections import Counter
from pyrtcm import RTCMReader
# 无公网时可用上游 tests/pygpsdata-NTRIP-USCL00CHL0.log（本机 35 帧）
path = "rtcm.bin"  # 或 pygpsdata-NTRIP-USCL00CHL0.log
with open(path, "rb") as fh:
    ids = Counter(m.identity for _, m in RTCMReader(fh) if m is not None)
print(sum(ids.values()), ids.most_common(8))
PY
```

**本机（上游 `pygpsdata-NTRIP-USCL00CHL0.log`）：** `35` 帧，前几类含 `1003`–`1013`、`1019` 等。无接收机/无公网时勿臆造直播 stdout。

## 4. I/O 与关键参数

| API | 作用 |
| --- | --- |
| `RTCMReader(stream, validate=1, quitonerror=1, labelmsm=1, parsed=1, msgfilter="", …)` | 包装二进制流 |
| `RTCMReader.parse(bytes, validate=1, labelmsm=1)` | 单帧 → `RTCMMessage` |
| `RTCMMessage(payload=bytes)` | 由 payload 构造（不可变）；再 `serialize()` |
| `msg.serialize()` | → 完整帧（`d3` + 长度 + payload + CRC24） |
| `parse_msm(msg)` | → `(meta: dict, sats: list, cells: list)` |
| `ecef2llh(x,y,z)` / `datadesc("DF025")` | ECEF→LLH；字段中文/英文说明 |

| `parsed` | 返回的第二元组元素 |
| --- | --- |
| `0` `PARSE_NONE` | 恒 `None`（只要 raw） |
| `1` `PARSE_FULL` | `RTCMMessage`（默认） |
| `2` `PARSE_META` | 格式化 `str`（更快，无 DF 属性） |

输入：任意 `read(n)->bytes` 流（文件 / `Serial` / socket；库内有 `SocketStream`）。输出：属性在 `msg.DF*` / `PRN_01` / `CELLSIG_01`；写盘用 `serialize()` 或直接写 `raw`。

## 5. 接到哪步

```text
NTRIP caster / 串口 RTCM3 / .log 二进制
  →（CLI）pygnssutils gnssntripclient / gnssstreamer 订流·录盘
  →（库）pyrtcm RTCMReader / parse_msm 拆电文
  →（GUI）pygpsclient 监视差分
  → 观测/改正落盘 → RINEX → georinex / pytecgg / rtklib / cssrlib
```

同系交叉：[pygnssutils](./pygnssutils.md) · [pyubx2](./pyubx2.md) · [pynmeagps](./pynmeagps.md) · [pygpsclient](./pygpsclient.md) · [data-access NTRIP](../data-access.md) · [bnc](./bnc.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `RTCM3 message invalid - failed CRC` | 截断/粘包/改写尾字节 | 整帧交给 `RTCMReader`；临时 `validate=0` 仅调试 |
| 2 | 迭代里 `parsed is None` 却还有 raw | `msgfilter` 未命中 | 先判 `if parsed is None: continue` |
| 3 | `AttributeError: CELLSIG` | MSM 字段带两位后缀 | `CELLSIG_01` / `getattr(msg, f"CELLSIG_{i:02d}")` |
| 4 | `CELLSIG` 期望 `L1` 却是 `1C` | `labelmsm` 默认 1 | 频段名用 `labelmsm=2` |
| 5 | `RTCMMessage` 赋值属性失败 | 对象不可变 | 改 payload 后重建；或只读 DF |
| 6 | `python -m pyrtcm` / 无 console script | 本包无 CLI | `pip install pygnssutils` → `gnssstreamer --protfilter 4` |
| 7 | 无 `msgfilter` / `PARSE_META` | 版本 &lt;1.2.0 | `pip install -U 'pyrtcm>=1.2.0'` |
| 8 | 未知类型 / 缺 DF | 字典未覆盖该 MSM/专有号 | 查 `RTCM_MSGIDS`；按上游 Extensibility 补类型 |
| 9 | NTRIP 字节流解不出 | 仍含 HTTP 头或未切二进制 | 用 gnssntripclient/`--datatype RTCM` 落盘；确认文件以 `d3` 起 |
| 10 | 把本库当 RTK/TEC 引擎 | 职责仅编解码 | 改正+观测齐后走 [rtklib](./rtklib.md)/[pytecgg](./pytecgg.md) |
| 11 | 与 PyGPSClient 字段漂移 | 传递依赖未齐升 | `pip install -U pyrtcm pyubx2 pynmeagps PyGPSClient pygnssutils` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本里读写 RTCM3 / 拆 MSM | **pyrtcm（本文）** |
| 同栈 CLI 拉 NTRIP / 录盘 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 桌面监视差分链路 | [pygpsclient](./pygpsclient.md) |
| NMEA / UBX | [pynmeagps](./pynmeagps.md) / [pyubx2](./pyubx2.md) |
| 多流录盘 / 生产 caster | [bnc](./bnc.md) / [bkg-ntripcaster](./bkg-ntripcaster.md) |
| Galileo HAS 页 → RTCM/IGS SSR | [haslib](./haslib.md) |
| PPP/PPP-RTK 用改正 | [cssrlib](./cssrlib.md) / [rtklib](./rtklib.md) |

相关：上游 README · Sphinx · [pygnssutils](./pygnssutils.md) · [pyubx2](./pyubx2.md) · [pynmeagps](./pynmeagps.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)
