# pygnssutils · GNSS 流 / NTRIP CLI 操作手册

目录：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pygnssutils> · 文档 <https://www.semuconsulting.com/pygnssutils> · PyPI `pygnssutils` · BSD-3-Clause · Python ≥3.10 · 本机验证 **1.2.7**（`gnssstreamer`/`gnssntripclient`/`gnssserver`；`pyrinexconv` **0.2.0 Beta**）

> 岗位：串口/TCP/NTRIP **探活、录流、轻量播发**。主 CLI（以本机 `-h` 为准）：`gnssstreamer`、`gnssntripclient`、`gnssserver`、`pyrinexconv`（实验性）。口令禁止进 git；用环境变量。旗标随小版本可能微调。

## 1. 用途与边界

**做：** 同一流解析 NMEA/UBX/SBF/QGC/RTCM3/SPARTN；拉源表 / 订 NTRIP；TCP 转发；短时录二进制；实验性 RAW→RINEX。

**不做：** 生产多挂载点高并发 → [bkg-ntripcaster](./bkg-ntripcaster.md)；多流 GUI 录盘主力 → [bnc](./bnc.md)；TEC/ROTI/PPP → 落盘转 RINEX 后走 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)（作者 **viventriglia**）/[oasis-roti](./oasis-roti.md)/[rtklib](./rtklib.md)。

一句话：解决「流从哪来」；电离层产品在 **落盘并转 RINEX 之后**。

| 组件 | 角色 |
| --- | --- |
| `gnssstreamer` | 双向流 CLI（收 + 可选灌改正） |
| `gnssntripclient` | NTRIP 客户端（源表 / 订流） |
| `gnssserver` | TCP 服务或单挂载点 NTRIP caster |
| `pyrinexconv` | 实验性二进制→RINEX（仍 Beta） |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip pygnssutils
gnssstreamer -V          # 期望：gnssstreamer 1.2.7（或以本机为准）
gnssntripclient -V
gnssserver -V
pyrinexconv -V           # 期望：pyrinexconv 0.2.0 Beta
# conda: conda install -c conda-forge pygnssutils
```

Windows：`py -3.11 -m venv ...`；串口形如 `COM3`。Linux 串口：用户进 `dialout` 后重登。

```bash
export PYGPSCLIENT_USER='your_user'          # rtk2go 等常要求合法邮箱作用户名
export PYGPSCLIENT_PASSWORD='your_pass'
# 勿把口令写入仓库；conf 文件 chmod 600
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `command not found` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| 打不开 `/dev/ttyACM0` | 无串口权限 | `sudo usermod -aG dialout $USER` 后重登 |
| 旧名 `gnssdump` | 已更名 | 用 `gnssstreamer` |

## 3. 端到端（本机 1.2.7 真跑，2026-09-24 ~03:08 ET）

无接收机时用文件 / 本机 TCP 回环；有公网时拉公开源表。下列 stdout **摘自实跑**，勿当固定不变的金样。

### 3.1 文件回放探活（`gnssstreamer`）

准备若干行 NMEA（或真实 UBX 日志）后：

```bash
gnssstreamer --filename demo_nmea.txt --verbosity 2 --limit 10
```

**期望（摘录）：**

```text
Messages input:    {'GNGGA': 3, 'GNGSA': 1, 'GNRMC': 1}
Messages filtered: {}
Messages output:   {'GNGGA': 3, 'GNGSA': 1, 'GNRMC': 1}
Streaming terminated, 5 messages processed with 0 errors.
<NMEA(GNGGA, time=12:35:19, lat=39.9041871667, NS=N, lon=116.3907426667, EW=E, quality=1, numSV=12, HDOP=0.9, alt=44.0, ...)>
```

串口探活（有硬件时）：

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 --verbosity 2
# Windows: --port COM3
```

### 3.2 过滤 GGA + lambda

```bash
gnssstreamer --filename demo_nmea.txt \
  --protfilter 1 --msgfilter GNGGA \
  --clioutput 4 \
  --output "lambda msg: print(f'lat={msg.lat}, lon={msg.lon}, q={msg.quality}')" \
  --verbosity 1 --limit 5
