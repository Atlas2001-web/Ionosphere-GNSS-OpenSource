# pygnssutils · GNSS 流 / NTRIP 操作手册

目录：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pygnssutils> · API 文档 <https://www.semuconsulting.com/pygnssutils> · PyPI `pygnssutils` · BSD-3-Clause

> 面向 **串口/TCP/NTRIP 探活、录流、轻量播发** 的岗位。主 CLI：`gnssstreamer`（原 `gnssdump`）、`gnssntripclient`、`gnssserver`、`pyrinexconv`。Python≥3.10。参数以本机 `-h` 与上游 README 为准。

## 1. 用途与边界

### 1.1 一句话

pygnssutils 是 semuconsulting 出品的 Python GNSS 工具集：在同一流里解析 NMEA/UBX/SBF/UNI/QGC/RTCM3/SPARTN，并提供 NTRIP 客户端、TCP/NTRIP 轻量服务端、以及实验性二进制日志→RINEX 转换。

### 1.2 核心组件

| 组件 | 角色 |
| --- | --- |
| `GNSSReader` | 多协议合流读取类 |
| `gnssstreamer` | 双向流 CLI（收+可选写校正） |
| `gnssserver` | TCP 服务器或单挂载点 NTRIP caster |
| `gnssntripclient` | NTRIP 客户端（RTCM/SPARTN） |
| `pyrinexconv` | 实验性 RINEX 转换 |
| `SocketServer` | 多客户端广播 / TLS |

### 1.3 应该用

- 实验室：看接收机是否吐 GGA/UBX/RTCM
- 向 caster 拉源表、订校正、把 RTCM 灌进接收机
- 把串口流转发到局域网 TCP，供 RTKLIB/其它客户端测
- 短时录二进制日志，供事后 `pyrinexconv` 或其它转换器
- 教学演示：本机 `gnssserver`（NTRIP 模式）+ `gnssntripclient`

### 1.4 不应该用

- 生产级多挂载点/高并发播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- 多流图形监控与 RINEX 专业记录 → [bnc](./bnc.md)
- 算 TEC/ROTI/PPP → 下游专用工具
- 把实验性 `pyrinexconv` 当唯一归档手段（科学归档优先官方接收机工具链 / BNC / 厂商转换）

### 1.5 与电离层工作的关系

- 本工具解决「流从哪来」；电离层产品在**落盘并转 RINEX 之后**才开始
- 典型：`gnssstreamer` 录 RAW → 转 RINEX → [gfzrnx](./gfzrnx.md) → [georinex](./georinex.md)/[pytecgg](./pytecgg.md)


## 2. 多平台安装

### 2.1 要求

- Python **≥3.10**
- 串口访问权限（Linux：用户进 `dialout` 组）
- 可选：`certifi`（macOS MQTT/TLS 常见需求）

### 2.2 Linux / macOS：venv + pip（推荐）

```bash
python3 -m venv ~/venv-gnss
source ~/venv-gnss/bin/activate
python -m pip install -U pip
python -m pip install -U pygnssutils
gnssstreamer -h | head
gnssntripclient -h | head
gnssserver -h | head
pyrinexconv -h | head
python -c "import pygnssutils; print(pygnssutils.__doc__[:60] if pygnssutils.__doc__ else 'ok')"
```

**期望：** 各命令打印帮助；无 `command not found`（若有，检查 `venv/bin` 是否在 PATH）。

### 2.3 Windows

```powershell
py -3.11 -m venv C:\venv-gnss
C:\venv-gnss\Scripts\activate
python -m pip install -U pip pygnssutils
gnssstreamer -h
# 串口名形如 COM3
```

### 2.4 conda-forge

```bash
conda install -c conda-forge pygnssutils
```

### 2.5 可选 GUI

```bash
pip install -U pygpsclient
# GUI 失败不影响 CLI
```

### 2.6 凭据环境变量（勿写入仓库）

```bash
export PYGPSCLIENT_USER='your_user'
export PYGPSCLIENT_PASSWORD='your_pass'
# TLS 自签证书路径（若需要）：
# export PYGNSSUTILS_CRTPATH="$HOME/pygnssutils.crt"
# export PYGNSSUTILS_PEMPATH="$HOME/pygnssutils.pem"
```

