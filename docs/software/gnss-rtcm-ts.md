# @gnss/rtcm · TypeScript RTCM3 编解码库（Node-NTRIP/rtcm）操作手册

> <https://github.com/Node-NTRIP/rtcm>：Nebojša Cvetković 写的 TypeScript 库，npm 包名 `@gnss/rtcm`。它按 RTCM 10403.3 Amd.1 声明了 166 个消息类，可以拆帧、校验 CRC-24Q、把消息解码成对象再编码回去，另带 Node `stream.Transform` 形式的流解码器和流编码器。库里**没有 NTRIP 客户端**。Node-NTRIP 的 caster 把它当依赖，见 [caster](./caster.md)。
> **结论先说：** 在 RTKLIB 真样本上，帧计数、1005、1019/1020、1004/1012 的解码结果和 pyrtcm 1.2.0 全部一致。**但 MSM（1071–1137）的卫星数据和信号数据解错了**：库按卫星逐颗读字段，RTCM 标准是同一字段先把所有卫星排完。只有卫星掩码、信号掩码、单元掩码（即 PRN 和信号组合）是对的。
> 实测时间：2026-09-26 04:41–04:48 EDT。环境：Debian box，Node v20.19.2，npm 9.2.0，TypeScript 5.9.3（仅用于编译示例），对照库 pyrtcm 1.2.0（Python 3.13.5 venv）。

## 1. 用途边界

| 能（已实测） | 不能 / 有问题 / 未测 |
| --- | --- |
| `RtcmTransport.decode/encode`：拆帧、CRC-24Q、1005/1006、1019/1020、1004/1012、1007/1008/1033 | **MSM1–7 的卫星数据和信号数据解错**（§5），PRN 和信号掩码没问题 |
| 解码后再编码：非 MSM 消息逐字节相同（用清零的缓冲区） | MSM 卫星掩码只看低 32 个 ID，**ID 33–64 的卫星被静默丢掉**（合成用例） |
| `RtcmDecodeTransformStream`：能从流中间开始同步，也能跳过坏帧（要设 `closeOnError:false`） | 流结束时**缓冲区里剩的最多约 1 KiB 消息会丢**（§6、坑 3） |
| TS 类型定义能用（`tsc --strict` 编译通过，调用方不用开 decorators） | 浏览器打包（依赖 `Buffer`、`stream`）：**未测** |
| — | NTRIP：库里没有这部分功能；实时流：**未在真接收机测试** |

## 2. 版本事实（2026-09-26 核实）

| 项 | 值 |
| --- | --- |
| npm | `@gnss/rtcm` **0.1.5**（latest，2021-07-20 11:56 EDT 发布）；0.1.1–0.1.4 都是 2020-09-26 发的；解包后 59 个文件，共 394425 B |
| GitHub | 默认分支 `master` `96108e4`（2021-07-21 14:23 EDT，`readme: Message length when encoding`）；打版本号的提交是 `fcc0073`（`package: v0.1.5`）；**没有 tag，也没有 release** |
| 许可 / 星 | **GPL-3.0-or-later**（package.json；GitHub 显示为 GPL-3.0）；★48，fork 26 |
| 维护 | 最后一次代码提交在 2021-07。之后只有 dependabot 分支（最晚 2023-03）和 PR #13（2025-03 提交，至今未合并）。issue 共 3 个，都已关闭 |
| Node | `engines.node >=11.0.0`；本篇在 v20.19.2 上测试 |
| 依赖 | `bit-buffer-ts ^0.8.1`（装到 0.8.1）、`reflect-metadata ^0.1.13`（装到 0.1.14）；`node_modules` 共 936 KB |
| 导出 | `RtcmTransport`（`decode`、`encode`、`crc24q`、`DecodeException`、`EncodeException`、`MAX_PACKET_SIZE=1029`）、`RtcmMessage`、`RtcmMessageUnknown`、`RtcmMessageType`、`RtcmDecodeTransformStream`、`RtcmEncodeTransformStream`，以及 166 个 `RtcmMessage*` 类 |
| 消息 | 1001–1017、1019–1027、1029–1035、1037–1039、1041/1042/1044–1046、SSR 1057–1068、MSM1–7（GPS/GLO/GAL/SBAS/QZSS/BDS/IRNSS 1071–1137）、1230，另有 63 个 `FUTURE_*_MSM` 占位（1141–1227）。4001–4095 私有消息只有枚举值，没有对应的类 |

