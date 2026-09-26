# micropyGPS · 纯 Python / MicroPython 逐字符 NMEA 解析器操作手册

目录：上游 <https://github.com/inmcm/micropyGPS>（Calvin McCoy / inmcm）· 单文件 `micropyGPS.py`（830 行，零依赖）· master tip **`f6c2b76`**（2022-01-06 20:38 PST，「Fix timestamp tests」；GitHub `pushed_at` 2023-02-18 只是 PR #47 的引用更新，**master 自 2022-01 起无提交**）· **MIT** · ★**391** / fork 116 · 无 tag / 无 release · **PyPI 无此包**（`micropyGPS`/`micropygps` 等名字均 404，`setup.py` 自称 1.0 但从未上传；有人上传的同名/非官方包本机没查到，出现了也别当官方）· 开着的 PR 6 个（#31 加 GLGSV/GAGSV、#46 忽略 talker 等，都未合并）· 本机实测 2026-09-26 01:34–01:40 EDT：**CPython 3.13.5** + **MicroPython 1.25.0 unix port**（Debian `micropython_1.25.0+ds-1` 解包到临时目录运行，没装进系统），两边输出除浮点末位外逐字一致；上游 `test_micropyGPS.py` pytest **9 passed**；MCU 真板**未测**。

> 岗位：**串口上一个一个来的字符 → 一个会自己更新的「当前 GPS 状态」对象**（时间、日期、经纬度、高度、速度、DOP、可见卫星）。冲突时：**本机源码 > 上游 README > 本文**。  
> **解析器 ≠ 定位解算器 ≠ 串口驱动。** 位置是接收机自己算好写进句子的，本库只抄字段；它**不开串口**，MicroPython 上的 `machine.UART` 读取循环要你自己写（§2）。C 同类 → [minmea](./minmea.md) / [libnmea](./libnmea.md)；桌面 Python → [pynmeagps](./pynmeagps.md) / [pynmea2](./pynmea2.md)；Rust → [nmea-parser](./nmea-parser.md) / [nmea-rs](./nmea-rs.md)；守护进程 → [gpsd](./gpsd.md)。

## 1. 用途与边界

**做：**

- `MicropyGPS.update(char)`：每次喂**一个字符**（长度 1 的 `str`），句子校验和通过且句型受支持时返回句头字符串（如 `'GNGGA'`），其余情况返回 `None`
- 支持句头**只有 17 个**（`supported_sentences` 字典）：`GP`/`GL` × RMC/GGA/VTG/GSA/GSV/GLL，外加 `GNGGA`/`GNRMC`/`GNVTG`/`GNGLL`/`GNGSA`
- 解析结果写进对象属性（覆盖式，只留最新值）；计数器 `clean_sentences`（校验和通过）、`parsed_sentences`（解析成功）、`crc_fails`
- 坐标三种表示：`'ddm'`（默认，度+分）、`'dd'`（十进制度）、`'dms'`（度分秒，秒取整）；本地时区偏移 `local_offset`
- 辅助：`latitude_string()`、`date_string()`、`speed_string()`、`compass_direction()`、`time_since_fix()`、`satellite_data_updated()`；`start_logging()` 把收到的字符原样写文件

**不做：**

- **不开串口**、不读 TCP/NTRIP；**不做定位解算**，不用 GSV/GSA 自己算 DOP
- **不认** `$GA…`/`$GB…`/`$BD…`/`$GN…GSV`、GST、GBS、ZDA、TXT、`$PUBX` 等：校验和对了也只 `clean_sentences += 1`，不解析
- 不认 `!AIVDM`（只认 `$` 开头）；不解 UBX/RTCM 二进制 → [pyubx2](./pyubx2.md) / [ublox](./ublox.md)
- **不能生成 NMEA**：没有 encode / 拼句 / 算校验和的公开 API，`start_logging()` 只是回写收到的原文
- 不按句返回对象：想拿「这一句」的字段，只能在 `update()` 返回句头的那一刻去读属性

