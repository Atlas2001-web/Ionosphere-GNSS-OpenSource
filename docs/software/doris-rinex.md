# doris-rinex · Rust DORIS RINEX 观测文件读写库（crate `doris-rs`）操作手册

目录：上游 <https://github.com/nav-solutions/doris> · crates.io **`doris-rs` 0.1.0**（2025-09-04 15:53 EDT 发布；= tag `v0.1.0` → `924ae02`）· main **`336dd19`**（2026-09-08 06:07 EDT「Bump libs」，比 v0.1.0 多 5 个提交，只放宽 `Cargo.toml` 依赖区间 + 改 README，**未发版**）· **MPL-2.0** · ★**3** · 下载 **1026** · MSRV **1.82**（只写在 `[package.metadata]`，**不是** `rust-version`，cargo 不强制）· 纯库无 bin · 本机 **rustc 1.98.1**（写作 2026-09-26 03:03–03:07 EDT；**R10质检复跑** 03:28–03:35 EDT：man.rs stdout / 写回 F_zero=1198 / 错误表 / georinex `unknown file type D` 全复现）· PROJECTS 登记名 `doris-rinex`

> 岗位：DORIS（法国 CNES 星载多普勒定轨系统）专用 RINEX 3 观测文件（`RINEX VERSION / TYPE` 行 `O` + `D`）的**解析与格式化**。一个文件 = 一颗 DORIS 卫星的接收机，观测对象是地面**信标站**网。冲突时：**上游源码 / docs.rs > 本文**。

## 1. 用途与边界

**做：**

- `DORIS::from_file` / `from_gzip_file`（默认 feature `flate2`）/ `parse(BufReader)` → `header` + `record`
- 头：卫星名、COSPAR、接收机/天线、观测类型、`L2 / L1 DATE OFFSET`、`STATION REFERENCE`（信标 → `GroundStation{label, site, domes, beacon_revision, k_frequency_shift}`）
- 记录：`BTreeMap<Key{epoch,flag}, Measurements>`；每历元星钟偏差 `satellite_clock_offset` + `(站, 观测量) → Observation{value, snr}`
- 写：`to_file` / `to_gzip_file` / `format(BufWriter)`；`standard_filename()`；`substract()` 做两文件差

**不做：**

- 定轨 / 多普勒处理 / 电离层改正：只是 I/O 层
- 普通 GNSS RINEX（OBS/NAV/CLK/MET/CRINEX）：`InvalidDoris`（§5）→ [rinex](./rinex.md)；IONEX → [ionex-rs](./ionex-rs.md)
- **不解析** `SYS / SCALE FACTOR`、`APPROX POSITION XYZ`、`CENTER OF MASS`、`TIME REF STATION`（源码注释掉或忽略，§7）
- 历元事件（flag > 1）README 自认支持不好

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `doris-rs` | DORIS RINEX 专用解析/生成 | `use doris_rs::prelude::*` |
| [rinex](./rinex.md) ≤ 0.21.1 | 旧版内含 `src/doris` 模块 | 0.22.0 已移出，只剩错误枚举 |
| [georinex](./georinex.md) 1.16.2 | Python RINEX | 读 DORIS 报 `unknown file type D` |
| IDS DORIS 产品（SINEX/轨道） | 解算结果 | 不是本库对象 |

## 2. 安装

```bash
export CARGO_HOME=/tmp/doris-man/cargo-home CARGO_TARGET_DIR=/tmp/doris-man/target
cargo new demo && cd demo
cargo add doris-rs@0.1.0          # 实锁 hifitime 4.3.1 / gnss-rs 2.7.0 / flate2 1.1.10 / itertools 0.14.0 / thiserror 2.0.21
cargo build --release             # rustc 1.98.1 无错
```

