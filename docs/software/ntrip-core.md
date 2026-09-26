# ntrip-core · Rust 异步 NTRIP 客户端库操作手册

目录：[`PROJECTS.json` → `ntrip-core`](../../PROJECTS.json) · 上游 <https://github.com/greenforge-labs/ntrip-core> · crates.io **`ntrip-core` 0.2.0**（2026-01-10 03:38 EST 发布；0.1.0 为 2025-12-20 00:00 EST）· git tag 只有 **`v0.1.0`**=`c6b661a`（**无 v0.2.0 tag**，CHANGELOG 的 compare 链接指向不存在的 tag）· main **`5949d60`**（2026-01-10 03:34 EST，“Release v0.2.0”）· **MIT** · ★**4** · `rust-version = "1.75"` · 实测 2026-09-26 05:19–05:32 EDT（rustc **1.98.1**，Debian RTKLIB str2str 2.4.3，pyrtcm 1.2.0，pygnssutils 1.2.7）

> 岗位：**纯库**（无 CLI/无 `[[bin]]`）：Tokio 上的 NTRIP **客户端**——拉 sourcetable、按坐标找最近 RTCM 挂载点、订一个挂载点拿**原始字节**。**不解 RTCM**（解帧 → [rtcm-rs](./rtcm-rs.md)），不做 caster/server，不上传。冲突时：**docs.rs / 上游源码 > 本文**。  
> 同名易混：PROJECTS 另有 `NtripCore`（bouskdav，C#），与本库无关。时间：上游提交/发布时间换算为美东（1 月为 EST），实测窗口 EDT。

## 1. 用途与边界

| 能力 | 上游声称 | 本文实测 |
| --- | --- | --- |
| NTRIP v1（`GET … HTTP/1.0`，收 `ICY 200 OK`） | 有 | ✅ 公网 centipede + 本机 caster |
| NTRIP v2（`HTTP/1.1` + `Ntrip-Version: Ntrip/2.0`，chunked 解码） | 有，默认 `Auto` 发 v2 请求 | ✅ 本机 chunked 逐字节一致；centipede 回 v2 但**不分块** |
| TLS（tokio-rustls，根证书=内置 `webpki-roots`） | `.with_tls()` | ✅ 只测 GA `ntrip.data.gnss.ga.gov.au:443` 的 sourcetable；TLS 订流需账号，**未测** |
| sourcetable 解析（STR/CAS/NET）+ Haversine 最近挂载点 | 有 | ✅ 4 个公网 caster；与独立 Python 解析逐条一致 |
| GGA 上报（v2 `Ntrip-GGA` 头 + 连上后流内 `send_gga`） | 有 | ✅ 头部送达（本机 caster 日志）；VRS 效果**未测** |
| 自动重连（默认 3 次 × 1 s，重连后重发上次 GGA） | 有 | ✅ 但“3 次”并非上限，见 §6 坑 3 |
| HTTP 代理（CONNECT，`$HTTP_PROXY`） | 0.2.0 新增 | **未测** |
| MSRV 1.75 | 声称 | **未测**（只用 1.98.1 构建） |

**不做：** RTCM/SPARTN 解码、CRC 校验、落盘、NMEA 解析、caster。接收机串口转发路径**未在真接收机测试**。

## 2. 安装（示例 crate，不用 cargo install）

```toml
# Cargo.toml
[dependencies]
ntrip-core = "=0.2.0"
tokio = { version = "1", features = ["rt-multi-thread", "macros", "time"] }
```

```bash
export TMPDIR=/tmp/ntripcore-man CARGO_TARGET_DIR=/tmp/ntripcore-man/target CARGO_HOME=/tmp/ntripcore-man/cargo
cargo build --release          # 82 个包，冷编译 29.5 s，二进制 5736776 B
```

实际解析：tokio 1.53.1、tokio-rustls 0.26.5、rustls 0.23.45（默认后端 **aws-lc-rs 1.18.1**，含 C 代码——“无 OpenSSL”≠“无 C 工具链”）、webpki-roots 0.26.11→1.0.9、base64 0.22、chrono、thiserror 1、tracing。上游 `cargo test`（19.0 s）：单元 **22** + 协议 **8** + doctest **7** 全过；联网集成 2 过 / 12 `#[ignore]`。

公开 API（`lib.rs` re-export）：

