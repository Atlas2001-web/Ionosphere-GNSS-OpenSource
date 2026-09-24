# ntripclient · BKG POSIX NTRIP 客户端操作手册

目录：[`PROJECTS.json` → `ntripclient`](../../PROJECTS.json) · wiki <https://software.rtcm-ntrip.org/wiki/ntripclient> · 门户索引 [rtcm-ntrip-software](./rtcm-ntrip-software.md) · SVN `https://software.rtcm-ntrip.org/svn/trunk/ntripclient`（guest/guest）· 源码 `$Id: ntripclient.c,v 1.51 2009/09/11 09:49:19 stoecker Exp $` · 末变 **r9404**（2021-04-14）· WC **r11044** · 本机 **`Version 1.51 (2009-09-11) GPL built Sep 24 2026`** · GPL · 本机验证（2026-09-24 06:23–06:25 EDT）：`make` → `./ntripclient`（**44240** B；**gcc 14.2.0**）；默认 euref **STR 222**；rtk2go **STR 766** / igs-ip **STR 384** / centipede **STR 1273**；centipede `VALDM` **8 s** → **11779** B / **70** 帧；rtk2go 无订户/假口令 → stderr `SOURCETABLE 200 OK`、**0** B；igs-ip 订流 **401** + HTML **79** B

> 岗位：官方 **POSIX C CLI**——拉 sourcetable / 订挂载点原始字节（stdout）。冲突时：**本机 `./ntripclient -h` / 仓内 README / 门户 > 本文**。  
> 对照：Rust 结构化客户 → [ntrip-client](./ntrip-client.md)；Python asyncio → [ntripstreams](./ntripstreams.md)；多协议 CLI → [pygnssutils](./pygnssutils.md)；多流 GUI → [bnc](./bnc.md)；源表浏览 → [ntripbrowser](./ntripbrowser.md)；上传端 → [ntripserver](./ntripserver.md)；门户地图 → [rtcm-ntrip-software](./rtcm-ntrip-software.md)。

## 1. 用途与边界

**做：**

- NTRIP **1.0 / 2.0**（http / rtsp / udp / auto）订流客户端
- 无 `-m`：向默认 **`euref-ip.net:2101`**（或 `-s/-r`）拉 **sourcetable** 到 stdout
- 有 `-m`：订挂载；Basic 鉴权（`-u/-p`）；可选 NMEA（`-n`）、串口输出（`-D…`）、代理
- URL 单参：`ntrip:mount[/user[:pass]][@server[:port]…]`

**不做：**

- **不是** 结构化 `MountInfo` / `find-nearest` → [ntrip-client](./ntrip-client.md)
- **不是** RTCM 帧解码库 → [pyrtcm](./pyrtcm.md) / [ntripstreams](./ntripstreams.md) `Rtcm3`
- **不是** 上传 / SOURCE → [ntripserver](./ntripserver.md)
- **不是** 多流运维 GUI → [bnc](./bnc.md)
- **不是** 自建 caster → [bkg-ntripcaster](./bkg-ntripcaster.md) / [ntripcaster-libev](./ntripcaster-libev.md)

一句话：**官方轻量订流 CLI**；电离层产品仍在「字节落盘 → RINEX/解码」之后。

| 符号 | 含义 |
| --- | --- |
| `1.51` | `$Revision: 1.51 $`（CVS 风格；目录末变多为 **r9404**） |
| `-m` / `--mountpoint` | 挂载点；**`-d` 已弃用**（仍会落到 `-m`） |
| `-M` | `http`/`rtsp`/`ntrip1`/`auto`/`udp` |
| User-Agent | `NTRIP NtripClientPOSIX/1.51` |

## 2. 获取 / 编译

```bash
sudo apt-get install -y build-essential subversion
svn checkout --username guest --password guest \
  https://software.rtcm-ntrip.org/svn/trunk/ntripclient
cd ntripclient
svn info | grep -E 'Revision|Last Changed Rev|Date'
# 本机：Revision 11044；Last Changed Rev 9404；2021-04-14

make
# cc -Wall -W -O3  ntripclient.c -o ntripclient
# 本机两条 -Wimplicit-fallthrough 提示，链接成功
ls -la ntripclient   # 本机 **44240** B
./ntripclient -h | head -3
# Version 1.51 (2009-09-11) GPL built Sep 24 2026
```