- feature：显式只有 `default = ["flate2"]`；可选依赖隐式 feature `serde`、`log`。`--no-default-features --features serde,log` 实测可编，`from_file` 读明文 529 历元不变；关掉 `flate2` 后 `from_gzip_file`/`to_gzip_file` 消失。
- 依赖：`hifitime 4`（时间）、`gnss-rs 2`（`DOMES`/`COSPAR`，开 `domes`/`cospar` feature）、`num`、`strum`、`bitflags`、`thiserror 2`。
- 上游仓库测试：main `336dd19` 手工拉 `data` 子模块后 `cargo test`：单元 **17** passed、doctest **14** passed。子模块 URL 是 `git@github.com:`（SSH），无 key 时 `--recursive` 拉不下来，改用 `https://github.com/nav-solutions/data`。
- MSRV 1.82 **未测**（本机只有 stable 1.98.1 与 1.74.1）。

## 3. 可编译例子 + 真实输出

数据：**上游测试数据** `nav-solutions/data` 仓 `DOR/V3/cs2rx18164.gz`（`209bfbd`；45698 B，sha256 `59418b9e…7042`；CryoSat-2，CNES `Expert` 生成，2018-06-13 起 **45 min 片段**，解压 3001 行）。IDS 公开镜像未取到：`doris.ign.fr` 超时，`ftp://doris.ensg.eu` 登录成功但数据连接报 `425 Security: Bad IP connecting`，CDDIS 需 Earthdata 账号 → 未用。

`src/bin/man.rs`（60 行，原样编译运行）：

```rust
use doris_rs::prelude::*;
use std::collections::{BTreeMap, BTreeSet};

fn main() {
    let path = std::env::args().nth(1).expect("usage: man <file>");
    let res = if path.ends_with(".gz") { DORIS::from_gzip_file(&path) } else { DORIS::from_file(&path) };
    let doris = match res {
        Ok(d) => d,
        Err(e) => { println!("ERR: {:?}", e); std::process::exit(2) }
    };
    let h = &doris.header;
    println!("version {}.{} | sat {} | cospar {:?}", h.version.major, h.version.minor,
             h.satellite, h.cospar.as_ref().map(|c| c.to_string()));
    println!("receiver {:?}", h.receiver);
    println!("first obs (header) {:?}", h.time_of_first_observation);
    println!("L2/L1 date offset {}", h.l1_l2_date_offset);
    let obs: Vec<String> = h.observables.iter().map(|o| o.to_string()).collect();
    println!("observables({}) {}", obs.len(), obs.join(","));
    println!("scaling_factors {:?}", h.scaling_factors);
    println!("stations(header) {}", h.ground_stations.len());
    let tlse = h.ground_stations.iter().find(|s| s.label == "TLSB").unwrap();
    println!("  TLSB {} {} rev={} k={}", tlse.site, tlse.domes, tlse.beacon_revision, tlse.k_frequency_shift);

    let rec = &doris.record;
    let epochs: Vec<_> = rec.epochs_iter().collect();
    println!("epochs {}", epochs.len());
    if let (Some(a), Some(b)) = (epochs.first(), epochs.last()) { println!("span {} -> {}", a.0, b.0); }

    let (mut n_obs, mut clk) = (0usize, Vec::new());
    let mut per_sta: BTreeMap<String, usize> = BTreeMap::new();
    let mut temp: BTreeMap<String, (f64, usize)> = BTreeMap::new();
    for m in rec.measurements.values() {
        if let Some(c) = m.satellite_clock_offset { clk.push(c.offset.to_seconds()); }
        let mut seen = BTreeSet::new();
        for (k, o) in m.observations.iter() {
            n_obs += 1;
            seen.insert(k.station.label.clone());
            if k.observable == Observable::Temperature {
                let e = temp.entry(k.station.label.clone()).or_default();
                e.0 += o.value; e.1 += 1;
            }
        }
        for s in seen { *per_sta.entry(s).or_default() += 1; }
    }
    let mut top: Vec<_> = per_sta.iter().collect();
    top.sort_by(|a, b| b.1.cmp(a.1));
    println!("observations {} | stations seen {} | top3 {:?}", n_obs, per_sta.len(), &top[..3.min(top.len())]);
    let (mn, mx) = clk.iter().fold((f64::MAX, f64::MIN), |a, &v| (a.0.min(v), a.1.max(v)));
    println!("clock offset n={} [{:.9}, {:.9}] s", clk.len(), mn, mx);
    if let Some((k, m)) = rec.measurements.iter().next() {
        for (ok, o) in m.observations.iter().take(4) {
            println!("first {} {} {} = {}", k.epoch, ok.station.label, ok.observable, o.value);
        }
        let f = m.observations.iter().find(|(ok, _)| ok.observable == Observable::FrequencyRatio);
        if let Some((_, o)) = f { println!("first F = {:e}", o.value); }
    }
    for (s, (sum, n)) in temp.iter().take(2) {
        println!("T mean {} = {:.3} °C (n={})", s, sum / *n as f64, n);
    }
}
```

