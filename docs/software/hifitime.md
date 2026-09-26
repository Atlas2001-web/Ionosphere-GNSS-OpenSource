# hifitime · 高精度时间尺库（GPST/GST/BDT/UTC/TAI/TT）操作手册

目录：nav-solutions 生态底层依赖（未单列 `PROJECTS.json`）· 上游 <https://github.com/nyx-space/hifitime> · crates.io **`hifitime` 4.3.1**（2026-08-07 发布；tag **`4.3.1`=`67ff2fc`**；master **`0d32fb8`**，2026-09-09）· **MPL-2.0** · ★**547** · `rust-version` 未声明 · **纯库**（另有 PyPI 同名绑定 **4.3.1**）· 本机 **rustc 1.98.1** / Python **3.13.5**（2026-09-26 00:36 EDT 真跑）· **质检复跑**（2026-09-26 00:45 EDT；Cargo.lock 实锁 **4.3.1**、pip **4.3.1**）：§3.1/3.2/3.3/3.5 关键行逐字对齐——GPST−UTC 18 s、周 **2295**/tow **86418** s、UTC 历元取周 **(6470, 0)**、`"… GPS"`→`00:00:12 UTC`、UTC 跨闰秒相减 **1 s**/TAI **2 s**、`00:00:35 TAI→23:59:58 UTC` 往返 `eq=false`、空串 `Err` 不 panic；Python 绑定同值

> 岗位：给 GNSS/航天代码一个**纳秒级、带时间尺标签**的 `Epoch` + `Duration`，并在 UTC/TAI/TT/GPST/GST/BDT/QZSST（及 ET/TDB/TCG/TCB）间换算，内置闰秒表。冲突时：**docs.rs / 上游 README / 本机 `cargo doc -p hifitime` > 本文**。
> 下游：[gnss-rs](./gnss-rs.md) 2.7.0（`^4.2`）· [rinex](./rinex.md) 0.22.0（`^4.2`）· [binex](./binex.md) 0.5.2（`^4.2`）· [sp3](./sp3.md) 1.4.1（`^4.1`）· [gnss-rtk](./gnss-rtk.md) 0.8.0（`^4.1`）· [cggtts](./cggtts.md) 4.4.0（`^4.1`）· [rnx2cggtts](./rnx2cggtts.md) 间接。以上均取自本机 registry 的 `Cargo.toml`。

## 1. 用途与边界

**做：**

- `Epoch` = 内部 `Duration`（i16 世纪 + u64 纳秒）+ `TimeScale` 标签；`==` 比较**同一物理瞬间**（跨时间尺可比）
- 换算：`to_time_scale(TimeScale::GPST)`；GNSS 相关枚举 `GPST/GST/BDT/QZSST/UTC/TAI/TT`（另 ET/TDB/TCG/TCB/TL/TCL）
- 周+周内秒：`to_time_of_week()` / `from_time_of_week(week, ns, ts)`；MJD/JD：`to_mjd_utc_days()`、`to_jde_tt_days()`、`from_mjd_utc()` …
- 解析：`Epoch::from_str("2024-01-01T00:00:30 GPST")`、`"JD …"`/`"MJD …"`；`from_format_str(s, "%Y %m %d %H %M %S.%f")`（RINEX 式空格历元）
- `Duration` 整数纳秒运算（`0.1 s × 3 == 0.3 s` 为真）；`TimeSeries` 等步长迭代；`Polynomial` + `precise_timescale_conversion`（广播 GPST−UTC 等多项式）
- `std`（默认）含 serde；`ut1` / `lts` 需联网下载 IERS 数据（本文未用）

**不做：**

