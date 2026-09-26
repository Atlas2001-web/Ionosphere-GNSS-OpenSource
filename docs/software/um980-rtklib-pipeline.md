# um980-rtklib-pipeline · UM980 混合日志 → 干净 NMEA / RINEX 3 → RTKLIB PPK 操作手册

目录：[`PROJECTS.json` → `um980-rtklib-pipeline`](../../PROJECTS.json) · 上游 <https://github.com/holubp/um980-rtklib-pipeline>（与 PROJECTS `url` 一致，默认分支 **main**）· tip **`25d9546`**（2026-06-06 11:20 EDT，`Fix Termux FTDI baud transitions`）· **无 tag** · **不在 PyPI**（包名 `um980-rtklib-pipeline` 0.1.0 只能源码装）· **GPL-3.0**（LICENSE 为 GPLv3，pyproject 写 GPL-3.0-or-later）· ★**1** · Python ≥3.11，GitHub 语言统计 Python + 少量 Shell/C（Termux USB 抓包工具）· 运行时**零依赖**，可选 PyYAML（`[config]`）/pytest · 入口 `um980-ppk` = `um980-rtklib-pipeline` · 本机 CPython 3.13.5 + venv，georinex 1.16.2；RTKLIB：**RTKLIB-EX 2.5.1**（rtklibexplorer `06e8644`，本机 gcc 现编 rnx2rtkp/convbin）与 Debian `rtklib` **2.4.3 b34** 对照 · 实测窗口 **2026-09-26 06:06–06:18 EDT**

> 一句话：纯 Python 自己解 UM980 串口混流（NMEA + Unicore ASCII/二进制），自己写 RINEX 3.04 OBS 和接收机星历 NAV，再拼 `rnx2rtkp` 命令跑 PPK。**不用 convbin 转流动站**（作者原话：多数 RTKLIB 没有 Unicore 解码，`convbin` 处理不了 ASCII 混流）。
> **本机无 UM980 接收机**：`init generate` 生成的命令、`capture-usb`/Termux 抓包、`record-base-rt` 实时基准站全部**「未在真接收机测试」**。数据来自公开真实日志 JHua07/Hardware-Projects `RTK_Trans/`（成都，UM98x，**该仓无 license，只在本地用，本篇不复制其内容**）。人造输入标「合成」。

## 1. 用途边界

| 做 | 不做 / 做不好 |
| --- | --- |
| 解析混流：NMEA（校验 XOR）、Unicore ASCII `#...A`（校验 CRC32）、Unicore 二进制 `AA 44 B5`（CRC32，按消息 ID） | **`$KSXT` 当坏句丢**（计入 noise，不进 `all.nmea`）；未知 ASCII 句只计数 |
| 原始观测：`OBSVMA`（ASCII）、`OBSVMB`、`OBSVMCMPB`（二进制）→ RINEX 3.04 OBS + 观测 CSV | **不认 `OBSVBASEA`**（接收机转发的基准站观测），本篇靠改名绕过（§3.3） |
| 星历：`GPSEPHA/GLOEPHA/GALEPHA/BDSEPHA/BD3EPHA` → `.nav/.gnav/.lnav/.cnav`；QZSS/二进制星历只报"不支持" | ION/UTC 只存诊断、**不写 NAV 头**；`TROPINFO` 不给 RTKLIB |
| NMEA：`all.nmea`（全部校验通过句）、`position.nmea`（每时刻最优 GGA/GNS/RMC）、BESTNAV → 标准 GGA/RMC/VTG | RMC 状态字只认 `A`：**`D`（差分）整句不算定位点**（§6 坑 1） |
| 拼 `rnx2rtkp`：自动选 NAV、查 rover/base 重叠与频点、基准站坐标（`--base-ecef`/EUREF 查表）、跑完按 Q 统计 | 不装 RTKLIB；生成的默认参数（无 `-k`）不可信（§3.4） |
| `init generate` 生成 UM980 日志命令脚本 + 串口带宽估算；EUREF 基准站/BRDC 下载（需联网，`--offline` 只打印 URL） | 实时 RTK、NTRIP 客户端（只有 `ntrip-sourcetable`/`record-base-rt`，未测） |