`./target/release/man cs2rx18164.gz` 真实 stdout：

```text
version 3.0 | sat CRYOSAT-2 | cospar Some("2010-013A")
receiver Some(Receiver { model: "DGXX", serial_number: "CHAIN1", firmware: "1.00" })
first obs (header) Some(2018-06-12T23:59:51.085331610 UTC)
L2/L1 date offset 2 μs
observables(10) L1,L2,C1,C2,W1,W2,Frequency ratio,Pressure,Temperature,Moisture rate
scaling_factors {}
stations(header) 53
  TLSB TOULOUSE 10003S005 rev=3 k=0
epochs 529
span 2018-06-13T00:00:33.179947800 TAI -> 2018-06-13T00:45:03.179947800 TAI
observations 11980 | stations seen 15 | top3 [("SYQB", 153), ("HBMB", 150), ("MAUB", 148)]
clock offset n=529 [-4.326636491, -4.326631626] s
first 2018-06-13T00:00:33.179947800 TAI OWFC C1 = -139623093.084
first 2018-06-13T00:00:33.179947800 TAI OWFC C2 = -139623340.448
first 2018-06-13T00:00:33.179947800 TAI OWFC L1 = -677713.668
first 2018-06-13T00:00:33.179947800 TAI OWFC L2 = -133531.158
first F = 1.6936999999999998e-9
T mean ADHC = -18.110 °C (n=98)
T mean BEMB = -34.006 °C (n=119)
```

读法：

- 头里登记 **53** 个信标，这 45 min 实际见到 **15** 个，单历元最多 **5** 站；**11980** 个值 = 1198 站·历元 × 10 观测量。
- 历元标签是 **TAI**（解析时硬编码 `TimeScale::TAI`）；星钟偏差约 −4.3266 s，单位 s；`snr` 全 `None`（§7）。
- `C1`/`C2` 是文件原始数字（头里声明 ×100 比例因子，**库没除**，§7）；`F` 被乘 10⁻¹¹（169.370 → 1.6937×10⁻⁹）。
- `first obs (header)` 是**错的**：文件写 `00:00:28.8533161 DOR`，库读成 TAI 00:00:28.0853316，Debug 又按 UTC 显示（−37 s）→ `23:59:51.085…`（§7）。

## 4. 交叉检查（独立 Python 按列宽解析）

方法：Python 直接读 gzip 文本，按 `>` 行取时间/星钟、`Dnn` 行起每 16 列一个字段（14 值 + LLI + SNR），信标号经 `STATION REFERENCE` 映射到 4 字母标签；Rust 侧另写 CSV 全量导出（`DUMP=rust.csv`）后逐键比较。

| 量 | Rust | Python | 差 |
| --- | ---: | ---: | ---: |
| 历元数 | 529 | 529（`>` 行 529） | 0 |
| 站·历元 | 1198 | 1198（`>` 行站数字段之和） | 0 |
| 观测值个数 | 11980 | 11980 | 键集合差 0 |
| 见到信标 | 15 | 15 | 0 |
| 10 个观测量逐值 | — | — | max\|Δ\| = **0**（F 按 ×10⁻¹¹ 比） |
| 星钟偏差 529 个 | — | — | max\|Δ\| = 8.9×10⁻¹⁶ s |
| 首历元 OWFC C1 | −139623093.084 | −139623093.084 | 0 |
| 末历元 WEUC L1 | −10550167.986 | −10550167.986 | 0 |
| T 均值 ADHC / BEMB | −18.110 / −34.006 °C | −18.11 / −34.006 °C | 0 |
| 站·历元 top3 | SYQB 153 / HBMB 150 / MAUB 148 | 同 | 0 |

