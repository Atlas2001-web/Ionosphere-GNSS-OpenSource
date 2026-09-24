# gps-measurement-tools · Google GNSS Logger 套件操作手册

目录：[`PROJECTS.json` → `gps-measurement-tools`](../../PROJECTS.json) · 上游 <https://github.com/google/gps-measurement-tools> · 许可 **Apache-2.0** · tip **`ab1aebb`** · 本机验证：clone 仓内 `demoFiles` → [android_rinex](./android_rinex.md) → RINEX3 → [georinex](./georinex.md) 探活（2026-09-24 EDT）。**无本机 MATLAB/Octave**，MATLAB WLS 路径标操作步骤、不臆造图窗。

> 岗位：手机 **GnssLogger** 落盘原始测量 +（可选）桌面 MATLAB 伪距/WLS 分析。冲突时：**上游 README / `LOGGING_FORMAT.md` / 本机 `gnsslogger_to_rnx -h` > 本文**。转 RINEX 主力 → [android_rinex](./android_rinex.md)；教学 NavData → [gnss_lib_py](./gnss_lib_py.md)。

## 1. 用途与边界

**做：**

- Android **GNSSLogger** App（仓内 `GNSSLogger/` Android Studio 工程；也可下官方 APK）录 `Raw,/Fix,/Nav,/Status,…`
- MATLAB `opensource/`：读 Logger、算伪距、C/No、WLS PVT、可选载波 ADR
- 仓内 `demoFiles/` 两份样例日志 + 小时星历 `*.16n`，可离线跑通读盘

**不做：**

- **不是** Logger→RINEX 转换器 → [android_rinex](./android_rinex.md)
- **不是** 测绘 PPP/RTK 引擎 → [rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)
- **不是** 校准 TEC → [pytecgg](./pytecgg.md)（多数手机日志仅 L1）
- **不是** 桌面串口/NTRIP GUI → [pygpsclient](./pygpsclient.md) / [bnc](./bnc.md)

一句话：Google 套件 = **手机原始测量采集规范 + MATLAB 教学分析**；进经典 GNSS/TEC 流水线先过 [android_rinex](./android_rinex.md)。

| 术语 | 含义 |
| --- | --- |
| `Raw,` | 一条 GnssMeasurement；含 `TimeNanos`/`FullBiasNanos`/`Svid`/`Cn0DbHz`/ADR… |
| `FullBiasNanos` | 硬件钟相对 GPS 的偏差；跳变→伪距台阶 |
| duty cycle | 为省电间歇开射频；样例小日志 **无可用载波**（`L1C` 全 0） |
| ADR | Accumulated Delta Range；`AccumulatedDeltaRangeState` 无效则相位可疑 |
| `ProcessGnssMeasScript.m` | MATLAB 入口：设 `dirName`/`prFileName` 后一键跑 |

## 2. 安装

### 2.1 源码（日志格式 + MATLAB + App 工程）

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/google/gps-measurement-tools.git
cd gps-measurement-tools
git rev-parse --short HEAD   # 本机：ab1aebb
ls opensource/demoFiles/
# 期望含：pseudoranges_log_2016_06_30_*.txt 与 *_08_22_*.txt
```

### 2.2 手机 GnssLogger

1. 用 Android Studio 打开 `GNSSLogger/` 编译，或装官方/发行 APK（以当前 Google/开发者页为准）。
2. 开 **Force full GNSS measurements**（开发者选项；因机而异）。
3. 录一段 → 拷出 `gnss_log_*.txt`（或 App 导出名）。
4. 头一行应对得上仓内 `LOGGING_FORMAT.md` 的 `Raw,` 列名。

### 2.3 MATLAB 分析（有许可证时）

```matlab
addpath('~/iono_ops/gps-measurement-tools/opensource');
% 编辑 ProcessGnssMeasScript.m：
%   dirName = '.../opensource/demoFiles';
%   prFileName = 'pseudoranges_log_2016_06_30_21_26_07.txt';
ProcessGnssMeasScript
```

无 MATLAB：本手册用 **android_rinex + georinex** 走同一份 demo（§3）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `ReadGnssLogger` 空 | `dirName`/`prFileName` 路径错 | 改绝对路径；`ls` 确认文件 |
| 星历 FTP 失败 | CDDIS 旧 FTP 已退役 | 手持 RINEX NAV 放同目录，脚本会本地读 |
| App 无 Raw | 机型/系统阉割 API | 换支持原始测量的机；或只用 `Fix,/Status,` |

## 3. 端到端：demo 日志 → RINEX → georinex（本机真跑）

样本（duty cycle、**无载波**）：`opensource/demoFiles/pseudoranges_log_2016_06_30_21_26_07.txt`（`Raw` 1379 / `Fix` 216）。

### 3.1 看输入

```bash
cd ~/iono_ops/gps-measurement-tools
head -n 6 opensource/demoFiles/pseudoranges_log_2016_06_30_21_26_07.txt
python3 - <<'PY'
from collections import Counter
from pathlib import Path
p=Path('opensource/demoFiles/pseudoranges_log_2016_06_30_21_26_07.txt')
c=Counter(l.split(',',1)[0] for l in p.open() if l.strip() and not l.startswith('#'))
print(dict(c), 'bytes', p.stat().st_size)
PY
# 期望：{'Fix': 216, 'Raw': 1379} bytes 297697；头含 Version: 1.4.0.0
```

### 3.2 转 RINEX（android_rinex）

```bash
# 假定已按 android_rinex 手册装好 gnsslogger_to_rnx
mkdir -p ~/iono_ops/gmt_e2e
gnsslogger_to_rnx \
  -o ~/iono_ops/gmt_e2e/gmt_demo.16o \
  -m GMTD -n 'gmt-e2e' -a 'Ionosphere-GNSS-OpenSource' \
  --integerize \
  ~/iono_ops/gps-measurement-tools/opensource/demoFiles/pseudoranges_log_2016_06_30_21_26_07.txt \
  2> ~/iono_ops/gmt_e2e/stderr.txt
echo EXIT:$?
wc -l ~/iono_ops/gmt_e2e/gmt_demo.16o ~/iono_ops/gmt_e2e/stderr.txt
head -n 16 ~/iono_ops/gmt_e2e/gmt_demo.16o
```

**本机（andrnx @ android_rinex `8ea7ab7`，2026-09-24 EDT）：**

```text
EXIT:0
1617 .../gmt_demo.16o
1379 .../stderr.txt
     3.03           O                   M                   RINEX VERSION / TYPE
GMTD                                                        MARKER NAME
SMARTPHONE                                                  MARKER TYPE
G    4 C1C L1C D1C S1C                                      SYS / # / OBS TYPES
  2016    06    30    21    26    25.0000000                TIME OF FIRST OBS
  2016    06    30    21    30    08.0000000                TIME OF LAST OBS
```

### 3.3 georinex 探活 + 载波对照

```bash
python -W ignore - <<'PY'
import georinex as gr, numpy as np
obs = gr.load("~/iono_ops/gmt_e2e/gmt_demo.16o".replace("~", __import__("os").path.expanduser("~")), use="G")
L = obs["L1C"].values
print(gr.__version__, dict(obs.dims), "L1C_zeros", int(np.nansum(L==0)))
print(obs.time.values[0], "->", obs.time.values[-1])
PY
```

**本机 georinex 1.16.2：** `time=223, sv=9`；**`L1C_zeros=1379`（全零）** —— 与脚本注释 *with duty cycling, no carrier phase* 一致。

有载波样例（同目录 `pseudoranges_log_2016_08_22_14_45_50.txt`，`Raw` 5041）：

```bash
gnsslogger_to_rnx -o ~/iono_ops/gmt_e2e/gmt_phase.16o -m GMTP --integerize \
  .../pseudoranges_log_2016_08_22_14_45_50.txt 2> ~/iono_ops/gmt_e2e/stderr_phase.txt
# 本机：EXIT:0；georinex time=207 sv=12；L1C zeros=775 / nonzero=1709
```

### 3.4 MATLAB（有环境时；本机未跑）

```matlab
dirName = '~/iono_ops/gps-measurement-tools/opensource/demoFiles';
prFileName = 'pseudoranges_log_2016_08_22_14_45_50.txt';  % 有载波
param.llaTrueDegDegM = [37.422578, -122.081678, -28];     % Charleston Park
% 再跑 ProcessGnssMeasScript.m → 伪距/CNo/PVT/ADR 图
```

期望：`ReadGnssLogger` 非空；星历可用后出 WLS 轨迹。本机无 MATLAB → **不伪造图窗**。

## 4. I/O 字段

| 侧 | 路径/字段 | 说明 |
| --- | --- | --- |
| 入 | `*.txt` Logger | 必需 `Raw,`；见 `LOGGING_FORMAT.md` |
| 入 | `Fix,/Status,/Nav,/NMEA,/Agc,…` | 分析/融合用；android_rinex 主吃 Raw |
| 出 | MATLAB 结构 `gnssRaw` | `TimeNanos`/`Svid`/`allRxMillis`… |
| 出 | RINEX OBS（经 android_rinex） | 样例 `C1C L1C D1C S1C`；`MARKER TYPE=SMARTPHONE` |
| 辅 | `hour*.16n` | demo 用 RINEX2 NAV；CDDIS 现多走 HTTPS |

列名随 Android 版本增删（`AgcDb`、`BasebandCn0DbHz`、独立 `Agc,` 行）。**新日志先 `head` 对照 `LOGGING_FORMAT.md`。**

## 5. 接到哪步

```text
手机 GnssLogger（本文 App）
  → 原始 *.txt
  → android_rinex → RINEX OBS → georinex 探活
  →（教学）gnss_lib_py / laika / rtklib 单频
  →（仅双频日志）gnss-tec / pytecgg
  → MATLAB ProcessGnssMeasScript（伪距/WLS 课）
```

路径 C 实时板卡流走 [pygpsclient](./pygpsclient.md)/[pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)，**不是** Logger CSV。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | RINEX `L1C` 全 0 | duty cycle / ADR 无效 | 换「无 duty cycle」日志；或 `AccumulatedDeltaRangeState` 过滤 |
| 2 | `android_rinex` 警告上千仍 EXIT:0 | 逐条测量跳过属正常 | 看 OBS 历元数，勿以警告判失败 |
| 3 | MATLAB 星历空 | 旧 `ftp://cddis…` 失效 | 手下 NAV 放 `dirName`；或改 HTTPS 客户端 |
| 4 | 新手机日志解析炸 | `Raw,` 列增删 | 对照 `LOGGING_FORMAT.md`；升/换转换器 |
| 5 | 只有 L1 却要 TEC | 消费机常见单频 | 换双频机/CORS；见 [data-access](../data-access.md) |
| 6 | `APPROX POSITION` 全 0 | Logger 未写天线坐标 | 定位端先验或先单点 |
| 7 | GPSTest 导出转失败 | 方言≠GnssLogger | 改用官方 Logger 或确认 `Raw,`+`ConstellationType` |
| 8 | 把本套件当 RINEX 工具 | 仓内无转 OBS CLI | `pip`/`clone` [android_rinex](./android_rinex.md) |
| 9 | WLS 与芯片位置差很大 | 未滤差测量 / 无真值 | 用 `SetDataFilter`；填 `llaTrueDegDegM` |
| 10 | 载波残差乱 | ADR 状态位未检 | 先画 `PlotAdr`；无效状态丢弃 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 手机录原始测量（官方格式） | **gps-measurement-tools / GnssLogger（本文）** |
| Logger → RINEX3 | [android_rinex](./android_rinex.md) |
| Android/多源 → NavData / 教学 WLS | [gnss_lib_py](./gnss_lib_py.md) |
| 外置板卡串口/NTRIP GUI | [pygpsclient](./pygpsclient.md) |
| 多流录盘 | [bnc](./bnc.md) |
| RINEX 探活 | [georinex](./georinex.md) |

相关：上游 README · `LOGGING_FORMAT.md` · [android_rinex](./android_rinex.md) · [gnss_lib_py](./gnss_lib_py.md) · [georinex](./georinex.md) · [pygpsclient](./pygpsclient.md) · 教程 [06](../tutorials/06-iono-positioning.md)
