# satellite-js · JavaScript/TypeScript SGP4/SDP4 轨道传播操作手册

目录：`PROJECTS.json` **`satellite-js`**（orbit-clock / SGP4-JS）· 上游 <https://github.com/shashwatak/satellite-js>（默认分支 `develop`，HEAD **`95e43b7`** 2026-09-25 16:59 EDT）· npm **`satellite.js` 7.1.0**（2026-07-23 发布；tag `7.1.0`=`582a72e`）· **MIT** · ★**1091** · 纯 ESM（`"type":"module"`，自带 `.d.ts`）· 本机 Node **v20.19.2** / npm 9.2.0 · 真跑 2026-09-26 02:09–02:30 EDT

> **质检复跑通过（有小修正）**（2026-09-26 03:59–04:04 EDT）。
> - 环境：npm `satellite.js@7.1.0`（2026-07-23 发布，MIT，`"type":"module"`），Node v20.19.2；develop HEAD `95e43b7`、tag `7.1.0`=`582a72e`、★1091 均核对无误。CelesTrak 重抓的 ISS/PRN02 TLE 与原文历元相同。
> - 逐字复现（脚本按原文描述重写）：§3.2 四行输出与 |dr|/|dv| 逐位一致（max 1.712e-2 m / 5.731e-6 m/s）；`jdsatepoch` 2461308.56454359、`jdsatepochF` undefined、tsince 1347.0572304725647；`sgp4(s,1347.0572304)` x=18021.574979685072；§3.3 克隆 `95e43b7` 后 `vitest --project js` 7 个文件 / 410 个测试通过，`tle.txt` 51949 行；对 tcppver 为 33 TLE / 666 态 / 1 null，max|dr| 1.171e-4 m（20413@1844335），max|dv| 8.529e-7 m/s；§3.4 纯 JS 四行逐位一致（0.549/0.881、53.480/57.941、26974.176/52133.889、31 星中位 1.675、max 469.596）；`eciToEcf` 与 astropy ITRS 差 53.16 m；`no` 0.0087510997、lat −0.16288 rad / −9.3325°；截断 TLE error 0 + NaN；+5 年 null / error 6，+3 年仍给坐标；OMM−TLE 1.91 m。
> - 修正：坑 11 耗时本次 259–279 ms（原 301 ms），改为区间；Python `SatrecArray` 同步改为 python-sgp4 质检实测的 160–185 ms。
> - 未复跑：`catalog` 测试（原文已记 OOM，为免拖垮共享机未重试）、WASM `BulkPropagator`。

