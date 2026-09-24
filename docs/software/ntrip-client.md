# ntrip-client · Rust NTRIP 客户端操作手册

目录：[`PROJECTS.json` → `ntrip-client`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/ntrip-client> · crates.io **`ntrip-client` 0.2.1** · tip **`7d4c6d3`**（tag `v0.2.1`）· **MPL-2.0** · MSRV **1.82** · tokio + `rtcm-rs` **0.11** · 本机验证 **rustc 1.98.1** + `cargo install --path . --example simple-cli`（2026-09-24 05:13 EDT）：rtk2go **766** / igs-ip **384** / centipede **1270** 挂载；`find-nearest`；centipede `VALDM` 订流 **86** 帧/8 s；rtk2go 无订户空响应、假口令 **403**；igs-ip 订流 **401**

> 岗位：纯 Rust **异步 NTRIP 客户对象**（拉 sourcetable / 订挂载 / `rtcm-rs` 解帧）+ 仓内示例 CLI **`simple-cli`**。冲突时：**本机 `simple-cli -h` / 上游 README / docs.rs > 本文**。  
> Python asyncio 轻量握手 → [ntripstreams](./ntripstreams.md)；多协议 CLI/小 caster → [pygnssutils](./pygnssutils.md)；生产 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)；多流 GUI → [bnc](./bnc.md)；同生态 Rust CRX 解压 → [crx2rnx](./crx2rnx.md)。

## 1. 用途与边界

**做：**

- 库 `NtripClient`：`list_mounts` → 结构化 `ServerInfo`/`MountInfo`；`mount` / `mount_with_sink` → `Stream` 收 `(rtcm_rs::Message, Vec<u8>)`
- 示例 CLI `simple-cli`：`list` / `find-nearest` / `subscribe`
- 预置 caster 别名：`rtk2go` / `centipede` / `linz` / `posau`；或 `ntrip://host:port` / `http(s)://…`
- TLS（`use_tls` / 端口 443 / `posau`）；NTRIP/2.0 头；Basic 鉴权
- `ServerInfo::find_nearest`（硬上限 **100 km**）

**不做：**

- **不是** crates.io 一装即得的 `ntrip-client` 可执行文件名（`[[bin]]` 无；CLI 是 **example**，装完叫 **`simple-cli`**）
- **不是** 上传端 / 自建 caster → [bkg-ntripcaster](./bkg-ntripcaster.md) / [ntripstreams](./ntripstreams.md) `-s`
- **不是** 多协议混流 CLI（NMEA/UBX/SPARTN）→ [pygnssutils](./pygnssutils.md)
- **不是** 多流 GUI / 运维录盘 → [bnc](./bnc.md)
- **不是** 完整 RTCM 生态百科（解帧靠 `rtcm-rs`；深度字段/自写帧 → [pyrtcm](./pyrtcm.md)）
- **不是** 定位 / TEC / PPP → 落盘后走 [rtklib](./rtklib.md) / [georinex](./georinex.md)

一句话：nav-solutions **`ntrip-client` = Rust/tokio 差分拉流积木**；电离层产品仍在「流落盘 → RINEX/改正」之后。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `simple-cli` | Rust example，clap 子命令 | `simple-cli -h` → `NTRIP command line tool`；必填 `--ntrip-user` |
| [ntripstreams](./ntripstreams.md) | Python asyncio CLI | `ntripstreams -h`；URL 位置参；可 `-s` 上传 |
| [pygnssutils](./pygnssutils.md) | `gnssntripclient` 等 | 多协议；semuconsulting 栈 |
| BKG `ntripclient`（POSIX） | 官方 C CLI | 见 `PROJECTS.json` → `ntripclient`（非本文） |

| 术语 | 含义 |
| --- | --- |
| `NtripConfig` | host/port/`use_tls`；可 `FromStr` |
| `RtcmProvider` | `rtk2go`/`centipede`/`linz`/`posau` |
| `MountInfo` | 解析 `STR;`：name/details/protocol/messages/location… |
| `find_nearest` | 球面距离；**>100 km 当无** |
| User-Agent | `NTRIP ntrip-client/0.2.1` |

## 2. 安装

```bash
# rustup（MSRV 1.82；本机 1.98.1）
. "$HOME/.cargo/env"
rustc --version

# 推荐：clone + 装 example 为 ~/.cargo/bin/simple-cli
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 --branch v0.2.1 https://github.com/nav-solutions/ntrip-client.git
cd ntrip-client
cargo install --path . --example simple-cli
which simple-cli
simple-cli -h

# 仅库（无同名可执行文件）
# cargo add ntrip-client   # 或 Cargo.toml 钉 0.2.1
```

