# sinex · Rust Bias-SINEX（DSB/OSB `.BIA`/`.BSX`）解析库操作手册

目录：上游 <https://github.com/nav-solutions/sinex>（旧址 `rtk-rs/sinex` **301** 跳转；crates 元数据仍写旧址）· crates.io **`sinex` 0.2.4**（2025-02-22 发布；包内 `.cargo_vcs_info.json` 指 **`e47d514`**，dirty；无 git tag）· main **`c236b9b`**（2025-03-10 09:55 EDT，只多 thiserror 2 / strum_macros 0.27 两个 dependabot 合并）· **MPL-2.0** · ★**1** · 下载 **9686** · 反向依赖 **0** · **未声明 MSRV**（无 `rust-version`，CI 用 stable）· 纯库 · 本机 **rustc 1.98.1**（2026-09-26 00:58–01:05 EDT 真跑）· **未登记** `PROJECTS.json`

> 岗位：nav-solutions 生态里 **SINEX 家族的读取器**，但 0.2.4 实际**只读 Bias-SINEX**（`%=BIA`）：头行、FILE/REFERENCE、FILE/COMMENT、INPUT/ACKNOWLEDGMENTS、BIAS/DESCRIPTION、BIAS/SOLUTION。冲突时：**上游源码 / docs.rs > 本文**。  
> 对电离层课的意义：卫星/接收机 **DCB（DSB）与 OSB** 就是 TEC 里要扣掉的"硬件延迟"（[09 课](../tutorials/09-dcb-biases-deep.md)）。本库只**读**别人估好的偏差，**不估计**。

## 1. 用途与边界

**做：**

- `Sinex::from_file(path)` → `header.bias_header()`（版本、机构、数据时段、`A/R` 模式、条数字段）+ `reference` + `comments` + `acknowledgments`
- `description.bias_description()`：`OBSERVATION_SAMPLING`、`PARAMETER_SPACING`、`DETERMINATION_METHOD`、`BIAS_MODE`、`TIME_SYSTEM`、卫星钟参考观测量
- `record.bias_solutions()` → `Vec<Solution>`：`btype`（DSB/ISB/OSB）、`svn`、`prn`、`station`、`obs=(OBS1, Option<OBS2>)`、起止时刻（`chrono::NaiveDateTime`）、`unit`、`estimate`、`stddev`

**不做：**

- **测站坐标 SINEX（`%=SNX`，SITE/ID、SOLUTION/ESTIMATE）**：直接 `UnknownSection`（§3.3）；**TRO-SINEX** 代码被注释掉，同样报错 → Python 用 [gnssanalysis](./gnssanalysis.md)
- **不估计** DCB/OSB → [gkit-bias](./gkit-bias.md)（C++ 全频点 DCB/UPD→OSB）/ [mcosb](./mcosb.md)（MATLAB 码 OSB）
- 不读 CODE 旧版 `P1C1/P1P2 .DCB` 文本（非 SINEX）；不解 `.gz`；不写文件；无 `hifitime` 时间类型（用 chrono）
- `slope`/`slope_stddev` 字段存在但恒 `None`

一句话：`sinex 0.2.4` = **Bias-SINEX 行解析器**；解析 ≠ DCB 估计 ≠ TEC 校准。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `sinex` | Rust Bias-SINEX 读取 | `use sinex::Sinex` |
| [gnssanalysis](./gnssanalysis.md) | GA Python：`bia.read_bia` + 坐标 `sinex` | PyPI |
| [gkit-bias](./gkit-bias.md) / [mcosb](./mcosb.md) | 偏差**估计**并写 BIA | 产出 `.BIA` |
| CODE `comWWWWD.dcb` | 旧 DCB 文本表（`P1-C1` 等） | 首行无 `%=BIA` |

## 2. 安装

```bash
cargo new sxdemo && cd sxdemo
cargo add sinex chrono@0.4      # 锁到 sinex 0.2.4 + gnss-rs 2.7.0 + hifitime 4.3.1
cargo build                      # 冷编 8.47 s，无报错
```

与 [gnss-qc](./gnss-qc.md) 不同：sinex 只用 `Constellation::from_str`，**gnss-rs 2.7.0 直接可编**，无需锁版本。实锁：`sinex 0.2.4` + `gnss-rs 2.7.0` + `chrono 0.4.45` + `strum 0.26.3` + `thiserror 1.0.69`（gnss-rs 另拉 thiserror 2）。

