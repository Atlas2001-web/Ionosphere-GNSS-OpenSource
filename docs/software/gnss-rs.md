# gnss-rs · GNSS 星座 / SV 基础类型库操作手册

目录：[`PROJECTS.json` → `nav-solutions-gnss`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/gnss> · crates.io **`gnss-rs` 2.7.0**（2026-09-08 发布；tag **`v2.7.0`=`71df4af`**；main **`1eff5ef`**）· **MPL-2.0** · ★**11** · MSRV **1.85.0** · **无 [[bin]]**（纯库；lib 名 `gnss_rs`）· 本机 **rustc 1.98.1**（2026-09-26 00:32 EDT 真跑）

> 岗位：nav-solutions 生态的**最底层共享类型**：`Constellation`（星座枚举）+ `SV`（卫星 = 星座 + PRN）+ 可选 SBAS 库 / DOMES / COSPAR。冲突时：**上游 README / docs.rs / 本机 `cargo doc -p gnss-rs` > 本文**。  
> 上层消费者：[rinex](./rinex.md)（0.22.0 依赖 `gnss-rs ^2.6`）· [gnss-rtk](./gnss-rtk.md)（0.8.0 → `^2.4`）· [sp3](./sp3.md)（1.4.1 → `^2.4`）· [cggtts](./cggtts.md)（4.4.0 → `^2.4`）· [rnx2cggtts](./rnx2cggtts.md) 间接。[binex](./binex.md) 0.5.2 的 `Cargo.toml` **未见** `gnss-rs` 依赖。

## 1. 用途与边界

**做：**

- `Constellation`：GPS/Glonass/Galileo/BeiDou/QZSS/IRNSS + **14** 个 SBAS 变体（WAAS/EGNOS/MSAS/GAGAN/BDSBAS/KASS/SDCM/ASBAS/SPAN/AusNZ/GBAS/NSAS/ASAL/通用 `SBAS`）+ `Mixed`
- 三种格式化：`{}`=全名+国别，`{:E}`=缩写，`{:x}`=**RINEX 单字母**；`FromStr` 大小写不敏感 + 模糊匹配
- `SV { prn: u8, constellation }`：`"G01"` 式 CNN 解析/打印、`timescale()`、`is_beidou_geo()`
- `std` 下内置 **SBAS 卫星库**：`S23` → `EGNOS`/`ASTRA-5B`/发射时刻；`sbas` feature 下 `sbas_selector(经纬度)` 选区域 SBAS
- `domes`：IERS DOMES 站号解析；`cospar`：COSPAR 发射号解析；`serde` 派生

**不做：**

- **没有** 载波/信号/频点/波长：2.7.0 源码**无** `Carrier`/`Signal`/频率 API → 频点在 [rinex](./rinex.md)（`rinex::carrier`）或 [gnss-rtk](./gnss-rtk.md)（`gnss_rtk::prelude::Carrier`）
- **不是** 文件读写（RINEX/SP3/BINEX/CGGTTS）→ [rinex](./rinex.md) / [sp3](./sp3.md) / [binex](./binex.md) / [cggtts](./cggtts.md)
- **不是** 定位/钟差/TEC 解算 → [gnss-rtk](./gnss-rtk.md) / [rtklib](./rtklib.md)；TEC → [gnss-tec](./gnss-tec.md) / [ionex-rs](./ionex-rs.md)
- **不是** 时间尺转换：`timescale()` 只返回 hifitime 的 `TimeScale` 标签；换算用 `hifitime`（本车道下一篇）
- **不是** 广播电文编解码 → [gnss-protos](./gnss-protos.md)

一句话：`gnss-rs` = **"G01 是谁、属于哪个星座/时间尺"**；一行观测值都不碰。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `gnss-rs` | 星座/SV 类型纯库 | `cargo add gnss-rs`；`use gnss_rs::prelude::*` |
| 名字四处不同 | 仓 `gnss` / 包 `gnss-rs` / 导入 `gnss_rs` / Python 模块 `gnss` | crates.io 查 `gnss` → `does not exist`（本机 2026-09-26） |
| [gnss-rtk](./gnss-rtk.md) | 解算库（含 `Carrier` 频点） | 依赖本库 |
| [rinex](./rinex.md) | RINEX 文件库（含 `Carrier`、`Observable`） | 重导出本库类型 |
| [gnss-protos](./gnss-protos.md) | LNAV 帧编解码 | 比特流 |

## 2. 安装

```bash
. "$HOME/.cargo/env"; rustc --version        # 本机 1.98.1（MSRV 1.85）
cargo new gnssrs_demo && cd gnssrs_demo
cargo add gnss-rs@2.7 --features std,full,serde   # full = sbas + domes + cospar
cargo add serde_json geo@0.31                      # 仅示例：JSON + sbas_selector 的 Point
```

| feature | 默认 | 作用 | 依赖 |
| --- | --- | --- | --- |
| （无） | ✓ | `no_std`；`Constellation` + `SV` 基础 | hifitime、thiserror |
| `std` | | SBAS 卫星库（`S23`→EGNOS 名称/发射时刻）、`SV::new_sbas` | hifitime/std |
| `sbas` | | `sbas_selector(Point)` 地理多边形 | std + geo 0.31 + geojson + bincode |
| `domes` | | `DOMES` / `DOMESTrackingPoint`（不需 std） | — |
| `cospar` | | `COSPAR` | std |
| `serde` | | 派生 Serialize/Deserialize（隐式可选依赖 feature） | serde |
| `python` | | pyo3 绑定（模块名 `gnss`） | pyo3 0.27 |
| `full` | | = `sbas`+`domes`+`cospar` | |

默认**不含 `std`**：同一串 `"S23"` 在默认 feature 下解析成 `SBAS`，开 `std` 才变成 `EGNOS`（见 §3.4）。

## 3. 可编译小例（本机真跑；2026-09-26 00:32 EDT）

`src/main.rs`（节选；完整即以下各段拼接，`use` 共用）：

```rust
use std::str::FromStr;
use geo::Point;
use gnss_rs::{prelude::*, sbas_selector};

for c in [Constellation::GPS, Constellation::Glonass, Constellation::Galileo,
          Constellation::BeiDou, Constellation::QZSS, Constellation::IRNSS,
          Constellation::WAAS, Constellation::BDSBAS, Constellation::Mixed] {
    println!("{:?}\t'{}'\t{:E}\t{:x}\tts={:?}\tsbas={}",
             c, c, c, c, c.timescale(), c.is_sbas());
}
for s in ["G", "c", "GAL", "BDS", "bdsbas", "NAV/IC", "Galileo (EU)", "S", "Z", "FOO"] {
    println!("{:?} -> {:?}", s, Constellation::from_str(s));
}
for s in ["G01", "e05", "C03", "C60", "C30", "R24", "S23", "S48", "S01", "G1", "G99"] {
    let sv = SV::from_str(s).unwrap();
    println!("{s} -> {:?} | Display={} | {{:x}}={:x} | bds_geo={} | ts={:?}",
             sv, sv, sv, sv.is_beidou_geo(), sv.timescale());
}
println!("{:?}", sbas_selector(Point::new(114.3, 30.6)));        // x=经度°, y=纬度°
println!("{:?}", DOMES::from_str("10002M006"));
println!("{:?}", COSPAR::from_str("2018-080A"));
println!("{}", serde_json::to_string(&SV::from_str("E13").unwrap()).unwrap());
```

### 3.1 星座：Display / 缩写 / RINEX 字母 / 时间尺

```text
GPS	'GPS (US)'	GPS	G	ts=Some(GPST)	sbas=false
Glonass	'Glonass (RU)'	GLO	R	ts=Some(UTC)	sbas=false
Galileo	'Galileo (EU)'	GAL	E	ts=Some(GST)	sbas=false
BeiDou	'BeiDou (CH)'	BDS	C	ts=Some(BDT)	sbas=false
QZSS	'QZSS (JP)'	QZSS	J	ts=Some(QZSST)	sbas=false
IRNSS	'IRNSS (IN)'	IRNSS	I	ts=None	sbas=false
WAAS	'WAAS (US)'	WAAS	S	ts=Some(GPST)	sbas=true
BDSBAS	'BDSBAS (CH)'	BDSBAS	S	ts=Some(GPST)	sbas=true
Mixed	'MIXED'	MIX	M	ts=None	sbas=false
```

要点：RINEX 字母 **G/R/E/C/J/I/S/M**；所有 SBAS 都打印成 `S`；Glonass 时间尺给 **UTC**（不是 GLONASST）；**IRNSS 为 `None`**；所有 SBAS 统一返回 **GPST**。

### 3.2 `Constellation::from_str`

```text
           "G" -> Ok(GPS)
           "c" -> Ok(BeiDou)
         "GAL" -> Ok(Galileo)
         "BDS" -> Ok(BeiDou)
      "bdsbas" -> Ok(BDSBAS)
      "NAV/IC" -> Ok(IRNSS)
"Galileo (EU)" -> Ok(Galileo)
           "S" -> Ok(SBAS)
           "Z" -> Err(Unknown)
         "FOO" -> Err(Unknown)
```

`{}` 输出（如 `"Galileo (EU)"`）可逆解析；单字母 `S` 只能回到通用 `SBAS`（不回 WAAS/EGNOS）。

### 3.3 SV：CNN 往返、北斗 GEO、SBAS 库

```text
  G01 -> SV { prn: 1, constellation: GPS } | Display=G01 | {:x}=G01 | bds_geo=false | ts=Some(GPST)
  e05 -> SV { prn: 5, constellation: Galileo } | Display=E05 | {:x}=E05 | bds_geo=false | ts=Some(GST)
  C03 -> SV { prn: 3, constellation: BeiDou } | Display=C03 | {:x}=C03 | bds_geo=true | ts=Some(BDT)
  C60 -> SV { prn: 60, constellation: BeiDou } | Display=C60 | {:x}=C60 | bds_geo=true | ts=Some(BDT)
  C30 -> SV { prn: 30, constellation: BeiDou } | Display=C30 | {:x}=C30 | bds_geo=false | ts=Some(BDT)
  R24 -> SV { prn: 24, constellation: Glonass } | Display=R24 | {:x}=R24 | bds_geo=false | ts=Some(UTC)
  S23 -> SV { prn: 23, constellation: EGNOS } | Display=ASTRA-5B | {:x}=S23 | bds_geo=false | ts=Some(GPST)
  S48 -> SV { prn: 48, constellation: ASAL } | Display=ALCOMSAT-1 | {:x}=S48 | bds_geo=false | ts=Some(GPST)
  S01 -> SV { prn: 1, constellation: SBAS } | Display=S01 | {:x}=S01 | bds_geo=false | ts=Some(GPST)
   G1 -> SV { prn: 1, constellation: GPS } | Display=G01 | {:x}=G01 | bds_geo=false | ts=Some(GPST)
  G99 -> SV { prn: 99, constellation: GPS } | Display=G99 | {:x}=G99 | bds_geo=false | ts=Some(GPST)
S23 Display reparse: Err("constellation parsing error: Unknown constellation")
S23 launch=Some(2021-11-01T00:00:00 UTC)
new_sbas(23)=Some(SV { prn: 23, constellation: EGNOS }) new_sbas(1)=None
```

- `is_beidou_geo()` 规则 = BeiDou 且 **PRN<6 或 PRN>58**（C03/C60 → true，C30 → false）
- SBAS 映射：库按 **PRN+100**（S23 ↔ PRN 123）查内置表；表里没有的（S01）保留通用 `SBAS`
- **PRN 不做合法性检查**：`G99`、`G00` 都 `Ok`
- 写文件请用 `{:x}`（恒为 CNN）；`{}` 对已知 SBAS 输出卫星名，**无法**再 `from_str`

### 3.4 默认 feature（无 std）对照

```text
default-features S23 -> SV { prn: 23, constellation: SBAS } | Display=S23
G05 -> G05
```

### 3.5 `sbas_selector`（`sbas` feature；`Point::new(经度°, 纬度°)`）

```text
Paris: Some(EGNOS)
Wuhan: Some(BDSBAS)
Boulder: Some(WAAS)
Tokyo: Some(MSAS)
Antarctica: None
```

### 3.6 DOMES / COSPAR / serde

```text
10002M006 -> DOMES { area: 100, site: 2, point: Monument, sequential: 6 } | Display=10002M006
40405S031 -> DOMES { area: 404, site: 5, point: Instrument, sequential: 31 } | Display=40405S031
1000M006 -> Err(invalid domes length)
ABCDEM006 -> Err(invalid domes format)
2018-080A -> COSPAR { year: 2018, launch: 80, code: "A" } | Display=2018-080A
1998-067 -> Err(Invalid COSPAR number)
abcd-080A -> Err(Invalid COSPAR number)
E13 json={"prn":13,"constellation":"Galileo"} back=SV { prn: 13, constellation: Galileo }
GPS json="GPS"
```

DOMES 中 `M`=Monument、`S`=Instrument；COSPAR 长度 **<9** 直接拒（`1998-067` 缺件号）。

### 3.7 非法输入（如实）

```text
  X01 -> Err("constellation parsing error: Unknown constellation")
    G -> Err("failed to parse PRN numer")
  G0A -> Err("failed to parse PRN numer")
   01 -> Err("constellation parsing error: Unknown constellation")
 S999 -> Err("failed to parse PRN numer")        # u8 溢出
thread 'main' panicked at …/gnss-rs-2.7.0/src/sv/mod.rs:199:60:
end byte index 1 is out of bounds for string of length 0
SV::from_str("") panicked=true
```

**空串 `SV::from_str("")` 是 panic，不是 `Err`**（`&string[0..1]` 越界）；错误信息原文拼写 `numer`。

## 4. I/O 与关键 API

| API | 输入 → 输出 |
| --- | --- |
| `Constellation::from_str(&str)` | 单字母/缩写/全名（大小写不敏感）→ `Result<_, ParsingError::Unknown>` |
| `format!("{}"/"{:E}"/"{:x}", c)` | `GPS (US)` / `GPS` / `G` |
| `c.timescale()` | `Option<hifitime::TimeScale>` |
| `c.is_sbas()` / `country_code()` / `from_country_code()` | 布尔 / `Some("US")` / 反查 |
| `SV::new(c, prn)` | 不校验 PRN |
| `SV::from_str("G01")` | `Result<SV, sv::ParsingError>`；空串 panic |
| `format!("{:x}", sv)` | 恒为 `G01` 式 CNN |
| `SV::new_sbas(prn)` / `launch_datetime()` / `duration_since_launch(t)` | std；仅内置 SBAS 表 |
| `sv.is_beidou_geo()` | PRN<6 或 >58 |
| `sbas_selector(Point)` | `sbas`；`Option<Constellation>` |
| `DOMES::from_str` / `COSPAR::from_str` | `domes` / `cospar` |
| 宏 `sv!("G08")` / `gnss!("gps")` | 内部 `unwrap()`；需 `use std::str::FromStr` + prelude |

prelude 同时重导出 `hifitime::{Epoch, TimeScale}`。

## 5. 接到哪步

```text
gnss-rs（G01/EGNOS/GPST 标签）
  → rinex / sp3 / cggtts / binex：文件里的 SV、星座字段
  → gnss-rtk：解算候选 SV、Carrier 频点（频点在 gnss-rtk/rinex）
  → rnx2cggtts：RINEX→CGGTTS 共视
  → 时间尺换算：hifitime
  → TEC/电离层：本库不参与（gnss-tec / ionex-rs / georinex）
```

交叉：[rinex](./rinex.md) · [rinex-cli](./rinex-cli.md) · [rnx2cggtts](./rnx2cggtts.md) · [gnss-rtk](./gnss-rtk.md) · [gnss-protos](./gnss-protos.md) · [sp3](./sp3.md) · [binex](./binex.md) · [cggtts](./cggtts.md) · [rinex2bin](./rinex2bin.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `S23` 有时 EGNOS 有时 SBAS | 默认 no_std 无 SBAS 表 | 显式 `features=["std"]`，全链统一 |
| 2 | `SV::new_sbas` 找不到 | 仅 `std` | 开 `std` |
| 3 | `sbas_selector` 不存在 / `Point` 类型不匹配 | 需 `sbas`；库绑 geo **0.31**，你用 0.33 则是另一个 `Point` | `--features sbas`；用 `gnss_rs::Point` 或锁 `geo@0.31` |
| 4 | 经纬度反了选错区 | `Point::new(x=经度, y=纬度)` | 先经后纬 |
| 5 | `to_string()` 写进文件后读不回 | 已知 SBAS 的 `{}`=卫星名 | 写盘用 `format!("{:x}", sv)` |
| 6 | 空串解析直接崩 | `from_str("")` 切片越界 panic | 调用前 `trim()` + 判空 |
| 7 | `G99`/`G00` 被接受 | 不校验 PRN 范围 | 上层自行校验 |
| 8 | Glonass 时间尺是 UTC、IRNSS 是 None | 库的约定 | 需要 GLONASST/IST 自行映射（hifitime） |
| 9 | 找 L1/L5 频率、波长 | 2.7.0 无载波 API | 用 [gnss-rtk](./gnss-rtk.md)/[rinex](./rinex.md) 的 `Carrier` |
| 10 | 上层 crate 拿不到 2.7 新行为 | rinex/sp3/gnss-rtk 声明 `^2.4`/`^2.6`，旧 `Cargo.lock` 仍锁老 2.x | `cargo update -p gnss-rs`；`cargo tree -i gnss-rs` 确认只有 2.7.0 |
| 11 | `sv!`/`gnss!` 宏编译报 `from_str` 未找到 | 宏展开需 `FromStr` 在作用域 | `use std::str::FromStr;` |
| 12 | 当解算/TEC 库用 | 只是类型定义 | 见 §5 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust 里统一表示星座 / SV / RINEX 字母 | **gnss-rs（本文）** |
| 载波频点、观测量代码 | [rinex](./rinex.md) / [gnss-rtk](./gnss-rtk.md) |
| 读写 RINEX / SP3 / BINEX / CGGTTS | [rinex](./rinex.md) / [sp3](./sp3.md) / [binex](./binex.md) / [cggtts](./cggtts.md) |
| SPP/PPP/RTK 解算 | [gnss-rtk](./gnss-rtk.md) / [rtklib](./rtklib.md) |
| RINEX→CGGTTS | [rnx2cggtts](./rnx2cggtts.md) |
| LNAV 帧编解码 | [gnss-protos](./gnss-protos.md) |
| GPST/GST/BDT/UTC 换算 | `hifitime`（本目录待写） |

相关：上游 README · docs.rs `gnss-rs` · [rinex](./rinex.md) · [gnss-rtk](./gnss-rtk.md) · [sp3](./sp3.md) · [cggtts](./cggtts.md) · [data-access](../data-access.md)