说明：wiki 几乎只有源码链；发行物请走 [rtcm-ntrip-software](./rtcm-ntrip-software.md) / BKG。`serial.c` 在 makefile 当前目标里**未**链入（串口路径依赖源码条件编译习惯，以本机 `make` 为准）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `svn: E215004` | 未带 guest | `--username guest --password guest` |
| 只有 `.c` 无二进制 | 未 `make` | 在含 `makefile` 目录执行 |
| 与 Rust `ntrip-client` 混淆 | 名字相近 | 本文 = BKG POSIX；Rust 见 [ntrip-client](./ntrip-client.md) |

## 3. 端到端（本机真跑；2026-09-24 06:23–06:25 EDT）

本机**无 rtk2go/igs-ip 订户口令**；下列含 **公开源表** + **centipede 公开口令订流** + **鉴权失败样例**。挂载点数随 caster 变，勿当金样。

### 3.1 `-h`（stderr，exit **1**）

```bash
./ntripclient -h
```

**本机摘录：**

```text
Version 1.51 (2009-09-11) GPL built Sep 24 2026
Usage:
./ntripclient -s server -u user ...
 -m --mountpoint the requested data set or sourcetable filtering criteria
 -s --server     the server name or address
 -p --password   the login password
 -r --port       the server port number (default 2101)
 -u --user       the user name
 -M --mode       mode for data request
     Valid modes are:
     1, h, http     NTRIP Version 2.0 Caster in TCP/IP mode
     2, r, rtsp     NTRIP Version 2.0 Caster in RTSP/RTP mode
     3, n, ntrip1   NTRIP Version 1.0 Caster
     4, a, auto     automatic detection (default)
     5, u, udp      NTRIP Version 2.0 Caster in UDP mode
…
```

### 3.2 无参 / 无 `-m`：默认 euref 源表

```bash
./ntripclient > /tmp/euref.st
# 默认 -s euref-ip.net -r 2101；stdout 为 HTTP 头 + CAS/NET/STR
wc -l /tmp/euref.st; grep -c '^STR;' /tmp/euref.st
```

**本机：** **240** 行 / **STR 222**（BKG Caster/2.0.48；`Ntrip-Version: Ntrip/2.0`）。

### 3.3 公开 caster 源表

```bash
./ntripclient -s rtk2go.com -r 2101 -M ntrip1 > /tmp/rtk2go.st
./ntripclient -s igs-ip.net -r 2101 -M http > /tmp/igs.st
./ntripclient -s caster.centipede.fr -r 2101 -M http > /tmp/cent.st
wc -l /tmp/rtk2go.st /tmp/igs.st /tmp/cent.st
grep -c '^STR;' /tmp/rtk2go.st /tmp/igs.st /tmp/cent.st
```

| caster | 本机行数 / STR（2026-09-24） |
| --- | --- |
| `rtk2go.com:2101` | **775** / **766**（SNIP；含 `SOURCETABLE 200 OK` 头） |
| `igs-ip.net:2101` | **401** / **384**（Ntrip/2.0） |
| `caster.centipede.fr:2101` | **1284** / **1273**（Millipede 0.8.1） |

### 3.4 订流：centipede `VALDM`（真字节）

公开口令与 [ntrip-client](./ntrip-client.md) / [rtcm3torinex](./rtcm3torinex.md) 一致（`centipede`/`password`）。`timeout` 截断即可；**勿**长时间挂着占满事件循环。

```bash
timeout 8 ./ntripclient -s caster.centipede.fr -r 2101 -m VALDM \
  -u centipede -p password -M http > /tmp/valdm.bin
wc -c /tmp/valdm.bin
# 本机：**11779** B；扫描 preamble `0xD3` → **70** 帧
# 类型计数（本机）：1004×8 1005×1 1008×1 1012×8 1019×11 1033×1
#   1077×8 1087×8 1097×8 1107×8 1127×8（共 11 类）
```

