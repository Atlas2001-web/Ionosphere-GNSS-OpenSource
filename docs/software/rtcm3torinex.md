# rtcm3torinex · BKG RTCM3→RINEX 转换器操作手册

目录：[`PROJECTS.json` → `rtcm3torinex`](../../PROJECTS.json) · wiki <https://software.rtcm-ntrip.org/wiki/rtcm3torinex> · 门户 <https://software.rtcm-ntrip.org/> · SVN `https://software.rtcm-ntrip.org/svn/trunk/rtcm3torinex`（guest/guest）· **URL 已核** · 门户标注 **obsolete，功能已并入 BNC** · 源码末变 **r9404**（2021-04-14）· WC **r11044** · 本机 **`Version 2.9404 (2021-04-14) GPL built Sep 24 2026`** · GPL-2+ · 本机验证：`make` 出二进制；默认拉 euref-ip **STR 222**；centipede `VALDM` → RINEX3 **43** 历元 / G03 C1C=**25238622.890**；`-P` 混星历 **75** 行；rtk2go 无订户 **400** · 2026-09-24 05:25 EDT

> 岗位：把 **NTRIP 上的 RTCM3 流** 直接打成 **RINEX OBS（+可选 NAV）**。冲突时：**本机 `./rtcm3torinex -h` / 仓内 `rtcm3torinex.txt` / 门户说明 > 本文**。  
> **对照：** 仅解码电文、不落 RINEX → [pyrtcm](./pyrtcm.md)；订流/录原始 → [pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md) / [ntrip-client](./ntrip-client.md)；生产多流 GUI/批处理 → [bnc](./bnc.md)（官方替代）；自建 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)。

## 1. 用途与边界

**做：**

- 作为 **NTRIP 客户端**：订挂载点 → 解码 RTCM3 → **stdout 写 RINEX OBS**
- 默认 RINEX **2.11**；`-3` → RINEX **3.0x**（本机实测 `3.00` OBS / `3.02` NAV）
- 可选星历文件：`-E/-G/-C/-Q/-B` 分系统，或 `-3 -P` 混星 NAV
- `-f` 用本地头模板覆盖 MARKER/ANT 等；`-O --changeobs` 允许观测类型中途变头
- 无 `-d` 时拉 **sourcetable**（本机默认 `euref-ip.net:2101`）

**不做：**

- **不是** 离线 `.rtcm3` / `.log` 文件转换器（**无文件/stdin 输入开关**）→ 先用 [pygnssutils](./pygnssutils.md) 录盘，或改用 [bnc](./bnc.md) / 自写 pyrtcm→RINEX
- **不是** RTCM3 结构化解码库 → [pyrtcm](./pyrtcm.md)（对比：pyrtcm = **帧级 DF/MSM**；本文 = **流→RINEX 文件**）
- **不是** 多流运维 / PPP / QC 主工具 → [bnc](./bnc.md) / [anubis](./anubis.md) / [gfzrnx](./gfzrnx.md)
- **不是** 现行主推：门户写明 **obsolete, included in BNC**；独立工具仍可编译，但新部署优先 BNC

一句话：rtcm3torinex = **单挂载点 NTRIP→RINEX 小转换器**；电离层/定位仍在 RINEX 落盘之后。

| 符号 | 含义 |
| --- | --- |
| `2.9404` | 版本串 = `RTCM3TORINEX_VERSION`「2」+ SVN 修订 **9404** |
| `-d` / `--data` | 挂载点名（mountpoint） |
| `-3` | 输出 RINEX3（否则 2.11） |
| `-P` | 混星 NAV；**必须**同时 `-3`，且不可与 `-E/-G/…` 同开 |
| `ntrip:…` | URL 单参写法（见 `-h`） |

## 2. 获取 / 编译

```bash
# 依赖：svn、cc、make（本机 apt: subversion + build-essential）
svn checkout --username guest --password guest \
  https://software.rtcm-ntrip.org/svn/trunk/rtcm3torinex
cd rtcm3torinex
svn info | grep -E 'Revision|Last Changed Rev|Date'
# 本机：Revision 11044；Last Changed Rev 9404；2021-04-14

make
# cc -Wall -W -O3 -Ilib lib/rtcm3torinex.c -lm -o rtcm3torinex
# 本机仅一条 -Wimplicit-fallthrough 提示，链接成功

./rtcm3torinex -h | head -3
# Version 2.9404 (2021-04-14) GPL built Sep 24 2026
# Usage: ./rtcm3torinex -s server -u user ...
```

说明：wiki 附件 `base`/`base.2` 实为 **Ntrip sourcetable 文本**（~33 KB），**不是** RTCM 样帧。无独立预编译发布页；正式替代见 [bnc](./bnc.md) FTP。

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `svn: E215004` 认证失败 | 未带 guest | `--username guest --password guest` |
| 只有 `rtcm3torinex.c` 无二进制 | 未 `make` | 在含 `makefile` 的目录执行 `make` |
| 想找「官方 zip」 | 独立工具已标 obsolete | SVN 源码 或改用 BNC |

