# ntripcaster-libev · libev NTRIP Broadcaster 操作手册

目录：[`PROJECTS.json` → `ntripcaster-libev`](../../PROJECTS.json) · 上游 <https://github.com/tisyang/ntripcaster> · tip **`cc17929`** · 源码 `VERSION`=**`1.1.0`** · **BSD-3-Clause** · NTRIP **1.0** · 依赖 **libev** + **cmake** · 本机验证（2026-09-24 06:15 EDT）：`cmake`/`make` → `./ntripcaster`；监听 **2101**；空源表 → 在线 **STR;LAB1**；源端 `ICY 200` / `ERROR - Bad Password`；客户端 `ICY 200` / `401`；字节透传（**未臆造 RTCM 帧体**） · **质检复跑** 2026-09-24 06:21 EDT（tip **`cc17929`**/`VERSION`=**1.1.0**；二进制 **74152** B；口 **2101**；空表 CL=**16**；在线 **STR;LAB1** CL=**111**；源 `ICY 200 OK\r\n`=**12** B / `ERROR - Bad Password` / `ERROR - Bad Mountpoint`；客 `ICY 200`=**12** B / **401**；未知挂载→源表；占位串透传 **match**；**未臆造 RTCM**；交叉 [cors-relay](./cors-relay.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[pygnssutils](./pygnssutils.md)/[data-access](../data-access.md)）

> 岗位：本机/实验室 **自建播发**（SOURCE 推流 → 动态源表 → CLIENT 订流）。JSON 配置；**无** `-h`/`--help`（多余参数当配置文件名）。冲突时：**上游 README / 源码 > 本文**。  
> 公网源表/订流入口 → [data-access](../data-access.md)「实时 NTRIP」；同作者 **帐号池中继** → [cors-relay](./cors-relay.md)；生产多用户播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)；脚本客户端 → [pygnssutils](./pygnssutils.md)。

## 1. 用途与边界

**做：**

- NTRIP **1.0** Broadcaster：`SOURCE <passwd> /<mnt>` 推流 + `GET /<mnt>` Basic 订流
- **动态源表**：仅列出**当时在线** SOURCE 挂载（无源 → 只有 `ENDSOURCETABLE`）
- JSON 鉴权：`tokens_client`（`user:pass` → 挂载/`*`）· `tokens_source`（口令 → 挂载/`*`）
- 单端口默认 **2101**（可改 `listen_port`）；限流 `max_client` / `max_source` / `max_pending`

**不做：**

- **不是** 上游帐号池中继 / 管理口 `USER-*` → [cors-relay](./cors-relay.md)
- **不是** NTRIP 2.0 / TLS / 正式 ACL 文件 / conf 中继项 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** 多流 GUI / 录 RINEX → [bnc](./bnc.md)
- **不是** 源表探测主力 → [ntripbrowser](./ntripbrowser.md) / [ntripstreams](./ntripstreams.md) / [ntrip-client](./ntrip-client.md)
- **不解码**、不校验 RTCM CRC；透传任意字节；**禁止**把实验室占位字节写成真实差分电文

一句话：**轻量自建播发端**；电离层产品仍在客户端落盘/转 RINEX 之后。对照同作者 [cors-relay](./cors-relay.md)（拉上游再分发）与 [bkg-ntripcaster](./bkg-ntripcaster.md)（生产级多用户）。

| 项 | 角色 |
| --- | --- |
| 默认 `0.0.0.0:2101` | Caster（SOURCE + CLIENT 同口） |
| CWD `ntripcaster.json` | 配置（可用 argv[1] 换路径） |
| 无管理 TCP / 无 SQLite | 改口令 = 改 JSON 后重启 |

## 2. 安装

```bash
sudo apt-get install -y build-essential cmake libev-dev git
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --recurse-submodules https://github.com/tisyang/ntripcaster.git
cd ntripcaster
git rev-parse --short HEAD   # 本机：cc17929
mkdir -p build && cd build
cmake ..
make -j"$(nproc)"
ls -la ntripcaster          # 本机 **74152** B
cp ../ntripcaster.json .
```

`cmake_minimum_required(2.8)` 在新 CMake 上仅 Deprecation Warning。Windows 需 MinGW（上游说明）；本手册只验证 Linux。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 缺 `ev.h` | 未装 libev | `libev-dev` |
| submodule 空 | 未 `--recurse` | `git submodule update --init` |
| `Address already in use` | 2101 被占 | 改 JSON `listen_port` 或停占用进程 |
| 无 Usage | 设计如此 | 参数 = 配置文件路径，不是 `-h` |

## 3. 冒烟：启动 → 空源表 → SOURCE → STR → 订流

**无** CLI 帮助。教学口令课后立刻改；口令**勿进 git**。

