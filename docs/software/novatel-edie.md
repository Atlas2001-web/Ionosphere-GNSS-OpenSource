# novatel_edie · NovAtel 官方 OEM 日志编解码库（EDIE）操作手册

目录：[`PROJECTS.json` → `novatel_edie`](../../PROJECTS.json) · 上游 <https://github.com/novatel/novatel_edie> · PyPI **`novatel-edie` 2.10.11**（2026-09-09 13:53 EDT 上传；wheel 内核自报 `Version: 3.11.11`，`GIT_SHA` 全 0）· GitHub main tip **`6db1f00`**（2026-09-25 18:23 EDT，打了 tag `CPP-v3.11.14`/`Python-v2.10.14`，**PyPI 未跟上**；GitHub「Release」页最新仍是 **CPP-v3.9.47**（2026-03-31），新版本只打 tag）· MIT · ★**32** · Requires-Python ≥3.8，但 wheel 只有 cp39/cp310/cp311 + cp312-abi3，平台 **manylinux x86_64/aarch64 + win_amd64**，**无 macOS wheel、无 sdist** · 本机 CPython 3.13.5 + g++ 14.2/CMake 3.31/Conan 2.32 · 实测 2026-09-26 02:47–02:59 EDT

> 岗位：**把 NovAtel OEM4/OEM6/OEM7 接收机的 ASCII / 简化 ASCII / 二进制日志解帧、解码、互转**（含 RANGECMP 解压、命令编码）。C++17 库 + nanobind Python 绑定，消息定义来自一份 JSON 库。冲突时：**源码 / `.pyi` 存根 > 上游 README > 本文**。
> **本机无 NovAtel 接收机**：真实数据只用两份公开文件（见 §3.1），错误用例的输入是**合成**的（在真帧上改字节）。

## 1. 用途与边界

**做：** `Framer` 在字节流里找 NovAtel 帧（二进制 `AA 44 12`、短二进制 `AA 44 13`、`#` ASCII、`%` 短 ASCII、`<` 简化 ASCII 应答，另外也能认出 NMEA 帧）；`Decoder` 按 JSON 库解头和体；`Parser`/`FileParser` 把上面串成迭代器；`Message.to_ascii()/to_binary()/to_abbrev_ascii()/to_flattened_binary()/to_json()/to_dict()` 互转；`RangeDecompressor` 把 RANGECMP/2/3/4/5 解压成 RANGE；`Commander` 把简化 ASCII 命令编成 `#…A` / 二进制命令帧；`Filter` 按消息名/ID/时间/时间状态/抽稀筛选；`RxConfigHandler` 拆 RXCONFIG。

**不做：** **不是定位解算器**（BESTPOS 只是把接收机自己算好的解读出来）；**不输出 RINEX**（要 RINEX 用 RTKLIB `convbin -r nov`，§4.3）；不解 NMEA 语句内容（NMEA 帧只按「未知字节」吐出）；不开串口、不做 NTRIP（上游 `serial_connection.py` 只是 pyserial 示例）；不认别家协议（UBX/SBF/RTCM 当垃圾字节）；PyPI 包带的 `novatel_edie` 命令行**只有** `generate-stubs` / `install-custom`（按自定义库生成存根/安装），**没有**解码/转换 CLI——转换 CLI 只在 C++ `examples/` 里。

| 名词 | 含义 |
| --- | --- |
| OEM4 帧 | NovAtel 二进制：28 B 头（同步 3 B + 头长 + msgID + 消息类型字节 + 端口 + 长度 …）+ 体 + CRC32 |
| 消息类型字节 | bit7 应答标志，bit5–6 格式；OEM7 把 **bit0–4 当 measurement source**（0 主天线/1 副天线） |
| RANGECMP | RANGE 的压缩版（每观测 24 B），需解压才得伪距/载波/多普勒 |
| 合成 | 本文人为构造或改写的输入，非接收机原样输出 |

## 2. 安装

