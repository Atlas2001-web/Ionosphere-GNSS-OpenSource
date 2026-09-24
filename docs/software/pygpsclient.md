# PyGPSClient · GNSS 协议桌面 GUI 操作手册

目录：[`PROJECTS.json` → `PyGPSClient`](../../PROJECTS.json) · 上游 <https://github.com/semuconsulting/PyGPSClient> · 文档 <https://www.semuconsulting.com/pygpsclient> · PyPI **`PyGPSClient` 1.7.6** · tip **`69b84cf`** · BSD-3-Clause · Python ≥3.10 + **tkinter ≥8.6** · 本机：`pip install` → 捆 CLI `gnssstreamer`/`pyrinexconv`；仓内 `tests/pygpsdata_rinextest.log` → RINEX O/N；**无 tkinter / 无显示，GUI 未起窗**（2026-09-24 EDT）

> 岗位：串口/TCP/文件上的 **NMEA·UBX·RTCM·SPARTN** 监视、接收机配置、NTRIP 客户/简易基站。冲突时：**上游 README / `pygpsclient -h` / 捆 `gnssstreamer -h` > 本文**。纯 CLI 自动化 → [pygnssutils](./pygnssutils.md)；多流运维 → [bnc](./bnc.md)。

## 1. 用途与边界

**做：**

- GUI：星空图、C/No、串口/套接字/二进制回放、UBX/NMEA/TTY 配置、NTRIP 客户、简易 NTRIP caster / socket server
- 二进制 datalog →（实验）**RINEX**（GUI「RINEX Conversion」或 CLI `pyrinexconv`）
- 安装时拉齐 [pygnssutils](./pygnssutils.md) CLI：`gnssstreamer` / `gnssntripclient` / `gnssserver` / `pyrinexconv`

**不做：**

- **不是** 精密 PPP/RTK 解算引擎 → 接收机固件或 [rtklib](./rtklib.md)/[pride-pppar](./pride-pppar.md)
- **不是** 生产级多用户 Caster → [bkg-ntripcaster](./bkg-ntripcaster.md)
- **不是** 手机 GnssLogger→RINEX → [android_rinex](./android_rinex.md)（本文 RINEX 面向 **u-blox RAW/RTCM** 等）
- **不是** TEC/ROTI 产品 → 落盘 RINEX 后走 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)/[oasis-roti](./oasis-roti.md)

一句话：PyGPSClient = **板卡联调 GUI**；电离层产品在 **录流→RINEX 之后**。

| 组件 | 角色 |
| --- | --- |
| `pygpsclient` | tkinter GUI 入口 |
| `gnssstreamer` | 无头自动化收/录/灌改正（与 GUI 同栈） |
| `pyrinexconv` | 实验性二进制→RINEX 3.05/4.02（Beta） |
| `gnssntripclient` / `gnssserver` | NTRIP 客户 / 单挂载点服务 |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
python -m pip install -U pip
python -m pip install --upgrade PyGPSClient
python -c "import importlib.metadata as m; print(m.version('PyGPSClient'))"
# 期望：1.7.6（或以本机为准）
gnssstreamer -V          # 捆 pygnssutils，本机 1.2.7
pyrinexconv -V           # 期望：pyrinexconv 0.2.0 Beta
# Linux 缺 tk：
#   sudo apt-get install -y python3-tk
# 串口权限：
#   sudo usermod -aG dialout $USER   # 然后重登
pygpsclient              # 有显示时起 GUI
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `No module named 'tkinter'` | 未装系统 Tk | `sudo apt-get install -y python3-tk` |
| `pygpsclient: not found` | venv 未激活 | `source ~/venv-gnss/bin/activate` |
| `[Errno 13] … /dev/ttyACM0` | 无 dialout | `usermod -aG dialout $USER` 后重登 |
| Wayland 窗体裁切 | 缩放/transient | 配置 `resizeable_dialog_b`/`transient_dialog_b`（见上游） |

本机（容器）：`pip` 成功得 **1.7.6**；`import tkinter` 失败 → **GUI 未跑**；CLI 通路已验证。

## 3. 端到端（本机真跑 CLI；GUI 标步骤）

### 3.1 文件回放探活（`gnssstreamer`，无硬件）