### 2.7 Linux 串口权限

```bash
sudo usermod -aG dialout "$USER"
# 重新登录后：
ls -l /dev/ttyACM0 /dev/ttyUSB0 2>/dev/null
```

### 2.8 systemd 常驻（gnssstreamer 摘要）

1. 按上游 `examples/gnssstreamer.service` 与 `gnssstreamer.conf` 修改路径
2. `sudo cp ... /etc/systemd/system && systemctl enable --now gnssstreamer`
3. `systemctl status gnssstreamer` 应为 active
4. 细节以仓库 examples 当前文件为准


## 3. 完整逐步命令与期望输出

### 3.1 串口探活（gnssstreamer）

```bash
source ~/venv-gnss/bin/activate
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 --verbosity 2
# Windows: --port COM3
```

**期望：** 持续打印 NMEA/UBX 解析对象；Ctrl+C 后摘要 `Messages input/output`。

### 3.2 过滤 GGA 并用 lambda 打印

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 9600 \
  --protfilter 1 --msgfilter GNGGA \
  --clioutput 4 \
  --output "lambda msg: print(f'lat={msg.lat}, lon={msg.lon}, q={msg.quality}')"
```

**期望：**

```text
lat=39.9042, lon=116.4074, q=1
lat=39.9042, lon=116.4075, q=1
```

### 3.3 录二进制日志（供事后转 RINEX）

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 \
  --format 2 --clioutput 1 \
  --msgfilter RXM-RAWX,RXM-SFRBX,NAV-PVT,GGA \
  --limit 5400 --verbosity 2 \
  --output $HOME/iono_ops/raw/ublox_raw.bin
# 建议至少 15–30 分钟（上游说明）
```

**期望：** 文件持续增大；结束时 message 计数非零。

### 3.4 读文件并十六进制+解析双看

```bash
gnssstreamer --filename $HOME/iono_ops/raw/ublox_raw.bin \
  --format 9 --verbosity 2 --quitonerror 2
```

### 3.5 拉 NTRIP 源表

```bash
gnssntripclient \
  --server rtk2go.com --port 2101 --https 0 \
  --datatype RTCM --ntripversion 2.0 \
  --ggainterval -1 \
  --reflat 39.90 --reflon 116.40 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**期望：** 提示 Closest mountpoint ...；随后打印 sourcetable 行列表。

### 3.6 订阅挂载点并接收 RTCM

```bash
gnssntripclient \
  --server rtk2go.com --port 2101 --https 0 \
  --mountpoint YOUR_MOUNT --datatype RTCM \
  --ggainterval 60 \
  --reflat 39.9042 --reflon 116.4074 --refalt 44.0 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**期望：** `Streaming RTCM data from ...`；周期性 `RTCMMessage received: 1005/1077/...`。

### 3.7 串口 + 并发 NTRIP 输入（边看定位边灌校正）

```bash
gnssstreamer --port /dev/ttyACM0 \
  --msgfilter GNGGA \
  --cliinput 1 \
  --input "http://caster.example:2101/MOUNT" \
  --rtkuser "$PYGPSCLIENT_USER" --rtkpassword "$PYGPSCLIENT_PASSWORD" \
  --rtkggaint 10 \
  --clioutput 4 \
  --output "lambda msg: print(msg.quality, msg.diffAge, msg.lat, msg.lon)"
```

**期望：** `quality` 从 1/2 升至 4/5（RTK float/fixed）——取决于基站距离与接收机能力。

### 3.8 本机轻量 NTRIP caster 演示

```bash
# 终端 A：接收机需已是基站模式并输出 RTCM
gnssserver --inport /dev/ttyACM0 --baudrate 38400 \
  --hostip 0.0.0.0 --outport 2101 \
  --ntripmode 1 --protfilter 4 --format 2 \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2

# 终端 B：
gnssntripclient --server 127.0.0.1 --port 2101 \
  --mountpoint pygnssutils --datatype RTCM \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2
```

**期望：** A 显示 client connected；B 收到 1005/1077 等。**仅限个人测试，非生产。**

### 3.9 纯 TCP 转发（非 NTRIP）

