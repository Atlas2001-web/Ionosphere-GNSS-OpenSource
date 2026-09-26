# minmea · 轻量纯 C NMEA 0183 解析库操作手册

目录：[`PROJECTS.json` → `minmea`](../../PROJECTS.json) · 上游 <https://github.com/kosma/minmea> · tip **`c43c9e7`** · 许可 **WTFPL**（可选 **MIT** / **LGPL-3.0+**，见 `LICENSE.grants`）· 单文件 `minmea.c` + `minmea.h` · 本机验证（2026-09-24 05:45 EDT）：CMake 建 `libminmea.a` + `example`；`check` 单测 **38/38**；例程/探针解官方样句 + 北京 NMEA（对齐 [gpsd](./gpsd.md)/[pynmeagps](./pynmeagps.md)） · **质检复跑通过**（2026-09-26 01:30–01:33 EDT，gcc 14.2：tip/38 checks/example/探针 7 行数值全部同 I/O；修：补出探针源码（原文未给 `/tmp/minmea_probe.c` 无法复现）、example GSA 实际打印 `$xxxxx sentence is not parsed`、坑 4 实测现象）

> 岗位：嵌入式/无堆分配环境下的 **NMEA 0183 语句解析**（定点优先，可选浮点坐标）。冲突时：**上游 README / `minmea.h` > 本文**。Python 编解码 → [pynmeagps](./pynmeagps.md)；系统守护 → [gpsd](./gpsd.md)；流 CLI → [pygnssutils](./pygnssutils.md)。

## 1. 用途与边界

**做：**

- ISO C99 单翻译单元：无动态分配；核心路径可不碰浮点
- 句型：`GBS`/`GGA`/`GLL`/`GSA`/`GST`/`GSV`/`RMC`/`VTG`/`ZDA`
- `minmea_sentence_id` → `minmea_parse_*`；`minmea_tocoord` / `minmea_tofloat` / `minmea_rescale`；`minmea_check`
- 仓内 `example`（stdin→解析打印）与 `tests.c`（libcheck）

**不做：**

- **不是** 完整 GNSS 引擎 / PPP / RTK → [rtklib](./rtklib.md)
- **不是** Python 高层对象模型 → [pynmeagps](./pynmeagps.md)
- **不是** UBX/RTCM/SBF 二进制 → [pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)
- **不是** 串口守护多客户端 → [gpsd](./gpsd.md)
- 仓内 `example` **未** switch `GSA`（库能解；例程默认分支会打 “not parsed”）

一句话：`minmea` = **MCU/嵌入式友好的 NMEA 解析核**；桌面脚本优先 pynmeagps。

| 术语 | 含义 |
| --- | --- |
| `minmea_float` | `{value,scale}` 定点；`minmea_tofloat` → `float` |
| `minmea_tocoord` | `ddmm.mmmm` 定点 → 十进制度 |
| talker | `$GP`/`$GN`/…；句型匹配忽略 talker |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/kosma/minmea.git
cd minmea && git rev-parse --short HEAD   # c43c9e7

# 单测需要 Debian check；仅库+example 可 -DMINMEA_ENABLE_TESTING=OFF
sudo apt-get install -y check cmake build-essential pkg-config
mkdir -p build && cd build
cmake .. && cmake --build . -j"$(nproc)"
./tests
# Running suite(s): minmea
# 100%: Checks: 38, Failures: 0, Errors: 0
ls libminmea.a example
```

`ctest` 另挂 `scan-build` 静态分析；无 clang-tools 时该项 **Not Run**（本机如此）。以直接跑 `./tests` 为准。

手写链接：把 `minmea.c`/`minmea.h` 拷进工程，并带上 CMake 同款宏（`_POSIX_C_SOURCE`/`_DEFAULT_SOURCE` 等），否则 `minmea_gettime`/`timegm` 易踩编译坑。

## 3. 端到端（本机真跑）

### 3.1 example：官方样句

```bash
cd ~/iono_ops/minmea/build
printf '%s\n' \
  '$GPGGA,123204.00,5106.94086,N,01701.51680,E,1,06,3.86,127.9,M,40.5,M,,*51' \
  '$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A' \
  '$GPGSV,2,1,08,01,40,083,46,02,17,308,41,12,07,344,39,14,22,228,45*75' \
  | ./example