- **不是** 星座/SV 类型 → [gnss-rs](./gnss-rs.md)（`Constellation::timescale()` 只返回本库的 `TimeScale` 标签）
- **没有** GLONASST / IRNSS 时间（IST）枚举：`TimeScale::from_str("GLONASST")`/`"IRNSS"`/`"GLO"`/`"IRN"` → `Err(TimeSystem)`（§3.7）
- **不是** 文件读写（RINEX/SP3/CGGTTS）→ [rinex](./rinex.md) / [sp3](./sp3.md) / [cggtts](./cggtts.md)
- **不是** 定位 / 钟差 / 时间传递**解算**：共视、GPST−UTC(k) 比对 → [rnx2cggtts](./rnx2cggtts.md)（CGGTTS 产出）/ [gnss-rtk](./gnss-rtk.md)（接收机钟差）；本库只做"时间标签的算术"

一句话：`hifitime` = **"这一刻在 GPST/BDT/UTC 下各读几点、差几秒、第几周"**；不碰任何观测值。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `hifitime` | 时间尺/历元/时长库 | `use hifitime::prelude::*` |
| [gnss-rs](./gnss-rs.md) | 星座 → 时间尺**标签**映射 | prelude 重导出 `hifitime::{Epoch, TimeScale}` |
| `chrono` / `time` crate | 民用 UTC/时区日历 | 无 GPST/BDT、无闰秒语义 |
| `anise`（同 nyx-space） | 星历/坐标框架 | 依赖本库，非时间库 |

## 2. 安装

```bash
. "$HOME/.cargo/env"; rustc --version          # 本机 1.98.1
cargo new hf_demo && cd hf_demo
cargo add hifitime                              # → 4.3.1；默认 feature = std（含 serde、web-time）
cargo run -q
# Python（可选）
python3 -m venv hfpy && . hfpy/bin/activate && pip install hifitime   # 本机装到 4.3.1 wheel
```

| feature | 默认 | 作用 |
| --- | --- | --- |
| `std` | ✓ | serde/serde_derive、`web-time`（`Epoch::now()`）、snafu backtrace |
| （关 std） | | `no_std`：`default-features = false` |
| `ut1` | | 从 JPL 下 UT1 数据（需网络，拉 ureq/tabled） |
| `lts` | | = std + ureq + ut1（在线闰秒表） |
| `python` | | pyo3 扩展模块（PyPI 包即此） |

## 3. 可编译小例（本机真跑；2026-09-26 00:36 EDT）

`src/main.rs`（节选；`use hifitime::prelude::*; use std::str::FromStr;`）：

```rust
let t = Epoch::from_gregorian_utc(2024, 1, 1, 0, 0, 0, 0);
for ts in [TimeScale::UTC, TimeScale::TAI, TimeScale::TT, TimeScale::GPST,
           TimeScale::GST, TimeScale::BDT, TimeScale::QZSST] {
    println!("{:>5}: {}", format!("{ts:?}"), t.to_time_scale(ts));
}
// 钟面读数差：把 s 尺下的 Gregorian 读数当 TAI 重建，再减参考
let d = |a: Epoch, s: TimeScale| -> Duration {
    let (y, m, dd, h, mi, se, ns) = a.to_gregorian(s);
    Epoch::from_gregorian(y, m, dd, h, mi, se, ns, TimeScale::TAI)
        - Epoch::from_gregorian(2024, 1, 1, 0, 0, 0, 0, TimeScale::TAI)
};
println!("GPST-UTC = {}", d(t, TimeScale::GPST));
println!("GPST-BDT = {}", d(t, TimeScale::GPST) - d(t, TimeScale::BDT));
let g = t.to_time_scale(TimeScale::GPST);
let (wk, ns) = g.to_time_of_week();
let back = Epoch::from_time_of_week(2295, 86_418 * 1_000_000_000, TimeScale::GPST);
println!("MJD_UTC={} JD_UTC={} JDE_TT={}", t.to_mjd_utc_days(), t.to_jde_utc_days(), t.to_jde_tt_days());
println!("{:?}", Epoch::from_format_str("2024 01 01 00 00 30.0000000", "%Y %m %d %H %M %S.%f"));
for e in TimeSeries::inclusive(start, start + 2.minutes(), 30.seconds()) { /* … */ }
```

