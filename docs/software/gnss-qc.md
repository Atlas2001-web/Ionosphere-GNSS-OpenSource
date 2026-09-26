# gnss-qc · Rust GNSS 数据质检（QC）上下文 + HTML 报告库操作手册

目录：上游 <https://github.com/nav-solutions/gnss-qc>（旧址 `rtk-rs/gnss-qc` **301** 跳转）· crates.io **`gnss-qc` 0.4.0**（2025-06-15 发布；tag **`v0.4.0`=`fe2d376`**；main **`3ee5918`**，2025-10-05 12:57 EDT，领先 tag **5** 提交，仓内仍标 0.4.0）· **MPL-2.0** · ★**1** · MSRV **1.82**（`package.metadata`）· **无 [[bin]]**（纯库）· 本机 **rustc 1.98.1**（2026-09-26 00:40–00:54 EDT 真跑）· **未登记** `PROJECTS.json`

> 岗位：nav-solutions 生态的 **QC 引擎**：把 OBS/NAV/CLK/ATX/METEO RINEX + SP3 装进一个 `QcContext`，判定能否 SPP/CPP/PPP，渲染 **HTML** 报告（maud + plotly）。冲突时：**docs.rs / 上游源码 > 本文**。  
> 名字谱系：`rinex-qc`（georust/rinex 工作区，停在 **0.2.0-alpha-1**，2024-09-04）→ 拆出为 **`gnss-qc`**（0.0.2 于 2025-02-18，被 [rinex-cli](./rinex-cli.md) 0.12.1 依赖）→ 0.1–0.4。共享 trait 同步改名：`rinex-qc-traits`（0.2.0）→ **`gnss-qc-traits`**（仓 `nav-solutions/qc-traits`，crates 最新 **0.5.0**，2026-09-08）。报告菜单至今仍印 **`RINEX-QC v0.4.0`**，链接指向 georust/rinex。

## 1. 用途与边界

**做：**

- `QcContext`：按产品类型（Observation / BroadcastNavigation / HighPrecisionClock / ANTEX / MeteoObservation / HighPrecisionOrbit）归档；同类文件 **`merge_mut` 合并**
- 兼容性判定：`is_navigation_compatible()`（OBS+NAV）/ `is_cpp_…` / `is_ppp_…` / `is_ppp_ultra_…`（需 CLK 与 OBS 同步）
- `QcReport::new(&ctx, QcConfig)` → `render().into_string()` 得整页 HTML：`Summary`（轻）或 `Full`（每星座 × 每信号：采样、缺口、卫星列表、观测时序图；SP3 头信息）
- 预处理 trait 经 prelude 重导出（来自 `gnss-qc-traits`）：`Filter`/`Preprocessing`/`Repair`/`Timeshift`/`TimeCorrectionsDB`
- `navigation` feature：接 ANISE 做后处理导航（本文**未测**）

**不做：**

- **不是** 定位解算器 → [gnss-rtk](./gnss-rtk.md)（gnss-qc 的 `navigation` 只是编排）
- **不是** TEC / 电离层产品 → [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) / [ionex-rs](./ionex-rs.md)；报告里 "Ionosphere Bias" 只是"能否双频消电离层"的勾
- **不是** teqc 式 MP1/MP2、周跳计数、SNR 统计表：0.4.0 的 SNR 只画时序图，多路径图**未填数据**（§6 坑 5）
- **不是** 文件解析器本身 → [rinex](./rinex.md) / [sp3](./sp3.md)；**不是** CLI → [rinex-cli](./rinex-cli.md)

一句话：`gnss-qc` = **"这包文件齐不齐、能做什么"的 HTML 体检单**；QC ≠ 定位 ≠ TEC。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `gnss-qc` | QC 上下文 + HTML 报告库 | `use gnss_qc::prelude::*` |
| `rinex-qc` | 旧名，停更 | crates 0.2.0-alpha-1，repo georust/rinex |
| `gnss-qc-traits` | 共享 trait（Merge/Filter/Timeshift/Decimate/Split/Masking） | 被 rinex、sp3、gnss-qc 共同依赖 |
| crates.io `antex` | **无关**（EngosSoftware 终端样式库） | ANTEX 解析在 [rinex](./rinex.md) 的 `antex` feature |
| [rinex-cli](./rinex-cli.md) | CLI 外壳 | 0.12.1 依赖 `gnss-qc 0.0.2`；tip 0.13.0 依赖 gnss-qc git rev `8265828` |