调用的外部程序（按源码）：**`rnx2rtkp`**（必需，跑 PPK）、**`crx2rnx`**（EUREF 下载的 Hatanaka 文件）、**`convbin`**（只在 `--base-rtcm` 把录下来的基准站 RTCM3 转 RINEX 时用；流动站不用）。作者按 RTKLIB-EX 写 conf，仓库根带 5 个 `.conf`。

## 2. 安装

```bash
unset TMPDIR VIRTUAL_ENV PYTHONPATH PIP_CACHE_DIR   # 共享机器先清环境
mkdir -p /tmp/um980pp-man/tmp && cd /tmp/um980pp-man
export TMPDIR=/tmp/um980pp-man/tmp PIP_CACHE_DIR=/tmp/um980pp-man/pipcache
git clone https://github.com/holubp/um980-rtklib-pipeline src    # HEAD = 25d9546
python3 -m venv venv && . venv/bin/activate
pip install -e 'src[config,test]'
cd src && pytest -q      # → 1 failed, 371 passed in 3.42s
# RTKLIB-EX（强烈建议，见 §3.4）
git clone --depth 1 https://github.com/rtklibexplorer/RTKLIB ../rtklib
make -C ../rtklib/app/consapp/rnx2rtkp/gcc && make -C ../rtklib/app/consapp/convbin/gcc   # clone+两者编译共 10.8 s
# 或 --rtklib-dir 指目录 / 放 ~/RTKLIB-ex-bin/bin/ / 放 PATH
```

失败的那 1 个测试 `test_non_executable_local_tool_is_mirrored_for_subprocess` 往 `/data/data/com.termux/files/usr/tmp` 建目录——Termux 专用路径，Linux 上必挂，与功能无关。`um980-ppk --help` 列出 21 个子命令：`init, analyze, parse-rover, extract, rinex, nav, base-candidates, quality-analyze, quality, quality-compare, capture-usb, annotation-gpx, optimize-settings, download-base, resolve-base, record-base-rt, ntrip-sourcetable, postprocess, run-rtklib, cleanup, pipeline`。

## 3. 例子 + 真实输出

数据：`rover.log`（1491303 B，2025-09-15 07:16 GPST，104 历元 1 Hz，含 OBSVMA + 星历 + BESTNAVA + OBSVBASEA，GGA 22 固定/82 浮点）；`all.log`（15821945 B，2025-05-28 09:02–09:12 GPST，622 历元，OBSVMA + OBSVBASEA + PVTSLNA + 20 类 NMEA，GGA 622 句全 q=4，星历几乎没有）。基准站 "2197"，`#BASEINFOA` 给 ECEF (−1327852.282, 5324085.405, 3241499.041) m，基线 ≈3.20 km。

典型流程（上游 README）：`init generate` 出接收机命令 → 野外录 `.unc` → `pipeline` 解析+写 RINEX → 补外部 NAV/基准站 → 跑 `rnx2rtkp`（或 `postprocess` 只做最后一步）。

all.log 的 `-v` 消息统计（`analysis.json` → `stream`）：

| 类别 | 数量 |
| --- | --- |
| 记录总数 / NMEA / Unicore ASCII / 二进制 | 47349 / 31788 / 14938 / 0 |
| noise | 91721 B（= 622 句 `$KSXT`，`rejection_examples` 全是 KSXT） |
| OBSVMA / OBSVBASEA / BESTNAVA / PVTSLNA | 622 / 622 / 622 / 622 |
| 星历 converted / unsupported | 8 / 0（GPS 2、GAL 4、BDS 2 条，远不够 → 必须外部 BRDC） |
| ION / UTC | 623 / 623 存为诊断，另报 malformed 622，不写 NAV 头 |

### 3.1 拆 NMEA/解算轨迹（`extract`）