### 3.1 同一时刻（2024-01-01T00:00:00 UTC）在各时间尺

```text
  UTC: 2024-01-01T00:00:00 UTC
  TAI: 2024-01-01T00:00:37 TAI
   TT: 2024-01-01T00:01:09.184000000 TT
 GPST: 2024-01-01T00:00:18 GPST
  GST: 2024-01-01T00:00:18 GST
  BDT: 2024-01-01T00:00:04 BDT
QZSST: 2024-01-01T00:00:18 QZSST
GPST-UTC = 18 s
TAI-UTC  = 37 s
TT-UTC   = 1 min 9 s 184 ms
GST-UTC  = 18 s
BDT-UTC  = 4 s
GPST-BDT = 14 s
leap_seconds(iers_only=true) = Some(37.0); leap_seconds_iers = 37
g == t ? true  | b == t ? true
gpst_seconds=1388102418 gst_seconds=768787218 bdt_seconds=567993604
```

- 实测：**GPST−UTC = 18 s**、**TAI−UTC = 37 s**、**TT−TAI = 32.184 s**、**BDT−GPST = −14 s**（BDT 比 GPST 慢 14 s）；GST、QZSST 与 GPST 读数相同（库内三者同偏移）
- `g == t` 为 true：换算不改瞬间，只改显示/算术所用尺
- 零点（本机反推）：`from_gpst_seconds(0)` → `1980-01-06T00:00:00 UTC`；`from_bdt_seconds(0)` → `2006-01-01T00:00:00 UTC`；`from_gst_seconds(0)` → `1999-08-21T23:59:47 UTC`

### 3.2 周 + 周内秒 / MJD / JD

```text
GPST week=2295 tow_ns=86418000000000 tow_s=86418
BDT  week=939 tow_s=86404
GST  week=1271 tow_s=86418
from_time_of_week(2295, 86418 s, GPST) = 2024-01-01T00:00:18 GPST | UTC 2024-01-01T00:00:00 UTC | ==t true
MJD_UTC=60310 MJD_TAI=60310.00042824074 JD_UTC=2460310.5 JDE_TT=2460310.5008007404
from_mjd_utc(60310.5) = 2024-01-01T12:00:00 UTC
day_of_year=1
```

周内秒 86418 = 周一 00:00:18 GPST（GPS 周从周日起）；周数**不回绕**（2295，不是 mod 1024）。**必须先转到 GPST/BDT/GST 再取周**——对 UTC/TAI 历元调用给的是自 1900 起的周：

```text
UTC epoch .to_time_of_week() = (6470, 0)
TAI epoch .to_time_of_week() = (6470, 37000000000)
GPST epoch .to_time_of_week() = (2295, 86418000000000)
from_time_of_week_utc(2295,0) = 1943-12-27T00:00:00 UTC
```

### 3.3 解析：RINEX 式历元 / 带尺字符串

```text
fmt "2024 01 01 00 00 30.0000000" -> Ok(2024-01-01T00:00:30 UTC)
fmt "24  1  1  0  0 30.0000000" -> Ok(2024-01-01T00:00:30 UTC)
parse "2024-01-01T00:00:30 GPST" -> 2024-01-01T00:00:30 GPST (ts=GPST)
parse "2024-01-01T00:00:30.123456789 BDT" -> 2024-01-01T00:00:30.123456789 BDT (ts=BDT)
parse "2024-01-01 00:00:30 GST" -> 2024-01-01T00:00:30 GST (ts=GST)
parse "2024-01-01T00:00:30 QZSST" -> 2024-01-01T00:00:30 QZSST (ts=QZSST)
parse "2024-01-01T00:00:30" -> 2024-01-01T00:00:30 UTC (ts=UTC)
parse "JD 2460310.5 UTC" -> 2024-01-01T00:00:00 UTC (ts=UTC)
parse "MJD 60310.5 TAI" -> 2024-01-01T12:00:00 TAI (ts=TAI)
parse "SEC 0 GPST" -> Err(TimeSystem, parsing from string)
```