- 时间标签：首/末历元 `00:00:33.179947800` / `00:45:03.179947800` 与文本逐位一致（记录部分无 §7 的头时间 bug）。
- georinex 1.16.2（venv 内装）：`gr.load` → `ValueError: unknown file type D`，不能作第二实现。

写回往返（`to_file` → `from_file`）：历元 529、值个数 11980 不变，但 `header == ` **false**、`record ==` **false**：1198 个 `F` 全变 0（写成 `0.000`），另见 §6。

## 5. 错误用例

输入除 `real.gz`/`full.txt`/`gnss_obs.rnx` 外均为**合成**（由真文件删改）。

| 输入 | 结果 |
| --- | --- |
| 空文件（合成） | **Ok**，头全空、0 历元（静默） |
| 只有头（合成） | Ok，10 观测量、53 站、0 历元 |
| 缺 `END OF HEADER`（合成） | Ok，0 历元（静默，记录被当头吃掉） |
| 明文截断在行中间（合成，60000 B） | Ok，151 历元（= 文本 `>` 行数），残行半个字段丢弃 |
| gzip 截断（合成，前 20000 B） | Ok，**228** 历元；`zcat` 能解出 230 个 `>` 并报 unexpected EOF → 末尾 2 历元静默丢 |
| 普通 GNSS RINEX 3（ACOR `…_MO.rnx`） | `Err(InvalidDoris)` |
| 首行把 `D` 改 `G`（合成） | `Err(InvalidDoris)` |
| 某值 `-67x713.668`（合成） | Ok，少 1 个值（11979），**静默** |
| 行截短到 40 列（合成） | Ok，**11977** 值（少 3），静默 |
| 站号 `D99` 不在头里（合成，改**记录**行首码，勿改头 `STATION REFERENCE`） | Ok，该历元消失（**528** 历元 / **11970** 值），静默 |
| 站号 `DXX`（合成） | `Err(StationFormat)` |
| 星钟 `-4.32x631626`（合成） | `Err(ClockOffset)` |
| 历元月份 13（合成） | **panic**（hifitime `invalid Gregorian date`，exit 101） |
| 删 `SYS / # / OBS TYPES`（合成） | **panic**（`record/parsing.rs:151` index out of bounds，exit 101） |
| CRLF 行尾（合成） | Ok，与原文件完全相同计数 |
| 明文文件名 `.gz` 走 `from_gzip_file`（合成） | **Ok 空对象**（0 历元，不报错） |
| `garbage` 7 字节 `.gz`（合成） | Ok 空对象，静默 |
| 文件不存在 | `Err(FileIO(NotFound))` |

结论：只有首行类型、站号格式、星钟字段、IO 会给 `Err`；坏数值、未知信标、非 gzip、截断 gzip 都**静默**；坏日期、缺观测类型会 **panic**。生产代码要自己查 `epochs == 0`、比对 `>` 行数，并对不可信输入用 `catch_unwind`。

## 6. I/O 说明

- 输入：明文 `from_file`（CRLF 可）；gzip `from_gzip_file`（按调用选，不看魔数）；任意 `Read` 走 `parse`。**不读** Hatanaka 压缩，未见 `.Z` 支持。
- 文件名：`CS2RX18164.gz` 类标准名解析进 `production`（`satellite="CS2RX", year=2018, doy=164, gzip_compressed=true`）。
- 输出 `to_file` 实测改动：`PGM` 写成 `doris-rs v0.1.0`；丢 COMMENT、`REC # / TYPE / VERS`、`ANT # / TYPE`、`APPROX POSITION XYZ`、`CENTER OF MASS`、`SYS / SCALE FACTOR`、`L2 / L1 DATE OFFSET`（读回 0 ns）、`TIME REF STATION`；`COSPAR NUMBER` 标签写成 `COSPAR` → 读回 `cospar=None`、`receiver=None`；头行尾空格被去掉；记录行 82 列、**LLI/SNR 全丢**；`F` 写 `0.000`。3001 行 → 2987 行。
- 结论：**只把它当读取器**；写出的文件不宜交给下游分析软件。