README 列了 103 个类名，**其中 11 个和实际导出的名字对不上**。例如 README 写 `RtcmMessageGpsL1Observables`，实际是 `…Observations`；`RtcmMessageStationaryArp` 实际是 `RtcmMessageStationArp`；`RtcmMessageGpsSatelliteEphemeris` 实际是 `…EphemerisData`。写代码时以 `build/index.d.ts` 为准。

## 3. 安装

```bash
export TMPDIR=$PWD/tmp npm_config_cache=$PWD/npmcache   # 共享机器上用自己的缓存目录
npm init -y && npm install @gnss/rtcm@0.1.5              # 冷缓存 0.8 s，装了 3 个包
```

## 4. 例子与真实输出

数据用 RTKLIB `180043e`（rtklib_2.4.3 分支，2020-12-29）的 `test/data/rcvraw/GMSD7_20121014.rtcm3`（262144 B，sha256 前 12 位 `8b466a682912`）和 `testglo.rtcm3`（57931 B，`71fd42a95453`）。

```js
// decode.js — 逐帧解码 RTCM3 文件（@gnss/rtcm 0.1.5）
const fs = require('fs');
const { RtcmTransport, RtcmMessageUnknown } = require('@gnss/rtcm');
const file = process.argv[2];
const buf = fs.readFileSync(file);
const t0 = process.hrtime.bigint();
const counts = {}, errs = {}; let off = 0, frames = 0, cells = 0, skipped = 0;
while (off < buf.length) {
  if (buf[off] !== 0xD3) { off++; skipped++; continue; }
  try {
    const [msg, len] = RtcmTransport.decode(buf.subarray(off));
    const t = msg.messageType; counts[t] = (counts[t] || 0) + 1; frames++;
    if (msg instanceof RtcmMessageUnknown) counts['unknown:' + t] = (counts['unknown:' + t] || 0) + 1;
    if (t >= 1071 && t <= 1137) cells += msg.satellites.reduce((a, s) => a + s.signals.length, 0);
    off += len;
  } catch (e) {
    const k = e.constructor.name + ': ' + e.message.split('\n')[0].slice(0, 60);
    errs[k] = (errs[k] || 0) + 1; off++; skipped++;
  }
}
const ms = Number(process.hrtime.bigint() - t0) / 1e6;
console.log(`${file}: ${buf.length} B, ${frames} frames, ${cells} MSM cells, ${skipped} bytes skipped, ${ms.toFixed(1)} ms`);
console.log('counts', JSON.stringify(counts));
console.log('errors', JSON.stringify(errs));
```

```text
$ node decode.js GMSD7_20121014.rtcm3
GMSD7_20121014.rtcm3: 262144 B, 1143 frames, 19558 MSM cells, 302 bytes skipped, 78.3 ms
counts {"1007":28,"1008":28,"1019":15,"1020":16,"1033":28,"1077":257,"1087":257,"1117":257,"1127":257}
errors {"DecodeException: RTCM decode exception: CRC does not match (expected 0, got b":1,"DecodeException: RTCM decode exception: CRC does not match (expected 0, got 3":1}
$ node decode.js testglo.rtcm3
testglo.rtcm3: 57931 B, 429 frames, 0 MSM cells, 58 bytes skipped, 20.2 ms
counts {"1004":186,"1005":19,"1012":186,"1019":19,"1020":19}
errors {}
```

- GMSD7 最后 302 B 是一个被截断的帧（文件正好截在 256 KiB）。截断帧读不到 CRC 时，库把收到的 CRC 当成 0，所以报 `expected 0`。testglo 开头有 58 B 不是 RTCM 帧的内容。两个样本都**没有**解成 `RtcmMessageUnknown` 的帧。
- 耗时：GMSD7 跑了 3 次，78–92 ms（约 3 MB/s，包含 JIT 预热）；testglo 20–23 ms。

各类型第一帧的字段（`first.ts`，用 `tsc --strict` 编译，按类型用 `instanceof` 收窄）：

```text
1077 sta 611 tow_ms 604784000 sats 1,3,6,7,11,13,16,19,21,23,30,31 sig 2,10,17,24
1019 PRN 28 week 685 toe_s 604784 sqrtA 5153.630821228027
1005 ARP ECEF m -3869297.5138000003, 3436571.3345000003, 3717369.3757     (testglo)
1019 PRN 3 week 538 toe_s 518400 sqrtA 5153.678451538086                  (testglo)
```

所有字段都是**原始整数**，库不做比例换算：`arpEcefX` 的单位是 0.1 mm，`a_1_2` 要乘 2⁻¹⁹，`t_oe` 要乘 16 s。1019 的周数是 10 位的（685 实际是 1709 周），要自己加 1024×n。

