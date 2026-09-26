# satpulse 手册（GNSS → PPS / PHC / PTP / NTP 授时，Go）

目录：[`PROJECTS.json` → `satpulse`](../../PROJECTS.json) · 上游 <https://github.com/jclark/satpulse> · 文档站 <https://satpulse.net>（源在仓内 `docs/`）

**先懂三个词：**
- **PPS**（pulse per second）：接收机每秒整点从一根线上打出的电脉冲，边沿对准 GNSS 秒，精度远高于串口 NMEA 报文（报文只说「这是几点几分」，晚到几十到几百 ms）。
- **PHC**（PTP hardware clock）：网卡上的硬件时钟（Linux 里是 `/dev/ptpN`），部分网卡有 SDP 引脚能直接给 PPS 打硬件时间戳。
- **PTP**（IEEE 1588，Linux 实现是 linuxptp 的 `ptp4l`）：用 PHC 在局域网里分发亚微秒级时间；**NTP**（chrony/ntpd）精度低一档但通用。

satpulse 做的事：读接收机串口报文（NMEA/UBX/Unicore/NovAtel/SBF/RTCM…）→ 配置接收机 → 把「报文给的整秒 + PPS 边沿」变成 PHC 校时（喂 ptp4l）或 chrony SOCK / NTP SHM 参考钟样本。

## 1. 用途边界

| 能 | 不能 / 不是 |
| --- | --- |
| `satpulsed` 守护：串口读 GNSS，给 chrony（SOCK）、NTPsec（SHM）出样本；有 PHC+PPS 时校 PHC 并更新 ptp4l | 不是 PTP 协议栈：PTP 报文收发仍靠 `ptp4l` |
| `satpulsetool gps`：探测型号/固件、开关星座/频点、PPS 脉宽、survey-in/固定坐标、RTCM/原始观测输出 | 不是 PPP/RTK 解算器（定位来自接收机自身） |
| `satpulsetool scan/annotate/replay/decode/pack`：离线把字节流 ↔ JSONL，解码并跑处理管线 | 不读 RINEX（`convobs` 只转接收机原始观测） |
| `satpulsewb`：浏览器 Workbench（评估/配置接收机） | 精度取决于 PPS 接线与 PHC；**只有串口报文时只有 ms~100 ms 级** |

## 2. 安装

本机（2026-09-26 02:05–02:20 EDT，Debian x86_64）实测事实：

| 项 | 值 |
| --- | --- |
| 最新正式版 | **v0.2**（2026-05-07 07:18 EDT 发布，tag `4eeeefa`） |
| 最新预发布 | **v0.3-pre-20260913**（2026-09-12 22:34 EDT 发布，`5c8989e`） |
| 本文所测 | main **`838c9fd`**（2026-09-25 06:15 EDT；`git describe` = `v0.3-pre-20260913-71-g838c9fd1`；`VERSION` 文件 `0.3`） |
| 许可 / ★ | MIT / 64 |
| Go 要求 | `go.mod` 写 `go 1.25.0`；系统 Go 1.24.4 + `GOTOOLCHAIN=local` 报 `go.mod requires go >= 1.25.0`，改用 /tmp 下 Go **1.25.1** |
| 测试 | `go test ./...`：**86** 包 ok、26 包无测试；`-json` 统计 **7381** 个测试用例 pass、0 fail |

```bash
# 发行包（上游 docs/setup/satpulse-install.md）：Releases 页下 _amd64.deb/_arm64.deb/_armhf.deb 或 .rpm
sudo dpkg -i satpulse_<日期>_arm64.deb
# 源码（本文做法）
git clone https://github.com/jclark/satpulse && cd satpulse
for c in satpulsed satpulsetool satpulsewb ifwait devtest; do go build -o bin/$c ./cmd/$c; done
```

产物：`satpulsed` 19.7 MB、`satpulsetool` 16.5 MB、`satpulsewb` 15.4 MB、`ifwait` 4.9 MB、`devtest` 2.9 MB。源码构建的 `-V` 输出 `no version information available`（版本号由打包流程注入）。

## 3. 命令与真实输出

`-h` 要点（原样摘录）：

| 命令 | 要点 |
| --- | --- |
| `satpulsed` | `-f/--config-file`、`-d/--serial-device`、`-w/--wait`（等网卡就绪）、`-s/--systemd-log`、`-v` |
| `satpulsetool` | 子命令 `gps` `serial` `sdp`（PHC 软件定义引脚）`syncsim` `ubxsim` `convobs` `decode` `annotate` `pack` `scan` `replay` `ntrip` `pmc`（向 ptp4l 发管理报文） |
| `satpulsewb` | `-L host:port`（此时默认关闭访问 token）、`-n` 不开浏览器、`-d/-s/--vendor/--packet-log` |
| `ifwait` | `-u/-c/-t`：等网卡 up/有载波 |
| `devtest` | **无参数解析**：`-h` 也会进入 600 s 的设备热插拔监听，只能 Ctrl-C |

