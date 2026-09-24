# ntrip-go · go-gnss/ntrip（Go NTRIP 库 / 云原生网关底座）操作手册

目录：[`PROJECTS.json` → `ntrip-go`](../../PROJECTS.json) · 上游 <https://github.com/go-gnss/ntrip> · tip **`6d11102`**（2026-02-18；`fix non-constant format string`）· 模块最新标签 **`v0.0.16`**（`5f17dd2`，proxy 2026-02-17；**tip 超前标签**）· `go.mod` **`go 1.24.0`** / `toolchain go1.24.10` · **Apache-2.0** · 本机验证（2026-09-24 06:28–06:30 EDT）：`go version go1.24.10`；`go build ./...`；`go test` **7 PASS**；`go build -o ntrip-relay ./cmd/relay` → **8598110** B；`-h` 超时默认 **`2ns`**；`NewClientRequest` 拉公网源表 rtk2go mounts=**766** / igs=**384** / GA=**918** / centipede=**1272**；本地 inmemory caster `127.0.0.1:18701`：源表 **16** B `ENDSOURCETABLE`、`POST`/`GET` **200**、坏口令 **401**、未知挂载 **404**、透传占位 **33** B（**非 RTCM**）

> 岗位：用 **Go + `net/http`** 做 NTRIP **客户端 / 服务端（POST）/ Caster（`http.Handler`）** 的嵌入式底座与示例中继。冲突时：**上游源码 / README / 本机 `go test` > 本文**。  
> 公网源表/订流账号 → [data-access](../data-access.md)「实时 NTRIP」；BKG **1.0** 官方对 → [ntripclient](./ntripclient.md) + [ntripserver](./ntripserver.md)；C++ **2.0** 样板 → [ntrip-cpp](./ntrip-cpp.md)；实验室 **1.0** 播发 → [ntripcaster-libev](./ntripcaster-libev.md)；生产多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)。

## 1. 用途与边界

**做：**

- 库 `github.com/go-gnss/ntrip`：`NewClientRequest` / `NewServerRequest`（**Ntrip/2.0** 头 + chunked POST）
- `NewCaster(addr, SourceService, logger)` → 包一层 `http.Server`（Idle/ReadHeader **10 s**；长连接读写由 Handler 控）
- 源表：`ParseSourcetable` / `Sourcetable.String`；v2 `GET /` 写表；v1 `GET /` → `SOURCETABLE 200 OK`（hijack）
- 示例 CLI：`cmd/relay`（源 caster → pipe → 目的 caster）
- 仓内参考实现：`internal/inmemory`（**仅本模块可 import**）

**不做：**

