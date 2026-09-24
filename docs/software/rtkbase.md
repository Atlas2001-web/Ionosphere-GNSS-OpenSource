# RTKBase · Stefal 树莓派 GNSS 基站 + Web UI 操作手册

目录：[`PROJECTS.json` → `rtkbase`](../../PROJECTS.json) · 上游 <https://github.com/Stefal/rtkbase> · 许可 **AGPL-3.0** · 发布 **v2.7.0** · tip **`2ce7ce0`** · 捆 **RTKLIB-EX v2.5.0**（`str2str`/`convbin`）· 本机验证：`settings.conf.default` 解析；`RTKBaseConfigManager` 合并默认/用户配置；`install.sh --help`；**无 Pi / 无 GNSS 硬件 → 未启 systemd / 未订 NTRIP / 未开 Web** · 2026-09-24 05:16 EDT · **质检复跑通过**（ConfigManager+install help；12 unit；无 Pi/GNSS 未启服务；tip `2ce7ce0`）

> 岗位：SBC（Raspberry Pi / Orange Pi）上把 **接收机 RAW → TCP → NTRIP/落盘/本地 caster**，并用 Flask Web 管服务。冲突时：**本机 `tools/install.sh --help` / `settings.conf` / 上游 README > 本文**。纯 CLI 流转 → [rtklib](./rtklib.md)；多用户 Caster → [bkg-ntripcaster](./bkg-ntripcaster.md)；桌面联调 → [pygpsclient](./pygpsclient.md)。

## 1. 用途与边界

**做：**

- 一键/`install.sh`：依赖、编 RTKLIB、部署 **systemd unit**、可选探测/配置 F9P·Mosaic-X5·UM980/982
- Web：星座电平、地图、启停服务、改设置、RAW→RINEX、下载日志
- 服务链：`str2str_tcp`（串口→TCP）→ `str2str_ntrip_{A,B}` / `str2str_file` / 本地 NTRIP caster / RTCM TCP·串口·UDP
- 默认口令 `admin`；Armbian 现成镜像可选

**不做：**

- **不是** 国家级 CORS / 发表级坐标引擎 → [pride-pppar](./pride-pppar.md) / [ginan](./ginan.md)
- **不是** 无硬件的纯软件 PPP 工具箱（本页冒烟止于配置/脚本）
- **不是** 通用 NTRIP 客户端库 → [ntripstreams](./ntripstreams.md) / [pygnssutils](./pygnssutils.md)
- 本机共享 Linux **无 USB 接收机、无 systemd 目标部署** → 下列「可测 / 不可测」须遵守

一句话：RTKBase = **爱好者/小台站的 Pi 基站发行版（Web + str2str + 接收机配置）**。

**质检边界：** 本机可复现 clone / `tools/install.sh --help` / ConfigManager 合并 INI / 12 个 unit 模板；**无树莓派、无 GNSS 接收机 → 未** `systemctl start`、**未**探测串口、**未**上行 NTRIP、**未**开 Web。

| 术语 | 含义 |
| --- | --- |
| `settings.conf` | 运行时 INI；由 `settings.conf.default` 合并而来 |
| `run_cast.sh` | 读 settings，拼 `str2str -in … -out …` |
| `str2str_tcp` | 接收机串口 → `tcp_port`（默认 **5015**） |
| NTRIP A/B | 两路上行 caster（默认示例 `caster.centipede.fr`） |
| `rtkbase_web` | Flask+SocketIO Web（默认 **80**） |
| `convbin.sh` | 压缩 RAW → RINEX（调 `convbin`） |

## 2. 安装路径（目标机：Pi/SBC）

### 2.1 一键（推荐）

```bash
# 先接好 GNSS 接收机 USB/UART，再：
cd ~
wget https://raw.githubusercontent.com/Stefal/rtkbase/master/tools/install.sh -O install.sh
chmod +x install.sh
sudo ./install.sh --all release
# 浏览器 http://<sbc-ip> ；默认密码 admin
```

### 2.2 分步（排障用）