- `from_format_str` **不认时间尺**，一律 UTC：RINEX 观测历元（GPST）解析后需 `Epoch::from_gregorian(.., TimeScale::GPST)` 重建，或拼 `" GPST"` 走 `from_str`
- 无尺后缀默认 **UTC**
- 头部字符串：`TimeScale::from_str("GPS")`→`GPST`、`"GAL"`→`GST`、`"BDS"`→`BDT`；`"gpst"`（小写）/`"QZS"`/`"GLO"`/`"IRN"` → `Err(TimeSystem)`
- **陷阱**：`Epoch::from_str("2024-01-01T00:00:30 GPS")` → `Ok(2024-01-01T00:00:12 UTC)`（按 GPST 解释后**换成 UTC 标签**），而 `" GPST"` 保留 GPST 标签

### 3.4 Duration 精度 / 格式化

```text
1ns diff = 1 ns total_ns=1
dur = 1 day 15 h 7 ns | secs=140400.000000007 | ns=140400000000007
0.1s*3 == 0.3s ? true (f64 0.1*3==0.3 ? false)
Duration::from_str("1 d 2 h 3 ns") = Ok("1 day 2 h 3 ns")
rfc3339=2024-01-01T00:00:12.123456789+00:00 iso=2024-01-01T00:00:30.123456 round1s=2024-01-01T00:00:30 GPST floor30s=2024-01-01T00:00:30 GPST
2024 01 01 00 00 30.123456789
```

（后两行输入 `2024-01-01T00:00:30.123456789 GPST`。）`to_rfc3339()` **先换成 UTC**；`to_isoformat()` 保留 GPST 读数但**截到 µs 且丢尺名**；无损写回用 `{}` 或 `Formatter::new(e, Format::from_str("%Y %m %d %H %M %S.%f")?)`。

### 3.5 闰秒边界（2016-12-31T23:59:60 UTC）如实

```text
2016-12-31T23:59:59 UTC -> TAI 2017-01-01T00:00:35 TAI | GPST 2017-01-01T00:00:16 GPST | leap=Some(37.0)
2016-12-31T23:59:60 UTC -> TAI 2017-01-01T00:00:35 TAI | GPST 2017-01-01T00:00:16 GPST | leap=Some(37.0)
2017-01-01T00:00:00 UTC -> TAI 2017-01-01T00:00:37 TAI | GPST 2017-01-01T00:00:18 GPST | leap=Some(37.0)
UTC 23:59:59 -> 00:00:00 elapsed = 1 s
TAI diff = 2 s
GPST same labels elapsed = 1 s
from_gregorian_utc(..,23,59,60,..) = 2016-12-31T23:59:59 UTC
maybe_from_gregorian_utc(..,23,59,60,..) = Ok(2016-12-31T23:59:59 UTC)
maybe 2017-06-30 23:59:60 = Err(InvalidGregorianDate)
```

TAI→UTC 逐秒（`TimeSeries` 1 s）与往返：

```text
2016-12-31T12:00:00 UTC: leap_seconds(true)=Some(36.0) iers=36 TAI=2016-12-31T12:00:36 TAI
2016-12-31T23:59:58 UTC: leap_seconds(true)=Some(37.0) iers=37 TAI=2017-01-01T00:00:34 TAI
2017-01-01T00:00:34 TAI -> 2016-12-31T23:59:57 UTC
2017-01-01T00:00:35 TAI -> 2016-12-31T23:59:58 UTC
2017-01-01T00:00:36 TAI -> 2016-12-31T23:59:59 UTC
2017-01-01T00:00:37 TAI -> 2017-01-01T00:00:00 UTC
2016-12-31T23:59:59 TAI -> 2016-12-31T23:59:23 UTC -> back 2016-12-31T23:59:59 TAI (eq=true)
2017-01-01T00:00:00 TAI -> 2016-12-31T23:59:23 UTC -> back 2016-12-31T23:59:59 TAI (eq=false)
2017-01-01T00:00:35 TAI -> 2016-12-31T23:59:58 UTC -> back 2017-01-01T00:00:34 TAI (eq=false)
2017-01-01T00:00:16 GPST -> 2016-12-31T23:59:58 UTC
2017-01-01T00:00:17 GPST -> 2016-12-31T23:59:59 UTC
```

