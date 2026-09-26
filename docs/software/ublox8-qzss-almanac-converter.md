# ublox8-qzss-almanac-converter · YUMA 历书 → u-blox UBX-MGA-GPS/QZSS-ALM 操作手册

目录：[`PROJECTS.json` → `ublox8-qzss-almanac-converter`](../../PROJECTS.json) · 上游 <https://github.com/jkivilin/ublox8-gps-qzss-yuma-almanac-converter>（**注意仓名**：`ublox8-qzss-almanac-converter` 只是目录名，GitHub 上该短名 404）· **无 tag / 无 PyPI / 无 pyproject**，main tip **`1170ab7`**（2026-02-10 15:51 EST，`Merge pull request #2 … add-ci-workflow`）· **MIT** · ★**12** · Python（CI 矩阵 3.11–3.13）· 本机 CPython 3.13.5 + venv：pyubx2 1.3.7 / pytest 9.1.1 / pylint 4.0.9 · 实测窗口 **2026-09-26 05:46–05:55 EDT**

> 一句话：一个 165 行的 `convert_alm.py`，把 **YUMA 文本历书**（GPS PRN 1–32 + QZSS PRN 193–197）转成 u-blox 8/M8 的 **UBX-MGA-GPS-ALM**（`0x13 0x00`）/ **UBX-MGA-QZSS-ALM**（`0x13 0x05`）二进制帧，每帧 44 B。转换本身只用标准库（`sys`/`math`/`struct`）。
> **本机无 u-blox 接收机**：把 `.ubx` 写进接收机、冷启动/TTFF 效果、MGA-ACK 回应，全部 **「未在真接收机测试」**。下文输出均为本机真跑；人造输入标 **「合成」**。

> **质检复跑通过（2026-09-26 06:10–06:15 EDT）**：clone `1170ab7`（短仓名仍 404），CPython 3.13.15，pyubx2 1.3.7 / pytest 9.1.1 / pylint 4.0.9。`pytest` 106 passed，pylint 10.00/10。4 个历书下载与字节数一致（21168/2864/18303/19008）。6 组转换的输出字节与帧数全部一致（1540/132/1408/1408/1496/1496，stdout 70 行），`cmp` 两条都相同，首帧十六进制一致。`print_ubx.py` 0 行 + 35 条 `Unknown message type`；SET 模式打印的两帧逐字相同。截断输入（4 行 `Converted` 后 `KeyError: 'almWNa'`、不生成文件）和 PRN 203（`KeyError: 'sat_type'`）复现。§4 的独立交叉检查和 §5 其余合成用例未重跑。

## 1. 用途边界

| 做 | 不做 |
| --- | --- |
| YUMA → MGA-GPS-ALM（PRN 1–32，**Health≠0 静默跳过**） | 不出星历（→ 同作者 [ubx-mga-rinex-ephemeris](./ubx-mga-rinex-ephemeris.md)）、不出 MGA-INI 时间/位置、不出 HEALTH/IONO/UTC |
| YUMA → MGA-QZSS-ALM（PRN 193–197 → svId 1–5，QZO：e 减 0.06、δi 相对 0.25 半周） | **GEO（PRN 198–202，如 199 QZS-3、200）静默跳过**：M8 规格 MGA-QZSS-ALM svId 仅 1–5 |
| QZSS 官网 `qg*.alm`/`q*.alm`/`g*.alm`、NAVCEN YUMA 均可读（两种浮点写法都吃） | 不读 SEM、RINEX、`.gz`；不做命令行解析（无 `-h`/`--help`，只认两个位置参数） |
| 标准库即可转换；附 `print_ubx.py`（pyubx2）打印 | 不发串口；不检查历书是否过期；不做 BDS/Galileo/GLONASS 历书 |

适用代际：上游 README 与 M8 协议规格 R28（UBX-13003221）写 **u-blox 8 / M8，协议版本 15–23.01**。F9/M10 是否接受同格式：**未测**。

## 2. 安装