```bash
gnssserver --inport /dev/ttyACM0 --hostip 127.0.0.1 --outport 50010 \
  --ntripmode 0 --verbosity 2
# 客户端：
gnssstreamer --socket 127.0.0.1:50010
```

### 3.10 gnssstreamer 作 socket 服务 + 远端客户端

```bash
# 服务端主机：
gnssstreamer --port /dev/ttyACM0 --clioutput 3 \
  --output 0.0.0.0:50011 --format 2 --verbosity 2
# 客户端：
gnssstreamer -S 192.168.0.10:50011
```

### 3.11 配置文件启动

```bash
# 将常用参数写入 conf，然后：
gnssstreamer -C ~/gnssstreamer.conf
# 或 export GNSSSTREAMER_CONF=...
# 同类：GNSSNTRIPCLIENT_CONF / GNSSSERVER_CONF
```

### 3.12 实验性 pyrinexconv

```bash
pyrinexconv -I $HOME/iono_ops/raw/ublox_raw.bin \
  --minobs 10 \
  --marker "LOCAL,1,GEODETIC" \
  --antenna "1,UNKNOWN" \
  --receiver "1,u-blox,ZED-F9P" \
  --observer "lab" \
  --obsfilter 1C \
  --verbosity 2
```

**期望：** 生成 `*_MO.rnx` 与 `*_MN.rnx` 并报告记录数。功能仍标 experimental——科学产品请复核。

### 3.13 落盘 RTCM 供离线分析

```bash
gnssntripclient --server HOST --port 2101 --mountpoint M \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --clioutput 1 --output $HOME/iono_ops/raw/mount.rtcm \
  --verbosity 2
```

*注：*`clioutput` 取值以 `-h` 为准（文件/串口/socket 等）。


## 4. 参数与文件字段表

### 4.1 gnssstreamer 输入源

| 方式 | 参数 | 例 |
| --- | --- | --- |
| 串口 | `--port` + baud/timeout | `/dev/ttyACM0` |
| 文件 | `--filename` | `log.bin` |
| TCP | `--socket` / `-S` | `192.168.0.1:50010` |

### 4.2 过滤与格式

| 参数 | 含义 |
| --- | --- |
| `--protfilter` | 协议位掩码（NMEA/UBX/RTCM 等，见 `-h`） |
| `--msgfilter` | 消息 ID 过滤，可带周期 `NAV-PVT(10)` |
| `--format` | 1解析 2原始 4hex 8表格式 hex 16字串 32JSON；可按位或 |
| `--verbosity` | 日志详细度 |
| `--quitonerror` | 遇错行为 |
| `--limit` | 最大消息数 |

### 4.3 clioutput / cliinput

| 方向 | 码 | 含义 |
| --- | --- | --- |
| output | 0 | stdout |
| output | 1 | 文件 |
| output | 2 | 串口 |
| output | 3 | TCP 服务 |
| output | 4 | lambda |
| input | 0 | 无 |
| input | 1 | NTRIP RTCM |
| input | 2 | NTRIP SPARTN |
| input | 4 | 串口 |
| input | 5 | 二进制文件（可含 CFG） |

*具体枚举以本机 `gnssstreamer -h` 为准（版本可能增减）。*

### 4.4 gnssntripclient 关键项

| 参数 | 含义 |
| --- | --- |
| `--server/--port/--https` | caster 地址与 TLS |
| `--mountpoint` | 挂载点；空=拉源表 |
| `--datatype` | RTCM 或 SPARTN |
| `--ntripversion` | 常 2.0 |
| `--ggainterval` | GGA 上报周期；`-1` 常表示不发 |
| `--reflat/--reflon/--refalt` | 参考位置 |
| `--ntripuser/--ntrippassword` | 鉴权 |
| `--clioutput/--output` | 校正输出到文件/串口/socket |

### 4.5 gnssserver 关键项

| 参数 | 含义 |
| --- | --- |
| `--inport/--baudrate` | 上游串口 |
| `--hostip/--outport` | 监听 |
| `--ntripmode` | 0=TCP，1=NTRIP caster |
| `--protfilter/--format` | NTRIP 模式需 RTCM 二进制 |
| `--ntripuser/--ntrippassword` | 客户端登录 |