## 2. 安装

```bash
# CPython：没有 PyPI 包，钉 commit 从 GitHub 装（本机 venv 实测可装，pip 显示 micropyGPS 1.0）
pip install "git+https://github.com/inmcm/micropyGPS@f6c2b76a3bedf7d85e77fc6d52e0346b68361ce2"
# 或直接复制单文件
curl -O https://raw.githubusercontent.com/inmcm/micropyGPS/f6c2b76a3bedf7d85e77fc6d52e0346b68361ce2/micropyGPS.py
```

MicroPython 板子：把 `micropyGPS.py` 拷到板上文件系统（如 `mpremote cp micropyGPS.py :`，**本机未连板，未测**）。UART 循环要自己写，下面是写法示意（**未在真板运行**）：

```python
from machine import UART
from micropyGPS import MicropyGPS
uart = UART(1, 9600)             # 引脚/波特率按板子和接收机改
gps = MicropyGPS(location_formatting='dd')
while True:
    buf = uart.read()            # 返回 bytes 或 None
    if buf:
        for b in buf:            # 迭代 bytes 得到 int，必须 chr()，否则 TypeError（§4）
            try:
                t = gps.update(chr(b))
            except IndexError:   # 字段不全的句子会抛出（坑 #5）
                t = None
            if t == 'GNGGA':
                print(gps.latitude, gps.longitude, gps.altitude)
```

## 3. 端到端（本机真跑；2026-09-26 01:34–01:40 EDT）

### 3.1 真实输入：gpsd 回归测试日志

与 [nmea-parser](./nmea-parser.md)、[nmea-rs](./nmea-rs.md) 用**同一批**：`https://gitlab.com/gpsd/gpsd/-/raw/master/test/daemon/<文件>`（gpsd master **`43362cd2`**，gpsd 本身 **BSD-2-Clause**），均为真实接收机录制：

| 文件 | 大小 | sha256₁₂ | 内容 |
| --- | ---: | --- | --- |
| `ublox-zed-f9p-nmea.log` | 58367 B | `6f99714a2800` | ZED-F9P，NMEA 4.10（GSV 带信号 ID、GSA 带系统 ID），Dunedin，2019-04-12，29 历元 |
| `ais-nmea.log` | 85460 B | `ac2d9f36e457` | GPS NMEA（全 `$GP`）+ `!AIVDM` 混录，2020-04-07 |
| `ublox-zed-f9t-ubx_nmea_l5.log` | 31754 B | `0531482cc9ea` | EVK-F9T，UBX 二进制与 NMEA 混在同一文件，2025-07-31 |

### 3.2 逐字节喂整个文件（`demo.py`，CPython / MicroPython 通用）

```python
import sys
sys.path.insert(0, 'micropyGPS')          # 上游 clone 目录
from micropyGPS import MicropyGPS

gps = MicropyGPS(location_formatting='dd')
n = {}
first = {}
with open(sys.argv[1], 'rb') as f:
    data = f.read()
for b in data:                            # 原始字节，含 UBX 二进制，不做任何切帧
    t = gps.update(chr(b))
    if t:
        n[t] = n.get(t, 0) + 1
        if t == 'GNGGA' and t not in first:
            first[t] = 1
            print('GGA', gps.timestamp, gps.latitude, gps.longitude,
                  gps.altitude, 'm sats', gps.satellites_in_use, 'hdop', gps.hdop)
print('parsed', sorted(n.items()))
print('clean', gps.clean_sentences, 'parsed', gps.parsed_sentences, 'crc_fails', gps.crc_fails)
print('last: date', gps.date, gps.date_string('long'), 'utc', gps.timestamp)
print('lat', gps.latitude_string(), 'lon', gps.longitude_string(), 'alt', gps.altitude, 'm geoid', gps.geoid_height, 'm')
print('in_use', gps.satellites_in_use, 'in_view', gps.satellites_in_view, 'hdop', gps.hdop, 'pdop', gps.pdop, 'vdop', gps.vdop, 'fix_type', gps.fix_type)
print('used', gps.satellites_used)
print('sat_data', sorted(gps.satellite_data.items()))
```