```

**本机摘录：** GGA `fix quality: 1`；RMC 浮点 **(48.117298, 11.516666)** speed **22.400000**；GSV `satellites in view: 8`，首星 snr **46**。

### 3.2 北京样句（与 gpsd 手册同源）

```bash
head -6 ~/iono_ops/gpsd-demo/demo_beijing.nmea | ./example
```

**本机：** `$GNRMC` → **(39.904186, 116.390739)**；`$GNGGA` → `fix quality: 1`。`$GNGSA` 在 example 中落入默认分支，打印 `$xxxxx sentence is not parsed`（见坑表）；库 API 可解。

### 3.3 库 API 探针

```bash
cat > /tmp/minmea_probe.c <<'C'
#include <stdio.h>
#include "minmea.h"
int main(void){
 const char *gga="$GPGGA,123204.00,5106.94086,N,01701.51680,E,1,06,3.86,127.9,M,40.5,M,,*51";
 const char *rmc="$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A";
 const char *gsa="$GPGSA,A,3,02,08,09,05,04,26,,,,,,,4.92,3.86,3.05*00"; /* tests.c 样句；*00 恰好是真校验和 */
 const char *brmc="$GNRMC,123519.00,A,3954.25123,N,11623.44456,E,0.1,0.0,240926,,,A*4B";
 const char *bgga="$GNGGA,123519.00,3954.25123,N,11623.44456,E,1,12,0.9,44.0,M,-8.0,M,,*5C";
 struct minmea_sentence_gga g; struct minmea_sentence_rmc r; struct minmea_sentence_gsa a;
 minmea_parse_gga(&g,gga); printf("GGA q=%d sats=%d hdop=%.2f alt=%.1f lat=%.8f lon=%.8f\n",g.fix_quality,g.satellites_tracked,minmea_tofloat(&g.hdop),minmea_tofloat(&g.altitude),minmea_tocoord(&g.latitude),minmea_tocoord(&g.longitude));
 minmea_parse_rmc(&r,rmc); printf("RMC valid=%d lat=%.6f lon=%.6f speed=%.3f\n",r.valid,minmea_tocoord(&r.latitude),minmea_tocoord(&r.longitude),minmea_tofloat(&r.speed));
 minmea_parse_gsa(&a,gsa); printf("GSA mode=%c fix=%d pdop=%.2f hdop=%.2f vdop=%.2f\n",a.mode,a.fix_type,minmea_tofloat(&a.pdop),minmea_tofloat(&a.hdop),minmea_tofloat(&a.vdop));
 minmea_parse_rmc(&r,brmc); printf("BJ RMC lat=%.8f lon=%.8f\n",minmea_tocoord(&r.latitude),minmea_tocoord(&r.longitude));
 minmea_parse_gga(&g,bgga); printf("BJ GGA q=%d sats=%d hdop=%.2f alt=%.1f\n",g.fix_quality,g.satellites_tracked,minmea_tofloat(&g.hdop),minmea_tofloat(&g.altitude));
 const char *all[]={gga,rmc,gsa,brmc,bgga}; for(int i=0;i<5;i++) printf("check%d=%d ",i,minmea_check(all[i],false));
 printf("\nid GGA=%d GSA=%d RMC=%d\n",minmea_sentence_id(gga,false),minmea_sentence_id(gsa,false),minmea_sentence_id(rmc,false));
 return 0;}
C
# 编译时与 CMake 一致带 feature 宏；见上游/本仓 CMakeLists.txt
cc -std=c99 -D_POSIX_C_SOURCE=199309L -D_DEFAULT_SOURCE \
  -I$HOME/iono_ops/minmea -o /tmp/minmea_probe /tmp/minmea_probe.c \
  $HOME/iono_ops/minmea/minmea.c
