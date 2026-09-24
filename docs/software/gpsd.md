# gpsd · GNSS/AIS 守护进程操作手册

目录：[`PROJECTS.json` → `gpsd`](../../PROJECTS.json) · 上游 <https://gitlab.com/gpsd/gpsd> · 官网 <https://gpsd.io/> · Debian **`gpsd` 3.25-5+deb13u2**（`gpsd-clients` / `gpsd-tools` 同版）· 许可 **BSD** · 本机验证 **`/usr/sbin/gpsd: 3.25 (revision 3.25)`** + `gpsfake`/`gpspipe`（2026-09-24 05:41 EDT）：无接收机时用自写 NMEA（北京坐标，对齐 [pynmeagps](./pynmeagps.md)/[pygnssutils](./pygnssutils.md)）喂 `gpsfake -P 2949` → `gpspipe -w` TPV **mode=3** lat=**39.904187167** lon=**116.390742667** altMSL=**44.0** uSat=**12**

> 岗位：用户态 **守护进程**：串口/USB/网络源上的 NMEA/厂商二进制 → 统一 JSON/NMEA 多客户端分发（默认 TCP **2947**）。冲突时：**本机 `gpsd -h` / 官网手册 > 本文**。  
> NMEA 编解码库 → [pynmeagps](./pynmeagps.md)；UBX 库 → [pyubx2](./pyubx2.md)；流/NTRIP CLI → [pygnssutils](./pygnssutils.md)；UBX→RINEX → [ubx2rinex](./ubx2rinex.md)；Pi 基站捆 gpsd → [rtkbase](./rtkbase.md)；多流 GUI → [bnc](./bnc.md)。

## 1. 用途与边界

**做：**

- 监听串口/`tcp://`/`udp://`/`ntrip://`/`gpsd://` 等源，识别驱动（本机 `-l` 含 **NMEA0183**、**u-blox**、**RTCM104V3** 等）
- 向多客户端推送统一 **JSON**（`TPV`/`SKY`/`DEVICE`…）或伪 NMEA（`gpspipe`）
- 无硬件时用 **`gpsfake`** 把日志/NMEA 文件喂进临时 gpsd（pty）
- 客户端工具：`gpspipe`、`cgps`/`gpsmon`、`gpsctl`、`gpsdecode`、`gpsrinex` 等（`gpsd-clients`）

**不做：**

- **不是** 精密载波 / PPP / RTK 引擎 → [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)/[ginan](./ginan.md)
- **不是** TEC / ROTI / 电离层产品 → 落盘观测后走 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)
- **不是** 厂商帧级编解码 API → [pynmeagps](./pynmeagps.md)/[pyubx2](./pyubx2.md)/[pyrtcm](./pyrtcm.md)
- **不是** 多挂载 NTRIP 生产 caster → [bkg-ntripcaster](./bkg-ntripcaster.md)/[bnc](./bnc.md)
- **不是** UBX→RINEX 采集器 → [ubx2rinex](./ubx2rinex.md)

一句话：`gpsd` = **位置/时间守护进程 + 多客户端分发**；电离层产品在「观测落盘」之后。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** `gpsd` | C 守护进程 + clients | `/usr/sbin/gpsd -V` → `3.25`；默认口 **2947** |
| [pygnssutils](./pygnssutils.md) | Python 流 CLI | `gnssstreamer`；无守护多客户模型 |
| [rtkbase](./rtkbase.md) | Pi 基站栈 | `install.sh --gpsd-chrony` 可捆本文 |
| [bnc](./bnc.md) | 多流 GUI/录盘 | Qt；不是系统 gpsd |

| 术语 | 含义 |
| --- | --- |
| `TPV` | Time-Position-Velocity JSON；`mode` 1=无修 / 2=2D / **3=3D** |
| `SKY` | 天空视图；`uSat`/`hdop` 等 |
| `gpsfake` | 用日志文件冒充接收机喂 gpsd（测客户端） |
| 控制套接字 `-F` | hotplug/`gpsdctl`；Debian 常由 systemd socket 激活 |