```bash
python3 -m venv /tmp/edie-man/venv
/tmp/edie-man/venv/bin/pip install novatel-edie          # 2.10.11，带 database.json（5 356 825 B）
/tmp/edie-man/venv/bin/pip install typing_extensions     # 仅 CLI 需要，见坑 1
/tmp/edie-man/venv/bin/python -c "import novatel_edie as ne; print(ne.CPP_PRETTY_VERSION)"
# Version: 3.11.11 / Branch: / SHA: 0000000000000000 0000000000000000 0000-00-00T00:00:00
```

- 消息库：包内 `novatel_edie/database.json` 与上游 `database/database.json` **逐字节相同**（`cmp`），**606 条消息定义 + 255 个枚举**，meta `{"subset":"all","messageFamily":"OEM"}`。
- Python 公开类（`dir(novatel_edie.oem)`）：`Framer` `Decoder` `Filter` `Parser` `FileParser` `Commander` `RangeDecompressor` `RxConfigHandler` `Message` `UnknownMessage` `Response` `Header` `MetaData` `GpsTime`；顶层还有 `FramerManager` `MessageDatabase` `STATUS` `ENCODE_FORMAT` `HEADER_FORMAT` `calculate_crc` 与一串 `*Exception`。**Python 没有独立 `Encoder` 类**（C++ 有 `encoder.hpp`），编码就是 `Message.encode(fmt)`。
- C++（试了一次，成功）：`cmake -S src -B build -DBUILD_TESTS=OFF -DBUILD_EXAMPLES=ON && cmake --build build -j8`，Conan 自动拉依赖并从源码编 gtest 等，02:51:57→02:53:42 EDT 完成；产物 `build/bin/linux-x86_64-gnu-Release/` 下 `libedie_common.a` `libedie_decoders_common.a` `libedie_oem_decoder.a` 与 8 个示例（`converter_file_parser` `converter_parser` `range_decompressor` `command_encoding` `json_parser` `rxconfig_handler` …）。`CONAN_HOME` 指到自己的目录，别污染共享 box。

## 3. 可运行示例 + 真实 stdout

### 3.1 数据来源

| 文件 | 来源 | 内容 |
| --- | --- | --- |
| `oemv_200911218.gps`（262144 B，sha256 前 12 位 `65c4e666c735`） | RTKLIB 仓库 `test/data/rcvraw/`，分支 `rtklib_2.4.3` = `180043e`（BSD-2，免账号） | **NovAtel OEMV 二进制**，2009-12-18 23:07:00–23:07:45 GPST，日本；被截在 256 KiB，末帧残缺 |
| `BESTPOS.GPS`（217002 B） | 上游 `benchmarks/resources/`，commit `6db1f00` | OEM7 ASCII `#BESTPOSA` ×1000，2018 周 1984 |

上游仓库**没有** RANGE/RANGECMP/星历真样例（`regression/` 只有 1 条 BESTUTM，`src/decoders/oem/test/resources/*sync_error*` 是 `FAKELOG` 测试帧），所以观测数据只能用 RTKLIB 的 OEMV 文件。

### 3.2 计数（`count.py`：`FileParser` 迭代，按类型计数）

```python
import sys, collections, novatel_edie as ne, novatel_edie.oem as oem
c = collections.Counter()
for m in oem.FileParser(sys.argv[1]):
    if isinstance(m, oem.Message):          k = m.name
    elif isinstance(m, oem.UnknownMessage): k = f"Unknown(id={m.header.message_id})"
    elif isinstance(m, ne.UnknownBytes):    k = "UnknownBytes"
    c[k] += 1
for k, v in sorted(c.items()): print(f"{k:28s}{v}")
```

`oemv_200911218.gps` 原样输入：

```text
BESTPOS                     49
GLOEPHEMERIS                8
RANGECMP                    46
RAWEPHEM                    25
SATVIS                      49
TRACKSTAT                   50
Unknown(id=287)             90
UnknownBytes                7
```