### 4.6 pyrinexconv 能力边界（experimental）

- RINEX 3.05 / 4.02（以当前 README 为准）
- UBX RXM-RAW/RAWX → OBS；RXM-SFRBX → NAV
- RTCM 星历 1019/1020/1041–1046 → NAV
- 部分 NMEA 气象 → MET


## 5. 接到电离层 / GNSS 哪一步

### 5.1 路径 C：实时入口

1. 本工具探活 / 订校正 / 录流
2. 可选 [bnc](./bnc.md) 多流对照
3. 落盘 → 转 RINEX
4. [gfzrnx](./gfzrnx.md) 规范化
5. TEC/ROTI/定位下游

### 5.2 与 data-access / 教程

- 数据源总览：[data-access](../data-access.md)
- 定位教程 [06](../tutorials/06-iono-positioning.md)：RTK 质量位可作课堂演示
- 闪烁 [05](../tutorials/05-scintillation-roti.md)：高采样录流后再算
- 生产播发边界 → [bkg-ntripcaster](./bkg-ntripcaster.md)

### 5.3 不要指望它做的事

不输出 IONEX、不估计 DCB、不跑 PPP-AR。流只是原料。


## 6. 可操作坑（≥12）

1. **venv 未激活：** `gnssstreamer: command not found`。先 `source venv/bin/activate`。
2. **串口权限：** Linux 非 dialout 用户打不开 `/dev/ttyACM0`。
3. **波特率不对：** 无数据或乱码。对照接收机配置（常见 9600/38400/115200）。
4. **VRS 不发 GGA：** 无校正流。设置合理 `--ggainterval` 与 lat/lon/alt。
5. **401/403：** 用户名密码或挂载点 ACL 错误；勿把密码写进 git。
6. **占 2101 冲突：** 与 BNC/正式 caster 抢端口。改 `--outport`。
7. **NTRIP 模式 format 非二进制：** 标准客户端解析失败。`--format 2`。
8. **基站未进 Base 模式：** `gnssserver -ntripmode 1` 无 1005/1077 可发。
9. **旧名 `gnssdump`：** 已更名为 `gnssstreamer`。更新脚本。
10. **TLS 证书：** HTTPS caster / MQTT 需正确 CRT；macOS 常见证书链问题按上游 Troubleshooting。
11. **SPARTN 解密失败：** 密钥过期或 basedate 错——联系服务商，不是电离层算法问题。
12. **pyrinexconv 当正式归档：** 仍为实验特性；发表数据用可追溯工具链复核。
13. **lambda 输出写错属性：** `msg.lat` 仅对特定 NMEA/UBX 消息存在；先不加 filter 看类型。
14. **防火墙：** 局域网客户端连不上 `hostip:port`。检查 listen 地址是否 `0.0.0.0`。
15. **长时间跑忘磁盘：** 原始日志可 GB 级。加 `--limit` 或 logrotate。
16. **把 RTCM 当 RINEX 喂 georinex：** 必败。先转换。


## 7. 同类怎么选

| 需求 | 优先 | 次选 |
| --- | --- | --- |
| 命令行探活/录流/轻量 NTRIP | **pygnssutils** | PyGPSClient GUI |
| 多流 GUI + 专业记录 | BNC | pygnssutils |
| 生产 caster | BKG NtripCaster | gnssserver（仅演示） |
| PPP-AR | PRIDE-PPPAR | — |
| RINEX 科学预处理 | GFZRNX | pyrinexconv（实验） |

### 7.1 相关链接

- GitHub：https://github.com/semuconsulting/pygnssutils
- 姊妹 GUI：https://github.com/semuconsulting/PyGPSClient
- 协议库：pyubx2 / pynmeagps / pyrtcm / pyspartn 等

### 7.2 检查清单

1. Python≥3.10，CLI `-h` 可用
2. 串口权限与波特率确认
3. 凭据在环境变量
4. 先源表后订阅
5. 录流文件非空再转换
6. 生产需求升级到 BKG caster / BNC

## 8. 场景卡片

### 8.1 只确认有没有固定解质量位