**本机打印（`for f in …; do echo "== $f"; python3 demo.py $f; done`，原样）：**

```text
== ublox-zed-f9p-nmea.log
GGA [0, 39, 56.0] [45.877567166666665, 'S'] [170.50011133333334, 'E'] 14.2 m sats 12 hdop 0.64
parsed [('GLGSV', 174), ('GNGGA', 29), ('GNGLL', 29), ('GNGSA', 116), ('GNRMC', 29), ('GNVTG', 29), ('GPGSV', 174)]
clean 1015 parsed 580 crc_fails 0
last: date (12, 4, 19) April 12th, 2019 utc [0, 40, 24.0]
lat 45.8775655° S lon 170.50011166666667° E alt 14.8 m geoid 1.8 m
in_use 12 in_view 10 hdop 0.73 pdop 1.18 vdop 0.92 fix_type 3
used [13, 12, 22, 19, 8, 21]
sat_data [(65, (53, 144, None)), (66, (58, 305, 34)), (67, (6, 313, None)), (72, (9, 137, 15)), (73, (6, 174, None)), (74, (5, 132, None)), (81, (64, 223, 35)), (82, (13, 214, 33)), (87, (14, 30, None)), (88, (62, 24, None))]
== ublox-zed-f9t-ubx_nmea_l5.log
GGA [19, 33, 34.0] [44.068854, 'N'] [121.314135, 'W'] 1139.9 m sats 12 hdop 0.62
parsed [('GNGGA', 9), ('GNGSA', 45), ('GNRMC', 9), ('GNVTG', 9), ('GPGSV', 45)]
clean 252 parsed 117 crc_fails 10
last: date (31, 7, 25) July 31st, 2025 utc [19, 33, 42.0]
lat 44.068853833333336° N lon 121.314134° W alt 1139.6 m geoid -21.3 m
in_use 12 in_view 8 hdop 0.62 pdop 1.12 vdop 0.94 fix_type 3
used []
sat_data [(8, (37, 282, 22)), (10, (73, 11, 22)), (18, (19, 128, 25)), (23, (36, 68, 37)), (24, (22, 60, 24)), (27, (41, 236, 42)), (28, (1, 165, 29)), (32, (63, 186, 38))]
```

读法：

- F9P `clean 1015` = 全部句子校验和都过；`parsed 580` = GGA/GLL/RMC/VTG 各 29 + GSA 116 + GPGSV 174 + GLGSV 174。差的 **435** 句 = `$GAGSV` 174 + `$GBGSV` 174 + GST 29 + GBS 29 + ZDA 29，**悄悄丢掉**，无任何计数器区分「不支持」
- F9T 逐字节喂**含 UBX 的原始文件**：0 异常，`clean 252` 与 pynmeagps 按行取出的 252 句相等，RMC/GGA **9/9**；`crc_fails 10` 全是 UBX 字节里偶然出现的 `$…*` 残片
- `used`/`sat_data`/`in_view`/`hdop` 都是**最后一句写入的值**：F9P 的 `used` 是第 4 条 `$GNGSA`（系统 ID 4 = 北斗）的 PRN，`sat_data` 是最后一组 `$GLGSV`（GLONASS 信号 3）；F9T 最后一条 GSA 是空表（系统 ID 6），于是 `used []`；`hdop` 首条 GGA 时 0.64，文件末是 GSA 写的 0.73
- `ais-nmea.log`：`clean 1313 parsed 1313`，GGA/GLL/RMC/VTG 各 164、GSA 165、GSV 492；183 句 `!AIVDM` 不以 `$` 开头，**不进任何计数器**
- MicroPython 1.25.0 unix 跑同一脚本：计数、日期、卫星表全部相同，只有浮点末位不同（`45.87756716666667`、`vdop 0.9200000000000001`）；F9P 全文件耗时 CPython 0.04–0.05 s（3 次），MicroPython unix 0.31 s