## 2. 安装

```bash
sudo apt-get update
sudo apt-get install -y gpsd gpsd-clients
# 可选：额外工具包（本机依赖链已拉上 gpsd-tools）
# sudo apt-get install -y gpsd-tools

# Debian 把守护进程放在 sbin（普通用户 PATH 常无）
/usr/sbin/gpsd -V
# 期望：/usr/sbin/gpsd: 3.25 (revision 3.25)
dpkg -l gpsd gpsd-clients | awk '/^ii/{print $2,$3}'
# 期望：gpsd 3.25-5+deb13u2
#       gpsd-clients 3.25-5+deb13u2

which gpsfake gpspipe gpsctl gpsdecode
gpsfake --version    # 期望：gpsfake: Version 3.25
gpspipe -V           # 期望：gpspipe: 3.25 …

/usr/sbin/gpsd -h | head -25
/usr/sbin/gpsd -l    # 已编译驱动列表
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `gpsd: command not found` | 二进制在 `/usr/sbin` | 用全路径，或 `export PATH="/usr/sbin:$PATH"` |
| 串口 `Permission denied` | 不在 `dialout` | `sudo usermod -aG dialout $USER` 后重登 |
| `DEVICES=""` 开机无设备 | `/etc/default/gpsd` 空 | 填 `DEVICES="/dev/ttyACM0"` 或靠 USBAUTO/`gpsdctl` |
| 本机无 systemd（容器） | PID1 非 systemd | 前台：`gpsd -N -n /dev/…`；或只用 `gpsfake` |

**本机 `/etc/default/gpsd`（Debian 默认）：** `DEVICES=""`、`GPSD_OPTIONS=""`、`USBAUTO="true"`。本验证环境 **无 systemd 总线**、**无 GNSS 接收机**，未启系统服务。

## 3. 端到端（本机 3.25 真跑；2026-09-24 05:41 EDT）

**样例来源：** 自写 `~/iono_ops/gpsd-demo/demo_beijing.nmea`（36 行 RMC+GGA+GSA；坐标与 [pynmeagps](./pynmeagps.md)/[pygnssutils](./pygnssutils.md) 手册北京点一致：`3954.25123,N` / `11623.44456,E`，日期 `240926`）。另有同目录 `demo_pygnss.nmea`（5 行，源自既有 pygnssutils 探活文件）。

### 3.1 版本 / 帮助（摘录）

```bash
export PATH="/usr/sbin:$PATH"
gpsd -V
gpsd -h
```

**本机（节选）：**

```text
gpsd: 3.25 (revision 3.25)
usage: gpsd [OPTIONS] device...
  -S, --port PORT           = set port for daemon, default 2947
  -n, --nowait              = don't wait for client connects to poll GPS
  -N, --foreground          = don't go into background
  -l, --drivers             = list compiled in drivers, and exit.
…
The following driver types are compiled into this gpsd instance:
                                NMEA0183
…
        n       b       c       *       u-blox
…
                        *       RTCM104V3
```

### 3.2 `gpsfake` + `gpspipe -w`（无接收机真 I/O）

```bash
mkdir -p ~/iono_ops/gpsd-demo && cd ~/iono_ops/gpsd-demo
# 准备 demo_beijing.nmea（见上；首两句）：
# $GNRMC,123519.00,A,3954.25123,N,11623.44456,E,0.1,0.0,240926,,,A*4B
# $GNGGA,123519.00,3954.25123,N,11623.44456,E,1,12,0.9,44.0,M,-8.0,M,,*5C

