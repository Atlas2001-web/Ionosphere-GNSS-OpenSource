# Node-NTRIP caster · `@ntrip/caster`（Node.js NTRIP 库）操作手册

目录：[`PROJECTS.json` → `caster`](../../PROJECTS.json) · 上游 <https://github.com/Node-NTRIP/caster> · npm **`@ntrip/caster` 0.3.2** · tip **`176e5cf`**（2022-12-24）· **GPL-3.0-or-later** · `Caster.NAME`=**`NodeNtripCaster/0.0.1`** · 本机验证（**2026-09-24 06:35 EDT**）：**Node v16.20.2** + `tsc` 产物；口 **18711**；空源表 body **`ENDSOURCETABLE\r\n`**（**16** B）；在线 **`STR;LAB1`**；客 `HTTP/1.1 200` + `gnss/data` 分块透传占位 **33** B（帧面 **39** B）；`POST /LAB2`→**200**；V1 `SOURCE`→**`ICY 200 OK`**；未知挂载→**500**；**未臆造 RTCM**

> 岗位：用 **TypeScript/Node** 嵌 NTRIP **V1/V2** caster（HTTP/可选 RTSP/RTP）、推拉远端、串口/文件/流传输与可插拔鉴权。冲突时：**上游 README / `src/` / 本机冒烟 > 本文**。  
> 公网源表/订流 → [data-access](../data-access.md)；生产多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)；实验室 JSON **1.0** → [ntripcaster-libev](./ntripcaster-libev.md)；Go 嵌入 → [ntrip-go](./ntrip-go.md)；门户地图 → [rtcm-ntrip-software](./rtcm-ntrip-software.md)；台站 Web → [rtkbase](./rtkbase.md)；订流脚本 → [ntrip-client](./ntrip-client.md)/[bnc](./bnc.md)。

## 1. 用途与边界

**做：**

- 库：`Caster` + `addTransport(NtripTransport.new({port}))` 监听；`AuthManager.authenticate`
- 协议：NTRIP **V1**（`SOURCE` / `ICY`）与 **V2**（`POST`/`GET` + `Ntrip-Version`）；可选 RTSP/RTP
- 传输：`NtripPushPullTransport`（push/pull 远端）、`StreamTransport`/`FileTransport`/`SerialTransport`、裸 TCP
- 源表：`generateSourcetable` / 过滤；挂载在线时动态 STR
- 依赖栈可解 RTCM/NMEA（`@gnss/rtcm` / `@gnss/nmea`）——**解码另验**，Caster 仍透传字节

**不做：**

- **不是** BKG Professional 多用户 ACL/中继产品 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** libev JSON 单二进制实验室播发 → [ntripcaster-libev](./ntripcaster-libev.md)
- **不是** Go `http.Handler` 底座 → [ntrip-go](./ntrip-go.md)
- **不是** 开箱 CLI（无 `ntripcaster` 命令）；需自写 `require`/`import` 启动
- **不保证** Node **≥18/20** 可用（`http-parser-ts` 依赖 `process.binding('http_parser')`）
- **禁止**把 smoke 占位串写成真实差分电文

一句话：**Node 生态可嵌入的 NTRIP caster 库**；对照 BKG 生产播发与 libev 轻量播发。

| | **本文 `@ntrip/caster`** | [bkg-ntripcaster](./bkg-ntripcaster.md) | [ntripcaster-libev](./ntripcaster-libev.md) | [ntrip-go](./ntrip-go.md) |
| --- | --- | --- | --- | --- |
| 形态 | **npm 库** | C 守护进程+conf | C 单二进制+JSON | Go 库+relay 示例 |
| 协议 | **V1+V2**（HTTP/RTSP/RTP） | V1/V2 生产 | **1.0 SOURCE** | 主推 **2.0** |
| 鉴权 | 自写 `AuthManager` | `*.aut` 文件 | JSON tokens | 自写 `SourceService` |
| 运行时 | **Node ≤16 实测** | 任意 Linux | libev | Go 1.24+ |

## 2. 安装

```bash
# 本机冒烟用 Node 16（系统 Node 20 会在 parser.remove 崩）
# 例：https://nodejs.org/dist/v16.20.2/node-v16.20.2-linux-x64.tar.xz
node -v   # 期望：v16.x（本机 v16.20.2）

mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/Node-NTRIP/caster.git
cd caster
git rev-parse --short HEAD   # 本机：176e5cf

npm install --legacy-peer-deps
# 入口会加载 SerialTransport → 可选依赖必须装上：
npm install --legacy-peer-deps serialport@9.2.8

npm run build    # tsc → build/
# 若新 TS 对 catch unknown 报错：保留/用已生成的 build/，或钉旧 typescript@4.3

# 应用内依赖：
# npm install -S @ntrip/caster@0.3.2
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `HTTP module imported before HTTPParser was bound` | 先 `require('http')` 再加载库 | **先** `require('@ntrip/caster')` |
| `Cannot find module 'serialport'` | optional 未装 | `npm i serialport@9` |
| Node 20：`parser.remove is not a function` | `http-parser-ts` 与新 http 不兼容 | 换 **Node 16**（或等上游修） |
| `npm ERESOLVE`（ts-jest peer） | 锁过严 | `--legacy-peer-deps` |

## 3. 真命令 + 期望输出（本机 · 口 18711）

最小启动（实验室：鉴权恒真；**公网禁止**）：

```js
// smoke.js — 必须先加载 caster，再碰 http/net
const {Caster, NtripTransport, StreamTransport, NtripVersion} = require('@ntrip/caster');
const {Readable} = require('stream');

const caster = new Caster({
  authManager: { async authenticate(a){ return {...a, authenticated:true}; } }
});
caster.addTransport(NtripTransport.new({
  port: 18711,
  versions: {[NtripVersion.V1]:true, [NtripVersion.V2]:true},
  protocols: {http:true}
})).open();

