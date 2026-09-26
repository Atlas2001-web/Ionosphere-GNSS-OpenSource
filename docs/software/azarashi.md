# azarashi · QZSS 灾害危机管理通报（DCR/DCX）解码器操作手册

目录：[`PROJECTS.json` → `azarashi`](../../PROJECTS.json) · 上游 <https://github.com/nbtk/azarashi> · PyPI **`azarashi` 0.17.0**（2026-09-24 07:35 EDT / 20:35 JST 上传）· tag **`v0.17.0`** = main **`1fb06ca`**（2026-09-24 07:28 EDT / 20:28 JST）· **MIT** · ★**44** · Python **≥3.11**（classifiers 3.11–3.14）· 唯一依赖 `pyserial>=3.5` · 规格 **IS-QZSS-DCR-017**（MT43）+ **IS-QZSS-DCX-004**（MT44）· 实测 2026-09-26 05:35–05:45 EDT（CPython 3.13.5，pyubx2 1.3.7）

> 岗位：把みちびき L1S 播发的**災危通報**（MT43 = 气象厅 JMA-DC 报；MT44 = DCX 扩展：L-Alert / J-Alert / 海外机构 CAMF）解成可读文本、Python 对象或 NDJSON。**不定位、不解 SLAS 改正（MT47–51）**，不配置接收机。冲突时：**上游 docs/ 与源码 > 本文**。
> PyPI 0.17.0 安装包与 `1fb06ca` 的 `azarashi/` 目录 `diff -rq` 完全相同。

## 1. 用途与边界

| 输入（`msg_type`） | 来源 | 本文实测 |
| --- | --- | --- |
| `nmea`（别名 `spresense`） | Sony Spresense 输出的 `$QZQSM,<satid>,<63 hex>*CK` | ✅ 上游 3 份真实日志 333 句 |
| `ublox` | u-blox `UBX-RXM-SFRBX`（只收 gnssId=5、sigId=1 的 L1S，校 Fletcher 校验） | ✅ 上游 F9P 记录 `ublox_260924.ubx.gz`（757640 B） |
| `hex` | 仅 63 位十六进制（250 bit + 2 bit 补零，无头无校验） | ✅；64 位报 `Too Long Sentence` |
| `l1s` | 内阁府公开归档 `QNNN_YYYYMMDD.l1s`（1 B PRN + 每秒 4 B GPS 时 + 32 B 报文） | ✅ 官方 2 个整日文件 |
| `net` | 自带 UDP transmitter/receiver 的 33 B 数据报（仅 `decode()`） | ✅ 本机回环 |
| Septentrio SBF / NovAtel / Allystar / Unicore 原始 L1S | **不支持**（`msg_type='septentrio'` → `AzarashiUnsupportedFormatError`）；需自己抽出 250 bit 转 63 位 hex | — |

覆盖：DCR 灾害类别 1–6、8–12、14 全部（EEW/震源/震度/南海海槽/海啸/西北太平洋海啸/火山/降灰/气象/洪水/台风/海上）；DCX 的 Null、L-Alert、J-Alert、MT 播发状态、海外机构（CAMF A1–A18 + 扩展字段，带英文）。**接收机实时路径未在真接收机测试。**

## 2. 安装

```bash
export TMPDIR=/tmp/azarashi-man PIP_CACHE_DIR=/tmp/azarashi-man/pipcache XDG_CACHE_HOME=/tmp/azarashi-man/cache
python3 -m venv /tmp/azarashi-man/venv && . /tmp/azarashi-man/venv/bin/activate
pip install azarashi==0.17.0          # 只带 pyserial 3.5
azarashi --help
```

`--help` 原文（子命令 `azarashi nmea --help` 等输出相同）：

