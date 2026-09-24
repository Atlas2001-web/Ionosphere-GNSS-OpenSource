# ntripserver · BKG POSIX NTRIP 上传端操作手册

目录：[`PROJECTS.json` → `ntripserver`](../../PROJECTS.json) · wiki <https://software.rtcm-ntrip.org/wiki/ntripserver> · 门户索引 [rtcm-ntrip-software](./rtcm-ntrip-software.md) · SVN `https://software.rtcm-ntrip.org/svn/trunk/ntripserver`（guest/guest）· 源码 `$Id: ntripserver.c 10685 2025-07-01 20:17:30Z stuerze $` · 末变 **r10685**（2025-07-01）· WC **r11044** · 本机 **`Version 1.10685 (2025-07-01) GPL built Sep 24 2026`** · GPL-2 · 本机验证（2026-09-24 06:23–06:25 EDT）：`make` → `./ntripserver`（**61672** B；**gcc 14.2.0**）；`-h`/无参 Usage；对本地 [ntripcaster-libev](./ntripcaster-libev.md) **SOURCE `ICY 200 OK`**；FIFO 馈入既有 centipede `VALDM` 捕获 → 客户端回拉 **7683** B / **42** 帧；**无串口/无接收机**——未臆造 RTCM；测完即杀，未留守护进程

> 岗位：把 **单路 GNSS 流**（串口 / TCP / 文件 / SISNeT / UDP / 另一 caster）**上传**到 NTRIP caster 或 TCP 目的端。冲突时：**本机 `./ntripserver` Usage / README / 门户 > 本文**。  
> 对照：订流客户端 → [ntripclient](./ntripclient.md)；实验室播发 → [ntripcaster-libev](./ntripcaster-libev.md)；生产播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)；帐号池中继 → [cors-relay](./cors-relay.md)；Python 上传 → [ntripstreams](./ntripstreams.md) `-s` / [pygnssutils](./pygnssutils.md)；门户 → [rtcm-ntrip-software](./rtcm-ntrip-software.md)。

## 1. 用途与边界

**做：**

- **输入**（`-M`）：1 串口 · 2 IP · 3 文件/`stdin` · 4 SISNeT · 5 UDP · 6 NTRIP1 caster · 7 NTRIP2 HTTP caster
- **输出**（`-O`）：1 http(NTRIP2) · 2 rtsp · 3 ntrip1 · 4 udp · 5 tcpip；默认文档写明偏 NTRIP1，未来会切 2.0
- 代理（`-E/-F`）、重连上限延时（`-R`）、目的挂载/口令（`-a/-p/-m/-c`，NTRIP2 另需 `-n` 用户）

**不做：**

- **不是** caster 本体（不监听客户端）→ [bkg-ntripcaster](./bkg-ntripcaster.md) / [ntripcaster-libev](./ntripcaster-libev.md)
- **不是** 订流拉表主力 → [ntripclient](./ntripclient.md) / [ntripbrowser](./ntripbrowser.md)
- **不是** 多流 GUI / 录盘 → [bnc](./bnc.md)
- **不解码** RTCM；只透传字节——**禁止**把实验室占位串写成「真实差分电文」
- **本机无 GNSS 接收机 / 无串口源**：仅文件/FIFO + 本地 caster 探针；无假造帧体

一句话：**官方单源上传客户端**；要播发请另起 caster。

| 符号 | 含义 |
| --- | --- |
| `1.10685` | `$Revision: 10685 $` → 版本串 `1.` + SVN 修订 |
| `-M 3 -s FILE` | 文件模拟输入（默认 `/dev/stdin`） |
| `SOURCE <pass> /<mnt>` | NTRIP1 上传握手（本机 Agent `NtripServerPOSIX/1.10685`） |
| `-O 3` | 目的 NTRIP **1.0** |

## 2. 获取 / 编译