### 3.5 鉴权失败（如实）

```bash
# rtk2go：无用户 / 假口令 —— 本机 stderr 同文，stdout **0** B
timeout 5 ./ntripclient -s rtk2go.com -r 2101 -m AgPartner_2 -M ntrip1
# Could not get the requested data: SOURCETABLE 200 OK

timeout 5 ./ntripclient -s rtk2go.com -r 2101 -m AgPartner_2 \
  -u nobody -p wrong -M ntrip1
# Could not get the requested data: SOURCETABLE 200 OK

# igs-ip 无口令
timeout 5 ./ntripclient -s igs-ip.net -r 2101 -m BRUX00BEL0 -M http \
  > /tmp/igs_sub.bin 2>/tmp/igs_sub.err
# stderr: Could not get the requested data: HTTP/1.1 401 Unauthorized
# /tmp/igs_sub.bin **79** B：
# <HTML><BODY>You are not authorized to access the requested data.</BODY></HTML>
```

对照：[ntripstreams](./ntripstreams.md) 无订户常报 HTTP **400**；[ntrip-client](./ntrip-client.md) rtk2go 假口令常见 **403**——**以各工具本机 stderr 为准**，勿强行对齐成同一状态码。

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| 源表 stdout | 可能含 HTTP/`SOURCETABLE` 头；STR 行以 `STR;` 起 |
| 订流 stdout | **原始字节**（常为 RTCM3）；程序**不解帧** |
| `-h` | 写 **stderr**；exit **1** |
| 默认 server | `euref-ip.net` |
| Agent | `NTRIP NtripClientPOSIX/<rev>` |

## 5. 接到哪步

1. 公网 caster / 政策 → [data-access](../data-access.md)  
2. 本 CLI 拉表/订流 → **本文**  
3. 结构化/近邻 → [ntrip-client](./ntrip-client.md)；脚本 → [pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md)  
4. 字节→RINEX → [rtcm3torinex](./rtcm3torinex.md) / [bnc](./bnc.md)；帧解码 → [pyrtcm](./pyrtcm.md)  
5. 上传 → [ntripserver](./ntripserver.md)；自建播发 → [ntripcaster-libev](./ntripcaster-libev.md) / [bkg-ntripcaster](./bkg-ntripcaster.md)

## 6. 坑（≥8）

1. **`-h` 走 stderr 且 exit 1**：管道只看 stdout 会以为「无帮助」。  
2. **无 `-m` = 源表**：不是「缺参报错」；默认连 euref。  
3. **`-d` 弃用**：仍可用，但打印 deprecated 并落入 `-m`。  
4. **与 Rust `ntrip-client` 同名易混**：可执行文件本文叫 `ntripclient`（无连字符）。  
5. **rtk2go 拒订不一定给 401**：本机回 `SOURCETABLE 200 OK` 文案。  
6. **igs-ip 401 体可能落进「数据文件」**：先看 stderr，再 `wc`/`file`。  
7. **订流无温和退出开关**：用 `timeout`/`CTRL+C`；勿当守护进程挂着。  
8. **串口 `-D`**：当前 `makefile` 只编 `ntripclient.c`；勿假设开箱即有完整 serial 链。  
9. **chunked / Ntrip2**：`-M http` 与 `-M ntrip1` 行为不同；失败时换 mode。  
10. **源表点数会变**：上表仅当日快照。  
11. **Windows**：README 另有 `-DWINDOWSVERSION`；本手册只验 Linux。  
12. **勿把 stderr 鉴权句当 RTCM**：`Could not get…` 不是差分电文。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 官方 POSIX 最小订流 CLI | **ntripclient（本文）** |
| Rust 结构化 list/近邻/解帧 | [ntrip-client](./ntrip-client.md) |
| Python asyncio / 可上传 | [ntripstreams](./ntripstreams.md) |
| 多协议录流 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 多流 GUI | [bnc](./bnc.md) |
| 只浏览源表 | [ntripbrowser](./ntripbrowser.md) |
| 上传到 caster | [ntripserver](./ntripserver.md) |
