# binex · BINEX 编解码库操作手册

目录：[`PROJECTS.json` → `binex`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/binex> · crates.io **`binex` 0.5.2** · tip tag **`v0.5.2`=`9530237`**（main 仓内已 **0.6.0**/`913e934`，**未**发 crates）· **MPL-2.0** · ★**5** · **无 [[bin]]**（纯库）· MSRV **1.85.0** / edition **2024** · 本机验证 **rustc 1.98.1**（2026-09-24 07:14 EDT；**质检复跑 07:17 EDT**：`binex` **0.5.2**；`glo3.bin` **16384** B/ok **4**/MonumentGeo×**3**+Eph/GLO×**1**/GLO clock=**6.355904042721001×10⁻⁵**/x=y=z=**10908.94238281**/slot=**0**；`ESBC1770.20N.bin` **10821632** B/ok **2642**/Geo×**3**+GLO **510**+SBAS **2129**；`[]`/`[0,0x11,0x22]`→`NoSyncByte`；`[0xe2,0x01]`→`NotEnoughBytes`；GLO encode→decode enc=**142**/clock+x 齐；MonumentGeo enc=**80**/comments=`[binex_demo]`/frames=**4**；垫页 `Decoder` 仅首帧；紧凑流 Decoder `["GEO","GLO …"]`（本机构造 **222** B，写作 **173** B——构造不同））：`cargo add binex@0.5.2`；对 [rinex2bin](./rinex2bin.md) 产物按 **4096 B** 页 `Message::decode`：`glo3.bin` MonumentGeo×**3**+Eph/GLO×**1**；`ESBC1770.20N.bin` Geo×**3**+GLO **510**+SBAS **2129**=**2642**；R01 `clock_offset_s`=**6.355904042721001×10⁻⁵**≡RINEX；自编码 GLO/MonumentGeo 往返齐；紧凑流 `Decoder` 得 GEO+GLO；空/`NoSyncByte`/`NotEnoughBytes`

> 岗位：nav-solutions **BINEX（Binary EXchange）** 开源消息的 **编解码 / 流解析** Rust 库。冲突时：**上游 README / docs.rs / 本机 `cargo doc -p binex` > 本文**。  
> RINEX→BINEX **CLI** → [rinex2bin.md](./rinex2bin.md)（锁 **`rinex` 0.17** + **`binex` 0.4.2**）；RINEX 库/CLI → [rinex.md](./rinex.md)/[rinex-cli.md](./rinex-cli.md)；共视 → [cggtts.md](./cggtts.md)/[rnx2cggtts.md](./rnx2cggtts.md)。**库 ≠ 定位/TEC；BINEX ≠ RINEX 文本。**

## 1. 用途与边界

**做：**

- `Message::decode` / `encode`：缓冲上的单帧开源 BINEX
- `Decoder::new` / `Decoder::new_gzip`：对 `Read` 连续流吐 `StreamElement::{OpenSource, ClosedSource}`
- 记录体：`Record::{MonumentGeo, EphemerisFrame, Solutions}`（GLO/SBAS/GPS/GAL/`GPSRaw` 等）
- 合成：`MonumentGeoRecord::new` / `Record::new_ephemeris_frame` + `Meta{big_endian,enhanced_crc,reversed}`

**不做：**

- **不是** 定位 / PPP / TEC → [rtklib.md](./rtklib.md)/[georinex.md](./georinex.md)/[pytecgg.md](./pytecgg.md)
- **不是** RINEX 文本读写 → [rinex.md](./rinex.md)/[rinex-cli.md](./rinex-cli.md)
- **不是** RINEX→BINEX CLI → [rinex2bin.md](./rinex2bin.md)
- **不是** CLI：无同名 bin；自写 `main`/`examples`
- 限制（上游）：**reversed** / **enhanced CRC** 未支持；little-endian 测过但缺公开数据集；长帧 MD5 未充分验证

一句话：`binex` = **BINEX 二进制帧 ↔ 结构体**；接在 rinex2bin / 接收机流之后，不是解算器。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `binex` | Rust 纯库 0.5.2 | `cargo add binex@0.5.2`；无同名命令 |
| [rinex2bin.md](./rinex2bin.md) | RINEX→BINEX CLI | `rinex2bin -V` → `0.1.0`；内锁 binex **0.4.2** |
| [rinex.md](./rinex.md) | RINEX 文本库 | 读 `.rnx`；不吃 BINEX 流 |
| [haslib.md](./haslib.md) | HAS：SBF/**BINEX**→SSR | 另一语境；HAS 页≠本文 MonumentGeo |

| 术语 | 含义 |
| --- | --- |
| SYNC | 帧头同步字节；BE+标准 CRC = **`0xE2`**（rinex2bin 默认） |
| MonumentGeo | 地标/注释帧；宣布流、软件名、头注释 |
| EphemerisFrame | NAV 体：本机 rinex2bin 产物见 **GLO** / **SBAS** |
| `Decoder` 内缓 | **4096 B**；与 rinex2bin「每消息整页写」叠加见 §3.1 |
| ClosedSource | 私有 MID；仅元数据 + 回调 `interprate` |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1（≥ MSRV 1.85）

cargo new --bin binex_demo && cd binex_demo
cargo add binex@0.5.2
# 默认 feature：flate2（gzip 流）

# tip 对照（可选；仓内已 0.6.0，日常钉 crates）
# git clone https://github.com/nav-solutions/binex && cd binex
# git checkout v0.5.2 && git log -1 --oneline   # 9530237
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| edition 2024 / MSRV | 0.5.2 要较新 toolchain | rustc ≥ **1.85** |
| `Decoder` 只吐 1 帧 | rinex2bin **4096** 尾零 + 内缓满 → `NoSyncByte`+EOS | 按页 `Message::decode`；或写紧凑流 |
| 当 CLI 用 | 纯库 | 自写小例；序列化用 [rinex2bin](./rinex2bin.md) |
| 跟 tip 0.6.0 | 未发 crates | 生产钉 **0.5.2** |

## 3. 端到端（本机 0.5.2 真跑；2026-09-24 07:14 EDT）

样例：[rinex2bin.md](./rinex2bin.md) 同源 `~/iono_ops/rinex2bin-demo/out/`（`--skip` ESBC / GLO3 / ACOR / coldstart）。

### 3.1 按页解码 `glo3.bin` / `ESBC1770.20N.bin`

rinex2bin **每消息 `write` 整 4096 B**（有效载荷后大量尾零）。`Decoder` 内缓同为 4096：读满一页、解出首帧后，剩余零字节 → `NoSyncByte` 且 `eos` → **只吐 1 条**。实务：对文件 **按 4096 B 切页** 调 `Message::decode`。

```rust
use std::fs;
use binex::prelude::*;

const PAGE: usize = 4096;

fn decode_pages(path: &str) {
    let raw = fs::read(path).unwrap();
    for (i, page) in raw.chunks(PAGE).enumerate() {
        match Message::decode(page) {
            Ok(msg) => match &msg.record {
                Record::MonumentGeo(g) => {
                    println!("p{i} GEO epoch={} comments={:?} frames={}",
                        g.epoch, g.comments,
                        g.frames.iter().map(|f| f.string.as_str()).collect::<Vec<_>>());
                }
                Record::EphemerisFrame(EphemerisFrame::GLO(g)) => {
                    println!("p{i} GLO clock={:.15e} x_km={}", g.clock_offset_s, g.x_km);
                }
                Record::EphemerisFrame(EphemerisFrame::SBAS(s)) => {
                    println!("p{i} SBAS prn={} x_km={}", s.sbas_prn, s.x_km);
                }
                other => println!("p{i} {other:?}"),
            },
            Err(e) => {
                if page.iter().any(|b| *b != 0) {
                    println!("p{i} ERR {e:?}");
                }
            }
        }
    }
}
```

**本机计数：**

| 文件 | 字节 | 页解码 ok | 类型 |
| --- | --- | --- | --- |
| `glo3.bin` | **16384** | **4** | MonumentGeo×**3** + Eph/GLO×**1**（KILL 前只刷出 1 条 GLO；rinex2bin 日志曾报 GLO×3） |
| `ESBC1770.20N.bin` | **10821632** | **2642** | Geo×**3** + GLO **510** + SBAS **2129**（rinex2bin debug 2643/SBAS 2130；末帧可能未刷满） |
| `acor2.bin` | **16384** | **4** | MonumentGeo×**4**（仅头；无观测体） |
| `cold_skip.bin` | **8192** | **2** | MonumentGeo×**2**（无 GPS EphemerisFrame） |

**glo3 首条 GLO（页 3；对照 RINEX `R01 2020 06 24 23 15 00`）：**

| 字段 | 本机 0.5.2 | 对照 |
| --- | --- | --- |
| `clock_offset_s` | **6.355904042721001×10⁻⁵** | RINEX **6.355904042721e-05** |
| `x_km` | **10908.94238281** | RINEX x **1.090894238281e+04** |
| `y_km`/`z_km` | **= x_km**（页内同一 BE double 出现 **3** 次） | RINEX y/z 不同；**生产者**（rinex2bin↔binex **0.4.2** forge）写入异常，0.4.2/0.5.2 解码一致 |
| `slot`/`day`/`tod_s` | **0** | 同上，勿当 RINEX 槽位 |

宣布串（真实）：`rtk-rs/rinex2bin v0.1.0 from V3 MIXED NAVIGATION DATA`；`meta=RNX2BIN`；SYNC **`0xE2`**。

### 3.2 `Decoder`：4096 垫页 vs 紧凑流

```rust
use std::fs::File;
use binex::prelude::*;

// 垫页文件：通常只得首帧
let mut d = Decoder::new(File::open("data/glo3.bin")?);
assert!(matches!(d.next(), Some(Ok(StreamElement::OpenSource(_))));
assert!(d.next().is_none()); // 本机：openish_count=1 后 EOS

// 自编码紧凑拼接：Decoder 正常连读
```

**本机紧凑流：** MonumentGeo + GLO（`slot=1`, `clock=6.355904042721001e-5`）→ `Decoder` 得 **`["GEO", "GLO …"]`**；总长 **173 B**。

### 3.3 encode 往返

```rust
use binex::prelude::*;

// 从 glo3 页解出的 GLO 再 encode→decode
// 本机：enc=142；clock_match=true；x_match=true

let geo = MonumentGeoRecord::new(
    Epoch::from_gpst_seconds(60.0),
    MonumentGeoMetadata::RNX2BIN,
    "Fancy GNSS receiver",
    "Magnificent antenna",
    "SITE34",
    "SITE34",
).with_comment("binex_demo");
let msg = Message::new(
    Meta { reversed: false, enhanced_crc: false, big_endian: true },
    Record::new_monument_geo(geo),
);
let need = msg.encoding_size();
let mut buf = vec![0u8; need];
let n = msg.encode(&mut buf, need)?;
let back = Message::decode(&buf[..n])?;
// 本机：enc=80；comments=["binex_demo"]；n_frames=4；be=true
```

### 3.4 失败边界（如实）

| 输入 | 本机 |
| --- | --- |
| `[]` | `Err(NoSyncByte)` |
| `[0x00,0x11,0x22]` | `Err(NoSyncByte)` |
| `[0xe2, 0x01]`（截断） | `Err(NotEnoughBytes)` |
| rinex2bin 垫页 + `Decoder` | 仅首帧后 `None`（见 §3.1） |

## 4. 输入 / 输出

| API | 作用 |
| --- | --- |
| `Message::decode(&[u8])` | 单帧；缓冲须含 SYNC |
| `Message::encode(&mut [u8], size)` | 返回写入长度；先 `encoding_size()` |
| `Decoder::new(R)` / `new_gzip` | 流式 `Iterator<Item=Result<StreamElement>>` |
| `Record::as_monument_geo` / `as_ephemeris` | 解包 |

| 输入 | 说明 |
| --- | --- |
| `.bin` / 套接字字节 | 开源 BINEX；gzip 走 `new_gzip` 或外层 `GzDecoder` |
| rinex2bin 产物 | 可用；**优先按页 decode** |

| 输出 | 说明 |
| --- | --- |
| `MonumentGeoRecord` | `epoch` / `meta` / `comments` / `frames[].string` |
| `GLOEphemeris` 等 | `clock_offset_s`、`x_km`…（单位：秒、km） |
| `ClosedSourceElement` | 私有 MID；仅元数据 |

## 5. 接到哪一步

```text
RINEX NAV --rinex2bin--> .bin（4096 垫页）
                         └─ 本文按页 Message::decode → MonumentGeo / Eph
紧凑 BINEX 流 / 接收机固件
                         └─ Decoder::new → StreamElement
需要共视 / TEC / 定位 → cggtts / gnss-tec / rtklib（本库不替代）
RINEX 文本 QC → rinex-cli / georinex（BINEX≠RINEX）
```

| 上游 | 本库 | 下游 |
| --- | --- | --- |
| [rinex2bin.md](./rinex2bin.md) `.bin` | 解码 / 再编码 | 自研消费、归档 |
| 接收机 BINEX 口 | `Decoder` | 实时应用（本仓无专用消费手册） |
| [rinex.md](./rinex.md) | **无直接接口**（文本≠二进制） | 先 rinex2bin 再进本文 |

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `Decoder` 只出 1 帧 | 4096 垫页 + 内缓 | 按页 `Message::decode`；或紧凑写出 |
| 2 | `.bin` ≫ 有效载荷 | rinex2bin 整页写 | 勿当压缩比；按 `encoding_size` 截断自编码 |
| 3 | GLO y/z = x；slot=0 | 生产者 forge 写入 | 信 `clock_offset_s`/x；对照 RINEX；勿臆造全字段 |
| 4 | ESBC 计数少 1 | KILL 未刷末帧 | 与 rinex2bin 手册一致；以落盘页数为准 |
| 5 | `EnhancedCrc`/`ReversedStream` | 库限制 | 勿开 `-c`/`-r` 若要本库解 |
| 6 | 当定位库 | 误解岗位 | 只做帧 I/O |
| 7 | 与 binex **0.4.2** 混锁 | rinex2bin 钉旧版 | 消费端可用 0.5.2；API 以本机为准 |
| 8 | tip **0.6.0** ≠ crates | 未发布 | 手册钉 **0.5.2** |
| 9 | OBS `.bin` 无观测体 | rinex2bin OBS WIP | 只见 MonumentGeo |
| 10 | GPS NAV 无 Eph | rinex2bin `forge_gps` 失败 | 同 cold_skip；勿臆造 GPS 帧 |
| 11 | `ClosedSource` | 私有 MID | 用 `Provider`/mid 自解 |
| 12 | 测完残留 | 临时 crate | `rm -rf` demo；无常驻进程 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| BINEX 编解码纯库 | **本文 `binex` 0.5.2** |
| RINEX→BINEX CLI | [rinex2bin.md](./rinex2bin.md) |
| RINEX 文本库/QC | [rinex.md](./rinex.md)/[rinex-cli.md](./rinex-cli.md) |
| CGGTTS 2E | [cggtts.md](./cggtts.md)/[rnx2cggtts.md](./rnx2cggtts.md) |
| SP3 轨道库 | 待写 `sp3`（同生态；本车道下一优先） |

## 8. 相关

[rinex2bin.md](./rinex2bin.md) · [rinex.md](./rinex.md) · [rinex-cli.md](./rinex-cli.md) · [cggtts.md](./cggtts.md) · [rnx2cggtts.md](./rnx2cggtts.md) · [gnss-protos.md](./gnss-protos.md) · [haslib.md](./haslib.md) · [ubx2rinex.md](./ubx2rinex.md) · [georinex.md](./georinex.md) · [README.md](./README.md)