```bash
gnssstreamer --port /dev/ttyACM0 --msgfilter GNGGA --clioutput 4 \
  --output "lambda m: print(m.quality, m.numSV, m.lat, m.lon)"
```

### 8.2 把 CFG 文件灌进 F9P

```bash
gnssstreamer --port /dev/ttyACM0 --cliinput 5 --input f9pconfig.ubx --verbosity 2
```

### 8.3 JSON 抓某类 RTCM

```bash
gnssstreamer --socket 127.0.0.1:50010 --format 32 --msgfilter 1087
```

### 8.4 源表距离排序后人工挑站

```bash
gnssntripclient --server CASTER --port 2101 --https 0 \
  --reflat LAT --reflon LON --ggainterval -1 \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2 | tee sourcetable.txt
```

### 8.5 TLS pem 自签（仅实验）

```bash
openssl req -x509 -newkey rsa:4096 -keyout pygnssutils.pem \
  -out pygnssutils.pem -sha256 -days 3650 -nodes
export PYGNSSUTILS_PEMPATH=$HOME/pygnssutils.pem
```

### 8.6 与 RTKLIB 联调

1. `gnssserver` TCP 模式出端口 50010
2. RTKLIB 流输入指向该 TCP
3. 或 `gnssntripclient` 输出到串口给接收机，RTKLIB 只收 GGA

### 8.7 高采样闪烁录流

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 115200 \
  --format 2 --clioutput 1 --output scint.bin --verbosity 2
# 事后转 RINEX，保留 1 Hz 或更高，勿先抽稀
```


## 9. 协议与质量位速查

### 9.1 NMEA quality（GGA）常用语义

| quality | 含义（常见） |
| --- | --- |
| 0 | 无效 |
| 1 | SPS/单点 |
| 2 | DGPS |
| 4 | RTK fixed |
| 5 | RTK float |

### 9.2 常用 RTCM 消息（基站）

| 类型 | 内容 |
| --- | --- |
| 1005/1006 | 基站坐标 |
| 1074/1077 | GPS MSM |
| 1084/1087 | GLO MSM |
| 1094/1097 | GAL MSM |
| 1124/1127 | BDS MSM |
| 1230 | GLONASS 码偏 |

### 9.3 从流到电离层产品的门禁

- 原始日志时长 ≥ 15 min（转 NAV/OBS 实验）
- 双频 RAW 已打开（F9P：RXM-RAWX）
- 转 RINEX 后 `gfzrnx -chk` 通过
- 再进 TEC/ROTI 链


## 10. 附录：命令一页纸

```bash
pip install -U pygnssutils
gnssstreamer -h
gnssntripclient -h
gnssserver -h
pyrinexconv -h
gnssstreamer --port /dev/ttyACM0 --verbosity 2
gnssntripclient --server HOST --port 2101 --mountpoint M ...
gnssserver --inport /dev/ttyACM0 --outport 2101 --ntripmode 1 --format 2 ...
```

终注：CLI 参数若变更，**以当前上游 README 与本机 `-h` 为准**。

## 11. 端到端操作剧本

### 11.1 剧本 A：新接收机开箱探活

```bash
source ~/venv-gnss/bin/activate
ls /dev/ttyACM* /dev/ttyUSB*
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 --verbosity 2
```

**期望：** 见到 NMEA 或 UBX；若无输出，改波特率为 9600/115200 再试。  
**下一步：** 记录默认消息列表，决定是否灌 CFG。

### 11.2 剧本 B：实验室 RTK 闭环

1. 基站接收机：SURVEY_IN/FIXED，打开 RTCM MSM。  
2. 终端 A：`gnssserver ... --ntripmode 1 --outport 2101 ...`。  
3. 终端 B：流动站串口 `gnssstreamer` + `--cliinput 1` 指到本机 caster。  
4. 观察 GGA `quality` 是否到 4/5。  

**期望：** 短基线快速固定。  
**失败：** 无 1005 → 基站未进 Base；401 → 密码；无 GGA 回传 → VRS/鉴权策略。

### 11.3 剧本 C：野外只录音频原始量

```bash
mkdir -p ~/iono_ops/raw
gnssstreamer --port /dev/ttyACM0 --baudrate 115200 \
  --format 2 --clioutput 1 \
  --msgfilter RXM-RAWX,RXM-SFRBX \
  --output ~/iono_ops/raw/field_$(date +%Y%m%d_%H%M).bin \
  --verbosity 2