- **RANGECMP 没被解压**（`decompress_range_cmp` 默认就是 `True`）。原因是 OEMV 在消息类型字节写了 `0x02`，EDIE 按 OEM7 规则把它读成 measurement source = 2，内部解压过滤器只放行 PRIMARY/SECONDARY → 直接跳过解压；手动 `RangeDecompressor.decompress()` 则抛 **`UnsupportedException`（STATUS.UNSUPPORTED）** ×46。转 ASCII 时头名也会带上后缀：`#RANGECMPA_2,SPECIAL,0,35.5,FINESTEERING,1562,515220.000,…`。
- id 287 是 OEMV 时代的 RAWWAASFRAME，OEM7 库里已没有这个 ID → `UnknownMessage`（带 52 B 原始体）。
- 7 段 `UnknownBytes` 共 40 B = 接收机提示符 `[USB1]\r\n` 等；另有 5 条 `<OK` 应答被 `FileParser` 默认**直接丢掉**（`ignore_abbreviated_ascii_responses=True`；用 `Framer` 能看到 `ABB_ASCII b'<OK\r\n'`）。
- 按 ID 扫描原始字节有 9 条 GLOEPHEMERIS（723），解出 8 条：第 9 条被 256 KiB 截断。
- 本文件里**没有** TIME、GPSEPHEM、RANGE 原帧，所以这几类无法做真实对照。

**把 317 帧的类型字节 `0x02→0x00` 并用 `ne.calculate_crc` 重算 CRC**（`patch.py`，得 `oemv_src0.gps`，只改头、不动体；属改写输入）后再跑：

```text
BESTPOS                     49
GLOEPHEMERIS                8
RANGE                       46
RAWEPHEM                    25
SATVIS                      49
TRACKSTAT                   50
Unknown(id=287)             90
UnknownBytes                7
```

`message_counts` 仍记为 `(140, HEADER_FORMAT.BINARY, 0): 46`，即按原始 ID 计数。46 条 RANGE 共 **1380** 条观测：GPS L1C/A 414、GPS L2P(Y) 414、GLONASS L1 230、GLONASS L2P 230、SBAS L1 92（按 `c_status` bit16–18 系统、bit21–25 信号统计）。

### 3.3 字段读取（真实 stdout）

```text
RANGE 首观测 dict: {'sv_prn': 3, 'sv_freq': 0, 'psr': 20213930.640625, 'sd_psr': 0.05000000074505806,
  'adr': -106224932.51171875, 'sd_adr': 0.005859375, 'dop': -1140.2265625, 'C_No': 51.0,
  'lock_time': 14247.375, 'c_status': 403741700}
#RANGEA,SPECIAL,0,35.5,FINESTEERING,1562,515220.000,00000800,9691,4807;30,3,0,20213930.641,0.050,-106224932.511719,0.006,-1140.227,51.0,14247.375,18109c04,…
BESTPOS 1562 515220.0 0 18 35.872994185 138.389661698 964.6399 16 9
RAWEPHEM {'prn': 11, 'week': 1562, 'toe': 518400, 'sub_frame1': 'len30', 'sub_frame2': 'len30', 'sub_frame3': 'len30'}
GLOEPHEMERIS [('sloto', 51), ('freqo', 0), ('sat_type', 1), ('false_iod', 18), ('ephem_week', 1562), ('ephem_time', 515715000), ...]
```

BESTPOS 那行依次是 周、周内秒、`solution_status`、`position_type`、纬度（°）、经度（°）、`orthometric_height`（m）、跟踪星数、参与解算星数。它和 BESTPOS.GPS（OEM7）用的**字段名不同**：OEMV 库版本给 `orthometric_height`，OEM7 BESTPOS 给 `height`——同名消息按头里的 CRC 选定义（坑 6）。`BESTPOS.GPS` 首条：`BESTPOS 1984 450849500.0 16 51.1163704936 -114.03827102462 1059.7447`，`to_json()` 开头为 `{"header": {"message": "BESTPOS","id": 42,"port": "COM1",…,"week": 1984,"seconds": 450849.500,…`。

## 4. 格式转换与核对

### 4.1 往返（`roundtrip.py`：原帧 → `to_*` → `Decoder.decode` → 逐字段比 `to_dict`）