```bash
sudo apt-get install -y build-essential subversion
svn checkout --username guest --password guest \
  https://software.rtcm-ntrip.org/svn/trunk/ntripserver
cd ntripserver
svn info | grep -E 'Revision|Last Changed Rev|Date'
# 本机：Revision 11044；Last Changed Rev 10685；2025-07-01

make
# cc -Wall -W ntripserver.c -o ntripserver
ls -la ntripserver   # 本机 **61672** B
./ntripserver 2>&1 | head -5
# Version 1.10685 (2025-07-01) GPL built Sep 24 2026
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `svn` 认证失败 | 未带 guest | `--username guest --password guest` |
| 只有源码 | 未 `make` | 执行 `make`（或 `make debug`） |
| 想「官方 zip」 | wiki 仅指 README/源码 | SVN 或门户 [rtcm-ntrip-software](./rtcm-ntrip-software.md) |

## 3. 端到端（本机真跑；2026-09-24 06:24–06:25 EDT）

**无串口接收机**：下列用 **文件/FIFO** + 已运行的本地 [ntripcaster-libev](./ntripcaster-libev.md)（`0.0.0.0:2101`，源口令 `test`，客户 `test:test`）。输入字节来自先前 [ntripclient](./ntripclient.md) 对 centipede `VALDM` 的真实捕获——**透传验证，不重新发明 RTCM**。探针结束后 **立刻杀掉** `ntripserver`（cors-relay 前车之鉴：勿留占事件循环的长挂进程）。

### 3.1 帮助（无参或 `-h`）

```bash
./ntripserver          # 打印完整 PURPOSE/OPTIONS
./ntripserver -h x     # 亦可；单独 -h 可能先报 getopt 再印 Usage
```

**本机开头：**

```text
Version 1.10685 (2025-07-01) GPL built Sep 24 2026
Usage:
./ntripserver [OPTIONS]
PURPOSE
   The purpose of this program is to pick up a GNSS data stream (Input, Source)
   from either
     1. a Serial port, or
     2. an IP server, or
     3. a File, or
     …
```

关键旗标（摘录）：`-M` 输入模式；`-O` 输出模式；`-a/-p/-m/-c` 目的 caster；文件输入 `-M 3 -s <File>`；NTRIP 源输入 `-M 6|7` + `-H/-P/-D/-U/-W`。

### 3.2 边界：无源时的文件模式

```bash
# 一次性读完小文件：握手可能成功，但传输阶段会饿死
./ntripserver -M 3 -s /tmp/valdm.bin -O 3 \
  -a 127.0.0.1 -p 2101 -m LAB1 -c test
```

**本机 stderr 要点：**

```text
Destination caster request:
SOURCE test /LAB1
Source-Agent: NTRIP NtripServerPOSIX/1.10685

Destination caster response:
ICY 200 OK

transfering data ...
WARNING: no data received from input
```

即：**SOURCE 鉴权通过 ≠ 已有可持续载荷**。文件过早 EOF → `WARNING: no data received from input`。

### 3.3 FIFO 探针：上传 + 订回（真字节）

```bash
mkfifo /tmp/ns_fifo
timeout 12 ./ntripserver -M 3 -s /tmp/ns_fifo -O 3 \
  -a 127.0.0.1 -p 2101 -m LAB1 -c test &
# 另终端/进程：分块写入先前 VALDM 捕获；同时：
timeout 5 ./ntripclient -s 127.0.0.1 -r 2101 -m LAB1 \
  -u test -p test -M ntrip1 > /tmp/ns_pull.bin