```text
usage: azarashi [-h] [-f INPUT] [-b BAUDRATE] [--record RECORD] [--time TIME]
                [-s] [-u] [-r] [-x] [-v] [--json] [--english]
                {hex,nmea,ublox,l1s}

azarashi CLI

positional arguments:
  {hex,nmea,ublox,l1s}  message type

options:
  -h, --help            show this help message and exit
  -f, --input INPUT     input serial device or file (default: stdin)
  -b, --baudrate BAUDRATE
                        baud rate of the serial device (default: 9600)
  --record RECORD       append the raw input to this file (default: None)
  --time TIME           time the input was received, e.g. 2026-09-01T12:00:00Z
                        (default: None)
  -s, --source          output the source messages (default: False)
  -u, --unique          supress duplicate messages (default: False)
  -r, --ignore-dcr      ignore dcr messages (default: False)
  -x, --ignore-dcx      ignore dcx messages (default: False)
  -v, --verbose         verbose mode (default: False)
  --json                output one JSON record per line (NDJSON) (default:
                        False)
  --english             output the text in English where the report has it
                        (default: False)
```

Python API：`decode(msg, msg_type='nmea', timestamp=None)`、`decode_stream(stream, msg_type, callback, …, unique=False, ignore_dcr=False, ignore_dcx=True, timestamp=None)`、`reset_reading_state()`、`to_json_dict()` / `to_ndjson()` / `json_schema`。另有 `python -m azarashi.network.transmitter|receiver`（UDP，默认 `ff02::1` 端口 2112）。

上游测试（仓库 clone，`python -m pytest tests`）：**2145 passed, 2 skipped**，10.3 s（跳过：缺 `jsonschema[format]`、缺 `ja_JP.UTF-8` locale）。

## 3. 例子 + 真实输出

**数据来源（均真实，非合成）：** ① 内阁府 QZSS 公开归档 `https://sys.qzss.go.jp/archives/l1s/2026/Q003_20260925.l1s`（PRN 189，UTC 日 = 2026-09-24 20:00 – 09-25 19:59:59 EDT）与 `Q004_20260924.l1s`（PRN 185，2026-09-23 20:00 – 09-24 19:59:59 EDT；含 10:00–12:00 JST = 09-23 21:00–23:00 EDT 训练时段），各 3110401 B；② 上游 `tests/` 的 F9P 记录与 `$QZQSM` 日志。

**3.1 真实震源报（Q003 归档抽出的一帧）**

```bash
echo '$QZQSM,61,C6AD14E6B8000389CC00CD57FFC6EDA54C0150F000000000000000126221FE8*02' \
  | azarashi nmea --time 2026-09-25T21:48:50Z
```

```text
2026-09-25T21:48:50Z --------------------------------
防災気象情報(震源)(発表)(優先)
26日6時23分ころ、地震がありました。
震源の近傍で津波発生の可能性があります。
この地震による日本への津波の影響はありません。

発表時刻: 9月26日6時48分

震央地名: 南太平洋
緯度・経度: 南緯21度12分0秒 東経168度30分0秒
深さ: 不明
マグニチュード: 7.0

Encountered EOF
```

即 2026-09-25 17:23 EDT（06:23 JST 9/26）南太平洋 M7.0，JMA 17:48 EDT 发报；整条命令 0.077 s。文本里的时刻是 **JST**，对象属性是 UTC（`report_time = 2026-09-25 21:48:00+00:00`）。`--english` / `get_text_en()` 给 “Place name of epicenter: South Pacific Ocean / Magnitude: 7.0”。

**3.2 hex 输入 + 英文（Q004 台风报）**

```bash
echo C6ADE4DEB68005EA0100006800477010D900FA8A1E0000000000001151FDA28 \
  | azarashi hex --time 2026-09-24T00:00:50Z --english
```

```text
JMA-DC Report (Typhoon) (Issue) (Regular)
Report time: 06:45 JST, 24 Sep.
Typhoon number: No. 26
Reference time: 06:00 JST, 24 Sep.
Type of reference time: Analysis
Latitude and longitude: N 17°55´00˝, E 134°50´00˝
Central pressure: 1002 hPa
Maximum wind speed: 20 m/s
Maximum wind gust speed: 30 m/s
```

（节选；另有 Elapsed/Scale/Intensity 三行。）

**3.3 官方整日归档**