| 类型 | 主要方法/字段 |
| --- | --- |
| `NtripConfig` | `new(host, port, mount)`、`with_credentials`、`with_tls`、`with_tls_skip_verify`、`with_version(NtripVersion::{V1,V2,Auto})`、`with_timeout`（仅 TCP 连接，默认 15 s）、`with_read_timeout`（默认 30 s，0=不限）、`with_reconnect(n, ms)` / `without_reconnect`、`with_proxy` / `with_proxy_from_env`、`validate` |
| `NtripClient` | `new(cfg)?`、`connect()`、`connect_with_gga(Option<&GgaSentence>)`、`read_chunk(&mut [u8]) -> usize`、`send_gga`、`disconnect`、`is_connected`、**关联函数** `get_sourcetable(&cfg)` |
| `Sourcetable` | `streams/casters/networks`、`parse(&str)`、`rtcm_streams`、`streams_by_distance`、`nearest_rtcm_stream(lat, lon)`、`find_streams(pat)` |
| `StreamEntry` | 19 字段（mountpoint, format, latitude, longitude, nmea_required, bitrate…）、`distance_km`、`is_rtcm` |
| `GgaSentence` | `new(lat, lon, alt)`、`with_quality/with_satellites/with_hdop`、`to_nmea()` |
| `Error`（`#[non_exhaustive]`） | `ConnectionFailed`、`Timeout`、`ReadTimeout`、`AuthenticationFailed`、`MountpointNotFound`、`HttpError`、`TlsError`、`NetworkError`、`StreamDisconnected`、`InvalidConfig`、`SourcetableParseError`、`ProxyError` |

## 3. 例子 + 真实输出

示例程序核心（自写 `nc-demo`，CRC-24Q 自己数 RTCM3 帧；`table`/`stream` 两个子命令）：

```rust
let cfg = NtripConfig::new(host, port, "");                  // table
let t = NtripClient::get_sourcetable(&cfg).await?;
println!("STR={} CAS={} NET={} rtcm_streams={}", t.streams.len(), t.casters.len(),
         t.networks.len(), t.rtcm_streams().len());
if let Some((s, d)) = t.nearest_rtcm_stream(lat, lon) { println!("nearest {} {:.1} km", s, d); }

let cfg = NtripConfig::new(host, port, mount).with_credentials(u, p)   // stream
    .with_version(NtripVersion::Auto).with_timeout(5).with_reconnect(1, 500);
let mut c = NtripClient::new(cfg)?;
tokio::time::timeout(Duration::from_secs(10), c.connect_with_gga(gga.as_ref())).await??; // 外包超时，见坑 4
loop { let n = c.read_chunk(&mut buf).await?; data.extend_from_slice(&buf[..n]); }
```

**sourcetable（公网，05:21 EDT）：**

```text
$ nc-demo table rtk2go.com 2101 x 40.7128 -74.0060
STR=766 CAS=0 NET=1 rtcm_streams=743 elapsed=0.170s
nearest VIAM_BASE2 (RTCM 3.2) - GPS+GLO+GAL+BeiDou @ (40.7400, -73.9500) 5.6 km
$ nc-demo table caster.centipede.fr 2101
STR=1276 CAS=1 NET=1 rtcm_streams=1276 elapsed=0.945s
$ nc-demo table ntrip.data.gnss.ga.gov.au 443 tls
STR=922 CAS=1 NET=2 rtcm_streams=922 elapsed=1.736s
$ nc-demo table euref-ip.net 2101
STR=225 CAS=5 NET=3 rtcm_streams=225 elapsed=0.640s
```

rtk2go 766 条 `nmea_required` **全为 1**；centipede 1272/1274 为 0（05:24 另一次拉取为 1274 条，表是活的）。

**rtk2go 订流失败（真实）：** 上游 README/示例用 `user@example.com`——

```text
$ nc-demo stream rtk2go.com 2101 VIAM_BASE2 ntripcore-test@example.com none 20 live.bin auto recon1
ERR HttpError { host: "rtk2go.com", status_code: 400, reason: "HTTP/1.1 400" } …   # 正文: "This eMail is not allowed."
$ … v1 …
ERR HttpError { host: "rtk2go.com", status_code: 0, reason: "200 Ok, its now sandbox time." }
```

没有真实邮箱，**rtk2go 订流未测**；改用 centipede（公开账号 `centipede/centipede`）：