## 3. 端到端（本机真跑）

### 3.1 `-h`（完整旗标，摘自本机）

```bash
./rtcm3torinex -h
```

**本机 stderr（exit 1）：**

```text
Version 2.9404 (2021-04-14) GPL built Sep 24 2026
Usage: ./rtcm3torinex -s server -u user ...
 -d --data             the requested data set
 -f --headerfile       file for RINEX header information
 -s --server           the server name or address
 -p --password         the login password
 -r --port             the server port number (default 2101)
 -t --timeout          timeout in seconds (default 60)
 -u --user             the user name
 -C --bdsephemeris     output file for BDS ephemeris data
 -E --gpsephemeris     output file for GPS ephemeris data
 -G --glonassephemeris output file for GLONASS ephemeris data
 -Q --qzssephemeris    output file for QZSS ephemeris data
 -B --sbasephemeris    output file for SBAS ephemeris data
 -P --mixedephemeris   output file for all ephemeris data
 -3 --rinex3           output RINEX type 3 data
 -S --proxyhost        proxy name or address
 -R --proxyport        proxy port, optional (default 2101)
 -n --nmea             NMEA string for sending to server
 -O --changeobs        Add observation type change header lines
 -M --mode             mode for data request
     Valid modes are:
     1, h, http     NTRIP Version 2.0 Caster in TCP/IP mode
     2, r, rtsp     NTRIP Version 2.0 Caster in RTSP/RTP mode
     3, n, ntrip1   NTRIP Version 1.0 Caster
     4, a, auto     automatic detection (default)
or using an URL:
./rtcm3torinex ntrip:data[/user[:password]][@[server][:port][@proxyhost[:proxyport]]][;nmea]
```

### 3.2 默认 sourcetable（euref-ip.net）

```bash
./rtcm3torinex -t 5 > /tmp/euref.st
# 无 -d → 拉源表；默认 -s euref-ip.net -r 2101
wc -l /tmp/euref.st; grep -c '^STR;' /tmp/euref.st
```

**本机：** **240** 行 / **STR 222**（随 caster 变）。另测：`rtk2go.com` **STR 767**；`caster.centipede.fr` **STR 1270**。

### 3.3 centipede `VALDM` → RINEX3 OBS（真转换）

公开口令与 [ntrip-client](./ntrip-client.md) 一致（`centipede`/`password`）。OBS 写 **stdout**；`CTRL+C`/`SIGINT` 在历元边界温和退出。

```bash
./rtcm3torinex -s caster.centipede.fr -r 2101 -d VALDM \
  -u centipede -p password -M http -t 30 -3 \
  > /tmp/valdm.rnx 2> /tmp/valdm.err
# 跑数秒后：kill -INT <pid>   # 或前台 CTRL+C
grep -c '^>' /tmp/valdm.rnx
head -20 /tmp/valdm.rnx
```

**本机（~11 s，SIGINT 后）：** OBS **56381 B**，`^>` 历元行 **43**；stderr：`Stop signal number 2 received. Trying to terminate gentle.`

**头（摘录）：**

```text
     3.00           OBSERVATION DATA    M (Mixed)           RINEX VERSION / TYPE
RTCM3TORINEX 2.9404 box                 20260924 092448 UTC PGM / RUN BY / DATE
RTCM3TORINEX                                                MARKER NAME
         .0000         .0000         .0000                  APPROX POSITION XYZ
G    8 C1C L1C D1C S1C C2  L2  D2  S2                       SYS / # / OBS TYPES
R    6 C1C L1C S1C C2C L2C S2C                              SYS / # / OBS TYPES
E    3 C1  L1  S1                                           SYS / # / OBS TYPES
C    3 C2I L2I S2I                                          SYS / # / OBS TYPES
  2026     9    24     9    25    6.0000000     GPS         TIME OF FIRST OBS
                                                            END OF HEADER
> 2026 09 24 09 25  6.0000000  0 12
G03  25238622.890   132629668.242 0                        39.000
```

说明：流含 1005/1006，但本段头 **APPROX 仍为 0**（流式头局限，见坑表）。同秒可能出现 **多条 `>`（按系统拆历元）**，读入前建议 [gfzrnx](./gfzrnx.md)/[rinexmod](./rinexmod.md) 或确认下游能接受。

### 3.4 `-3 -P` 混星 NAV

```bash
./rtcm3torinex -s caster.centipede.fr -r 2101 -d VALDM \
  -u centipede -p password -M http -3 -P /tmp/mix.n \
  > /tmp/valdm_p.rnx
# ~10 s 后 SIGINT
head -5 /tmp/mix.n; wc -l /tmp/mix.n
```

**本机：** `/tmp/mix.n` **6067 B / 75 行**；头 `3.02 … N: GNSS NAV DATA … M: Mixed`；体含 `R08 2026 09 24 09 15 …` 等。

### 3.5 负例（勿当成功）

