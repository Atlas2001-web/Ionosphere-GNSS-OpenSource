# rt-navi · Rust 实时导航（u-blox 串口 + gnss-rtk）操作手册

目录：[`PROJECTS.json` → `rt-navi`](../../PROJECTS.json) · 上游 <https://github.com/nav-solutions/rt-navi> · crates.io **`rt-navi` 0.0.1**（2024-07-28 12:39 EDT，唯一版本，下载 1251）· GitHub main **`ca95fb8`**（2026-04-12 06:40 EDT，仓内 `Cargo.toml` 已是 **0.0.2**，未发版）· **无 tag / 无 release** · **MPL-2.0** · ★**12** · README 标 MSRV 1.87 · edition 2024 · 本机 **rustc 1.98.1**，实测 2026-09-26 03:32–03:50 EDT；**质检复跑** 04:03–04:15 EDT

> 岗位：概念验证（PoC）——把 u-blox 接收机当「原始测量器」，从串口读 UBX `RXM-RAWX`（伪距）+ `RXM-SFRBX`（GPS 星历），喂给 [gnss-rtk](./gnss-rtk.md) 逐历元解 PVT，打印到日志。冲突时：**上游源码 > README > 本文**。  
> **本篇没有真接收机**：所有接收机相关行为均为「**未在真接收机测试**」，数据来自 socat 伪串口回放公开 F9P 录制（§3）。

> **质检复跑通过**（2026-09-26 04:03–04:15 EDT）。
> - 环境：rustc **1.98.1**；`CARGO_TARGET_DIR` 独立目录；release 冷编译 **1 min 20 s**（补丁版再编 **1 min 14 s**），二进制 **≈38.5 MB**，`--version` → `rt-navi 0.0.2`；`--help` 去 ANSI 与原文一致。crates.io **0.0.1**/下载 **1251**/2024-07-28 16:39 UTC；GitHub main **`ca95fb8`**/MPL-2.0/★**12** 核对无误。
> - 数据：rtkexplorer F9P zip（wpdmdl=2552）→ `rover.ubx` **14071360 B** sha256 `ba2e782f…95156a`；pyubx2 **1.3.7**：RAWX **4521**/SFRBX **92962**/GNRMC·GGA·GLL·GST 各 **4521**/无 NAV-PVT。
> - 上游原样 200 历元：stdout 启动段与 `Did not receive ACK` 一致；**200/200** `pre-fit`、**0** 解；回写 **70 B** = CFG-MSG×3（RAWX/NAV-PVT/SFRBX）+ CFG-RATE measRate=**10000** navRate=**10** timeRef=**1** + MON-VER。
> - SPP+仅 L1 补丁 400 历元：解 **173**；首解行 `lat=40.097007° long=254.852687 alt=1590.218778m | dt=4.783406E-3s` 逐字；错误计数 125/101/1；对 PPK（ECEF）3D 中位/p95/max **14.246 / 22.589 / 23.080 m**，水平 **5.669 m**，天向 **+13.063 m** 逐位一致；GGA×383（alt+sep，GGA 时标按 UTC+18→GPST）对 PPK 中位 **1.281 m**/max **2.152 m**。
> - 错误：`/dev/ttyNOPE`/`/dev/null` panic exit **101**；`-b abc` exit **2**；同伪串口二次打开 busy **101**；64 KiB 随机静默；写端断开约 3 s → Broken pipe 日志洪水 **≈97 MB / 140 万行**（与原文 144 MB/209 万同行量级，时长切点略异）。
> - 未重跑：仅 SPP（不滤 L1）16.102 m 表行、LNAV 子帧交叉细表、`ubx27/31`、真接收机。


## 1. 用途与边界

**做（源码 + 回放实测）：**

- 打开**一个**串口（`serialport`，8E1，10 ms 读超时），写 5 条 UBX 配置：`CFG-MSG` 开 RAWX/NAV-PVT/SFRBX、`CFG-RATE`、`MON-VER` 轮询
- 解析 `RXM-RAWX` → 每星一个 `Candidate`（只填伪距）；`RXM-SFRBX` GPS/QZSS LNAV 子帧 1–3 → 开普勒星历缓存
- 调 `gnss_rtk::PPP::new_survey(...).resolve()`，成功打 `new solution | lat=… long=… alt=…`，失败打 `ppp error: …` 并 `reset()`
- 接收机自己的 `NAV-PVT` 若到达，打 `ublox lat=… long=… alt=…` 供对照（本篇录制无 NAV-PVT，未触发）

