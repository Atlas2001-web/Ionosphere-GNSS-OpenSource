# rtcm-rs · RTCM 3 编解码 Rust 库操作手册

目录：[`PROJECTS.json` → `rtcm-rs`](../../PROJECTS.json) · 上游 <https://github.com/martinhakansson/rtcm-rs> · crates.io **`rtcm-rs` 0.11.0**（2024-04-28 发布，下载 **52897**）· tag **`v0.11.0`=`d4d0269`**；master tip **`f08941b`**（2024-10-29，**未发 crates**，修「空 MSM」）· **MIT OR Apache-2.0** · ★**33** · 纯库（无 [[bin]]）· MSRV **1.66.1** / edition 2021 · `#![forbid(unsafe_code)]` · 本机 **rustc 1.98.1**（2026-09-26 01:05–01:08 EDT）：centipede `VALDM` 真流 **53271 B / 322 帧**；1005 ECEF **(4151313.6403, 380499.3117, 4811408.2782) m**；1077 首历元 **12 星 / 21 格**；G01 C1C PR **20276061.853 m**；pyrtcm **1.2.0** 逐字段对齐；**1107×35 在 0.11.0 解成 `Corrupt`**（tip 修复）；1005 编码往返 **25 B**；x=10¹² m **静默回绕**

> 岗位：**RTCM 10403.x（到 3.4）消息 ↔ Rust 结构体**。冲突时：**上游 README / docs.rs / 本机源码 > 本文**。  
> **编解码库 ≠ RTK 解算 ≠ RINEX 转换 ≠ NTRIP 客户端。** 取流 → [ntrip-client](./ntrip-client.md)/[ntripclient](./ntripclient.md)；转 RINEX → [rtcm3torinex](./rtcm3torinex.md)；Python 同类 → [pyrtcm](./pyrtcm.md)；解算 → [rtklib](./rtklib.md)。

## 1. 用途与边界

**做：**

- 帧层：`next_msg_frame(&[u8])` / `MsgFrameIter`：找 `0xD3` 前导、校 10 bit 长度 + **CRC-24Q**，跳过垃圾
- 消息层：`MessageFrame::get_message()` → `Message::Msg1005(Msg1005T{..})` 等；物理量已缩放为 **m / ms / dBHz**
- 编码：`MessageBuilder::build_message(&Message)` → 完整帧字节（含前导、长度、CRC）
- 覆盖：1001–1230 观测/星历/辅助、MSM1–7（1071–1137）、1300–1304 等，共 **108** 个 `msgXXXX` feature（每消息一个）
- `no_std`、无堆分配（`tinyvec`/定长 `DataVec`）；可选 `serde`

**不做：**

- **不**取流 / 不连 caster → [ntrip-client](./ntrip-client.md)/[ntripclient](./ntripclient.md)/[str2str](./rtklib.md)
- **不**组装观测历元、不写 RINEX → [rtcm3torinex](./rtcm3torinex.md)/`convbin`
- **不**做定位 / RTK / 周跳 → [rtklib](./rtklib.md)/[gnss-rtk](./gnss-rtk.md)
- **不**做 MSM 物理量合成：伪距要自己 `(粗整 + 粗小数 + 精) × c`（见 §3.2）
- **不**解 RTCM 2.x；厂商私有 4001–4095 无对应 feature（落 `MsgNotSupported`）

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `rtcm-rs` | Rust 纯库 0.11.0 | `cargo add rtcm-rs@0.11.0`；`use rtcm_rs::prelude::*` |
| [pyrtcm](./pyrtcm.md) | Python 同类（semuconsulting） | 字段名用 `DF025` 等标准编号；本文用语义名 |
| [rtcm3torinex](./rtcm3torinex.md) | BKG C 程序：RTCM3→RINEX | 出文件；不给 API |
| [gnss-protos](./gnss-protos.md) | GPS 导航电文比特帧 | 卫星广播电文 ≠ RTCM 差分帧 |
| [binex](./binex.md) | BINEX 编解码 | 另一种二进制交换格式 |
| [pyubx2](./pyubx2.md)/[ubx2rinex](./ubx2rinex.md) | u-blox UBX | 接收机私有协议 ≠ RTCM |

## 2. 安装与 features

```bash
. "$HOME/.cargo/env"; rustc --version   # 本机 1.98.1（≥ MSRV 1.66.1）
cargo new --bin rtcm_demo && cd rtcm_demo
cargo add rtcm-rs@0.11.0                # 默认 = all_msgs + std + test_gen
# 裁剪 + no_std（只要 1005/1077）：
# cargo add rtcm-rs@0.11.0 --no-default-features -F msg1005,msg1077
# 要 JSON：-F serde（上游另有 rtcm-json crate 示范）
```