```text
$ um980-ppk extract rover.log -v --analysis-json --obs-csv --solution all --out-dir .
INFO: parsed rover log: records=1295 nmea=624 unicore_ascii=671 unicore_binary=0 noise=0 B
INFO: extracted solutions: points=185 nmea_records=185 all_nmea=624
INFO: decoded raw observations: observations=6473 epochs=104 unsupported_observation_records=0 ...
INFO:   ephemerides: records=262 converted=68 unsupported=194
WARNING: BD3EPH contained 30 records but 10 RTKLIB-compatible BDS-3 ephemerides were written; ...
real 0m0.497s
```

产物：`rover.all.nmea` 624 行、`rover.position.nmea` 104 行、`rover.solution.nmea` 185 行、`solution.csv/.gpx`、`observations.csv`（796822 B）、`analysis.json`。`points=185` = 82 句 RMC(`A`) + 103 句 GGA：22 句 RMC(`D`) 被丢。

### 3.2 写 RINEX（`rinex`）——务必加 `--rinex-compat convbin`

```text
$ um980-ppk rinex rover.log -v --rinex-compat convbin --out-dir .
INFO: wrote rover cnav file: rover.rover-bds.cnav      (187 行)
INFO: wrote rover gnav file: rover.rover-glo.gnav      (51 行)
INFO: wrote rover lnav file: rover.rover-gal.lnav      (99 行)
INFO: wrote rover nav file: rover.rover-gps.nav        (155 行)
INFO: wrote rover RINEX OBS: rover.direct.obs          (3531 行，104 历元，G/R/E/C/J)
real 0m0.285s
```

头部：`3.04 OBSERVATION DATA M: MIXED`，G `C1C L1C D1C S1C C2L…`，R `C1C…C2C`，E `C1C…C7Q`，C 16 型 `C2I…C6I…C1P…C7I`，J `C1C…C2L`。`all.log` 同命令：13.2 s（解析占 12.3 s），`rover.direct.obs` 22640 行/622 历元/45880 个观测。

### 3.3 端到端 PPK（`pipeline`）

找不到成都附近的公开 IGS/CORS（最近 IGS 站数百千米外，不够 RTK 固定）。改用日志里接收机收到的基准站观测 `#OBSVBASEA`：自写 20 行脚本把它**改名 `#OBSVMA` 并重算 CRC32**（1244/1244 原 CRC 通过，写出 622 条），再用本工具转成 `base.direct.obs`（28005 行/622 历元/80238 观测，G/R/E/C，APPROX 0 0 0）。星历用 BKG `BRDC00WRD_R_20251480000_01D_MN.rnx`（RINEX 3.05，免账号）。

```text
$ um980-ppk pipeline all.log --base-obs base.direct.obs \
    --nav-file BRDC00WRD_R_20251480000_01D_MN.rnx --base-station 2197 \
    --base-ecef -1327852.282 5324085.405 3241499.041 \
    --rnx2rtkp .../RTKLIB/app/consapp/rnx2rtkp/gcc/rnx2rtkp \
    --rtkconf src/um980-onepass-gps-gal-bds-el28.conf --run-rtklib --out-dir pipe -v
WARNING: selected NAV systems not useful for relative RTK because they are missing from rover/base OBS intersection: J
INFO: RTKLIB Q=1 (fixed; GGA quality=4 rtk fixed): 585 epochs (94.1%), duration=9m44s, track=5.3 m
INFO: RTKLIB Q=2 (float; GGA quality=5 rtk float): 37 epochs (5.9%), duration=37s, track=23.4 m
INFO: phase rtklib_run elapsed=4.488s
real 0m18.488s
```

输出 `pipe/all-rtk.pos` 650 行（622 解 + 头），另有 `.pos.stat`、`rtkpost-wrapper.sh`、`rerun.sh`、`commands.md`（逐步复现命令）、`pipeline-manifest.json`。

### 3.4 同一数据、不同 RTKLIB/配置（`postprocess`，全部 exit 0）