export PATH="/usr/sbin:$PATH"
# -1 单遍；-n 不等客户端就读；-P 改端口避开系统 2947；-c 句间延时
gpsfake -1 -n -P 2949 -c 0.05 demo_beijing.nmea &
# 等监听起来后：
gpspipe -w -n 40 localhost:2949 | tee /tmp/gpspipe_gpsd.json
# 结束后杀掉 gpsfake/临时 gpsd（或等 -1 自然结束）
```

**本机 `gpspipe -w` 类计数（40 行）：** `VERSION`×1 · `DEVICES`×1 · `WATCH`×1 · `DEVICE`×1 · `TPV`×24 · `SKY`×12。

**本机 TPV（首帧 3D，含 `epv`；摘录）：**

```text
{"class":"TPV","device":"/dev/pts/1","mode":3,"time":"2026-09-24T12:35:19.000Z",
 "lat":39.904187167,"lon":116.390742667,"altHAE":36.0,"altMSL":44.0,"alt":44.0,
 "epv":18.4,"eph":17.1,"speed":0.051,"track":0.0,"geoidSep":-8.0,"sep":22.8,…}
```

**本机 SKY / DEVICE（摘录）：**

```text
{"class":"SKY","device":"/dev/pts/1","hdop":0.9,"uSat":12}
{"class":"DEVICE","path":"/dev/pts/1","driver":"NMEA0183","readonly":"true",
 "bps":4800,"parity":"N","stopbits":1,"cycle":1.0,…}
```

| 字段 | 本机值 | 备注 |
| --- | --- | --- |
| 监听 | `localhost:2949`（`-P 2949`） | 默认应为 **2947** |
| `mode` | **3** | 3D fix |
| `lat` / `lon` | **39.904187167** / **116.390742667** | 与 NMEA 北京点一致 |
| `altMSL` / `altHAE` | **44.0** / **36.0** | GGA 椭球高差 → HAE |
| `time` | **2026-09-24T12:35:19.000Z** | RMC 日期 `240926` + GGA 时刻 |
| `uSat` / `hdop` | **12** / **0.9** | 来自 GSA/GGA |
| pty 驱动 | **NMEA0183** @ **4800** 8N1 | `gpsfake` 默认从口 |

末帧（同次抓取）约 `lat=39.904189` / `lon=116.390744`（样例内坐标微递增）。数字随样例变，勿当金样。

### 3.3 有硬件时（本机未跑）

```bash
# 用户进 dialout 后：
sudo gpsd -N -n -D 2 /dev/ttyACM0
# 另开终端：
gpspipe -w -n 20
# 或交互监视（需终端）：cgps / gpsmon
```

本机无 `/dev/ttyACM*` / USB GNSS，**未**捕获真机 stdout。

### 3.4 边界探针

| 探针 | 本机结果 |
| --- | --- |
| `echo '$GNGGA…*5C' \| gpsdecode -j` | **空 stdout**（exit 0）；单句 NMEA 对本机 3.25 客户端无可见 JSON |
| `gpsctl -f localhost:2949` | `stat(localhost:2949) failed`——`gpsctl` 要的是 **设备路径**，不是 `host:port` |
| `systemctl status gpsd` | 无 systemd 总线（容器）；`/etc/default/gpsd` 仍可读 |
| 默认服务无 `DEVICES` | 开机不会自动绑串口；需配置或 USB hotplug |

## 4. I/O 与关键参数

| 入口 | 作用 |
| --- | --- |
| `gpsd [opts] device…` | 守护进程；`device` 可为串口或 URL |
| `-S PORT` | JSON/NMEA 服务口，默认 **2947** |
| `-n` / `-N` | 立即轮询 / 前台 |
| `-l` | 列出驱动后退出 |
| `-F sock` | 控制套接字（hotplug） |
| `gpsfake [opts] logfile…` | 日志→临时 gpsd；`-P` 端口、`-1` 单遍、`-n` nowait、`-c` 周期 |
| `gpspipe -w` | 订 JSON WATCH；`-n COUNT` / `-s SEC` |
| `gpspipe --nmea` | 伪 NMEA 输出 |

| JSON class | 用途 |
| --- | --- |
| `VERSION` | 协议/发行（本机 release **3.25**，proto **3.15**） |
| `DEVICES`/`DEVICE` | 源路径、驱动、波特率 |
| `WATCH` | 订户旗标（json/nmea/raw…） |
| `TPV` | 时间·位置·速度 |
| `SKY` | 卫星/DOP |

## 5. 接到哪步

```text
接收机串口 / NMEA·UBX 日志
  → gpsd / gpsfake（本文）→ 多客户端 JSON/NMEA（2947）
  → 应用取位 / 授时（rtkbase 可捆 chrony）