## 5. 交叉检查（对 pyrtcm 1.2.0 逐帧比较）

方法：把 `decode.js` 解出的对象存成 JSON，`compare.py` 用 `RTCMReader(quitonerror=0)` 逐帧读同一个文件，按帧序号配对。pyrtcm 输出的值已经乘过比例因子，脚本先除回去，再和 TS 的原始整数比较（`round(py/scale) == ts`）。注意 pyrtcm 1.2.0 对 1020 的 DF121/124/125/133/135 **不做**比例换算，比较时按比例 1 处理。

| 项 | GMSD7 | testglo |
| --- | --- | --- |
| 帧数 / 类型序列 | 1143 = 1143，序列完全一致 | 429 = 429，序列完全一致 |
| 按类型计数 | 两边全等（见 §4） | 两边全等 |
| 1005 ECEF（3 个字段 ×19 帧） | — | 57 个值，**0 不等** |
| 1019（30 个字段） | 450 个值，**0 不等** | 570 个值，**0 不等** |
| 1020（35 个字段） | 560 个值，**0 不等** | 665 个值，**0 不等** |
| 1004/1012（每颗卫星 10–11 个字段） | — | 32560 个值，**0 不等** |
| MSM7 单元数 / NSat / PRN | 19558 = 19558；NSat 1028 帧、PRN 6951 个全等 | — |
| MSM DF397（第 1 颗卫星） | 1028 个值，0 不等 | — |
| MSM DF397（第 2 颗及以后） | 5923 个值中 **5917 个不等**（max\|Δ\|=187 ms） | — |
| MSM DF398 / DF399 / 扩展信息（所有卫星） | **不等率 75–100%**；只有 NSat=1 的 257 帧 1117 全对 | — |
| MSM 信号 DF405 / DF406 / DF407 / DF408 / DF404 / DF420 | 19558 个单元中不等 18530 / 19558 / 19286 / 19534 / 18011 / 7798 | — |

```python
# compare.py 片段：MSM 卫星字段比较（py 为 pyrtcm 消息，s 为 TS JSON 里的一颗卫星）
SAT = [('roughRangeIntegerMilliseconds','DF397',1), ('extendedInformation','EXT',1),
       ('roughRangeModulo1Millisecond','DF398',2**-10), ('roughPhaserangeRateMetersPerSecond','DF399',1)]
for i, s in enumerate(sats, 1):
    for a, df, sc in SAT:
        pv = getattr(m, f"{ext if df == 'EXT' else df}_{i:02d}")   # ext: GLO 用 DF419，其余用 ExtSatInfo
        cmp(f'MSM.sat.{df}', s[a], pv, sc)                        # round(pv/sc) == s[a] ?
```

第一帧 1077 的例子：pyrtcm 读出卫星 1 的扩展信息是 0，DF398 是 135/1024 ms；TS 读出 4 和 145/1024 ms。TS 这个 4 其实是第 2 颗卫星 DF397（66=0x42）的高 4 位。**原因**（源码 `observations/msm/common.ts` 的 `decodeBody`）：代码对每颗卫星跑一遍 `satelliteDecoder.run(satellite, s)`，一次读完这颗卫星的所有字段；RTCM MSM 的排列是同一字段先把所有卫星排完（先是 N 个 DF397，再是 N 个扩展信息、N 个 DF398……），信号数据也是这样按字段排的。1033 的接收机字符串 `TRIMBLE NETR9` 和 pyrtcm 的 DF228 一致。

**编码往返**（`roundtrip.js`：decode → `encode` → 和原帧逐字节比较）：

| 类型 | 输出缓冲区复用、不清零 | 每次先 `out.fill(0)` |
| --- | --- | --- |
| 1004/1005/1007/1008/1019/1020/1033 | 全部相同 | 全部相同 |
| 1012（186 帧） | **12 帧相同**，其余差在最后一个字节的填充位 | 186/186 相同 |
| 1077/1087/1117/1127（1028 帧） | 0 帧相同 | 0 帧相同：每帧都差在 bit 58–64，即 DF001 的 7 个保留位（原文件是 1，库写 0）。**数据位 0 个不同**，填充位也没有不同 |

```js
// roundtrip.js 核心（缓冲区清零版）
const out = Buffer.alloc(RtcmTransport.MAX_PACKET_SIZE);
const [msg, len] = RtcmTransport.decode(buf.subarray(off));
out.fill(0); const n = RtcmTransport.encode(msg, out);
const same = buf.subarray(off, off + len).equals(out.subarray(0, n));
```