| rnx2rtkp | 配置 | 解数 | Q=1 | 对 GGA 固定解（Q=1∩q=4） |
| --- | --- | --- | --- | --- |
| Debian 2.4.3 b34 | 默认生成 `-p 2 -f 2 -sys G,R,E,C,J -m 10 -t -c` | **0** | 0 | —（rover 单点 χ² 全拒） |
| RTKLIB-EX 2.5.1 | 同上默认生成 | 622 | 6 | 6 个全是**错固定**：水平 3.34 m、高 +22.9 m |
| RTKLIB-EX 2.5.1 | `um980.conf` | 621 | 42 | 41 个：水平中位 9.6 mm，dU +138 mm |
| RTKLIB-EX 2.5.1 | `um980-autoqc-baseline.conf` | 622 | 22 | 未比 |
| RTKLIB-EX 2.5.1 | `um980-onepass-gps-gal-bds-el28.conf` | 622 | **585** | 584 个，见 §4.3 |
| Debian 2.4.3 b34 | `um980-onepass-gps-gal-bds-el28.conf` | 179 | 102 | 错固定最大 1.67 km |

结论：**只用 RTKLIB-EX + 仓库自带 conf**；不带 `-k` 的生成参数会给出假 Q=1。`rover.log` 同法（接收机星历或 BKG 258 BRDC 两种 NAV 结果相同）：104 历元全 Q=2，窗口仅 104 s，接收机自己 22 历元固定。

## 4. 交叉检查

### 4.1 NMEA 与原始日志逐句比（自写 XOR 校验扫描）

| 日志 | 原始 `$` 行 | 校验通过 | `all.nmea` 行 | 逐句顺序 |
| --- | --- | --- | --- | --- |
| rover.log | 624 | 624 | 624 | **完全一致**，0 丢 0 串 |
| all.log | 32410 | 32410 | **0** | 全丢：RMC 全为 `D` → NMEA 定位点 0 → 自动改用 BESTNAV 轨迹时把 `all_nmea` 清空（源码 `bestnav_records_to_solution_extraction` 返回 `all_nmea=[]`）；另 622 句 `$KSXT` 本就被判坏 |

all.log 的 `solution.nmea` 1866 行是 BESTNAV 生成的 GGA/RMC/VTG（3×622），不是原句。

### 4.2 RINEX 对原始 OBSVMA（自写解析 + georinex 1.16.2 读 RINEX）

按（历元，伪距，系统）配对，查 C/L/D/S：

| 文件 | 历元 RINEX/原始 | 观测配对 | L 有值 | 最大差 |
| --- | --- | --- | --- | --- |
| rover.log → rover.direct.obs | 104/104 | 6473/6473 | 3918（=原始 0x400 相位有效位 3918） | L 0.0005 周，D 0，S 0 |
| all.log → rover.direct.obs | 622/622 | 45880/45880 | 36445（=0x400 位 36445） | 同上 |
| OBSVBASEA → base.direct.obs | 622/622 | 80232/80238（6 个伪距重复跳过） | 80232 | 同上 |

native 折行版 `rover.direct.obs`（9223 行，同 104 历元）交给同一脚本：georinex 在 `obs3.py` 抛 `IndexError: index 28 is out of bounds`；RTKLIB-EX/2.4.3 `-p 0` 单点均 0 解，而 convbin 版分别 104/78 解。

L = −ADR（UM980 相位符号与 RINEX 相反，工具已翻号）；卫星号 R = PRN−37、J = PRN−192，其余不变。独立转换器对照：RTKLIB-EX `convbin -r unicore` 对这两份 ASCII 日志**输出 0 历元**（只解二进制 OBSVMB），故无法用 convbin 直转对照。改名脚本逻辑：只保留 `#OBSVBASEA` 行，先按 `crc32(body)` 验原 CRC，把 `OBSVBASEA,` 换成 `OBSVMA,` 后重算 CRC32（Unicore/NovAtel 算法 = `zlib.crc32(b, 0xFFFFFFFF) ^ 0xFFFFFFFF`）。字段布局两者相同（每观测 11 字段），但时间戳是接收机记录时刻，最后一个 rover 历元无对应基准站（age 1.0 s，末行跳成 Q=2）。基准站 D 写成 `0.000` 而不是空（OBSVBASEA 本无多普勒）。