**不做：** 文件/回放输入（非 tty 直接 panic，§5）；RINEX/NMEA/CSV/GPX 输出；RTK（README 写「近期开发」，`rtcm.rs` 只有空结构体且未编译）；载波相位（代码注释掉）；多接收机。

| 易混 | 是什么 | 区别 |
| --- | --- | --- |
| **本文** main `ca95fb8` | 真正调 gnss-rtk 的版本 | 须 git clone 自编；`-p/--port` |
| crates.io `rt-navi 0.0.1` | 2024 年 rtk-rs 时期存根 | `main()` 打开串口后**直接返回**，不读数据、不解算（§3.1） |
| [gnss-rtk](./gnss-rtk.md) | PVT 求解库 | rt-navi 锁 git rev `5eb681c`（=0.7.6，MPL-2.0，2025-05-29），比其 main 落后 18 提交 |
| [ublox](./ublox.md) | UBX 编解码 crate | rt-navi 用 **0.6**（当前 0.10.0）；0.6 的 RAWX 块不暴露 `sigId`（记作 `reserved2`） |

## 2. 安装

```bash
export CARGO_TARGET_DIR=/tmp/rtnavi-man/target CARGO_HOME=/tmp/rtnavi-man/cargo
git clone https://github.com/nav-solutions/rt-navi && cd rt-navi   # 子模块 tools 可不拉
cargo build --release                                              # 默认 feature ubx23（M8 系）
$CARGO_TARGET_DIR/release/rt-navi --version                         # → rt-navi 0.0.2
```

- 本机 1.98.1：**1 min 14 s** 编过，18 条 warning（死代码、`proc-macro-error2` future-incompat），二进制 38.5 MB；首次拉依赖+编译占 `/tmp/rtnavi-man` 约 1.9 GB
- 仓库 **不提交 Cargo.lock**（`.gitignore`），每次解析最新 semver 依赖，今天能编≠明天能编
- 协议选择：`--no-default-features --features ubx27`（F9）/ `ubx31` / `ubx14`。README 写的 `--ubx31` 不是合法 cargo 参数；只能选一个，`--all-features` 不能编（README 自述，未测）
- `cargo install rt-navi` 装到的是 **0.0.1 存根**；它 `--locked` 在 1.98.1 上 2 min 03 s 可编过，但无用

## 3. 命令与真实输出

### 3.1 CLI（`--help` 原文，去 ANSI 色）

```text
High precision Navigation, in real time

Usage: rt-navi [OPTIONS] --port <port> [COMMAND]

Commands:
  ublox  Select configuration settings for specific UART/USB port to send to uBlox as configuration message
  help   Print this message or the help of the given subcommand(s)

Options:
  -h, --help
          Print help (see a summary with '-h')
  -V, --version
          Print version

GNSS Receiver (Hardware):
  -p, --port <port>
          Define serial port (ex: /dev/ttyACM0 on Linux)
  -b, --baud <baud>
          Serial port baud rate
          [default: 9600]
```

- `ublox` 子命令有 `--select usb|uart1|uart2`、`--baud`、`--stop-bits`、`--data-bits`、`--parity`、`--in-*/--out-*`，**但 `main.rs` 从不读取**（配置端口代码整段注释），传了等于没传
- README 的 `--coords-ecef-km=…` 初值选项 **CLI 里不存在**
- 无参数 → 打印帮助，exit 2。0.0.1 存根的 CLI 只有 `-u, --ublox <PORT>`，对伪串口 exit 0 立即退出
- 日志走 **stdout**（env_logger，`RUST_LOG=info|debug|trace`，时间戳为 UTC `Z`）；`Malformed packet`、`Did not receive ACK` 走 **stderr**

### 3.2 回放：socat 伪串口 + 公开 F9P 录制

