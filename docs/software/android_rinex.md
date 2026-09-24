# android_rinex · GnssLogger → RINEX 操作手册

目录：[`PROJECTS.json` → `android_rinex`](../../PROJECTS.json) · 上游 <https://github.com/rokubun/android_rinex> · 包名 **`andrnx`**（`setup.py` `0.1`）· 本机验证 clone **`8ea7ab7`**（2020-06-24）+ 仓内样例 `data/pseudoranges_log_2017_07_17_13_46_25.txt` 实跑

> 岗位：把 Google **GnssLogger**（及兼容 CSV 原始测量）转成 **RINEX 3 OBS**，衔接手机数据与经典 GNSS/TEC 流水线。冲突时：**本机 `gnsslogger_to_rnx -h` / 上游 README > 本文**。

## 1. 用途与边界

**做：**

- Android GnssLogger `Raw,` 行 → RINEX **3.03** 观测文件（`O` / Mixed）
- 写入伪距 / 载波 / 多普勒 / CN0（样例为 **L1：`C1C L1C D1C S1C`**；源码亦认 GPS/GAL **L5/E5a** 等频点，取决于日志是否记录）
- 可选：站名 / 观测者 / 机构头、`--integerize` 整秒历元、`--fix-bias` 固定首个 `FullBiasNanos`、`--filter-mode sync|trck`

**不做：**

- **不是** 厂商接收机 RAW→RINEX 台网入库 → [autorino](./autorino.md)
- **不是** 读盘探活 / xarray → [georinex](./georinex.md)；**不是** 校准 sTEC → [pytecgg](./pytecgg.md)
- **不产出** NAV（`.yyN`/`.rnx` 导航）；定位/TEC 另备广播星历或精密产品
- **不保证** 双频 TEC：多数消费机日志只有 L1；样例 OBS **无 L2/L5 列**，不能直接喂双频几何无关 TEC
- 不替代 RTKLIB/PRIDE 里的天线/钟差模型；手机天线相位中心与 duty-cycle 须在定位端另处理

一句话：android_rinex = **手机原始测量 → 可被经典工具读的 RINEX OBS 适配器**。

| 术语 | 含义 |
| --- | --- |
| GnssLogger | Google GPS Measurement Tools App 落盘的 CSV（`Raw,` / `Fix,` / `Nav,`） |
| `FullBiasNanos` | 硬件钟相对 GPS 的偏差；跳变会导致伪距台阶 → `--fix-bias` |
| ADR | Accumulated Delta Range（载波）；`ADR_STATE_VALID` 无效则相位可疑 |
| OSN | GLONASS orbital slot number；缺 OSN 的 R 星本工具直接跳过 |
| `filter-mode sync` | 更严：TOW 已知、码锁定、无模糊、其余信号标志齐（默认） |
| `filter-mode trck` | 较松：TOW 已知、码锁定、无模糊即可 |

## 2. 安装

无 PyPI 发行；从 GitHub clone 后 `pip install -e .`（注册脚本 `gnsslogger_to_rnx`）。

```bash
cd ~/iono_ops
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
git clone --depth 1 https://github.com/rokubun/android_rinex.git
cd android_rinex
python -m pip install -e .
gnsslogger_to_rnx -h | head -n 5
# 期望：usage: gnsslogger_to_rnx [-h] [--output <output rinex file>] ...
python -c "import andrnx; print(andrnx.__file__)"
# 期望：.../android_rinex/andrnx/__init__.py
```

纯开发也可：`export PYTHONPATH=$PWD` 后直接跑 `bin/gnsslogger_to_rnx`（本机两种方式均可用）。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `gnsslogger_to_rnx: command not found` | 未 `pip install -e .` 或 venv 未激活 | 激活 venv；或 `PYTHONPATH=$PWD bin/gnsslogger_to_rnx` |
| `No module named 'andrnx'` | 只拷了 `bin/` | 在仓根安装或设 `PYTHONPATH` |
| 输入是 GPSTest 导出 | 列名/方言可能不同 | 确认含 `Raw,` 与 `ConstellationType`；否则先用官方 GnssLogger |

## 3. 端到端：仓内样例 → RINEX 3.03（本机真跑）

样本：Nexus 9 / GnssLogger **1.4.0.0**，约 23 min，`Raw` 23290 行（仓内自带，无需外网）。

### 3.1 看一眼输入

```bash
cd ~/iono_ops/android_rinex
head -n 8 data/pseudoranges_log_2017_07_17_13_46_25.txt
wc -l data/pseudoranges_log_2017_07_17_13_46_25.txt
# 期望：28752；头含 Version / Raw,ElapsedRealtimeMillis,...ConstellationType
```

**本机（2026-09-24 EDT）头几行要点：**

```text
# Version: 1.4.0.0, Platform: N
# Raw,ElapsedRealtimeMillis,TimeNanos,...,ConstellationType
```

### 3.2 转换（推荐写头 + 整秒）

```bash
mkdir -p ~/iono_ops/android_out
gnsslogger_to_rnx \
  -o ~/iono_ops/android_out/nex9_lab.17o \
  -m NEX9 -n 'lab-demo' -a 'Ionosphere-GNSS-OpenSource' \
  --integerize \
  data/pseudoranges_log_2017_07_17_13_46_25.txt \
  2> ~/iono_ops/android_out/stderr.txt
echo EXIT:$?
wc -l ~/iono_ops/android_out/nex9_lab.17o ~/iono_ops/android_out/stderr.txt
head -n 20 ~/iono_ops/android_out/nex9_lab.17o
```

**本机截断结果（andrnx/setup 0.1 @ `8ea7ab7`，2026-09-24 EDT）：**

```text
EXIT:0
15213 .../nex9_lab.17o
27533 .../stderr.txt
     3.03           O                   M                   RINEX VERSION / TYPE
Rokubun             Ionosphere-GNSS-OpenSource2026-09-24 08:03:45 PGM / RUN BY / DATE
NEX9                                                        MARKER NAME
SMARTPHONE                                                  MARKER TYPE
lab-demo            Ionosphere-GNSS-OpenSource              OBSERVER / AGENCY
UNKN                UNKN                AndroidOS >7.0      REC # / TYPE / VERS
UNKN                internal                                ANT # / TYPE
        0.0000        0.0000        0.0000                  APPROX POSITION XYZ
G    4 C1C L1C D1C S1C                                      SYS / # / OBS TYPES
R    4 C1C L1C D1C S1C                                      SYS / # / OBS TYPES
  2017    07    17    11    46    44.0000000                TIME OF FIRST OBS
  2017    07    17    12    09    42.0000000                TIME OF LAST OBS
> 2017 07 17 11 46 44.0000000  0 10
G05  24903458.30700     34969.22500     -1487.73600        33.92200
G16  22055851.72200    -59093.66400      2494.58300        30.47200
...
```

stderr 大量 `-- WARNING:`（正常，勿当失败）。本机统计：`skip_glo_no_osn=18944`，`adr_invalid=4616`，`code_lock_invalid=2414`，其它警告 `1559`（合计 27533 行）。示例：

```text
-- WARNING: ADR State [ 0x 4      100 ] has ADR_STATE_VALID [ 0x 1        1 ] not valid for satellite [ G25 ]
-- WARNING: State [ 0x10    10000 ] has STATE_CODE_LOCK [ 0x 1        1 ] not valid for satellite [ G27 ]
-- WARNING: Skipping measurement for GLONASS sat without OSN [ R93 ]
```

### 3.3 下游探活（georinex）

```bash
python -W ignore - <<'PY'
import georinex as gr
obs = gr.load("~/iono_ops/android_out/nex9_lab.17o".replace("~", __import__("os").path.expanduser("~")), use="G")
print(gr.__version__, dict(obs.dims), list(obs.data_vars))
print(obs.time.values[0], "->", obs.time.values[-1], "nsv=", int(obs.sv.size))
print(obs[["C1C","L1C","S1C"]].isel(time=0).to_dataframe().dropna(how="all").head(6))
PY
```

**本机（georinex 1.16.2）：**

```text
1.16.2 {'time': 1379, 'sv': 11} ['C1C', 'L1C', 'D1C', 'S1C']
2017-07-17T11:46:44.000000 -> 2017-07-17T12:09:42.000000 nsv= 11
              C1C        L1C     S1C
sv
G05  2.490346e+07  34969.225  33.922
G16  2.205585e+07 -59093.664  30.472
G18  2.408485e+07 -61379.113  31.965
G20  2.304942e+07 -15148.961  34.835
G21  2.097181e+07  -2150.930  36.014
G26  2.072916e+07 -28692.721  35.988
```

另：`L1C` 有限值 13818 个，其中 **`L1C==0` 达 4616**（与 ADR 无效警告同量级）——相位列里的 0 **不是**健康周计数，下游须当缺测。

## 4. I/O 字段

| 侧 | 路径/字段 | 说明 |
| --- | --- | --- |
| 入 | `*.txt` GnssLogger | 必需 `Raw,`；可选 `Fix,`/`Nav,`（本工具主用 Raw） |
| 出 | `*.yyo` / `*.rnx` OBS | RINEX 3 Mixed；头含 `SMARTPHONE` `MARKER TYPE` |
| 出 | stderr | 逐条测量警告；体量大，建议重定向文件 |
| 观测量 | `C1C L1C D1C S1C`（样例） | 伪距 m、载波 cycle、多普勒 m/s、CN0 dB-Hz |
| 头 | `APPROX POSITION XYZ` | 样例为全 0；真机可后补或靠 `Fix,` 另算 |

