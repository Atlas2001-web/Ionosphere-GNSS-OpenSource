# sgp4-rs · Rust `sgp4` crate（TLE/OMM → TEME）操作手册

目录：`PROJECTS.json` **`sgp4-rs`**（orbit-clock / SGP4-Rust）· 上游 <https://github.com/neuromorphicsystems/sgp4>（Western Sydney 大学 ICNS）· crates.io **`sgp4` 2.4.0**（2026-02-23 发布 = tag `2.4.0` = master **`66b6318`**）· **MIT** · ★**120** · 本机 rustc/cargo **1.98.1**，依赖锁定 chrono 0.4.45 / serde 1.0.229 / serde_json 1.0.151 · 真跑 2026-09-26 02:57–03:00 EDT

> 岗位：纯 Rust（可 `no_std`）的 SGP4/SDP4，把 **TLE / OMM(JSON)** 传播成 **TEME** 位置（km）/速度（km/s）。精度仍是 **km 级**（GPS 对 IGS SP3 中位 ~1.7 km），**不是**精密轨道。冲突时：**docs.rs / 上游 README > 本文**。
> 姊妹篇：[python-sgp4](./python-sgp4.md)（本文 §3.2 与之差 **≤ 9 µm**）、[satellite-js](./satellite-js.md)（JS 版）；严格 IERS 帧/SP3 插值：[orekit](./orekit.md)；Rust 数值积分：[nyx](./nyx.md)（nyx 无 SGP4）；精密轨道下载：[data-access · SP3](../data-access.md#sp3--clk--bias)。

## 1. 用途与边界

**做：** `Elements::from_tle` / `parse_2les` / `parse_3les` / `serde_json` 读 OMM → `Constants::from_elements(...)` → `constants.propagate(MinutesSinceEpoch(t))` 得 `Result<Prediction, Error>`；AFSPC 兼容模式；`propagate_from_state` 保留深空共振积分状态；上游称支持 `no_std`（无 alloc 也能解析 TLE+传播，本文未测）。

**不做：**

- **不做坐标转换**：只有 TEME。ITRS/ECEF、经纬高、仰角要自己接（本文 §3.3 用 astropy）
- **不拉数据、不读 XML/KVN/CSV OMM**：只有 JSON（serde）和 TLE
- **不算时间尺度**：输入是 `chrono::NaiveDateTime` 当 UTC，`datetime_to_minutes_since_epoch` 明写"不考虑闰秒"；SP3（GPST）要自己 −18 s
- **不报"已衰减"**：没有 python-sgp4 的 error 6（§7 坑 3）
- **默认常数是 WGS84**，不是 CelesTrak/python-sgp4 的 WGS72（§7 坑 1）

## 2. 安装

```bash
cargo new sgp4cmp && cd sgp4cmp
cargo add sgp4@2.4.0 serde_json chrono     # 默认 feature: alloc, std, serde（serde 才有 OMM）
cargo build --release                      # 本机冷编译 9.2 s（含依赖）；target 52 MB，CARGO_HOME 15 MB；二进制 0.85 MB
```

`no_std`：`default-features = false, features = ["libm"]`（未测）。

本文所有数字来自一个自写 CLI `sgp4cmp`（`teme` / `sp3` / `bench` / `tle` / `life` / `ver` 六个子命令，约 170 行）。核心四行：

```rust
let elements = sgp4::parse_3les(&txt)?;                      // 或 serde_json::from_str::<Vec<sgp4::Elements>>(&json)?
let c = sgp4::Constants::from_elements(&elements[i])?;        // ⚠ WGS84；要对齐 CelesTrak 用下面的 WGS72 写法
let m = elements[i].datetime_to_minutes_since_epoch(&utc)?;   // NaiveDateTime（UTC），纳秒整数差
let p = c.propagate(m)?;                                      // p.position [km] / p.velocity [km/s]，TEME
```

对齐 python-sgp4 默认（WGS72 + improved 模式）：

```rust
sgp4::Constants::new(sgp4::WGS72, sgp4::iau_epoch_to_sidereal_time, e.epoch(), e.drag_term,
    sgp4::Orbit::from_kozai_elements(&sgp4::WGS72, e.inclination*D2R, e.right_ascension*D2R, e.eccentricity,
        e.argument_of_perigee*D2R, e.mean_anomaly*D2R, e.mean_motion*(PI/720.0))?)?
```

## 3. 真命令 + 实测输出（2026-09-26 EDT）

输入与 [python-sgp4](./python-sgp4.md) 完全相同：`/workspace/sgp4work` 里 2026-09-26 02:09 EDT 从 CelesTrak 抓的 `gps-ops.tle`（32 星）/`gps-ops.json`（OMM）/`iss.tle`，以及 IGS `IGS0OPSULT_20262680000_02D_15M_ORB.SP3`（BKG 镜像）。

### 3.1 传播

```bash
sgp4cmp teme iss.tle ISS wgs72 2026-09-26T00:00:00
sgp4cmp teme gps-ops.tle "PRN 02" wgs72 2026-09-26T00:00:00 2026-09-26T06:00:00
```

```
ISS   t=817.9351920min  r= -949.485596 4511.500075 -5001.757253   v= -7.322557177 0.764630116 2.076133336
PRN02 t=1347.0572304min r= 18021.574980 -18486.667125 -4235.878206 v= 2.017883433 1.198689134 3.155333530
PRN02 t=1707.0572304min r= -18241.277918 19245.665147 4873.354746 v= -1.977397925 -1.143054481 -3.057086236
```

（显示截到 mm；与 python-sgp4 手册 §3.2 同时刻逐位一致。）同一命令换 `default`（`from_elements`，WGS84）：PRN02 `r= 18021.584106 -18486.650601 -4235.851255`，差 ~33 m。

### 3.2 与 python-sgp4 2.27 在 TEME 比（本人比对）

`sgp4cmp sp3 ... <mode> 18` 在 SP3 的 192 个历元（GPST−18 s = UTC）× 32 星输出 TEME CSV，Python 侧 `Satrec.sgp4(jd, fr)` 同时刻算：

```
wgs72   vs python (TLE): n=6144 |dr| median=4.2e-06 m  max=8.8e-06 m  (PRN02 max 8.6e-06)  |dv| max=1.9e-09 m/s
afspc   vs python (TLE): n=6144 |dr| max=8.6e-06 m     （GPS 倾角 55°，不走 Lyddane 分支，两模式相同）
default vs python (TLE): n=6144 |dr| median=26.9 m  max=34.1 m   |dv| max=3.4e-03 m/s   ← WGS84 vs WGS72
OMM wgs72 vs python OMM: n=6144 |dr| median=5.6e-07 m max=1.39e-03 m（G20；EPOCH 微秒解析差）
```

结论：**配成 WGS72 时与 python-sgp4 是 µm 级**（CSV 只保留到 1e-9 km，已到分辨率），远优于预期的 mm。

### 3.3 PRN 02 对 IGS SP3（本人比对，非上游数字）

TEME → **astropy 8.0.1** `TEME→ITRS`（IERS-A）→ 与 SP3 前 24 h（96 历元）逐历元 3D 差：

```
wgs72  PRN02: mean=0.534 rms=0.551 min=0.316 max=0.828 km | 31 星 mean3D 中位 1.658 km，min 0.302，max 469.612（G13）
default(WGS84) PRN02: mean=0.517 rms=0.534 max=0.802 km   | 31 星中位 1.658 km
OMM    PRN02: mean=0.533 rms=0.551 max=0.826 km
WRONG  leap=0（GPST 当 UTC）: mean=53.489 km；WRONG TEME 当 ECEF: mean=26974.176 km
```

与 python-sgp4 手册的 0.534 km 完全一致。WGS84 这次"好 17 m"只是巧合：TLE 是按 WGS72 拟合的，别据此改常数。

### 3.4 深空（SDP4）：官方 33 组校验 TLE

`ver.py` 把 `SGP4-VER.TLE` 逐组送 `sgp4cmp ver l1 l2 start stop step <mode>`，对 `tcppver.out`（Vallado C++，**improved 模式** + WGS72，8 位小数）：

```
wgs72(improved): 近地 9 星 max|dr|=7.7e-06 m；深空 24 星 max|dr|=4.2e-03 m（23333，e=0.97、周期 13.7 d）
                 GPS 类 12 h 共振 8195/9880/21897/28129 ≤ 3.6e-05 m；GEO 25954/28626 ≤ 7.5e-06 m
afspc:           23599（i=6.9°，Lyddane 分支）max 964 m —— tcppver 是 improved 模式，对不上属预期；
                 同星 python-sgp4 `sgp4init(WGS72,'a',…)` @420 min = 4083.185512 km，与 crate afspc 输出逐位相同
解析拒绝 4 组：11801 "Parsing an integer field failed"（行 1 国际编号空白）；33333/33334/33335 "Bad line checksum"
20413 两组同号（tcppver 按号存），只比了第二组：69/70 点 ≤ 5.0e-04 m
传播报错 2 组：22312 @494.2 min、28350 @1560 min "propagated eccentricity (-0.00133) is outside the range [0, 1["（与 C++ 同处停）
```

### 3.5 错误用例

```bash
sgp4cmp tle "<ISS 行1 改末位>" "<行2>"
```

```
bad checksum   → ERR Bad line checksum on TLE line 1 between characters 68 and 69   (BadChecksum)
行 2 截到 60 列 → ERR Bad line length on TLE line 2 between characters 0 and 60        (BadLength)
行 1 尾随 3 空格 → ERR Bad line length on TLE line 1 between characters 0 and 72
CRLF 文件      → parse_3les: BadLength Line1 end 70（去 \r 后正常）
两行 NORAD 不同 → NoradIdMismatch
OMM ECCENTRICITY=1.2 → from_elements: OutOfRangeEpochEccentricity(1.2)
OMM EPOCH 带 "Z" → serde: Error("trailing input", line 1, column 100)
OMM NORAD_CAT_ID/MEAN_MOTION 写成字符串 → 照常解析（u64_or_string/f64_or_string）
```

衰减（ISS TLE 外推，`sgp4cmp life iss.tle ISS wgs72 <天>`）：

```
+1461 d OK alt~130.7 km   +1826 d OK alt~-68.7 km   +3000 d OK alt~-1502.8 km   +5000 d OK |r|=8.1 km
+8000 d ERR The propagated eccentricity (-0.00186) is outside the range [0, 1[
python-sgp4 同 TLE：+1461 d e=0，+1826 d 起 e=6（decayed）
```

### 3.6 速度（本人实测，同机同时段，8 核负载 ~5–7）

32 GPS × 10080 min = 322560 状态，单线程：

| 实现 | 耗时 |
| --- | --- |
| **sgp4 crate** `propagate`（release） | **85–88 ms**（264–272 ns/状态）；init 32 星 0.04 ms |
| crate `propagate_from_state`（保留共振状态） | 86–89 ms（1 min 步长无收益；结果逐位相同） |
| python-sgp4 `SatrecArray`（C++ 扩展） | 160–181 ms |
| python-sgp4 逐个 `sgp4_tsince` | 232 ms |
| satellite.js 7.1.0（Node） | 268 ms |

ISS 单星 322560 状态 74.5 ms（231 ns）。

## 4. I/O 字段

| 项 | 说明 |
| --- | --- |
| TLE | 严格 69 列；**校验 checksum**、行长、NORAD 一致；`parse_3les` 名称行可带尾空格，1/2 行不能 |
| OMM | 仅 JSON（CelesTrak `FORMAT=json` 数组可直接 `Vec<Elements>`）；`EPOCH` 须无时区后缀 |
| `Elements` | 度 / rev/day（`inclination` `mean_motion` …）；`datetime: NaiveDateTime`；`drag_term`=B* |
| 时间 | `MinutesSinceEpoch(f64)`；`datetime_to_minutes_since_epoch` 纳秒整数差，不计闰秒 |
| 输出 | `Prediction { position: [f64;3] km, velocity: [f64;3] km/s }`，TEME |
| 错误 | 解析 `tle::Error{BadChecksum/BadLength/NoradIdMismatch/ExpectedInteger…}`；初始化 `ElementsError`；传播 `gp::Error{OutOfRangeEccentricity/OutOfRangePerturbedEccentricity/NegativeSemiLatusRectum}` |

## 5. 参数

| 选择 | 常数 / 恒星时 | 何时用 |
| --- | --- | --- |
| `Constants::from_elements` | **WGS84** + IAU | 上游默认；与 CelesTrak 生成方不一致（GPS 差 27–34 m） |
| `Constants::new(WGS72, iau_epoch_to_sidereal_time, …)` | WGS72 + IAU | 对齐 python-sgp4 / satellite-js / tcppver（本文推荐） |
| `from_elements_afspc_compatibility_mode` + `propagate_afspc_compatibility_mode` | WGS72 + AFSPC | 对齐老 AFSPC 程序；只在 Lyddane（周期>225 min 且 i<0.2 rad）轨道与 improved 不同（23599 差 964 m） |
| `propagate_from_state(t, state, afspc)` | — | 深空共振星单调时间序列复用积分器；state 用 `c.initial_state().as_mut()`（近地星为 `None`；源码对近地星传 `Some` 会 assert，未实测） |

## 6. 接到哪步

CelesTrak/Space-Track TLE/OMM →（本 crate，Rust 服务/嵌入式）TEME → 自己或外部库转 ITRS（astropy / [orekit](./orekit.md)）→ 可见性、粗 IPP/掩星几何、TLE 质量监控。需要 m/cm 级 → [data-access](../data-access.md#sp3--clk--bias) 下 SP3 → [sp3](./sp3.md)；需要力模型外推/定轨 → [nyx](./nyx.md)（Rust）或 [orekit](./orekit.md)。Python 脚本 → [python-sgp4](./python-sgp4.md)；网页 → [satellite-js](./satellite-js.md)。

## 7. 坑（均实测）

1. **默认 WGS84**：`from_elements` 与 python-sgp4/CelesTrak（WGS72）差 **27–34 m**（GPS）。对账/回归测试一律用 §2 的 WGS72 写法。
2. **AFSPC 模式 ≠ tcppver**：官方 `tcppver.out` 是 improved 模式；用 AFSPC 比 23599 会差 964 m，别误判为 bug。
3. **没有"已衰减"错误**：ISS 外推 5 年高度 −68.7 km、13.7 年 `|r|`=8 km 仍返回 `Ok`；python-sgp4 此时 e=6。自己判 `|r| < 6378 km + 阈值`。
4. **TLE 解析很严**：checksum 错、行尾空格、CRLF、国际编号空白都会拒（官方校验集 4/33 组读不进）。读文件先 `trim_end()` 每行；需要宽松解析时自己修 checksum。
5. **OMM `EPOCH` 带 `Z` 就崩**：`trailing input`。Space-Track 某些导出带时区，先剥掉。
6. **TEME ≠ ECEF**：直接比 SP3 差 **26974 km**。
7. **GPST vs UTC**：`NaiveDateTime` 没有时间尺度，SP3 历元不减 18 s → **53.5 km**。
8. **OMM ≠ TLE 逐位**：同星 OMM 比 TLE 多一位小数；PRN02 在 2026-09-26 00:00 UTC 差 **1.39 m**（与 python-sgp4 相同），48 h 内逐星最大差中位 **1.86 m**、最大 4.8 m（G13）。
9. **`propagate_from_state` 不一定更快**：GPS 1 min 步长 7 天，与 `propagate` 同为 ~87 ms、结果逐位相同；只有大步长长弧的共振星才值得用。
10. **错误走 `Result`，不给 NaN**：发散轨道（22312 @494.2 min、28350 @1560 min）返回 `OutOfRangeEccentricity`；服务里别 `unwrap`——本 CLI 读 CRLF 文件时 `unwrap` 直接 panic、退出码 101。
11. **TLE 老化**：同组 GPS TLE 历元差 8 天，G13 对 SP3 469.6 km——看 `elements.datetime` 再用。

## 8. 选型（本人比较，基于上文实测）

| 需求 | 选 |
| --- | --- |
| Rust 服务 / 嵌入式（`no_std`）TLE 传播，要快、要类型化错误 | **本 crate**（WGS72 写法） |
| Python 批量 + 现成帧转换 | [python-sgp4](./python-sgp4.md) + astropy/skyfield（与本 crate µm 级一致，慢约 2×） |
| 浏览器 / Node | [satellite-js](./satellite-js.md)（带 GMST 级 `eciToEcf`） |
| 严格 ITRF、SP3 插值、TLE 拟合 | [orekit](./orekit.md) |
| Rust 力模型积分 / 定轨 | [nyx](./nyx.md) |
| m/cm 级 GNSS 轨道 | SP3：[data-access](../data-access.md#sp3--clk--bias) → [sp3](./sp3.md) |

| 维度（本人实测） | sgp4 crate 2.4.0 | python-sgp4 2.27 | satellite.js 7.1.0 |
| --- | --- | --- | --- |
| 默认常数 | WGS84 | WGS72 | WGS72 |
| 与 python-sgp4 TEME 差 | ≤ 8.8 µm（WGS72） | — | 5–17 mm（时间表示） |
| PRN02 对 SP3 mean | 0.534 km | 0.534 km | — |
| 322560 状态 | 85–88 ms | 160–181 ms（数组） | 268 ms |
| checksum | 校验 | 不校验 | — |
| 衰减 | 无错误码 | e=6 | — |
| OMM | JSON | JSON/XML/CSV | JSON |