```bash
sudo ./install.sh --dependencies
sudo ./install.sh --rtklib          # explorer RTKLIB v2.5.0-EX
sudo ./install.sh --rtkbase-release # 或 --rtkbase-repo master
sudo ./install.sh --unit-files
sudo ./install.sh --gpsd-chrony     # 可选：接收机授时
sudo ./install.sh --detect-gnss
sudo ./install.sh --configure-gnss
sudo ./install.sh --start-services  # rtkbase_web, str2str_tcp, gpsd, chrony…
```

常用旗标：`--user=john` → 装到 `/home/john/rtkbase`；`--help` 看全表。

### 2.3 本机（文档仓 / 无硬件）可做的核对

```bash
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone --depth 1 https://github.com/Stefal/rtkbase.git
cd rtkbase && git rev-parse --short HEAD   # 本机 2ce7ce0
bash tools/install.sh --help | head -n 30

python3 -m venv ~/iono_ops/venv-rtkbase && source ~/iono_ops/venv-rtkbase/bin/activate
pip install -U pip
pip install Flask Flask-Login Flask-SocketIO Flask-WTF Bootstrap-Flask WTForms PyYAML psutil requests

cp settings.conf.default /tmp/rtkbase_user.conf
python3 - <<'PY'
import sys
sys.path.insert(0, 'web_app')
from RTKBaseConfigManager import RTKBaseConfigManager
cm = RTKBaseConfigManager('settings.conf.default', '/tmp/rtkbase_user.conf')
print('version', cm.config.get('general', 'version'))
print('tcp_port', cm.get_main_settings())
print('ntrip_A', cm.get_ntrip_A_settings())
print('datadir', cm.config.get('local_storage', 'datadir'))
PY
# 期望：version 2.7.0；tcp_port 5015；caster.centipede.fr / Your_mount_name
```

**本机结果（tip `2ce7ce0` / conf 2.7.0，2026-09-24 05:11 EDT；质检复跑 2026-09-24 05:16 EDT 同数）：** `install.sh --help` 正常；ConfigManager 写出合并后的 `/tmp/rtkbase_user.conf`；解析到 **12** 个 `unit/*.service`。未启动 Web（缺 root/systemd/接收机）。

## 3. 服务、NTRIP 与数据流

### 3.1 核心 unit（占位符由 install 替换）

| unit | 作用 |
| --- | --- |
| `str2str_tcp.service` | `run_cast.sh in_serial out_tcp` |
| `str2str_ntrip_A.service` | TCP → NTRIP A（`Requires=str2str_tcp`） |
| `str2str_ntrip_B.service` | 第二路上行 |
| `str2str_local_ntrip_caster.service` | 板载 NTRIP caster（默认端口 **2101**） |
| `str2str_file.service` | RAW 落盘轮转 |
| `str2str_rtcm_svr.service` | RTCM TCP 服务（默认 **5016**） |
| `rtkbase_web.service` | Web UI |
| `rtkbase_archive.timer` | 归档/清盘 |
| `rtkbase_raw2nmea.service` | RAW→NMEA TCP（**5014**） |

```bash
# 目标机上（安装后）：
systemctl status rtkbase_web str2str_tcp str2str_ntrip_A
journalctl -u str2str_ntrip_A -n 50 --no-pager
```

### 3.2 settings 关键节

| 节 | 关键键 | 冒烟默认 |
| --- | --- | --- |
| `[general]` | `web_port` / `web_authentification` | 80 / true |
| `[main]` | `position` lat lon h；`com_port`；`tcp_port` | 示例坐标；空串口；**5015** |
| `[ntrip_A]` | `svr_addr_a` `svr_port_a` `mnt_name_a` `svr_pwd_a` `rtcm_msg_a` | centipede / 2101 / Your_mount_name |
| `[ntrip_B]` | 同上 B 路 | 同左 |
| `[local_ntrip_caster]` | `local_ntripc_port` / mnt / msg | 2101 |
| `[local_storage]` | `datadir` `file_rotate_time` `archive_rotate` | `$BASEDIR/data` / 24h / 60d |
| `[rtcm_svr]` | `rtcm_svr_port` | 5016 |

`run_cast.sh` 把 NTRIP A 拼成：

```text
str2str -in tcpcli://localhost:5015#<format> \
  -msg <rtcm_msg_a> \
  -out ntrips://:<pwd>@<addr>:<port>/<mnt>#rtcm3 -p <lat lon h>
```