取自己的日志：手机装 [gps-measurement-tools](https://github.com/google/gps-measurement-tools) → 录一段 → 拷出 `gnss_log_*.txt`。数据门户与 IGS 站见 [data-access](../data-access.md)；手机线在 [categories](../categories.md)「手机/嵌入式」。

## 5. 参数（CLI）

| 参数 | 作用 | 本机备注 |
| --- | --- | --- |
| `-o/--output` | 输出 OBS；省略则打到 **stdout** | 大文件务必 `-o`，避免终端被灌爆 |
| `-m/--marker-name` | `MARKER NAME` | 例：`NEX9` |
| `-n/--observer` `-a/--agency` | 观测者 / 机构 | 写入 `OBSERVER / AGENCY` |
| `--receiver-*` / `--antenna-*` | 接收机与天线头字段 | 默认 `UNKN` / `AndroidOS >7.0` / `internal` |
| `--integerize` / `-i` | 历元取整秒，并用 range rate 回推伪距 | 样例 FIRST/LAST OBS 变为 `.0000000` |
| `--fix-bias` / `-b` | 固定首个 `FullBiasNanos` | 抑伪距台阶；相位不一定同跳 |
| `--pseudorange-bias` | 伪距减常数（米） | TOW 解码差时急救 |
| `--skip-edit` | 跳过伪距范围编辑 | 脏数据排查用 |
| `--filter-mode sync\|trck` | 测量门限 | 默认 `sync`；过严无星可试 `trck` |

## 6. 接到哪步

```text
GnssLogger 手机录制
  → android_rinex（本文）→ RINEX OBS
  → georinex 探活 / gfzrnx 抽稀
  →（单频）rtklib / cssrlib / laika 教学定位
  →（仅当日志含双频 L1+L2/L5）gnss-tec / pytecgg 做 TEC
  → 概念：教程 06 电离层与定位；02/16 一日 TEC（需双频）
```

路径 C 实时流仍走 [pygnssutils](./pygnssutils.md)/[bnc](./bnc.md)；手机文件流走本文。

## 7. 坑（≥8）

1. **stderr 上万行 WARNING 仍 EXIT:0** — 不要以「有警告」判失败；看 OBS 头与历元数。
2. **`L1C==0` 仍写入** — ADR 无效时相位可被写成 0；`georinex` 会当合法 0。QC/定位前应掩掉 0 或对照 ADR 警告。
3. **GLONASS 无 OSN 整星丢弃** — 样例近 1.9 万条 skip；勿期望 R 满星。
4. **样例只有 L1 观测量列** — 不能直接算双频 TEC；要 TEC 换双频手机/测绘接收机或走 IGS 站（[data-access](../data-access.md)）。
5. **无 NAV 输出** — SPP/PPP/TEC 需另备 `.yyN`/brdc；[georinex](./georinex.md) 只读 OBS 不够定轨。
6. **`APPROX POSITION` 全 0** — 许多手机日志不写天线坐标；RTKLIB 需先验或先单点。
7. **`--integerize` 改变时间戳** — 与原始 `TimeNanos` 非整秒对齐；和传感器融合时勿混用两套时间。
8. **`--fix-bias` 只钉伪距钟偏** — 上游说明相位有时不跳；组合观测前检查 C/L 一致性。
9. **`--filter-mode` 拼写** — 仅 `sync` / `trck`；其它值 `ValueError: Invalid value of --filter-mode`。
10. **仓停在 2020、GnssLogger 格式在变** — 新 App 列增删可能导致解析失败；先 `head` 对照仓内样例头。
11. **输出到 stdout 无 `-o`** — 巨量 OBS + 警告刷屏；脚本里永远 `-o` 并把警告 `2>` 到文件。
12. **单频手机 duty cycle / 天线** — 载波连续性和多路径差于测绘机；周跳/ROTI 结论勿直接对标 CORS。

## 8. 选型

| 你要… | 用 |
| --- | --- |
| 手机 GnssLogger → RINEX | **android_rinex（本文）** |
| 测绘/厂商接收机 RAW 台网入库 | [autorino](./autorino.md) |
| 已有 RINEX，Python 探活 | [georinex](./georinex.md) |
| 双频校准 TEC | [pytecgg](./pytecgg.md)（先确认 OBS 有双频） |
| 教学单频定位 | [rtklib](./rtklib.md) / [laika](./laika.md) / [cssrlib](./cssrlib.md) |
| IGS/CORS 下载而非手机 | [data-access](../data-access.md)；下载器候选见 `PROJECTS.json`（FAST/GDDS 等，手册待补） |

相关：上游 README · Google [gps-measurement-tools](https://github.com/google/gps-measurement-tools) · [data-access](../data-access.md) · [georinex](./georinex.md) · [rtklib](./rtklib.md) · 教程 [06](../tutorials/06-iono-positioning.md)