### 4.3 PPK 对接收机 RTK 固定解（GGA q=4，UTC+18 s 对齐 GPST，椭球高 = MSL + 分离）

onepass conf，584 个共同固定历元：dE 均值 −23.5 mm/σ 17.4 mm/max 65.8 mm；dN +19.2/15.2/55.3 mm；dU **+132.0**/42.6/198.0 mm；水平中位 26.1 mm，3D 最大 212.7 mm。`um980.conf` 的 41 个历元 dU 同样 +138 mm → 系统性高差约 13 cm，推测是 BASEINFOA 坐标/天线参考点约定不同（未核实）。

## 5. 错误用例（合成，`rinex --rinex-compat convbin`，除注明外）

| 输入 | 退出码 | 行为 |
| --- | --- | --- |
| 空文件 | 2 | `ERROR: RINEX writer emitted no observation types: no observations decoded` |
| 不存在的文件 | 2 | `ERROR: [Errno 2] No such file or directory` |
| rover.log 截断到一半（切在记录中间） | 0 | 50 历元，半截记录计入 noise 3.7 KiB，无警告 |
| 中间插 4096 B 随机字节 + 假 `AA 44 B5` 头 | 0 | 104 历元、6473 观测全在，noise 4.1 KiB，静默 |
| 头部插 `$PXYZ`（合法校验）、`#FOOBARA`（合法 CRC）、`$GPXXX*00`（坏校验） | 0 | PXYZ 进 `all.nmea`；FOOBARA 只计数；GPXXX 记 `invalid_structure_or_checksum` |
| OBSVMA 第 51 条起 TOW −3600 s，末 10 条周数 −1024（周翻转） | 0 | RINEX 按时间重排，`TIME OF FIRST OBS` 变 **2006-01-30**；只在 JSON 里 `large_gaps=1/interval_max_s=3507`，**无警告** |
| `--rnx2rtkp /nonexistent/rnx2rtkp` | 2 | `ERROR: rnx2rtkp executable missing` |
| `--base-obs nobase.obs` | 2 | 先两条 WARNING，再 `ERROR: RTKLIB input does not exist` |
| pipeline 不给任何基准站 | 2 | `ERROR: --station is required to download base observations` |
| `--nav-file nonav.rnx` | 2 | `ERROR: no NAV data available…` |
| RTKLIB 跑完 0 个解（§3.4 第 1 行） | **0** | 只有 WARNING `no solution rows`，**脚本判不出失败** |

## 6. 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | UM980 `.unc`/`.log` 字节流（任意扩展名）；可选 `--base-obs`（RINEX）/`--base-rtcm`（RTCM3，经 convbin）/`--download-base`（EUREF）；`--nav-file/--nav-glob` 或接收机星历；`--rtkconf` |
| 时间窗 | `--start-time/--end-time`（ISO-8601，**无时区按 UTC**） |
| 输出 | `<base>.all/position/solution.nmea`、`solution.csv/gpx`、`observations.csv`、`direct.obs`（RINEX 3.04）、`rover-*.nav/gnav/lnav/cnav`、`analysis.json`、`*-rtk.pos`（+`.stat`）、wrapper/`rerun.sh`/`commands.md` |
| 日志 | `-v` 分阶段耗时；`-d` 打印精确 argv 与 stdout/stderr 日志路径 |

## 7. 坑