Features：**无**。crates 包 `exclude = ["data/*"]`，`tests/parser.rs` 要 clone 仓库才跑得动；仓内 fixture：`data/BIA/V1/example-{1a,1b,2a,2b}.bia`（CODE 2016）+ `data/TROP/V2/example1.txt`。main 上 `cargo test`：单元 **7 passed** + parser **1 passed**。

## 3. 可编译小例（本机真跑）

`src/main.rs`（`--fix` 走 §6 的预处理绕过 0.2.4 两个 bug）：

```rust
use sinex::{bias::BiasType, Sinex};
use std::collections::HashMap;

fn main() {
    let path = std::env::args().nth(1).expect("usage: sxdemo <file.bia> [--fix]");
    let fix = std::env::args().any(|a| a == "--fix");
    let path = if fix { normalize(&path) } else { path };
    let snx = match Sinex::from_file(&path) {
        Ok(s) => s,
        Err(e) => { println!("ERR {:?} / {}", e, e); return; }
    };
    let h = snx.header.bias_header().unwrap();
    println!("header: v{} creator={} data={} start={} end={} mode={:?} length={}",
        h.version, h.creator_code, h.data_code, h.start_time, h.end_time, h.bias_mode, h.length);
    println!("created = {}  (raw header field)", h.date);
    println!("ref.output = {}", snx.reference.output);
    println!("ref.software = {}", snx.reference.software);
    println!("comments={} acks={}", snx.comments.len(), snx.acknowledgments.len());
    let d = snx.description.bias_description().unwrap();
    println!("desc: sampling={:?} spacing={:?} method={:?} mode={:?} tsys={:?} sat_clk_ref={:?}",
        d.sampling, d.spacing, d.method, d.bias_mode, d.system, d.sat_clock_ref);
    let sols = snx.record.bias_solutions().unwrap();
    let mut by_type: HashMap<String, usize> = HashMap::new();
    for s in sols.iter() { *by_type.entry(format!("{:?}", s.btype)).or_default() += 1; }
    println!("solutions={} by_type={:?}", sols.len(), by_type);
    let mut sats: Vec<&str> = sols.iter().filter(|s| s.station.is_none()).map(|s| s.prn.as_str()).collect();
    sats.sort(); sats.dedup();
    println!("satellites={} stations={}", sats.len(),
        { let mut v: Vec<_> = sols.iter().filter_map(|s| s.station.clone()).collect(); v.sort(); v.dedup(); v.len() });
    // G01 code biases
    let osb = |prn: &str, obs: &str| sols.iter().find(|s| s.btype == BiasType::OSB && s.prn == prn && s.obs.0 == obs && s.obs.1.is_none()).map(|s| s.estimate);
    for s in sols.iter().filter(|s| s.prn == "G01" && s.station.is_none()).take(8) {
        println!("  {:?} {} {} {:?} {:?}..{:?} {} {:+.4} ±{:.4} dur={}h",
            s.btype, s.svn, s.prn, s.obs, s.start_time, s.end_time, s.unit, s.estimate, s.stddev, s.duration().num_hours());
    }
    for prn in ["G01", "G02", "G19"] {
        if let (Some(c1c), Some(c1w), Some(c2w)) = (osb(prn, "C1C"), osb(prn, "C1W"), osb(prn, "C2W")) {
            println!("  {prn}: DCB C1C-C1W = {:+.4} ns, C1C-C2W = {:+.4} ns, C1W-C2W = {:+.4} ns",
                c1c - c1w, c1c - c2w, c1w - c2w);
        }
    }
}

/// 0.2.4 workaround: Latin-1 -> lossy UTF-8; +/- section lines trim_end; solution lines insert 1 col
fn normalize(src: &str) -> String {
    let bytes = std::fs::read(src).expect("read");
    let text = String::from_utf8_lossy(&bytes);
    let mut out = String::new();
    for line in text.lines() {
        if line.starts_with('+') || line.starts_with('-') {
            out.push_str(line.trim_end());
        } else if line.len() > 70 && [" OSB ", " DSB ", " ISB "].iter().any(|k| line.starts_with(k)) {
            out.push_str(&line[..70]); // 规范列：行首空格 + 值 21 + σ 11
            out.push(' ');             // 补 1 列，凑成 crate 期望的 22/12 宽
            out.push_str(&line[70..]);
        } else {
            out.push_str(line);
        }
        out.push('\n');
    }
    let dst = format!("{src}.fixed");
    std::fs::write(&dst, out).expect("write");
    dst
}
```