```bash
time azarashi l1s -f Q004_20260924.l1s > Q004.txt        # real 3.43 s
azarashi l1s -u --json -f Q004_20260924.l1s > Q004.ndjson  # 145 行
```

| 文件 | 86400 帧中 MT 分布 | 报告数（不去重） | `-u --json` 去重后 |
| --- | --- | --- | --- |
| Q003_20260925 | MT43 21600 / MT44 20160 / MT50 37440 / MT48、49 各 2880 / MT47 1440；CRC 全过 | 41760 | 75：台风 63、海上 10、震源 1、DCX Null 1 |
| Q004_20260924 | MT43 21600 / MT44 20160 / 其余同上 | 41760 | 145：台风 63、南海海槽 27（页）、海上 13、气象 11、海啸 8、降灰 6、DCX 海外 10、洪水 2、EEW/震源/震度/火山/Null 各 1；`test=true` 60 |

训练 EEW 实际输出（Q004，2026-09-24T01:00:14Z = 09-23 21:00 EDT）：`防災気象情報(緊急地震速報)(発表)(訓練/試験)`、`*** これは訓練です ***`、震央 日向灘、M7.2、深さ 10km、震度6弱〜程度以上、長周期地震動階級2、島根…九州 17 区。DCX 海外报为印尼 Tsunami 测试（A2 Indonesia，椭圆中心 5.11284°, 95.769926°，半轴 165.324/90.407 km）。

**3.4 u-blox 记录（上游 `tests/ublox_260924.ubx.gz`，ZED-F9P 实收）：** SFRBX 14570 条 L1S 帧 → azarashi 7039 份报告（Null 3400、气象 1893、南海海槽 386、台风 329、海啸 234、降灰 198、洪水 182、海上 103、震源 90、震度 90、火山 68、EEW 66），0.55 s。

**3.5 UDP 转发（本机回环，未测 IPv6 组播）：** `receiver -b 127.0.0.1 -p 21120` + `transmitter -d 127.0.0.1 -p 21120 -t nmea -f tests/qzqsm_260924.log`：发 72 句，收 72 份报告。

**3.6 Python API（同一归档，真实输出）**

```python
import azarashi
from datetime import datetime, timezone
with open('Q003_20260925.l1s', 'rb') as f:            # 二进制模式
    r = azarashi.decode_stream(f, msg_type='l1s', ignore_dcx=False)   # 无 callback → 只取 1 份
print(type(r).__name__, r.timestamp, r.satellite_prn, r.message_type)
# NullMsg 2026-09-25 00:00:00+00:00 189 DCX
r = azarashi.decode('$QZQSM,61,C6AD14E6B8000389CC00CD57FFC6EDA54C0150F000000000000000126221FE8*02',
                    timestamp=datetime(2026, 9, 25, 21, 48, 50, tzinfo=timezone.utc))
r.magnitude, r.seismic_epicenter, r.depth_of_hypocenter   # ('7.0', '南太平洋', '不明')
```

循环读时按三类异常分流：`AzarashiReadOn`（坏帧，继续读）、`AzarashiReopenStream`（设备掉线，重开）、`AzarashiStopReading`（文件读完，实测 `AzarashiNoMoreData`）；`AzarashiFixTheCall` 是调用写错，别吞。

## 4. 交叉检查

自写独立最小解析器（≈60 行，不 import azarashi）：按 IS-QZSS-DCR-017 / DCX-004 取 1-based 比特位——PAB 1–8、MT 9–14、Rc 15–17、Dc 18–21、At 22–41（月 4/日 5/时 5/分 6）、It 42–43、Vn 215–220、CRC-24Q（多项式 0x1864CFB，覆盖前 226 bit）227–250；气象 Ar 54 + 6×(Ww 5, Pl 19)、台风 Bt/Dt/Du/Tn/Sr/Ic/LatLon 41 bit/Pr/W1/W2、海上 8×(Dw 5, Pl 14)、EEW De/Ma/Ep/Ll/Ul/80 bit 区位图；DCX SDMT/SDM + CAMF A1–A17。归档时间字为 `week<<20 | sow`，减 18 s 得 UTC，按时间戳与 azarashi 报告一一配对。

