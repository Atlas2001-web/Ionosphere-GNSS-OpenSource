# libnmea · 轻量纯 C NMEA 0183 解析库操作手册

目录：[`PROJECTS.json` → `libnmea`](../../PROJECTS.json) · 上游 <https://github.com/jacketizer/libnmea> · tip **`91fd433`**（`master`；PR **#58** talker 无关句型匹配）· 许可 **MIT** · ★**326** · 本机验证（2026-09-24 06:36–06:37 EDT）：`make` → `build/libnmea.so` **24576** B + 7×`build/nmea/libgp*.so`；`make check` → **All tests passed!**（断言 **74**）；`make examples` → `parse_stdin`/`minimum`；北京 GGA/RMC（validate=**1**）lat=**39.9041866667**/lon=**116.3907433333**/sats=**12**/alt=**44.0**；`$GNGGA` 同解；`validate=0` 时坏校验和仍解析（`parse_stdin` 默认此路径）

> 岗位：桌面/嵌入式 **NMEA 0183 → C 结构体**（动态加载句型模块）。冲突时：**上游 README / `nmea.h` > 本文**。单文件无 `dlopen` → [minmea](./minmea.md)；Python → [pynmeagps](./pynmeagps.md)/[pynmea2](./pynmea2.md)；系统守护 → [gpsd](./gpsd.md)。

## 1. 用途与边界

**做：**

- 模块化解析：`GPGGA`/`GPGLL`/`GPGSA`/`GPGSV`/`GPRMC`/`GPTXT`/`GPVTG`（`src/parsers/` 各一 `.so`）
- `nmea_parse(sentence, length, check_checksum)`；`nmea_free`
- 动态加载（默认）或 `NMEA_STATIC=...` 静态链入
- 例程：`examples/parse_stdin.c`（stdin 流）、`examples/minimum.c`（单句）
- tip **`91fd433`**：只匹配句型 ID，**忽略 talker**（`$GN…`/`$GP…` 等同）

**不做：**

- **不是** GNSS 引擎 / PPP / RTK → [rtklib](./rtklib.md)
- **不是** UBX/RTCM/SBF → [pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)
- **不是** 无堆/定点 MCU 路径 → [minmea](./minmea.md)（本库用 `malloc` + `dlopen`）
- **无** 官方 tag；PyPI 亦无（纯 C）

一句话：`libnmea` = **可插拔句型模块的 NMEA C 库**；与 minmea 互补（动态 vs 单文件）。

| 术语 | 含义 |
| --- | --- |
| `NMEA_PARSER_PATH` | 句型 `.so` 目录；**须尾斜杠**（如 `…/lib/nmea/`） |
| `check_checksum` | `nmea_parse` 第 3 参：`1` 校验失败→`NULL`；`0` 跳过 |
| talker | `$GP`/`$GN`/…；自 PR#58 起不参与句型匹配 |

## 2. 安装

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://github.com/jacketizer/libnmea.git
cd libnmea && git rev-parse --short HEAD   # 本机：91fd433
make && make check
# → Building build/libnmea.so
# → All tests passed!
ls -la build/libnmea.so build/nmea/        # 24576 B；7 个 libgp*.so
PREFIX=$PWD/target make install            # 可选；本机 ldconfig 缺失可忽略（Error 127）
export LD_LIBRARY_PATH="$PWD/build${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export NMEA_PARSER_PATH="$PWD/build/nmea/" # 尾斜杠必需
make examples                              # → build/parse_stdin build/minimum
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Failed to parse` / 空输出 | 未设 `NMEA_PARSER_PATH` 或漏尾 `/` | `export NMEA_PARSER_PATH=…/nmea/` |
| `ldconfig: No such file` | 容器无 `ldconfig` | 忽略；用 `LD_LIBRARY_PATH` |
| 坏校验和仍出结构体 | `parse_stdin` 调 `nmea_parse(..., 0)` | 自写代码传 **`1`** |

## 3. 端到端（本机真跑；2026-09-24 06:37 EDT）

### 3.1 官方 README 样句

```bash
cd ~/iono_ops/libnmea
export LD_LIBRARY_PATH="$PWD/build" NMEA_PARSER_PATH="$PWD/build/nmea/"
echo -ne '$GPGLL,4916.45,N,12311.12,W,225444,A,*1D\r\n' | ./build/parse_stdin
```

**本机：** `Latitude 49° 16.450000′ N` / `Longitude 123° 11.120000′ W` / `Time 22:54:44`。

### 3.2 `minimum`（仓内 GSV）

```bash
./build/minimum
# GPGSV Sentence: Num=3 ID=1 SV=11；#1 PRN=3 el=3 az=111 snr=0
```

### 3.3 北京样句（对齐 [gpsd](./gpsd.md)/[minmea](./minmea.md)/[pynmea2](./pynmea2.md)）

```bash
# ddmm.mmmm：39.904187→3954.2512；116.390743→11623.4446
printf '%s\r\n' \
  '$GPGGA,060000.00,3954.2512,N,11623.4446,E,1,12,0.9,44.0,M,-8.0,M,,*4F' \
  '$GPRMC,060000.00,A,3954.2512,N,11623.4446,E,0.0,0.0,240926,,,A*59' \
  | ./build/parse_stdin