MSM 往返能对上数据位，是因为编码器 `encodeBody` 也按卫星逐颗写，和解码器错的方式一样，两个错误互相抵消了。**所以往返一致并不说明 MSM 解对了**。推断：用 `construct()` 按真实数值构造的 MSM，交给其他解码器会被读错（没有单独构造验证）。

## 6. 错误用例（全部是「合成」输入，素材取自上面两个真实文件里的帧）

| 用例 | `RtcmTransport.decode` 的行为 |
| --- | --- |
| 空 Buffer | **`TypeError: Cannot read properties of undefined (reading 'toString')`**，不是 `DecodeException` |
| 坏 CRC（1005 帧翻转 1 bit） | `DecodeException: CRC does not match` |
| 截断（只给 25 B 帧的前 20 B） | `DecodeException: CRC does not match (expected 0, …)` |
| 帧前有垃圾 `hello` | `DecodeException: Invalid preamble (expected d3, got 68)`，**不会自己往后找同步头** |
| 未知消息号 4072 / 1300（CRC 正确） | 解成 `RtcmMessageUnknown`，但 `messageType` 报成 **4064 / 1296**（源码用了 `<<4 \|\| >>4`，把按位或写成了逻辑或） |
| 编码 `RtcmMessageUnknown` | **`RangeError: offset is out of bounds`**（源码 `message.raw.set(buffer, 3)` 把源和目标写反了），所以没法透传未知消息 |
| 长度字段写 1023，实际只有 40 B | `DecodeException: CRC does not match` |
| 长度字段写 10（1005 需要 19 B），CRC 重新算过 | `DecodeException: Could not run script: Cannot get/set 38 bit(s) …` |
| 长度 0 / 1 的帧，CRC 正确 | 静默解成 `RtcmMessageUnknown`，`messageType=-1` |
| MSM7 里放 BDS 卫星 ID 40（改掩码高 32 位，CRC 重新算过） | **静默返回，`satellites=[]`**，不报错；pyrtcm 读出 `NSat 1 PRN_01 040 NCell 6` |

`RtcmDecodeTransformStream`（`stream.js` 核心）：

```js
const d = new RtcmDecodeTransformStream({ closeOnError: coe });   // 默认 closeOnError=true
d.on('data', () => n++); d.on('error', e => console.log('error after', n, e.message));
d.on('end', () => console.log('end:', n, 'msgs'));
fs.createReadStream(file, { highWaterMark: hwm }).pipe(d);
```


| 用例 | 结果 |
| --- | --- |
| 3 帧一次性 `end(buf)` | **只输出 1 条**，另外 2 条留在缓冲区里（没有实现 `_flush`） |
| 整个文件用 `createReadStream` 读，chunk 64 KiB / 1 KiB / 16 B | GMSD7 分别出 1141 / 1141 / 1143 条，testglo 分别出 423 / 423 / 429 条。chunk 越大，结尾丢的越多 |
| 逐字节写入：帧前有 junk | 3/3，能正常同步 |
| 逐字节写入：两帧之间有 junk 或坏 CRC，用默认 `closeOnError:true` | 出 1 条后触发 **`error` 事件，流终止** |
| 同上，`closeOnError:false` | 3/3，能重新同步 |
| 截断帧后面跟 10 个完整帧（`closeOnError:false`） | 11/11，能恢复 |

NTRIP：库里没有这部分功能，**不适用**。串口和实时 TCP 流：**未在真接收机测试**。

## 7. I/O 要点

- 输入是 `Uint8Array`/`Buffer`，**第一个字节必须是 0xD3**。`decode` 返回 `[message, 字节数]`，找下一帧的循环要自己写（见 `decode.js`）。
- 输出对象里的字段是原始整数（DF 单位），没有工程单位。MSM 另有 getter，例如 `roughRangeMeters`；消息里有 `info.satelliteIds` 和 `info.signalIds`。
- 编码时缓冲区至少要 `MAX_PACKET_SIZE=1029` 字节，函数返回写入的长度。库**不会清零填充位**：README 示例用的是 `Buffer.allocUnsafe`，这样填充位里会留下旧数据，CRC 照样合法，但输出每次可能不一样。
- 流：解码器是 `readableObjectMode`；编码器是 `writableObjectMode`，输出原始字节。

## 8. 坑