### 3.1 真实公开文件：CODE MGEX OSB `com22370.bia`（2022-11-20，DOY 324）

来源：BKG IGS 镜像 `https://igs.bkg.bund.de/root_ftp/IGS/products/mgex/2237/com22370.bia.Z`（88385 B，解压 **6738** 行；BIAS/SOLUTION **6668** 行全为 OSB）。CAS `CAS0MGXRAP_*_DCB.BSX` 试了 IGN / gipp.org.cn FTP / WHU FTP 均超时或 502，本机**未取到**；CDDIS 需 Earthdata 登录。

不加 `--fix` 直接失败（§6 坑 1）：

```text
ERR UnknownSection("FILE/REFERENCE                                                                 ") / unknown type of section
```

加 `--fix` 后（原样，前 8 条 G01 截取）：

```text
header: v1.00 creator=COD data=MGX start=2022-11-20 00:00:00 end=2022-11-21 00:00:00 mode=Absolute length=6712
created = 2022-12-02 10:00:00  (raw header field)
ref.output = CODE IGS 1-day MGEX bias solution for G/R/E/C/J
ref.software = Bernese GNSS Software Version 5.5
comments=19 acks=2
desc: sampling=Some(300) spacing=Some(86400) method=Some(ClockAnalysis) mode=Absolute tsys=GNSS(GPS) sat_clk_ref={BeiDou: ["C2I", "C6I"], Galileo: ["C1C", "C5Q"], QZSS: ["C1C", "C2L"], Glonass: []}
solutions=6668 by_type={"OSB": 6668}
satellites=97 stations=139
  OSB G063 G01 ("C1C", None) 2022-11-20T00:00:00..2022-11-21T00:00:00 ns -1.4477 ±0.0065 dur=24h
  OSB G063 G01 ("C1W", None) 2022-11-20T00:00:00..2022-11-21T00:00:00 ns -0.0000 ±0.0000 dur=24h
  OSB G063 G01 ("C2L", None) 2022-11-20T00:00:00..2022-11-21T00:00:00 ns -1.3410 ±0.0181 dur=24h
  ...
  OSB G063 G01 ("L1C", None) 2022-11-20T00:00:00..2022-11-21T00:00:00 ns -1.1579 ±0.0000 dur=24h
  G01: DCB C1C-C1W = -1.4477 ns, C1C-C2W = -1.4477 ns, C1W-C2W = +0.0000 ns
  G02: DCB C1C-C1W = +1.7988 ns, C1C-C2W = +1.7988 ns, C1W-C2W = +0.0000 ns
  G19: DCB C1C-C1W = +2.3341 ns, C1C-C2W = +2.3341 ns, C1W-C2W = -0.0000 ns
```

与原文逐行对照（文件第 68/69/73 行）：

```text
 OSB  G063 G01           C1C       2022:324:00000 2022:325:00000 ns                 -1.4477      0.0065
 OSB  G063 G01           C1W       2022:324:00000 2022:325:00000 ns                 -0.0000      0.0000
 OSB  G063 G01           C2W       2022:324:00000 2022:325:00000 ns                 -0.0000      0.0000
```

交叉核对：同目录旧格式 `com22370.dcb`（"DIFFERENTIAL (P1-C1) CODE BIASES"）写 `G01 1.448`、`G02 -1.799`、`G19 -2.334` ns，正好 = −(C1C−C1W)，即 P1−C1 = OSB(C1W) − OSB(C1C)。**注意** GPS C1W/C2W 的 OSB 按钟基准（`SATELLITE_CLOCK_REFERENCE_OBSERVABLES G C1W C2W`）取 0，所以**从这份 OSB 算不出 P1−P2 DCB**；做 TEC 要的是 DSB 产品（CAS DCB、CODE P1P2）或 GIM 附带 DCB。换算尺度：GPS L1/L2 上 1 ns 码偏差差 ≈ **2.854 TECU**（$c\cdot 10^{-9}/[40.3\times10^{16}(1/f_2^2-1/f_1^2)]$）。