## 7. 坑（现象 → 原因 → 修复）

1. **头 `TIME OF FIRST OBS` 小数错位** → `parse_time_of_obs` 把 7 位小数 `8533161` 当纳秒按 `{:08}` 拼成 `.08533161` → 慢 0.768 s；上游 README 对应断言已注释掉。修：自己从文本取，或用第一个记录历元。
2. **`{:?}` 打印头时间显示 UTC**（差 37 s）→ hifitime `Debug` 一律转 UTC 呈现，`Display` 才按自身时间尺（实测 `{}` = `2018-06-13T00:00:28.085331610 TAI`）。修：日志用 `{}`，比较前对齐 `time_scale`。
3. **`SYS / SCALE FACTOR` 不解析**，`scaling_factors` 恒空，`C1`/`C2` 保留文件原数。修：按头自己除以 100（本文件声明 `D 100 2 C1 C2`）。
4. **`F` 自动 ×10⁻¹¹**，但写回时按 `%.3` 输出成 `0.000` → 往返 1198 个值全丢。
5. **未知信标整历元丢**：只要该站号不在 `STATION REFERENCE` 中，就无日志地跳过；开 `log` feature 才有 debug 行。
6. **截断 gzip 静默少历元**；非 gzip 喂 `from_gzip_file` 得空对象而非 Err。
7. **panic**：非法日期、缺观测类型行（§5）。
8. **`GroundStation` 相等含私有 `code`**：自己 `default().with_…()` 构造时要 `.with_unique_id(n)`，否则 `==` 失败。
9. **SNR/LLI 不可用**：11980 个值 `snr` 全为 `None`（解析时挂载代码被注释），写出也不带。
10. 数据子模块 SSH URL（§2）；crates.io 0.1.0 与 main 仅依赖区间不同，功能相同。

## 8. 选型

| 你要… | 用 |
| --- | --- |
| Rust 里读 DORIS RINEX（头、信标、历元、原始 L/C/W/F/P/T/H） | **本文**（避开 §7 的 1–4） |
| 普通 GNSS RINEX OBS/NAV/MET/CLK、CRINEX | [rinex](./rinex.md)；CLI [rinex-cli](./rinex-cli.md) |
| 多文件 QC 报告 | [gnss-qc](./gnss-qc.md)（不收 DORIS） |
| SP3 精密轨道（DORIS 卫星定轨产品） | [sp3](./sp3.md) |
| 时间系（TAI/UTC/GPST） | [hifitime](./hifitime.md) |
| `DOMES`/`COSPAR`/星座 | [gnss-rs](./gnss-rs.md) |
| Python 读 GNSS RINEX | [georinex](./georinex.md)（DORIS 不支持，需自写列宽解析，见 §4） |

未测：MSRV 1.82 编译、IDS/CDDIS 全天文件（非上游片段）、RINEX 2 DORIS、`substract()`、`serde` 序列化输出、epoch flag > 1、超大文件性能。

## 9. 相关

[rinex.md](./rinex.md) · [rinex-cli.md](./rinex-cli.md) · [gnss-qc.md](./gnss-qc.md) · [sp3.md](./sp3.md) · [hifitime.md](./hifitime.md) · [gnss-rs.md](./gnss-rs.md) · [georinex.md](./georinex.md) · [ionex-rs.md](./ionex-rs.md) · [docs.rs/doris-rs](https://docs.rs/doris-rs) · [IDS](https://ids-doris.org/) · [README.md](./README.md)
