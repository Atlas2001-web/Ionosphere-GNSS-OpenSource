# cors-relay · CORS/NTRIP 差分中继操作手册

目录：[`PROJECTS.json` → `cors-relay`](../../PROJECTS.json) · 上游 <https://github.com/tisyang/cors-relay> · tip **`1238947`**（`REPO_VERSION`=`123894`，`REPO_DATE`=`2020-04-23`）· **BSD-3-Clause** · NTRIP **1.0** · 依赖 **libev** + **sqlite3** · 本机验证（2026-09-24 05:45 EDT）：`cmake`/`make` → `./cors-relay`；管理口 **8000**；Caster **8001–8003**；源表 **3** STR；鉴权 **ICY 200** / **401** · **质检复跑** 2026-09-24 06:17 EDT（tip **`1238947`**/`REPO`=`123894`/`2020-04-23`；二进制 **188496** B；管理 `USER-LIST`/`SOURCE-LIST`/`CLIENT-LIST` 对齐；8001/8002/8003 源表 STR×**3**/`Content-Length`=**390**；合法订流仅 **`ICY 200 OK\r\n`**（**12** B，无后续差分字节）；错口令/未知用户 **401**；未知挂载→源表非 401；**无真源未臆造 RTCM**；交叉 [ntripcaster-libev](./ntripcaster-libev.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[pygnssutils](./pygnssutils.md)）

> 岗位：把上游 CORS/NTRIP 帐号池 **中继再分发** 给内网客户端（GGA 上行 + RTCM 下行）。**无** `-h`/`--help`；冲突时：**上游 README / 源码端口与命令字 > 本文**。  
> 公网源表/订流入口 → [data-access](../data-access.md)「实时 NTRIP」；脚本客户端 → [pygnssutils](./pygnssutils.md)；多流 GUI → [bnc](./bnc.md)；同作者自建播发 → [ntripcaster-libev](./ntripcaster-libev.md)；生产播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)。

## 1. 用途与边界

**做：**

- NTRIP **1.0** Caster：客户端接入 → 从 SQLite 帐号池取空闲源 → 建上游 Client → 转发 GGA / 差分
- TCP **管理口**（默认 **8000**）：`USER-*` / `SOURCE-*` / `CLIENT-LIST`
- 同挂载点、距离 **&lt;30 km** 的客户端 **复用** 同一上游连接（代码 `d < 30000`）
- 硬编码源表 3 挂载：`RTCM30_GG` / `RTCM23_GPS` / `RTCM32_GGB`（面向千寻类口习惯）

**不做：**

- **不是** 通用多挂载专业播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** 多流 GUI / 录 RINEX → [bnc](./bnc.md)
- **不是** 源表探测主力 → [ntripbrowser](./ntripbrowser.md) / [ntripstreams](./ntripstreams.md) / [ntrip-client](./ntrip-client.md)
- **不是** NTRIP 2.0 / TLS / VRS；端口与挂载名 **写死在代码**，改行为要改源码重编
- **无** 真实上游时 **不臆造** RTCM 帧内容（本机仅验证到 `ICY 200 OK` + 管理命令）

一句话：**帐号池中继**；电离层产品仍在客户端落盘/转 RINEX 之后。

| 端口 | 角色 |
| --- | --- |
| **8000** | 管理控制台（文本命令 + `CONSOLE_PASSWD`） |
| **8001 / 8002 / 8003** | NTRIP Caster（与上游端口 **必须同号**） |
| **7999** | `127.0.0.1` 日志 TCP（ulog） |
| CWD `cors-relay.db` | sqlite3 用户/源帐号 |
| CWD `log_cors-relay.YYMMDD_HHMM` | 运行日志 |

## 2. 安装

```bash
sudo apt-get install -y build-essential cmake libev-dev libsqlite3-dev git
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --recurse-submodules https://github.com/tisyang/cors-relay.git
cd cors-relay
git rev-parse --short HEAD   # 本机：1238947
mkdir -p build && cd build
cmake ..
make -j"$(nproc)"
ls -la cors-relay
```

本机构建：`REPO_VERSION` 头文件为 `123894` / `2020-04-23`；链接产出 `build/cors-relay`（本机 **188496** B）。`cmake_minimum_required(2.8)` 在新 CMake 上仅 Deprecation Warning。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 缺 `ev.h` / sqlite | 未装 dev 包 | `libev-dev` `libsqlite3-dev` |
| submodule 空 | 未 `--recurse` | `git submodule update --init` |
| `Address already in use` | 8000–8003 被占 | 换机或改源码 `gates[]`/`8000` 后重编 |