1. **RMC 状态 `D` 不认**：RTK 模式下 UM980 常输出 `D`；rover.log 丢 22 个固定历元，all.log 全部丢 → 回落 BESTNAV 并**清空 `all.nmea`**（0 行，exit 0）。要原句自己 `grep '^\$'`。
2. **`rinex`/`extract` 默认 `--rinex-compat native` 写的是 80 列折行的"RINEX 3"**：georinex `IndexError`，RTKLIB-EX 与 2.4.3 单点都 0 解。只有 `pipeline` 默认 `convbin`。
3. **LLI 恒为 0**：四种解码路径都写 `lli=0`，锁定时间不转周跳标志，靠 RTKLIB 自己探测。
4. **`--rnx2rtkp-option=-r x y z` 被覆盖**：工具随后追加 `-r` 基准站头坐标（0 0 0）。用 `--base-ecef`/`--base-llh`。
5. 基准站 RINEX 头 APPROX 为 0 0 0、`--base-station` 非 EUREF 名会警告"could not resolve"，必须显式给坐标。
6. **无 `-k` 的生成参数不可信**（§3.4）；Debian 2.4.3 读同一 conf 仍出公里级错固定。
7. RTKLIB 0 解时 exit 0；要在脚本里查 `*-rtk.pos` 非注释行数。
8. 周翻转/时间跳变静默写进 RINEX（首历元 2006 年），只在 `analysis.json` 可见。
9. BD3EPH 同星同历元多频点被合并（30→10），QZSS/二进制星历不转；ION/UTC 不进 NAV 头。
10. `$KSXT` 被当坏句；OBSVBASEA 不解。
11. 输出目录里同名文件**默认直接覆盖**（实测 rc 0、mtime 更新、无提示）；`--skip-existing` 才复用。
12. `--start-time/--end-time` 不带时区按 **UTC**，而 RINEX/`.pos` 是 GPST（差 18 s）；UM980 日志本身 GPST，NMEA 是 UTC。
13. pytest 有 1 个 Termux 路径用例在 Linux 必挂，不代表安装坏了。

## 8. 未测

真接收机串口/`capture-usb`/Termux 抓包（未在真接收机测试）；`init generate` 脚本下发（只生成：`OBSVMB COM1 0.5` + `GPSEPHB…QZSSEPHB COM1 300` 等 33 行，带宽 38%）；真实 OBSVMB/OBSVMCMPB 二进制日志（无公开样本，仅上游 pytest 合成用例）；EUREF 下载与 `crx2rnx`；`--base-rtcm`/`record-base-rt`/`ntrip-sourcetable`；`quality-*`、`optimize-settings`、`annotation-gpx`；Windows 路径风格。

## 9. 许可（非法律意见）

GPL-3.0(-or-later)：自己用、内部改都无义务；把它（或改版、与之合成一个程序的代码）**分发**给别人时须同样以 GPL 提供源码。它通过子进程调 RTKLIB（BSD-2），RTKLIB 不受传染；只把 `.obs/.pos` 结果交付客户不算分发本程序。

## 10. 选型

| 你要… | 用 |
| --- | --- |
| UM980 混合日志 → RINEX 3 + 一条命令跑 PPK（ASCII/二进制观测都行） | 本工具（记住 `--rinex-compat convbin` + RTKLIB-EX conf） |
| UM982/UM980 串口实时拿 fix/航向（ASCII PVTSLN/BESTNAV/HPR） | [um982-driver](./um982-driver.md) |
| 只有纯二进制 OBSVMB、想用官方链路 | RTKLIB-EX `convbin -r unicore`（[rtklib-explorer](./rtklib-explorer.md) / [rtklib](./rtklib.md)） |
| u-blox RAWX → RINEX | [ubx2rinex](./ubx2rinex.md) |
| NovAtel OEM 日志 | [novatel-edie](./novatel-edie.md) |
| 检查/切分/QC 生成的 RINEX | [rinex-cli](./rinex-cli.md) / [georinex](./georinex.md) |
| 只拆 NMEA 做轨迹 | [pynmeagps](./pynmeagps.md) |
| 自建基准站录 RTCM/RINEX | [rtkbase](./rtkbase.md)；公开 CORS 见 [cors-networks](./cors-networks.md) |