输入数据：gpsd 仓 `test/daemon/` 真实 u-blox 日志（gpsd commit **`43362cd`**，2026-09-24；BSD-2）：`ublox-zed-f9p-nmea.log`（ZED-F9P hpg1.11，2019-04-12 新西兰 Dunedin，纯 NMEA）与 `ublox-zed-f9t-ubx_nmea_l5.log`（EVK-F9T TIM 2.25，2025-07-31 美国 Bend，UBX+NMEA 混流）。先 `grep -av '^#'` 去掉 gpsd 注释头（原因见坑 1）。

### 3.1 离线：scan → annotate → replay

```bash
satpulsetool scan f9t.raw > f9t.jsonl          # 字节流 → JSONL 包日志
satpulsetool annotate f9t.jsonl                # 每包加 payload 解码
satpulsetool replay --vendor u-blox f9t.jsonl  # 跑处理管线，出 time/pos/navEpoch
```

- F9P：1015 包全是 NMEA（GSV 各 174、GNGSA 116、RMC/GGA/ZDA/GST/GBS 各 29）。replay 出 `time` 58、`posGeo` 58、`navEpoch` 28、`satellites` 29。
- F9T：362 包 = UBX（NAV-PVT/POSECEF/TIMEGPS/CLOCK/SAT/DOP 各 9、NAV-SIG 6）+ NMEA + **30 段无 tag 的二进制碎片**（未识别，不报错）。

真实输出片段（F9T replay，首历元）：

```json
{"type":"time",...,"data":{"utcTime":"2025-07-31T19:33:33.999880784Z","accuracy":21,"tag":"UBX","nativeMsgID":"NAV-PVT"}}
{"type":"posGeo",...,"data":{"latLon":[44.068854,-121.314135],"height":1118.512,"heightMSL":1139.862,...}}
{"type":"navEpoch",...,"data":{"fixLevel":"code","solutionDim":"3D","acc":{"pos":2.8,"hor":1.549,"vert":2.328,...},
 "numSVUsed":23,"gnssUsed":["GPS","GAL","BDS"],"bandsUsed":["L1","L5"],...}}
```

NAV-PVT 的 `nano=-119216` 被正确并入：UTC = 19:33:34 − 119.216 µs；同一历元 NMEA RMC/ZDA 给的是整秒 `19:33:34Z`。NAV-TIMEGPS 解出 `week 2377`、`leapS 18`、`tAcc 8` ns。F9P（纯 NMEA）首历元 `2019-04-12T00:39:56Z`、`[-45.877567167, 170.500111333]`、`fixLevel code / 3D / 12 星 / PDOP 1.05`。

### 3.2 伪终端：socat pty + satpulsed → chrony SOCK

```bash
socat pty,raw,echo=0,link=/tmp/gpsA pty,raw,echo=0,link=/tmp/gpsB &
python3 feed2.py f9p.raw /tmp/gpsB &   # 合成节拍：整行写入，每个 $GNRMC 前 sleep 1 s
```

配置（`sp.toml`，路径均改到 /tmp）：

```toml
[serial]
device = "/tmp/gpsA"
speed = 9600
[ntp]
sock.path = "/tmp/chrony.sock"
```

`satpulsed -f sp.toml` 真实日志：

```text
level=INFO msg="no interface specified, running without a PTP hardware clock"
level=INFO msg="detected a GPS"
level=INFO msg="initial GPS fix status" fixLevel=code solutionDim=3D
```

用 Python 绑定 `/tmp/chrony.sock` 代替 chrony 收包：每秒 1 个 **40 B** 数据报，magic `0x534f434b`（"SOCK"），`offset ≈ -235373364.66 s`（2019 年日志 vs 2026 年系统钟，差约 7.46 年，说明它如实上报「GNSS 时间 − 系统时间」），`pulse=0`（没有 PPS），`leap=0`。

### 3.3 ubxsim：上游自带 u-blox 模拟器（无需硬件的配置路径）

```bash
satpulsetool ubxsim --link /tmp/sim gps/app/ubxsim/testdata/f9p/f9p-personality.ubx &
satpulsetool gps -d /tmp/sim -s 38400        # 探测
satpulsetool gps -d /tmp/sim -s 38400 -c     # 读当前配置
satpulsetool gps -d /tmp/sim -s 38400 -g GPS,GAL -p 0.1 --survey
```

真实输出：`Hardware: ZED-F9P`、`Firmware: HPG 1.51 PROTVER 27.50`、`Supported GNSS: GPS,GAL,BDS,GLO,QZSS,SBAS`；`-c` 列出 `Time pulse: enabled; width 0.1 s; period 1 s; polarity rising; aligned to GNSS time; only when locked`、`Antenna cable delay: 50 ns`、`Mode: mobile`；改配置后回显 `Constellations enabled: GPS, GAL`、`Time GNSS: GPS`、`Mode: static`。

`satpulsewb -n -L 127.0.0.1:8099 -d /tmp/gpsA -s 9600`：`GET /` 返回 200、414 B HTML（`<title>SatPulse Workbench</title>`）；前端交互未测。

### 3.4 硬件功能（**未在真硬件测试**；配置取自上游，标来源）

```toml
# PHC 校时：上游 docs/setup/phc.md
[phc]
interface = "enp1s0"   # PPS 接到该网卡 PHC 的 SDP 引脚
pin = 1                # 非 0 号引脚才需要
# 串口 PPS：上游 configs/satpulse.toml
[serial]
pps.pin = "cts"        # cts / dcd / dsr / ri
# 更新 ptp4l：上游 configs/satpulse.toml
[ptp]
ptp4l.udsAddress = "/var/run/ptp4l"
clockAccuracy = 150
```

chrony 侧（上游 `configs/chrony.conf` 与 `docs/setup/ntp.md`）：

```text
refclock SOCK /var/run/chrony.satpulse.sock poll 2 filter 4 refid GNSS
# GPIO PPS 方案：
refclock PPS /dev/pps0 poll 2 lock GPS refid PPS
refclock SOCK /var/run/chrony.satpulse.sock offset 0.1 delay 0.2 refid GPS noselect
```

ptp4l 侧（上游 `configs/ptp4l.conf`）：`[global] masterOnly 1 / BMCA noop / clockClass 52`。systemd 用 `satpulse@ttyAMA0` 实例名传串口。

## 4. I/O 表

| 输入 | 输出 |
| --- | --- |
| 串口 / pty（`serial.device` 或 `-d`，`speed` 波特率） | chrony SOCK 数据报（40 B，magic `SOCK`）或 NTP SHM 段 |
| PPS：串口 modem 脚（cts/dcd/dsr/ri）或 PHC SDP 引脚 | PHC 被校准；ptp4l 经 UDS 收到 clockClass/accuracy |
| 字节流文件（`scan`） | JSONL 包日志：`t`、`tag`（NMEA/UBX/SDBP/NOVAA…）、`msg`、`ascii` 或 `bin`（hex） |
| JSONL 包日志（`annotate`/`replay`） | 带 `payload` 的 JSONL；管线事件 `time`/`posGeo`/`velGeo`/`posECEF`/`navEpoch`/`satellites` |
| TOML 配置（`-f` 或 `SATPULSE_CONFIG_FILE`） | 日志（slog 文本；`-s` 转 systemd 优先级格式） |

## 5. 错误用例（全部实测）

| 场景 | 真实行为 |
| --- | --- |
| `satpulsed -d /dev/ttyNOPE`（无 `-f`） | `must specify a config file with -f option or SATPULSE_CONFIG_FILE environment variable`（`-d` 不能单独用） |
| 有配置 + 错串口路径 | `open /dev/ttyNOPE: no such file or directory`，exit **1**；`satpulsetool gps` 同句 |
| TOML 语法错（`[serial` 缺 `]`） | `toml: expected character ]` 并打印出错行 |
| 未知键（`speeed=1`） | `strict mode: fields in the document are missing in the target struct`，exit **78**（严格模式，拼错不会静默忽略） |
| 类型错（`speed="fast"`） | `cannot decode TOML string into struct field daemon.SerialConfig.Speed of type *int` |
| 权限不足（非 root 开 `/dev/ttyS0`，属 `root:dialout` 660） | `open /dev/ttyS0: permission denied`，需加入 dialout 组 |
| 垃圾输入（pty 喂 `/dev/urandom`） | `GPS detection failed: cannot parse GPS output` + `received data from GPS in unrecognized format (serial communication problem?)`；进程不退出 |
| 串口无数据 | `satpulsetool gps`：约 8.6 s 后 `GPS detection failed: no output detected from GPS`，exit 1；`satpulsed` 打 WARN 后继续等 |
| 离线垃圾（20000 B 随机字节 `scan`） | exit 0；1194 段无 tag，1 段误认 `SDBP`，`replay` 报 `SDBP checksum failed` WARN |
| 波特率不对 | **未测**：pty 不模拟波特率，`-s` 任意值都能读；真串口上表现应接近「垃圾输入」行，未核实 |
| `[phc] interface="lo"` / `"enp0s3"`（virtio 无 PHC） | `interface … cannot be used because it does not have a PTP hardware clock`，exit **78** |
| `pps.pin="cts"` 用在 pty 上 | `serial PPS requires a TTY with modem-control pins: ioctl(TIOCMGET) …: inappropriate ioctl for device`，exit 1 |
| `satpulsetool serial -p dcd`（pty） | 依次 WARN：kernel 方式 `no N_PPS line discipline`、wait 方式 `TIOCMIWAIT … inappropriate ioctl`，最后 `TIOCMGET` 报错 exit 1 |
| `sock.path` 在 `/var/run` 但无 chrony | INFO `the refclock socket is not ready`，继续运行（chrony 先建 socket，satpulsed 是发送端） |
| `ptp4l.udsAddress` 但无 PHC、无 ptp4l | 无报错、照常运行（是否向 ptp4l 发送未验证） |