# 测完：kill ntripserver；rm /tmp/ns_fifo
wc -c /tmp/ns_pull.bin
```

**本机结果：**

| 步骤 | 事实 |
| --- | --- |
| SOURCE | `ICY 200 OK`；Agent `NtripServerPOSIX/1.10685` |
| 上传中源表 | 出现 `STR;LAB1;…`（CL≈**113**） |
| 客户端订回 | **7683** B；扫描 `0xD3` → **42** 帧 |
| 结束后源表 | 回到空表 `ENDSOURCETABLE`（CL=**16**） |
| 进程 | **无**残留 `ntripserver` |

无本地 caster / 无串口时：停在「`-h` + 无源边界」即可，**不要**向公网 caster 盲传实验字节。

### 3.4 交叉对照

| 工具 | 角色 | 对照点 |
| --- | --- | --- |
| [ntripclient](./ntripclient.md) | 官方订流 | 本机 FIFO 回拉用的就是它 |
| [ntrip-client](./ntrip-client.md) / [ntripstreams](./ntripstreams.md) / [pygnssutils](./pygnssutils.md) | 现代客户/脚本 | 订流/小 caster；上传也可用 streams `-s` |
| [ntripcaster-libev](./ntripcaster-libev.md) | 实验室播发 | 本探针目的端 |
| [bkg-ntripcaster](./bkg-ntripcaster.md) | 生产播发 | 正规多用户 / 配置项 |
| [cors-relay](./cors-relay.md) | 帐号池中继 | 拉上游再分发，不是 SOURCE 上传工具 |

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| stdout | 常打印 `file input: …` 等状态 |
| stderr | 目的主机摘要、`SOURCE` 请求/响应、`WARNING` |
| 成功上传握手 | `ICY 200 OK`（NTRIP1） |
| 输入饿死 | `WARNING: no data received from input` |
| 默认目的 | 文档默认 `euref-ip.net:2101`（**勿**对公网误传实验流） |

## 5. 接到哪步

1. 有接收机串口/TCP 源 → 本文 `-M 1|2`  
2. 仅有文件/录盘 → `-M 3` + 本地 caster 联调  
3. 目的播发 → [ntripcaster-libev](./ntripcaster-libev.md) / [bkg-ntripcaster](./bkg-ntripcaster.md)  
4. 客户端验证 → [ntripclient](./ntripclient.md) / [pygnssutils](./pygnssutils.md)  
5. 中继池场景 → [cors-relay](./cors-relay.md)

## 6. 坑（≥8）

1. **`-h` getopt 怪癖**：单独 `-h` 可能先报 `option requires an argument`；无参更稳。  
2. **默认输出仍偏 NTRIP1**：文档写明未来改 2.0；目的端不支持时换 `-O`。  
3. **文件模式 EOF**：短文件易 `WARNING: no data…`；联调用 FIFO/管道持续喂。  
4. **`ICY 200` 只是握手**：不证明客户端已收到差分。  
5. **无串口勿硬编 `/dev/gps`**：`-M 1` 默认设备在无硬件上报错属预期。  
6. **勿对公网 caster 用实验口令/占位流**：实验室用本地播发端。  
7. **测完即杀**：长挂 `ntripserver`/`ntripcaster` 会拖垮共享 box（cors-relay 教训）。  
8. **与 `ntripclient` 成对**：一个 SOURCE、一个 GET；名字差三个字母。  
9. **NTRIP2 目的需 `-n` 用户**：只填 `-c` 不够。  
10. **`-R` 重连**：未设则失败即停；脚本里勿误以为会永远重试。  
11. **透传不校验 CRC**：坏帧也会上传。  
12. **Windows**：README/`WINDOWSVERSION`；本手册只验 Linux。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 官方单源 → caster 上传 | **ntripserver（本文）** |
| 官方订流 | [ntripclient](./ntripclient.md) |
| 实验室自建播发 | [ntripcaster-libev](./ntripcaster-libev.md) |
| 生产多用户播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 上游帐号池中继 | [cors-relay](./cors-relay.md) |
| Python 上传/小工具 | [ntripstreams](./ntripstreams.md) / [pygnssutils](./pygnssutils.md) |
| 多流 GUI | [bnc](./bnc.md) |