```

**`parse_stdin`（validate=0）摘录：** GGA sats=**12** alt=**44.0**；RMC `39° 54.251200′ N` / `116° 23.444600′ E` / `24 Sep 06:00:00 2026`。

**库 API（`nmea_parse(..., 1)`）本机探针：**

| 输入 | 结果 |
| --- | --- |
| 北京 GGA `*4F` | sats=**12** alt=**44.0** lat=**39:54.2512** lon=**116:23.4446** |
| 北京 RMC `*59` | lat=**39.9041866667** lon=**116.3907433333** |
| `$GNGGA` 同体 `*51` | type=`NMEA_GPGGA`；sats=**12** |
| 同 GGA 改 `*00` + validate=**1** | **`NULL`** |
| 同 GGA 改 `*00` + validate=**0** | 仍 OK（与 `parse_stdin` 一致） |
| `make check` | **All tests passed!**（**74** 条断言） |

## 4. I/O 与关键 API

| API / 路径 | 作用 |
| --- | --- |
| `nmea_parse(s,n,check)` | 解析；失败 `NULL` |
| `nmea_free` | 释放句型数据 |
| `nmea_gpgga_s` 等 | 各句结构体（见 `src/parsers/*.h`） |
| `build/nmea/libgp*.so` | 运行时句型模块 |

## 5. 坑

1. **`NMEA_PARSER_PATH` 尾斜杠** —— README 强调；漏了模块加载失败。
2. **`parse_stdin` 不校验和** —— 第 3 参固定 `0`；生产代码用 `1`。
3. **`PREFIX=… make install` + `ldconfig`** —— 无 root/`ldconfig` 时 Error 127；改 `LD_LIBRARY_PATH` 即可。
4. **句型白名单** —— 仅 7 类；无 `ZDA`/`GBS`/`GST`（那些见 [minmea](./minmea.md)）。
5. **磁偏角空字段** —— 北京 RMC 无磁偏角时 `parse_stdin` 打 `Invalid Magnetic Variation Direction!!`（仍给出经纬）。

## 6. 与相近工具

| 需求 | 选 |
| --- | --- |
| 无 `dlopen`/定点 MCU | [minmea](./minmea.md) |
| Python 对象/流 | [pynmeagps](./pynmeagps.md)/[pynmea2](./pynmea2.md) |
| 多客户端 JSON | [gpsd](./gpsd.md) |
| 本库 | C 工程要可扩展句型 `.so` |

## 7. 本机未跑 / 边界

- **未** `sudo make install` 进 `/usr`（用本地 `build/`/`target/`）
- **未** 测 `NMEA_STATIC` 全静态链接产物大小
- **未** 接真串口——仅 stdin/字符串

## 8. 参考

- 上游 <https://github.com/jacketizer/libnmea>
- 交叉：[minmea](./minmea.md) · [pynmea2](./pynmea2.md) · [pynmeagps](./pynmeagps.md) · [gpsd](./gpsd.md) · [pygpsclient](./pygpsclient.md)