**本机 `simple-cli -h`（2026-09-24 EDT）：**

```text
NTRIP command line tool

Usage: simple-cli [OPTIONS] --ntrip-user <USER> <NTRIP_HOST> <COMMAND>

Commands:
  list          List mount points on an NTRIP server
  find-nearest  Find the nearest mount point to a specified location
  subscribe     Subscribe to a specified mount point and print received RTCM messages
  help          Print this message or the help of the given subcommand(s)

Arguments:
  <NTRIP_HOST>  NTRIP server identifier or URI ("rtk2go", "linz" etc., or "[ntrip|http|https]://host:port")

Options:
      --ntrip-user <USER>      Username for the NTRIP service [env: NTRIP_USER=]
      --ntrip-pass <PASS>      Password for the NTRIP service [env: NTRIP_PASS=] [default: ""]
      --log-level <LOG_LEVEL>  Set log level [default: info]
  -h, --help                   Print help
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `cargo install ntrip-client` 后无 `ntrip-client` 命令 | 包只有 lib + example | `cargo install --path . --example simple-cli` 或 `cargo run --example simple-cli -- …` |
| 缺 `--ntrip-user` → clap 报错 exit **2** | 用户名无默认值（list 也要） | `--ntrip-user anonymous` 或 `export NTRIP_USER=…` |
| `package … requires rustc 1.82` | 旧 toolchain | rustup stable |

Release 页无预编译 asset 时以源码/`cargo` 为准。

## 3. 端到端（本机 0.2.1 真跑；2026-09-24 05:13 EDT）

本机**无 rtk2go/igs-ip 订户口令**；下列含 **公开 list** + **centipede 公开口令订流** + **鉴权失败样例**。挂载点数随 caster 变，勿当金样。

### 3.1 CLI：`list` 公开 sourcetable

```bash
export NTRIP_USER=anonymous   # list 仍强制要用户名；口令可空
simple-cli rtk2go list | tee /tmp/ntrip_rtk2go.txt | head -5
# 计数勿用 head 截断管道（见坑）；整表落盘：
simple-cli --ntrip-user anonymous rtk2go list > /tmp/ntrip_rtk2go.txt
grep -c ' INFO simple_cli: .* - ' /tmp/ntrip_rtk2go.txt

simple-cli --ntrip-user anonymous 'ntrip://igs-ip.net:2101' list > /tmp/ntrip_igsip.txt
grep -c ' INFO simple_cli: .* - ' /tmp/ntrip_igsip.txt

simple-cli --ntrip-user centipede --ntrip-pass password centipede list > /tmp/ntrip_cent.txt
grep -c ' INFO simple_cli: .* - ' /tmp/ntrip_cent.txt
```

**本机 stdout（摘录）：**

```text
 INFO simple_cli: Start NTRIP/RTMP tool
 INFO simple_cli: Listing NTRIP mounts
 INFO simple_cli: aamakinen - Evijarvi (63.360, 23.360)
 INFO simple_cli: AgPartner_2 - Bendorzyn (52.700, 19.570)
…
 INFO simple_cli: ABMF00GLP0 - Les-Abymes (16.260, -61.530)
 INFO simple_cli: ABPO00MDG0 - Antananarivo (-19.020, 47.230)
…
```

| caster | 本机挂载数（2026-09-24） |
| --- | --- |
| `rtk2go` | **766**（与 [ntripstreams](./ntripstreams.md) STR≈765 同量级） |
| `ntrip://igs-ip.net:2101` | **384**（对齐 ntripstreams STR**384**） |
| `centipede` | **1270** |

### 3.2 CLI：`find-nearest`

```bash
# 负经度必须 -- 分隔，否则 clap 当旗标
simple-cli --ntrip-user anonymous rtk2go find-nearest 63.36 23.36
simple-cli --ntrip-user anonymous rtk2go find-nearest -- 40.71 -74.00
simple-cli --ntrip-user anonymous rtk2go find-nearest 48.85 2.35
simple-cli --ntrip-user centipede --ntrip-pass password centipede find-nearest 45.76 4.84
```

**本机：**