- **不是** 开箱生产 Caster（无用户文件 / conf / TLS / 管理口）→ [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** NTRIP **1.0 `SOURCE <pass> /mnt`** 上传（`http.Server` 路径注释写明 v1 SOURCE 需 `net.Listen`）→ [ntripserver](./ntripserver.md) / [ntripcaster-libev](./ntripcaster-libev.md)
- **不是** BKG POSIX 订流 CLI → [ntripclient](./ntripclient.md)
- **不是** 帐号池中继产品 → [cors-relay](./cors-relay.md)
- **不解码** RTCM / 不录 RINEX → [pyrtcm](./pyrtcm.md) / [bnc](./bnc.md)
- **禁止**把本地 smoke 的 `SMOKE-PLACEHOLDER-BYTES-NOT-RTCM` 写成真实差分电文

一句话：**Go 云原生差分流网关底座**；对照 BKG **1.0 官方对** 与 **ntrip-cpp 2.0 C++ 样板**。

| 项 | 角色 |
| --- | --- |
| `NewClientRequest` | `GET` + `User-Agent: NTRIP go-gnss/ntrip/client` + `Ntrip-Version: Ntrip/2.0` |
| `NewServerRequest` | chunked `POST` + `…/server` UA + v2 头 |
| `Caster` | `SourceService` 插拔：源表 / Publisher / Subscriber |
| `cmd/relay` | 双端重连示例（**非**生产运维工具） |

### 与已文档 NTRIP 对照

| | **ntrip-go（本文）** | [ntripclient](./ntripclient.md)+[ntripserver](./ntripserver.md) | [ntrip-cpp](./ntrip-cpp.md) | [ntripcaster-libev](./ntripcaster-libev.md) |
| --- | --- | --- | --- | --- |
| 语言/形态 | **Go 库** + 示例 relay | BKG **POSIX CLI** | C++ **库+exam** | C **单二进制** |
| 协议重心 | **2.0** HTTP；客 v1 GET 可 hijack | **1.0** 为主（server 可 `-O 1`→2） | **2.0 POST** + 客 `ICY` | **1.0 SOURCE** |
| 源推 | v2 **POST**；无 `SOURCE` | `SOURCE …` / NTRIP2 http | `POST` | `SOURCE` |
| 源表 | `GET /` **可用**（空表仅 `ENDSOURCETABLE`） | client 拉公网 | **死路径** `401` | 动态 STR |
| 部署取向 | **云原生 / 嵌入服务** | 脚本/嵌入式上传订流 | 学握手 / 嵌 C++ | 实验室播发 |

## 2. 安装

```bash
# 需 Go ≥ 1.24（go.mod：go 1.24.0；本机 toolchain 拉起 go1.24.10）
go version   # 本机：go version go1.24.10 linux/amd64

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/go-gnss/ntrip.git
cd ntrip
git rev-parse --short HEAD   # 本机：6d11102

go build ./...
go test ./... -count=1
# ok  github.com/go-gnss/ntrip  ~0.1s   ← 本机 7 个测试全 PASS
# ?   github.com/go-gnss/ntrip/cmd/relay
# ok  github.com/go-gnss/ntrip/internal/inmemory  [no tests to run]

go build -o ntrip-relay ./cmd/relay
ls -la ntrip-relay   # 本机 **8598110** B
```

模块消费（服务内 embed）：

```bash
go get github.com/go-gnss/ntrip@v0.0.16   # proxy 最新标签；若要 tip 行为请 pin commit 6d11102
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `go: go.mod requires go >= 1.24` | 本机 Go 过旧 | 升 Go 或开 `GOTOOLCHAIN=auto` |
| `use of internal package …/internal/inmemory` | `internal/` 禁跨模块 | 自实现 `SourceService`，或把示例放进本仓 `cmd/` |
| 想「官方二进制」 | 上游只发库 | `go build` 自编；relay 仅示例 |

## 3. 真命令 + 期望输出

### 3.1 `relay -h`（唯一自带 CLI）

```bash
./ntrip-relay -h
```

**本机（2026-09-24 06:28 EDT）：**

```text
Usage of ./ntrip-relay:
  -dest string
    	NTRIP caster URL to stream from
  -dpass string
    	Password for accessing the Destination NTRIP caster
  -duser string
    	Username for accessing the Destination NTRIP caster
  -source string
    	Source NTRIP caster URL to stream from
  -spass string
    	Password for accessing the Source NTRIP caster
  -suser string
    	Username for accessing the Source NTRIP caster
  -timeout duration
    	NTRIP reconnect timeout (default 2ns)
```

注意：`flag.Duration("timeout", 2, …)` 的字面量 **`2` = 2 纳秒**，不是 2 秒——帮助里默认 **`2ns`** 是真坑。

无参启动会立刻对空 URL 死循环重连（测完请 `kill`）：

```text
client failed to connect <nil> Get "": unsupported protocol scheme ""
server failed to connect <nil> Post "": unsupported protocol scheme ""
```

### 3.2 库：公网源表（`NewClientRequest`）

```go
req, _ := ntrip.NewClientRequest("http://rtk2go.com:2101/")
resp, err := http.DefaultClient.Do(req)
// User-Agent=NTRIP go-gnss/ntrip/client ; Ntrip-Version=Ntrip/2.0
body, _ := io.ReadAll(resp.Body)
st, _ := ntrip.ParseSourcetable(string(body))
fmt.Println(resp.StatusCode, len(body), len(st.Mounts))
```

**本机探针（2026-09-24 06:29 EDT；`ParseSourcetable` mounts）：**

| URL | status | bytes | mounts |
| --- | ---: | ---: | ---: |
| `http://rtk2go.com:2101/` | **200** | **137925** | **766** |
| `http://www.igs-ip.net:2101/` | **200** | **85638** | **384** |
| `https://ntrip.data.gnss.ga.gov.au/` | **200** | **212642** | **918** |
| `http://caster.centipede.fr:2101/` | **200** | **276627** | **1272** |

订流需挂载账号；无订户时勿臆造帧。本机另探：`GET …/WTZR0`（假帐）→ igs **404** HTML **52** B；`GET …/NEAR`（rtk2go）→ **200** 且正文仍以 `STR;…` 开头（像回源表，**不是**近邻流验收）。

### 3.3 本地 Caster 冒烟（inmemory；口 **18701**）

仓内 `internal/inmemory` + `NewCaster`（示例程序勿提交上游）。鉴权：user/pass = `username`/`password`；挂载 `LAB1`；写入占位串（**声明非 RTCM**）。

**本机结果：**

```text
SOURCETABLE status=200 bytes=16 body_head="ENDSOURCETABLE\r\n"
SERVER status=200
UNAUTH status=401 bytes=0
CLIENT status=200
CLIENT first_read n=33 data="SMOKE-PLACEHOLDER-BYTES-NOT-RTCM\n"
NOSUCH status=404 bytes=0
```

logrus 要点：`accepted request`（POST/GET）· `connection refused … not authorized` · `mount not found` · UA=`NTRIP go-gnss/ntrip/client|server` · `request_version=2`。

`go test -v` 同仓：**TestSourcetableString / Decode / GetSourcetable / CasterServerClient / CasterHandlers / AsyncPublishSubscribe / MountInUse** → **7 PASS**（Handlers 覆盖 v1/v2 源表、401、404、PUT→501 等）。

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| 客请求 | `GET /<mnt>` + Basic；头 `Ntrip-Version: Ntrip/2.0` |
| 源请求 | `POST /<mnt>` + Basic + `Transfer-Encoding: chunked` |
| v2 成功订流 | HTTP **200** + `Content-Type: gnss/data`（Flush 后推字节） |
| v1 成功订流 | hijack 后写 **`ICY 200 OK\r\n`** |
| v2 鉴权失败 | **401** + `WWW-Authenticate: Basic realm="<path>"` |
| v2 无挂载 | **404** |
| 挂载占用 | **409**（`ErrorConflict`） |
| 空源表正文 | 仅 **`ENDSOURCETABLE\r\n`**（**16** B）——需自填 `Sourcetable` |
| 数据面 | Publisher→Subscriber **原样透传**；不校 CRC |

## 5. 参数

| API / 旗标 | 默认 / 本机 | 说明 |
| --- | --- | --- |
| `NewCaster(addr, svc, log)` | 例 `:2101` / `127.0.0.1:18701` | `ListenAndServe` |
| `-source` / `-dest` | 空 | relay 两端完整 URL（含挂载路径） |
| `-suser/-spass` `-duser/-dpass` | 空 | Basic |
| `-timeout` | **`2ns`（字面量 2）** | 须写 `-timeout 2s` |
| `SourceService` | 自实现 | `GetSourcetable` / `Publisher` / `Subscriber` |
| `NewClientV1` | TCP 手写 | 源码 **TODO: Remove v1 client** |

## 6. 接到哪步

1. 公网实时流账号 / 源表礼仪 → [data-access](../data-access.md)「实时 NTRIP」  
2. 要 **Go 服务内嵌** caster/client → **本文**  
3. 只要命令行订流/上传 → [ntripclient](./ntripclient.md) / [ntripserver](./ntripserver.md) / [pygnssutils](./pygnssutils.md)  
4. 学 C++ **2.0 POST** → [ntrip-cpp](./ntrip-cpp.md)  
5. 实验室 **1.0** 自建 → [ntripcaster-libev](./ntripcaster-libev.md)；帐号池 → [cors-relay](./cors-relay.md)  
6. 生产多用户 / TLS → [bkg-ntripcaster](./bkg-ntripcaster.md)  
7. 拆 RTCM / 录盘 → [pyrtcm](./pyrtcm.md) / [bnc](./bnc.md) → 路径 A/D

## 7. 坑（≥8）

1. **库 ≠ 产品**：无 ACL 文件、无 TLS、无管理 UI——生产请自补或换 [bkg-ntripcaster](./bkg-ntripcaster.md)。  
2. **`-timeout` 默认 2 ns**：`flag.Duration(..., 2, …)`；必须 `-timeout 2s`。  
3. **空参 relay 死循环**：空 scheme 狂打日志；测完务必杀掉。  
4. **`internal/inmemory` 不可外用**：跨模块 `go build` 直接报错；示例须落在本 module。  
5. **无 NTRIP 1.0 `SOURCE`**：与 [ntripserver](./ntripserver.md) / libev 源推语法不互通。  
6. **空源表只有 16 B**：未填充 `Sourcetable` 时 `GET /` 仍 200，但只有 `ENDSOURCETABLE`。  
7. **Go 1.24+**：旧发行版直接拒编译。  
8. **标签滞后 tip**：`v0.0.16` ≠ `6d11102`；复现请 pin commit。  
9. **`NewClientV1` 将删**：新代码别依赖。  
10. **v1 SOURCE 走不通 `http.Server`**：注释已写；勿对 Caster 发 `SOURCE`。  
11. **relay `-dest` 帮助文案写 “stream from”**：实为上传目的端（笔误）。  
12. **占位透传 ≠ RTCM**：smoke `n=33` 只证明管道；真流再用 pyrtcm/BNC。  
13. **公网「近邻」挂载名别盲信**：rtk2go `/NEAR` 本机回的是源表头，不是差分流。  
14. **客 GGA**：Handler `drainReader` 丢弃 body——NMEA 上报被忽略（符合本实现）。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| Go / 云原生嵌入差分网关 | **ntrip-go（本文）** |
| BKG 官方命令行订流 / 上传 | [ntripclient](./ntripclient.md) / [ntripserver](./ntripserver.md) |
| C++ NTRIP **2.0** 握手样板 | [ntrip-cpp](./ntrip-cpp.md) |
| 实验室 JSON **1.0** 播发 | [ntripcaster-libev](./ntripcaster-libev.md) |
| CORS 帐号池再分发 | [cors-relay](./cors-relay.md) |
| 正规多用户播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 五分钟脚本拉流 | [pygnssutils](./pygnssutils.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |
