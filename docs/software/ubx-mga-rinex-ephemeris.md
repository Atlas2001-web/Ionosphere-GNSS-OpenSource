# ubx-mga-rinex-ephemeris · RINEX 广播星历 → u-blox UBX-MGA 辅助星历 操作手册

目录：[`PROJECTS.json` → `ubx-mga-rinex-ephemeris`](../../PROJECTS.json) · 上游 <https://github.com/jkivilin/ubx-mga-gnss-rinex-ephemeris-converter> · **无 tag / 无 PyPI**，main tip **`eb0c6e8`**（2026-04-18 14:03 EDT，`Add Galileo (GAL) ephemeris support`）· **MIT** · ★**6** · Python ≥3.10（CI 矩阵 3.10–3.13）· 本机 CPython 3.13.5 + venv：georinex 1.16.2 / numpy 2.5.3 / xarray 2026.7.0 / pyubx2 1.3.7 / pyserial 3.5 · 实测窗口 **2026-09-26 02:35–02:46 EDT**

> 一句话：把公开 RINEX 导航文件（广播星历）转成 u-blox 8/M8 能吃的 **UBX-MGA-*-EPH** 二进制帧，再用自带 `ubx_tool.py` 从串口灌进接收机，缩短冷启动首次定位。两个脚本：`convert_eph.py`（离线转换，本文主角）、`ubx_tool.py`（串口/TCP 发送、复位、测 TTFF、离线 parse）。
> **本机无 u-blox 接收机**：写入接收机、TTFF 改善、M8 以外型号兼容性，全部 **「未在真接收机测试」**。下文所有输出均为本机真跑；人造输入标 **「合成」**。

## 0. 先懂：AssistNow / MGA 辅助数据是什么

- 接收机要定位，除了测伪距，还必须知道每颗卫星**此刻在哪、钟差多少**——这就是**星历**（ephemeris，开普勒根数 + 钟差多项式，GLONASS 为位置/速度向量）。
- **冷启动**时接收机没有星历，只能从卫星信号里慢慢解调：GPS LNAV 电文 50 bit/s，星历在子帧 1–3，每 30 s 一帧重复；信号弱、遮挡、刚上电时解调常失败，首次定位时间（TTFF）因此是几十秒到数分钟。
- **A-GNSS（辅助 GNSS）**：星历先从别处（网络、文件）拿到，直接写进接收机；接收机只需捕获信号、测伪距即可解算，TTFF 可降到秒级。u-blox 把这套输入消息叫 **MGA**（Multiple GNSS Assistance，class `0x13`），官方服务叫 **AssistNow**：Online（服务器实时星历，需 token）、Offline（预测轨道，数天–数周）、Autonomous（接收机自己外推）。
- 本工具 ≈ **离线自制版 Online**：星历来源换成 IGS/BKG 等**公开 RINEX 广播星历**，不需要 u-blox 账号；代价是星历新鲜度取决于你下载的文件（GPS 拟合区间一般 4 h，GLONASS 30 min 更新）。
- 上游 README 自述其作者实测 3D TTFF 27.3 s（本文**未复现**）。

## 1. 用途边界

| 做 | 不做 |
| --- | --- |
| RINEX 2（GPS `.n` / QZSS `.q`）、RINEX 3 MIXED → MGA-GPS/QZSS/GLO/GAL-EPH | **BDS / NavIC / SBAS**：读到也静默丢弃（无 MGA-BDS-EPH） |
| 每文件附 MGA-GPS-HEALTH、MGA-QZSS-HEALTH | 不检查星历相对**当前时间**是否过期（见 §7） |
| 头里有 `GPSA/GPSB`、`GPUT`、`GLUT/GLGP`、`GAGP`、`GAUT` 时附 IONO/UTC/TIMEOFFSET | 不支持 RINEX 4 的 `> ION`/`> STO` 记录，CNAV 会被当 LNAV 误编（§7） |
| `.gz` 输入自动解压；多文件合并输出 | 不收 `.zip` / `.Z` / `.crx`；不生成历书（→ 同作者 `ublox8-qzss-almanac-converter`） |
| `ubx_tool.py send --assist` 前置 MGA-INI 时间+位置 | 不做 F9/M10 专门适配（上游只写 u-blox 8/M8） |

## 2. 安装

```bash
mkdir -p /tmp/mgarnx-man && cd /tmp/mgarnx-man
git clone https://github.com/jkivilin/ubx-mga-gnss-rinex-ephemeris-converter up   # eb0c6e8
python3 -m venv venv && . venv/bin/activate
export PIP_CACHE_DIR=/tmp/mgarnx-man/pipcache          # 共享机器：缓存放自己目录
pip install -r up/requirements.txt pytest              # georinex>=1.16 numpy pyubx2>=1.2.38 pyserial>=3.5
cd up && python -m pytest -q                           # → 337 passed in 11.24s（README 仍写 253 tests）
```

无 `setup.py`/`pyproject`，不装成命令：一律 `python convert_eph.py …` / `python ubx_tool.py …`。

## 3. 命令与真实输出

### 3.1 `convert_eph.py -h`（本机原文，exit 0）

```text
usage: convert_eph.py [-h] -o OUTPUT [--time DATETIME] [--max-age HOURS]
                      [--systems SYSTEMS] [--all-epochs] [--verbose]
                      input [input ...]
  -o, --output OUTPUT  Output UBX binary file
  --time DATETIME      Target time for epoch selection (ISO format, e.g.
                       2026-02-07T16:00). Default: latest available epoch.
  --max-age HOURS      Maximum ephemeris age in hours (default: 4.0, GLONASS
                       capped at 1.0)
  --systems SYSTEMS    Comma-separated GNSS systems to include (default:
                       GPS,QZSS,GLO,GAL)
  --all-epochs         Output all epochs, not just the best per satellite
  --verbose, -v        Show per-satellite conversion details
```

`ubx_tool.py -h`：`port {poll,dump-dbd,dump-eph,send,reset,ttff,monitor,enable-ubx,parse,decode-eph}`，全局 `--tcp` `--baud`（默认 115200）`--timeout`（默认 3 s）。离线只能用 `parse` / `decode-eph`。

### 3.2 真实数据：BKG 公开 BRDC（免账号）

```bash
curl -O https://igs.bkg.bund.de/root_ftp/IGS/BRDC/2026/268/BRDC00WRD_R_20262680000_01D_MN.rnx.gz   # 1220113 B
python convert_eph.py BRDC00WRD_R_20262680000_01D_MN.rnx.gz -o d268.ubx -v      # 2.15 s，exit 0
```

```text
Loading data/BRDC00WRD_R_20262680000_01D_MN.rnx.gz...
  Satellites: 93, epochs: 327
  Time range: 2026-09-24T00:00:00.000000000 to 2026-09-25T23:50:00.000000000
  GPS health: all 32 healthy
  QZSS health: all 5 healthy

Converted 95 messages for 93 satellites (6856 bytes) to out/d268.ubx
  Including: GPS-HEALTH, QZSS-HEALTH
 G01 2026-09-25T22:00:00.000000000   645  511200   5153.7470 0.0019889202
 E05 2026-09-25T23:50:00.000000000    101  517800   5440.6074 0.0002529490
 R01 2026-09-25T23:45:00.000000000    -8540.116   -23773.543    -3574.392 -1.8688757e-04
```

该文件（RINEX 3.05，gfzrnx 合并）记录数：E 6222 / S 12068 / R 1324 / C 1000 / G 407 / J 122 / I 110——C/S/I **全部静默丢弃**。pyubx2 1.3.7（`msgmode=SET`）逐帧解码输出，帧数/字节与工具自报一致：

| UBX-MGA 子类型 | 帧 | 字节 | B/帧 |
| --- | ---: | ---: | ---: |
| MGA-GPS-EPH | 32 | 2432 | 76 |
| MGA-GAL-EPH | 30 | 2520 | 84 |
| MGA-GLO-EPH | 26 | 1456 | 56 |
| MGA-QZSS-EPH | 5 | 380 | 76 |
| MGA-GPS-HEALTH | 1 | 48 | 48 |
| MGA-QZSS-HEALTH | 1 | 20 | 20 |
| **合计** | **95** | **6856** | |

**没有 IONO/UTC**：BKG 这份 3.05 头里只有 `LEAP SECONDS`，没有 `IONOSPHERIC CORR` / `TIME SYSTEM CORR`。

### 3.3 其它真实文件（全部 exit 0）

| 输入 | 帧 / 字节 | 子类型要点 |
| --- | --- | --- |
| BKG `BRDC00WRD_R_2026269…`（当日滚动，末历元 2026-09-26T08:00） | 94 / 6800 | GLO 25，余同上 |
| BKG `BRDC00WRD_S_2026268…`（BNC 实时流汇编） | 95 / 6856 | 与 R 文件同构 |
| ESBC `ESBC00DNK_R_20201770000_01D_MN.rnx.gz`（2020，头含 GPSA/GPSB/GPUT/GAGP/GAUT） | 61 / 3992 | GPS 31、GLO 23、QZSS 3、**GPS-IONO 24 B、GPS-UTC 28 B**；**GAL 0**（§7 坑 6） |
| RINEX 2 `brdc0010_rinex_v2.22n`（CDDIS 头，GPS） | 33 / 2480 | GPS 32 + HEALTH |
| RINEX 2.12 `brdc0400.26n`+`.26q`（上游 testdata，QZSS 官方站） | 37 / 2628 | GPS 28、QZSS 5、IONO、UTC、两份 HEALTH |
| RINEX 4.00 `BRD400DLR_S_20240010000_01D_MN.rnx`（DLR） | 88 / 6304 | 看似成功，**实为误编**（坑 5） |
| 同 BKG 268 + `--time 2026-09-25T12:00` | 84 / 6024 | GPS 24、GAL 28、GLO 25、QZSS 5 |
| 同 BKG 268 + `--all-epochs` | 3943 / 290504 | GPS 320（原 407 记录）、GAL 2175（原 6222，I/F-NAV 与同 toc 去重）、GLO 1324、QZSS 122 |

`python ubx_tool.py - parse d268.ubx` → exit 0，逐帧打印 95 条 pyubx2 对象，顺序 **E→G→J→R，HEALTH 在最后**（按卫星标签字母排序）。

## 4. 字段对照（RINEX 原值 vs 输出帧解码，BKG 268）

做法：按 pyubx2 的 MGA 载荷定义逐字段取**原始整数**，自己乘精确 2 的幂 LSB（半圆 ×π → rad），与 RINEX 文本逐项相减。另列 pyubx2 属性值（它会四舍五入，见坑 12）。