```

**期望（本机）：**

```text
lat=39.9041871667, lon=116.3907426667, q=1
lat=39.9041873333, lon=116.3907428333, q=1
lat=39.9041875, lon=116.390743, q=2
```

| 旗标 | 作用（1.2.7 `-h`） |
| --- | --- |
| `--port` / `--filename` / `--socket` | 串口 / 文件 / `host:port` **三选一** |
| `--baudrate` / `--timeout` | 串口参数（默认 9600 / 3.0） |
| `--protfilter` | 位掩码：1 NMEA，2 UBX，4 RTCM3，8 SBF，16 QGC；默认可 OR 到 31 |
| `--msgfilter` | 消息 ID，可加周期 `NAV-PVT(10)` |
| `--format` | 1 解析 / 2 原始 / 4 hex / 8 表格式 hex / 16 字串 / 32 JSON；可 OR（例 `9=1\|8`） |
| `--clioutput` | 0 终端 / 1 二进制文件 / 2 串口 / 3 TCP 服务 / 6 TCP+TLS / 4 表达式 / 5 文本文件 |
| `--output` | 与 clioutput 匹配的路径 / `host:port` / lambda |
| `--cliinput` | 0 无 / 1 NTRIP RTCM / 2 NTRIP SPARTN / 4 串口 / 5 二进制文件 |
| `--input` | NTRIP URL 或文件等 |
| `--rtkuser` / `--rtkpassword` / `--rtkggaint` | 灌改正时的鉴权与 GGA 周期 |
| `--limit` / `--verbosity` / `--quitonerror` | 条数、日志、错误策略 |

### 3.3 录二进制（事后转 RINEX）

```bash
mkdir -p ~/iono_ops/raw
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 \
  --format 2 --clioutput 1 \
  --msgfilter RXM-RAWX,RXM-SFRBX,NAV-PVT,GGA \
  --limit 5400 --verbosity 2 \
  --output ~/iono_ops/raw/ublox_raw.bin
# 建议 ≥15–30 min；结束看 Messages output 非空
ls -l ~/iono_ops/raw/ublox_raw.bin
```

### 3.4 拉公开 NTRIP 源表

```bash
gnssntripclient \
  --server rtk2go.com --port 2101 --https 0 \
  --datatype RTCM --ntripversion 2.0 \
  --ggainterval -1 \
  --reflat 39.90 --reflon 116.40 \
  --ntripuser "${PYGPSCLIENT_USER:-anon}" \
  --ntrippassword "${PYGPSCLIENT_PASSWORD:-password}" \
  --verbosity 2
```

**期望（本机实跑）：** 打印 `Sourcetable:`（大量 `STR;...`），然后：

```text
Closest mountpoint to reference location (39.9, 116.4) = Piggy-BJ-DX2, 32.83 km.
Sourcetable retrieved
```

源表行样例（节选）：

```text
STR;Piggy-BJ-DX2;Daxing District, Beijing;RTCM 3.3;1004(1), 1005(1), ...;2;GPS+GLO+GAL+BeiDou+SBAS;SNIP;CHN;39.61;116.33;...
```

空源表 → DNS/防火墙/caster 拒绝。

| 旗标 | 作用 |
| --- | --- |
| `--server` / `--port` / `--https` | caster 与 TLS（0=HTTP，1=HTTPS） |
| `--mountpoint` | 空=源表；非空=订流 |
| `--datatype` | `RTCM` / `SPARTN` |
| `--ntripversion` | 常 `2.0` |
| `--ggainterval` | GGA 周期；`-1`=不发 |
| `--reflat` / `--reflon` / `--refalt` | 参考位置（VRS / 最近站排序） |
| `--ntripuser` / `--ntrippassword` | 鉴权（默认 anon/password，多数公网不可订流） |
| `--clioutput` / `--output` | 改正写出文件/串口/socket |

### 3.5 订挂载点（需合规账号）

```bash
gnssntripclient \
  --server rtk2go.com --port 2101 --https 0 \
  --mountpoint YOUR_MOUNT --datatype RTCM \
  --ggainterval 60 \
  --reflat 39.9042 --reflon 116.4074 --refalt 44.0 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**期望：** `Streaming RTCM data from HOST:PORT/MOUNT ...`；有流时周期性见到 `1005`/`1077` 等。

**本机用 anon/password 订 `Piggy-BJ-DX2` 实况：** HTTP **400**，体为