| 路径 | 结果 |
| --- | --- |
| 二进制 → `to_binary()` | 227/227 帧**与原帧逐字节相同**（6 类消息） |
| 二进制 → ASCII → 二进制 → ASCII | 227/227 文本相同（ASCII 输出是稳定的） |
| 二进制 → ASCII / 简化 ASCII → 解码 | RAWEPHEM、GLOEPHEMERIS 全等；其余类别有舍入：RANGE 最大差 **0.00098**（`sd_adr` 0.005859375→0.006），TRACKSTAT 0.0005 Hz，BESTPOS 4.2×10⁻⁵ m，SATVIS 仰角 0.05° |
| OEM7 ASCII（BESTPOS.GPS）→ `to_ascii()` | 1000/1000 与原行逐字节相同；ASCII→二进制→ASCII 1000/1000 相同 |
| `to_json()` | 227/227 能被 `json.loads` 解析；结构为 `{"header":{…},"body":{…}}` |

结论：**只有二进制是无损的**，ASCII 按固定小数位输出，有舍入。

### 4.2 C++ 与 Python 一致

`converter_file_parser src/database/database.json cpp_in.gps ASCII`（输入即 `oemv_src0.gps`）输出 `Converted 227 logs in 4ms`，得到 `cpp_in.gps.ASCII` **404183 B**，与 Python `to_ascii()` 拼接的结果**逐字节相同**（C++ 用的是 tip 3.11.14，wheel 是 3.11.11）；`.UNKNOWN` 文件 0 B（id 287 那 90 帧属于 NO_DEFINITION，不会写进去）。

### 4.3 RANGECMP 解压 vs RTKLIB convbin（独立工具交叉核对）

```bash
convbin -r nov -v 3.02 -od -os -o rtk.obs -n rtk.nav oemv_200911218.gps   # Debian rtklib 2.4.3 b34，读原始文件
```

RINEX 观测 46 历元（23:07:00–23:07:45 GPST），类型 G `C1C L1C D1C S1C C2W L2W D2W S2W` / R `…C2P L2P…` / S `C1C L1C D1C S1C`。`cmp_rinex.py` 把 EDIE 解压出的每条 RANGE 观测按（历元、卫星、频段）对到 RINEX：

```text
RANGE obs matched 1380 unmatched 0 epochs 46
max|C-psr| m=0.0005  max|L+adr| cyc=0.0005  max|D-dop| Hz=0.0005
```

也就是 1380/1380 全部对上，差值只来自 RINEX 保留 3 位小数；载波相位符号满足 RINEX $L = -\mathrm{ADR}$。星历方面：RAWEPHEM 的 9 颗 PRN（3/6/7/8/11/13/16/19/22，toe = 518400 s）与 `rtk.nav` 的 GPS 集合相同；GLOEPHEMERIS 的 `sloto` 50/51/52/54/60 减 37 后为 R13/R14/R15/R17/R23，也与 `rtk.nav` 的 GLONASS 集合相同。

## 5. 错误用例（`errors.py`；输入全部是**合成**的，基于真帧改写）

Python 层把 STATUS 映射成异常：`BUFFER_EMPTY`→`BufferEmptyException`、`INCOMPLETE`→`IncompleteException`、`UNSUPPORTED`→`UnsupportedException`、`NO_DEFINITION`→`NoDefinitionException`、`MALFORMED_INPUT`→`MalformedInputException`，JSON 读失败→`JsonDbReaderException`。`Parser` 开了 `return_unknown_bytes=True`。**全部用例都没有崩溃、没有 segfault。**