数据：rtkexplorer「U-blox F9P kinematic PPP data set 12/24/20」（<https://rtkexplorer.com/download/u-blox-f9p-kinematic-ppp-data-set-12-24-20/>，zip sha256 `fd9e58a1…ddf6f8`）中 `rover.ubx`（14071360 B，sha256 `ba2e782f…95156a`）。pyubx2 1.3.7 统计：`RXM-RAWX` 4521、`RXM-SFRBX` 92962、NMEA GNRMC/GGA/GLL/GST 各 4521，**无 NAV-PVT**；2020-12-24 21:28:42–22:44:02 GPST，前 40 min 静止。参考真值：同包 `rover_ppk.pos`（RTKLIB demo5 b33f 动态 PPK，Q=1）。

```bash
socat pty,raw,echo=0,link=/tmp/rtnavi-man/ttyRX pty,raw,echo=0,link=/tmp/rtnavi-man/ttyTX &
RUST_LOG=info rt-navi -p /tmp/rtnavi-man/ttyRX > run.log 2>&1 &
sleep 4
# replay.py：按 RXM-RAWX 边界切块，每块写入 ttyTX 后停 50 ms（20× 加速），并收走 rt-navi 写回的字节
python replay.py rover.ubx /tmp/rtnavi-man/ttyTX 0.05 0 200
```

`replay.py`（本篇自写，pyubx2 只用来找 RAWX 字节偏移）：

```python
import sys, os, time, select
from pyubx2 import UBXReader
src, tty, gap, start, n = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
data, offs, pos = open(src, 'rb').read(), [], 0
with open(src, 'rb') as s:
    for raw, p in UBXReader(s, protfilter=7, quitonerror=0):   # NMEA+UBX+RTCM 都计长度
        if getattr(p, 'identity', '') == 'RXM-RAWX':
            offs.append(pos)
        pos += len(raw)
offs.append(len(data))
fd, back = os.open(tty, os.O_RDWR | os.O_NOCTTY), b''
for i in range(start, min(start + n, len(offs) - 1)):
    os.write(fd, data[offs[i] if i else 0:offs[i + 1]])
    t_end = time.time() + gap
    while time.time() < t_end:                      # 同时收走 rt-navi 写出的 CFG 字节
        if select.select([fd], [], [], max(0, t_end - time.time()))[0]:
            back += os.read(fd, 4096)
open('back.bin', 'wb').write(back)
```

pyubx2 解析 14 MB 需约 20 s，rt-navi 在此期间空等；每次运行后要杀掉并**重开 socat**（§5 独占锁）。

**块间必须留空隙**：rt-navi 读到一次 10 ms 超时才把本轮候选交给解算器；100 个 RAWX 一口气写入 → 解析 100 次 `new measurements`，只产生 **1** 个 proposal（其余被 `candidates.clear()` 覆盖）。

上游 main 原样（200 历元，`RUST_LOG=info` 的 stdout 原文节选）：

```text
[2026-09-26T07:48:21Z INFO  anise::almanac] Loading bytes as DAF/SPK
[2026-09-26T07:48:21Z INFO  rt_navi] solver deployed
Did not receive ACK message for request
[2026-09-26T07:48:24Z INFO  rt_navi] rt-navi deployed
[2026-09-26T07:48:42Z ERROR rt_navi] ppp error: not enough candidates match pre-fit criteria
[2026-09-26T07:48:43Z ERROR rt_navi] ppp error: not enough candidates match pre-fit criteria
```

- 200/200 历元全部 `pre-fit` 失败，**0 个解**。`debug` 下每星一条 `missing secondary frequency`（共 7655 条）：`Config::default()` 的 `method` 是 **CPP（双频码）**，而 rt-navi 把所有信号都标成 `Carrier::L1` → 永远凑不出第二频点。README 日志里的 `method: SPP` 与当前代码不符
- 启动时回读到 rt-navi 写出的 70 B，pyubx2 解码：3×`CFG-MSG`（RAWX/NAV-PVT/SFRBX，6 个端口 rate=1）、`CFG-RATE measRate=10000, navRate=10, timeRef=1`、`MON-VER` 轮询。源码构造了开 GPS/Galileo/QZSS、关 GLONASS 的 `CFG-VALSET`，**但从未发送**

### 3.3 本地两行补丁后能出解（非上游行为）

```diff
+    cfg.method = Method::SPP;                          // src/main.rs
+    if meas.reserved2() != 0 { continue; }             // src/ublox/mod.rs：只留 sigId 0（L1C/A、E1、B1I…）
```