| feature | 作用 | 本机观察 |
| --- | --- | --- |
| `all_msgs`（默认） | 打开全部 `msgXXXX` | Cargo.toml 共 **108** 个消息 feature |
| `std`（默认） | `std::error::Error` 实现 | 关掉即 `no_std` |
| `test_gen`（默认） | **仅上游生成测试用** | 默认会拖进 `rand 0.8` + `getrandom`/`libc`；裁剪版依赖树只剩 `crc-any` + `tinyvec` |
| `msgXXXX` | 单消息 | 未开的消息号 → `Message::MsgNotSupported`（VALDM：开 1005+1077 时其余 **283** 帧全落此） |
| `serde` | Serialize/Deserialize | 本篇未测 |

上游 examples（`v0.11.0` 实跑）：`decode`（单帧）、`decode_iterator`（`testdata/msgs_1.rtcm` 974 B → 1005×2/1007/1030/1074×6）、`encode`（1001 → 29 B）。`cargo build` 在 1.98.1 下有 dead_code / 生命周期省略 **warning**，无 error。

## 3. 端到端（本机真跑；2026-09-26 01:05–01:08 EDT）

### 3.1 真实输入：centipede `VALDM` 抓 35 s

```bash
timeout 35 str2str -in ntrip://centipede:centipede@caster.centipede.fr:2101/VALDM \
  -out file://./valdm.rtcm3        # 公开挂载（ntripclient 手册同源）；结束后 pgrep str2str 为空
# 53271 B，sha256 前 12 位 6e8c2b96f31f；1033 自报 "RTKBase Ublox_ZED-F9P" fw 2.3.4
```

### 3.2 解码 + 计数 + 取字段（`src/main.rs`，完整可编）

```rust
use rtcm_rs::prelude::*;
use std::collections::BTreeMap;

const C_M_PER_MS: f64 = 299_792.458; // 光速 m/ms

fn main() {
    let path = std::env::args().nth(1).expect("usage: rtcm_demo <file.rtcm3>");
    let buf = std::fs::read(&path).unwrap();
    let mut it = MsgFrameIter::new(&buf);
    let mut cnt: BTreeMap<u16, (usize, usize)> = BTreeMap::new(); // (帧数, Corrupt 数)
    let mut msm_shown = false;
    for f in &mut it {
        let n = f.message_number().unwrap_or(0);
        let msg = f.get_message();
        let e = cnt.entry(n).or_default();
        e.0 += 1;
        if matches!(msg, Message::Corrupt) { e.1 += 1; }
        match msg {
            Message::Msg1005(m) if e.0 == 1 => println!(
                "1005 sta={} ECEF=({:.4}, {:.4}, {:.4}) m gps={} glo={} gal={}",
                m.reference_station_id, m.antenna_ref_point_ecef_x_m,
                m.antenna_ref_point_ecef_y_m, m.antenna_ref_point_ecef_z_m,
                m.gps_flag, m.glonass_flag, m.galileo_flag),
            Message::Msg1006(m) => println!("1006 h_ant={} m", m.antenna_height_m),
            Message::Msg1077(m) if !msm_shown => {
                msm_shown = true;
                let d = &m.data_segment;
                println!("1077 tow_ms={} nsat={} nsig_cells={}",
                    m.gps_epoch_time_ms, d.satellite_data.len(), d.signal_data.len());
                let s = &d.satellite_data[0];
                let g = &d.signal_data[0];
                let rough = s.gnss_satellite_rough_range_integer_ms.unwrap() as f64
                    + s.gnss_satellite_rough_range_mod1ms_ms;
                let pr = (rough + g.gnss_signal_fine_pseudorange_ext_ms.unwrap()) * C_M_PER_MS;
                println!("  G{:02} {:?} cnr={:?} dBHz PR={:.3} m",
                    g.satellite_id, g.signal_id, g.gnss_signal_cnr_ext_dbhz, pr);
            }
            _ => {}
        }
    }
    println!("bytes={} consumed={}", buf.len(), it.consumed());
    for (n, (k, bad)) in &cnt {
        println!("  {n}: {k}{}", if *bad > 0 { format!(" (Corrupt {bad})") } else { String::new() });
    }
}
```

**本机打印（`cargo run --release -- ../valdm.rtcm3`，原样摘录）：**

```text
1077 tow_ms=536721000 nsat=12 nsig_cells=21
  G01 SigId(1, 'C') cnr=Some(49.0) dBHz PR=20276061.853 m
1005 sta=0 ECEF=(4151313.6403, 380499.3117, 4811408.2782) m gps=1 glo=1 gal=0
1006 h_ant=0 m
bytes=53271 consumed=53271
  1004: 35  1005: 4  1006: 1  1008: 4  1012: 35  1019: 12  1020: 17  1033: 4
  1042: 10  1046: 24  1077: 35  1087: 35  1097: 35  1107: 35 (Corrupt 35)  1127: 35  1230: 1
```