### 3.3 可测 vs 不可测（无 Pi/GNSS）

| 可（本机已做） | 不可（需硬件/SBC） |
| --- | --- |
| clone、`install.sh --help`、读 unit/settings | `detect-gnss` / `configure-gnss` |
| ConfigManager 合并 INI | `systemctl start` 全栈 |
| 有系统 `str2str`/`convbin` 时可看 `-h` | 真实串口 RAW、上行 NTRIP 鉴权成功 |
| 读 `tools/convbin.sh` 逻辑 | Web 卫星图/电平实况 |
| | Armbian 刷机与 POE 供电验收 |

## 4. 接到哪步

- 流转发/事后解 → [rtklib](./rtklib.md)；多用户播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)
- 协议层调试 → [ntripstreams](./ntripstreams.md) / [pyrtcm](./pyrtcm.md) / [pyubx2](./pyubx2.md)
- 板卡桌面 → [pygpsclient](./pygpsclient.md)；精密事后 → [ginan](./ginan.md) / [pride-pppar](./pride-pppar.md)
- 工作流 **C**：本文（台站侧）→（可选 [bkg-ntripcaster](./bkg-ntripcaster.md)）→ 流动端 [rtklib](./rtklib.md)/[pygpsclient](./pygpsclient.md)

## 5. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | Web 打不开 | 服务未起 / 防火墙 / 错 IP | `systemctl status rtkbase_web`；试 `http://<ip>` |
| 2 | 无卫星/无流 | 未识别接收机或串口空 | `sudo ./install.sh --detect-gnss`；查 `com_port` |
| 3 | NTRIP 401/断流 | 密码/挂载名错 | Web Settings 改 `svr_pwd_*`/`mnt_name_*` 后重启 unit |
| 4 | `str2str_ntrip_A` 反复重启 | 依赖的 `str2str_tcp` 挂了 | `systemctl status str2str_tcp`；先修串口 |
| 5 | 坐标漂、固定差 | `position` 仍是示例 | 用 PPP/CORS 后处理填精确坐标再播 1005/1006 |
| 6 | 在 x86 无硬件跑 `--all` | 脚本假定 SBC+接收机 | 只做 §2.3 配置冒烟；真站用 Pi |
| 7 | Debian < 12 无法升级 | 上游弃用旧系统 | 升到 Debian 12+ / Ubuntu 24.04+ |
| 8 | Python < 3.11 警告 | 2.7.0 起弃用 | `python3 --version`；换系统镜像 |
| 9 | RAW→RINEX 失败 | 无 `convbin` 或格式不符 | 确认 RTKLIB 安装；查 `receiver_format` |
| 10 | 磁盘被日志吃满 | 未开归档/阈值 | 调 `archive_rotate`/`min_free_space`；启 `rtkbase_archive.timer` |
| 11 | 当 CORS 运营平台 | 缺冗余/监测/SLA | 小站可用；国家级另选架构 |
| 12 | 与 [ginan](./ginan.md) 混用期望 | 实时基站 ≠ 精密分析中心 | 基站 RTKBase；事后精密用 Ginan/PRIDE |

## 6. 选型

| 你要… | 用 |
| --- | --- |
| Pi 基站 + Web + NTRIP 上行 | **本文 RTKBase** |
| 裸 `str2str`/`rnx2rtkp` | [rtklib](./rtklib.md) |
| 多用户 Caster | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 桌面收 NTRIP/UBX | [pygpsclient](./pygpsclient.md) |
| 事后精密 PPP/POD | [ginan](./ginan.md) / [pride-pppar](./pride-pppar.md) |

## 7. 相关

[rtklib](./rtklib.md) · [ginan](./ginan.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [ntripstreams](./ntripstreams.md) · [pygnssutils](./pygnssutils.md) · [pygpsclient](./pygpsclient.md) · [pyubx2](./pyubx2.md) · [pyrtcm](./pyrtcm.md) · [README](./README.md)

- 现成镜像：上游 README → Armbian_RTKBase releases
- 局域网发现：`tools/find_rtkbase/dist`
- 许可：AGPL-3.0（Web 源来自 ReachView 系修改）