前 400 历元（21:28:42–21:35:21 GPST）：

```text
[2026-09-26T07:44:11Z ERROR rt_navi] ppp error: survey initialization requires at least 4 SV temporarily
[2026-09-26T07:44:12Z INFO  rt_navi] new solution | lat=40.097007° long=254.852687 alt=1590.218778m | dt=4.783406E-3s drift=0.000000E0s/s
[2026-09-26T07:44:12Z ERROR rt_navi] ppp error: first solution is discarded
[2026-09-26T07:44:13Z ERROR rt_navi] ppp error: not enough candidates match post-fit criteria
```

| 版本 | 解数 / 400 | 首解 | 3D 误差中位 / p95 / max（对 PPK） | 水平中位 | 天向中位 |
| --- | ---: | --- | --- | ---: | ---: |
| 仅 SPP 补丁 | 173 | 21:29:08（首个 RAWX 后 26 s） | 16.102 / 27.283 / 28.192 m | 6.874 m | +14.716 m |
| SPP + 只留 L1 | 173 | 21:29:08 | 14.246 / 22.589 / 23.080 m | 5.669 m | +13.063 m |
| F9P 自身 GGA（383 历元） | — | — | 1.281 m 中位，max 2.152 m | — | — |

其余历元：125 次 `survey initialization requires at least 4 SV temporarily`（前 ~26 s 等星历）、101 次 `not enough candidates match post-fit criteria`、1 次 `first solution is discarded`。经度按 0–360° 打（254.85° = −105.15°），`long=` 后无 ° 号。

## 4. 交叉检查（pyubx2 1.3.7 独立解同一文件）

| 项 | pyubx2 | rt-navi | 结论 |
| --- | --- | --- | --- |
| RAWX 历元（前 200） | 200，首历元 `rcvTow=422922.005` week 2137 | 200 次 `new measurements`，时刻 `2020-12-24T21:28:42 GPST` | 一致（rt-navi 把 TOW **四舍五入到整秒**） |
| 每历元候选数 | 去重卫星数（首历元 62 条测量 → 39 星） | `new proposal (39 candidates)` | 200/200 一致 |
| 伪距值 | 7655 个星-历元 | 7655 条 `L1 observation: c_n=…` | 与「该星在 RAWX 中**最后一个信号**的 prMes」max\|Δ\| = 0 m |
| 是否真是 L1 | sigId 0 的 prMes | 同上 | **4916/7655 不同**，中位 2.918 m，max 73.046 m（L2C/E5b/B2I 覆盖了 L1） |
| GPS LNAV 子帧（前 200 历元） | L1C/A sf1/2/3 = 52/59/60；L2C（sigId 4）118 帧 | 合法 TOW 的 Ephemeris1/2/3 = 52/59/60 | 合法部分完全一致 |
| 伪子帧 | — | 另有 43 个 Ephemeris1 + 6 个 Ephemeris2，TOW=30402、620226 等（>604800） | L2C CNAV 帧被当 LNAV 误解，进星历缓存 |

补丁后 L1 值逐一核对：15014 个值与 sigId 0 prMes 差为 0。

## 5. 错误用例（伪串口 socat；除「不存在设备」外输入均为**合成**）

| 输入 | 结果 |
| --- | --- |
| `-p /dev/ttyNOPE` | **panic**，exit 101：`Failed to open port /dev/ttyNOPE: No such file or directory` |
| `-p /dev/null`（非 tty） | **panic**，exit 101：`Failed to open port /dev/null: Not a typewriter` → 不能直接读文件 |
| 同一伪串口第二次打开 | **panic** `Device or resource busy`（serialport 独占锁）；第一个进程被杀后仍 busy，须重开 socat |
| `-b abc` | clap 报错，exit 2 |
| `-b 0` / `-b 4000000` | 伪串口不管波特率，照常启动、静默；真串口错波特率**未测** |
| 空输入（无字节） | 3 s 后 `Did not receive ACK message for request`，之后**静默空转** |
| 64 KiB 随机字节（合成） | **静默**，无任何日志 |
| 截半的 RAWX + 完整 RAWX（合成） | 半帧丢弃，下一帧正常解析；两次运行一次静默、一次 stderr 1 行 `Malformed packet` |
| RAWX 改一个字节（合成） | stderr `Malformed packet, ignore it; cause Not valid packet's checksum, expect 0x27b0, got 0x9bad`，丢帧 |
| 头长度 0xFFFF（合成） | 静默恢复，后续帧正常 |
| 写端关闭（杀 socat） | `ERROR … ublox error: Broken pipe` **死循环**：约 3 s 写出 209 万行 / 144 MB |
| SIGTERM | 直接退出 143，无收尾 |