## 6. 坑

1. **注释头会被当数据**：gpsd 日志开头的 `# Submitter: Luke Reid <luke@…>` 被 `scan` 切成碎片，其中 `<luke` 被误标 `tag:"NOVAA"`（NovAtel 缩写 ASCII 以 `<` 开头）。喂之前先 `grep -av '^#'`。
2. **按时间间隔断包**：`replay` 默认 `--idle-gap 0.15` s；pty 回放若 96 B 一块、块间 sleep 100 ms，`satpulsed` 把句子从中间切开，报 `received invalid data` 和 `invalid GSV message number: expected 1 or 2, got 3`。改成整行写、按历元停顿后零告警。真串口不会句中停顿，这是**合成节拍**的坑。
3. **没 PPS 就只有报文精度**：SOCK 样本 `pulse=0`，时间来自 NMEA/UBX 报文到达时刻，精度 ms~百 ms 级；chrony 里要配 `offset`/`delay` 或只作 `noselect` 粗对时。
4. **pty 不能测 PPS**：pty 没有 modem-control 脚，`TIOCMGET` 直接失败；PHC 需要真网卡（虚拟机 virtio/lo 无 PHC）。
5. **Go ≥ 1.25**：Debian 13 自带 1.24 编不过。
6. **`devtest` 不认 `-h`**：直接进入 600 s 监听。
7. **源码构建无版本号**：`-V` 为 `no version information available`，报 bug 时写 commit。
8. **`satpulsewb -L` 默认关 token**：暴露到非回环地址时加 `--token`。
9. **严格 TOML**：拼错键 exit 78 是好事；但 `speed` 省略时 pty 上照样能跑（pty 无波特率），上真串口必须写对。
10. **0.3 仍是预发布**：v0.2 与 main 差大量功能（`[ntrip]`、`[[stream.push]]`、macOS/Windows 等见 NEWS.md），按版本查文档。

## 7. 选型

| 需求 | 选 |
| --- | --- |
| 树莓派/PC 做 GNSS 时间服务器，要一套「配接收机 + PPS + PHC + ptp4l/chrony」 | **satpulse** |
| 通用 GNSS 守护、给多客户端 JSON、gpsmon/cgps | [gpsd](./gpsd.md)（chrony 用 SHM/SOCK 接 gpsd，功能相近但不配 PHC） |
| 只要 NTP 且已有 `/dev/pps0` | chrony `refclock PPS` + NMEA 源（gpsd 或 satpulse） |
| PTP 协议本身、PHC↔系统钟 | linuxptp：`ptp4l`、`phc2sys`、`ts2phc -s nmea`（可替代 satpulse 的 PHC 校时，但不配接收机） |
| 老 ntpd / NTPsec | SHM 参考钟（satpulse `[ntp] shm.segment`） |
| 在 Rust 里解 UBX / 做时间尺度换算 | [ublox](./ublox.md)、[hifitime](./hifitime.md)（GPST/UTC/TAI） |
| 共视时间传递 CGGTTS | [cggtts](./cggtts.md)、[rnx2cggtts](./rnx2cggtts.md) |
| 验证导航电文真伪（OSNMA） | [galileo-osnma](./galileo-osnma.md) |

一句话：**satpulse = 接收机配置 + 授时守护**，PTP 协议交给 ptp4l，NTP 交给 chrony；只解析报文用 gpsd 或各语言库即可。

## 8. 复现记录

- 数据：gpsd `43362cd` 两份日志（BSD-2），去 `#` 注释后 58003 B / 30437 B。
- 合成部分：pty 喂数节拍脚本、随机字节垃圾、错误 TOML、`lo`/`enp0s3` PHC 配置、pty 上的 PPS 配置。
- 未测：真实接收机、PPS 捕获（串口脚 / GPIO / PHC SDP）、PHC 校时精度、chrony/ptp4l 真对接、NTP SHM、Ntrip 收发、`syncsim`、`convobs`、Workbench 前端、macOS/Windows、错误波特率。