```text
This Caster requires a well formed eMail as the user name to connect.
```

→ 注册后把邮箱放进 `PYGPSCLIENT_USER`，勿把口令写进 git。

### 3.6 串口 + 并发 NTRIP 灌改正

```bash
gnssstreamer --port /dev/ttyACM0 \
  --msgfilter GNGGA \
  --cliinput 1 \
  --input "http://caster.example:2101/MOUNT" \
  --rtkuser "$PYGPSCLIENT_USER" --rtkpassword "$PYGPSCLIENT_PASSWORD" \
  --rtkggaint 10 \
  --clioutput 4 \
  --output "lambda msg: print(msg.quality, msg.diffAge, msg.lat, msg.lon)"
```

**期望：** `quality` 可能升至 4/5（视基线与接收机）。无硬件时跳过。

### 3.7 本机 TCP 转发（无串口回环）

终端 A：上游字节源（任意进程往 `127.0.0.1:45000` 送 NMEA/RTCM）。终端 B：

```bash
gnssserver --socket 127.0.0.1:45000 \
  --hostip 127.0.0.1 --outport 50010 \
  --ntripmode 0 --format 2 --verbosity 2
# 期望：
# Starting server ...
# Starting output thread, broadcasting on 127.0.0.1:50010...
```

终端 C：

```bash
gnssstreamer --socket 127.0.0.1:50010 --verbosity 2 --limit 6
```

**期望（本机）：**

```text
Client ('127.0.0.1', ...) connected. Total clients 1/5.   # 服务端
Messages input:    {'GNGGA': 3, 'GNRMC': 3}
Streaming terminated, 6 messages processed with 0 errors. # 客户端
```

有接收机时把 `--socket` 换成 `--inport /dev/ttyACM0 --baudrate 38400`。

### 3.8 本机轻量 NTRIP caster（个人测试）

```bash
# 终端 A：上游须已出 RTCM（教学可用 socket 灌流；生产串口）
gnssserver --socket 127.0.0.1:45001 \
  --hostip 127.0.0.1 --outport 2101 \
  --ntripmode 1 --protfilter 4 --format 2 \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2
# 期望：broadcasting on 127.0.0.1:2101...

# 终端 B：源表
gnssntripclient --server 127.0.0.1 --port 2101 --https 0 \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --ggainterval -1 --verbosity 2
```

**期望（本机源表）：**

```text
CAS;127.0.0.1;2101;pygnssutils/1.2.7;SEMU;0;GBR;;;0.0.0.0;0;none
NET;PYGNSSUTILS;SEMU;B;N;none;none;none;none
STR;pygnssutils;PYGNSSUTILS;RTCM 3.3;1002(1),1006(5),1010(1),1077(1),1087(1),1097(1),1127(1),1230(1),4072_0(1),4072_1(1);2;GPS+GLO+GAL+BDS;PYGNSSUTILS;GBR;;;0;0;PYGNSSUTILS;none;B;N;0;
ENDSOURCETABLE
Sourcetable retrieved
```

```bash
# 终端 B：订流
gnssntripclient --server 127.0.0.1 --port 2101 \
  --mountpoint pygnssutils --datatype RTCM \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2
```

**期望：** `Streaming RTCM data from 127.0.0.1:2101/pygnssutils ...`；服务端 `Client ... connected`。

| `gnssserver` 旗标 | 作用 |
| --- | --- |
| `--inport` / `--socket` / `--baudrate` | 上游串口或 `host:port` |
| `--hostip` / `--outport` | 监听（默认 `0.0.0.0:50010`） |
| `--ntripmode` | 0=TCP；1=NTRIP caster |
| `--protfilter` / `--format` | NTRIP 模式需 RTCM **二进制**（`--format 2`，`--protfilter 4`） |
| `--ntripuser` / `--ntrippassword` | 客户端登录（默认 anon/password，务必改） |
| `--maxclients` | 最大客户端（默认 5） |
| `--ntriprtcmstr` | 源表 STR 中 RTCM 类型串 |

**仅限个人/课堂。** 正式多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)。

### 3.9 实验性 `pyrinexconv`