## 3. 冒烟：启动 → 管理口 → 源表 → 鉴权

**无** CLI 帮助。启动即监听；口令用环境变量（教学口令课后立刻改）：

```bash
cd ~/iono_ops/cors-relay/build
export CONSOLE_PASSWD=labpass          # 默认字面量 passwd；勿提交
stdbuf -oL -eL ./cors-relay
```

**本机启动横幅 + 日志（2026-09-24 05:45 EDT，ANSI 已剥；质检复跑 06:17 EDT 进程仍在听 8000–8003）：**

```text
qxbroadcaster version 123894, 2020-04-23
05:45:04.463 [DEBUG] ntripcaster.c:1200: fetch 0 user tokens, 0 source tokens
05:45:04.463 [INFO ] ntripcaster.c:1226: setup server on 0.0.0.0:8001 OK.
05:45:04.463 [INFO ] ntripcaster.c:1226: setup server on 0.0.0.0:8002 OK.
05:45:04.463 [INFO ] ntripcaster.c:1226: setup server on 0.0.0.0:8003 OK.
05:45:04.463 [INFO ] ntripcaster.c:1245: setup console on 0.0.0.0:8000 OK.
```

同目录生成 `cors-relay.db` 与 `log_cors-relay.*`。stdout 可能全缓冲 → 用 `stdbuf -oL` 或看日志文件。

### 3.1 管理命令（TCP 8000，一行一条，`\r\n`）

| 命令 | 格式 |
| --- | --- |
| `USER-LIST` | `USER-LIST <passwd>` |
| `USER-ADD` | `USER-ADD <passwd> user:pass EDATE [ETIME]`（缺省时刻 `23:59:59`） |
| `USER-UPDATE` | `USER-UPDATE <passwd> user newpass` |
| `CLIENT-LIST` | `CLIENT-LIST <passwd>` |
| `SOURCE-ADD` | `SOURCE-ADD <passwd> SERVER user:pass EDATE [ETIME]`（**无端口字段**） |
| `SOURCE-LIST` | `SOURCE-LIST <passwd>` |

**本机真实往返（Python `socket`，口令 `labpass`）：**

```text
>>> USER-LIST labpass
OK USER-LIST

>>> USER-LIST wrong
ERROR bad password

>>> USER-ADD labpass demo:demopass 2099-12-31
OK USER-ADD

>>> USER-LIST labpass
OK USER-LIST
demo:demopass	2099-12-31 23:59:59

>>> SOURCE-ADD labpass 127.0.0.1 srcuser:srcpass 2099-12-31
OK SOURCE-ADD

>>> SOURCE-LIST labpass
OK SOURCE-LIST
127.0.0.1	srcuser:srcpass	2099-12-31 23:59:59	?

>>> CLIENT-LIST labpass
OK CLIENT-LIST

>>> USER-UPDATE labpass demo newpass
OK USER-UPDATE

>>> USER-LIST labpass
OK USER-LIST
demo:newpass	2099-12-31 23:59:59
```

未知命令（如 `HELP`）无应答体，连接关闭。控制台单次会话约 **2 s** 超时（`ev_once`）。

### 3.2 源表（任意 Caster 口，无挂载 / 未知挂载）

```bash
# 等价：curl -s http://127.0.0.1:8001/ | head
python3 - <<'PY'
import socket
s=socket.create_connection(('127.0.0.1',8001),timeout=3)
s.sendall(b'GET / HTTP/1.0\r\nUser-Agent: NTRIP lab/1.0\r\n\r\n')
print(s.recv(4096).decode('latin-1'))
PY
```

**本机真实响应（8001/8002/8003 相同；Date 为 UTC）：**

```text
SOURCETABLE 200 OK
Server: https://github.com/tisyang/cors-relay
Date: Thu Sep 24 09:45:19 2026 UTC
Connection: close
Content-Type: text/plain
Content-Length: 390

STR;RTCM30_GG;RTCM30_GG;RTCM3X;1005(10),1004-1012(1),1033(10);2;GNSS;POPNet;CHN;0.00;0.00;1;1;POP Platform;none;B;N;500;POP
STR;RTCM23_GPS;RTCM23_GPS;RTCM2X;1(1),31(1),41(1),3(10),32(30);2;GNSS;POPNet;CHN;0.00;0.00;1;1;POP Platform;none;B;N;500;POP
STR;RTCM32_GGB;RTCM32_GGB;RTCM3X;1005(10),1074-1084-1124(1);2;GNSS;POPNet;CHN;0.00;0.00;1;1;POP Platform;none;B;N;500;POP
ENDSOURCETABLE
```