录原始观测 / 差分改正 → pygnssutils / ubx2rinex / bnc
  → RINEX → georinex / pytecgg / rtklib
NMEA/UBX 帧级脚本 → pynmeagps / pyubx2（不必经 gpsd）
```

路径 C（实验室 CORS）可把本文与 [pygnssutils](./pygnssutils.md)/[rtkbase](./rtkbase.md) 并列：gpsd 管「系统取位分发」，pygnssutils/BNC 管「流与改正」。

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `gpsd: command not found` | 在 `/usr/sbin` | 全路径或改 PATH |
| 2 | 客户端连上无 TPV | 守护在等客户端且无 `-n`；或无源 | `gpsd -n …`；查 `DEVICES`/串口 |
| 3 | 串口打不开 | 权限/`dialout` | 加组重登；或 `sudo` |
| 4 | `gpsfake` 后口非 2947 | 忘了 `-P` / 与系统实例冲突 | 显式 `-P`；`gpspipe … host:port` |
| 5 | `cgps`/`gpsmon` 在 CI 挂住 | 交互 TUI | 用 `gpspipe -w -n …` 非交互 |
| 6 | 当 PPP/TEC 引擎 | 职责是分发位置 | 观测落盘另走 RTKLIB/pytecgg |
| 7 | `gpsctl host:port` 失败 | 要设备节点 | `gpsctl /dev/ttyACM0`；JSON 用 `gpspipe` |
| 8 | `gpsdecode` 吃 GGA 无输出 | 本机 3.25 实跑空 | 解码 NMEA 改 [pynmeagps](./pynmeagps.md)；或走 gpsd→TPV |
| 9 | systemd 配置不生效 | 容器无 PID1 systemd | 前台 `-N` 或只用 gpsfake |
| 10 | USB 插上无设备 | `USBAUTO`/udev/权限 | 查 `gpsdctl`、`/dev/tty*`、组 |
| 11 | 多客户端互相抢串口 | 直接打开同一 tty | **只**让 gpsd 独占设备，客户连 2947 |
| 12 | NTRIP URL 当 caster | gpsd 是订户侧源 | 自建 caster → [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 13 | 时间/日期怪 | 仅 GGA 无日期 | 样例带 RMC 日期；或接收机输出 ZDA/RMC |
| 14 | `alt`≠`altHAE` | MSL vs 椭球高 | 读字段名；本机差来自 `geoidSep` |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 系统级 GNSS 取位 / 多进程共享 | **本文 gpsd** |
| 无硬件测客户端 | **gpsfake** + `gpspipe` |
| 脚本解析/生成 NMEA | [pynmeagps](./pynmeagps.md) |
| 脚本 UBX / 录流 / NTRIP CLI | [pyubx2](./pyubx2.md) / [pygnssutils](./pygnssutils.md) |
| UBX→RINEX | [ubx2rinex](./ubx2rinex.md) |
| Pi 基站 + Web + 可选 gpsd 授时 | [rtkbase](./rtkbase.md) |
| 多流录盘 / 生产差分 | [bnc](./bnc.md) / [bkg-ntripcaster](./bkg-ntripcaster.md) |
| PPP / TEC | [rtklib](./rtklib.md) / [pytecgg](./pytecgg.md) |

## 8. 相关

[pynmeagps](./pynmeagps.md) · [pyubx2](./pyubx2.md) · [pygnssutils](./pygnssutils.md) · [ubx2rinex](./ubx2rinex.md) · [pygpsclient](./pygpsclient.md) · [rtkbase](./rtkbase.md) · [bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [ntrip-client](./ntrip-client.md) · [rtklib](./rtklib.md) · [README](./README.md)