const input = new Readable({read(){}});
caster.addTransport(StreamTransport.new({
  type:'server', source:'smoke', mountpoint:'LAB1', input
})).open();
input.push(Buffer.from('SMOKE-PLACEHOLDER-BYTES-NOT-RTCM\n'));
```

用 **裸 TCP** 探（Node `http` 客户端可能被自定义 parser 搅乱头/体）：

```text
# GET /  （空挂载）
HTTP/1.1 200 OK
Server: NTRIP NodeNtripCaster/0.0.1
Content-Type: gnss/sourcetable
… body: ENDSOURCETABLE\r\n          ← 16 B

# GET /  （LAB1 在线）
… body: STR;LAB1;;;;0;;;;;;0;0;;none;;;0;none\r\nENDSOURCETABLE\r\n

# GET /LAB1 + Basic
HTTP/1.1 200 OK + Content-Type: gnss/data
body(chunked): 21\r\nSMOKE-PLACEHOLDER-BYTES-NOT-RTCM\n\r\n   ← 占位 33 B

# POST /LAB2 (Ntrip/2.0, chunked) → HTTP/1.1 200 OK
# SOURCE pass /LAB3\r\n…          → ICY 200 OK\r\n\r\n
# GET /NOSUCH                     → HTTP/1.1 500 Internal Server Error
```

**本机（2026-09-24 06:35 EDT，Node 16.20.2，tip `176e5cf`）：** 上表状态码与 body 均已复现；占位串**不是** RTCM。

## 4. I/O 与参数

| 项 | 含义 |
| --- | --- |
| 客订流 | `GET /<mnt>` + Basic；头 `Ntrip-Version: Ntrip/2.0` → `gnss/data` |
| 源推 V2 | `POST /<mnt>` + chunked |
| 源推 V1 | `SOURCE <secret> /<mnt>` → `ICY 200 OK` |
| 源表 | `GET /` → `gnss/sourcetable`；无源仅 `ENDSOURCETABLE` |
| `NtripTransportOptions.port` | 监听口（本机 **18711**） |
| `versions` / `protocols` | 开关 V1/V2、http/rtsp/rtp |
| `AuthManager` | 须返回 `authenticated`；可看 Basic/Bearer/secret |
| `StreamTransport` | 进程内喂 `Readable` 当 server |

## 5. 接到哪步

1. 公网礼仪 / 账号 → [data-access](../data-access.md)  
2. Node 服务内嵌播发 / 推拉 → **本文**  
3. 生产多用户 / conf ACL → [bkg-ntripcaster](./bkg-ntripcaster.md)  
4. 实验室 JSON 1.0 → [ntripcaster-libev](./ntripcaster-libev.md)；Go → [ntrip-go](./ntrip-go.md)  
5. Pi 基站 Web → [rtkbase](./rtkbase.md)；门户总览 → [rtcm-ntrip-software](./rtcm-ntrip-software.md)  
6. 订流 / 录盘 → [ntrip-client](./ntrip-client.md) / [bnc](./bnc.md) / [pygnssutils](./pygnssutils.md) → 路径 A/D

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | Node 20 启动即崩 | `http-parser-ts` / `parser.remove` | 用 **Node 16**；盯上游 Issue |
| 2 | `HTTPParser was bound` | `http` 先于库加载 | 调整 `require` 顺序 |
| 3 | 缺 `serialport` | 入口 re-export 串口 | `npm i serialport@9`（即使不用串口） |
| 4 | 未知挂载 **500** | 实现抛错映射 | 勿当 404；自捕 `ConnectionError` |
| 5 | `http.get` 头体错乱 | 自定义 parser 副作用 | 冒烟用 **net.Socket** / 真 NTRIP 客户端 |
| 6 | 空表只有 16 B | 无在线 SOURCE | 先 `StreamTransport`/`POST`/`SOURCE` |
| 7 | `npm run build` TS18046 | 新 tsc 更严 | 钉 `typescript@4.3` 或用已有 `build/` |
| 8 | 当 BKG 产品部署 | 无 users.aut/TLS 套件 | 生产换 [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 9 | 与 libev 混口令语法 | V1 `SOURCE` secret ≠ JSON token | 分清实现；别混文档 |
| 10 | 占位当 RTCM | Caster 不验 CRC | 真流再用 [pyrtcm](./pyrtcm.md)/BNC |
| 11 | `Caster.NAME` 仍 0.0.1 | 包版本 0.3.2 ≠ UA 字符串 | 日志认 `NodeNtripCaster/0.0.1` |
| 12 | tip 停在 2022 | 上游不活跃 | pin commit；评估 Node 生命周期 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Node/TS 服务内嵌 NTRIP | **本文** |
| 正规多用户播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 实验室 JSON 1.0 | [ntripcaster-libev](./ntripcaster-libev.md) |
| Go 云原生嵌入 | [ntrip-go](./ntrip-go.md) |
| C++ 2.0 样板 | [ntrip-cpp](./ntrip-cpp.md) |
| Pi 基站一键 | [rtkbase](./rtkbase.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |

## 8. 相关

[bkg-ntripcaster](./bkg-ntripcaster.md) · [ntripcaster-libev](./ntripcaster-libev.md) · [ntrip-go](./ntrip-go.md) · [ntrip-cpp](./ntrip-cpp.md) · [ntrip-client](./ntrip-client.md) · [bnc](./bnc.md) · [rtkbase](./rtkbase.md) · [rtcm-ntrip-software](./rtcm-ntrip-software.md) · [pygnssutils](./pygnssutils.md) · [data-access](../data-access.md) · [README](./README.md)