| 用例 | `Parser.read()` 序列 | 底层 |
| --- | --- | --- |
| 正常 ASCII / 二进制 BESTPOS | `BESTPOS` → BufferEmpty | — |
| ASCII 坏 CRC（单独） | 立刻 BufferEmpty，217 B **留在缓冲区**等更多数据 | Framer：`IncompleteException` |
| ASCII 坏 CRC + 好帧 | `UnknownBytes(217B)` → `BESTPOS` | 能重新同步 |
| 二进制坏 CRC | `UnknownBytes(104B)` | Framer `UNKNOWN:104B`；**`Decoder.decode()` 不校验 CRC**，照样解码 |
| 截断（ASCII 60 B / 二进制 40 B） | 单独：BufferEmpty，字节留缓冲；后接好帧：`UnknownBytes` → `BESTPOS` | Framer（测了二进制）：`IncompleteException` |
| 帧前 6 B 垃圾 | `UnknownBytes(6B)` → `BESTPOS` | — |
| 未知 ID 9999（CRC 正确） | `UnknownMessage(id=9999)` | Framer `BINARY:104B`（STATUS NO_DEFINITION，不抛异常） |
| NMEA GGA（校验和对/错都试） | 都是 `UnknownBytes(72B)` | Framer（校验和正确的那条）认出 `NMEA:72B`，但不解码 |
| UBX 帧头 + 垃圾 | `UnknownBytes(100B)` | — |
| 空消息库（`MessageDatabase.from_string` 放空列表） | 正常 BESTPOS 帧 → `UnknownMessage(id=42)` | — |
| 库路径不存在 / JSON 残缺 | `JsonDbReaderException`（信息里带 `/project/src/...json_db_reader.cpp` 行号） | — |
| `FileParser('/不存在')` | **不报错**，迭代结果为空 `[]` | 坑 4 |
| `Commander.encode(b'NOTACOMMAND 1')` | `NoDefinitionException` | — |

## 6. I/O 表

| 输入 | 组件 | 输出 |
| --- | --- | --- |
| 文件路径 | `FileParser(path[, db])` | 迭代出 `Message` / `UnknownMessage` / `UnknownBytes`（/ `Response`） |
| 任意字节块 | `Parser.write()` + `read()` / 迭代 | 同上；`flush(return_flushed_bytes=True)` 取出残留 |
| 字节块 | `Framer.write()` + 迭代 | `(frame_bytes, MetaData)`；`meta.format` ∈ BINARY/SHORT_BINARY/ASCII/SHORT_ASCII/ABB_ASCII/NMEA/UNKNOWN… |
| 单帧 | `Decoder.decode()` / `decode_header` + `decode_payload` | `Message` / `Response` / `UnknownMessage` |
| `Message` | `to_ascii` / `to_abbrev_ascii` / `to_binary` / `to_flattened_binary` / `to_json` / `to_dict` | `MessageData.message`（bytes）或 dict |
| RANGECMP 帧 + MetaData | `RangeDecompressor.decompress(frame, meta, fmt)` | RANGE（接口标注 unstable，构造时打印警告） |
| 简化 ASCII 命令 | `Commander.encode(cmd, fmt)` | `#…A` 命令行或二进制命令帧（`FRESET STANDARD` → 36 B） |
| JSON 库 | `MessageDatabase(path)` / `from_string` / `merge` / `append_messages` | 自定义库，可传给上面各组件 |

## 7. 坑

