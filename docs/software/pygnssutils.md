# pygnssutils · GNSS 流 / NTRIP CLI 操作手册

目录：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/pygnssutils> · 文档 <https://www.semuconsulting.com/pygnssutils> · PyPI `pygnssutils` · BSD-3-Clause · Python ≥3.10

> 岗位：串口/TCP/NTRIP **探活、录流、轻量播发**。主 CLI（以本机 `-h` 为准）：`gnssstreamer`、`gnssntripclient`、`gnssserver`、`pyrinexconv`（实验性）。口令禁止进 git。本页对照当前包帮助；旗标名随小版本可能微调。

## 1. 用途与边界

**做：** 同一流解析 NMEA/UBX/SBF/RTCM3/SPARTN 等；订 NTRIP 改正；TCP 转发；短时录二进制；实验性 RAW→RINEX。

**不做：** 生产多挂载点高并发 → [bkg-ntripcaster](./bkg-ntripcaster.md)；多流 GUI 录盘主力 → [bnc](./bnc.md)；TEC/ROTI/PPP → 落盘转 RINEX 后走 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)/[oasis-roti](./oasis-roti.md)/[rtklib](./rtklib.md)。

一句话：解决「流从哪来」；电离层产品在 **落盘并转 RINEX 之后**。

| 组件 | 角色 |
| --- | --- |
| `gnssstreamer` | 双向流 CLI（收 + 可选灌改正） |
| `gnssntripclient` | NTRIP 客户端（源表 / 订流） |
| `gnssserver` | TCP 服务或单挂载点 NTRIP caster |
| `pyrinexconv` | 实验性二进制→RINEX |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip pygnssutils
gnssstreamer -h | head
gnssntripclient -h | head
gnssserver -h | head
pyrinexconv -h | head
# conda: conda install -c conda-forge pygnssutils
```

Windows：`py -3.11 -m venv ...`；串口形如 `COM3`。Linux 串口：用户进 `dialout` 组后重新登录。

```bash
export PYGPSCLIENT_USER='your_user'
export PYGPSCLIENT_PASSWORD='your_pass'
# 勿把口令写入仓库；conf 文件 chmod 600
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `command not found` | 未激活 venv | `source ~/venv-gnss/bin/activate` |
| 打不开 `/dev/ttyACM0` | 无串口权限 | `sudo usermod -aG dialout $USER` 后重登 |
| 旧名 `gnssdump` | 已更名 | 用 `gnssstreamer` |

## 3. 端到端（真实旗标）

### 3.1 串口探活

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 --verbosity 2
# Windows: --port COM3
```

**期望：** 持续打印解析对象；Ctrl+C 后有消息计数摘要。

### 3.2 过滤 GGA + lambda 输出

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 9600 \
  --protfilter 1 --msgfilter GNGGA \
  --clioutput 4 \
  --output "lambda msg: print(f'lat={msg.lat}, lon={msg.lon}, q={msg.quality}')"
```

| 旗标 | 作用 |
| --- | --- |
| `--port` / `--filename` / `--socket` | 串口 / 文件 / `host:port` 三选一 |
| `--baudrate` / `--timeout` | 串口参数 |
| `--protfilter` | 位掩码：1 NMEA，2 UBX，4 RTCM3…（见 `-h`） |
| `--msgfilter` | 消息 ID，可加周期 `NAV-PVT(10)` |
| `--format` | 1 解析 / 2 原始 / 4 hex / 8 表格式 hex / 16 字串 / 32 JSON；可 OR |
| `--clioutput` | 0 终端 / 1 二进制文件 / 2 串口 / 3 TCP 服务 / 4 表达式 / 5 文本文件 |
| `--output` | 与 clioutput 匹配的路径/`host:port`/lambda |
| `--cliinput` | 0 无 / 1 NTRIP RTCM / 2 NTRIP SPARTN / 4 串口 / 5 二进制文件 |
| `--input` | NTRIP URL 或文件等 |
| `--limit` / `--verbosity` / `--quitonerror` | 条数、日志、错误策略 |

### 3.3 录二进制（事后转 RINEX）

```bash
mkdir -p ~/iono_ops/raw
gnssstreamer --port /dev/ttyACM0 --baudrate 38400 \
  --format 2 --clioutput 1 \
  --msgfilter RXM-RAWX,RXM-SFRBX,NAV-PVT,GGA \
  --limit 5400 --verbosity 2 \
  --output ~/iono_ops/raw/ublox_raw.bin
# 建议 ≥15–30 min
ls -l ~/iono_ops/raw/ublox_raw.bin
```

### 3.4 拉 NTRIP 源表

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

**期望：** 提示最近挂载点；打印源表行。空源表 → DNS/防火墙/账号。

| 旗标 | 作用 |
| --- | --- |
| `--server` / `--port` / `--https` | caster 与 TLS |
| `--mountpoint` | 空=源表；非空=订流 |
| `--datatype` | RTCM / SPARTN |
| `--ntripversion` | 常 2.0 |
| `--ggainterval` | GGA 周期；`-1` 常表示不发 |
| `--reflat` / `--reflon` / `--refalt` | 参考位置（VRS 常需） |
| `--ntripuser` / `--ntrippassword` | 鉴权 |
| `--clioutput` / `--output` | 改正写出文件/串口/socket |