```text
$ nc-demo stream caster.centipede.fr 2101 IPGP centipede centipede 30 live_nc.bin auto recon1
connected elapsed=0.182s
bytes=79161 reads=133 frames=461 crc_bad_skips=0 types={1004: 30, 1005: 3, 1006: 1, 1008: 3, 1012: 30,
 1019: 30, 1020: 30, 1033: 3, 1042: 30, 1045: 60, 1046: 60, 1077: 30, 1087: 30, 1097: 30, 1107: 30,
 1127: 60, 1230: 1} elapsed=30.185s
```

≈ 2.6 kB/s、1 Hz MSM7（1077 GPS / 1087 GLO / 1097 GAL / 1107 SBAS / 1127 BDS）+ 星历 1019/1020/1042/1045/1046。centipede 对 v2 请求回 `HTTP/1.1 200 OK` + `Ntrip-Version`，**不分块**（库按 raw 读，正确）。

## 4. 交叉检查

| 对照 | 方法 | 结果 |
| --- | --- | --- |
| 公网同流 | centipede IPGP：str2str 先起 2 s、晚停 4 s，同时 ntrip-core 收 30 s | str2str 89701 B；ntrip-core 79161 B **是 str2str 文件的连续子串**（偏移 5290），逐字节一致；pyrtcm 数出 461 帧=自写 CRC 461 帧，类型序列相同 |
| 本机回放 | 去头后 `clean.bin` 89661 B / 521 帧（md5 `fe40b894…`），Python caster 以 ICY、ICY+头、v2 chunked（块长随机 1–1500）、v2 非分块、需 Basic 认证 5 种方式发 | ntrip-core **5/5 `cmp` 一致**，521 帧；str2str ICY 一致、ICY+头多 21 B、chunked **0 B**（2.4.3 只认 `ICY 200`）；pygnssutils 1.2.7 输出为连续子串但缺头尾（80–83 kB，丢起始同步段） |
| sourcetable | rtk2go 原始 138658 B 由本机 caster 回放；独立 Python 按 `;` 切 ≥19 字段 | ntrip-core 768 条 = Python 768 条，mountpoint/format/lat/lon/nmea 逐条一致 |
| GGA | `to_nmea()` 校验和用 Python 独立 XOR | 3/3 一致（但见坑 6 的进位错误） |

真实命令（05:25 EDT 公网；05:28 EDT 本机回放）：

```text
$ timeout 34 str2str -in ntrip://centipede:centipede@caster.centipede.fr:2101/IPGP -out file://live_s2s.bin &
$ sleep 2; nc-demo stream caster.centipede.fr 2101 IPGP centipede centipede 30 live_nc.bin auto recon1
$ python cmp.py live_nc.bin live_s2s.bin            # pyrtcm RTCMReader + bytes.find
live_nc.bin 79161 B frames 461
live_s2s.bin 89701 B frames 521
A is contiguous substring of B at offset 5290
type seq equal True
$ nc-demo stream 127.0.0.1 18810 V2C - - 5 rep_V2C.bin auto norecon
connected elapsed=0.000s
bytes=89661 reads=115 frames=521 crc_bad_skips=0 types={1004: 34, 1005: 3, …}
ERR StreamDisconnected { reason: "Chunked stream ended" } | Stream disconnected: Chunked stream ended
$ cmp rep_V2C.bin clean.bin && echo IDENTICAL
IDENTICAL
```

附带发现：centipede 的 v1 应答是 `ICY 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\n`，**RTKLIB str2str 2.4.3 把后 40 B 头部当数据写进文件**；ntrip-core 走 v2 无此问题。

## 5. 错误用例（合成，本机 Python caster；另注“公网”者为真实）