```bash
mkdir -p ~/iono_ops/pygps_e2e
python - <<'PY'
from pynmeagps import NMEAMessage, GET
lines=[]
for t,lat,lon,q in [
 ("12:35:19",39.9041871667,116.3907426667,1),
 ("12:35:20",39.9041873333,116.3907428333,1),
 ("12:35:21",39.9041875,116.390743,2),
]:
    m=NMEAMessage("GN","GGA",GET,time=t,lat=lat,NS="N",lon=lon,EW="E",
                  quality=q,numSV=12,HDOP=0.9,alt=44.0,altUnit="M",sep=-18.0,sepUnit="M")
    s=m.serialize().decode()
    lines.append(s if s.startswith("$") else "$"+s)
open(__import__("os").path.expanduser("~/iono_ops/pygps_e2e/demo.nmea"),"w").write("\n".join(lines)+"\n")
PY
# 路径按本机家目录改写；或用绝对路径
gnssstreamer --filename ~/iono_ops/pygps_e2e/demo.nmea --verbosity 2 --limit 10
```

**本机 stdout（节选）：**

```text
Messages input:    {'GNGGA': 3}
Messages filtered: {}
Messages output:   {'GNGGA': 3}
Streaming terminated, 3 messages processed with 0 errors.
<NMEA(GNGGA, time=12:35:19, lat=39.9041871667, ... quality=1, ...)>
```

串口（有 F9P 等时）：

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 115200 --verbosity 2
# GUI：选端口 → Connect；Protocols Shown 勾 NMEA/UBX/RTCM
```

### 3.2 二进制 datalog → RINEX（`pyrinexconv`）

上游测试日志（约 10 MB，含 RAW/X + 星历类消息）：

```bash
git clone --depth 1 https://github.com/semuconsulting/PyGPSClient.git ~/iono_ops/PyGPSClient
pyrinexconv -I ~/iono_ops/PyGPSClient/tests/pygpsdata_rinextest.log \
  -T O,N -R 3.05 --verbosity 2
# 输出写在输入文件同目录，长名 *.rnx
```

**本机（pyrinexconv 0.2.0 Beta）：**

```text
Processing successful. Output file names and number of records processed:
Observation: .../pygpsdata_R_202605081420_28M_01S_MO.rnx - 1,677
Navigation:  .../pygpsdata_R_202605081400_02H_MN.rnx - 55,037
```

头摘要（OBS）：

```text
     3.05           O: OBSERVATION      M: MIXED            RINEX VERSION / TYPE
PYRINEXCONV 0.2.0 …
G    8 C1C L1C D1C S1C C2X L2X D2X S2X                      SYS / # / OBS TYPES
E    8 C1X L1X D1X S1X C7X L7X D7X S7X                      SYS / # / OBS TYPES
  2026     5     8    14    20    6.0050000     GPS         TIME OF FIRST OBS
  2026     5     8    14    48    2.0050000     GPS         TIME OF LAST OBS
```

下游探活（大文件建议限时窗；本机 `time` 维可用）：

```bash
python -W ignore - <<'PY'
import georinex as gr
p = __import__("os").path.expanduser(
  "~/iono_ops/PyGPSClient/tests/pygpsdata_R_202605081420_28M_01S_MO.rnx")
obs = gr.load(p, tlim=("2026-05-08T14:20:00","2026-05-08T14:25:00"))
print(gr.__version__, dict(obs.dims), list(obs.data_vars)[:8])
# 期望：历元>0；含双频列（机型相关）
PY
```

**本机 georinex 1.16.2（5 min 窗）：** `time=1, sv=20`，含 `C1X/L1X`…（完整 1677 历元可再放宽 `tlim`）。全文加载若遇异常字符/内存，先 `grep -c '^>' file.rnx` 对账（本机 **1677**）。

GUI 等价：Menu → Options → **RINEX Conversion** → 选 `.log` → O/N → Start。建议录 **≥15–30 min** RAW。

### 3.3 NTRIP 客户（GUI 步骤；口令勿进 git）

1. 天线图标 / Menu → Options → **NTRIP Configuration**
2. 填 caster host/port；TLS 按服务商勾选
3. 用户/口令用环境变量习惯（与 pygnssutils 一致），**不要**写进仓库 json 后提交
4. 空 mountpoint → Connect 拉源表 → 选近站；需要时开 GGA 周期（10/60 s）
5. 横幅 **corr:** 变 ✓ 表示改正龄期在刷新；控制台刷屏可关掉 Protocols Shown 里的 RTCM 显示（后台仍灌）

CLI 等价见 [pygnssutils](./pygnssutils.md) `gnssntripclient` / `gnssstreamer --cliinput 1`。

### 3.4 长时间无人值守录流

GUI 不适合 12 h+ 挂机。用捆 CLI：

```bash
gnssstreamer --port /dev/ttyACM0 --baudrate 115200 --timeout 3 \
  --format 2 --clioutput 1 --output ~/iono_ops/raw/ublox.bin \
  --verbosity 2