| 数据 | 帧（MT43+44） | 逐字段比对次数 | 差值 |
| --- | --- | --- | --- |
| Q003_20260925.l1s | 41760 | 711952（37 类字段） | **0** |
| Q004_20260924.l1s | 41760 | 695358（46 类字段） | **0** |
| F9P UBX（pyubx2 1.3.7 拆 SFRBX → 自写解析） | 7039 | 99405 | **0**；pyubx2 抽出的 250 bit 与 azarashi `message` 7039/7039 逐位相等、svId 顺序一致 |
| 上游 3 份 `$QZQSM` 日志 | 333 | 5242 | **0**；NMEA 校验 333/333、CRC-24Q 333/333 |

独立来源对照：上游 F9P 实收日志 `qzqsm_260924.log` 72 句中 **71** 句在官方 Q004 归档里逐字出现；缺的 1 句来自卫星 61（PRN 189），不在 Q004。第一次比对时海上报出现 300/765 处“差值”，原因是我按 `Dw≠0` 过滤；规格写明空槽是 Dw 与 Pl **都**为 0，而 Dw=0 是有效码——改按 `Pl≠0` 后归零（azarashi 正确）。

## 5. 错误用例（全部合成；由真实台风帧改位并重算 CRC/NMEA 校验）

| 用例 | 结果 |
| --- | --- |
| 坏 CRC（翻第 100 bit） | `AzarashiInvalidMessageError: CRC Mismatch`（继承 `AzarashiReadOn`） |
| 坏 NMEA 校验 / 截断 40 位 hex / 无 `*CK` | `Checksum Mismatch, should be 0B` / `Too Short Sentence` |
| **错误前导 0x00（CRC 重算）** | **静默成功**，照常出台风报，只在 `report.preamble='Undefined Preamble (Code: 0)'` |
| MT=50、MT=0 | `Undefined Message Type: 50` / `0` |
| Dc=7（Unused）、Dc=15 | `Undefined Disaster Category: 7` / `15` |
| Vn=2；At 月=15 | `Unsupported JMA-DC Report Version: 2`；`Invalid Report Time: 15 as month` |
| 未知地区码（气象 Pl=524287）/ DCX A2=511、A4=127 | **不报错**：`府県予報区(コード番号：524287)`、`Undefined Country/Region (Code: 511)`、`UNDEFINED (Code: 127)` |
| 随机 63 hex | `CRC Mismatch`；随机体+补 CRC+强制 MT43 → `Unsupported JMA-DC Report Version: 18` |
| 空串、hex 空 / 非十六进制 `ZZZ…` | `Empty Message` / `Invalid Message` |
| 非法 `msg_type` | `AzarashiUnsupportedFormatError`（`AzarashiFixTheCall`，不应在循环里吞掉） |
| u-blox 随机 50 B | `Unknown Message Header` |
| `.l1s` 截到 1000 B | 前 27 条记录出 14 份报告，尾部半条**静默丢弃**，exit 0 |
| `.l1s` 中间删 5 B | 1 条 `Record Out of Step After GPS Week 2437 Second 345717`，随后自动重同步，余 193 份报告 |
| `-f /dev/ttyNOPE`（路径不存在） | 被当串口打开 → `SerialException` 回溯，exit 1 |

无崩溃（除串口路径）。CLI 遇坏帧只在 **stderr** 打 `# [AzarashiInvalidMessageError] …` 并继续，最终 exit **0**。

## 6. I/O

- 输入：见 §1；文件建议 `open(path, 'rb')`（文本模式遇坏字节会抛 `UnicodeDecodeError`）。
- 文本输出：每报一块，首行 `<UTC 接收时刻>Z ----…`；`-s` 附原句，`-v` 详细。`Encountered EOF` 走 stderr，属正常结束。
- NDJSON（`--json`）：`schema_version=1`、`type`（如 `qzss.dcr.typhoon`、`qzss.dcx.outside_japan`）、`test`、`received_at`、`satellite{system,prn}`、`nmea`、`text`、`text_en`、`data{…}`；码值为 `{scheme, code, recognized, labels{ja,en}}`。不可与 `-v`/`-s` 同用。
- 对象：`get_params()` 深拷贝；`*_raw` 原码、`*_en` 英文、`*_no` 分支号；时间属性均为带时区 UTC。