| 字段 | G01 RINEX | G01 解码 | E05 RINEX | E05 解码 | 最大 \|误差\|/LSB |
| --- | --- | --- | --- | --- | ---: |
| toe | 511200 s | 511200 s（LSB 16 s） | 517800 s | 517800 s（LSB 60 s） | 0 |
| toc | 511200 s | 511200 s | 517800 s | 517800 s | 0 |
| √A | 5153.746959686 √m | 误差 2.8×10⁻¹⁰ | 5440.607383728 √m | 误差 2.7×10⁻¹¹ | 1.5×10⁻⁴ |
| e | 1.988920150325×10⁻³ | 误差 3.0×10⁻¹⁶ | 2.529489574954×10⁻⁴ | 误差 8.6×10⁻¹⁸ | <10⁻⁵ |
| M₀ | −1.851950852729 rad | 误差 4.3×10⁻¹³ | −1.145088902212 rad | 误差 8.7×10⁻¹⁴ | 3×10⁻⁴ |
| Δn | 4.336252050875×10⁻⁹ rad/s | 误差 3.5×10⁻²² | 3.466573028632×10⁻⁹ rad/s | 误差 6.1×10⁻¹⁷ | 1.7×10⁻⁴ |
| Ω₀ / i₀ / ω | 逐项 | ≤5×10⁻¹³ rad | 逐项 | ≤5×10⁻¹³ rad | 3.4×10⁻⁴ |
| Ω̇ / IDOT | −7.9189×10⁻⁹ / −4.0645×10⁻¹⁰ rad/s | ≤4.3×10⁻²² | −6.0499×10⁻⁹ / −1.7322×10⁻¹⁰ rad/s | ≤5.5×10⁻¹⁸ | 1.5×10⁻⁵ |
| Cuc/Cus/Cic/Cis | 逐项 | ≤1.1×10⁻¹⁸ rad | 逐项 | ≤1.8×10⁻¹⁹ rad | <10⁻⁹ |
| Crc / Crs | 167.71875 / −73.0625 m | 0 | 311.59375 / −55.84375 m | 0 | 0 |
| af0 | 1.638713292778×10⁻⁴ s | 误差 4.6×10⁻¹⁷ | 6.590283010155×10⁻⁵ s | 误差 3.8×10⁻¹⁹ | <10⁻⁶ |
| af1 | −8.867573342286×10⁻¹² s/s | 误差 5×10⁻²⁶ | 2.629008122312×10⁻¹² s/s | 误差 4×10⁻²⁵ | 3×10⁻¹¹ |
| TGD / BGD(E1,E5b) | −8.8476×10⁻⁹ s | 误差 4.6×10⁻²³ | 1.3970×10⁻⁹ s（原始整数 6 × 2⁻³²） | 误差 2.2×10⁻²² | <10⁻¹¹ |
| IODC / IODnav | 645（IODE 133 = 645 & 0xFF） | 645 | 101 | 101 | 0 |

结论：两星 22 个字段 **|误差| ≤ 3.4×10⁻⁴ LSB**，即广播值本就在 ICD 网格上，转换**无损**。附带核对：G01 `SVacc` 2.0 m → `uraIndex` 0；E05 SISA 3.12 m → `sisaIndexE1E5b` 107（100 + (3.12−2)/0.16）；GLO R01 x/y/z = −8540.1162109375 / −23773.54345703125 / −3574.3916015625 km 与 RINEX 一致，`tau` = −SVclockBias = −1.868875697×10⁻⁴ s，`tb` 原始 11（02:45 MSK = 23:45 UTC + 3 h），`H`=频道号 1；ESBC `GPS-UTC` utcA1 原始整数 3 → 2.6645×10⁻¹⁵ s/s，与头 `GPUT` 2.664535259E-15 相符。

## 5. 错误用例（本机；人造输入标「合成」）

| 情形 | exit | 真实行为 |
| --- | ---: | --- |
| RINEX 2 / 2.12（GPS、QZSS） | 0 | 正常（georinex 或内置解析器） |
| RINEX 3.05 MIXED（含 C/S/I） | 0 | G/J/R/E 转换，C/S/I 无提示丢弃 |
| RINEX 4.00 DLR | 0 | GPS CNAV / QZSS CNV2 被当 LNAV 编码，32 颗 GPS 中 **21 颗** health≠0（1/7/63）；合成「只保留 LNAV」版本 → 仅 G01/G27=63（该日真不健康） |
| `--systems BDS` | 1 | `No ephemeris data converted.` |
| 过期：ESBC 2020 默认模式 | 0 | 照常输出 2020 星历，无任何警告 |
| `--time 2026-09-27T12:00`（未来）/ `--time 2026-09-26T06:40`（当前 UTC，距末历元 6.8 h） | 1 | `No ephemeris data converted.` |
| `--time yesterday` | 1 | `Error: invalid time format: yesterday` |
| 合成：空文件 / 只有头 | 1 | `Error: Could not parse … (unsupported RINEX format)` |
| 合成：`head -c 4800000` 截断（停在 GPS 区中间） | 0 | 45 帧 3632 B：GAL 30、GPS **14**、无 GLO/QZSS，无警告 |
| 合成：G01 22:00 记录 Toe 改成 `XXXX` | 0 | 该记录静默丢弃，G01 退回 20:00（IODC 644），无警告 |
| 合成：G01 Cis 改成 9999 rad | 0 | **饱和**到 I2 上限 32767×2⁻²⁹ = 6.1033×10⁻⁵，无警告 |
| 合成：256 字节随机二进制 | 1 | `'utf-8' codec can't decode byte 0x80` |
| 上游 `brdc0400.26.zip` 直接喂 | 1 | 同上 utf-8 错（不认 zip） |
| 合成：gzip 但文件名无 `.gz` | 1 | `can't decode byte 0x8b`（只按后缀判断） |
| 合成：截断 `.rnx.gz` | 1 | Python traceback `EOFError: Compressed file ended…` |
| ESBC OBS `.crx` / `.crx.gz` | 1 | georinex 当观测文件读完后 traceback `KeyError: "No variable named 'sqrtA'…"`（明显慢：本批 13 个用例共 133 s，其余均秒级） |
| 不存在的输入 | 1 | `Error: [Errno 2] No such file or directory` |
| `-o /nonexist/x.ubx` | 1 | 转换完才 traceback `FileNotFoundError` |
| 好文件 + 空文件 两个输入 | 0 | 坏的打印 Error 后跳过，照常输出 95 帧 |