```bash
mkdir -p /tmp/qzssalm-man && cd /tmp/qzssalm-man
export TMPDIR=/tmp/qzssalm-man/tmp PIP_CACHE_DIR=/tmp/qzssalm-man/pipcache   # 共享机器：缓存放自己目录
git clone https://github.com/jkivilin/ublox8-gps-qzss-yuma-almanac-converter src   # 1170ab7
python3 -m venv venv && ./venv/bin/pip install pytest pyubx2 pylint           # 仅测试/打印需要
cd src && ../venv/bin/pytest -q test_convert_alm.py      # → 106 passed in 1.39s
../venv/bin/pylint convert_alm.py print_ubx.py           # → rated at 10.00/10
```

入口就是脚本：`python3 convert_alm.py <输入.alm> <输出.ubx>`。**没有 `--help`**：无参数运行 → `IndexError: list index out of range`，exit 1。README 用法原文：

```text
Usage:
  python3 convert_alm.py [input almanac file] [output UBX file]
```

## 3. 例子与真实输出

### 3.1 取公开历书（免账号）

- QZSS 官网 <https://sys.qzss.go.jp/dod/en/archives/pnt.html> → Almanac（YUMA Format）。页面用表单查，文件本身是静态路径：`https://sys.qzss.go.jp/archives/almanac/<年>/qg<年><DOY>.alm`（QZSS+GPS）、`q…`（仅 QZSS）、`g…`（仅 GPS）。
- NAVCEN：`https://www.navcen.uscg.gov/sites/default/files/gps/almanac/current_yuma.alm`。

```bash
curl -sS -O https://sys.qzss.go.jp/archives/almanac/2026/qg2026268.alm   # 200，21168 B，参考时刻 2026/09/25 00:00
curl -sSL -o gps_yuma.alm https://www.navcen.uscg.gov/sites/default/files/gps/almanac/current_yuma.alm  # 200，19008 B
```

`qg2026268.alm`：37 个 ID（GPS 01–32 + QZSS 194/195/196/199/200），全部 `week: 390`（= GPS 周 2438 mod 1024），GPS toa 61440 s、QZSS toa 86016 s；QZSS Health 为 `001`（194/195/199）与 `016`（196/200）。NAVCEN 文件 32 颗、toa 147456 s、Health 全 000，浮点写成 `0.1998424530E-002` 风格。

### 3.2 转换（05:50 EDT 实跑）

```bash
python convert_alm.py qg2026268.alm qg2026268.ubx      # rc=0，0.014 s
python convert_alm.py gps_yuma.alm  gps_yuma.ubx       # rc=0，0.013 s
```

stdout 原文（每颗星两行，共 70 行，末尾截取）：

```text
-------
Converted UBX-MGA almanac for GPS satellite ID 32.
-------
Converted UBX-MGA almanac for QZSS satellite ID 194.
-------
Converted UBX-MGA almanac for QZSS satellite ID 195.
-------
Converted UBX-MGA almanac for QZSS satellite ID 196.
```

| 输入 | 输入字节 | 输出字节 | 帧数（44 B/帧） | 说明 |
| --- | ---: | ---: | ---: | --- |
| `qg2026268.alm` | 21168 | 1540 | 35 = 32 GPS + 3 QZSS | 199/200（GEO）无提示跳过 |
| `q2026268.alm` | 2864 | 132 | 3 | 与上行尾部 132 B `cmp` 逐字节相同 |
| `g2026268.alm` | 18303 | 1408 | 32 | 与 `qg` 前 1408 B `cmp` 逐字节相同 |
| NAVCEN `gps_yuma.alm` | 19008 | 1408 | 32 | 另一份 GPS 历书，toa 不同 |
| 仓内 `testdata/qg2026040.alm` | 21168 | 1496 | 34 = 31 GPS + 3 QZSS | GPS PRN 20 `Health: 031` 被跳过 |
| 仓内 `testdata/qg2023058.alm` | 20023 | 1496 | 34 = 31 GPS + 3 QZSS | 文件只有 31 颗 GPS；199 跳过 |

耗时：20 次循环 0.232 s（≈12 ms/次，基本是解释器启动）。首帧十六进制：`b5 62 13 00 24 00 02 00 01 00 58 10 86 0f …`（type=2, version=0, svId=1, almWNa=0x86=134）。

### 3.3 查看输出：`print_ubx.py` 在 pyubx2 1.3.7 下**什么都不打印**

