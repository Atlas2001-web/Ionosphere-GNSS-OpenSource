# piksi_tools · Swift/Piksi 现场 SBP 工具操作手册

目录：[`PROJECTS.json` → `piksi_tools`](../../PROJECTS.json) · 上游 <https://github.com/swift-nav/piksi_tools> · **URL 已核** · PyPI **`piksi-tools` / `piksi_tools` 4.0.0**（元数据名 `piksi-tools`）· tip **`02f1532`**（2023-09-25）· 仓内脚本自报 **`v3.1.1.dev14+g27d57f0`** · 许可 **LGPL-3.0**（`LICENSE`；`setup.cfg` 写 BSD 为陈旧元数据）· 本机：`pip install --no-deps` + `sbp` 6.5.2（Py3.13 上 `libsettings` 编不过）· 无 console_scripts · **无 Swift 接收机硬件** · 2026-09-24 05:28 EDT

> 岗位：配 [libsbp](./libsbp.md) 做 **Piksi/Swift 现场**：串口日志、离线 SBP→JSON/CSV、配置读写、刷机、机内文件。冲突时：**本机 `serial_link.py -h` / 上游 README > 本文**。协议编解码细节 → [libsbp](./libsbp.md)；ROS 2 → 列表 `swiftnav-ros2`（尚未短硬）；数值例程 → 列表 `libswiftnav`。

## 1. 用途与边界

**做：**

- CLI（包内 `.py`，无 entry point）：`serial_link` / `sbp_msg_2_csv` / `sbpjson_expand` / `settings` / `fileio` / `bootload_v3`
- 离线：`--file` 重放 `.bin`/SBP；`-l` 写 JSON 日志；`-t MsgPosLLH` 抽 CSV
- 在线（需硬件）：串口/TCP/FTDI；配置 `settings`；刷机 `bootload_v3`；机内 `fileio`

**不做：**

- **不是** 通用多品牌 RTK/PPP → [rtklib](./rtklib.md) / [ginan](./ginan.md)
- **不是** SBP 协议库本体 → [libsbp](./libsbp.md)（`pip install sbp` / `sbp2json`）
- **不是** Septentrio/u-blox/RTCM 工具 → [pysbf2](./pysbf2.md) / [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md)
- **无 Rx**：**禁止臆造** 串口 NED/`settings all` 成功 stdout

一句话：piksi_tools = **Swift 现场运维壳**；协议真相在 libsbp。

| 符号 | 含义 |
| --- | --- |
| SBP | Swift Binary Protocol；preamble=`0x55` |
| `serial_link` | 串口/文件客户端；可 `-l` JSON 落盘 |
| `sbp_msg_2_csv` | 按消息类/号抽 CSV（`-t`/`-i`，`-f bin\|json`） |
| `libsettings` | 声明依赖；Py3.13 常编不过——本机用 `--no-deps` 绕过 |
| `MsgPosLLH` | `msg_type=522` |

## 2. 安装

```bash
python3 -m venv ~/venv-gnss && source ~/venv-gnss/bin/activate
# 理想路径（Py≤3.11 且能编 libsettings）：
python -m pip install -U pip 'piksi_tools==4.0.0'
# 本机 Py3.13：libsettings 缺 libsbp C 头失败 → 拆装
python -m pip install 'sbp==6.5.2' numpy pyserial six monotonic PyYAML configparser future
python -m pip install --no-deps 'piksi_tools==4.0.0'
python -c "import importlib.metadata as m; print(m.version('piksi_tools'), m.version('sbp'))"
# 期望：4.0.0 6.5.2
# 入口：无 bin/serial_link；用模块或包路径
python -m piksi_tools.serial_link -h | head -3
PKG=$(python -c 'import piksi_tools,os; print(os.path.dirname(piksi_tools.__file__))')
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `Failed building wheel for libsettings` | 需 `libsbp/sbp.h`；Py3.13 易挂 | `--no-deps` + 手装 `sbp` 等；或换 Py3.10/3.11 |
| `No module named 'future'` | `fileio`/`bootload_v3` 未声明依赖 | `pip install future` |
| `command not found: serial_link` | **无** console_scripts | `python -m piksi_tools.serial_link` 或 `$PKG/serial_link.py` |
| 与固件字段对不上 | SBP/固件漂移 | 对齐固件与 `sbp` 版本；见 [libsbp](./libsbp.md) |

## 3. 端到端（本机真跑；无 Rx）

样例：`PT=/path/to/piksi_tools`（clone tip `02f1532`）；可选对照 `LIB=.../libsbp`。

### 3.1 CLI 帮助（节选本机）

```bash
python -m piksi_tools.serial_link -h
```

**本机（头）：**

```text
usage: serial_link.py [-h] [-p PORT] [-b BAUD] [--rtscts] [-t] [-f] [--file]
                      [--json] [--playback] [-v] [-r] [-l] [-o LOG_DIRNAME]