本机 4.3.1 实测结论：

- **`23:59:60` 不可表示**：解析/构造静默折叠为 `23:59:59`（与之同一 TAI 瞬间），不报错；非闰秒日的 `:60` → `Err(InvalidGregorianDate)`
- **UTC 历元相减不计闰秒**：`00:00:00 − 23:59:59 UTC = 1 s`，真实经过 **2 s**（转 TAI/GPST 再减才对）
- **UTC→TAI 正确**，但 **TAI→UTC 在 `2017-01-01T00:00:00…00:00:36 TAI` 这 37 s 窗口内早 1 s**（推断：闰秒表按 TAI 瞬间切换），往返 `eq=false`；GPST→UTC 同理（`00:00:16 GPST` 应为 `23:59:59 UTC`，给 `23:59:58`）；`leap_seconds()` 在同一窗口已报 37。窗口外往返恒等
- 实务：闰秒附近的历元**全程用 GPST/TAI 存储和相减**，只在最后显示时转 UTC

### 3.6 TimeSeries

```text
#0 2024-01-01T00:00:00 GPST  week=2295 tow=86400
#1 2024-01-01T00:00:30 GPST  week=2295 tow=86430
#2 2024-01-01T00:01:00 GPST  week=2295 tow=86460
#3 2024-01-01T00:01:30 GPST  week=2295 tow=86490
#4 2024-01-01T00:02:00 GPST  week=2295 tow=86520
exclusive count = 4
```

`inclusive` 含端点（5 个），`exclusive` 不含终点（4 个）；步长 `30.seconds()` 即 RINEX 30 s 采样。

### 3.7 非法输入（如实）

```text
bad "2024-13-01T00:00:00 UTC" -> Err(InvalidGregorianDate)
bad "2024-02-30T00:00:00 UTC" -> Err(InvalidGregorianDate)
bad "2024-01-01T25:00:00 UTC" -> Err(Parse { source: ValueError, details: "invalid hour" })
bad "2024-01-01T00:00:00 GLONASST" -> Err(Parse { source: TimeSystem, details: "parsing as Gregorian date with time scale" })
bad "2024-01-01T00:00:00 IRNSS" -> Err(Parse { source: TimeSystem, details: "parsing as Gregorian date with time scale" })
bad "garbage" -> Err(Parse { source: UnknownFormat, details: "invalid year" })
bad "" -> Err(Parse { source: UnknownFormat, details: "less than 7 characters" })
bad fmt -> Err(Parse { source: UnexpectedCharacter { found: '/', option1: Some(' '), option2: None }, details: "when parsing from format string" })
TimeScale::from_str GLO/IRN: Err(TimeSystem) Err(TimeSystem) Ok(BDT)
```

全部返回 `Err`，**未见 panic**（含空串，对比 gnss-rs `SV::from_str("")` panic）。

**与 [gnss-rs](./gnss-rs.md) 映射交叉**：gnss-rs 2.7.0 `Constellation::timescale()` 给 GPS→`GPST`、Galileo→`GST`、BeiDou→`BDT`、QZSS→`QZSST`、SBAS→`GPST`、**Glonass→`UTC`**、**IRNSS→`None`**——正因本库无 GLONASST/IST 枚举。GLONASST = UTC(SU)+3 h，按 UTC 处理时需自行 +3 h；IRNSS 时间需上层自理（以 IRNSS ICD 为准）。