## 6. 输入 / 输出

| 项 | 内容 |
| --- | --- |
| 输入 | RINEX 2 NAV（`.YYn`/`.YYq`）、RINEX 3 NAV（`*_MN.rnx`）；可 `.gz`；可多个 |
| 输出 | `-o` 指定的裸 UBX 二进制：`B5 62 13 id len payload CK_A CK_B` 连续拼接，无文件头 |
| 帧长 | GPS/QZSS-EPH 76 B（载荷 68）、GAL-EPH 84 B、GLO-EPH 56 B、GPS-HEALTH 48 B、QZSS-HEALTH 20 B、GPS-IONO 24 B、GPS-UTC 28 B |
| 顺序 | 星历按标签排序（E、G、J、R），再 HEALTH → IONO → UTC → GLO/GAL 时间偏差 |
| stdout | 只打印输出文件名（便于脚本）；统计/逐星表走 **stderr** |
| 选历元 | 默认：每星**最新**有效记录；`--time`：离目标最近且 ≤`--max-age`（GLO ≤1 h）；`--all-epochs`：全部 |
| 物理单位 | 角度字段在帧里是**半圆**（×π 得 rad）；GAL toe/toc LSB 60 s，GPS 16 s |

## 7. 坑

1. **默认模式无视 `--max-age`**：不给 `--time` 就取每星最后一条，不管多旧。BKG 268 实测 G10 选了 2026-09-24T10:00（距文件末 37.8 h）、R26 选了 06:45（GLONASS 旧 17 h）。要卡时效就**总是带 `--time`**。
2. **不看系统时钟**：2020 年 ESBC 照转不误、exit 0。灌进接收机前自己确认 toe 在 ±2 h 内。
3. **用昨天的日文件就过期**：02:40 EDT（06:40 UTC）对 268 文件 `--time` 当前 → exit 1。应拉当日滚动文件（BKG 269 每小时更新，末历元已到 08:00 UTC）。
4. **BKG BRDC 头无电离层/UTC 参数** → 输出没有 GPS-IONO/UTC/GAL-UTC；需要时并一个头里有 `GPSA/GPUT` 的测站 NAV（如 ESBC 类文件）一起输入。
5. **RINEX 4 会静默误编**：工具不看 `> EPH Gxx CNAV` 类型行，取最新记录，CNAV 字段错位进 MGA-GPS-EPH（G01：toe 116992 不在整点、health 7、IODC 7）。RINEX 4 先滤成只含 LNAV，或改用 RINEX 3。
6. **georinex 读某些文件 Galileo 全 NaN**：ESBC 24 颗 E 星进了数据集但 √A 全 NaN，工具的回退只在「返回 None」时触发 → **0 帧 GAL-EPH 且无提示**；内置解析器单独读同文件，E01 就有 16 个有效历元。输出后务必数一遍子类型。
7. **BDS/SBAS/NavIC 无输出也无提示**，`--systems BDS` 只得 exit 1。
8. **坏字段不报错**：非数字 → 整条记录丢弃并退回旧历元；超量程 → 饱和截断。都 exit 0。
9. **截断文件 exit 0**：按 C→E→G→I→J→R→S 顺序，截在 GPS 段就丢掉 GLO/QZSS。
10. **压缩只认 `.gz` 后缀**：zip、`.Z`、`.crx`、无后缀 gzip 均失败；截断 gz 和 `-o` 目录不存在都是裸 traceback。
11. **pyubx2 解 MGA 必须 `msgmode=SET`**：默认 GET 模式 → `UBXMessageError: Unknown message type b'\x13\x02', mode GET`。
12. **pyubx2 属性值被 `SCALROUND` 四舍五入**：G01 af1 显示 −9e-12（真值 −8.8676×10⁻¹²，差 1.5%）、E05 af1 显示 3e-12（真值 2.629×10⁻¹²，差 14%）、IDOT 差约 0.3%、ESBC utcA1 显示 0.0；且 `bgdE1E5b` 不乘 2⁻³²（显示 6）。做误差分析要自己从原始整数换算。
13. **不健康卫星照样写入**：R27 health 4 → `B=4` 原样进帧；QZSS HEALTH 里 1/16 是 L1C/A、L1C/B 互斥位，工具判「healthy」。
14. **GPS-UTC 的 WNlsf、DN 写 0**（RINEX 头不带），跨闰秒公告期慎用。
15. **`--time` 是朴素时间**：直接与 RINEX 历元标签比（GPS/GAL 为 GPST/GST，GLO 为 UTC），不做时区/闰秒换算（读源码所得）。
16. 上游 README 自报 253 tests、示例 `URA=2.0m(idx=1)`；本机 main 为 337 passed、2.0 m → idx 0（后者符合 ICD）。以本机为准。