...
Swift Navigation SBP Client version v3.1.1.dev14+g27d57f0.d20230510
```

其它本机已核：`settings.py -h`（子命令 `save|reset|read|all|write|…`）；`fileio.py -h`（`-w/-r/-l/-d`）；`bootload_v3.py -h`；`sbp_msg_2_csv.py -h`；`sbpjson_expand.py -h`。

### 3.2 无硬件门禁（默认口）

```bash
python -m piksi_tools.serial_link -p /dev/ttyUSB0 --timeout 1
python $PKG/settings.py all
```

**本机：**

```text
Error opening serial device '/dev/ttyUSB0':
[Errno 2] could not open port /dev/ttyUSB0: [Errno 2] No such file or directory: '/dev/ttyUSB0'

The following serial devices were detected:

	/dev/ttyS0 (n/a)
```

（exit 0——**勿当联机成功**。）

### 3.3 `sbp_msg_2_csv`：仓内大日志 → PosLLH CSV

```bash
python $PKG/sbp_msg_2_csv.py -t MsgPosLLH -f bin -o large \
  $PT/tests/data/20170513-180207.1.1.26.bin
wc -l MsgPosLLH_large.csv
awk -F, 'NR>1 && $3+0>0 {print; exit}' MsgPosLLH_large.csv
awk -F, 'NR>1 && $4+0!=0 {last=$0} END{print last}' MsgPosLLH_large.csv
```

**本机：**

```text
Extracing class <class 'sbp.navigation.MsgPosLLH'> with msg_id 522 to csv file MsgPosLLH_large.csv
…  # 伴随: SBP dispatch error: 'NoneType' object is not callable（framer 警告，仍出 CSV）
4687 MsgPosLLH_large.csv   # 1 头 + 4686 行
12027,34,3799400,37.77347765314567,-122.41791667510296,-7.947109745228893,3642,3914,6,1
12027,34,4226900,37.77346617512907,-122.41787679782918,-3.462091523140768,1004,2048,8,1
```

说明：`tow=0` 的空解约数百行属日志内容；**nonzero tow ≈4276**。同文件 `MsgBaselineNED` 4686 行但 **n/e/d 全 0**（无基线解）。

### 3.4 对照 [libsbp](./libsbp.md) `roundtrip.sbp`

```bash
python $PKG/sbp_msg_2_csv.py -t MsgPosLLH -f bin -o rt $LIB/test_data/roundtrip.sbp
head -2 MsgPosLLH_rt.csv
```

**本机：**

```text
467 MsgPosLLH_rt.csv
sender,length,tow,lat,lon,height,h_accuracy,v_accuracy,n_sats,flags
22963,34,271497800,37.831235254413826,-122.28650677009367,-17.215181577283488,513,1115,15,6
```

与 libsbp 手册 `sbp2json --include 522` 一致（≈37.8312°N 122.2865°W，`n_sats=15`）。

### 3.5 `serial_link --file`：重放 + JSON 日志

```bash
python -m piksi_tools.serial_link --file \
  -p $PT/tests/data/20170513-180207.1.1.26.bin \
  --timeout 5 -l -o /tmp/piksi-out --logfilename large_replay --skip-metadata