```text
 INFO simple_cli: Finding nearest NTRIP mount to (63.36, 23.36)
 INFO simple_cli: Nearest mount: aamakinen - Evijarvi (63.360, 23.360), 0.000 km away

 INFO simple_cli: Finding nearest NTRIP mount to (40.71, -74)
 INFO simple_cli: Nearest mount: VIAM_BASE2 - Queens (40.740, -73.950), 5.380 km away

 INFO simple_cli: Finding nearest NTRIP mount to (48.85, 2.35)
 INFO simple_cli: No mounts found

 INFO simple_cli: Finding nearest NTRIP mount to (45.76, 4.84)
 INFO simple_cli: Nearest mount: BEFF - Villeurbanne (45.767, 4.880), 3.207 km away
```

巴黎附近 rtk2go「无结果」= **100 km 硬阈值**内无挂载，不是网络失败。

### 3.3 CLI：`subscribe`（短时）

```bash
# centipede 文档式公开口令（本机通）
timeout 8 simple-cli --ntrip-user centipede --ntrip-pass password \
  --log-level info centipede subscribe VALDM
# 期望：多行 Received RTCM message: (Msg…. Debug 极长，可 | head 或重定向后统计

# 无订户 / 假口令 / igs 匿名（本机失败样例）
timeout 12 simple-cli --ntrip-user anonymous --log-level debug rtk2go subscribe aamakinen
timeout 12 simple-cli --ntrip-user 'test@example.com' --ntrip-pass x rtk2go subscribe aamakinen
timeout 12 simple-cli --ntrip-user anonymous --log-level debug \
  'ntrip://igs-ip.net:2101' subscribe ABMF00GLP0
```

**本机要点：**

| 场景 | 结果 |
| --- | --- |
| centipede `VALDM`，8 s | **86** 行 `Received RTCM`；类型含 Msg**1004**/1012/**1077**/1087/1097/1127、**1046**/1020、1005…；偶发 `Trimming buffer` / `RTCM parse error: … incomplete` |
| rtk2go `aamakinen` + `anonymous` | `NTRIP server returned empty response` → `Error: Response error` |
| rtk2go + 假邮箱口令 | `HTTP/1.1 403 Forbidden` → `Response error` |
| igs-ip `ABMF00GLP0` 匿名 | `HTTP/1.1 401 Unauthorized` → `Response error` |

**本机 RTCM 行前缀（极长 Debug 已截断）：**

```text
 INFO simple_cli: Received RTCM message: (Msg1004(Msg1004T { reference_station_id: 0, gps_epoch_time_ms: 378803000, sync…
```

（`Debug` 单行可达数千字符；脚本统计请用 `grep -c 'Received RTCM'` / 抽 `Msg####`，勿整页粘贴进日志仓。）

### 3.4 库：`list_mounts`（本机 demo）

```rust
// Cargo.toml: ntrip-client = "0.2.1" ; tokio = { version = "1", features = ["full"] }
use ntrip_client::{NtripClient, NtripConfig, NtripCredentials, RtcmProvider};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let mut c = NtripClient::new(
        NtripConfig::from_provider(RtcmProvider::Rtk2Go),
        NtripCredentials::default().with_username("anonymous"),
    ).await?;
    let info = c.list_mounts().await?;
    println!("rtk2go mounts {}", info.services.len());

    let mut c2 = NtripClient::new(
        "ntrip://igs-ip.net:2101".parse()?,
        NtripCredentials::default().with_username("anonymous"),
    ).await?;
    println!("igs-ip mounts {}", c2.list_mounts().await?.services.len());
    Ok(())
}
```

**本机 stdout：**

```text
provider_host rtk2go.com mounts 766
aamakinen details=Evijarvi lat=63.360 lon=23.360
igs-ip mounts 384
```

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `simple-cli … list` | HTTP(S) GET `/` → 解析 `STR;` 打印 name/details/lat/lon |
| `… find-nearest <lat> <lon>` | list 后最近挂载（≤100 km） |
| `… subscribe <mount>` | TCP(+TLS) GET `/mount` → 流式 `rtcm-rs` 解帧打日志 |
| `--ntrip-user` / `NTRIP_USER` | **必填**（含仅 list） |
| `--ntrip-pass` / `NTRIP_PASS` | 默认空；有用户则发 Basic |
| `--log-level` | 默认 `info`；订流排障用 `debug` |
| `NtripClient::list_mounts` | → `ServerInfo` |
| `NtripClient::mount` | → `NtripHandle`（`Stream`） |
| `NtripConfig::from_provider` / `FromStr` | 别名或 URI |

