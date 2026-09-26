# pyubxutils · u-blox UBX 接收机配置命令行工具集操作手册

目录：[`PROJECTS.json` → `pyubxutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pyubxutils> · PyPI **`pyubxutils` 1.0.6**（2026-02-11 18:13 UTC 上传）· tag **`v1.0.6`=`b758ec0`**；main tip **`31527a9`**（2026-09-23，领先 tag 6 commit，只改 README/版权串，下文坑仍在）· BSD-3-Clause · ★**5** · Python ≥3.10 · 依赖 `pyserial>=3.5`、`pyubx2>=1.2.58`（本机解析到 **pyubx2 1.3.7** / pynmeagps 1.1.7 / pyrtcm 1.2.0 / pyserial 3.5）· 本机 CPython 3.13.5 · 2026-09-26 02:14–02:45 EDT

> 岗位：**对串口上的 u-blox 板卡做「批量存/载/比对配置、开关消息、设基站」**。6 个 CLI：`ubxsave` `ubxload` `ubxcompare` `ubxsetrate` `ubxbase` `ubxsimulator`。冲突时：**本机 `-h` / 源码 > 上游 README > 本文**。编解码底层 → [pyubx2](./pyubx2.md)；拉流/NTRIP → [pygnssutils](./pygnssutils.md)（其 1.1.9 起把 ubx* 工具拆到本包）。
> **本机无接收机**：串口一律是 socat 伪终端 + 自写「假接收机」桥（下称**合成桥**）：UBX 命令交给上游 `UBXSimulator` 回 ACK-ACK，另由桥对 12 个键回 CFG-VALGET 合成值、可选注入合成 RTCM 1006、可选整帧回放 gpsd 真实 F9T 日志作背景流。**写入接收机的效果全部「未在真接收机测试」。**

## 1. 用途与边界

**做：** `ubxsave` 逐键 CFG-VALGET 轮询 RAM 层 → 存成 CFG-VALSET 二进制 `.ubx`；`ubxload` 把 `.ubx` 里的 CFG-VALSET 逐帧下发并数 ACK/NAK；`ubxcompare` 比较多份 `.ubx` / u-center `.txt` 配置的键值差；`ubxsetrate` 用 **CFG-MSG**（老式）批量开关 UBX/NMEA 消息；`ubxbase` 用 CFG-VALSET 设 **Survey-in / Fixed / 关闭** 基站模式并开 RTCM 1006/1077/1087/1097/1127/1230；`ubxsimulator` 进程内合成 UBX/NMEA 流（**EXPERIMENTAL**）。

**不做：** 不解码/录流（→ [pyubx2](./pyubx2.md) / [pygnssutils](./pygnssutils.md) `gnssstreamer`）；不转 RINEX（→ [ubx2rinex](./ubx2rinex.md)）；不做 NTRIP；不支持 TCP/文件端口（`-P` 只进 `serial.Serial`）；不刷固件；`ubxsimulator` **不是虚拟串口**，不能给别的程序当 `/dev/tty*`。

| 符号 | 含义 |
| --- | --- |
| CFG-VALSET / VALGET | Gen9+（F9/M10）配置库写 / 读，class/id `06 8A` / `06 8B` |
| CFG-MSG | 老式消息速率命令 `06 01`，Gen9 起标「deprecated」 |
| layer | RAM=1 / BBR=2 / Flash=4；本包**只存/写 RAM** |
| 合成 | 本文桥或模拟器造的输入，非真机输出 |

## 2. 安装

```bash
python3 -m venv /tmp/pyubxutils-man/venv
/tmp/pyubxutils-man/venv/bin/pip install pyubxutils        # 拉 pyubx2/pynmeagps/pyrtcm/pyserial
/tmp/pyubxutils-man/venv/bin/ubxsave -V                    # → ubxsave 1.0.6
```

entry_points（`dist-info/entry_points.txt`）：`ubxbase` `ubxcompare` `ubxload` `ubxsave` `ubxsetrate` `ubxsimulator`（→ `ubxsimulator_cli:main`）。**没有** `ubxpoll`/`ubxdump` 之类。所有工具共有 `-C/--config`（`KEY=VALUE` 行文件，或环境变量 `UBXSAVE_CONF` 等）、`--verbosity {-1..3}`、`--logtofile`。

## 3. 命令与真实输出

**假接收机**（合成）：`socat -d pty,raw,echo=0,link=ttyDEV pty,raw,echo=0,link=ttyAPP &`，桥 `bridge.py` 开 `ttyDEV`，工具连 `ttyAPP`。桥用 `UBXReader(parsing=False)` 整帧收；**用 `msgmode=POLL` 解析会静默丢掉 SET 帧**（我第一次就是这样，ubxload 显示 0 ACK）。

### 3.1 `-h` 要点

| 工具 | 关键参数（默认） |
| --- | --- |
| `ubxsave` | `-P`、`-O ubxconfig-YYYYmmddHHMMSS.ubx`、`--baudrate 9600`、`--timeout 0.2`、`--waittime 5` |
| `ubxload` | `-I`、`-P`、`--baudrate 9600`、`--timeout 3.0`、`--waittime 5` |
| `ubxcompare` | `-I a,b,…`（必填）、`-F {0 txt,1 ubx,2 按后缀}`=2、`-D {0 全部,1 只差异}`=1 |
| `ubxsetrate` | `--msgClass`（必填，**数字或 `0x..`**，或 `allubx/minubx/allnmea/minnmea`）、`--msgID`、`--rate 1` |
| `ubxbase` | `--baudrate 38400`、`--portype {USB,UART1,UART2,I2C}`、`--timemode {0,1,2}`=1、`--acclimit 100`（cm）、`--duration 60`（s，≤3600）、`--postype {0 ECEF,1 LLH}`=1、`--fixedpos`、`--waittime 5` |
| `ubxsimulator` | `-I` 间隔 ms=1000、`-T` 3 s、`--simconfigfile ~/ubxsimulator.json`、`--verbosity` **默认 1** |

### 3.2 ubxsave → `.ubx`（合成桥 variant 0）

```bash
ubxsave -P ttyAPP -O cfg-A.ubx --waittime 3
```

```text
Saving configuration from ttyAPP to cfg-A.ubx. Press Ctrl-C to terminate early.
Waiting 3 seconds for final responses...
Configuration successfully saved. 1 CFG-VALSET messages saved to cfg-A.ubx
```

耗时 **29.6 s**：pyubx2 1.3.7 的 `UBX_CONFIG_DATABASE` 有 **1295** 键，**每键一帧** VALGET、间隔 0.02 s（桥记到 1295 帧，首帧 `b562068b08000000000002002330ee0f` = 键 `0x30230002` CFG_ANA_ORBMAXERR）。输出 77 B，pyubx2 `msgmode=SET` 解码：

```text
b562068a45000101030006009120010a…0100524080250000 46b2
<UBX(CFG-VALSET, version=1, ram=1, bbr=0, flash=0, action=3, …, CFG_NAVSPG_DYNMODEL=0, CFG_RATE_MEAS=1000, …, CFG_TMODE_MODE=1, CFG_UART1_BAUDRATE=9600)>
```

字节核对：长度 `0x45`=69=4 B 头 + 12 键（5×L 各 5 B + 3×E1/U1 各 5 B + 2×U2 各 6 B + U4 8 B = 65 B）；`01002130 e803` = 键 `0x30210001` CFG_RATE_MEAS = 1000 ms；`01005240 80250000` = CFG_UART1_BAUDRATE 9600，末 2 B `46 b2` 为校验。`action=3`（commit）——**单帧文件没有 action=1 的 start**，真机是否接受未在真接收机测试。

### 3.3 ubxcompare（两份合成配置 + u-center 格式合成 txt）

桥 `--variant 1` 改 4 个值后再存 `cfg-B.ubx`：

```text
$ ubxcompare -I cfg-A.ubx,cfg-B.ubx
1 configuration commands processed in cfg-A.ubx
1 configuration commands processed in cfg-B.ubx
2 files processed, list of differences in config keys and their values follows: 
CFG_MSGOUT_UBX_NAV_PVT_USB (DIFFS!); 1: '0', 2: '1'
CFG_NAVSPG_DYNMODEL (DIFFS!); 1: '0', 2: '4'
CFG_RATE_MEAS (DIFFS!); 1: '1000', 2: '200'
CFG_UART1_BAUDRATE (DIFFS!); 1: '9600', 2: '38400'
Total config keys: 12. Total differences: 4.
```

退出码 **0**（有差异也 0）。1.0.6 起可混格式：`ucenter-synth.txt`（合成，行形如 `CFG-VALGET - 06 8B 0A 00 01 00 00 00 01 00 21 30 C8 00`，非 CFG 行如 `MON-VER - …` 被丢弃）与 `cfg-B.ubx` 比 → `CFG_RATE_MEAS (None); 1: '200', 2: '200'`，txt 缺的 10 键全标 `DIFFS!`（只出现在一个文件里也算差异）。

### 3.4 ubxload（合成桥回 ACK-ACK）

```text
$ ubxload -I cfg-B.ubx -P ttyAPP --waittime 10 --verbosity 3
… DEBUG - pyubxutils.ubxload - LOAD 1 - CFG-VALSET          (02:18:30.554)
… DEBUG - pyubxutils.ubxload - WRITE 1 CFG-VALSET           (02:18:33.555)
… DEBUG - pyubxutils.ubxload - ACKNOWLEDGEMENT 1 - <UBX(ACK-ACK, clsID=CFG, msgID=CFG-VALSET)>
Configuration successfully loaded. 1 CFG-VALSET messages sent and acknowledged.
```

桥收到的帧与 `cfg-B.ubx` **`cmp` 完全一致**（原样转发，不改 layer）。注意 LOAD→WRITE 隔了 **3.0 s**：读线程先阻塞一次 `--timeout 3.0` 才发（见坑 4）；`--waittime 3` 复测一次成功，属贴边竞态。同一机制下 `ubxbase --timemode 0 --waittime 2` 在**安静端口**稳定得到 `2 configuration messages sent, 0 acknowledged`，加 `--timeout 0.2` 即 `2 … acknowledged`；桥改为整帧回放 gpsd F9T 真实日志作背景流后，`ubxload --waittime 2` 也 **1.1 s** 成功（此时 stderr 夹几行 pyubx2 `Unknown protocol header b'$\x00'.`，来源未查清，不影响计数）。

### 3.5 ubxsetrate（CFG-MSG）

```text
$ ubxsetrate -P ttyAPP --msgClass 0x01 --msgID 0x07 --rate 2
Opening serial port ttyAPP @ 9600 baud ...
Sending configuration message <UBX(CFG-MSG, msgClass=NAV, msgID=NAV-PVT, rateDDC=2, rateUART1=2, rateUART2=2, rateUSB=2, rateSPI=2, reserved=0)>...
Configuration message(s) sent.
```

桥收到 `b5620601080001070202020202002104`：`06 01` CFG-MSG，载荷 `01 07` + 5 口速率全 `02` + 保留 `00`，校验 `21 04`。**所有口同一速率、不等 ACK**。批量：`minubx` 3 帧（NAV-DOP/PVT/SAT）、`minnmea` 5 帧（GGA/GSA/GSV/RMC/VTG）、`allnmea` 30 帧、`allubx` 42 帧（桥共收 80 帧 = 3+5+30+42）。

### 3.6 ubxbase

Fixed LLH（桥注入合成 RTCM 1006，`d300153ee0…` 21 B 全零载荷）：

```text
$ ubxbase -P ttyAPP --timemode 2 --postype 1 --fixedpos 52.123456789,13.987654321,4567.89 --acclimit 5 --waittime 4
Configuring device at port ttyAPP as base station using fixed timing mode
Fixed position format LLH, [52.123456789, 13.987654321, 4567.89], accuracy limit 5cm
Enabling output messages
Configuration successful. 2 configuration messages acknowledged. 5 RTCM 1006 (active base) messages confirmed.
```

解码首帧：`CFG_TMODE_MODE=2, POS_TYPE=1, FIXED_POS_ACC=500, LAT=521234567, LAT_HP=89, LON=139876543, LON_HP=21, HEIGHT=4567, HEIGHT_HP=89` —— 纬度 = 521234567×10⁻⁷° + 89×10⁻⁹°；高度 `--fixedpos` 第三项单位 **cm**（4567 cm + 0.89 cm）；精度 5 cm → 500（单位 0.1 mm）。

Survey-in `--timemode 1 --duration 5 --acclimit 250 --portype UART1`（无 RTCM 注入）：`2 acknowledged … 0 RTCM 1006` → `Configuration unsuccessful`，耗时 9.3 s（waittime 3 + duration 5）。解码：`CFG_TMODE_SVIN_ACC_LIMIT=25000`（250 cm）、`SVIN_MIN_DUR=5`；第二帧键是 **`CFG_MSGOUT_…_USB`** 而非 UART1（坑 1）。`--timemode 0` 发 `CFG_TMODE_MODE=0` + 6 个 RTCM 输出置 0，成功条件是「全 ACK 且 0 帧 1006」。

### 3.7 ubxsimulator

```bash
ubxsimulator --simconfigfile pyubxutils-main/examples/ubxsimulator.json --verbosity 3
```

```text
INFO - pyubxutils.ubxsimulator - UBX Simulator started
DEBUG - … <UBX(NAV-PVT, iTOW=02:15:32.043000, year=2026, month=9, day=26, hour=2, min=15, …, fixType=3, …
DEBUG - … <NMEA(GNGGA, time=06:15:32.040000, lat=52.4766751667, NS=N, lon=13.39247, EW=E, quality=5, numSV=12, …
```

上游示例 json（NAV-PVT/DOP/SAT + GGA/RMC/PQTM*，`simVector` 按 `headMot` 135° 移动）。SIGINT 4 s → `Terminated by user, 25 messages processed`，rc=0。**不加 `--verbosity 3` 什么都不打印**（消息走 DEBUG）。模拟器只对 UBX 输入回 ACK-ACK，另对 MON-VER 轮询、CFG-RATE 轮询/设置、`AT+ECHO=` 有响应；**不回 CFG-VALGET**，所以 `ubxsave` 不能只靠它。

## 4. I/O 表

| 工具 | 输入 | 输出 | 成功判据（源码） |
| --- | --- | --- | --- |
| ubxsave | 串口（逐键 VALGET，RAM 层） | `.ubx`：每 64 键一帧 CFG-VALSET（RAM，txn start/ongoing/commit） | 收到 VALGET 数 == 写入键数 |
| ubxload | `.ubx`（`SETPOLL` 读） | 原帧写串口 | ACK 数 == 帧数 |
| ubxcompare | `.ubx` / u-center `.txt`（CFG-VALGET 转 VALSET；CFG-MSG/PRT 等老式也收） | stdout 键值表 | 无（只打印） |
| ubxsetrate | 参数 | CFG-MSG 帧 | 无（不等 ACK） |
| ubxbase | 参数 | 2 帧 CFG-VALSET（RAM） | 全 ACK 且（基站模式 1006 >1 帧 / 关闭模式 0 帧） |
| ubxsimulator | json | 进程内流（DEBUG 日志） | — |

## 5. 错误用例（真实行为 + 退出码）

| 用例 | 结果 | rc |
| --- | --- | ---: |
| 4 个串口工具 `-P /dev/ttyNOPE` | `SerialException: [Errno 2] could not open port /dev/ttyNOPE` traceback；**ubxsave 已先建出 0 B 输出文件** | 1 |
| 不给 `-P`（ubxsetrate 实测，其余源码同逻辑） | `ParameterError: Serial port must be specified` traceback | 1 |
| `ubxsetrate --msgClass NAV --msgID PVT` | `ParameterError … invalid literal for int() with base 10: 'NAV'` | 1 |
| `ubxsetrate --msgClass 0x01 --msgID 0x99` | `Unknown message type: class 1 (0x01), id 153 (0x99)` | 1 |
| `ubxsetrate --msgClass 1`（缺 ID） | `'NoneType' object is not subscriptable` | 1 |
| ubxload 截断文件（前 40 B） | `Configuration successfully loaded. 0 CFG-VALSET messages sent and acknowledged.` | 0 |
| ubxload 改坏 1 字节（校验和错）/ 纯文本垃圾 | 同上「successfully loaded. 0」 | 0 |
| ubxcompare 同三份坏文件 | 打印 `Serial stream terminated unexpectedly. 71 bytes requested, 34 bytes returned.` / `Message checksum b'\x19\x84' invalid - should be b'\nK'`，`0 configuration commands processed`，照常出表 | 0 |
| ubxcompare 不存在文件 | `ERROR parsing nope.ubx! [Errno 2]…`，照常出表（12 键全差异） | 0 |
| ubxload 无 ACK（桥静默） | `1 sent, 0 acknowledged, 0 rejected, 1 null responses. Consider increasing waittime to >5 seconds.`，6.1 s | 0 |
| ubxsave 设备完全不应答 | **`Configuration successfully saved. 0 CFG-VALSET messages saved`**，0 B 文件，28 s | 0 |
| ubxbase 无 1006 | `Configuration unsuccessful … Consider increasing accuracy limit…` | 0 |
| ubxload `-C` 文件里写 `waittime=3` | `TypeError: must be real number, not str` | 1 |
| `-C` 文件有无 `=` 的行 | `ValueError: Configuration file invalid: bad.conf, not enough values to unpack` | 1 |
| ubxsimulator json 缺失 / 坏 JSON | ERROR 日志后用默认值启动，无消息 → 约 2 s 后 `TimeoutError` traceback | 1 |
| 波特率不匹配 | **未测**：pty 不模拟波特率（`--baudrate 38400` 对 9600 的桥照样通）；真串口上预期表现为读不到帧 → 同「无 ACK」 | — |

结论：**除参数/打开端口错误外，失败一律 rc=0**；只能 grep stdout 的 `successfully` + 核数字，且 ubxsave/ubxload 的「0 条也 successfully」必须另查。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `ubxbase --portype UART1` 仍开 `…_USB` 输出 | CLI 选项叫 `portype`，代码读 `porttype`（1.0.6 与 main `31527a9` 均如此） | `-C` 文件写一行 `porttype=UART1`（实测解码得 `CFG_MSGOUT_RTCM_3X_TYPE1006_UART1`） |
| 2 | 设备没接/没回也「successfully saved」 | `msg_rcvd == cfgkeys` 在 0==0 时成立 | 检查输出文件 >0 B，`ubxcompare -D 0` 看键数 |
| 3 | 坏/截断文件「successfully loaded. 0」 | 读到坏帧即当 EOF，0==0 判成功 | 下发前先 `ubxcompare -I f.ubx` 确认键数 |
| 4 | 安静端口上 ubxload/ubxbase 报 null response | 读线程先阻塞满 `--timeout` 才发帧，`waittime` 从构造时算起 | `--waittime` 大于 `--timeout` 几秒，或降 `--timeout 0.5` |
| 5 | 所有失败 rc=0 | `main()` 丢弃 `run()` 返回值 | 脚本里 grep 汇总行，别信 `$?` |
| 6 | `--msgClass NAV` 报 int 错 | 只收数字/`0x..` | 查 pyubx2 `UBX_MSGIDS`：NAV-PVT = `0x01 0x07` |
| 7 | ubxsetrate 5 个口同速率、无确认 | 固定 CFG-MSG 全口；Gen9 已弃用该命令 | F9/M10 用 VALSET（`ubxload` 自制文件或 [pyubx2](./pyubx2.md) `config_set`） |
| 8 | 存下来的只有 RAM 层 | ubxsave 用 `POLL_LAYER_RAM`、写 `SET_LAYER_RAM` | 要落 Flash/BBR 需另发 CFG-VALSET（layers=4/2）或 CFG-CFG |
| 9 | ubxsave 一次半分钟+ | 1295 键逐键轮询 ×0.02 s；键表随 pyubx2 版本变 | 固定 pyubx2 版本再对比文件；老接收机大量键无应答属正常 |
| 10 | `-C` 配置里数字参数崩 | 配置值全是字符串，且**覆盖**命令行同名参数 | 数值参数放命令行，`-C` 只放 `port`/`infile` |
| 11 | 模拟器 NAV-PVT `hour=2`、GGA `06:15` | UBX 用 `datetime.now()` 本地时，NMEA 用 UTC | `TZ=UTC ubxsimulator …`（实测 NAV-PVT `hour=6` 与 GGA `06:26` 对齐） |
| 12 | 把 `UBXSimulator` 当 stream 喂 `UBXLoader` | `run()` 打印 `self._stream.port` → `AttributeError: 'UBXSimulator' object has no attribute 'port'` | 用 socat pty + 桥，或自己给对象加 `port` 属性 |
| 13 | 日志毫秒 `33.55` 与 `33.162` 混排 | `LOGFORMAT` 用 `{msecs:.0f}` 不补零（55 ms 显示成 .55） | 排时间差时别按字符串排序 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 命令行批量备份/恢复/比对 F9 配置、一条命令设基站 | **pyubxutils（本文）** |
| 脚本里精确构造任意 UBX 帧（任意 layer、事务） | [pyubx2](./pyubx2.md) |
| 录流 / NTRIP / 小 caster | [pygnssutils](./pygnssutils.md) |
| Python 桌面 GUI 看星、改配置 | [pygpsclient](./pygpsclient.md) |
| u-blox 官方 GUI（Windows，`.txt` 配置导出，ubxcompare 可读；本文只用合成 txt 测过） | u-center / u-center 2（厂商闭源，本目录无手册） |
| Rust 里编解码 UBX、Builder 生成配置帧 | [ublox（Rust）](./ublox.md) |
| UBX RAWX → RINEX 观测 | [ubx2rinex](./ubx2rinex.md) |
| 守护进程多客户端分发；`ubxtool` 查/改 u-blox | [gpsd](./gpsd.md)（`ubxtool` 随 gpsd 发行） |
| Go 授时守护 + 串口配 F9P/F9T、自带 ubxsim | [satpulse](./satpulse.md) |
| ROS 接 F9P | [ublox_dgnss](./ublox-dgnss.md) / [ublox_driver](./ublox-driver.md) |

## 8. 复现素材

- gpsd `test/daemon/ublox-zed-f9t-ubx_nmea_l5.log`（commit **`c05330a`**，2025-07-31，SPDX **BSD-2-clause**，Gary E. Miller，EVK-F9T）：去 777 B 注释头后 30977 B，pyubx2 数得 NAV-PVT 9、NAV-SAT 9、MON-RF 2、GAGSV 54 等，**不含任何 ACK**，只作背景流。
- 合成桥：`UBXSimulator(configfile=空 json)` 处理 ACK；对 `CFG_RATE_*`、`CFG_UART1_BAUDRATE`、`CFG_MSGOUT_UBX_NAV_PVT_*`、`CFG_TMODE_MODE`、`CFG_NAVSPG_DYNMODEL` 回合成 VALGET（variant 0/1 两组值）；RTCM 1006 为 pyrtcm 构造的全零载荷。
- 未测：真接收机写入/ACK/NAK、真实波特率不匹配、BBR/Flash 持久化、Survey-in 真收敛、`AT+` TTY 命令路径、Windows COM 口。