```bash
# rtk2go 无合法订户
./rtcm3torinex -s rtk2go.com -d AgPartner_2 -u 'lab@example.com' -M http -3
# 本机 stderr：Could not get the requested data: HTTP/1.1 400

# 错误挂载
./rtcm3torinex -s rtk2go.com -d NOSUCHMOUNTXYZ -u 'lab@example.com' -3
# 本机：No 'Content-Type: gnss/data' found

# -P 与 -E 同开 / 无 -3 的 -P
./rtcm3torinex -3 -P mix.n -E gps.n -s x -d y
# Combined ephemeris file specified with another one.
./rtcm3torinex -P mix.n -s x -d y
# RINEX2 cannot created combined ephemeris file.
```

## 4. I/O

| 方向 | 内容 |
| --- | --- |
| 入 | **仅** NTRIP 套接字（`-s/-r/-d/-u/-p/-M/-n` 或 `ntrip:` URL）；**无**本地 RTCM 文件开关 |
| 出 OBS | **stdout** RINEX 2.11 或 3（`-3`）；`PGM`=`RTCM3TORINEX 2.9404` |
| 出 NAV | `-E/-G/-C/-Q/-B` 或 `-3 -P` 指定路径的文件 |
| 头覆盖 | `-f`：普通 RINEX OBS 头行；勿乱改 `# / TYPES` / `TIME OF FIRST OBS`（工具会警告） |
| 停 | `SIGINT/SIGTERM/SIGQUIT/SIGPIPE` → 完成当前历元再退；超时硬杀见 `ALARMTIME` |

支持电文（仓内 `rtcm3torinex.txt`）：1001–1004、1009–1013、1019/1020、1045/1046、MSM 1071–1127 等；**1005–1008 天线/坐标电文不保证写入头**（本机 APPROX=0）。

## 5. 参数（常用）

| 旗标 | 作用 |
| --- | --- |
| `-s/-r/-u/-p/-d` | caster / 端口(2101) / 用户 / 口令 / 挂载点 |
| `-t` | 读超时秒（默认 60） |
| `-M http\|ntrip1\|rtsp\|auto` | NTRIP 模式（默认 auto） |
| `-3` | RINEX3 |
| `-O` | 允许中途增加观测类型（写 change 头；下游兼容性差） |
| `-n` | 发 NMEA（需 GGA 的挂载点） |
| `-S/-R` | HTTP 代理 |

## 6. 接到哪步

```text
NTRIP caster
  ├─ 只要拆 RTCM 帧 / MSM          → pyrtcm（库）+ pygnssutils 录流
  ├─ 要一份可用 RINEX 文件（单流） → rtcm3torinex（本文）或 BNC
  └─ 多流 / GUI / 生产             → bnc
        ↓
RINEX OBS(+NAV) → georinex / gfzrnx / anubis / pytecgg / rtklib …
```

**对比 [pyrtcm](./pyrtcm.md)：** pyrtcm 读文件/串口、返回 `RTCMMessage`/`parse_msm`，**不写 RINEX**；rtcm3torinex **写 RINEX**，但 **不解析给你看 DF**。流水线常为：`pygnssutils` 录 `.rtcm3` → 实验室用 pyrtcm 质检电文；要文件级 OBS 则 BNC/本文（实时）或自写转换。

## 7. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 门户写 obsolete | 独立工具停更，逻辑进 BNC | 新项目优先 [bnc](./bnc.md)；本文仅保 SVN 路径 |
| 2 | 无法 `rtcm3torinex foo.rtcm3` | **无离线文件输入** | 先 NTRIP，或换 BNC/自写 |
| 3 | rtk2go / igs-ip 订流 400/401 | 要订户或账号 | 配真实用户；或用 centipede 公开口令探针 |
| 4 | `APPROX POSITION` 全 0 | 流式头在首历元定型；1005 未必写入 | `-f` 头模板；或事后 [rinexmod](./rinexmod.md) |
| 5 | 同秒多条 `>` 历元 | 按星座拆输出 | 下游合并/抽稀；或改 BNC |
| 6 | 后期新观测类型消失 | 默认冻结尾类型 | 加 `-O`（兼容性自担） |
| 7 | `-P` 报错 | 无 `-3` 或与 `-E/-G/…` 并用 | 只留 `-3 -P file` |
| 8 | 相位模 299792.458 / COMMENT | RTCM 模糊度未给 | 换含完整模糊度的 MSM；见 txt 说明 |
| 9 | wiki `base` 当样帧 | 实为 sourcetable 文本 | 用真 NTRIP 或自备 RTCM |
| 10 | CTRL+C 后文件截断？ | 未等温和退出 | 等 `Trying to terminate gentle` 再读盘 |

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 单挂载点命令行 → RINEX，能接受 SVN 老工具 | **rtcm3torinex（本文）** |
| 多流、GUI、持续维护 | **[bnc](./bnc.md)**（官方替代） |
| 只要电文字段 / MSM 数组 / 脚本 | **[pyrtcm](./pyrtcm.md)** + [pygnssutils](./pygnssutils.md) |
| Rust 订流探针 | **[ntrip-client](./ntrip-client.md)** |
| 自建播发 | **[bkg-ntripcaster](./bkg-ntripcaster.md)** |

