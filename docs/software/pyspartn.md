# pyspartn · SPARTN 消息编解码库操作手册

目录：[`PROJECTS.json` → `pyspartn`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pyspartn> · 文档 <https://www.semuconsulting.com/pyspartn/> · PyPI **`pyspartn` 1.1.0** · tip **`8fc58f8`** · BSD-3-Clause · Python ≥3.10 · 本机验证 1.1.0（**无接收机 / 无 L-band**；传输层构造往返；上游 `tests/spartnOCB.log` / `spartnGAD.log` / `spartnMIXED.log`；`examples/d9s_spartn_data.bin` 3007 帧；密钥样例解密）· 2026-09-24 04:50 EDT

> 岗位：纯 Python **解析/序列化 SPARTN**（传输层 + 可选解密解码 OCB/HPAC/GAD/BPAC/EAS）。冲突时：**上游 README / Sphinx / 本机 `help(SPARTNReader)` > 本文**。串口/NTRIP/录流 CLI → [pygnssutils](./pygnssutils.md)；桌面 GUI → [pygpsclient](./pygpsclient.md)；同系 NMEA/UBX/RTCM → [pynmeagps](./pynmeagps.md) / [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md)。Galileo HAS（另一套改正）→ [haslib](./haslib.md)。**本包无 CLI entry point**（拉流用 `gnssstreamer` / `gnssntripclient`）。

## 1. 用途与边界

**做：**

- 流式读**纯 SPARTN** 二进制（文件/串口/套接字）；迭代 `SPARTNReader`
- 单帧 `SPARTNReader.parse(bytes)` → `SPARTNMessage`；`serialize()` 写回完整帧
- `decode=True` + 有效 `key`/`basedate`：解密并展开 OCB / HPAC / GAD 等载荷字段（`SF*`）
- 同作者栈底层：被 [pygpsclient](./pygpsclient.md) / [pygnssutils](./pygnssutils.md) 在 SPARTN 路径上用到

**不做：**

- **不是** NTRIP 握手/订流/录盘 CLI → [pygnssutils](./pygnssutils.md)（对比：pyspartn = **电文编解码**；pygnssutils = **拉流/录盘**）
- **不是** 桌面监视 GUI → [pygpsclient](./pygpsclient.md)
- **不是** RTCM3 / NMEA / UBX → [pyrtcm](./pyrtcm.md) / [pynmeagps](./pynmeagps.md) / [pyubx2](./pyubx2.md)
- **不是** Galileo HAS 页解码 → [haslib](./haslib.md)（HAS = E6 C/Nav→SSR；SPARTN = u-blox 开放 PPP-RTK 格式；协议不同）
- **不是** 定位滤波 / PPP 引擎 → [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md)；解析库**不会**单独抬高精度
- **不**保证无密钥仍可读加密载荷（商用流几乎一律 `eaf=1`）

一句话：pyspartn = **SPARTN 二进制的结构化读写**；电离层/精密产品仍在「改正灌进接收机或落盘 → 观测/解算」之后。

| 符号 | 含义 |
| --- | --- |
| `SPARTNReader` | 流包装：`read()` 或 `for raw, msg in reader` |
| `SPARTNMessage` | 一帧；`identity` 如 `SPARTN-1X-OCB-GPS`、`SPARTN-1X-GAD` |
| OCB / HPAC / GAD | 轨道时钟偏差 / 高精度大气 / 网格大气描述 |
| `eaf` | 载荷是否加密（样例与商用流多为 1） |
| `timeTagtype` | 0=16-bit 模糊时标（需 `basedate`）；1=32-bit `gnssTimeTag` |
| `VALCRC` / `VALNONE` | CRC 校验开/关（`validate` 默认 1） |
| `ERRIGNORE`/`ERRLOG`/`ERRRAISE` | `quitonerror` 0/1/2 |
| `HASCRYPTO` | 运行时是否已装 `cryptography`（解密依赖） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip 'pyspartn>=1.1.0'
python -c "import importlib.metadata as m; print(m.version('pyspartn'))"
# 期望：1.1.0
# 本包 entry_points 为空（无 pyspartn 命令）
python -c "import importlib.metadata as m; print(list(m.distribution('pyspartn').entry_points))"
# 期望：[]
# 解密载荷另装（默认不随 pyspartn 拉上）：
python -m pip install -U cryptography
python -c "from pyspartn import HASCRYPTO; print(HASCRYPTO)"
# 期望：True
# 样例日志（本手册 §3）：
mkdir -p ~/iono_ops && git clone --depth 1 https://github.com/semuconsulting/pyspartn.git ~/iono_ops/pyspartn
# 流 CLI 另装：pip install pygnssutils  → gnssstreamer / gnssntripclient
```

conda：`conda install -c conda-forge pyspartn`。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'pyspartn'` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| `python -m pyspartn` 失败 | 无 `__main__` / 无 console script | 用库 API；CLI 用 `gnssstreamer` |
| `HASCRYPTO False` 却 `decode=True` | 未装 cryptography | `pip install cryptography` |
| 与文档 API 不符 | 钉死了旧版 | `pip install -U 'pyspartn>=1.1.0'` |

## 3. 端到端（本机 1.1.0 真跑）

**本机无 u-blox 接收机、无 L-band 解调、无 PointPerfect 订户密钥**：下列全部用**构造字节 + 上游仓内样例**真跑编解码。商用密钥勿提交 git；下文密钥来自上游 **tests/examples 公开样例**（仅用于回归，已过期）。

### 3.1 传输层：parse → serialize 往返

```bash
python - <<'PY'
from pyspartn import SPARTNReader, SPARTNMessage, SPARTNMessageError, SPARTNParseError

raw = b"s\x00\x12\xe2\x00|\x10[\x12H\xf5\t\xa0\xb4+\x99\x02\x15\xe2\x05\x85\xb7\x83\xc5\xfd\x0f\xfe\xdf\x18\xbe\x7fv \xc3`\x82\x98\x10\x07\xdc\xeb\x82\x7f\xcf\xf8\x9e\xa3ta\xad"
msg = SPARTNReader.parse(raw, decode=False)
print(msg)
print(raw.hex())
assert msg.serialize() == raw
assert SPARTNMessage(transport=raw).serialize() == raw
print("roundtrip OK", msg.identity, msg.nData, msg.eaf)

badcrc = raw[:-1] + bytes([0xa1])
try:
    SPARTNReader.parse(badcrc)
except SPARTNMessageError as e:
    print("badcrc", e)
try:
    SPARTNReader.parse(b"x\x00\x12\xe2\x00|\x10[\x12H\xf5\t\xa0\xb4+\x99\x02\x15")
except SPARTNParseError as e:
    print("badpreamble", e)
PY
```

**本机 stdout：**

```text
<SPARTN(SPARTN-1X-OCB-GPS, msgType=0, nData=37, eaf=1, crcType=2, frameCrc=2, msgSubtype=0, timeTagtype=0, gnssTimeTag=3970, solutionId=5, solutionProcId=11, encryptionId=1, encryptionSeq=9, authInd=1, embAuthLen=0, crc=7627181)>
730012e2007c105b1248f509a0b42b990215e20585b783c5fd0ffedf18be7f7620c36082981007dceb827fcff89ea37461ad
roundtrip OK SPARTN-1X-OCB-GPS 37 1
badcrc Invalid CRC 7627169
badpreamble Unknown message preamble 120
```

注意：`SPARTNMessage` **只能**从已有 `transport=` 字节构造（无字段级「从零拼帧」API）；生成侧用 `serialize()` 回写。对象初始化后**不可变**（改 `eaf` 会 `SPARTNMessageError`）。

### 3.2 上游测试日志：传输层流读

`tests/spartnOCB.log`（本机 1077 B）：

```bash
python - <<'PY'
from pathlib import Path
from pyspartn import SPARTNReader, ERRIGNORE
path = Path.home() / "iono_ops/pyspartn/tests/spartnOCB.log"
with path.open("rb") as fh:
    for i, (raw, msg) in enumerate(SPARTNReader(fh, quitonerror=ERRIGNORE), 1):
        print(i, msg.identity, "nData", msg.nData, "eaf", msg.eaf, "tt", msg.gnssTimeTag)
PY
```

**本机（前 4 + 末行规模）：**

```text
1 SPARTN-1X-OCB-GPS nData 30 eaf 1 tt 28075
2 SPARTN-1X-OCB-GLO nData 33 eaf 1 tt 38857
3 SPARTN-1X-OCB-BEI nData 36 eaf 1 tt 28061
4 SPARTN-1X-OCB-GAL nData 34 eaf 1 tt 28075
…共 10 帧（GPS/GLO 各 3，BEI/GAL 各 2）
```

`tests/spartnMIXED.log`（82674 B）同法：`quitonerror=ERRIGNORE` → **422** 帧（OCB×4 星座各 56；HPAC×4 各 45；GAD 18）。混有噪声字节时默认 `ERRLOG` 会刷屏 `Unknown protocol`——批处理统计用 `ERRIGNORE`。

### 3.3 解密解码（样例密钥）

上游 tests 密钥 / basedate（**仅样例**）：

```bash
python - <<'PY'
from datetime import datetime, timezone
from pathlib import Path
from pyspartn import SPARTNReader, ERRIGNORE, date2timetag

KEY = "930d847b779b126863c8b3b2766ae7cc"
BD = datetime(2024, 4, 18, 20, 48, 29, 977255, tzinfo=timezone.utc)
print("basedate_tt", date2timetag(BD))
root = Path.home() / "iono_ops/pyspartn/tests"

with (root / "spartnGAD.log").open("rb") as fh:
    for i, (raw, msg) in enumerate(
        SPARTNReader(fh, decode=True, key=KEY, basedate=BD, quitonerror=ERRIGNORE), 1
    ):
        nsf = sum(1 for a in dir(msg) if a.startswith("SF"))
        print(i, msg.identity, "nData", msg.nData, "nSF", nsf,
              "SF005", getattr(msg, "SF005", None), "SF030", getattr(msg, "SF030", None))

with (root / "spartnOCB.log").open("rb") as fh:
    for i, (raw, msg) in enumerate(
        SPARTNReader(fh, decode=True, key=KEY, basedate=BD, quitonerror=ERRIGNORE), 1
    ):
        nsf = sum(1 for a in dir(msg) if a.startswith("SF"))
        print("ocb", i, msg.identity, "nSF", nsf)
        if i >= 4:
            break
PY
```

**本机 stdout：**

```text
basedate_tt 451169309
1 SPARTN-1X-GAD nData 191 nSF 228 SF005 152 SF030 31
2 SPARTN-1X-GAD nData 62 nSF 74 SF005 152 SF030 9
3 SPARTN-1X-GAD nData 191 nSF 228 SF005 153 SF030 31
4 SPARTN-1X-GAD nData 62 nSF 74 SF005 153 SF030 9
ocb 1 SPARTN-1X-OCB-GPS nSF 63
ocb 2 SPARTN-1X-OCB-GLO nSF 71
ocb 3 SPARTN-1X-OCB-BEI nSF 71
ocb 4 SPARTN-1X-OCB-GAL nSF 71
```

错密钥（`quitonerror=ERRRAISE`）→ `SPARTNDecryptionError: Message type SPARTN-1X-GAD timetag … not successfully decrypted - check key and basedate`。

### 3.4 大样例：`d9s_spartn_data.bin`

`examples/d9s_spartn_data.bin`（~846 KB）。传输层：

```bash
python - <<'PY'
from collections import Counter
from pathlib import Path
from pyspartn import SPARTNReader, ERRIGNORE
path = Path.home() / "iono_ops/pyspartn/examples/d9s_spartn_data.bin"
c = Counter()
with path.open("rb") as fh:
    for _, msg in SPARTNReader(fh, quitonerror=ERRIGNORE):
        fam = ("OCB" if "OCB" in msg.identity else
               "HPAC" if "HPAC" in msg.identity else
               "GAD" if "GAD" in msg.identity else msg.identity)
        c[fam] += 1
print(sum(c.values()), dict(c))
PY
```

**本机：** `3007 {'OCB': 1692, 'HPAC': 1127, 'GAD': 188}`。

解密样例（上游 examples 密钥；basedate ≈ 2023-09-01 18:00 UTC）：

```bash
python - <<'PY'
from datetime import datetime, timezone
from pathlib import Path
from pyspartn import SPARTNReader, ERRIGNORE
KEY = "bc75cdd919406d61c3df9e26c2f7e77a"
BD = datetime(2023, 9, 1, 18, 0, 0, tzinfo=timezone.utc)
path = Path.home() / "iono_ops/pyspartn/examples/d9s_spartn_data.bin"
with path.open("rb") as fh:
    for i, (_, msg) in enumerate(
        SPARTNReader(fh, decode=True, key=KEY, basedate=BD, quitonerror=ERRIGNORE), 1
    ):
        nsf = sum(1 for a in dir(msg) if a.startswith("SF"))
        print(i, msg.identity, "eaf", msg.eaf, "nSF", nsf, "tt", msg.gnssTimeTag)
        if i >= 6:
            break
PY
```

**本机：**

```text
1 SPARTN-1X-OCB-GLO eaf 1 nSF 79 tt 25927
2 SPARTN-1X-OCB-GAL eaf 1 nSF 71 tt 15145
3 SPARTN-1X-OCB-GLO eaf 1 nSF 79 tt 25937
4 SPARTN-1X-OCB-GAL eaf 1 nSF 71 tt 15155
5 SPARTN-1X-HPAC-GPS eaf 1 nSF 489 tt 431280750
6 SPARTN-1X-HPAC-GPS eaf 1 nSF 514 tt 431280750
```

### 3.5 有硬件 / 订户时

```python
from serial import Serial
from pyspartn import SPARTNReader
# 口上必须是「纯 SPARTN」字节；混 UBX/NMEA 请改 pyubx2 或 gnssstreamer 分流
with Serial("/dev/ttyACM0", 38400, timeout=3) as stream:
    spr = SPARTNReader(stream, decode=True, key="<your-32hex-key>")
    raw, msg = spr.read()
    print(msg.identity, msg.eaf)
```

NTRIP PointPerfect Flex：用 [pygnssutils](./pygnssutils.md) `gnssntripclient` / `gnssstreamer --cliinput 2`（`--datatype SPARTN`），再把录盘文件喂给本库。上游 README 记：u-blox **L-band / MQTT SPARTN 已于 2025-10 停服**；多数用户现走 **IP NTRIP**。无订户时仍可用 §3.1–3.4 做编解码回归。

## 4. I/O 与关键参数

| API | 作用 |
| --- | --- |
| `SPARTNReader(stream, validate=1, quitonerror=1, decode=False, key=None, basedate=None, …)` | 包装二进制流 |
| `SPARTNReader.parse(bytes, …)` | 单帧 → `SPARTNMessage` |
| `SPARTNMessage(transport=bytes, …)` | 从整帧构造 |
| `msg.serialize()` | → 含前导 `s`(0x73)、CRC 的 `bytes` |
| `date2timetag(datetime)` / `timetag2date` / `convert_timetag` | 时标换算 |
| `HASCRYPTO` | 是否可解密 |

| `validate` | 含义 |
| --- | --- |
| `VALCRC` (1) | CRC 错 → `SPARTNMessageError`（默认） |
| `VALNONE` (0) | 忽略坏 CRC/长度 |

| `decode` 相关 | 含义 |
| --- | --- |
| `decode=False` | 只解析传输层头（`msgType`/`nData`/`eaf`/…） |
| `decode=True` | 需 `cryptography` + 有效 `key`；`timeTagtype=0` 还要准的 `basedate`（半日内）或 `TIMEBASE` 借流内 32-bit 时标 |
| `key` | 32 位十六进制字符串（约 4 周一轮换） |
| `basedate` | `datetime`（UTC）或 32-bit `gnssTimeTag` int |

流须**仅含 SPARTN**；MQTT 录盘时关掉 Key/Assist 等 UBX 主题，否则要先抽帧。

## 5. 接到哪步

```text
PointPerfect NTRIP / 历史 .bin
  →（CLI）pygnssutils 订流/录盘
  →（库）pyspartn 解析 / 解密
  →（GUI）pygpsclient 监视灌板
  → 接收机固定 / 或改正旁路进 PPP 引擎（cssrlib/rtklib…）
  → 电离层产品仍走 RINEX → georinex / pytecgg
```

同系交叉：[pyubx2](./pyubx2.md) · [pynmeagps](./pynmeagps.md) · [pyrtcm](./pyrtcm.md) · [pygpsclient](./pygpsclient.md) · [pygnssutils](./pygnssutils.md)。HAS 对照：[haslib](./haslib.md)（Galileo E6→SSR，不是 SPARTN）。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `SPARTNDecryptionError: … check key and basedate` | 密钥过期或 basedate 偏半日以上 | 向服务商取当期 key；历史流按录制日设 `basedate` |
| 2 | `HASCRYPTO` False / 解密 ImportError | 未装 cryptography | `pip install cryptography`（部分 32-bit 机需 Rust） |
| 3 | 刷屏 `Unknown protocol b'…'` | 流含非 SPARTN 字节且 `quitonerror=ERRLOG` | `ERRIGNORE`；或先分流/裁剪为纯 SPARTN |
| 4 | `Invalid CRC …` | 截断帧 / 改过字节 | 保留完整帧；调试可临时 `validate=VALNONE` |
| 5 | `Unknown message preamble 120` | 首字节不是 `s`(0x73) | 确认未把 UBX/RTCM/文本当 SPARTN |
| 6 | `Object is immutable…` | 构造后改属性 | 重新 `parse`/`SPARTNMessage(transport=…)` |
| 7 | `timeTagtype=0` 开头几帧解密失败 | `basedate=TIMEBASE` 时尚无同星座 32-bit 时标可借 | `quitonerror=ERRLOG`；或给真实 basedate；等 HPAC 等带 32-bit 的帧过去 |
| 8 | GLONASS 时标对不上 | GLO 用 UTC+3 日界 | basedate/时标换算按星座；对照上游 `convert_timetag` 测例 |
| 9 | 期望本库出固定解 / TEC | 职责仅编解码 | 改正进接收机或 PPP；TEC → [georinex](./georinex.md)/[pytecgg](./pytecgg.md) |
| 10 | L-band / 旧 MQTT 示例全失败 | 2025-10 后服务停 | 改 PointPerfect Flex **NTRIP IP**；库侧编解码仍可用样例回归 |
| 11 | 与 PyGPSClient 版本漂移 | 传递依赖未升级 | `pip install -U pyspartn PyGPSClient pygnssutils` |
| 12 | `python -m pyspartn` / 无命令 | 无 entry point | 用 API；流用 `gnssstreamer` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 脚本里读写/解密 SPARTN | **pyspartn（本文）** |
| RTCM3（含 MSM） | [pyrtcm](./pyrtcm.md) |
| UBX / NMEA | [pyubx2](./pyubx2.md) / [pynmeagps](./pynmeagps.md) |
| 同栈 CLI 拉 NTRIP SPARTN/录盘 | [pygnssutils](./pygnssutils.md) |
| 桌面监视/灌板 | [pygpsclient](./pygpsclient.md) |
| Galileo HAS → SSR | [haslib](./haslib.md) |
| PPP / PPP-RTK 解算 | [cssrlib](./cssrlib.md) / [rtklib](./rtklib.md) |
| 多流录盘运维 | [bnc](./bnc.md) |

相关：上游 README · Sphinx · [pyubx2](./pyubx2.md) · [pynmeagps](./pynmeagps.md) · [pyrtcm](./pyrtcm.md) · [pygpsclient](./pygpsclient.md) · [pygnssutils](./pygnssutils.md) · [haslib](./haslib.md) · 教程 [06](../tutorials/06-iono-positioning.md) · [data-access 实时](../data-access.md#实时-rtcm--ssr--ntrip)