### 3.3 交叉核对（pynmeagps 1.1.7，`NMEAReader.parse(validate=1)` 逐行；F9T 先取最后一个非 ASCII 字节之后的尾巴）

| 核对 | 结果 |
| --- | --- |
| 逐类句数 | F9P pynmeagps：GP/GL/GA/GB GSV 各 174、GSA 116、GGA/GLL/RMC/VTG/ZDA/GST/GBS 各 29，共 1015 = 本库 `clean`；本库解析的 7 类计数与之逐类相同。AIS 文件 1313、F9T 252 同样相等 |
| GGA（UTC、纬度、经度、高度、卫星数、HDOP；经纬度转带符号十进制度比到 1e-9°） | F9P **29/29**、AIS 文件 **164/164**、F9T **9/9** 全同；首条 `00:39:56, −45.877567167°, 170.500111333°, 14.2 m, 12, 0.64` |
| RMC 日期 | 29/29、164/164、9/9 相同（本库存 `(日, 月, 两位年)`） |
| GSV：每组收齐（`satellite_data_updated()` 为真）时的 PRN 集合 vs pynmeagps 同组 svid | F9P **116/116** 组、AIS **164/164**、F9T **18/18** 组全同；F9P 条目 1276 = 1276，**没有信号 ID 变成的假卫星**；但 F9P 全部 2378 个条目里 GA/GB 的 **1102** 个本库根本不解析 |

### 3.4 三库同文件对照（F9P / F9T；另两库数字取自各自手册）

| 项 | micropyGPS `f6c2b76` | [nmea-parser](./nmea-parser.md) 0.11.0 | [nmea-rs](./nmea-rs.md)（`nmea` 0.8.0） |
| --- | --- | --- | --- |
| F9P GSV 卫星条目 | 1276（只解 GP/GL），**无假星** | 2523（多 **145** 颗信号 ID 假星） | 2378，无假星 |
| NMEA 4.10 信号 ID | 按 `卫星数` 字段算末句星数，末字段不会被当 PRN；ID 本身被丢 | 当 PRN | 丢弃，不当 PRN |
| 北斗 `$GB`/`$BD`、伽利略 `$GA` GSV | **都不认**（只 `clean+1`） | GA 认，`$GB` → `Other` | 都认 |
| GSA 系统 ID | 忽略；4 条 `$GNGSA` 互相覆盖 | 无 | 有，按系统累加 |
| GST / GBS / ZDA | 都不认 | 都 `Unsupported` / ZDA 认 | GST、ZDA 解；GBS 报错 |
| 日期 | 只 RMC 写 `date`；GGA 不碰日期 | GGA 固定 2000-01-01 | GGA 不造日期，融合取 RMC |
| UBX 混流原样喂入 | 逐字节 `chr()` **0 异常**，252/252，RMC 9/9 | lossy 整行 **panic** | 0 panic |
| 小写校验和 / 无校验和 | 接受 / **静默丢弃** | 判坏 / 照收 | 接受 / 拒收 |

## 4. 错误用例（本机实测，CPython 与 MicroPython 结果一致；「真实」= 日志原句，其余为**合成**）

每例用新对象，`→` 后是 `update()` 非 None 返回值与计数器变化：