（计数行为排版合并成两行，数值未改。）合计 **322** 帧；1004/1012 传统观测与 MSM7 并发；1019/1020/1042/1046 = GPS/GLO/BDS/GAL 星历；1230 GLO 码相偏差 `SigId(2,'P')` bias **−163.84 m**（数值来源未核实，勿直接当偏差改正用）。

**pyrtcm 1.2.0 交叉（同一文件，`RTCMReader`）：** 16 类计数**完全一致**；1005 `DF025/026/027` = 4151313.6403 / 380499.3117 / 4811408.2782000005；1077 `NSat=12 NCell=21`、`DF397_01=67`、`DF398_01=0.6337890625`、`DF405_01=-0.00012680143117904663`、`DF408_01=49.0`——与 rtcm-rs 逐位相同。pyrtcm 把 1107 解成 `NSat=0 NCell=0`（空 MSM），rtcm-rs 0.11.0 却给 `Corrupt`，见 §3.5。

### 3.3 流式：套接字 / 分块读

```rust
let (used, mf) = next_msg_frame(&buf);   // used = 垃圾 + 本帧长度
let got = mf.is_some();
buf.drain(..used);                       // Incomplete 时 used 停在 0xD3 处，保留半帧
if !got { /* 读下一块再试 */ }
```

本机：文件按 **512 B** 分块喂入 → `frames=322 leftover=0 B`，与整读一致。

### 3.4 编码往返：合成 1005（**本机构造，坐标取自 VALDM 实测值**）

```rust
use rtcm_rs::msg::Msg1005T;
let m = Message::Msg1005(Msg1005T {
    reference_station_id: 2001, reserved_24_6: 0,
    gps_flag: 1, glonass_flag: 1, galileo_flag: 1, reference_station_ind: 0,
    antenna_ref_point_ecef_x_m: 4151313.6403, single_receiver_osc_ind: 1,
    reserved_73_1: 0, antenna_ref_point_ecef_y_m: 380499.3117,
    quarter_cycle_ind: 0, antenna_ref_point_ecef_z_m: 4811408.2782,
});
let bytes = MessageBuilder::new().build_message(&m).unwrap().to_vec();
let (_, f) = next_msg_frame(&bytes);
let back = f.unwrap().get_message();
```

| 项 | 本机 |
| --- | --- |
| 帧长 / 头 / CRC | **25 B** / `d3 00 13 3e d7` / `c1 96 37` |
| 解回 | sta=**2001**，x=**4151313.6403**，y=**380499.3117**，z=**4811408.2782000005**，gal=**1** |
| z 差 | **9.31×10⁻¹⁰ m**（0.1 mm 量化 + f64 表示）→ `Debug` 字符串比较为 **false**，要按容差比 |
| x = 10¹² m（超 DF025 38 bit 量程） | **`Ok(25)` 不报错**，解回 x=**−5825462.272 m**（静默回绕） |
| `Message::Empty` | `Err(EncodingNotSupported)` |

### 3.5 失败边界（本机如实）

| 输入（均由上面 25 B 合成帧改造） | `next_msg_frame` | `MsgFrameIter` |
| --- | --- | --- |
| 原帧 | used=25，得 1005 | 1 帧 |
| 末字节 CRC 翻转 | used=25，`None` | 0 帧（静默丢弃，无错误值） |
| 载荷翻 1 bit | used=25，`None` | 0 帧 |
| 截掉尾 4 B | used=**0**，`None` | 0 帧，consumed=0（等更多数据） |
| `GARBAGE\x00\x11` 前缀 + 帧 | used=34，得 1005 | 1 帧 |
| 截断帧 + 完整帧 | used=46，得 1005 | 1 帧（截断帧 CRC 不过，被跳过） |
| 假 `d3 03 ff` 前缀（宣称 1023 B）+ 完整帧 | used=**0**，`None` | **0 帧**：总长不足 1029 B 判 `Incomplete`，后面的好帧被挡住 |
| `[]` | used=0 | 0 帧 |
| `MessageFrame::new` 截断 / CRC 坏 | `Err(Incomplete)` / `Err(NotValid)` | — |
| 真流 1107（22 B 载荷、卫星掩码全 0） | 帧层 OK | 0.11.0 → **`Message::Corrupt`**；git tip `f08941b` → `Msg1107` 空 `satellite_data`/`signal_data` |

## 4. 输入 / 输出