> 岗位：在浏览器/Node 里把 TLE/OMM 传播成 **TEME（库里叫 ECI）** 位置/速度，再用自带 `eciToEcf`/`eciToGeodetic`/`ecfToLookAngles` 做**可视化级**几何。精度 **km 级**（GPS 实测中位 ~1.7 km，§3.4）。冲突时：**上游 README / `dist/*.d.ts` > 本文**。
> 姊妹篇：[python-sgp4](./python-sgp4.md)（同算法 Python 版；本文所有交叉数值与其对拍）。精密轨道：[data-access · SP3](../data-access.md#sp3--clk--bias) → [gnssanalysis](./gnssanalysis.md)。

## 1. 用途与边界

**做：** `twoline2satrec` / `json2satrec`（OMM JSON）→ `propagate(satrec, Date)` 或 `sgp4(satrec, tsinceMin)` → `{position, velocity, meanElements}`；`gstime`、`eciToEcf`、`ecfToEci`、`eciToGeodetic`、`geodeticToEcf`、`ecfToLookAngles`、`dopplerFactor`、`sunPos`、阴影；7.x 起带 WASM `BulkPropagator`（本文未测）。

**不做：** 不拉 TLE；不是精密星历；`eciToEcf` **只按 GMST 旋转**（无 UT1−UTC、无极移、无章动项）→ 与 astropy ITRS 差 **53 m**（§3.4），可视化够、测量不够。

| 易混 | 是什么 |
| --- | --- |
| **本文** npm `satellite.js` | JS/TS SGP4 + 简易坐标变换 |
| [python-sgp4](./python-sgp4.md) | Python 同算法，只给 TEME，历元拆双 double |
| CesiumJS / 各类 "tle.js" | 多为封装本库的可视化层 |

## 2. 安装

```bash
npm init -y && npm i satellite.js      # → satellite.js@7.1.0
# 纯 ESM：用 .mjs 或 "type":"module"；CommonJS 需 await import('satellite.js')
```

```js
import * as satellite from 'satellite.js';
```

## 3. 真命令 + 实测输出（2026-09-26 EDT）

### 3.1 输入

TLE/OMM 与 [python-sgp4 §3.1](./python-sgp4.md#31-拉-tleomm记录抓取时刻) 同一批：2026-09-26 02:09:18 EDT 从 CelesTrak GP API 抓 `gps-ops`（32 星）+ ISS。ISS 历元 `26268.43198945`（2026-09-25 10:22:03.888 UTC = 06:22 EDT）；GPS BIIR-13 PRN 02 历元 `26268.06454359`（2026-09-25 01:32:56.566 UTC = 09-24 21:33 EDT）。

### 3.2 传播 + 与 python-sgp4 交叉

```js
const s  = satellite.twoline2satrec(l1, l2);
const pv = satellite.propagate(s, new Date('2026-09-26T00:00:00Z'));   // UTC
// pv.position {x,y,z} km（TEME），pv.velocity km/s；s.error 为错误码
```

`node js_prop.mjs` 实测（与 python-sgp4 2.27 同时刻相减）：

```
satellite.js 7.1.0
ISS (ZARYA)|2026-09-26T00:00Z 0 -949.485591 4511.500075 -5001.757254 -7.322557178 0.764630120 2.076133331 |dr|=5.074e-3 m |dv|=5.709e-6 m/s
ISS (ZARYA)|2026-09-27T00:00Z 0 688.165462 -4592.529187 4953.048800 7.228249664 -1.288068479 -2.198008431 |dr|=5.084e-3 m |dv|=5.731e-6 m/s
GPS BIIR-13 (PRN 02)|2026-09-26T00:00Z 0 18021.574988 -18486.667120 -4235.878192 2.017883432 1.198689136 3.155333531 |dr|=1.712e-2 m |dv|=2.536e-6 m/s
GPS BIIR-13 (PRN 02)|2026-09-26T06:00Z 0 -18241.277927 19245.665143 4873.354732 -1.977397924 -1.143054482 -3.057086236 |dr|=1.661e-2 m |dv|=2.388e-6 m/s
max |dr|=1.712e-2 m, max |dv|=5.731e-6 m/s
```

差异来源（已查实）：`s.jdsatepoch = 2461308.56454359` 单 double（`jdsatepochF` 为 `undefined`），`jday()` 算出的 tsince = `1347.0572304725647` min，Python 拆分精确值 `1347.0572304`；`satellite.sgp4(s, 1347.0572304)` → `{x: 18021.574979685072, …}` 与 Python **逐位相同**。

### 3.3 测试 / 校验向量

npm 包**不带**测试。克隆仓库跑：

```bash
git clone --depth 1 https://github.com/shashwatak/satellite-js && cd satellite-js && npm ci
npx vitest run --project js        # Test Files 7 passed (7) / Tests 410 passed (410)，754 ms
npx vitest run --project catalog   # 51949 行 tle.txt 全目录：默认堆 OOM 崩；8 GB 堆被系统 Killed（15 GB 机）→ 未跑成
# wasm_release / wasm_debug 需 em++（emscripten）先 npm run build，本机无 → 未跑
```

补做：用 python-sgp4 包内官方 `SGP4-VER.TLE` + `tcppver.out` 对本库逐行比（`node jsver.mjs`）：

```
satellite.js vs tcppver.out: 33 TLE, 666 states compared, 1 null, max|dr|=1.171e-4 m (20413@1844335), max|dv|=8.529e-7 m/s
```

（`20413` 在向量里出现两次，按顺序配对，别用 satnum 做字典键。）

### 3.4 对 IGS SP3 的精度（纯 JS 流水线，本人比对）

SP3：BKG 免登录镜像 `IGS0OPSULT_20262680000_02D_15M_ORB.SP3`（前 24 h / 96 历元，GPST）。每历元 `new Date(gpst − 18 s)` → `propagate` → `eciToEcf(pos, gstime(date))` → 与 SP3 差：

```
PRN02 eciToEcf(gstime): mean=0.549 max=0.881 km (n=96)
PRN02 WRONG no leap   : mean=53.480 max=57.941 km (n=96)
PRN02 WRONG no ecf    : mean=26974.176 max=52133.889 km (n=96)
ALL 31 sats median mean3D=1.675 min=0.306 max=469.596
```

对照 python-sgp4 + astropy 严格 `TEME→ITRS`：PRN02 mean **0.534** km、全星中位 **1.658** km。同一点（PRN02，2026-09-25 12:00 UTC）`eciToEcf` 与 astropy ITRS 差 **53.1 m**——这就是 GMST-only 旋转的代价；相对 SGP4 本身 km 级误差可忽略。最大值 469.6 km 为 G13 BIII-10（TLE 老 4.7 d，见 python-sgp4 §3.4）。

## 4. I/O 字段

| 项 | 说明 |
| --- | --- |
| `twoline2satrec(l1, l2)` | 7.x `.d.ts` 只有两个参数（无 opsmode；多传被忽略） |
| `json2satrec(omm, opsmode?)` | CelesTrak `FORMAT=json` 单条对象 |
| `propagate(s, Date \| y,mo,d,h,mi,s[,ms], {communityDecayCheckEnabled})` | `Date` 只有 **ms** 分辨率 |
| 返回 | `{position, velocity, meanElements}` 或 **`null`**（出错）；`s.error` 为 `SatRecError` 枚举：0 None / 1 MeanEccentricityOutOfRange / 2 MeanMotionBelowZero / 3 PerturbedEccentricityOutOfRange / 4 SemiLatusRectumBelowZero / 6 Decayed |
| satrec 字段 | 弧度、rad/min：`inclo` 0.96117、`no` **0.0087510997**（PRN02；已是 un-Kozai，≠ Python `no_kozai` 0.0087510929） |
| `eciToGeodetic(pos, gmst)` | `{longitude, latitude}` **弧度**、`height` km；PRN02 实测 lat −0.16288 rad → `degreesLat` −9.3325° |

## 5. 参数

| 参数 | 说明 |
| --- | --- |
| `communityDecayCheckEnabled` | 非官方 SGP4 的"早已衰减"检查；默认关，打开后结果不再与 Vallado 逐位一致 |
| `gstime(date)` | GMST（IAU-82），`eciToEcf` 的旋转角；不含 UT1 修正 |
| `BulkPropagator`（WASM） | 7.x 新增批量接口；需要额外初始化，本文未测 |

## 6. 接到哪步

CelesTrak GP（JSON/TLE）→ 本库 → `eciToEcf`/`ecfToLookAngles` → 地图/3D 地球/过境表（前端）→ 需要严谨框架或 m 级 → 后端 [python-sgp4](./python-sgp4.md) + astropy；GNSS 精密 → [data-access](../data-access.md#sp3--clk--bias) SP3 + [gnssanalysis](./gnssanalysis.md) / [sp3](./sp3.md)；动力学外推 → [gmat](./gmat.md)。

## 7. 坑（均实测）

1. **"ECI" 实为 TEME**：直接当 ECEF 与 SP3 比 → **26974 km**；要 `eciToEcf(pos, gstime(date))`。
2. **`eciToEcf` 简化**：GMST-only，vs astropy ITRS **53 m**；别拿去做 m 级比较。
3. **GPST/UTC**：`Date` 是 UTC，SP3 是 GPST，不减 18 s → **53.5 km**。
4. **截断/坏 TLE 不报错**：截断两行 → `s.error === 0`，`propagate` 返回**非 null** 但全 `NaN`（Python 同输入给 error 2）。要自己 `Number.isFinite(pv.position.x)`。
5. **衰减返回 `null`**：ISS TLE +5 年 → `null`、`s.error=6 Decayed`；+3 年仍给坐标（无物理意义）。`pv.position` 前先判 null。
6. **弧度 / 分钟**：`satrec.no` rad/min、角度弧度、`eciToGeodetic` 经纬弧度；忘了 `degreesLat/Long` 是常见 bug。
7. **时间精度**：单 double 历元 + `Date` ms → 与 Python 差 5–17 mm；做逐位对拍用 `sgp4(s, tsince)`。
8. **OMM vs TLE**：PRN02 OMM 多一位偏心率（0.01725844）→ 同时刻 **1.91 m**（Python 1.39 m；JS `EPOCH` 走 `Date` 只保留到 ms 可能贡献部分差，未单独拆）。
9. **纯 ESM**：`require('satellite.js')` 不可用；Node 需 `.mjs`/`"type":"module"` 或动态 `import()`。
10. **catalog 测试吃内存**：51949 行全目录测试在 15 GB 机 OOM；CI 只跑 `--project js`。
11. **速度**：32 星×10080 分钟逐次 `propagate(Date)` = 322560 状态 **259–301 ms**（两次实测；Python `SatrecArray` 160–185 ms）。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 网页/Node 过境、星下点、3D 可视化 | **本库** |
| Python 批量 + 严格 TEME→ITRS | [python-sgp4](./python-sgp4.md) + astropy |
| m/cm 级 GNSS 轨道 | SP3 → [gnssanalysis](./gnssanalysis.md) |
| 力学模型外推 / 定轨 | [gmat](./gmat.md) / Orekit |
| Rust 嵌入 | sgp4-rs（`PROJECTS.json` 已登记） |