## 7. 坑

1. **API 与 CLI 默认不同**：`decode_stream()` 默认 `ignore_dcx=True`（丢 DCX），CLI 两者都出。
2. **不校验前导码**：错前导 + 合法 CRC 照样解出；要严格就自己查 `report.preamble`。
3. **缺年/日要靠接收时刻补**：DCR 无年，DCX 只有星期+时刻；回放旧记录不加 `--time` 会用“现在”（上游 9-24 日志不加时首行是 `2026-09-26T09:36:22Z`）。`.l1s` 用记录内 GPS 时，不能给 `timestamp`。
4. **一帧一报**：单星上同一报重播间隔中位 32 s（常见 32/36 s，高优先级 4 s），整日 41760 份；统计/告警用 `-u` 或 `unique=`（只记最近 256 条；`unique` 对 DCX 忽略 SD 字段）。
5. **自写去重别按整帧**：bit 221–226（Reserved）在重播间变化（Q003 一条震源报出现 16 种整帧），前导码也在 0x53/0x9A/0xC6 间轮换；azarashi 的 `raw` 取 DCR bit 9–220、DCX bit 25–220，按它去重得 Q003 74 条 DCR + 1 DCX = 75，与 `-u` 一致。
6. **未知码不抛异常**（灾种 Dc 除外）：地区码、DCX 国家/灾种码越界只变成“(コード番号：N)”名；下游要看 `recognized` 或 `*_raw`。
7. **文本时区混用**：DCR 文本 JST，西北太平洋海啸与 DCX 文本 UTC；机器处理只用属性/JSON。
8. **exit code 不反映坏帧**：坏 CRC、截断全是 exit 0 + stderr；`-f` 写错路径才 exit 1（当串口）。
9. **hex 严格 63 位**：从 `.l1s`/SBF 抽的 32 B（64 位）要右移 4 bit 截成 63 位，否则 `Too Long Sentence`。
10. **只认 u-blox/Spresense**：其它厂商 L1S 原始帧需自写抽取；u-blox 还要开 `CFG-MSGOUT-UBX_RXM_SFRBX_*` 并启用 QZSS L1S（上游 docs/preparation.md，未测）。
11. 归档时间字不是秒计数而是 `week<<20 | sow`，自写解析易错 2^20 倍。

## 8. 未测

真接收机（u-blox 串口、Spresense）实时读取、`--record`、IPv6 组播转发、Python 3.11/3.12/3.14、`ruff`/`mypy`/`pyright`、JSON Schema 校验（缺 jsonschema）、西北太平洋海啸（Dc 6）实帧。

## 9. 选型

| 需求 | 用 |
| --- | --- |
| 把災危通報 DCR/DCX 变成可读文本/NDJSON/Python 对象 | **azarashi** |
| 同一 `.l1s` 看 SLAS 改正（MT47–51）或 L6 CLAS/MADOCA | [qzsl6tool](./qzsl6tool.md)（L1S 也能逐帧显示） |
| 只拆 u-blox UBX 层（SFRBX dwrd）、配置接收机 | [pyubx2](./pyubx2.md) / [pyubxutils](./pyubxutils.md) / [pygnssutils](./pygnssutils.md)；Rust → [ublox](./ublox.md) |
| NMEA 通用解析（是否认 `$QZQSM` 未测；不解灾害报文） | [pynmeagps](./pynmeagps.md) / [gpsd](./gpsd.md) |
| Septentrio SBF 拆包（能否取到 L1S 原始块未测） | [pysbf2](./pysbf2.md)，自抽 250 bit 转 63 位 hex 再喂 azarashi |
| 其它导航电文完整性/认证（Galileo OSNMA） | [galileo-osnma](./galileo-osnma.md) |
