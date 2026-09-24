# ntrip-cpp · NTRIP 2.0 C++（caster/client/server）操作手册

目录：[`PROJECTS.json` → `ntrip-cpp`](../../PROJECTS.json) · 上游 <https://github.com/ybzwyrcld/ntrip> · tip **`b431661`** · CMake **`1.2.0`** · Agent `NTRIP* /1.2.0.b431661` · **MIT** · NTRIP **2.0 为主**（客端兼容 `ICY`）· 依赖 **C++11** + **epoll**（Linux）· 本机验证（2026-09-24 06:18 EDT）：两处上游构建补丁后 `cmake`/`make` → caster **8090**；`POST` 源 → `HTTP/1.1 200`；客 `HTTP/1.1 200` / `ICY 200` / `401`；样例透传 **Recv[70]**（源码 `kExmapleData`，**非公网 CORS**）

> 岗位：嵌入 C++ 服务的 **NTRIP 握手与挂载点参考实现**（库 `libntrip` + 四个 exam）。**无** `-h`/`--help`（argv 被忽略）。冲突时：**上游源码 / README > 本文**。  
> 公网源表/订流 → [data-access](../data-access.md)「实时 NTRIP」；NTRIP **1.0** 轻量播发 → [ntripcaster-libev](./ntripcaster-libev.md)；帐号池中继 → [cors-relay](./cors-relay.md)；生产多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)；脚本客户端 → [pygnssutils](./pygnssutils.md)。

## 1. 用途与边界

**做：**

- 静态库 **`libntrip`**：`NtripCaster` / `NtripServer` / `NtripClient`（`include/ntrip/*.h`）
- **Server**：`POST /<mnt> HTTP/1.1` + `Ntrip-Version: Ntrip/2.0` + `Authorization: Basic` + `Ntrip-STR:`
- **Client**：`GET /<mnt> HTTP/1.1` + Basic；可选 GGA 周期上报
- **Caster**：epoll 单口；登记源挂载后按 **同挂载同 user:pass** 转发字节
- 示例默认：`127.0.0.1:8090` · `test01`/`123456` · 挂载 **`RTCM32`**

**不做：**

- **不是** 生产级多用户 ACL / conf 中继 / TLS → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** NTRIP **1.0** `SOURCE <passwd> /mnt` 推流（本仓 ParseData **只认 POST/GET**）→ [ntripcaster-libev](./ntripcaster-libev.md) / [cors-relay](./cors-relay.md)
- **不是** 可用源表服务：`SendSourceTableData` **有实现、无调用**；`GET /` → **`401`**（≠ `SOURCETABLE 200`）
- **不是** 帐号池中继 / 管理口 → [cors-relay](./cors-relay.md)
- **不是** 多流 GUI / 录 RINEX → [bnc](./bnc.md)
- **不解码** RTCM；exam 的 70 B 是源码硬编码样例，**禁止**当成真实差分电文验收

一句话：**C++ NTRIP 2.0 握手样板**；对照已文档化的 **1.0 caster**（libev / cors-relay）与 **BKG 专业播发**。

| 项 | 角色 |
| --- | --- |
| 默认 `0.0.0.0:8090` | Caster（exam `Init(8090, 30, 2000)`） |
| `NtripServer` | 源端 POST 推流 |
| `NtripClient` | 客端 GET 订流 |
| CMake `NTRIP_BUILD_CASTER` | **默认 OFF**；开 caster 需本地补丁（§2） |

### 与已文档 caster 对照

| | **ntrip-cpp（本文）** | [ntripcaster-libev](./ntripcaster-libev.md) | [cors-relay](./cors-relay.md) | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| --- | --- | --- | --- | --- |
| 协议重心 | **2.0 POST** + 客端 `ICY` 兼容 | **1.0 SOURCE** | **1.0** 中继 | **1.0 / 2.0** |
| 源表 | **死路径**（`GET /`→401） | 动态在线 STR | 硬编码 3 STR | 正式 sourcetable |
| 鉴权模型 | 源登记的 user:pass = 客口令 | JSON tokens | SQLite 帐号池 | 用户文件 / 配置 |
| 默认口 | **8090** | 2101 | 8001–8003 | 常 2101 |
| 形态 | **库 + exam** | 单二进制 | 单二进制 | 专业套件 |

## 2. 安装

```bash
sudo apt-get install -y build-essential cmake git
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/ybzwyrcld/ntrip.git   # README 仍写 hanoi404，以 catalog URL 为准
cd ntrip
git rev-parse --short HEAD   # 本机：b431661
```

### 2.1 默认构建（无 caster，开箱可用）