```bash
cd ~/iono_ops/ntripcaster/build
# 默认仓库自带 ntripcaster.json：test:test / source 口令 test / 挂载 *
stdbuf -oL -eL ./ntripcaster ntripcaster.json
```

**本机启动横幅 + 日志（2026-09-24 06:15 EDT，ANSI 已剥；质检复跑 06:21 EDT 进程仍在听 2101）：**

```text
ntripcaster ver 1.1.0
by https://github.com/tisyang/ntripcaster
10:15:00.244 [INFO ] ntripcaster.c:755: using config file 'ntripcaster.json'
10:15:00.244 [INFO ] ntripcaster.c:717: load client tokens count: 1
10:15:00.244 [INFO ] ntripcaster.c:734: load client tokens count: 1
10:15:00.244 [INFO ] ntripcaster.c:739: use addr: 0.0.0.0
10:15:00.244 [INFO ] ntripcaster.c:740: use port: 2101
10:15:00.244 [INFO ] ntripcaster.c:742: use max client limit: 0
10:15:00.244 [INFO ] ntripcaster.c:743: use max source limit: 0
10:15:00.244 [INFO ] ntripcaster.c:744: use max pending limit: 0
10:15:00.244 [INFO ] ntripcaster.c:774: setup server on 0.0.0.0:2101 OK.
```

说明：第二行「load client tokens」实际是 **source tokens**（源码日志字符串写错）；`max_pending` 打印为 **0** 见 §6 坑（JSON 写了 10，因源码笔误被 `max_source` 覆盖）。stdout 可能全缓冲 → 用 `stdbuf -oL`。

### 3.1 空源表（无 SOURCE）

```bash
python3 - <<'PY'
import socket
s=socket.create_connection(('127.0.0.1',2101),timeout=3)
s.sendall(b'GET / HTTP/1.0\r\nUser-Agent: NTRIP lab/1.0\r\n\r\n')
print(s.recv(4096).decode('latin-1'))
PY
```

**本机真实响应（Content-Length: 16 = `ENDSOURCETABLE\r\n`；Date 为 UTC；质检复跑 06:21 EDT 同 CL=16）：**

```text
SOURCETABLE 200 OK
Server: https://github.com/tisyang/ntripcaster.git
Date: Thu Sep 24 10:14:40 2026 UTC
Connection: close
Content-Type: text/plain
Content-Length: 16

ENDSOURCETABLE
```

### 3.2 SOURCE 推流（NTRIP 1.0）

```text
SOURCE <passwd> /<mnt>\r\n
Source-Agent: NTRIP <name>\r\n
\r\n
```

**本机真实往返（口令 `test`，挂载 `LAB1`）：**

```text
>>> SOURCE wrong /LAB1 + Source-Agent
ERROR - Bad Password

>>> SOURCE test /LAB1 + Source-Agent
ICY 200 OK

>>> 同挂载再 SOURCE（已有源）
ERROR - Bad Mountpoint
```

SOURCE 须**保持连接**；挂断后该 STR 从源表消失。

### 3.3 在线源表 + 客户端鉴权

SOURCE 在线后再次 `GET /`：

```text
SOURCETABLE 200 OK
Server: https://github.com/tisyang/ntripcaster.git
Date: Thu Sep 24 10:15:02 2026 UTC
Connection: close
Content-Type: text/plain
Content-Length: 111

STR;LAB1;LAB1;RTCM3X;1005(10),1074-1084-1124(1);2;GNSS;NET;CHN;0.00;0.00;1;1;None;None;B;N;0;
ENDSOURCETABLE
```

STR 字段由源码**硬编码模板**生成（非真实站元数据）；末段 `0` 为当时 `in_bps`。源表缓存约 **3 s**。质检复跑：在线 body **111** B；未知挂载 `/NOPE`（带合法 Basic）→ **仍回源表**非 401；SOURCE 挂断后 ≥3 s → 空表 CL=**16**。

客户端（挂载**必须已有 SOURCE**，否则仍回源表，**不会**先 401）：

```bash
# Basic base64('test:test') = dGVzdDp0ZXN0
python3 - <<'PY'
import base64, socket, time
# 先另开进程保持 SOURCE，再跑本段
tok=base64.b64encode(b'test:test').decode()
bad=base64.b64encode(b'test:wrong').decode()
for label,t in [('bad',bad),('ok',tok)]:
    s=socket.create_connection(('127.0.0.1',2101),timeout=3)
    s.sendall(f'GET /LAB1 HTTP/1.0\r\nUser-Agent: NTRIP lab/1.0\r\nAuthorization: Basic {t}\r\n\r\n'.encode())
    time.sleep(0.3)
    print(label, repr(s.recv(256).decode('latin-1')))
    s.close()
PY
```