### 3.2 crate fixture：`example-1b.bia`（CODE 30 天相对 DSB，2016）

```text
header: v1.00 creator=COD data=IGS start=2016-10-22 00:00:00 end=2016-11-28 00:00:00 mode=Relative length=194
desc: sampling=Some(300) spacing=Some(86400) method=Some(CombinedAnalysis) mode=Relative tsys=GNSS(GPS) sat_clk_ref={GPS: ["C1W", "C2W"], Glonass: ["C1P", "C2P"]}
solutions=50 by_type={"ISB": 15, "DSB": 35}
  DSB G063 G01 ("C1W", Some("C1C")) 2016-10-22T00:00:00..2016-11-28T00:00:00 ns +1.4376 ±0.0081 dur=888h
  DSB G063 G01 ("C2W", Some("C2C")) 2016-10-22T00:00:00..2016-11-28T00:00:00 ns +8.7736 ±0.0228 dur=888h
  DSB G063 G01 ("C1W", Some("C2W")) 2016-10-22T00:00:00..2016-11-28T00:00:00 ns -7.5594 ±0.0084 dur=888h
```

原文 `DSB   G063 G01           C1W  C1C  2016:296:00000 2016:333:00000 ns                  1.4376      0.0081`——fixture 行**无行首空格**，所以不需 `--fix`。这里 G01 **C1W−C2W = −7.5594 ns** 就是 TEC 要扣的那类 DCB（×2.854 ≈ −21.6 TECU 量级）。`example-2a.bia`（OSB 行缺 OBS2 列）解析得 **solutions=0**，无报错（§6 坑 4）。

### 3.3 失败边界（原样）

| 输入 | 不加 `--fix` | 加 `--fix` |
| --- | --- | --- |
| 空文件 | **Ok**，头为默认值：`creator=Unknown … start=2026-09-26 05:01:47.04…`（当下 UTC），solutions=0 | 同左 |
| 缺路径 `nope.bia` | `ERR FileError(Os { code: 2, kind: NotFound, … })` | 本例 `normalize` 自身 `expect` panic |
| 前 300 行截断（无 `-BIAS/SOLUTION`） | panic `end byte index 12 is out of bounds for string of length 11` | **Ok，solutions=233**，header 仍写 `length=6712`，不报截断 |
| 按 20000 B 截断（末行半截 `OSB  G066 G27`） | `UnknownSection("FILE/REFERENCE   …")` | panic `end byte index 4 is out of bounds for string of length 3` |
| `.bia.gz` | panic `lib.rs:152:30` `stream did not contain valid UTF-8` | `ERR MissingHeader`（lossy 后首行非 `%=`） |
| 旧格式 `com22370.dcb` | `ERR MissingHeader` | 同左 |
| TRO fixture `example1.txt` | `ERR UnknownSection("TROP/DESCRIPTION")` | 同左 |
| 手写 5 行 `%=SNX` 坐标 SINEX（**合成**，仅测分支） | `ERR UnknownSection("SITE/ID")` | 同左 |

## 4. I/O 与关键 API

| 入口 | 说明 |
| --- | --- |
| `Sinex::from_file(&str)` | 唯一入口；无 `from_reader`/`from_str` |
| `header.bias_header()` | `version`/`creator_code`/`data_code`/`date`/`start_time`/`end_time`/`bias_mode`/`length` |
| `description.bias_description()` | `sampling`/`spacing`/`method`/`bias_mode`/`system`/`rcvr_clock_ref`/`sat_clock_ref: HashMap<Constellation, Vec<String>>` |
| `record.bias_solutions()` | `Vec<bias::Solution>`；卫星行 `station=None`，测站行 `station=Some("JOG2")` 类 |
| `Solution::from_str(line)` | 可单独解析一行（固定列宽） |
| `Solution::duration()` | `chrono::TimeDelta` |

时间是 `NaiveDateTime`（**无时间系**；`TIME_SYSTEM` 另见 description）；要换 GPST/UTC 请自己转 [hifitime](./hifitime.md)。

## 5. 接到哪步

```text
下载 CAS/CODE/WHU .BSX/.BIA（解压）→ sinex 读 DSB/OSB（本文）
   → OSB 两两相减得 DCB；或直接取 DSB
   → 在 GF 伪距 STEC 里扣卫星/接收机 DCB（02、09、10 课）→ vTEC / GIM
```