```bash
mkdir -p build && cd build
cmake .. -DNTRIP_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release
# 日志可见：-- Not build ntrip caster
make -j"$(nproc)"
ls -la libntrip.a examples/ntrip_*_exam
# 本机（无 caster）：libntrip.a ≈ 44614 B；client/server/client_to_server exam 在 examples/
```

### 2.2 打开 Caster（**必须两处本地补丁**，否则 tip `b431661` 配不过）

上游缺陷（本机已复现）：

1. `examples/CMakeLists.txt`：`add_executable(ntrip_caster …)` 与后续 `ntrip_caster_exam` 目标名不一致 → CMake Error  
2. `include/ntrip/ntrip_caster.h`：`#include "../thread_raii.h"` → 找不到头（同目录应为 `"thread_raii.h"`，对照 client/server 的 `"./thread_raii.h"`）

```bash
# 在仓库根目录打补丁后：
sed -i 's/add_executable(ntrip_caster /add_executable(ntrip_caster_exam /' examples/CMakeLists.txt
sed -i 's|#include "../thread_raii.h"|#include "thread_raii.h"|' include/ntrip/ntrip_caster.h
mkdir -p build && cd build
cmake .. -DNTRIP_BUILD_CASTER=ON -DNTRIP_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release
make -j"$(nproc)"
ls -la libntrip.a examples/ntrip_caster_exam
# 本机（含 caster）：libntrip.a ≈ 95688 B；ntrip_caster_exam ≈ 60488 B
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `make all` 缺 `cmake_definition.h` | 顶层 Makefile 不跑 configure | 用 **CMake**（或先 cmake 生成头） |
| `NTRIP_BUILD_CASTER=ON` 配置失败 | exam 目标名笔误 | 补丁 1 |
| `../thread_raii.h: No such file` | caster 头路径错误 | 补丁 2 |
| `bind` 后静默 `exit(1)` | 无 `SO_REUSEADDR`；口占用/残留 | 换口或停占用进程后再启 |
| README `hanoi404/ntrip` | 旧 fork 名 | 用 `ybzwyrcld/ntrip` |

## 3. 冒烟：Caster → Server → Client

**无** CLI 帮助；参数写死在 `examples/*_exam.cc`。教学口令课后改；**勿进 git**。

```bash
cd ~/iono_ops/ntrip/build
# 终端 1
stdbuf -oL -eL ./examples/ntrip_caster_exam
# 终端 2
stdbuf -oL -eL ./examples/ntrip_server_exam
# 终端 3
stdbuf -oL -eL ./examples/ntrip_client_exam
```

**本机横幅（2026-09-24 06:18 EDT）：**

```text
NtripCaster service running...
NtripServer service running...
Send example data success!!!
NtripClient service running...
Recv[70]: D3 00 40 41 2E 06 44 19 1E F5 00 A4 00 00 10 B6 11 08 C2 E8 1D 58 1A 72 C8 46 CD 1A 08 EA 81 2C 3E DC 1B BB D9 5D 90 61 E8 05 2F FB 89 9A 4D CC EB FE 4C 25 28 FB 6C DA 7F 61 8E 60 9C BF FB 6A 2D 30 02 19 8F 73
```

说明：`Recv[70]` 字节与 `examples/ntrip_server_exam.cc` 中 `kExmapleData` **一致**——是 exam 循环 `SendData` 的样例，**不是**公网 CORS/RTCM 解码结果；勿据此写 MSM/站心结论。

### 3.1 握手探针（Python `socket`，caster+server 已起）

```text
>>> GET / HTTP/1.0（无挂载 / 探源表）
HTTP/1.1 401 Unauthorized          # 27 B；≠ SOURCETABLE（死路径）

>>> SOURCE 123456 /RTCM99 + Source-Agent   # NTRIP 1.0 源推
(empty)                                 # 不解析 SOURCE

>>> GET /RTCM32 + Basic test01:123456 + HTTP/1.1
HTTP/1.1 200 OK                         # 17 B

>>> GET /RTCM32 + Basic test01:123456 + HTTP/1.0
ICY 200 OK                              # 12 B（1.0 风格响应）

>>> GET /RTCM32 + Basic wrong:wrong
HTTP/1.1 401 Unauthorized               # 27 B

>>> POST /RTCM32 重复挂载（另一 user）
ERROR - Bad Password                    # 22 B（文案误导，实为挂载占用）
```

Agent 常量（cmake 生成 `src/cmake_definition.h`）：`NTRIP NTRIPCaster/1.2.0.b431661` · `…Client/…` · `…Server/…`。

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| Server 请求行 | `POST /<mnt> HTTP/1.1` |
| Server 头 | `Ntrip-Version: Ntrip/2.0` · `Ntrip-STR: STR;…` · `Authorization: Basic` · `Transfer-Encoding: chunked` |
| Client 请求行 | `GET /<mnt> HTTP/1.1`（exam）；HTTP/1.0 → 响应改 `ICY 200 OK` |
| 鉴权 | 客 **user:pass 必须等于** 该挂载 Server 登记时的一对；无独立用户库 |
| `Ntrip-STR` | `STR;<mnt>;<mnt>;…` 中两段名须与 POST 路径一致，否则拒源 |
| 成功源响应 | `HTTP/1.1 200 OK\r\n`（仅状态行，无多余头） |
| 失败客响应 | `HTTP/1.1 401 Unauthorized\r\n` |
| 数据面 | 源 `SendData` 字节原样到已鉴权客；**不校验 CRC** |

## 5. 参数（改 exam / API，无 CLI）

| API / 常量 | exam 默认 | 说明 |
| --- | --- | --- |
| `NtripCaster::Init(port, max_conn, epoll_ms)` | `8090, 30, 2000` | 监听与 epoll 超时 |
| Server/Client `Init(ip,port,user,pass,mnt[,str])` | `127.0.0.1` / `test01` / `123456` / `RTCM32` | 改口令=改源码重编 |
| `set_location(lat,lon)` / `set_report_interval(s)` | 22.57311, 113.94905 / 1 s | 客端周期 GGA |
| `NTRIP_BUILD_CASTER/CLIENT/SERVER/EXAMPLES` | OFF/ON/ON/OFF | CMake 开关 |

## 6. 接到哪步

1. 公网实时流账号/源表 → [data-access](../data-access.md)「实时 NTRIP」  
2. 学 **2.0 POST** 或嵌入 C++ → **本文**  
3. 实验室 **1.0** 自建播发 → [ntripcaster-libev](./ntripcaster-libev.md)  
4. 上游 CORS 帐号池再分发 → [cors-relay](./cors-relay.md)  
5. 正式多用户 / TLS / 源表运维 → [bkg-ntripcaster](./bkg-ntripcaster.md)  
6. 脚本/Rust 订流 → [pygnssutils](./pygnssutils.md) / [ntrip-client](./ntrip-client.md) / [ntripstreams](./ntripstreams.md)  
7. 落盘后 TEC/定位 → 路径 A/D

## 7. 坑（≥8）

1. **无 `-h`**：`./ntrip_caster_exam --help` 仍直接监听 8090（吞掉参数）。  
2. **默认不编 caster**：忘记 `-DNTRIP_BUILD_CASTER=ON` 时只有 client/server exam。  
3. **开 caster 必打两补丁**：目标名 + `thread_raii` 头路径（§2.2）；否则 tip `b431661` 无法配置/编译。  
4. **顶层 `make all` 缺头文件**：依赖 `cmake_definition.h`；请用 CMake。  
5. **`GET /` ≠ 源表**：恒 `401`；`SendSourceTableData` 未挂到请求路径——不要拿 [ntripbrowser](./ntripbrowser.md) 习惯硬套。  
6. **无 NTRIP 1.0 `SOURCE`**：与 [ntripcaster-libev](./ntripcaster-libev.md) / [cors-relay](./cors-relay.md) 不互通源推语法。  
7. **客口令=源口令**：换一对 user:pass 推源后，旧客端立刻 401。  
8. **重复挂载文案撒谎**：占用中回 `ERROR - Bad Password`（不是口令错）。  
9. **`bind` 失败静默 `exit(1)`**：无错误字符串；8090 被占时像“闪退”。  
10. **无 `SO_REUSEADDR`**：短时重启可能偶发 bind 失败。  
11. **exam 样例 ≠ 真 RTCM**：`Recv[70]` 只证明透传；真流再用 [pyrtcm](./pyrtcm.md) / [bnc](./bnc.md)。  
12. **README 克隆 URL 过时**：写 `hanoi404/ntrip`；catalog / 本手册用 `ybzwyrcld/ntrip`。  
13. **stdout 全缓冲**：横幅/Send 行可能晚现 → `stdbuf -oL`。  
14. **多连接 TODO**：源码注释 *Multiple connections still have problems*——压测勿当生产。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| C++ 嵌入 / 学 NTRIP **2.0 POST** 握手 | **ntrip-cpp（本文）** |
| 实验室 JSON **1.0** 自建播发 | [ntripcaster-libev](./ntripcaster-libev.md) |
| CORS 帐号池 → 内网再分发 | [cors-relay](./cors-relay.md) |
| 正规多用户播发 / 源表运维 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 五分钟脚本拉流 | [pygnssutils](./pygnssutils.md) |
| Rust/asyncio 订流 | [ntrip-client](./ntrip-client.md) / [ntripstreams](./ntripstreams.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |
| Go 云原生网关（catalog 待短硬） | `ntrip-go`（`go-gnss/ntrip`） |