## 2. 安装（版本锁是关键）

`cargo add gnss-qc` 在 2026-09 **编不过**：0.4.0 要 `rinex ^0.20`（解析到 0.20.2），而 cargo 同时选中 `gnss-rs 2.7.0`，该版起 `Constellation` 去掉了 `UpperHex`：

```text
error[E0277]: the trait bound `gnss::constellation::Constellation: UpperHex` is not satisfied
  --> …/rinex-0.20.2/src/navigation/ionosphere/nequick_g.rs:87:13
error: could not compile `rinex` (lib) due to 3 previous errors
```

本机逐级试：`gnss-rs` 2.7.0 ✗、2.6.0 ✗、**2.5.0 ✓**。而 `sp3 1.4.1` → `gnss-qc-traits 0.4.1` → `gnss-rs ^2.6`，所以还得把 sp3 压到 **1.3.0**：

```toml
[dependencies]
gnss-qc = "0.4.0"
# gnss-rs>=2.6 删了 Constellation 的 UpperHex，rinex 0.20.2 编不过
gnss-rs = "=2.5.0"
sp3 = "=1.3.0"
```

实锁：`gnss-qc 0.4.0` + `rinex 0.20.2` + `sp3 1.3.0` + `gnss-qc-traits 0.3.2` + `gnss-rs 2.5.0` + `hifitime 4.3.1`；`cargo build --release` 冷编 **2 m 22 s**，二进制 **4266328** B。

main（`3ee5918`，git 依赖 rinex rev `a10b41a`=0.22.0 系 + sp3 `0ac81cf`=1.4.1）同病：直接编同一 E0277；`cargo update -p gnss-qc-traits --precise 0.4.0 && cargo update -p gnss-rs --precise 2.5.0` 后通过（冷编 **3 m 29 s**），下文 ESBC 输出与 crates 版**逐字相同**。rinex-cli tip 的 `Cargo.toml` 用 `ssh://git@github.com/nav-solutions/gnss-qc.git`，无 SSH key 拉不下。

Features：默认 `sp3` + `flate2`（`.gz` 直读）；`navigation`（anise + log）；`embed_ephem`（离线 ANISE 星历）；`plot` 已注释掉（但 plotly 是**硬依赖**，Full 报告照样出图）。仓库**无** `examples/`；`src/tests` 依赖 `data` 子模块（`rtk-rs/data`），crates 包不含数据。

## 3. 可编译小例（本机真跑）

`src/main.rs`（按扩展名选加载函数，打印上下文，再各渲染一次 Summary/Full）：

```rust
use gnss_qc::prelude::*;

fn main() -> Result<(), Error> {
    let mut ctx = QcContext::new();
    for f in std::env::args().skip(1) {
        let up = f.to_uppercase();
        let r = if f.ends_with(".gz") && up.contains(".SP3") { ctx.load_gzip_sp3_file(&f) }
            else if f.ends_with(".gz") { ctx.load_gzip_rinex_file(&f) }
            else if up.ends_with(".SP3") { ctx.load_sp3_file(&f) }
            else { ctx.load_rinex_file(&f) };
        match r { Ok(()) => println!("load OK  {f}"), Err(e) => println!("load ERR {f}  -> {e}") }
    }
    println!("name={} timescale={:?}", ctx.name(), ctx.timescale());
    println!("obs={} brdc={} sp3={} sp3_clk={}", ctx.has_observation(),
        ctx.has_brdc_navigation(), ctx.has_sp3(), ctx.sp3_has_clock());
    println!("nav_compat={} cpp={} ppp={} ppp_ultra={}", ctx.is_navigation_compatible(),
        ctx.is_cpp_navigation_compatible(), ctx.is_ppp_navigation_compatible(),
        ctx.is_ppp_ultra_navigation_compatible());
    if let Some(obs) = ctx.observation() {
        println!("obs epochs={} sv={} first={:?} last={:?}", obs.epoch_iter().count(),
            obs.sv_iter().count(), obs.first_epoch(), obs.last_epoch());
    }
    for (kind, tag) in [(QcReportType::Summary, "summary"), (QcReportType::Full, "full")] {
        let html = QcReport::new(&ctx, QcConfig::default().with_report_type(kind))
            .render().into_string();
        std::fs::write(format!("qc_{tag}.html"), &html).unwrap();
        println!("qc_{tag}.html -> {} bytes", html.len());
    }
    Ok(())
}
```