`python print_ubx.py qg2026268.ubx` → stdout 0 行、rc=0，stderr 35 次 `Unknown message type b'\x13\x00', mode GET`。原因：MGA 是输入消息，pyubx2 须 `msgmode=SET`。自己打：

```bash
python -c "from pyubx2 import UBXReader,SET
for r,p in UBXReader(open('qg2026268.ubx','rb'),msgmode=SET,validate=1): print(p)"
```

```text
<UBX(MGA-GPS-ALM, type=2, version=0, svId=1, svHealth=0, e=0.00199508667, almWNa=134, toa=61440, deltaI=0.004440307617, omegaDot=-2.572e-09, sqrtA=5153.6953125, omega0=-0.198251962662, omega=0.051708459854, m0=0.609137773514, af0=0.000162124634, af1=-7e-12, reserved0=0)>
<UBX(MGA-QZSS-ALM, type=2, version=0, svId=2, svHealth=1, e=0.014904499054, almWNa=134, toa=86016, deltaI=-0.03179359436, omegaDot=-8.88e-10, sqrtA=6493.68310546875, omega0=-0.689635157585, omega=-0.495792746544, m0=-0.035623550415, af0=-2.861023e-06, af1=0.0, reserved0=0)>
```

QZSS 帧里 `e=0.0149`、`deltaI=-0.0318` 是**相对值**（加回 0.06 / 0.25 半周才是 0.0749 / 0.2182 半周）。

## 4. 交叉检查（独立实现，05:51 EDT）

方法：自写 YUMA 解析（不 import 工具）；pyubx2 `validate=1` 解帧 + 自写 Fletcher-8 校验和与长度检查；按 M8 规格尺度把字段还原为物理量（角度 ×π 回弧度，QZSS e +0.06、δi +0.25 半周，GPS δi +0.30 半周），与 YUMA 原值逐字段求 |Δ|/LSB。

| 检查 | qg2026268（35 帧） | NAVCEN（32 帧） |
| --- | --- | --- |
| 帧头 `b5 62`、长度 36、校验和 | 35/35 通过 | 32/32 通过 |
| svHealth / almWNa(=week mod 256) / type=2 / version=0 / reserved=0 | 0 不符 | 0 不符 |
| e、toa、δi、af0 max\|Δ\| | 0.0000 LSB | 0.0000 LSB |
| sqrtA / Ω₀ / ω / M₀ max\|Δ\| | 0.0011 / 0.0012 / 0.0013 / 0.0013 LSB | 0.0010 / 0.0013 / 0.0013 / 0.0013 LSB |
| Ω̇ max\|Δ\|（均值） | 0.1299（0.0631）LSB，PRN 195 | 0.1364（0.0711）LSB |
| af1 max\|Δ\|（均值） | 0.0995（0.0463）LSB | 0.0995（0.0506）LSB |

复现脚本骨架（`xcheck.py`，本机自写，未入库）：

```python
msgs=[p for _,p in UBXReader(open(ubx,'rb'),msgmode=SET,validate=1,protfilter=2)]
prn = m.svId if m.identity=='MGA-GPS-ALM' else m.svId+192      # QZSS svId→PRN
phys = (m.deltaI + (0.30 if gps else 0.25))*pi                   # 其余角度字段 ×pi
d_lsb = (phys - yuma[prn]['Orbital Inclination(rad)']) / (2**-19*pi)
```

结论：全部字段 **< 0.14 LSB，远在 1 LSB（取整上限 0.5 LSB）内**。Ω̇ 与 af1 残差偏大是因 YUMA 只印 10 位有效数字（如 `-8.080336578E-09`），源头即非整 LSB，不是工具误差。

卫星位置（自写开普勒传播，YUMA 原值 vs UBX 还原值，同一公式，地固系）：

| 相对 toa | qg2026268 max / mean | NAVCEN max / mean |
| --- | --- | --- |
| 0 s | 0.024 m / 0.010 m | 0.019 m / 0.008 m |
| 3600 s | 0.224 m（PRN 195）/ 0.063 m | 0.136 m / 0.061 m |
| 3 d | 16.06 m / 4.53 m | 10.59 m / 4.40 m |

