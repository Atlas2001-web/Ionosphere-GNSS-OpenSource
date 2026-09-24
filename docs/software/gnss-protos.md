# gnss-protos · GPS/QZSS 广播帧编解码库操作手册

目录：[`PROJECTS.json` → `gnss-protos`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/gnss-protos> · crates.io **`gnss-protos` 0.0.2** · tip **`6bfdf6b`**（仓内 `Cargo.toml` **0.1.0-beta**；无 git tag）· **MPL-2.0** · ★**4** · **无 [[bin]]**（纯库）· 本机验证 **rustc 1.98.1**（2026-09-24 06:42 EDT）：`cargo test --features gps --lib` → **53 passed / 13 failed**；`data/GPS/eph{1,2,3}.bin` 各 **128** 帧；`burst.bin` **384** 帧；`encode_raw`→`decode` 往返 **msg/week/iodc** 对齐

> 岗位：nav-solutions **GPS（+QZSS）LNAV 子帧 1–3（星历）比特流编解码** Rust 库。冲突时：**上游 README / docs.rs / 本机 `cargo doc -p gnss-protos` > 本文**。  
> RINEX 文件库 → [rinex](./rinex.md) / [rinex-cli](./rinex-cli.md)；UBX→RINEX → [ubx2rinex](./ubx2rinex.md)；UBX 帧 → [pyubx2](./pyubx2.md)；Galileo HAS 页 → [haslib](./haslib.md)；实时演示（若提及）→ <https://github.com/nav-solutions/rt-navi>（本目录无专页）。

## 1. 用途与边界

**做：**

- `GpsQzssDecoder`：在**未字节对齐**的比特流里找前导 `0x8B`，返回**已处理比特数** + 可选 `GpsQzssFrame`
- `GpsQzssFrame::encode_raw`：星历子帧 → **38** 字节缓冲（300 bit + 4 bit 填充）
- 当前解锁：**Ephemeris1 / 2 / 3**（`gps` feature；tip 默认开启；crates.io **0.0.2** 默认**空**，须 `--features gps`）
- 可选 `with_parity_verification()` 验字校验；默认不验

**不做：**

- **不是** RINEX/CRX/SP3 文件读写 → [rinex](./rinex.md) / [rinex-cli](./rinex-cli.md) / [georinex](./georinex.md)
- **不是** 定位/PPP/导航滤波器 → [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md) / rt-navi
- **不是** UBX/RTCM/SPARTN/HAS 电文 → [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pyspartn](./pyspartn.md) / [haslib](./haslib.md)
- **不是** CLI：`Cargo.toml` **无 `[[bin]]`**；无 `gnss-protos` 命令
- tip **尚未** 解锁 Almanac / 帧 4–5 健康页（README 写明后续）

一句话：`gnss-protos` = **广播导航帧 ↔ 结构体**；电离层/定位仍在「星历进解算或落盘成 RINEX NAV」之后。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `gnss-protos` | Rust 纯库 | `cargo add gnss-protos --features gps`；无同名 bin |
| [rinex](./rinex.md) | RINEX 文件库 | 读 `.rnx`/`.crx`；不吃 300-bit 帧 |
| [rinex-cli](./rinex-cli.md) | RINEX QC CLI | `rinex-cli -V` |
| [ubx2rinex](./ubx2rinex.md) | UBX→RINEX CLI | 要 `RXM-RAWX` |
| [pyubx2](./pyubx2.md) | UBX 编解码 | Python；无 console script |

| 术语 | 含义 |
| --- | --- |
| `GPS_FRAME_BITS` | **300**（10×30-bit word） |
| `GPS_FRAME_BYTES` | **38**（300/8+1；末字节 4 bit 填充） |
| `GPS_PREAMBLE_BYTE` | **0x8B** |
| `processed` | `decode` 返回的**比特**数（不是字节） |
| lazy 推进 | README：`ptr += processed/8 - 1`（半字节重叠） |

## 2. 安装

```bash
. "$HOME/.cargo/env"
rustc --version   # 本机：1.98.1

# crates.io 0.0.2（default 无 gps）
cargo new --bin gp_demo && cd gp_demo
cargo add gnss-protos@0.0.2 --features gps
# 或 tip（default=["gps"]）：
# mkdir -p ~/iono_ops && cd ~/iono_ops
# git clone https://github.com/nav-solutions/gnss-protos.git
# cd gnss-protos && git log -1 --oneline   # 6bfdf6b
# # data/ 子模常是 git@ → 改 HTTPS：
# git submodule set-url data https://github.com/nav-solutions/data.git
# git submodule update --init --depth 1 data
# ls data/GPS/{eph1,eph2,eph3,burst}.bin
# cargo test --features gps --lib
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `GpsQzssDecoder` 找不到 | 未开 `gps` | crates：`--features gps`；tip：默认已开 |
| `data/GPS` 空 / SSH 失败 | submodule `git@` | HTTPS clone `nav-solutions/data` |
| 期望有 CLI | 纯库 | 自写 `examples/`/`src/main.rs` |
| `cargo test --lib` 13 fail | 缺 IQ 样例 / 浮点往返 / delayed | 以样例 bin 解码 + 下文真 I/O 为准 |

## 3. 端到端（本机 tip `6bfdf6b` 真跑；2026-09-24 06:42 EDT）

样例：子模 `data/GPS/`（eph1/2/3 各 **4864** B；burst **14592** B）。无接收机。

### 3.1 常量与 `encode_raw` → `decode`

```rust
use gnss_protos::{
    GpsQzssDecoder, GpsQzssFrame, GpsQzssFrameId, GpsQzssHow, GpsQzssSubframe,
    GpsQzssTelemetry, GpsQzssFrame1, GPS_FRAME_BITS, GPS_FRAME_BYTES, GPS_PREAMBLE_BYTE,
};

assert_eq!(GPS_FRAME_BITS, 300);
assert_eq!(GPS_FRAME_BYTES, 38);
assert_eq!(GPS_PREAMBLE_BYTE, 0x8B);

let frame = GpsQzssFrame::default()
    .with_telemetry(
        GpsQzssTelemetry::default()
            .with_message(0x1234)
            .with_integrity()
            .with_reserved_bit(),
    )
    .with_hand_over_word(
        GpsQzssHow::default()
            .with_tow_seconds(15_000)
            .with_frame_id(GpsQzssFrameId::Ephemeris1)
            .with_alert_bit()
            .with_anti_spoofing(),
    )
    .with_subframe(GpsQzssSubframe::Ephemeris1(
        GpsQzssFrame1::default()
            .with_week(0x123)   // 291
            .with_iodc(1),
    ));
let raw = frame.encode_raw();
assert_eq!(raw.len(), 38);
assert_eq!(raw[0], 0x8B);
let (bits, out) = GpsQzssDecoder::default().decode(&raw, raw.len());
assert_eq!(bits, 300);
let out = out.expect("decoded");
assert_eq!(out.telemetry.message, 0x1234);
assert_eq!(out.subframe.as_eph1().unwrap().week, 291);
assert_eq!(out.subframe.as_eph1().unwrap().iodc, 1);
```

**本机（另一组构造 EPH1，msg=4660/week=202/iodc=18）：** `encode_raw_len=38`；`first8=[8b, 48, d3, 4d, 21, 51, 92, 03]`；`processed_bits=300`；**msg_match=true / week_match=true / iodc_match=true**（`tow`/`af0` 量化后可不对齐）。上文 `week=291/iodc=1` 样例同路径：`raw[0]=0x8B`、`len=38`、`processed_bits=300`、msg/week/iodc 对齐。  
注意：手填 `tow`/`af0`/`af1`/`tgd` 经量化后可能与输入不完全相等（tip `ephemeris2/3_reciprocal` 亦因浮点失败）；**以 model/样例 bin 字段为准**，勿臆造全字段 bit-exact。

### 3.2 解码 `eph1.bin` / `eph2.bin` / `eph3.bin`

```rust
use std::{fs::File, io::Read};
use gnss_protos::{GpsQzssDecoder, GPS_FRAME_BYTES};

fn decode_file(path: &str) -> usize {
    let mut buf = Vec::new();
    File::open(path).unwrap().read_to_end(&mut buf).unwrap();
    let mut dec = GpsQzssDecoder::default();
    let (mut ptr, mut n, mut size) = (0usize, 0usize, buf.len());
    while size > GPS_FRAME_BYTES - 2 && n < 512 {
        let (processed, frame) = dec.decode(&buf[ptr..], size);
        if let Some(f) = frame {
            n += 1;
            if n <= 2 {
                println!("#{n} bits={processed} msg={} id={:?}",
                    f.telemetry.message, f.how.frame_id);
            }
            let adv = processed / 8 - 1; // lazy
            ptr += adv; size -= adv;
        } else {
            let adv = processed / 8;
            if adv == 0 { break; }
            ptr += adv; size = size.saturating_sub(adv);
        }
    }
    println!("{path}: frames={n} bytes={}", buf.len());
    n
}
```

**本机 stdout（节选；2026-09-24 06:42 EDT）：**

```text
=== data/GPS/eph1.bin bytes=4864 GPS_FRAME_BITS=300 GPS_FRAME_BYTES=38 preamble=0x8B ===
#1 processed_bits=300 tlm.msg=4660 integrity=true | how.tow=15000 id=Ephemeris1
   EPH1 week=291 iodc=1 ura=2 health=0 toc=0s
#2 processed_bits=316 tlm.msg=4661 | how.tow=15000 id=Ephemeris1 week=292 iodc=2
… #128 msg=4787 week=418 iodc=128
decoded_frames=128

=== data/GPS/eph2.bin ===
#1 bits=300 msg=4660 id=Ephemeris2
   EPH2 iode=1 toe=54320s e≈0.099999999977 sqrt_a=5353.000000000 m0≈0.100000000093 fit=true aodo=18
decoded_frames=128

=== data/GPS/eph3.bin ===
#1 bits=300 msg=4660 id=Ephemeris3
   EPH3 iode=18 cic≈1.000240e-6 cis≈2.000481e-6 crc=122 i0≈0.000999987125
decoded_frames=128
```

首帧 `processed_bits=**300**`；后续懒推进常见 **316**（=300+16）。`msg=4660`(=`0x1234`) 起递增。

### 3.3 `burst.bin`（EPH1→2→3 交错）

```text
=== data/GPS/burst.bin bytes=14592 ===
#1 Ephemeris1 week=291 iodc=1 ura=2
#2 Ephemeris2 iode=1 toe=54320
#3 Ephemeris3 iode=18 crc=122
#4 Ephemeris1 week=292 …
decoded_frames=384   # 128×3
```

### 3.4 `cargo test`（诚实）

```bash
cd ~/iono_ops/gnss-protos
cargo test --features gps --lib
# 本机：53 passed; 13 failed
# 失败类：缺 IQ 文件（l1_iq4mega/i12mega/i24mega/gpssim）、
#         eph1_bin_delayed / eph2_bin / eph3_bin 断言、
#         ephemeris2/3 raw+reciprocal 浮点、preamble_search、zeros_padder
```

**通过且足以支撑手册：** `eph1_bin`、`ephemeris1_raw`、`ephemeris1_reciprocal`、字/TLM/HOW 单测等。缺文件失败**不**臆造 IQ 解码 stdout。

## 4. I/O 与关键 API

| API | 作用 |
| --- | --- |
| `GpsQzssDecoder::default()` | 不验 parity |
| `.with_parity_verification()` | 坏 parity → 丢弃帧 |
| `decode(&[u8], size) -> (usize, Option<GpsQzssFrame>)` | **比特**进度 + 帧 |
| `GpsQzssFrame::encode_raw() -> [u8; 38]` | 含前导；末字节填 0 |
| `encode()` / `encode_to_buffer` | word 级 / 写入缓冲 |
| `subframe.as_eph1/2/3()` | 解包星历 |

| 字段（本机样例 #1） | 值 |
| --- | --- |
| `telemetry.message` | **4660** |
| `how.tow` / `frame_id` | **15000** / `Ephemeris1..3` |
| EPH1 `week` / `iodc` / `ura` | **291** / **1** / **2** |
| EPH2 `iode` / `toe` / `sqrt_a` | **1** / **54320** / **5353** |
| EPH3 `iode` / `crc` | **18** / **122** |

输入：任意比特对齐的 LNAV 缓冲（接收机 SFRB/基带、或仓内 bin）。输出：结构体；**不**写 RINEX。

## 5. 接到哪步

```text
基带 / u-blox SFRBX / 自制 300-bit 流
  → gnss-protos 解 EPH1–3
  →（可选）组装广播星历 → 自写 NAV 或喂解算器
  → 文件场景仍用 rinex / georinex / ubx2rinex
  → TEC/PPP：georinex / pytecgg / rtklib / cssrlib
```

交叉：[rinex](./rinex.md) · [rinex-cli](./rinex-cli.md) · [ubx2rinex](./ubx2rinex.md) · [pyubx2](./pyubx2.md) · [haslib](./haslib.md) · [pyspartn](./pyspartn.md) · [pyrtcm](./pyrtcm.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 找不到 `GpsQzssDecoder` | 未启用 `gps` | `cargo add gnss-protos --features gps` |
| 2 | `decode` 一直 `None` | 无前导 / 缓冲短于 38 B | 确认 `0x8B`；`size≥38` |
| 3 | 同一帧解两次 | 按**字节**推进 | 用返回的**比特**：`adv=processed/8-1` |
| 4 | parity 全丢 | 开了校验但流未贴 parity | 调试先 `default()`；发送侧写对 parity |
| 5 | 手写 `af0`/`tow` 往返不等 | 量化/HOW 编码 | 用 `model` 或样例 bin；勿强断言全 f64 |
| 6 | `cargo test` IQ 失败 | 子模无 `iq-*.bin` | 忽略或自备；以 eph/burst 为准 |
| 7 | 当定位引擎用 | 库只编解码 | 接 rtklib/cssrlib/rt-navi |
| 8 | 当 RINEX 库用 | 协议层≠文件层 | [rinex](./rinex.md)/[georinex](./georinex.md) |
| 9 | crates 0.0.2 ≠ tip API | 版本漂移 | 锁 rev / 读 docs.rs 对应版 |
| 10 | 找 `gnss-protos` 命令 | 无 bin | 自写 binary |
| 11 | Almanac/帧4–5 | 未实现 | 等上游；勿臆造字段 |
| 12 | 与 ubx2rinex 混用期望 | UBX 容器≠LNAV 裸帧 | SFRBX 抽 300-bit 再喂本库 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust 解/编 GPS LNAV 星历帧 | **gnss-protos（本文）** |
| RINEX 文件 QC/读写 | [rinex-cli](./rinex-cli.md) / [rinex](./rinex.md) |
| UBX 录包→RINEX | [ubx2rinex](./ubx2rinex.md) |
| UBX/RTCM/SPARTN Python | [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) / [pyspartn](./pyspartn.md) |
| Galileo HAS 页 | [haslib](./haslib.md) |
| PPP / 实时导航 | [rtklib](./rtklib.md) / [cssrlib](./cssrlib.md) / rt-navi |

相关：上游 README · docs.rs `gnss-protos` · [rinex](./rinex.md) · [ubx2rinex](./ubx2rinex.md) · [rinex-cli](./rinex-cli.md) · [pyubx2](./pyubx2.md) · [haslib](./haslib.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)