## 8. 选型

| 你要… | 用 | 说明 |
| --- | --- | --- |
| 零维护、最新星历/预测轨道灌 u-blox | u-blox 官方 **AssistNow** Online/Offline | 需 token；覆盖 BDS；本仓无手册 |
| 无账号、离线、自带 RINEX 生成 MGA 星历 | **本工具** | GPS/QZSS/GLO/GAL；8/M8 |
| 在 Python 里自己拼/解 UBX（含 MGA） | [pyubx2](./pyubx2.md) | 本文用它解码；注意 SET 模式与四舍五入 |
| 批量下发 CFG 配置、存载 `.ubx` | [pyubxutils](./pyubxutils.md) | `ubxload` 只认 CFG-VALSET，不是 MGA 灌注工具 |
| Rust 程序里编解码 UBX | [ublox](./ublox.md)（ublox-rs） | 纯库，无 RINEX 输入 |
| RINEX NAV → BINEX | [rinex2bin](./rinex2bin.md) | 方向不同：存档/交换，不给接收机 |
| 反方向：UBX 流 → RINEX OBS/NAV | [ubx2rinex](./ubx2rinex.md) | 可把接收机真实星历导成 RINEX 再与本工具对照 |
| 只读 RINEX 进 xarray | [georinex](./georinex.md) | 本工具的底层解析器之一 |

## 9. 未测 / 相关

- **未在真接收机测试**：`ubx_tool.py send/reset/ttff/poll/dump-dbd/dump-eph/monitor/enable-ubx`、`--tcp` 模式、MGA-ACK 回应、实际 TTFF、F9/M10 兼容性。
- 未测：QZSS 官方站当日文件在线下载（只用了上游 testdata 内 2026-02-09 的真实文件）；`decode-eph`（需 AID-EPH 抓包）。
- 数据来源：BKG `igs.bkg.bund.de/root_ftp/IGS/BRDC/`（HTTP 目录，免登录）；ESBC 与 [rinex2bin](./rinex2bin.md)/[rnx2cggtts](./rnx2cggtts.md) 同源；RINEX 2/4 样例取自本机其它项目测试数据。
- 同作者历书版：`ublox8-qzss-almanac-converter`（YUMA → MGA-GPS/QZSS-ALM，PROJECTS 已登记，本仓暂无手册）。