历书本身精度是 km 级，量化带来的 m 级差可忽略。反例（同一脚本）：若接收机把 QZSS 的 e 当绝对值（不加 0.06），QZS 194/195/196 一日内位置差最大 **5060 km**、均值约 3900 km——所以 e_ref 语义必须对；IS-QZSS-PNT-004 表 5.7.1-3 写明 QZO e_ref=0.06、i_ref=0.25 半周，与源码一致，但 M8 规格未写 e_ref，**接收机端解读未在真接收机测试**。

## 5. 错误用例（全部「合成」，由 `qg2026268.alm` 改写）

| 用例 | 结果 | exit | 输出文件 |
| --- | --- | ---: | --- |
| 空文件 | 静默，0 帧 | 0 | 0 B 文件 |
| 截断（第 5 颗记录中途断） | 先打印 4 行 `Converted…` 再 `KeyError: 'almWNa'` | 1 | **不生成** |
| 缺 `Af1` 行 | `KeyError: 'af1'` | 1 | 不生成 |
| `Eccentricity: 1.5E-O3` / 值为空 | `ValueError: could not convert string to float` | 1 | 不生成 |
| `Af0=0.05 s`（超 I2） | `struct.error: 'h' format requires -32768 <= number <= 32767` | 1 | 不生成 |
| GPS `e=0.04`（超 U2） / QZSS `e=0.05`（<0.06 变负） | `struct.error: 'H' format requires 0 <= number <= 65535` | 1 | 不生成 |
| `toa=1100000`（超 U1） / `sqrtA<0` | `struct.error: 'B' …` / `'I' …` | 1 | 不生成 |
| PRN 0 / 33 / 192 / 203 | `KeyError: 'sat_type'`（未知 PRN 直接崩，不是跳过） | 1 | 不生成 |
| 只有 PRN 199（GEO） | 静默 0 帧 | 0 | 0 B |
| GPS `Health: 063` | 静默跳过 | 0 | 0 B |
| QZSS `Health: 063` | **照样输出** svHealth=63 | 0 | 44 B |
| PRN 01 重复两次 | 后者覆盖前者（af0 170→105），只 1 帧 | 0 | 44 B |
| `week` = 390 / 2438 / 1024 / 0 / −1 / 390.6 | almWNa = 134 / 134 / 0 / 0 / **255** / **135**（负数与小数都不报错） | 0 | 44 B |
| CRLF 行尾 | 正常 | 0 | 44 B |
| 键名 `SQRT(A) (m 1/2)`（少一个空格） | `KeyError: 'sqrtA'` | 1 | 不生成 |
| 含 0xFF 字节 | `UnicodeDecodeError` | 1 | 不生成 |
| 输入不存在 / 输出目录不存在 | `FileNotFoundError`（后者已打印 `Converted…`） | 1 | 不生成 |

规律：任何异常都是 Python traceback + exit 1，且**全有或全无**（写文件在最后）；静默的是「跳过」和「截位」。

## 6. I/O：字段与尺度（MGA-GPS-ALM 与 MGA-QZSS-ALM 同构，payload 36 B）

| 偏移 | 字段 | 类型 | 尺度（单位） | YUMA 行 | 换算 |
| ---: | --- | --- | --- | --- | --- |
| 0/1 | type/version | U1 | 固定 2/0 | — | — |
| 2 | svId | U1 | GPS 1–32；QZSS 1–5 | `ID` | QZSS：PRN−192 |
| 3 | svHealth | U1 | — | `Health` | 原样 |
| 4 | e | U2 | 2⁻²¹ | `Eccentricity` | QZSS 先减 0.06 |
| 6 | almWNa | U1 | 周 | `week` | round(week) mod 256 |
| 7 | toa | U1 | 2¹² s | `Time of Applicability(s)` | ÷4096 |
| 8 | deltaI | I2 | 2⁻¹⁹ 半周 | `Orbital Inclination(rad)` | ÷π 后减 0.30（GPS）/0.25（QZSS） |
| 10 | omegaDot | I2 | 2⁻³⁸ 半周/s | `Rate of Right Ascen(r/s)` | ÷π |
| 12 | sqrtA | U4 | 2⁻¹¹ m^½ | `SQRT(A)  (m 1/2)`（两个空格） | — |
| 16/20/24 | omega0/omega/m0 | I4 | 2⁻²³ 半周 | `Right Ascen at Week` / `Argument of Perigee` / `Mean Anom` | ÷π |
| 28 | af0 | I2 | 2⁻²⁰ s | `Af0(s)` | — |
| 30 | af1 | I2 | 2⁻³⁸ s/s | `Af1(s/s)` | — |
| 32 | reserved | U1[4] | 0 | — | — |