### 3.1 ESBC OBS + NAV + GRG SP3（2020-06-25，DOY 177）

输入：`ESBC00DNK_R_20201770000_01D_30S_MO.rnx`（**34573249** B，已 CRX→RNX）+ `ESBC00DNK_R_20201770000_01D_MN.rnx.gz`（285554 B）+ `GRG0MGXFIN_20201770000_01D_15M_ORB.SP3.gz`（198794 B）——与 [rnx2cggtts](./rnx2cggtts.md)/[sp3](./sp3.md) 同批。

```text
load OK  …/ESBC00DNK_R_20201770000_01D_30S_MO.rnx
load OK  …/ESBC00DNK_R_20201770000_01D_MN.rnx.gz
load OK  …/GRG0MGXFIN_20201770000_01D_15M_ORB.SP3.gz
name=ESBC00DNK_R_20201770000_01D_30S_MO timescale=Some(GPST)
obs=true brdc=true sp3=true sp3_clk=true
nav_compat=true cpp=true ppp=true ppp_ultra=false
obs epochs=2880 sv=113 first=Some(2020-06-24T23:59:42 UTC) last=Some(2020-06-25T23:59:12 UTC)
qc_summary.html -> 6849 bytes
qc_full.html -> 72308856 bytes
```

另加计时版实测：加载 OBS **450 ms** / NAV 59 ms / SP3 17 ms；Summary **559 ms**；Full **20609 ms**；墙钟 **22.3 s**（两次运行 Summary 逐字节相同）。`first` 印成 UTC 23:59:42 是 hifitime `Debug` 换算：GPST 00:00:00 − 18 s，见 [hifitime](./hifitime.md)。

**Summary（6849 B）** 去标签后的全部文字 + 图标颜色：

| 项 | 值 |
| --- | --- |
| Timescale | GPST |
| Compliancy | NAVI ✓ · CPP ✓ · PPP ✓ · **PPP (Ultra) ✗**（tooltip：`CLK RINEX is not synchronous to OBS RINEX`——实际是**没给** CLK） |
| Troposphere Bias → Model optimization | ✗（`missing Meteo IONEX`，原文如此） |
| Ionosphere Bias → Model optimization / Cancelling | ✗（需 IONEX）/ ✓（双频直接消） |

**Full（72308856 B ≈ 69 MiB）**：`<script>` **88** 个、`Plotly.newPlot` **84** 处（数据全内嵌）。去掉脚本后文字 14323 字符，关键字段：

| 块 | 实际输出 |
| --- | --- |
| OBS Sampling | 2020-06-25T00:00:00 GPST → 23:59:30 GPST · 23 h 59 min 30 s · 30 s · 0.033 Hz · **No gaps detected** |
| 星座 / 卫星（OBS） | BDS **29**（C05…C37）· GPS **31**（缺 G23）· Glonass **23**（R01…R24，缺 R22）· Galileo **22** · QZSS J01–J03 · EGNOS S23/S26/S36 · BDSBAS S44 · SDCM S25 → 合计 **113** = `sv_iter().count()` |
| 信号 | GPS L1/L2/L5 · BDS B1/B2/B3 · Glonass **`G1(None), G2(None)`**, G3 · EGNOS L1/L5 |
| 缺口示例 | BDSBAS S44：**8** Data gaps，最长 12 h 2 min（起 10:25:00 GPST），共 1279 历元；SDCM S25：4 gaps，最长 5 min；QZSS L5：11 gaps |
| 每信号 Epochs | **`SPP Compatible 0/2880 (0%)`**，CPP/PPP 同为 0%——所有信号皆如此（§6 坑 4） |
| 图 | SSI（`Power [dB]`，即 SNR）/ Doppler / Phase / Pseudo Range 四类时序；trace 名如 `C05(S2I)` |
| NAV | 各星座卫星列表；Galileo **24**（比 OBS 多 E14/E18），其余与 OBS 同 |
| SP3 | revision `c` · Agency GRGS · MIXED · GPST · **IGb14** · Orbit FIT · 00:00 → 23:45 GPST · 15 min · No gaps |