# 事后：pyrinexconv -I ~/iono_ops/raw/ublox.bin -T O,N
```

## 4. I/O 与关键参数

| 侧 | 形式 | 说明 |
| --- | --- | --- |
| 入 | 串口 / TCP·UDP / `*.log`·`*.ubx` | GUI Connect 三选一 |
| 入 | NTRIP RTCM3/SPARTN | 灌进接收机口 |
| 出 | 二进制 datalog / GPX / sqlite | Options 面板开关 |
| 出 | `*_MO.rnx` / `*_MN.rnx` | `pyrinexconv` / GUI 转换 |
| 配置 | `~/pygpsclient.json` 或 `-C` | 保存/加载；升级后建议重存 |

| CLI（`pyrinexconv`） | 作用 |
| --- | --- |
| `-I` | 输入二进制日志 |
| `-R {3.05,4.02}` | RINEX 版本 |
| `-T O,N,M` | 观测/导航/气象 |
| `-G` / `-O` / `-S` | 系统 / 观测码 / 卫星过滤 |
| `-os/-ns` | 观测源 u-blox；导航 u-blox\|rtcm3 |

## 5. 接到哪步

```text
板卡 UART/USB
  → PyGPSClient GUI 联调 / 配 UBX MSG
  →（脚本）gnssstreamer 录 bin
  → pyrinexconv → RINEX
  → georinex 探活 → pytecgg / oasis-roti / rtklib
手机 Logger CSV → android_rinex（不要走本文 RINEX 对话框）
多流 7×24 → bnc；多用户播发 → bkg-ntripcaster
```

路径 C：[pygnssutils](./pygnssutils.md) ↔ **本文 GUI** ↔ [bnc](./bnc.md)。

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `No module named 'tkinter'` | 缺系统 Tk | `sudo apt-get install -y python3-tk` |
| 2 | 校验和 WARNING 刷屏 | 波特率/带宽不够 | 先升到 115200+；USB-UART 勿硬上 460800 |
| 3 | `pyrinexconv` 观测很少 | 日志太短/无 RAW | 录 ≥15–30 min；确认 RXM-RAWX 已开 |
| 4 | NTRIP 已连但无固定 | 基线远/天线差/无 GGA | 换近挂载点；开 GGA；查 corr 龄期 |
| 5 | 把 GUI 当 PPP 引擎 | 仅监视+灌流 | 解算用固件或 [rtklib](./rtklib.md) |
| 6 | 手机 GnssLogger 丢进 RINEX 对话框 | 源不是 u-blox bin | 改 [android_rinex](./android_rinex.md) |
| 7 | 口令进了 `pygpsclient.json` 且提交 | 配置含明文 | 撤密；改环境变量；`chmod 600` |
| 8 | 长录 GUI 卡死 | 刷新过密/日志过大 | 改用 `gnssstreamer`；增大 `guiupdateinterval_f` |
| 9 | georinex 全文件 `time=0` | 大文件/方言边缘 | 加 `tlim=`；或 `grep -c '^>'` 对账后再分段读 |
| 10 | TTY 模式丢协议 | TTY 与其它协议互斥 | 停流后再切；配完切回 UBX/NMEA |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| F9P 等板卡 GUI 联调 / NTRIP | **PyGPSClient（本文）** |
| 同栈无头脚本 / CI | [pygnssutils](./pygnssutils.md) |
| 多流 GUI 录盘 / REQC | [bnc](./bnc.md) |
| 多用户 Caster | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 手机 Logger → RINEX | [android_rinex](./android_rinex.md) |
| RINEX → xarray | [georinex](./georinex.md) |

相关：上游 README · [INSTALLATION.md](https://github.com/semuconsulting/PyGPSClient/blob/main/INSTALLATION.md) · [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [android_rinex](./android_rinex.md) · [georinex](./georinex.md) · [gps-measurement-tools](./gps-measurement-tools.md) · 教程 [06](../tutorials/06-iono-positioning.md)