### 3.3 订挂载鉴权（无真实上游 → 只验握手）

```text
# 合法用户 demo:newpass →（质检复跑：整段仅 12 B，无后续差分）
ICY 200 OK

# 错口令 / 未知用户 / 已知挂载但无 Authorization →
HTTP/1.0 401 Unauthorized

# 未知挂载（即使带合法 Basic）→ 回源表，不是 401
SOURCETABLE 200 OK
… STR×3 …
ENDSOURCETABLE
```

之后须客户端继续推 **GGA**；本机 `SOURCE-ADD` 指向 `127.0.0.1` 且无对端 Caster 时 **不会** 出现可持续 RTCM 字节（质检复跑确认 `ICY 200` 后 2 s 内 **0** 额外字节）——**禁止臆造帧 dump**。有真源时：`SOURCE-ADD` 的 `SERVER` 填上游 IP，且上游端口 = 本机监听口（8001↔8001 …）。

联调客户端示例（有真源后）：

```bash
# 见 docs/software/pygnssutils.md；口令勿进 git
# gnssntripclient --server 127.0.0.1 --port 8001 --https 0 \
#   --mountpoint RTCM32_GGB --ntripuser demo --ntrippassword "$PASS" \
#   --datatype RTCM --ntripversion 1.0
```

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| 启动横幅 | 历史名 **`qxbroadcaster`** + `git describe --abbrev=6` |
| `CONSOLE_PASSWD` | 管理口令；未设则 **`passwd`** |
| `SOURCE-ADD` 无端口 | 上游端口 ≡ 本机 Caster 口 |
| 复用半径 | ECEF 距离 **&lt;30000 m** 且同 gate/mnt |
| 重复登录 | 同 `user:pass` 新连接 **挤掉** 旧 agent |
| NTRIP 版本 | **1.0**（`ICY 200 OK`） |

## 5. 接到哪步

1. 注册/取得上游 NTRIP → [data-access](../data-access.md)  
2. 本机中继池 → **本文**  
3. 客户端探源表/订流 → [ntripbrowser](./ntripbrowser.md) / [pygnssutils](./pygnssutils.md) / [ntrip-client](./ntrip-client.md) / [bnc](./bnc.md)  
4. 自建轻量播发 → [ntripcaster-libev](./ntripcaster-libev.md)；生产多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)  
5. 落盘后 TEC/定位 → 路径 A/D（[georinex](./georinex.md) / [rtklib](./rtklib.md) …）

## 6. 坑（≥8）

1. **无 `-h`**：任何参数仍直接起服务；勿期待 Usage。  
2. **横幅叫 `qxbroadcaster`**：与二进制名 `cors-relay` 不一致，属历史遗留。  
3. **挂载写死**：非三 STR 名（含带合法 Basic）→ **只回源表**，不会 401 提示「无此挂载」（质检复跑 `/NOPE` 已确认）。  
4. **端口写死 8001–8003**：上游必须同端口；千寻外网常见 8001/2/3 习惯。  
5. **`SOURCE-ADD` 无端口字段**：填错 IP 只会在订流后失败，管理口仍 `OK`。  
6. **管理口默认口令 `passwd`**：公网务必 `CONSOLE_PASSWD` + 防火墙；口令禁进 git。  
7. **DB 在 CWD**：换目录启动 = 新空库；备份/迁移需拷 `cors-relay.db`。  
8. **同用户挤线**：测试两客户端同帐号会踢掉先连者。  
9. **无上游勿造 RTCM stdout**：仅 `ICY 200` 不够当「差分已通」。  
10. **NTRIP 1.0 only**：现代 2.0/TLS 客户端可能需改客户端或换 [bkg-ntripcaster](./bkg-ntripcaster.md)。  
11. **stdout 缓冲**：无 `stdbuf` 时横幅可能晚于日志文件。  
12. **64 位指针告警**：`on_iter_*` 把 `wsocket` 塞进 `void*`；本机构建可跑，非可移植写法。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 上游帐号池 → 内网多用户中继 | **cors-relay（本文）** |
| 同作者轻量自建播发（SOURCE 推流） | [ntripcaster-libev](./ntripcaster-libev.md) |
| 正规多用户播发 / 中继配置项 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 五分钟脚本拉流 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |
| 只查源表 | [ntripbrowser](./ntripbrowser.md) |

同作者播发端见已短硬 [ntripcaster-libev](./ntripcaster-libev.md)（口 **2101**；动态源表；对照本文帐号池中继）。