| API | 作用 |
| --- | --- |
| `next_msg_frame(&[u8]) -> (usize, Option<MessageFrame>)` | 找下一合法帧；返回已消费字节 |
| `MsgFrameIter::new(&[u8])` + `consumed()` | 整缓冲迭代；遇 `Incomplete` 即停 |
| `MessageFrame::{message_number, crc, frame_data, data, get_message}` | 帧元数据 + 解码 |
| `MessageBuilder::build_message(&Message) -> Result<&[u8]>` | 编码；返回借用内部缓冲，需 `.to_vec()` 才能跨调用 |
| `Message::{MsgXXXX, Empty, Corrupt, MsgNotSupported}` | 结果枚举；**解码不返回 `Result`** |

| 输出单位 | 例 |
| --- | --- |
| m | `antenna_ref_point_ecef_*_m`、`l1_pseudorange_m` |
| ms | MSM 粗/精距离（`*_ms`），×299792.458 得 m |
| dBHz / m/s | `gnss_signal_cnr_ext_dbhz`、`*_phaserange_rate_m_s` |
| `Option<_>` | 标准「无效值」位图 → `None` |

## 5. 接到哪一步

```text
caster ──ntrip-client / ntripclient / str2str──> RTCM3 字节流
   └─ 本文 next_msg_frame → Message → 自研监控 / 转发过滤 / 入库（serde→JSON）
   └─ 要 RINEX → rtcm3torinex / convbin（本库不写 RINEX）
   └─ 要解算 → rtklib / gnss-rtk（本库不定位）
自研基准站 → MessageBuilder 生成 1005/1033/MSM → ntripserver / caster 推流
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 1107 全是 `Corrupt` | 0.11.0 不认 NSat=0 的空 MSM | 视空 MSM 为正常；或钉 git `f08941b`；统计 Corrupt 时按消息号分 |
| 2 | CRC 坏帧无声消失 | 帧层只返回 `None` | 自己比 `consumed` 与帧长和，估丢包 |
| 3 | 流尾 / 伪 `0xD3` 让迭代器提前停 | `Incomplete` 语义 = 等数据 | 流式用 §3.3 的 drain 循环；整文件末尾残帧可忽略 |
| 4 | 超量程值编码成功 | 构造时不做范围检查 | 编码前自行校验量程；往返断言 |
| 5 | 往返 `==` 失败 | 0.1 mm 量化 + f64 | 按 DF 分辨率容差比较 |
| 6 | 依赖里冒出 `rand` | 默认 feature `test_gen` | `--no-default-features` 再按需开 `std`/`msgXXXX` |
| 7 | 裁剪后大量 `MsgNotSupported` | 对应 `msgXXXX` 未开 | 补 feature；不是数据坏 |
| 8 | MSM 伪距要自拼 | 库只给 DF 字段 | 粗整 + 粗小数 + 精（ms）× c；GLONASS 频道另见 `Msm57GloSat` |
| 9 | 1230 bias −163.84 m | 站方配置未核实 | 使用前对照接收机/站方文档，勿直接改正 |
| 10 | 字段名与 pyrtcm 不同 | 语义名 vs `DFxxx` | 对照 `src/msg/msgXXXX.rs` 的 `(name, dfNNN)` 表 |
| 11 | tip ≠ crates | 空 MSM 修复只在 master | 生产钉 0.11.0 并处理 `Corrupt`，或 git rev 锁定 |
| 12 | 测完残留 | str2str / 临时 crate | `timeout` 抓流；`pgrep str2str` 为空；`rm -rf` 工程 |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| Rust / 嵌入式 / no_std 下解或生成 RTCM3 | **本文 `rtcm-rs` 0.11.0** |
| Python 解析、快速看字段 | [pyrtcm](./pyrtcm.md) |
| RTCM3 → RINEX 文件 | [rtcm3torinex](./rtcm3torinex.md) / RTKLIB `convbin` |
| 从 caster 取流 | [ntrip-client](./ntrip-client.md)（Rust）/ [ntripclient](./ntripclient.md)（C）/ [rtcm-ntrip-software](./rtcm-ntrip-software.md) |
| u-blox UBX 协议 | [pyubx2](./pyubx2.md)；Rust `ublox` crate → [ublox](./ublox.md) |
| BINEX / GPS 电文比特 | [binex](./binex.md) / [gnss-protos](./gnss-protos.md) |

## 8. 相关

[pyrtcm.md](./pyrtcm.md) · [rtcm3torinex.md](./rtcm3torinex.md) · [ntrip-client.md](./ntrip-client.md) · [ntripclient.md](./ntripclient.md) · [ntripserver.md](./ntripserver.md) · [rtcm-ntrip-software.md](./rtcm-ntrip-software.md) · [gnss-protos.md](./gnss-protos.md) · [binex.md](./binex.md) · [ubx2rinex.md](./ubx2rinex.md) · [pyubx2.md](./pyubx2.md) · [rtklib.md](./rtklib.md) · [README.md](./README.md)