交叉：[gkit-bias](./gkit-bias.md)（估计端）· [mcosb](./mcosb.md) · [gnssanalysis](./gnssanalysis.md) · [gnss-qc](./gnss-qc.md) · [rinex](./rinex.md) · [sp3](./sp3.md) · [hifitime](./hifitime.md) · [gnss-rs](./gnss-rs.md)。课：[02 双频 TEC 与 DCB](../tutorials/02-gnss-dualfreq-tec.md) · [09 DCB/硬件延迟](../tutorials/09-dcb-biases-deep.md) · [10 GIM 工作流](../tutorials/10-build-gim-workflow.md)。

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 真实 CODE 文件 `UnknownSection("FILE/REFERENCE   …")` | `+FILE/REFERENCE` 行尾带空格补到 80 列，`match` 按原串比 | 预处理 `+`/`-` 行 `trim_end()` |
| 2 | 去尾空格后 panic `byte index 12 … length 11` | 解析器先 `trim()` 行首空格，再按 值 22 + σ 12 列切；规范行（行首空格、值 21 + σ 11，共 103 列）trim 后只剩 102 | 在第 70 字节后插 1 空格（本例 `normalize`）；fixture 行本就无行首空格 |
| 3 | panic `stream did not contain valid UTF-8` | `lines().unwrap()`；CODE 注释里 `Jäggi` 是 Latin-1 | `from_utf8_lossy` 或 `iconv -f latin1` |
| 4 | 行解析失败**静默丢弃**（example-2a → 0 条；半截行则 panic） | `if let Ok(sol)`，列宽不对的行被跳过 | 用 `grep -c '^ *OSB'` 与 `solutions.len()` 对数 |
| 5 | `created = 10:00:00`，原文 `36073` s = 10:01:13 | `parse_datetime` 用浮点小时整除，分秒恒 0 | 需要秒级时自己解析 `YYYY:DDD:SSSSS` |
| 6 | `sat_clk_ref` 里 **GPS 丢了** | 遇到只有星座无观测量的行（`R`）时整表覆盖 | 需要时自己扫 BIAS/DESCRIPTION |
| 7 | 空文件/非 BIA 头返回 Ok，时间 = 当前时刻 | 头解析失败回落 `Header::default()`（`Utc::now`） | 检查 `creator_code != "Unknown"` |
| 8 | 截断文件不报错 | 不校验 `-BIAS/SOLUTION` 闭合或 `length` | 自行比对 |
| 9 | `.gz` 读不了 | 无 flate2 | 先 `gzip -d` / `uncompress` |
| 10 | 坐标 SINEX / TRO 报 `UnknownSection` | 0.2.4 只实现 BIA | [gnssanalysis](./gnssanalysis.md) |
| 11 | 以为 GPS C1W−C2W = 0 是真值 | OSB 钟基准把 C1W/C2W 定为 0 | TEC 用 DSB 产品或 GIM DCB |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust 程序里读 Bias-SINEX DSB/OSB | **本文**（配 §3 预处理） |
| Python 读 BIA + 坐标 SINEX + 比较 | [gnssanalysis](./gnssanalysis.md) |
| 自己估 DCB/OSB | [gkit-bias](./gkit-bias.md) / [mcosb](./mcosb.md) |
| 校准 sTEC/vTEC（含弧段偏差处理） | [pytecgg](./pytecgg.md)；[gnss-tec](./gnss-tec.md) 只出未扣 DCB 的 GF TEC |
| RINEX / SP3 解析 | [rinex](./rinex.md) / [sp3](./sp3.md) |
| 时间系换算 | [hifitime](./hifitime.md) |

## 8. 相关

[gkit-bias.md](./gkit-bias.md) · [mcosb.md](./mcosb.md) · [gnssanalysis.md](./gnssanalysis.md) · [gnss-qc.md](./gnss-qc.md) · [rinex.md](./rinex.md) · [sp3.md](./sp3.md) · [hifitime.md](./hifitime.md) · [gnss-rs.md](./gnss-rs.md) · [docs.rs/sinex](https://docs.rs/sinex) · [IGS Bias-SINEX 1.00 规范](https://files.igs.org/pub/data/format/sinex_bias_100.pdf) · [README.md](./README.md)