### 3.8 Python 绑定（pip 4.3.1，本机真跑）

```python
from hifitime import Epoch, TimeScale, Duration, TimeSeries
e = Epoch("2024-01-01T00:00:00 UTC")
for ts in [TimeScale.GPST, TimeScale.GST, TimeScale.BDT, TimeScale.TAI, TimeScale.TT, TimeScale.QZSST]:
    print(ts, e.to_time_scale(ts))
print("tow", e.to_time_scale(TimeScale.GPST).to_time_of_week())
print(Epoch("2024-01-01T00:00:30.123456789 BDT") - Epoch("2024-01-01T00:00:30 BDT"))
for t in TimeSeries(Epoch("2024-01-01T00:00:00 GPST"), Epoch("2024-01-01T00:01:00 GPST"), Duration("30 s"), True):
    print(t)
```

```text
TimeScale.GPST 2024-01-01T00:00:18 GPST
TimeScale.GST 2024-01-01T00:00:18 GST
TimeScale.BDT 2024-01-01T00:00:04 BDT
TimeScale.TAI 2024-01-01T00:00:37 TAI
TimeScale.TT 2024-01-01T00:01:09.184000000 TT
TimeScale.QZSST 2024-01-01T00:00:18 QZSST
tow (2295, 86418000000000)
mjd_utc 60310.0 jde_utc 2460310.5
leap 37.0
123 ms 456 μs 789 ns
2024-01-01T00:00:00 GPST
2024-01-01T00:00:30 GPST
2024-01-01T00:01:00 GPST
HifitimeError TimeSystem, parsing as Gregorian date with time scale
```

与 Rust 结果一致；`TimeSeries(start, end, step, inclusive)` 第 4 参为布尔；非法尺抛 `HifitimeError`。

## 4. I/O 与关键 API

| API | 输入 → 输出 |
| --- | --- |
| `Epoch::from_str(s)` | `"YYYY-MM-DDThh:mm:ss[.f] TS"` / `"JD x TS"` / `"MJD x TS"`；无 TS = UTC；`"GPS"` 后缀→UTC 标签 |
| `Epoch::from_format_str(s, fmt)` | strftime 式（`%Y %m %d %H %M %S.%f`、`%y`）→ **UTC** |
| `Epoch::from_gregorian(y,m,d,h,mi,s,ns, ts)` / `from_gregorian_utc` | 构造；`:60` 折叠 |
| `e.to_time_scale(ts)` | 同瞬间换标签 |
| `e.to_gregorian(ts)` | `(i32,u8,u8,u8,u8,u8,u32)` 钟面读数 |
| `e.to_time_of_week()` / `Epoch::from_time_of_week(w, ns, ts)` | `(u32 周, u64 纳秒)`；按 `e` 自身尺 |
| `to_gpst_seconds` / `to_gst_seconds` / `to_bdt_seconds` | 自各系统零点的 f64 秒 |
| `to_mjd_utc_days` / `to_jde_utc_days` / `to_jde_tt_days` / `from_mjd_utc` | f64 天 |
| `e.leap_seconds(iers_only)` / `leap_seconds_iers()` | `Option<f64>` / `i32` |
| `a - b` | `Duration`（按 `a` 的尺算；UTC 相减不含闰秒） |
| `Duration`：`30.seconds()`、`1.5.days()`、`Duration::from_str("1 d 2 h")` | `total_nanoseconds()` → i128 |
| `TimeSeries::inclusive/exclusive(start, end, step)` | `Iterator<Item=Epoch>` |
| `e.round(d)` / `e.floor(d)` | 对齐采样格点 |
| `precise_timescale_conversion(forward, ref, Polynomial, target)` | 广播 a0/a1/a2 修正 |

## 5. 接到哪步