1. **MSM 数值不能用**：卫星数据和信号数据按卫星逐颗读，只有 NSat=1 时卫星字段是对的，只有 NCell=1 时信号字段是对的，其余情况都错。用它做 RTK、RINEX 转换，或者把 MSM 当 CN0 监测源，都会得到错误结果。可以只用它拆帧、做 CRC 和识别类型，MSM 另外解析。
2. **往返一致是假象**：编码器错的方式和解码器一样，所以 decode→encode 在数据位上逐字节相同（只差 DF001 保留位）。仓库自带测试是构造后往返的形式（本篇没有运行这些测试），查不出这种错误。
3. **流解码器结尾丢消息，而且会攒消息**：每次循环最多输出 1 条；chunk 用完以后缓冲区里剩的消息要等下一个 chunk 到了才输出；流结束时直接丢掉。推断：做实时 NTRIP 转发时，消息会晚一个 TCP 包才出来（**未在真接收机测试**）。
4. 默认 `closeOnError:true`：已经同步之后，只要碰到一个坏 CRC 或几个垃圾字节，整个流就结束了。实时场景要设 `closeOnError:false`。
5. 卫星掩码只看前 32 位：BDS C33 以后、Galileo E33–E36、SBAS 高位 ID 都会被**静默丢掉**。
6. `RtcmMessageUnknown` 的 `messageType` 报错，而且没法编码：私有消息（4072 u-blox 等）不能透传。
7. 空输入抛 `TypeError`，不是 `DecodeException`：只 `catch` `DecodeException` 的代码会漏掉。
8. README 里的类名有 11 个过时，以 `.d.ts` 为准。
9. 1019 的 10 位周数、比例因子、GLONASS 符号-幅值编码的换算都要自己做（GLONASS 的符号库已经处理对了，1020 和 pyrtcm 全等）。
10. **GPL-3.0-or-later 的影响**：只要分发包含本库的程序，包括打进前端 bundle 发给浏览器、Electron 应用、嵌入式固件、npm 再发布，整个组合作品通常都要按 GPL 兼容条款提供源码。只在服务器端运行、不对外分发，GPL（不是 AGPL）一般不要求公开源码。闭源 SDK 或 MIT/Apache 项目想直接依赖它，要先找法务评估，或者换宽松许可的库（§10）。以上不是法律意见。
11. 项目已经停更（2021-07），PR #13 一直没合并。要用只能自己 fork 修补上面这些问题。

## 9. 接到哪步 / 未测清单

- **上游**：RTCM3 文件或字节流（本篇用的是 RTKLIB 仓库里的样本）。实时源可以用 [caster](./caster.md)、[ntrip-client](./ntrip-client.md) 或 [bnc](./bnc.md) 转发来的字节（**未测**）。
- **下游**：1005/1006 → 基站坐标；1019/1020 → 自己按 IS-GPS-200 / GLONASS ICD 换算单位。MSM 不要直接往下游送（坑 1）。
- **未测**：SSR 1057–1068、1041–1046 星历、1021–1027 坐标变换、1029/1230、MSM1–6（和 MSM7 用同一个 `decodeBody`，推断同样有错）；浏览器和 Deno；Node 11–18 的兼容性；仓库自带的 jest 测试（没装 devDependencies）。
- **未在真接收机测试**：串口和 TCP 实时流、和 NTRIP caster 联调。

## 10. 选型

| 需求 | 选 |
| --- | --- |
| Node/TS 里只要拆帧、CRC、看类型，或者解 1005/1006/1019/1020/传统观测 | **本库**（注意坑 3、4、10） |
| Node 里要正确的 MSM 数值 | 本库需要 fork 修 `decodeBody`/`encodeBody`；或者在旁路调用 [pyrtcm](./pyrtcm.md)、[rtklib](./rtklib.md) |
| Python：解析、生成、对照基准（本篇的参照） | [pyrtcm](./pyrtcm.md)（BSD-3） |
| Rust：嵌入式或服务端 | [rtcm-rs](./rtcm-rs.md)（MIT OR Apache-2.0） |
| Go：轻量解析 | [go-gnss-rtcm](./go-gnss-rtcm.md)（Apache-2.0） |
| Go：RTCM3 → JSON 检查，同一个库还能处理 RINEX/BINEX/SBF | [earthscope-gnsstools](./earthscope-gnsstools.md) `gnss-inspect`（同一份 GMSD7 和 pyrtcm 的单元数全等；**不能**把 RTCM 转成 RINEX） |
| RTCM → RINEX | [rtklib](./rtklib.md) `convbin` / [rtcm3torinex](./rtcm3torinex.md)；BKG 工具集见 [rtcm-ntrip-software](./rtcm-ntrip-software.md) |
| Node 生态的 NTRIP caster（依赖本库，但只透传字节） | [caster](./caster.md) |