| 输入 | 结果 |
| --- | --- |
| 真实 `$GNGGA,003956.00,…*56\r\n` | `['GNGGA']`，clean+1 parsed+1；`_latitude=[45, 52.65403, 'S']` |
| 合成：校验和改 `*57` | `[]`，**crc_fails+1**，`sentence_active` 仍为 True（等下一个 `$` 复位） |
| 合成：真实 VTG `*3B` 改小写 `*3b` | `['GNVTG']`——`int(…, 16)` 接受小写 |
| 合成：去掉 `*56` | `[]`，三个计数器都不变——**静默丢弃**；后接真实句能正常解析 |
| 合成：截断到 40 字符（无 `*`）后接真实句 | 只出后面那句 `['GNGGA']`；截断句无痕迹 |
| 合成：截断 GGA `…,S,17030.0` **补上正确校验和** | `[]`，clean+1 parsed+0（`IndexError` 被 GGA 内部吞掉） |
| 合成：同样截断的 RMC / VTG / GLL，及 `$GNGSA,A,3,13,,1.0*2F`，都带正确校验和 | **`update()` 直接抛 `IndexError: list index out of range`**（这些解析函数只捕获 `ValueError`） |
| 合成：`$PUBX,40,GLL,0,0,0,0,0,0*HH` | `[]`，clean+1（不支持的句型） |
| 合成：`$PUBX,00,…`（109 字符，正确校验和） | `[]`，**三个计数器都不变**——超过 `SENTENCE_LIMIT = 90` 被丢 |
| 合成：GGA 补零到 `$` 之后 88/89/90/91 字符（含 `*HH`） | 都解析成功；92、93 字符 → 静默丢弃（最后一个校验字符那一步先判合法再判长度，所以实际上限是 91） |
| 真实 `$GNGST…` / 真实 `$GBGSV…` | `[]`，clean+1 |
| 合成：`$GPGSV,1,1,01,33,62,034,08,7`（1 星 + 信号 ID 7） | `['GPGSV']`，`satellite_data={33: (62, 34, 8)}`，无假星 |
| 合成：`$GPGSV,1,1,05,33,62,034,08,7`（`卫星数` 字段写 5，实际 1 星） | **抛 `IndexError`**——循环按 `卫星数` 读下标越界 |
| 合成：`$GPGSV,1,1,08,33,62,034,08`（写 8 实 1） | 本例（`*4A`）返回 `[]`，clean+1：校验和字段 `4A` 被当 PRN，`int()` 失败；校验和恰好是十进制数字时会出假卫星或越界 |
| 真实 GPGSV：历元 A 丢 3/3，历元 B 丢 1/3，只来 B 的 2/3、3/3 | 两句都返回 `'GPGSV'`，`satellite_data_updated()` = **True**，12 颗里 PRN5 C/N₀=19 是 **A 的旧值**（B 为 18）——静默混历元 |
| 真实 GPGSV：历元 B 丢 3/3 | `satellite_data_updated()` = False，`last_sv_sentence=2`，表里 8 颗是 A/B 混合 |
| 合成：先真实 GGA，再 `$GNRMC,…,V,…`（无效） | `['GNRMC']`，**经纬度被清成 `[0, 0.0, 'N']` / `[0, 0.0, 'W']`**，`valid=False` |
| 合成：先真实 GGA，再 `$GNGGA,003958.00,,,,,0,00,99.99,,,,,,` | `['GNGGA']`，时间更新到 00:39:58，**经纬度保留上一条的旧值** |
| 合成：真实 GGA 中间插入 `\t\x00` | `['GNGGA']`——码值 < 10 或 > 126 的字符被**跳过、不参与校验和** |
| `update(整数)`（迭代 bytes 得到的 int） | CPython `TypeError: ord() expected string of length 1, but int found`；MicroPython `TypeError: can't convert 'int' object to str implicitly` |
| `update(b'$')` 这类长度 1 的 bytes | 不报错但**永远 0 句**（`b'$' != '$'`）；MicroPython 每字符打一行 `Warning: Comparison between bytes and str` |
| `update(整句字符串)` | `TypeError: ord() expected a character, but string of length 71 found` |
| `date_string('long')`：日 = 3 / 23 / 0 | `April 3th, 2019` / `April 23th, 2019` / 未定位时 `December 0th, 200` |

## 5. 输入 / 输出