### 3.2 其它组合

| 输入 | 结果 |
| --- | --- |
| 仅 `ESBC…MO.crx.gz`（CRINEX+gzip 直读） | load **1841 ms**；epochs 2880/sv 113；`nav_compat=false cpp=true ppp=true`；Summary **6930** B |
| ESBC OBS + ACOR OBS（2021-12-21，另一站） | **两者都 OK 并被合并**：epochs **2905**（2880+25）/sv **118**/last=2021-12-21；name 仍是 ESBC；Full **72707270** B/**34.7 s** |
| 空上下文（无参数） | `name=Undefined timescale=None`，全 false；Summary=Full=**7061** B，exit 0 |

### 3.3 失败边界（原样 stdout/stderr）

```text
$ gqcdemo /nope/X.rnx            # exit 101
thread 'main' panicked at …/rinex-0.20.2/src/lib.rs:886:35:
from_file: open error: Os { code: 2, kind: NotFound, message: "No such file or directory" }

$ gqcdemo /nope/X.SP3            # exit 101
thread 'main' panicked at …/sp3-1.3.0/src/parsing.rs:61:55:
File open error: No such file or directory (os error 2)

$ echo hello > bad.rnx && gqcdemo bad.rnx          # exit 0，上下文为空
load ERR bad.rnx  -> RINEX parsing error: OBS RINEX invalid timescale

$ cp GRG0MGXFIN_…ORB.SP3 grg.txt && gqcdemo grg.txt  # SP3 走错入口，同一句
load ERR grg.txt  -> RINEX parsing error: OBS RINEX invalid timescale
```

## 4. I/O 与关键 API

| 入口 | 输入 | 输出 / 失败 |
| --- | --- | --- |
| `load_rinex_file(p)` | 明文 RINEX / CRINEX | `Err(RinexParsing)`；**文件不存在 → panic** |
| `load_gzip_rinex_file(p)` | `.rnx.gz`/`.crx.gz` | 同上 |
| `load_sp3_file` / `load_gzip_sp3_file` | SP3 a/c/d | `Err(SP3Parsing)`；不存在 → panic |
| `load_rinex(p, Rinex)` / `load_sp3(p, SP3)` | 已解析对象 | 同类型时 `merge_mut` |
| `QcReport::new(&ctx, cfg)` | `QcConfig { report: Summary \| Full }` | `render()` → `maud::Markup`；`into_string()` 得 HTML |
| `QcReportType::from_str` | `sum`/`summ`/`summary`/`full` | 其它 → `InvalidReportType` |
| `ctx.filter_mut(&Filter)` / `repair_mut(Repair)` / `timescale_transposition_mut(ts)` | qc-traits 预处理 | 就地改上下文 |
| `add_chapter(QcExtraPage)` | 自定义 HTML 页 | 挂到菜单 |

HTML 引用外部 CDN（Bulma、Font Awesome、plotly JS）；离线打开样式/图会缺。

## 5. 接到哪步

```text
下载/解压 → [crx2rnx]/[gfzrnx] → gnss-qc 体检（本文，或 rinex-cli 外壳）
          → 齐：gnss-rtk / rtklib 定位；georinex / pytecgg 算 TEC
          → 不齐：补 NAV/SP3/CLK，或换站/换日
```

交叉：[rinex](./rinex.md)（解析，ANTEX 也在此）· [rinex-cli](./rinex-cli.md)（CLI；其 HTML 标 `RINEX-QC v0.0.2` 即本库早期版）· [sp3](./sp3.md) · [gnss-rs](./gnss-rs.md) · [hifitime](./hifitime.md) · [gnss-rtk](./gnss-rtk.md)。

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `cargo add gnss-qc` 后 rinex 报 `UpperHex` E0277 | gnss-rs ≥2.6 去掉该 trait；rinex 0.20.2 仍用 `{:X}` | 锁 `gnss-rs = "=2.5.0"` + `sp3 = "=1.3.0"`（§2） |
| 2 | 想配最新 rinex 0.22 / sp3 1.4 | crates 0.4.0 要 `rinex ^0.20`、`gnss-qc-traits ^0.3.1` | 用 git main + `gnss-qc-traits 0.4.0` + `gnss-rs 2.5.0`；或等新发版 |
| 3 | 缺文件进程直接 exit **101** | rinex 0.20.2 `lib.rs:886` / sp3 1.3.0 `parsing.rs:61` 对 open 失败 `panic!` 而非 `Err` | 调用前 `Path::exists()` |
| 4 | 每信号 `SPP Compatible 0/2880 (0%)` | 0.4.0 `report/rinex/obs.rs` 里计数代码被注释，恒 0；星座级 SPP/CPP/PPP 勾也是 `false // TODO` | 以 Summary 的 Compliancy 或 `ctx.is_*_compatible()` 为准 |
| 5 | 以为有多路径 / SNR 统计 | `Code Multipath` 图创建后从不加 trace（HTML 里 `code_mp` **0** 处）；SSI 只有时序图 | MP/SNR 统计用 [teqc](./teqc.md) `+qc` / [anubis](./anubis.md) / [gnss-multipath-analysis](./gnss-multipath-analysis.md) |
| 6 | 两个不同测站被合成一个 OBS | 同产品类型一律 `merge_mut`，不查 MARKER | 一站一 `QcContext` |
| 7 | 纯文本 / SP3 误传给 `load_rinex_file` | 报 `RINEX parsing error: OBS RINEX invalid timescale`（误导性） | 先按扩展名/首行分流 |
| 8 | Full 报告 69 MiB、20 s | 84 张 plotly 图数据全内嵌 | 批量巡检用 `Summary`（≈7 KB、<1 s） |
| 9 | Glonass 信号印 `G1(None)` | FDMA 频道号未从 NAV/头部带入 | 只作展示瑕疵 |
| 10 | 报告写 `RINEX-QC`、链接 georust | 历史名残留 | 以本仓/crates 名 `gnss-qc` 为准 |
| 11 | `PPP (Ultra) ✗` 提示 CLK 不同步 | 未载入 CLK 时也显示此句 | 真要 Ultra 就加同日 `.CLK` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| Rust 程序内嵌 QC、输出 HTML | **本文** |
| 命令行一把出报告 / 文件手术 | [rinex-cli](./rinex-cli.md)（外壳，内核即 gnss-qc） |
| 经典 MP1/MP2、周跳、完整性百分比 | [teqc](./teqc.md)（EOL）/ [anubis](./anubis.md)（XTR；本文只给"能不能用"的粗勾） |
| RINEX 拼接/抽稀/检查 | [gfzrnx](./gfzrnx.md) |
| Python 读 OBS 自己统计 | [georinex](./georinex.md) / [gnss_lib_py](./gnss_lib_py.md) |
| 定位 | [gnss-rtk](./gnss-rtk.md) / [rtklib](./rtklib.md) |
| TEC | [gnss-tec](./gnss-tec.md) / [pytecgg](./pytecgg.md) |

## 8. 相关

[rinex.md](./rinex.md) · [rinex-cli.md](./rinex-cli.md) · [sp3.md](./sp3.md) · [gnss-rs.md](./gnss-rs.md) · [hifitime.md](./hifitime.md) · [gnss-rtk.md](./gnss-rtk.md) · [teqc.md](./teqc.md) · [anubis.md](./anubis.md) · [docs.rs/gnss-qc](https://docs.rs/gnss-qc) · [README.md](./README.md)