```

回实验室：

```bash
pyrinexconv -I ~/iono_ops/raw/field_XXXX.bin --verbosity 2 --minobs 10
gfzrnx -finp *_MO.rnx -fout clean.rnx -chk -kv -f
```

再进 TEC/ROTI 链。

### 11.4 剧本 D：只取源表做站网规划

```bash
gnssntripclient --server CASTER --port 2101 --https 0 \
  --ggainterval -1 --reflat LAT --reflon LON \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2 | tee ~/iono_ops/log/sourcetable.txt
```

**期望：** 获得挂载点名、位置、格式、费率字段；选距离近且 MSM 全的点。

### 11.5 剧本 E：TCP 供 RTKLIB 读流

```bash
gnssserver --inport /dev/ttyACM0 --hostip 0.0.0.0 --outport 50010 \
  --ntripmode 0 --verbosity 2
# RTKLIB 输入：TCP client → host:50010
```

## 12. 消息过滤配方

| 目的 | msgfilter / protfilter 思路 |
|---|---|
| 看定位 | `GNGGA` 或 `NAV-PVT` |
| 看卫星数 | `GNGSA`/`NAV-SAT` |
| 录原始观测 | `RXM-RAWX` |
| 录星历子帧 | `RXM-SFRBX` |
| 只要 RTCM | `protfilter` 限 RTCM，或 filter `1005,1077,...` |
| 降频日志 | `NAV-PVT(10)` 每 10 秒一条 |

```bash
gnssstreamer --port /dev/ttyACM0 --protfilter 2 --msgfilter NAV-PVT(5) --verbosity 1
```

## 13. 输出格式选择指南

| format 值 | 适用 |
|---|---|
| 1 | 人读解析对象 |
| 2 | 录原始、转播、NTRIP |
| 4/8 | 协议排障 |
| 16 | 简单日志 |
| 32 | 接 JSON 管道 |
| 9 (=1|8) | 解析+十六进制对照 |

## 14. 与 BNC / BKG caster 分工

| 场景 | 用 pygnssutils | 换用 |
|---|---|---|
| 5 分钟确认串口 | 是 | — |
| 课堂单挂载点演示 | `gnssserver` | — |
| 7×24 多挂载点 | 否 | bkg-ntripcaster |
| 多流图形+RINEX 记录 | 否 | BNC |
| 脚本化 CI 探活 | 是 | — |

## 15. 安全注意事项

- 默认演示密码必须更换。  
- 不要把 caster 无鉴权暴露到公网。  
- 自签证书仅实验；生产用正式证书。  
- 日志里可能回显坐标——注意脱敏。  

## 16. 故障树（简）

1. 无数据 → 线缆/供电/波特率/权限。  
2. 有 NMEA 无 RTCM → 订没订上、filter、基站。  
3. 有 RTCM 不固定 → 基线长、干扰、天线、质量模式。  
4. 转换 RINEX 空 → 录制时未开 RAWX；时长不足。  
5. TLS 失败 → 证书链 / `PYGNSSUTILS_CRTPATH`。  

## 17. 移交与复现信息模板

```text
date:
pygnssutils_version:
python:
port/baud:
caster/mount:
commands:
raw_file_sha256:
notes:
```

```bash
python -m pip show pygnssutils | sed -n '1,5p'
```

## 18. 接到本仓库其它页的检查表

- [ ] 流已落盘  
- [ ] 已转 RINEX 或确认下游直接吃 UBX（少见）  
- [ ] [gfzrnx](./gfzrnx.md) 完成 `-chk`  
- [ ] TEC：[pytecgg](./pytecgg.md) / 教程 [02](../tutorials/02-gnss-dualfreq-tec.md)  
- [ ] ROTI：保留高采样  
- [ ] 定位对照：[rtklib](./rtklib.md) / [pride-pppar](./pride-pppar.md)  

终注：CLI 名称与参数若上游变更，**以当前上游 README 与本机 `-h` 为准**。