| API / 属性 | 类型与单位 | 由谁写 |
| --- | --- | --- |
| `MicropyGPS(local_offset=0, location_formatting='ddm')` | 偏移单位：小时；格式 `'ddm'`/`'dd'`/`'dms'` | — |
| `update(ch) -> str 或 None` | `ch` 必须是长度 1 的 `str` | — |
| `timestamp` | `[时, 分, 秒.0]`，时已加 `local_offset` 再 `% 24` | RMC / GGA / GLL |
| `date` | `(日, 月, 两位年)`；初值是**列表** `[0, 0, 0]`，RMC 之后变元组 | 只有 RMC |
| `latitude` / `longitude` | ddm：`[度, 分, 'N'/'S']`；dd：`[度, 半球]`（**无符号**）；dms：`[度, 分, 秒(整数), 半球]` | RMC / GGA / GLL |
| `altitude` / `geoid_height` | m（海拔 / 大地水准面差距） | GGA |
| `speed` | `(kn, mph, km/h)`：RMC 写列表、VTG 写元组；换算系数 1.151 / 1.852 | RMC / VTG |
| `course` | °（真北） | RMC / VTG |
| `satellites_in_use` | GGA 的卫星数（u-blox 封顶 12） | GGA |
| `satellites_used` | 最后一条 GSA 的 PRN 列表 | GSA |
| `hdop` / `pdop` / `vdop` | 无量纲；`hdop` 由 GGA 与 GSA **交替覆盖** | GGA / GSA |
| `satellite_data` | `{PRN: (仰角°, 方位°, C/N₀ dB-Hz)}`，缺值为 `None`；GSV 第 1 句**清空重建** | GSV |
| `satellites_in_view` / `last_sv_sentence` / `total_sv_sentences` | 最后一组 GSV 的值 | GSV |
| `fix_stat` / `fix_type` / `valid` | GGA 质量指示 / GSA 1–3 / RMC·GLL 状态 A | 见左 |
| `clean_sentences` / `parsed_sentences` / `crc_fails` | 累计计数，无「不支持」「超长」「无校验和」计数 | `update()` |