```text
hifitime（Epoch + TimeScale）
  → gnss-rs：Constellation/SV → TimeScale 标签（Glonass→UTC、IRNSS→None）
  → rinex / sp3 / binex：文件历元字段均为 hifitime::Epoch
  → gnss-rtk：解算历元、接收机钟差（时间以 hifitime 计）
  → cggtts / rnx2cggtts：CGGTTS 跟踪历元（MJD + STTIME）、共视时间传递
  → TEC/电离层：只用到历元对齐，不参与解算
```

交叉：[gnss-rs](./gnss-rs.md) · [rinex](./rinex.md) · [sp3](./sp3.md) · [cggtts](./cggtts.md) · [rnx2cggtts](./rnx2cggtts.md) · [gnss-rtk](./gnss-rtk.md) · [binex](./binex.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 周数 6470、周内秒不对 | `to_time_of_week()` 用历元**自身**尺（UTC/TAI 自 1900） | 先 `.to_time_scale(TimeScale::GPST)` |
| 2 | RINEX 历元解析后差 18 s | `from_format_str` 一律 UTC | 用读数 `from_gregorian(.., GPST)` 重建 |
| 3 | `"… GPS"` 解析结果是 UTC 标签 | 解析后转 UTC | 用 `"GPST"` 后缀；头部用 `TimeScale::from_str("GPS")` |
| 4 | 跨闰秒 UTC 相减少 1 s | UTC 相减不计闰秒 | 先转 TAI/GPST 再减 |
| 5 | `23:59:60` 被吞成 `23:59:59` | 无法表示闰秒那一秒 | 闰秒秒内数据保留原始 GPST 历元 |
| 6 | 闰秒后 37 s（TAI）/18 s（GPST）内转 UTC 早 1 s、往返不等 | 4.3.1 实测（推断闰秒表按 TAI 瞬间切换） | 该窗口内不转 UTC；或自行用 `leap_seconds` 校核 |
| 7 | `GLONASST`/`IRNSS` 解析失败 | 无该枚举 | 与 gnss-rs 一致：GLO 按 UTC(+3 h 自理)，IRNSS 自理 |
| 8 | `to_isoformat()` 丢纳秒和尺名 | 截 µs、无后缀 | 写盘用 `{}` 或 `Formatter` |
| 9 | `to_rfc3339()` 时间"变了" | 先转 UTC 再输出 | 需要 GPST 读数用 `{}` |
| 10 | 依赖树里多份 hifitime | 下游声明 `^4.1`/`^4.2`；若另有依赖仍锁 3.x 会并存两份 | `cargo tree -i hifitime`；`cargo update -p hifitime` |
| 11 | `ut1`/`lts` 构建/运行时报网络错误 | 需下载 IERS/JPL 数据 | 离线只用默认 `std` |
| 12 | 当时间传递/定位解算库用 | 只做时间算术 | 见 §5：rnx2cggtts / gnss-rtk |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust 中 GPST/GST/BDT/UTC/TAI/TT 换算、周+周内秒、MJD | **hifitime（本文）** |
| Python 同上（纳秒、闰秒） | `pip install hifitime`（§3.8） |
| 星座/SV → 时间尺标签 | [gnss-rs](./gnss-rs.md) |
| 读写 RINEX / SP3 / CGGTTS | [rinex](./rinex.md) / [sp3](./sp3.md) / [cggtts](./cggtts.md) |
| RINEX→CGGTTS 共视时间传递 | [rnx2cggtts](./rnx2cggtts.md) |
| 接收机钟差 / 定位解算 | [gnss-rtk](./gnss-rtk.md) / [rtklib](./rtklib.md) |
| 民用时区日历 | chrono / Python `datetime`（无 GNSS 尺） |

相关：上游 README · docs.rs `hifitime` · [gnss-rs](./gnss-rs.md) · [rinex](./rinex.md) · [sp3](./sp3.md) · [cggtts](./cggtts.md) · [data-access](../data-access.md)