```bash
pyrinexconv -I ~/iono_ops/raw/ublox_raw.bin \
  --minobs 10 \
  --marker "LOCAL,1,GEODETIC" \
  --antenna "1,UNKNOWN" \
  --receiver "1,u-blox,ZED-F9P" \
  --observer "lab" \
  --obsfilter 1C \
  --verbosity 2
```

**本机对纯 NMEA 文件实跑：** 进度到 100%，产出空壳：

```text
Processing successful. Output file names and number of records processed:
Observation: pygpsdata_R_999912310000_00U_00U_MO.rnx - 0
Navigation: pygpsdata_R_999912310000_00U_MN.rnx - 0
Meteorology: pygpsdata_R_999912310000_00U_00U_MM.rnx - 0
```

→ 需要 UBX `RXM-RAWX`/`RXM-SFRBX`（或 RTCM 星历）才有观测/导航记录。仍标 **experimental**——发表数据请用可追溯工具链复核（厂商转换 / [bnc](./bnc.md) / [gfzrnx](./gfzrnx.md)）。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| 串口 / 文件 / TCP | streamer 三源 |
| NTRIP caster | 源表或挂载点 |
| 口令 | 环境变量或 conf（勿进 git） |

| 输出 | 下游 |
| --- | --- |
| 解析对象 / 二进制日志 | 探活；事后转 RINEX |
| RTCM 文件 | 回放 |
| TCP/NTRIP 服务 | [rtklib](./rtklib.md) 等客户端 |
| RINEX（实验） | [gfzrnx](./gfzrnx.md) → [anubis](./anubis.md) → TEC/ROTI |

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 C 实时入口 | §3 | 落盘 → A/B |
| 多流 GUI 录盘 | — | [bnc](./bnc.md) |
| 正式播发 | — | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 定位演示 | §3.6–3.8 | [rtklib](./rtklib.md) · [06](../tutorials/06-iono-positioning.md) |
| 读盘 TEC | 录流转 RINEX 后 | [georinex](./georinex.md) · [pytecgg](./pytecgg.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `command not found` | 未激活 venv | `source .../activate` |
| 2 | 串口 Permission denied | 非 dialout | 加组并重登 |
| 3 | 无数据/乱码 | 波特率错 | 试 9600/38400/115200 |
| 4 | VRS 无流 | 未发 GGA | 设 `--ggainterval` 与 lat/lon/alt |
| 5 | 401/403/400「well formed eMail」 | 口令/ACL/rtk2go 要邮箱用户名 | 注册；`PYGPSCLIENT_USER`；勿贴聊天 |
| 6 | 2101 冲突 | 与 BNC/正式 caster 抢端口 | 改 `--outport` |
| 7 | NTRIP 客户端解不出 | format 非二进制 / 上游无 RTCM | `gnssserver --format 2 --protfilter 4`；先确认基站吐 MSM |
| 8 | caster 无 1005/1077 | 接收机未进 Base | 先配基站模式 |
| 9 | 脚本仍写 `gnssdump` | 旧名 | 改 `gnssstreamer` |
| 10 | TLS 失败 | 证书/时间 | NTP；查 `--tlscrtpath` / PEM |
| 11 | SPARTN 解密失败 | 密钥/basedate | 联系服务商 |
| 12 | `pyrinexconv` 记录数全 0 | 输入非 UBX RAWX | 录 `RXM-RAWX`；或换正式转换链 |
| 13 | lambda 属性错 | 消息类型无该字段 | 先不过滤看类型 |
| 14 | 局域网连不上 | 监听地址/防火墙 | `--hostip 0.0.0.0`；放行端口 |
| 15 | 磁盘写满 | 长时 1 Hz 日志 | `--limit`；logrotate |
| 16 | 把 RTCM 当 RINEX 喂 georinex | 格式错 | 先转换 |
| 17 | 口令进 git | conf 误提交 | `chmod 600`；gitignore；轮换 |
| 18 | 当 TEC 引擎 | 链选错 | 落盘后 [pytecgg](./pytecgg.md)（viventriglia） |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| CLI 探活/录流/轻量 NTRIP | **pygnssutils** |
| 多流 GUI 录盘 | [bnc](./bnc.md) |
| 正式多用户播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 事后定位 | [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md) |
| RINEX 科学预处理 | [gfzrnx](./gfzrnx.md)（`pyrinexconv` 仅实验） |

## 8. 相关

[bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · [README](./README.md)