十进制度由 $\varphi = D + M/60$ 得到，dd 模式本身不丢精度（CPython/unix port 为双精度，GGA 29/29 比到 1e-9° 全同）。

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 多星座接收机只剩 GPS/GLONASS 卫星，北斗/伽利略消失 | 句头表写死 17 个，无 `GA`/`GB`/`BD` GSV，也无 `GNGSV` | 自己往 `MicropyGPS.supported_sentences` 加键（如 `'GAGSV': MicropyGPS.gpgsv`，未合并的 PR #31 就是这个）；或换 pynmeagps / nmea-rs |
| 2 | `satellite_data` 只有最后一个星座、最后一个信号 | 每组 GSV 第 1 句把字典整个替换 | 在 `satellite_data_updated()` 为真时把当组复制走，按 talker + 信号分别存 |
| 3 | `satellites_used` 一会儿是 GPS 一会儿是北斗 PRN，或者是空表 | NMEA 4.10 每历元多条 `$GNGSA`，系统 ID 被忽略，后一条覆盖前一条 | 在 `update()` 返回 `'GNGSA'` 时读 `gps_segments[18]`（系统 ID）自己累加 |
| 4 | `hdop` 值来回跳 | GGA 和 GSA 都写 `hdop` | 要哪个就在对应句返回时立即读 |
| 5 | 主循环被 `IndexError` 打断 | RMC/VTG/GLL/GSA/GSV 对字段不足只捕获 `ValueError`；GSV `卫星数` 与实际不符也越界 | 每次 `update()` 包 `try/except IndexError`；解析器在调用前已复位 `sentence_active`，后续句子不受影响 |
| 6 | 不带校验和的句子、超过 91 字符的句子（`$PUBX,00` 109 字符）凭空消失 | 只有校验和两位齐了才解析；`SENTENCE_LIMIT = 90` | 需要时调大 `SENTENCE_LIMIT`；无校验和的设备换 [nmea-parser](./nmea-parser.md) |
| 7 | GSV 丢句后卫星表混历元，`satellite_data_updated()` 仍为 True | 只看「当前句号 == 总句数」 | 以 GGA/RMC 为历元边界自己收组，丢句则整组作废 |
| 8 | `local_offset=-5` 后时间变 19:39，日期还是 UTC 的 4 月 12 日 | 只对小时 `% 24`，不进位日期；`5.5` 得到 `[5.5, 39, 56.0]` | 保持 `local_offset=0`，拿 UTC 自己用 `time`/`datetime` 换算 |
| 9 | RMC 状态 V 一来，位置变成 0°N 0°W | 无效 RMC 把经纬度清零（默认半球 W）；GGA 质量 0 反而保留旧位置 | 用前先看 `valid` / `fix_stat`，不要只看经纬度是否非零 |
| 10 | dms 模式误差可达十几米 | 秒 `round()` 成整数：首条 GGA 经度 30.00668′ 的 0.4008″ 被舍成 `0"`，约 8.6 m | 要精度用 `'dd'` 或 `'ddm'` |
| 11 | 单精度板子上 dd 丢精度 | 许多 MicroPython 移植的 float 是 32 位；按 float32 舍入模拟（本机 `struct`，非真板），170.5001113° → 170.5001068°，约 0.35 m | 在 MCU 上保留 `_longitude` 的度、分两段，传到上位机再合成 |
| 12 | `update(b)` 报 `TypeError` 或永远不出句子 | `uart.read()` 给 bytes，迭代得 int；切片得 bytes | `gps.update(chr(b))` |
| 13 | `date_string('long')` 写出 `3th`、`23th`，未定位时 `December 0th, 200` | 代码写成 `== (3, 23)`；月份下标 −1 | 用 `date` 元组自己格式化；年份是两位，世纪要自己补 |
| 14 | 想拿这一句的原始字段/类型 | 没有句对象；`gps_segments` 下一个 `$` 就被清空 | 在返回句头的那次调用里读 `gps_segments` |
| 15 | 以为能发 NMEA / 配置命令给接收机 | 无编码 API | 自己拼句 + XOR 校验和，或 pynmeagps / pyubx2 |
| 16 | 上游停滞 | master 最后提交 2022-01；PR #31/#46 等积压；无 PyPI | 钉 commit 拷单文件，本地打补丁 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| MicroPython 板子上读 GPS 模块，只要 GPS/GLONASS 位置、时间 | **本文 micropyGPS**（包 `try/except`，按坑 #1–#3 打补丁） |
| 桌面 Python 解析**并生成** NMEA、NMEA 4.10 信号 ID、GST/GBS/UBX | [pynmeagps](./pynmeagps.md) / UBX 用 [pyubx2](./pyubx2.md) |
| 经典 Python 按句解析、老代码兼容 | [pynmea2](./pynmea2.md) |
| 嵌入式 C、无动态分配 | [minmea](./minmea.md)；可插拔句型模块 → [libnmea](./libnmea.md) |
| Rust 解 NMEA + AIS | [nmea-parser](./nmea-parser.md) |
| Rust / `no_std` 解 GNSS NMEA，要系统 ID、GST | [nmea-rs](./nmea-rs.md) |
| 多客户端共享接收机、JSON 输出 | [gpsd](./gpsd.md) |

## 8. 相关

[pynmeagps.md](./pynmeagps.md) · [pynmea2.md](./pynmea2.md) · [minmea.md](./minmea.md) · [libnmea.md](./libnmea.md) · [nmea-parser.md](./nmea-parser.md) · [nmea-rs.md](./nmea-rs.md) · [gpsd.md](./gpsd.md) · [pyubx2.md](./pyubx2.md) · [ublox.md](./ublox.md) · [README.md](./README.md)