**本机（质检复跑 06:21 EDT：握手段均恰 **12** B/`\r\n` 结尾）：**

```text
bad → HTTP/1.0 401 Unauthorized
ok  → ICY 200 OK
```

随后 SOURCE 侧写入的字节会原样到 CLIENT。本机用占位串 `LAB-BYTES-0123456789\n` 验证透传成功（质检复跑 **match=True**）——**这不是 RTCM**；有真接收机/文件源后再对接 [pyrtcm](./pyrtcm.md) / [bnc](./bnc.md)。

联调客户端示例（有真源后）：

```bash
# 见 docs/software/pygnssutils.md；口令勿进 git
# gnssntripclient --server 127.0.0.1 --port 2101 --https 0 \
#   --mountpoint LAB1 --ntripuser test --ntrippassword "$PASS" \
#   --datatype RTCM --ntripversion 1.0
```

## 4. I/O 字段与约定

| 项 | 含义 |
| --- | --- |
| 启动横幅 | `ntripcaster ver 1.1.0` + 仓库 URL |
| argv[1] | 配置文件路径；缺省 `ntripcaster.json`（CWD） |
| `tokens_client` 键 | 明文 `user:pass`；线上 Basic = Base64 该串 |
| `tokens_source` 键 | **仅口令**（无用户名）；`SOURCE <passwd> /mnt` |
| 挂载值 `*` | 任意挂载；否则须精确匹配 |
| 源表 | **仅在线 SOURCE**；无静态 sourcetable.dat |
| NTRIP 版本 | **1.0**（`ICY 200 OK`） |
| User-Agent / Source-Agent | **必填**；缺则握手失败并关连接 |

最小 JSON（与仓库默认一致，教学用）：

```json
{
  "listen_addr": "0.0.0.0",
  "listen_port": 2101,
  "max_client": 0,
  "max_source": 0,
  "max_pending": 10,
  "tokens_client": { "test:test": "*" },
  "tokens_source": { "test": "*" }
}
```

`0` = 对应上限无限制（pending 名义默认 10，见坑）。

## 5. 接到哪步

1. 需要公网实时流 → [data-access](../data-access.md)「实时 NTRIP」  
2. 本机自建轻量播发 → **本文**  
3. 上游 CORS 帐号池再分发 → [cors-relay](./cors-relay.md)  
4. 正式多用户 / 中继配置项 → [bkg-ntripcaster](./bkg-ntripcaster.md)  
5. 客户端探表/订流 → [ntripbrowser](./ntripbrowser.md) / [pygnssutils](./pygnssutils.md) / [ntrip-client](./ntrip-client.md) / [bnc](./bnc.md)  
6. 落盘后 TEC/定位 → 路径 A/D

## 6. 坑（≥8）

1. **无 `-h`**：`./ntripcaster -h` 会把 `-h` 当配置文件名并尝试启动。  
2. **无源订挂载 = 源表**：`GET /LAB1` 在无 SOURCE 时回 `SOURCETABLE`，**不是** 401（质检复跑挂断后带 Basic 亦然）——先起源再测鉴权；未知挂载同理。  
3. **必须带 Agent 头**：CLIENT 要 `User-Agent:`，SOURCE 要 `Source-Agent:`，否则静默失败。  
4. **同挂载单源**：第二路 SOURCE → `ERROR - Bad Mountpoint`（占用中）。  
5. **`max_pending` 笔误**：`caster_init_config` 用 `cJSON_IsNumber(max_source)` / `max_source->valueint` 写 pending；JSON `max_source:0` 时 pending 被改成 **0**（日志可见）。  
6. **日志「client tokens」重复**：source 加载也打印 `load client tokens count`。  
7. **STR 元数据是模板**：经纬度/`RTCM3X`/消息列表**不代表**真实站；只作挂载存在提示。  
8. **源表 3 s 缓存**：刚上线/刚下线可能短暂看到旧表。  
9. **口令在 JSON 明文**：公网务必改强口令 + 防火墙；勿提交真实口令。  
10. **NTRIP 1.0 only**：2.0/TLS 客户端请换 [bkg-ntripcaster](./bkg-ntripcaster.md) 或改客户端。  
11. **stdout 缓冲**：无 `stdbuf` 时横幅可能迟迟不出现。  
12. **透传 ≠ 差分已通**：仅 `ICY 200` + 任意字节不够当 RTCM 验收——用真源再验。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 实验室自建轻量播发（JSON） | **ntripcaster-libev（本文）** |
| 上游帐号池 → 内网多用户中继 | [cors-relay](./cors-relay.md) |
| 正规多用户播发 / 中继配置项 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 五分钟脚本拉流 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 多流 GUI 录盘 | [bnc](./bnc.md) |
| 只查源表 | [ntripbrowser](./ntripbrowser.md) |