1. **CLI 在干净 venv 起不来**：`novatel_edie --help` 报 `ModuleNotFoundError: No module named 'typing_extensions'`（`stubgen.py` 用到了它，元数据只声明了 `typer>=0.15`、`importlib_resources`）。手动 `pip install typing_extensions` 即可；况且 CLI 也不能解码。
2. **老接收机的 RANGECMP 会静默不解压**：OEM4/OEMV 类型字节 bit0–4 非 0 时，`FileParser` 照样吐 RANGECMP，不报错也不记日志（内部解压过滤器直接跳过）。可以改写类型字节再重算 CRC（§3.2），或者直接改用 RTKLIB。同理，转 ASCII 时头名会带 `_2` 后缀（`#BESTPOSA_2`），别的工具不一定认。
3. **ASCII 有损**：需要无损就用二进制 / `to_dict`；RANGE 的 `sd_adr` 等字段转 ASCII 后会被舍入。
4. **缺文件时静默为空**：`FileParser` 接受不存在的路径，迭代结果就是空的。先自己 `os.path.exists`。
5. **FileParser 默认丢 `<OK` 这类应答**；要看到命令应答，设 `ignore_abbreviated_ascii_responses=False` 或者直接用 `Framer`。
6. **同名消息字段名会随定义版本变**：OEMV 的 BESTPOS 给 `orthometric_height`，OEM7 给 `height`（按头里的定义 CRC 选）；写代码时用 `to_dict().get()` 兜底。
7. **GLONASS PRN 带 +37 偏移**（RANGE `sv_prn` 取 38–61，槽号 = PRN − 37），SBAS 用原始 PRN 120–158（RINEX `Sxx` = PRN − 100）；转 RINEX 编号前要先换算。
8. **`Decoder` 不校验 CRC**，CRC 只在 Framer 层检查。绕过 Framer 直接喂帧时，坏帧会被当成好帧解出来。
9. **`Commander` 不补默认参数**：`LOG COM1 BESTPOSB ONTIME 1` 抛 `MalformedInputException`，必须写全 `… ONTIME 1.0 0.0 NOHOLD`。
10. `header.milliseconds` 是 float 毫秒；属性访问拿到的 `position_type` 是 int（16），`to_dict()` 里则是枚举 `SolType.SINGLE`。
11. 版本口径有三套：PyPI 2.10.11 / wheel 内核 3.11.11 / GitHub tag 已到 3.11.14，而 Release 页停在 3.9.47。引用时写清是哪一个。wheel 的 `GIT_SHA` 全 0，追不到 commit。
12. C++ 示例会在当前目录写 `default.log` 滚动日志；参数顺序是「库 JSON、输入、格式」。
13. 部分脚本退出时 stderr 偶尔打印 `nanobind: leaked N instances!`（本机在 Framer/Decoder 混用时见到），结果不受影响。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 解 / 转 NovAtel OEM7 日志（ASCII↔二进制↔JSON），或写 NovAtel 命令 | **本文 EDIE** |
| NovAtel（含 OEM4/OEMV 老格式）→ RINEX，或直接做 SPP/RTK | RTKLIB `convbin -r nov` / `rnx2rtkp`（[rtklib](./rtklib.md)；本文交叉核对用的就是它） |
| ROS 里实时接 NovAtel | `novatel_oem7_driver`（PROJECTS 已登记，本目录暂无手册） |
| u-blox UBX（厂商协议同类） | [pyubx2](./pyubx2.md)（Python）· [ublox](./ublox.md)（Rust）· 转 RINEX 用 [ubx2rinex](./ubx2rinex.md) |
| Septentrio SBF | [sbfparser](./sbfparser.md)（官方 Cython）· [pysbf2](./pysbf2.md)（纯 Python） |
| Swift SBP | [libsbp](./libsbp.md) |
| 串口守护进程 / 多客户端 JSON（NMEA 与部分二进制协议） | [gpsd](./gpsd.md) |
| RTCM3 | [pyrtcm](./pyrtcm.md) · [rtcm-rs](./rtcm-rs.md) |

## 9. 未测 / 复现

未测：真实 NovAtel 接收机（串口 / `Commander` 命令下发）；RANGECMP2/3/4/5 与 OEM7 原生 RANGE（缺公开样例，所以无法拿「同历元 RANGE vs RANGECMP」做对照，改用 convbin 核对）；TIME、GPSEPHEM、短二进制头、RXCONFIG 真数据；`FramerManager` 多协议混流；`install-custom` 自定义库；C++ 单元测试（本次构建时 `BUILD_TESTS=OFF`）；Windows/aarch64 wheel。

复现脚本（都在 `/tmp/edie-man/w`，事后已清理）：`count.py` `patch.py` `roundtrip.py` `bytes_rt.py` `cmp_rinex.py` `errors.py`；数据用 §3.1 的两个 URL 重新下载即可。

[rtklib.md](./rtklib.md) · [pyubx2.md](./pyubx2.md) · [ublox.md](./ublox.md) · [sbfparser.md](./sbfparser.md) · [pysbf2.md](./pysbf2.md) · [libsbp.md](./libsbp.md) · [gpsd.md](./gpsd.md) · [pyrtcm.md](./pyrtcm.md) · [README.md](./README.md)