# stderr 可出现：
# INFO Position saved [37.7734, -122.4179, 14.6]
wc -l /tmp/piksi-out/large_replay
head -1 /tmp/piksi-out/large_replay
```

**本机：** JSON 行 **61599**；`--skip-metadata` 时一行一例：

```text
{"preamble":85,"msg_type":522,"sender":12027,"length":34,"payload":"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==","crc":37822}
```

（前段 payload 全 0 = 空解帧；后段有真实 LLH，与 §3.3 CSV 一致。）Top `msg_type` 含 522/521/526/… 各 **4686**。

小文件 `tests/data/piksi.bin`（72 KB）：夹杂明文 log，`MsgPosLLH` CSV 可为空；伴生 `crc mismatch` / `Unhandled byte`——属夹具，非必坏工具。`device_details.yaml` 记固件 `v0.17-…` / `hw_revision: piksi_2.3.1`。

### 3.6 串口/配置/刷机（需硬件；本机未跑）

```bash
# 默认常找 /dev/ttyUSB0；无设备见 §3.2——勿当已测成功 stdout
python -m piksi_tools.serial_link -p /dev/ttyUSB0 -b 115200 -l -o ./logs
python $PKG/settings.py -p /dev/ttyUSB0 all
python $PKG/fileio.py -p /dev/ttyUSB0 -l /
python $PKG/bootload_v3.py -p /dev/ttyUSB0 firmware.image_set.bin
```

## 4. 接到哪步

```text
Swift Rx UART/TCP 或 .bin/.sbp 日志
  → piksi_tools serial_link / sbp_msg_2_csv（本文）
  → 精细编解码 / sbp2json → [libsbp](./libsbp.md)
  →（ROS2）swiftnav-ros2（列表；尚未短硬）
  → 落盘观测/位置 → georinex / rtklib / 电离层链
```

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `pip install piksi_tools` 编 `libsettings` 失败 | 缺 libsbp C 头 / 新 Python | `--no-deps`+手装；或 Py3.10/3.11 |
| 2 | `serial_link: command not found` | 无 console_scripts | `python -m piksi_tools.serial_link` |
| 3 | `No module named 'future'` | fileio 隐式依赖 | `pip install future` |
| 4 | 默认口报错仍 exit 0 | 无 `/dev/ttyUSB0` | 看 stderr；无 Rx 用 `--file` |
| 5 | `MsgPosLLH` 大量 0 | 日志含未收敛历元 | `awk '$3>0'` 滤 tow；或换 roundtrip.sbp |
| 6 | `BaselineNED` 全 0 | 无基线解 | 看 PosLLH；有基线再滤 n\|e\|d |
| 7 | `SBP dispatch error: 'NoneType'…` | 旧帧/未知类型 vs 新 `sbp` | 警告可忽略；钉匹配的 `sbp` 版本 |
| 8 | `piksi.bin` CRC/Unhandled byte | 夹杂非 SBP 文本 | 换 `20170513-…bin` 或 libsbp 样例 |
| 9 | PyPI 4.0.0 vs 脚本 v3.1.1.dev… | wheel 内嵌 scm 串 | 以 `importlib.metadata.version('piksi_tools')`=**4.0.0** 为准 |
| 10 | `setup.cfg` 写 BSD、`LICENSE` LGPL | 元数据过时 | 以 **LGPL-3.0**/`LICENSE` 为准（同 PROJECTS） |
| 11 | 当多品牌 RTK 套件 | 仅 Swift/SBP | 其它机型走对应驱动/协议库 |
| 12 | 只要协议不要现场壳 | 用错层 | 只用 [libsbp](./libsbp.md) |

## 6. 选型

| 你要… | 用 |
| --- | --- |
| Swift 现场日志/配置/刷机 | **本文 piksi_tools** |
| SBP 编解码 / `sbp2json` | [libsbp](./libsbp.md) |
| Swift → ROS 2 | 列表 **`swiftnav-ros2`**（高优先缺篇） |
| Septentrio ROS | [septentrio-gnss-driver](./septentrio-gnss-driver.md) |
| u-blox / RTCM3 | [pyubx2](./pyubx2.md) / [pyrtcm](./pyrtcm.md) |
| 定位/PPP | [rtklib](./rtklib.md) / [ginan](./ginan.md) |

## 7. 相关

[libsbp](./libsbp.md) · [septentrio-gnss-driver](./septentrio-gnss-driver.md) · [pyubx2](./pyubx2.md) · [pyrtcm](./pyrtcm.md) · [pysbf2](./pysbf2.md) · [pygnssutils](./pygnssutils.md) · [rtkbase](./rtkbase.md) · [README](./README.md)

- 上游：<https://github.com/swift-nav/piksi_tools>
- PyPI：<https://pypi.org/project/piksi-tools/>
- 用户指南（厂商）：Swift Support「Piksi Tools User Guide」
- 许可：LGPL-3.0（仓内 `LICENSE`）