| 场景 | 返回 | 重连? | 静默? |
| --- | --- | --- | --- |
| 错密码 → `401 Unauthorized` | `AuthenticationFailed{user}` 3 ms | 否（connect 直接返回） | 否 |
| 无账号访问需认证挂载 | `AuthenticationFailed{username:""}` | 否 | 否 |
| `404 Not Found` | `MountpointNotFound` | 否 | 否 |
| 公网 centipede v2 请求不存在挂载 | `MountpointNotFound`（真 404） | — | 否 |
| 公网 centipede **v1** 请求不存在挂载 → `SOURCETABLE 200 OK` | **`connected`**，277313 B sourcetable 当数据交出，0 帧 | — | **是** |
| 合成：挂载不存在回 sourcetable（Auto） | 同上，138658 B，0 帧 | — | **是** |
| 公网 centipede 错密码 | 照样出流（caster 不校验） | — | — |
| `ICY 200 OK` | 正常，V1 | — | — |
| `HTTP/1.1 200 OK` 非分块 | 正常，V1 raw | — | — |
| `HTTP/1.1 200`（无 reason） | `HttpError{status_code:200}` | 否 | 否，但误报 |
| `Transfer-Encoding: chunked` | 正常解块，逐字节一致 | — | — |
| `Transfer-Encoding:chunked`（无空格）或 `TRANSFER-ENCODING:  Chunked` | 当 raw：90450 B，块长行混入，415 帧 + 107 次 CRC 失配 | — | **是** |
| 非法块长 `zz` | `NetworkError(InvalidData "Invalid chunk size: zz")` | 默认会重连 | 否 |
| 头部 > 4096 B | `NetworkError("Header too large or incomplete")` | 否 | 否 |
| `ICY 200 OK\r\n` 与后续头分两个 TCP 段到达 | 40 B 头部文字混进数据 | — | **是** |
| caster 发 2000 B 即断（默认重连） | 20 s 内服务端见 **20** 次连接，交出 40000 B（同一段 ×20），19 次 CRC 失配，**从不报错** | 是，无上限 | **是** |
| 同上 `without_reconnect()` | `StreamDisconnected("Server closed connection")` | 否 | 否 |
| 连上后停发（read_timeout 2 s，默认重连） | 30 s 内 10 次重连，从不报错 | 是，无上限 | **是** |
| 同上 `without_reconnect()` | `ReadTimeout{2}` @2.008 s | 否 | 否 |
| 接受 TCP 但不回头部 | `connect` **永久挂起**（外包 10 s 超时才返回） | — | **是** |
| 端口拒绝 | `ConnectionFailed(ConnectionRefused, os 111)` | — | 否 |
| DNS 失败 `no-such-host.invalid` | `ConnectionFailed(Uncategorized "failed to lookup address information")` 7 ms | — | 否 |
| sourcetable 返回 `401` | `HttpError{401}`（**不是** `AuthenticationFailed`） | — | 否 |
| sourcetable 发完不关连接 | 15.003 s 后 `Timeout{15}`，已收完整表被丢弃 | — | 否，但误报 |
| sourcetable 用 chunked 回 | STR **575/768**、NET 0 | — | **是** |
| sourcetable > 1 MB（1109264 B） | `SourcetableParseError("too large (>1MB)")` | — | 否 |
| 畸形 sourcetable（9 行） | 得 5 条：18 字段 STR、小写 `str;`、短 CAS 丢；`abc`/`50,10` 坐标变 **0.00,0.00**；非 UTF-8 变 U+FFFD | — | **是** |

典型错误原文（合成）：

```text
ERR AuthenticationFailed { host: "127.0.0.1", username: "user" } | Authentication failed for 127.0.0.1 (user: user) elapsed=0.003s
ERR HttpError { host: "127.0.0.1", status_code: 200, reason: "HTTP/1.1 200" } | HTTP error from 127.0.0.1: 200 HTTP/1.1 200
ERR Timeout { timeout_secs: 15 } | Connection timed out after 15 seconds elapsed=15.003s      # sourcetable 不关连接
ERR connect hung >10s (outer tokio timeout) elapsed=10.002s                                  # 哑 caster
```

## 6. I/O

- **入：** host/port/mount/账号（含控制字符 → `InvalidConfig`，防头注入）；可选 `GgaSentence`（十进制度、m）。请求 UA 固定 `NTRIP ntrip-core/0.2.0`；sourcetable 恒用 `GET / HTTP/1.0`。
- **出：** `read_chunk` 返回原始字节数（v2 已去 chunk 包装）；**不保证帧边界**（centipede 30 s：133 次读 461 帧）。sourcetable → `Vec<StreamEntry>`，坐标 f64 度，`distance_km` 用 R=6371 km。
- **默认值：** `timeout_secs=15`、`read_timeout_secs=30`、`max_reconnect_attempts=3`、`reconnect_delay_ms=1000`、`ntrip_version=Auto`、`use_tls=false`。
- **GGA 实例**（`GgaSentence::new(40.0,-75.0,100.0)`，默认 quality 1/10 星/HDOP 1.0，校验和经 Python 复核）：
  `$GPGGA,093120.00,4000.0000,N,07500.0000,W,1,10,1.0,100.0,M,0.0,M,,*40`