## 6. I/O

- **输入**：仅串口/tty。需要 `RXM-RAWX`（伪距）+ `RXM-SFRBX`（GPS/QZSS LNAV）；Galileo/BeiDou/GLONASS 只进候选、无星历，SBAS 也进候选
- **输出**：只有日志行（stdout），无文件。解：`lat`（°）、`long`（0–360°）、`alt`（m，椭球高）、`dt`（s）、`drift`（s/s）
- **写接收机**：启动即写 `CFG-MSG`×3 + `CFG-RATE`（RAM 层，未存 flash）+ `MON-VER` 轮询；**会改掉接收机当前输出率**

## 7. 坑

1. 上游默认 CPP + 全标 L1 → 本篇录制 **0 解**；要出解至少改成 SPP（§3.3），这是本地补丁不是上游行为
2. ublox 0.6 拿不到 `sigId`：多频接收机（F9P/F9T）同一颗星的 L1/L2 伪距互相覆盖，最多差 73 m；L2C CNAV 帧被误解成 LNAV 子帧
3. `CFG-RATE measRate=10000 ms, navRate=10`：真接收机上会变成**每 10 s 一个测量、100 s 一个导航解**（按 UBX 定义推断，**未在真接收机测试**）
4. `CFG-VALSET` 构造了但没发；README 说的「GPS+QZSS+Galileo 激活」不会发生
5. 串口写死 **8E1**（偶校验）；u-blox 出厂 UART 通常 8N1——真 UART 可能收不到正确字节（**未在真接收机测试**；USB-ACM 不受影响）
6. 解算只在读超时后触发：一次读到多个 RAWX 只解最后一个；TOW 取整到秒，>1 Hz 采样会撞时刻
7. 写端断开 → 日志洪水（数十 MB/s），日志重定向到文件时会迅速吃满磁盘
8. `ublox` 子命令与 README 的 `--coords-ecef-km` 都是摆设；crates.io 0.0.1 是存根；无 Cargo.lock、无 tag，定版只能记 commit
9. 即使补丁后，SPP 天向偏 +13 m、3D 中位 14 m，远差于同一接收机自身解（1.3 m）：只能算「链路能通」的演示

**未测**：真接收机（M8/F9，USB 与 UART）、`ubx14/27/31` feature、NAV-PVT 对照打印、QZSS 星历、长时间运行/内存、RTK、`ublox` 子命令、MSRV 1.87。

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 看 gnss-rtk 能否接实时 u-blox 流（演示/读代码） | **本文**，但要自己打补丁 |
| Rust 里编解码 UBX、配置接收机 | [ublox](./ublox.md)（0.10 有 `sigId`；rt-navi 仍用 0.6） |
| Rust 里自己搭 PVT，喂 RINEX/自定义观测 | [gnss-rtk](./gnss-rtk.md) |
| Rust 离线「RINEX OBS+NAV → 坐标」一步到位 | [sidereon](./sidereon.md) |
| u-blox 串口/文件 → RINEX，再事后处理 | [ubx2rinex](./ubx2rinex.md) →（[rtklib](./rtklib.md)/[sidereon](./sidereon.md)） |
| 多客户端共享接收机、要接收机自己的定位解 | [gpsd](./gpsd.md) |
| Python 解/造 UBX、做本篇式交叉核对 | [pyubx2](./pyubx2.md) |
| 串口实时 RTK/PPP 且要结果可信 | RTKLIB `rtknavi`/`rtkrcv`（[rtklib](./rtklib.md)），不是本文 |

30 秒：**rt-navi = nav-solutions 的「u-blox 串口 → gnss-rtk」PoC；无文件输入、无输出文件；上游默认配置在 F9P 录制上 0 解，改 SPP 后 3D 中位约 14 m。要可用工具请走 ubx2rinex + 离线求解，或 RTKLIB。**