帧 = `b5 62 13 <00|05> 24 00` + payload + CK_A CK_B = 44 B；多帧直接拼接，无文件头。

## 7. 坑

1. **仓名不是目录名**：`jkivilin/ublox8-qzss-almanac-converter` 404，真名 `ublox8-gps-qzss-yuma-almanac-converter`。
2. **GEO 静默丢**：真实文件里 PRN 199/200 没有任何提示就没了；想知道丢了谁，只能数 `Converted` 行。
3. **QZSS 不按健康过滤，GPS 按**：实测 QZSS 官网文件在役星 Health 为 001/016，照样写入 svHealth；接收机如何解读 QZSS svHealth **未在真接收机测试**。
4. **未知 PRN 崩溃而非跳过**：注释写 192–202，代码只认 193–202；IS-QZSS 已规定 196/197 可能改用 203/204，届时整份文件 `KeyError: 'sat_type'` 失败。
5. **stdout 的 `Converted` ≠ 已写盘**：输出在所有星处理完后一次写；中途异常时屏幕已打印若干 `Converted`，文件却不存在。
6. **周数不校验**：负数取模成 255、小数四舍五入成 135，均 exit 0；almWNa 只有 8 位，本身无法区分 256 周倍数，历书时效要自己管。
7. **键名逐字匹配**：`SQRT(A)  (m 1/2)` 中间两个空格；别的 YUMA 生成器少个空格就 `KeyError`。
8. **`print_ubx.py` 在 pyubx2 1.3.7 下静默**：默认 GET 模式不认 MGA 输入消息，要 `msgmode=SET`（§3.3）。
9. **只给历书**：冷启动辅助通常还需时间（MGA-INI-TIME）与位置；本工具不产生，需另配（如 [ubx-mga-rinex-ephemeris](./ubx-mga-rinex-ephemeris.md) 的 `ubx_tool.py send --assist`，同样未在真接收机测试）。

## 8. 未测

- 写入真实 u-blox 8/M8、F9、M10 并观察 MGA-ACK / TTFF：**未在真接收机测试**。
- 通过串口发送 `.ubx` 的任何路径（u-center、`ubx_tool.py send`、自写 pyserial）：未测。
- QZSS svHealth=1/16 在接收机中的效果、QZSS 相对 e 的接收机端解读：未测。
- 与广播星历/精密轨道比较历书位置精度：未测（本篇只证明「转换无损」，不评估历书本身精度）。

## 9. 选型

| 需求 | 用 |
| --- | --- |
| YUMA 历书 → M8 MGA-ALM（GPS+QZSS QZO） | **本工具** |
| RINEX 广播星历 → MGA-GPS/QZSS/GLO/GAL-EPH + 串口发送 | [ubx-mga-rinex-ephemeris](./ubx-mga-rinex-ephemeris.md) |
| 解析 / 生成任意 UBX（含校验本篇输出） | [pyubx2](./pyubx2.md) · Rust：[ublox](./ublox.md) |
| 串口批量下发 CFG 配置 | [pyubxutils](./pyubxutils.md) |
| QZSS L1S 災危通報 DCR/DCX 解码 | [azarashi](./azarashi.md) |
| QZSS L6（CLAS/MADOCA）等原始电文 | [qzsl6tool](./qzsl6tool.md) |
| UBX 原始观测 → RINEX | [ubx2rinex](./ubx2rinex.md) |

30 秒结论：手头只有 QZSS 官网/NAVCEN 的 YUMA、目标是 M8 冷启动历书辅助，用它（先 `cmp` 帧数、确认 GEO 被丢）；要星历或要真发串口，换 ubx-mga-rinex-ephemeris。