- **日志：** `tracing`，需自己装 subscriber；`Authorization` 在 debug 日志里打码。

## 7. 坑

1. **v1 + 不存在挂载 = “连接成功”**：caster 回 `SOURCETABLE 200 OK` 时 `contains("200 OK")` 放行，把表当 RTCM 交给你。上层务必解帧/校 CRC。
2. **chunked 识别靠字面 `transfer-encoding: chunked`**（小写后精确匹配含一个空格）；变体空白即把块长行混进数据。状态行也须含 `200 OK`，裸 `HTTP/1.1 200` 被判错。
3. **重连计数在每次 `read_chunk` 内重置**：只要重连后能读到 1 字节就清零，“3 次”对抖动 caster 形同无限；重连后数据从新连接起点续，**不去重、不对齐帧**（本例同一 2000 B 重复 20 次）。需要感知断线就 `without_reconnect()` 自己管。
4. **`with_timeout` 只管 TCP connect**：发请求后读头部、TLS 握手之后读头部**无超时**，哑 caster 让 `connect()` 永挂——外面包 `tokio::time::timeout`。
5. **sourcetable 读到 EOF 才算完**：caster 不关连接就 15 s 后报 `Timeout`；不解 chunked；>1 MB 直接拒。
6. **GGA 进位错误**：`GgaSentence::new(40.99999999, -74.99999999, …)` 输出 `4060.0000,N,07460.0000,W`（应为 `4100.0000`/`07500.0000`）；|度| 小数部分 ≥ 0.9999992（距整度约 9 cm 内，分四舍五入到 60.0000）即触发。`new()` 默认冒充 quality 1/10 星/HDOP 1.0（`Default` 则是 0/0/99.9）；时间取系统 UTC 钟，`$GPGGA` 前缀固定。
7. **rtk2go 用 `@example.com` 会被 400**（上游示例原样照抄即失败）；v1 则回非标准 `200 Ok, its now sandbox time.` → `HttpError{status_code:0}`。须用真实邮箱。
8. **TLS 根证书是编进去的 Mozilla 集**（代码注释写“system roots”但实为 `webpki_roots`）：企业私有 CA 只能 `with_tls_skip_verify()`（不安全）。
9. `StreamEntry` 数值解析失败一律静默给 0（坐标 0,0 会进 `nearest_rtcm_stream` 候选）；少于 19 字段的 STR 被丢。
10. 没有 v0.2.0 tag：要锁源码请锁 crates.io `=0.2.0` 或 commit `5949d60`。

## 8. 接到哪步

`ntrip-core`（原始字节）→ [rtcm-rs](./rtcm-rs.md) / [pyrtcm](./pyrtcm.md) 解帧 → [rtklib](./rtklib.md) `str2str`/`rtkrcv` 或接收机串口（**未在真接收机测试**）；落盘后 → [rtcm3torinex](./rtcm3torinex.md)。

## 9. 选型

| 你要… | 用 |
| --- | --- |
| Rust/Tokio 里只要“原始字节 + 结构化 sourcetable + 最近挂载点”，要 TLS/代理 | **ntrip-core（本文）** |
| Rust 客户端且顺手解 RTCM（内置 rtcm-rs、带 `simple-cli`） | [ntrip-client](./ntrip-client.md) |
| Go 客户端/服务端/caster 底座 | [ntrip-go](./ntrip-go.md) |
| 命令行一把拉流/转发（C，BKG） | [ntripclient](./ntripclient.md) + [ntripserver](./ntripserver.md) |
| Python asyncio 握手/上传 | [ntripstreams](./ntripstreams.md)；CLI 全家桶 → [pygnssutils](./pygnssutils.md) |
| 只浏览 sourcetable/地图 | [ntripbrowser](./ntripbrowser.md) |
| C++ 客户端/小 caster | [ntrip-cpp](./ntrip-cpp.md)、[ntripcaster-libev](./ntripcaster-libev.md)、[bkg-ntripcaster](./bkg-ntripcaster.md) |
| 解 RTCM3 帧 | [rtcm-rs](./rtcm-rs.md)、[go-gnss-rtcm](./go-gnss-rtcm.md)、[pyrtcm](./pyrtcm.md) |

**未测汇总：** rtk2go 订流（需真实邮箱）、TLS 订流、HTTP 代理、VRS/GGA 实效、MSRV 1.75、长时（>30 s）稳定性、真接收机。