| `STR;` → `MountInfo`（节选） | 含义 |
| --- | --- |
| `name` / `details` | 挂载名 / 站名描述 |
| `protocol` | RTCM 3.x / RAW / CMRx…（未识别 → `Unknown`） |
| `location` | 纬经；`(0.000, 0.000)` 可能未填 |

**与 [ntripstreams](./ntripstreams.md) / [pygnssutils](./pygnssutils.md) 差异（选型关键）：**

| 维度 | ntrip-client（本文） | ntripstreams | pygnssutils |
| --- | --- | --- | --- |
| 语言 | Rust / tokio | Python asyncio | Python |
| CLI | example `simple-cli` | `ntripstreams` | `gnssntripclient` 等 |
| sourcetable | 结构化 + 近邻 | 原文行 / 轻 API | 有 |
| 订流解码 | 内置 `rtcm-rs` | 部分 `Rtcm3` | 全家桶+落盘 |
| 上传/caster | 无 | `-s` 上传 | 小 caster |
| 预置别名 | rtk2go/centipede/linz/posau | 无（纯 URL） | 配置式 |

## 5. 接到哪步

```text
公开 / 实验室 caster
  → simple-cli list / find-nearest
  → subscribe 或 NtripClient::mount（RTCM 帧）
  →（可选）旁路 pyrtcm 深字段 / 录盘
  → georinex / rtklib / pytecgg
运维多流：bnc；自建：bkg-ntripcaster
脚本 asyncio：ntripstreams；多协议：pygnssutils
CRX 归档：同生态 crx2rnx
```

路径 C：[pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md) / **ntrip-client（本文）** / [bnc](./bnc.md) →（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ [rtklib](./rtklib.md)。

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `cargo install ntrip-client` 找不到命令 | 无 `[[bin]]` | `--example simple-cli` 或 `cargo run --example` |
| 2 | 缺 `--ntrip-user` exit 2 | clap 必填 | 即使只 list 也要传；可用 env |
| 3 | `find-nearest … -74` 报 unexpected argument | 负经度被当旗标 | `find-nearest -- 40.71 -74.00` |
| 4 | Paris 等 `No mounts found` | **100 km** 内无点 | 换 caster（如 centipede）或放宽自写距离逻辑 |
| 5 | rtk2go 订流 `empty response` / `403` | 需合法订户（常邮箱用户名） | 配真实 `NTRIP_USER`/`PASS`；list 仍可匿名 |
| 6 | igs-ip 订流 `401` | 挂载要账号 | 申请 IGS-IP 或换公开网 |
| 7 | `Received RTCM` 单行数 KB | `{:?}` Debug 整枚消息 | 统计用 `grep -c`；生产用库 API 取枚举而非打满日志 |
| 8 | 订流初段 `Trimming buffer` / incomplete | 流对齐 / 半帧 | 短时 WARN 可忽略；持续失败查鉴权与挂载名 |
| 9 | 期望上传或自建 caster | 本库**只做客户** | [ntripstreams](./ntripstreams.md) `-s` / [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 10 | 与 ntripstreams 旗标混用 | 两套 CLI | 见 §4 对照表 |
| 11 | `posau` / `https` 失败 | TLS/证书/网络 | 确认 `use_tls`；公司网拦 443/2101 |
| 12 | 口令进 git / 手册 | 环境未隔离 | 只用 env；示例占位符 |
| 13 | `| head` 后 Broken pipe | 日志打满被关管道 | list 先重定向再 `head`/`wc` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust/tokio 嵌差分拉流 + 结构化挂载表 | **ntrip-client（本文）** |
| Python asyncio 握手 / 轻 RTCM / 可上传 | [ntripstreams](./ntripstreams.md) |
| 多协议 CLI 录流 / 小 caster | [pygnssutils](./pygnssutils.md) |
| 生产多用户 caster | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 多流 GUI 运维录盘 | [bnc](./bnc.md) |
| RTCM3 深字段（Python） | [pyrtcm](./pyrtcm.md) |
| 同生态 Rust CRX→RNX | [crx2rnx](./crx2rnx.md) |
| RTK / PPP | [rtklib](./rtklib.md) |

## 8. 相关

[ntripstreams](./ntripstreams.md) · [pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [bnc](./bnc.md) · [crx2rnx](./crx2rnx.md) · [pyrtcm](./pyrtcm.md) · [rtklib](./rtklib.md) · [data-access 实时](../data-access.md#实时-rtcm--ssr--ntrip) · [README](./README.md)