/tmp/minmea_probe
```

**本机结果（2026-09-24 05:45 EDT）：**

| 输入 | 结果 |
| --- | --- |
| 官方 GGA | q=**1** sats=**6** hdop=**3.86** alt=**127.9** lat=**51.11568069** lon=**17.02528000** |
| 官方 RMC | valid=**1** lat=**48.117298** lon=**11.516666** speed=**22.400** |
| 官方 GSA | mode=`A` fix_type=**3** pdop=**4.92** hdop=**3.86** vdop=**3.05** |
| 北京 RMC | lat=**39.90418625** lon=**116.39073944** |
| 北京 GGA | q=**1** sats=**12** hdop=**0.90** alt=**44.0** |
| `minmea_check` | 上述五句均为 **1** |
| `./tests` | **38** checks，Failures=**0** |

## 4. I/O 与关键 API

| API | 作用 |
| --- | --- |
| `minmea_sentence_id(line, strict)` | 识别句型枚举（本机 GGA=2 / GSA=4 / RMC=7） |
| `minmea_parse_gga/rmc/gsa/…` | 填对应 `struct minmea_sentence_*` |
| `minmea_tocoord` / `minmea_tofloat` | 定点 → 度 / float |
| `minmea_check(line, strict)` | 校验和；`strict` 控制空字段等 |
| `minmea_gettime` | 日期+时间 → `timespec`（需正确 feature 宏） |

输入：单行 NMEA（建议保留 `*` 校验与 `\n`）。输出：C 结构体字段；无堆、无全局可变状态（可重入于单行解析）。

## 5. 接到哪步

```text
UART/日志 NMEA 行
  → minmea_parse_*（MCU / C 固件）
  → 桌面脚本改 pynmeagps；多客户端分发改 gpsd
  → 观测落盘后再 georinex / pytecgg / rtklib
```

## 6. 坑

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | CMake：`Package 'check' not found` | 未装 libcheck | `apt install check` 或 `-DMINMEA_ENABLE_TESTING=OFF` |
| 2 | `ctest` 半失败 | 缺 `scan-build` | 忽略该项；直接 `./tests` |
| 3 | example：`$xxxxx sentence is not parsed`（GSA 行） | example switch 无 GSA 分支 | 用 `minmea_parse_gsa`；勿当库不支持 |
| 4 | 不带宏编译：`warning: 'struct timespec' declared inside parameter list`（CMake 带 `-Werror` 即成错误） | 缺 POSIX/BSD 宏 | 抄 CMake `CMAKE_C_FLAGS` 宏集 |
| 5 | 坐标差 60× | 把 `ddmm.mmmm` 当十进度 | 必走 `minmea_tocoord` |
| 6 | 浮点禁区链接失败 | 目标无 libm / 禁用 float | 只用定点 `value/scale` + `minmea_rescale` |
| 7 | 长句截断 | 缓冲 < `MINMEA_MAX_SENTENCE_LENGTH` | 加大缓冲；先 `minmea_check` |
| 8 | 校验失败 | 日志被改 / 缺 `*` | 修源；或 `strict`/`check` 策略按嵌入式场景放宽 |
| 9 | 当 TEC/PPP 库用 | 职责仅句子解析 | 产品链见 [georinex](./georinex.md)/[pytecgg](./pytecgg.md) |
| 10 | 与 pynmeagps 数值微差 | 舍入/字段全集不同 | 对照同一原始行；以各自 API 文档为准 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| MCU / 无堆 C 解析 NMEA | **minmea（本文）** |
| Python 编解码 / 生成 | [pynmeagps](./pynmeagps.md) |
| 系统守护 + JSON 客户端 | [gpsd](./gpsd.md) |
| 流录制 / NTRIP CLI | [pygnssutils](./pygnssutils.md) |

相关：[pynmeagps](./pynmeagps.md) · [gpsd](./gpsd.md) · [pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · 教程 [06](../tutorials/06-iono-positioning.md)