### 3.5 订挂载点

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

**期望：** `Streaming RTCM...`；周期性 `1005/1077/...`。

### 3.6 串口 + 并发 NTRIP 灌改正

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

**期望：** `quality` 可能升至 4/5（视基线与接收机）。

### 3.7 本机轻量 NTRIP caster（个人测试）

```bash
# 终端 A：接收机须已是基站并吐 RTCM
gnssserver --inport /dev/ttyACM0 --baudrate 38400 \
  --hostip 0.0.0.0 --outport 2101 \
  --ntripmode 1 --protfilter 4 --format 2 \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2

# 终端 B
gnssntripclient --server 127.0.0.1 --port 2101 \
  --mountpoint pygnssutils --datatype RTCM \
  --ntripuser labuser --ntrippassword 'change-me-now' \
  --verbosity 2
```

| `gnssserver` 旗标 | 作用 |
| --- | --- |
| `--inport` / `--baudrate` | 上游串口 |
| `--hostip` / `--outport` | 监听 |
| `--ntripmode` | 0=TCP；1=NTRIP caster |
| `--protfilter` / `--format` | NTRIP 模式需 RTCM **二进制**（format 2） |
| `--ntripuser` / `--ntrippassword` | 客户端登录 |

**仅限个人测试。** 正式多用户 → [bkg-ntripcaster](./bkg-ntripcaster.md)。

### 3.8 实验性 `pyrinexconv`

```bash
pyrinexconv -I ~/iono_ops/raw/ublox_raw.bin \
  --minobs 10 \
  --marker "LOCAL,1,GEODETIC" \
  --antenna "1,UNKNOWN" \
  --receiver "1,u-blox,ZED-F9P" \
  --observer "lab" \
  --obsfilter 1C \
  --verbosity 2
```

**期望：** 生成 OBS/NAV 类 RINEX 并报告记录数。仍标 experimental——发表数据请复核。

## 4. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| 串口 / 文件 / TCP | streamer 三源 |
| NTRIP caster | 源表或挂载点 |
| 口令 | 环境变量或 conf（勿进 git） |

| 输出 | 下游 |
| --- | --- |
| 解析对象 / 二进制日志 | 探活；事后转 RINEX |
| RTCM 文件 | 回放 |
| TCP/NTRIP 服务 | [rtklib](./rtklib.md) 等客户端 |
| RINEX（实验） | [gfzrnx](./gfzrnx.md) → [anubis](./anubis.md) → TEC/ROTI |

## 5. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 路径 C 实时入口 | §3 | 落盘 → A/B |
| 多流 GUI 录盘 | — | [bnc](./bnc.md) |
| 正式播发 | — | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 定位演示 | §3.6–3.7 | [rtklib](./rtklib.md) · [06](../tutorials/06-iono-positioning.md) |

## 6. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | `command not found` | 未激活 venv | `source .../activate` |
| 2 | 串口 Permission denied | 非 dialout | 加组并重登 |
| 3 | 无数据/乱码 | 波特率错 | 试 9600/38400/115200 |
| 4 | VRS 无流 | 未发 GGA | 设 `--ggainterval` 与 lat/lon/alt |
| 5 | 401/403 | 口令/ACL | 改密；查并发限额；勿贴聊天 |
| 6 | 2101 冲突 | 与 BNC/正式 caster 抢端口 | 改 `--outport` |
| 7 | NTRIP 客户端解不出 | format 非二进制 | `gnssserver --format 2` |
| 8 | caster 无 1005/1077 | 接收机未进 Base | 先配基站模式 |
| 9 | 脚本仍写 `gnssdump` | 旧名 | 改 `gnssstreamer` |
| 10 | TLS 失败 | 证书/时间 | NTP；查 CRT 路径 |
| 11 | SPARTN 解密失败 | 密钥/basedate | 联系服务商 |
| 12 | `pyrinexconv` 当正式归档 | 仍实验性 | 用可追溯工具链复核 |
| 13 | lambda 属性错 | 消息类型无该字段 | 先不过滤看类型 |
| 14 | 局域网连不上 | 监听地址/防火墙 | `0.0.0.0`；放行端口 |
| 15 | 磁盘写满 | 长时 1 Hz 日志 | `--limit`；logrotate |
| 16 | 把 RTCM 当 RINEX 喂 georinex | 格式错 | 先转换 |
| 17 | 口令进 git | conf 误提交 | `chmod 600`；gitignore；轮换 |
| 18 | 当 TEC 引擎 | 链选错 | 落盘后 [pytecgg](./pytecgg.md) |

## 7. 选型

| 需求 | 选 |
| --- | --- |
| CLI 探活/录流/轻量 NTRIP | **pygnssutils** |
| 多流 GUI 录盘 | BNC |
| 正式多用户播发 | BKG NtripCaster |
| 事后定位 | RTKLIB / PRIDE-PPPAR |

## 8. 相关

[bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · [README](./README.md)
