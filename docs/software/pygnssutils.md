# pygnssutils · NTRIP 客户端 / 简易 Caster / 多协议 GNSS 流工具（Python）

> 目录条目：[`PROJECTS.json` → `pygnssutils`](../../PROJECTS.json)  
> 上游仓库：<https://github.com/semuconsulting/pygnssutils>  
> 官方文档：<https://www.semuconsulting.com/pygnssutils>  
> PyPI：`pip install pygnssutils` · 许可：**BSD-3-Clause**  
> 列表分类：[03 GNSS 数据](../../lists/03-gnss-data.md) · 子类：RTCM/NTRIP  
> 同门 GUI：[PyGPSClient](https://github.com/semuconsulting/PyGPSClient)  
> 本页角色：把「协议流」接到实验、脚本与简易播发；**不算 TEC、不做精密定位滤波**。

---

## 目录（本页导航）

1. [场景：什么时候必须用它](#1-场景什么时候必须用它)
2. [概念：把名词一次对齐](#2-概念把名词一次对齐)
3. [安装与环境](#3-安装与环境)
4. [逐步例子（含预期输出）](#4-逐步例子含预期输出)
5. [输入输出与数据格式](#5-输入输出与数据格式)
6. [接到本仓哪一步分析](#6-接到本仓哪一步分析)
7. [常见坑（≥12）](#7-常见坑12)
8. [同类选型](#8-同类选型)
9. [附录：检查清单 / 决策树 / 运维备忘](#9-附录)

---

## 1. 场景：什么时候必须用它

### 1.1 一句话

**pygnssutils** 是 semuconsulting 生态里的 **Python CLI + 可嵌入类**：在 `pyubx2` / `pyrtcm` / `pynmeagps` / `pysbf2` 等协议库之上，提供：

- `gnssntripclient`：从 NTRIP Caster 拉 **RTCM3** 或 **SPARTN**；
- `gnssserver`：TCP 转发，或 **单挂载点** NTRIP Server/Caster；
- `gnssstreamer`（历史名曾近 `gnssdump`）：串口 / 文件 / socket / NTRIP 等多源读写、过滤、格式化；
- `GNSSReader` 等类：同一条流上混合读 NMEA、UBX、SBF、RTCM、SPARTN 等。

它解决的是 **「流怎么进、怎么出、怎么在脚本里自动化」**，不是「坐标怎么解」或「TEC 怎么校准」。

### 1.2 典型一天（故事化场景）

**场景 A · 新板卡开箱联调（30–60 分钟）**

实验室新到 u-blox ZED-F9P。你要确认：串口有 UBX/NMEA；能连上校内 NTRIP；RTCM 类型里出现 1005/1077；板卡进 FIXED。用本包比装一整套 BNC 更快：`gnssstreamer` 看协议 → `gnssntripclient` 拉流 → 必要时 `gnssserver` 把串口 RTCM 转成局域网可订的挂载点，给另一台笔记本上的 RTKLIB 用。

**场景 B · 课程演示「最小 CORS」**

教师机：接收机 + `gnssserver --ntripmode 1`。学生机：`gnssntripclient` 或手机 NTRIP App。目标是讲清 mountpoint、源表、鉴权、GGA，而不是讲模糊度。演示结束即可关进程，不必上 BKG Professional Caster。

**场景 C · 脚本化录差分流**

科研助理每天用 cron 订阅某公开/合作 caster，把 RTCM 落到按日期命名的文件，周末批量转 RINEX，再跑 [PyTECGg](./pytecgg.md) 或 [IonoMoni](./ionomoni.md)。本包适合「无 GUI 的可重复拉取」。

**场景 D · 回归测试喂流**

你在写自己的 RTCM 解析器或质量探针。需要稳定、可过滤的字节流。`gnssstreamer` 从文件重放，或从 caster 拉真流，过滤到只要 MSM，写入测试夹具。

**场景 E · 不该用的时候**

- 同时监视 50+ 挂载点、要运维仪表盘、要内置实时 PPP → [BNC](./bnc.md)。  
- 对外提供多用户、多挂载点、组权限、中继 → [BKG NtripCaster](./bkg-ntripcaster.md)。  
- 只要读本地 RINEX 算 TEC → [georinex](./georinex.md) / [PyTECGg](./pytecgg.md)，与 NTRIP 无关。

### 1.3 与本仓电离层主线的关系

```text
NTRIP/串口流 ──► pygnssutils ──► 二进制 RTCM/原始观测流
                      │
                      ├─► RTKLIB / 板卡（定位）
                      │
                      └─► 转 RINEX ──► georinex / Anubis / PyTECGg / IonoMoni
```

**记住：** 本包停在「流」；电离层科学从 RINEX（或厂商专有观测）才真正开始。

### 1.4 谁会受益

| 角色 | 收益 |
|---|---|
| 嵌入式/板卡工程师 | 快速确认差分链路 |
| 课程教师 | 最小 caster 演示 |
| 科研助理 | cron 录流 |
| 开源贡献者 | 协议回归测试 |
| 电离层研究生 | 仅当需要实时落盘时；平时优先事后 RINEX |

---

## 2. 概念：把名词一次对齐

### 2.1 NTRIP 三件套

| 术语 | 人话 | 你在本包里怎么碰到 |
|---|---|---|
| **NtripServer** | 把接收机/编码器的流 **推** 进 caster | 板卡固件或 `gnssserver` 作源侧 |
| **NtripCaster** | 登记挂载点、鉴权、转发 | 别人的主机，或本包简易单挂载点，或 BKG |
| **NtripClient** | **拉** 某个 mountpoint | `gnssntripclient` |

### 2.2 源表与挂载点

- **Sourcetable**：HTTP 响应里的文本表，常见记录类型 `CAS`（caster）、`NET`（网络）、`STR`（流/挂载点）。  
- **Mountpoint**：`STR` 的名字，客户端订阅目标。大小写、是否带前导 `/` 因实现而异，以源表原文为准。  
- **动态源表**：有的 caster 只显示 **当前在线** 的流；离线挂载点「昨天还在今天没了」是常态。

### 2.3 RTCM3 与 SPARTN

- **RTCM3**：差分、观测、站坐标、MSM 等消息族。电离层/定位联调里最常见。典型类型（视源流）：1005/1006（天线参考点）、1074–1077（GPS MSM）、108x GLONASS、109x Galileo、112x BDS、1230 等。  
- **SPARTN**：另一类改正编码，常与 PPP-RTK / 商用服务相关。`--datatype SPARTN` 与 RTCM 不要混用假设。  
- **本包能力**：拉流 + 用底层库解析/过滤；**不**替你做网络 RTK 引擎。

### 2.4 GGA 与 VRS

许多 **网络 RTK / VRS** 要求客户端周期性发送 NMEA **GGA**（近似位置），caster 或服务端才生成/选择适合你的虚拟观测或改正。

本包对应概念：

- `--ggainterval`：发送间隔（秒）；特殊值（如 `-1`）表示不发——以当前 `-h` 为准。  
- `--reflat` / `--reflon` / `--refalt`：固定参考坐标。  
- 若嵌入库且上层 App 实现活体坐标回调，可用接收机真位置代替固定值（见官方 `GNSSNTRIPClient` 说明）。

**坐标错半球或偏差几百公里** → 轻则无固定，重则收到「别人的格子」的改正。

### 2.5 NTRIPv1 与 v2

握手、鉴权头、是否强制基本认证等细节不同。接错版本的典型症状：401、空 body、立刻断开。联调时 **源表成功但订阅失败**，优先核对 `--ntripversion`。

### 2.6 本包 CLI 地图

| CLI | 主职责 | 类比 |
|---|---|---|
| `gnssntripclient` | 客户端：源表或订阅 | curl 的 NTRIP 版 |
| `gnssserver` | TCP 服务或单挂载点 caster | 迷你 icecast/NTRIP |
| `gnssstreamer` | 多源 I/O + 过滤 + 格式化 | GNSS 界的 `socat`+过滤器 |
| （库）`GNSSReader` | 混合协议读取 | 统一 `*Reader` |
| （库）`GNSSNTRIPClient` | 可编程客户端 | CLI 背后的类 |
| （库）`GNSSSocketServer` | 可编程服务端 | `gnssserver` 背后 |

### 2.7 协议过滤（protfilter）直觉

板卡可能同时吐 NMEA + UBX + RTCM。过滤设错会出现「串口灯在闪、解析器却沉默」。联调顺序建议：

1. 不过滤或宽过滤，确认有字节；  
2. 看消息类型分布；  
3. 再收紧到只要 RTCM 或只要 UBX。

具体 bit/枚举以你版本 `-h` 与文档为准（版本间可能调整）。

### 2.8 安全模型（概念层）

- 账号密码可通过 CLI 或环境变量 `PYGPSCLIENT_USER` / `PYGPSCLIENT_PASSWORD`（与 PyGPSClient 共用习惯）。  
- TLS/`--https`、自签证书、PEM 路径：公司 caster 常见；**调试用 self-sign 开关不要留在生产**。  
- `gnssserver` 绑 `0.0.0.0` = 网卡可达范围内谁都能连（视防火墙）。单挂载点试验 ≠ 生产授权模型。

### 2.9 它明确不做的事

- 不输出 STEC/VTEC/ROTI/AATR/GIM。  
- 不做 PPP/RTK 状态估计（那是 RTKLIB/板卡/PRIDE）。  
- 不做多租户配额、计费、复杂源表编辑 GUI。  
- 不实现 VRS 算法本身（只配合需要 GGA 的上游服务）。

---

## 3. 安装与环境

### 3.1 要求

- **Python ≥ 3.10**（以当前 PyPI / 上游 `requires-python` 为准）。  
- 串口访问权限（Linux 常见需 `dialout` 组）。  
- 网络：出站访问 caster 端口（常见 2101；亦有 80/443）。

### 3.2 推荐：虚拟环境安装

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python3 -m pip install -U pip
python3 -m pip install -U pygnssutils

gnssntripclient -h | head
gnssserver -h | head
gnssstreamer -h | head

python3 -c "import pygnssutils; print('ok', getattr(pygnssutils, '__version__', 'version-attr-varies'))"
```

### 3.3 账号与环境变量

```bash
export PYGPSCLIENT_USER='your_user'
export PYGPSCLIENT_PASSWORD='your_pass'
# 验证当前 shell 是否可见（不要把输出贴到公开 issue）
echo "user_set=$([ -n \"$PYGPSCLIENT_USER\" ] && echo yes || echo no)"
```

**禁止：** 把密码写进 Git 仓库、截图发到公开聊天、写进世界可读的 crontab 明文（可用受限文件 + `set -a; source`）。

### 3.4 可选同门 GUI

```bash
python3 -m pip install -U pygpsclient
# GUI 安装与系统 Qt/显示相关，失败时不影响 CLI 使用
```

### 3.5 升级与锁定

```bash
python3 -m pip install -U pygnssutils
python3 -m pip freeze | grep -i pygnss
# 科研可复现：把 pygnssutils==x.y.z 写进 requirements.txt
```

### 3.6 安装失败常见原因

| 现象 | 处理 |
|---|---|
| `pip` 指向 Python2 | 用 `python3 -m pip` |
| 公司镜像缺包 | 临时官方 PyPI 或内网镜像同步 |
| 权限错误 | 不要 `sudo pip`；用 venv |
| CLI 找不到 | 确认 `which gnssntripclient` 在 venv 的 `bin` |

### 3.7 与 RTKLIB / BNC 共存

三者可同机安装，无强制冲突。注意 **端口 2101** 不要重复占用：`gnssserver`、NtripCaster、其他演示服务选不同端口。

---
## 4. 逐步例子（含预期输出）

> **占位符说明：** `example-caster.example.org`、`YOUR_MOUNT`、坐标、串口路径均须换成你有权限的真实值。  
> **参数权威：** 若本地 `-h` 与下文不一致，**以你安装版本为准**（上游偶有选项更名）。

### 4.1 例子 A · 只探活 sourcetable

**目的：** 不订阅业务流，先确认网络、鉴权、源表可读。

```bash
gnssntripclient \
  --server example-caster.example.org \
  --port 2101 \
  --https 0 \
  --datatype RTCM \
  --ntripversion 2.0 \
  --reflat 39.9042 --reflon 116.4074 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**预期输出（特征，非逐字）：**

- 连接与 HTTP 状态相关日志；  
- 多行源表文本，含 `STR;` 开头的挂载点描述；  
- 能读到格式（RTCM3.x 等）、载波、参考位置近似值。

**成功判据：** 你能指出即将订阅的 mountpoint 字符串，与源表完全一致。

**失败分流：**

- 超时 → DNS/防火墙/错端口；  
- 401 → 账号或版本；  
- 空表 → 权限或 caster 配置为不返回表。

### 4.2 例子 B · 订阅挂载点并观察 RTCM 类型

```bash
gnssntripclient \
  --server example-caster.example.org \
  --port 2101 \
  --mountpoint YOUR_MOUNT \
  --datatype RTCM \
  --ntripversion 2.0 \
  --ggainterval 60 \
  --reflat 39.9042 --reflon 116.4074 --refalt 44.0 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**预期：**

- 持续有消息类型打印或统计（取决于 verbosity/格式选项）；  
- 典型可见 1005/1006、以及各系统 MSM（1077/1097/1127 等，视源而定）；  
- 约每 60 s 有 GGA 发送痕迹（若服务需要且 verbosity 足够）。

**成功判据：** 连续 2 分钟不是「零消息」；类型集合与服务文档大致相符。

**把日志落到文件：**

```bash
gnssntripclient \
  --server example-caster.example.org \
  --port 2101 \
  --mountpoint YOUR_MOUNT \
  --datatype RTCM \
  --ntripversion 2.0 \
  --ggainterval 60 \
  --reflat 39.9042 --reflon 116.4074 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2 \
  > /tmp/ntrip_$(date +%Y%m%d_%H%M).log 2>&1
```

### 4.3 例子 C · 无 GGA 的「裸流」对照实验

有的挂载点是单向广播（如某些 SSR），不需要 GGA。对比：

```bash
# 不发送 GGA（参数名/哨兵值以 -h 为准；下列为常见思路）
gnssntripclient \
  --server example-caster.example.org \
  --port 2101 \
  --mountpoint YOUR_SSR_MOUNT \
  --datatype RTCM \
  --ntripversion 2.0 \
  --ggainterval -1 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

**预期：** 若该服务本就不需 GGA，流正常；若是 VRS，则可能空闲或断开——由此 **用实验证明该挂载点是否要位置**。

### 4.4 例子 D · 本机单挂载点 caster（串口 → NTRIP）

```bash
# 终端 1：服务端
gnssserver \
  --inport "/dev/ttyACM0" \
  --hostip 0.0.0.0 \
  --outport 2101 \
  --ntripmode 1 \
  --protfilter 4 \
  --format 2 \
  --ntripuser labuser \
  --ntrippassword 'change-me-now' \
  --verbosity 2
```

```bash
# 终端 2：本机客户端冒烟
gnssntripclient \
  --server 127.0.0.1 \
  --port 2101 \
  --mountpoint pygnssutils \
  --ntripuser labuser \
  --ntrippassword 'change-me-now' \
  --datatype RTCM \
  --verbosity 2
```

**预期：**

- 服务端日志显示有客户端连接；  
- 客户端看到与串口源一致的 RTCM/协议消息；  
- 默认挂载点名常见为 `pygnssutils`（**以上游当前文档为准**，若不同以 `-h`/文档为准）。

**Windows 串口：** 将 `/dev/ttyACM0` 换成 `COM3` 等；管理员权限有时需要。

**成功判据：** loopback 订阅稳定 5 分钟无断；再考虑局域网 IP。

### 4.5 例子 E · 仅 TCP 转发（非 NTRIP 模式）

```bash
gnssserver \
  --inport "/dev/ttyACM0" \
  --hostip 127.0.0.1 \
  --outport 50010 \
  --ntripmode 0 \
  --verbosity 2
```

**预期：** 普通 TCP 客户端可连 `50010` 吃原始字节；适合喂 RTKLIB `str2str` 的 TCP 输入。

### 4.6 例子 F · gnssstreamer 看「板卡到底吐什么」

```bash
gnssstreamer \
  --inport "/dev/ttyACM0" \
  --verbosity 2
```

**预期：** 混合协议时能看到 NMEA 句、UBX 类名或 RTCM 类型（取决于格式选项）。先宽后窄。

过滤思路（选项名以 `-h` 为准）：

```bash
gnssstreamer \
  --inport "/dev/ttyACM0" \
  --protfilter 4 \
  --verbosity 2
```

### 4.7 例子 G · 从文件重放

```bash
# 将已录制的原始流当输入（扩展名不重要，内容是字节流）
gnssstreamer \
  --infile /data/captures/base_20260918.bin \
  --verbosity 2
```

**预期：** 按文件速率或实时策略重放（行为以上游为准）；用于演示与回归，不消耗 caster 配额。

### 4.8 例子 H · Python 库：GNSSNTRIPClient 骨架

```python
"""minimal_ntrip_skeleton.py — 骨架，非正式生产代码"""
from pygnssutils.gnssntripclient import GNSSNTRIPClient

def main():
    client = GNSSNTRIPClient()
    ok = client.run(
        server="example-caster.example.org",
        port=2101,
        mountpoint="YOUR_MOUNT",
        ntripuser="user",
        ntrippassword="pass",  # 改为 os.environ
        version="2.0",
        datatype="RTCM",
        ggainterval=60,
        reflat=39.9042,
        reflon=116.4074,
        refalt=44.0,
    )
    print("run accepted:", ok)
    # 生产中：注册输出介质、处理重连、捕获 KeyboardInterrupt、避免明文密码

if __name__ == "__main__":
    main()
```

**预期：** `run` 返回成功后后台拉流；你必须按官方文档把数据写到 `Queue`、串口或文件。本骨架只验证「能启动」。

### 4.9 例子 I · 接到 RTKLIB str2str（概念命令）

```bash
# 概念：本机 gnssserver TCP 50010 → str2str → 再输出
# 精确参数见 rtklib.md 与你编译的 str2str -h
str2str -in tcpcli://127.0.0.1:50010 -out file:///%Y%m%d_%h%M.rtcm3
```

**预期：** 文件增大；`rtkrcv` 或板卡可再消费。电离层分析仍建议最终 RINEX。

### 4.10 例子 J · 双工具交叉验证

1. 同一挂载点用 `gnssntripclient` 记 3 分钟消息类型集合 T1。  
2. 用 [BNC](./bnc.md) 订同一挂载点，看消息统计 T2。  
3. 若 T1、T2 差异巨大 → 本机过滤/版本/GGA 问题优先于「服务坏了」。

### 4.11 例子 K · HTTPS caster

```bash
gnssntripclient \
  --server secure-caster.example.org \
  --port 443 \
  --https 1 \
  --mountpoint YOUR_MOUNT \
  --ntripversion 2.0 \
  --ntripuser "$PYGPSCLIENT_USER" \
  --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2
```

自签证书时需按上游打开允许自签并配置 PEM（选项名以 `-h` 为准）。**预期：** TLS 握手成功后再出现源表/消息；失败则先用 `openssl s_client` 证明网络与证书链。

### 4.12 例子 L · 录流 1 小时后的「是否值得转 RINEX」检查

```bash
# 伪流程
ls -lh /data/captures/*.bin
# 若平均码率过低（接近 0）：挂载点空窗或断连
# 若码率正常：用 BNC/厂商/自定义转 RINEX，再 georinex.load 探活
```

**预期决策：**

- 码率正常 → 进入 [georinex](./georinex.md)；  
- 码率近 0 → 先修 NTRIP，不要怀疑 TEC 算法。

### 4.13 短会话完整演示脚本（实验室）

```bash
#!/usr/bin/env bash
# lab_ntrip_smoke.sh — 示例，请改主机与挂载点
set -euo pipefail
source .venv/bin/activate
: "${PYGPSCLIENT_USER:?set user}"
: "${PYGPSCLIENT_PASSWORD:?set pass}"
HOST=example-caster.example.org
MOUNT=YOUR_MOUNT

echo "[1] sourcetable"
timeout 30 gnssntripclient --server "$HOST" --port 2101 \
  --ntripversion 2.0 --verbosity 1 \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" || true

echo "[2] subscribe 90s"
timeout 90 gnssntripclient --server "$HOST" --port 2101 \
  --mountpoint "$MOUNT" --datatype RTCM --ntripversion 2.0 \
  --ggainterval 30 --reflat 39.9 --reflon 116.4 \
  --ntripuser "$PYGPSCLIENT_USER" --ntrippassword "$PYGPSCLIENT_PASSWORD" \
  --verbosity 2 || true

echo "done"
```

**预期：** 第一步能刷源表；第二步 90 s 内有消息；`timeout` 退出码可能非 0（因超时），以日志内容为准。

---
## 5. 输入输出与数据格式

### 5.1 总表

| 方向 | 内容 | 备注 |
|---|---|---|
| 输入 | NTRIP 源表、RTCM3/SPARTN 流 | 需网络与账号 |
| 输入 | 串口字节流 | UBX/NMEA/RTCM/SBF 等 |
| 输入 | 文件/TCP | 重放或转发 |
| 输出 | 终端解析日志 | verbosity 控制 |
| 输出 | 转发二进制 | 串口/文件/TCP |
| 输出 | 简易 caster 播发 | 单挂载点 |
| 不做 | TEC 产品、PPP 解 | 外接工具 |

### 5.2 认证材料格式

- 用户名/密码：ASCII 常见；特殊字符注意 shell 引号。  
- 环境变量优先于写进脚本。  
- 某些 caster 用「套餐密钥」当密码——仍是密码学意义上的秘密。

### 5.3 源表行（概念认识）

你不需要手写源表也能当客户端，但要会读：

```text
STR;MOUNT1;desc;RTCM 3.3;1005(1),1077(1),...;2;GPS+GLO;...;...;...;none;N;N;0;...
```

字段含义以 RTCM/NTRIP 文档为准；本包负责拉取，不负责替运营商生成合法源表（那是 NtripCaster 管理域）。

### 5.4 录制文件如何命名（建议规范）

```text
/data/ntrip/{caster}/{mount}/{YYYY}/{DOY}/{mount}_{YYYYDDD}_{HHMM}.rtcm3
```

便于一周后对接 RINEX 批量任务。本包不强制该结构。

### 5.5 与 RINEX 的边界

| 问题 | 答案 |
|---|---|
| pygnssutils 直接写 RINEX 吗？ | 不是其主职责；请用 BNC/`convbin`/厂商工具等 |
| 只有 RTCM MSM 能算 TEC 吗？ | 需先有观测手段并转到分析软件可读格式 |
| 只有改正流没有原始观测？ | 通常不够做双频 STEC |

### 5.6 日志级别

`--verbosity` 提高后：更好排错，也更刷屏。cron 建议低 verbosity + 旋转日志，避免盘满。

### 5.7 时间与坐标格式

- GGA 参考坐标：十进制度（常见），注意不是度分秒字符串。  
- 高程：与椭球/正常高混淆会导致轻微差异；VRS 通常对平面位置更敏感。  
- 时间戳：日志用本地/UTC 取决于环境；科学分析统一 UTC。

---

## 6. 接到本仓哪一步分析

### 6.1 决策表

| 你的下一目标 | 下一篇文档 | 教程 |
|---|---|---|
| 多流 GUI / 录 RINEX | [bnc.md](./bnc.md) | [data-access](../data-access.md) |
| 生产播发 | [bkg-ntripcaster.md](./bkg-ntripcaster.md) | data-access |
| 实时定位 | [rtklib.md](./rtklib.md) | [06](../tutorials/06-iono-positioning.md) |
| 打开事后观测 | [georinex.md](./georinex.md) | [02](../tutorials/02-gnss-dualfreq-tec.md) |
| QC | [anubis.md](./anubis.md) / [gfzrnx.md](./gfzrnx.md) | data-access |
| 绝对 TEC | [pytecgg.md](./pytecgg.md) | [02](../tutorials/02-gnss-dualfreq-tec.md) · [09](../tutorials/09-dcb-biases-deep.md) |
| ROTI/AATR | [ionomoni.md](./ionomoni.md) / [oasis-roti.md](./oasis-roti.md) | [05](../tutorials/05-scintillation-roti.md) |

### 6.2 推荐链路（实时 → 电离层）

1. `gnssntripclient` 验证流；  
2. BNC 或等价工具落 RINEX；  
3. Anubis/GFZRNX；  
4. georinex 探活；  
5. PyTECGg 或 IonoMoni；  
6. ionex-gim 对照 GIM。

### 6.3 推荐链路（仅定位）

1. `gnssntripclient` 或板卡内置 NTRIP；  
2. RTKLIB `rtkrcv`；  
3. 高 ROTI 时段对照 IonoMoni（解释失锁），见教程 05/06。

### 6.4 学习路径中的位置

见 [README.md](./README.md) 路径 C（实时差分联调）。本页是路径 C 的第一站。

---

## 7. 常见坑（≥12）

1. **401/403：** 密码、NTRIPv1/v2、挂载点 ACL。先源表后订阅。  
2. **VRS 无流：** 缺 GGA、间隔过大、参考坐标不在服务区。  
3. **源表有、订阅无：** 动态源表显示「曾存在」；或大小写/斜杠不一致。  
4. **TLS 失败：** 忘了 `--https`、公司代理、自签未允许。  
5. **串口 Permission denied：** 用户不在 `dialout`；拔插后设备名变了。  
6. **误当 BNC：** 期待多流仪表盘与内置 PPP。  
7. **公网裸奔：** 默认密码 + `0.0.0.0` + 无防火墙。  
8. **protfilter 过猛：** 有字节无解析。  
9. **GGA 坐标复制错误：** 经纬度对调、符号错误（东西半球）。  
10. **cron 无环境变量：** 交互 shell 能跑、定时任务 401。  
11. **CLI 选项漂移：** 升级后未看 `-h`。  
12. **SPARTN/RTCM 搞混：** datatype 选错。  
13. **端口占用：** 2101 已被 NtripCaster 占用。  
14. **把改正流当双频观测：** 无法直接 STEC。  
15. **verbosity=0 却抱怨「没输出」：** 提高日志级别。  
16. **防火墙仅放行出站 80：** 2101 被默默丢弃。  
17. **一机多 Python：** `pip install` 装到 A，shell 跑的是 B。  
18. **密码特殊字符被 shell 展开：** 用单引号或 env。

### 7.1 坑位速查表

| 症状 | 最可能原因 | 先做的一件事 |
|---|---|---|
| 立即 401 | 密码/版本 | 只测源表 |
| 连上零消息 | GGA/挂载点空 | 对照 BNC |
| 有字节无类型 | 过滤/datatype | 关过滤 |
| loopback 行局域网不行 | 防火墙/绑定 | 查 `ss -lntp` |
| 仅高峰失败 | 限流/配额 | 问运营商 |

---

## 8. 同类选型

| 需求 | 首选 | 次选 | 不要选本包的理由 |
|---|---|---|---|
| 脚本/CI 单流 | **pygnssutils** | 自写 HTTP | — |
| 多流 GUI | **BNC** | PyGPSClient | 本包偏 CLI |
| 生产 caster | **BKG NtripCaster** | 商业 caster | 单挂载点不够 |
| 协议库 only | pyrtcm/pyubx2 | — | 无需 CLI |
| 定位 | RTKLIB/PRIDE | 板卡 | 本包不解算 |
| TEC | PyTECGg/IonoMoni | — | 本包无观测模型 |

**口诀：** 开发调试 → pygnssutils；值班盯盘 → BNC；对外播发 → NtripCaster；算科学量 → 换工具链。

### 8.1 与 BNC 对照细表

| 维度 | pygnssutils | BNC |
|---|---|---|
| 安装 | pip | 安装包/编译 |
| 多流 | 弱 | 强 |
| 录 RINEX | 非长项 | 强 |
| 实时 PPP | 无 | 有（能力范围内） |
| 自动化 | 极佳 | 一般 |
| 嵌入 Python | 极佳 | 差 |

### 8.2 与 BKG NtripCaster 对照

| 维度 | gnssserver | NtripCaster |
|---|---|---|
| 挂载点 | 单（试验） | 多 |
| 用户组 ACL | 极简 | 完整 |
| 中继 | 非重点 | 有 |
| 容量宣称 | 试验级 | 百源千客户端量级 |

---
## 9. 附录

### 9.1 实验室 30 分钟检查清单

1. `pip show pygnssutils` 记录版本号。  
2. `python3 -c "import pyrtcm,pyubx2"` 确认依赖可导入。  
3. 只跑 sourcetable，保存文本。  
4. 标注目标挂载点字符串。  
5. 订阅 2 分钟，记录 RTCM 类型列表。  
6. 若 VRS：确认 GGA 发送。  
7. 第二工具（BNC）交叉验证。  
8. 若自建 server：先 127.0.0.1 再局域网。  
9. 决定落盘策略（rtcm vs 转 RINEX）。  
10. 密码移出命令行历史。  
11. 写一行笔记：服务是否要 GGA、NTRIPv?、端口。  
12. 把笔记链到当日实验原始记录。

### 9.2 故障排查决策树

```text
连不上
  ├─ 主机名能解析吗？
  ├─ tcping/nc 端口通吗？
  ├─ 401？ → 账号 / ntripversion / 挂载点 ACL
  └─ TLS？ → https 开关与证书

连上无消息
  ├─ 源表中该 STR 是否声明在线？
  ├─ 要不要 GGA？坐标是否在服务区？
  ├─ datatype 是否 RTCM/SPARTN 搞反？
  └─ 服务是否限并发（第二会话挤掉第一）？

有字节解不出
  ├─ protfilter 是否过滤过头？
  ├─ 是否其实是 UBX 不是 RTCM？
  └─ 提高 verbosity / 十六进制抽查同步字 0xD3
```

### 9.3 运维备忘（小型实验网）

- 端口规划：caster `2101`，TCP 原始转发 `50010`，避免冲突。  
- 日志：`/var/log/lab-ntrip/` 按天切割。  
- 监控：一分钟码率 + 进程存活即可，不必上全套 APM。  
- 备份：只备份配置与脚本，不备份大体积 rtcm（或只留 7 天）。  
- 变更：改密码日通知所有学生机配置。

### 9.4 与 data-access 的对应

| data-access 出现的东西 | 本包动作 |
|---|---|
| 公开 NTRIP 列表 | 探活与录流 |
| 「自建播发」 | 先 gnssserver，再评估 BKG |
| RINEX 下载链接 | 不替代；事后数据直接下 |
| SP3/IONEX | 无关 |

### 9.5 课程演示逐字稿（教师可用）

1. 「NTRIP 像有挂载点的收音机。」  
2. 展示源表一行 STR。  
3. 订阅后展示 1077 等类型。  
4. 关掉 GGA，展示 VRS 停流（若条件允许）。  
5. 启动 `gnssserver`，学生机连接。  
6. 强调：这不是 TEC；TEC 要双频观测与校准。  
7. 作业：录 10 分钟流 + 写清是否需要 GGA。

### 9.6 安全加固清单

- [ ] 非默认密码  
- [ ] 不绑公网除非必要  
- [ ] 防火墙限 IP  
- [ ] TLS 在公网场景  
- [ ] 不在 git 中存密  
- [ ] 学生账号按学期轮换  
- [ ] 退出实验停进程  

### 9.7 性能直觉

- 单挂载点 RTCM MSM：通常几十 kbps 量级（视卫星数与倍率）。  
- Python 足够实验教学；千客户端不是目标。  
- 瓶颈常在网络抖动与磁盘，不在解析。

### 9.8 版本记录怎么写进实验笔记

```text
date: 2026-09-20
pygnssutils: x.y.z
python: 3.12.z
caster: host/mount/ntripversion
gga: interval=60, lat=..., lon=...
result: types={1005,1077,...}, ok=true
```

### 9.9 引用与责任

- 版权与许可以上游 BSD-3-Clause 为准。  
- 本页是 Ionosphere-GNSS-OpenSource 的使用导读。  
- 差分服务 ToS、转发是否允许，由运营商约束。  
- 参数漂移以 `-h` 与 <https://www.semuconsulting.com/pygnssutils> 为准。

### 9.10 扩展阅读（站外）

- RTCM 标准文档（需自行获取授权/购买渠道）。  
- NTRIP 协议说明（BKG/IGS 相关页面）。  
- 上游 GitHub README 与 RELEASE notes。  
- 本仓 [bnc.md](./bnc.md)、[bkg-ntripcaster.md](./bkg-ntripcaster.md)、[rtklib.md](./rtklib.md)。

---

## 10. 加深理解：协议与链路分层

### 10.1 四层模型（教学用）

1. **物理/串口层：** USB-UART、波特率、电缆。  
2. **字节流层：** 粘包、阻塞读、重连。  
3. **协议层：** NMEA 句、UBX 类 ID、RTCM 预览字 `0xD3`。  
4. **服务层：** NTRIP 挂载点、鉴权、GGA 合约。

本包主要帮你打通 2–4；第 1 层靠系统与驱动。

### 10.2 为什么「能 ping 通」仍可能 NTRIP 失败

ICMP 通只说明主机可达；TCP 2101 可能仍被过滤；HTTP 鉴权可能失败；TLS 可能失败。请按服务层逐级测，不要停在 ping。

### 10.3 为什么教学环境爱用 2101

历史习惯与示例文档统一；并非协议强制。若 2101 被占用，改 `outport`/`port` 即可，只要客户端一致。

### 10.4 客户端实现差异

不同客户端对「挂载点是否加前导 `/`」「NTRIPv2 头字段」处理略有差异。**交叉验证**（本包 vs BNC）是最快的排除法。

---

## 11. 加深理解：与电离层产品的距离

### 11.1 三种「电离层相关」数据

| 种类 | 例子 | 本包关系 |
|---|---|---|
| 双频原始观测 | RINEX L1/L2 | 需落盘转换后才能用 |
| 改正数 | RTCM SSR、区域差分 | 可拉流，但是改正不是 STEC 产品 |
| 格网产品 | IONEX GIM | 完全另一条下载链 |

### 11.2 常见误解

- 「我订了含 MSM 的流，就等于有了 TEC 时间序列」→ 否，还要完成载波几何无关、整平、偏差处理。  
- 「NTRIP 账号里有电离层」→ 账号只授权流，不附送科学校准。  
- 「实时 ROTI」→ 需专用监测软件或自写流水线，不是 `gnssntripclient` 开关。

### 11.3 何时值得把实时流纳入电离层课题

- 研究闪烁对 **实时定位** 的影响（流 + ROTI + 固定率联合）。  
- 需要补「站点本地实时」而公开 RINEX 延迟太高。  
- 其余情况：优先 CDDIS/区域数据中心的事后 RINEX，质量与元数据更全。

---

## 12. 命令行参数记忆法（非权威，只助记）

> 正式参数表见 `-h`。这里只给记忆钩子。

- `server/port/https`：连哪里。  
- `mountpoint`：订什么；空则常为源表模式。  
- `ntripversion/user/password`：怎么握手。  
- `datatype`：RTCM 还是 SPARTN。  
- `gga*` + `ref*`：位置合约。  
- `verbosity`：嘴碎程度。  
- `ntripmode`（server）：0=TCP，1=NTRIP。  
- `inport/infile`：字节从哪来。  
- `hostip/outport`：服务绑哪。

---

## 13. 练习题（自学）

1. 只根据源表，写出你服务区最合适的挂载点及理由（距离、格式、是否需 GGA）。  
2. 故意输错密码，记录客户端表现，形成「症状库」。  
3. 在要 GGA 的挂载点上，把纬度加 10°，观察流与定位变化。  
4. 用 `gnssserver` 与 BNC 互为客户端/源，画数据路径图。  
5. 将 15 分钟 RTCM 转为 RINEX（任何工具），用 georinex 列出卫星。  
6. 写一段 cron，失败时邮件/飞书通知（自行实现）。  
7. 对比同一时段 RTCM 录包与公开 RINEX 的卫星可见性差异。  
8. 阅读上游对 SPARTN 的说明，用三句话总结与 RTCM 差异。

### 13.1 练习题参考思路（不给标准命令答案）

1. 看 STR 的位置字段与格式字段；优先 RTCM3 MSM、距离近、文档标明支持你的星座。  
2. 401 与重试间隔是关键观察点。  
3. VRS 可能停流或定位漂——说明位置合约的存在。  
4. 路径图应含串口、server、网络、client、RTKLIB。  
5. 卫星列表为空 → 转换失败或过滤过头。  
6. 通知里不要打印密码。  
7. 实时流可能缺某些系统或采样不同。  
8. 编码族、典型服务商、解密需求（若有）三点即可。

---

## 14. 术语对照（中英）

| 中文 | English |
|---|---|
| 挂载点 | mountpoint |
| 源表 | sourcetable |
| 播发站 | caster |
| 差分改正 | correction stream |
| 虚拟参考站 | VRS |
| 多系统多频消息 | MSM |
| 鉴权 | authentication |
| 自签证书 | self-signed certificate |
| 串口 | serial port |
| 重放 | replay |

---

## 15. 与 PROJECTS.json 字段对照

- `name`: pygnssutils  
- `license`: BSD-3-Clause  
- `category`: gnss-data  
- `subcategory`: RTCM/NTRIP  
- `user_relation`: none（非维护者自有）  
- `one_liner_zh`: NMEA/UBX/RTCM/NTRIP/SPARTN 的 Python CLI 工具集  

本页展开的是「怎么用」，不修改 JSON。

---

## 16. 长附录：逐项讲解「一次成功的联调」日志里该有什么

下面用**示意日志**说明如何阅读（并非某版本的逐字拷贝）。你的时间戳、线程名、拼写可能不同。

```text
[INFO] Connecting to example-caster.example.org:2101
[INFO] NTRIP version 2.0
[INFO] Requesting mountpoint YOUR_MOUNT
[INFO] HTTP 200
[INFO] GGA scheduled every 60 s
[DEBUG] RTCM 1005 received
[DEBUG] RTCM 1077 received
[DEBUG] RTCM 1097 received
[DEBUG] GGA sent lat=39.9042 lon=116.4074
```

**阅读顺序：**

1. 是否真正 Connecting 到你以为的主机；  
2. 版本是否 v2；  
3. HTTP 是否 200（401/404/503 各有含义）；  
4. 是否出现你期望的消息类型；  
5. GGA 是否按计划出现。

若只有 Connecting 没有 200：停在 TCP/TLS。  
若 200 后无 RTCM：服务空窗或过滤。  
若有 RTCM 无 1005：有的流不发站坐标，不一定是错误。

### 16.1 HTTP 状态直觉

| 码 | 直觉 |
|---|---|
| 200 | 订阅成功（仍可能后续空闲） |
| 401 | 鉴权 |
| 404 | 挂载点不存在 |
| 503 | 服务忙或源离线 |
| 302/301 | 少见；注意代理 |

### 16.2 「空闲」与「失败」的区别

- **失败：** 握手错、鉴权错、TLS 错、进程崩溃。  
- **空闲：** 握手成功但长时间无消息——可能源站维护、或 VRS 未接受 GGA。

排错时先定性是哪一种，再往下。

---

## 17. 长附录：串口层备忘

### 17.1 Linux 设备名

- `/dev/ttyACM0`：常见 USB-CDC；  
- `/dev/ttyUSB0`：USB-serial 芯片；  
- 拔插后编号可能变；用 `udev` 规则做稳定符号链接更佳。

### 17.2 波特率

许多 GNSS 板卡默认 115200 或更高。设错波特率 → 看起来「有数据」实为乱码，解析器全丢。先用 `minicom`/`screen`/`gnssstreamer` 确认可读 NMEA（若启用）。

### 17.3 权限

```bash
groups | tr ' ' '\n' | grep dialout || echo 'need dialout'
# 管理员将用户加入 dialout 后需重新登录
```

### 17.4 Windows 注意

- 设备管理器查看 COM 号；  
- 某些驱动需厂商包；  
- 防火墙可能拦截 `gnssserver` 监听（首次弹窗允许）。

---

## 18. 长附录：把本包装进更大的自动化

### 18.1 systemd 用户服务思路（示意）

```ini
# ~/.config/systemd/user/lab-ntrip.service  — 示意，非通用模板
[Unit]
Description=Lab NTRIP recorder
After=network-online.target

[Service]
Type=simple
EnvironmentFile=%h/.config/lab-ntrip.env
ExecStart=%h/venv/bin/gnssntripclient --server %i ...
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

环境文件权限 `600`，只含 USER/PASSWORD。

### 18.2 失败告警最小策略

- 连续 5 分钟码率为 0 → 告警；  
- 进程退出 → systemd 重启 + 告警；  
- 磁盘 > 85% → 停录告警。

### 18.3 不要做的自动化

- 自动把密码 echo 到聊天机器人；  
- 自动公网暴露无鉴权 caster；  
- 自动强制 `selfsign=1` 到生产配置仓库。

---

## 19. 长附录：科研伦理与数据使用

- 录制他人 caster 的流，遵守服务条款与是否允许再分发。  
- 课程演示使用合作单位明确授权的挂载点。  
- 论文中写明实时数据来源、采样、是否 VRS、软件版本。  
- 涉及人身安全的导航应用，本教学工具链不足以代替认证系统。

---

## 20. 收束：你学完本页应当能做什么

- [ ] 独立安装 pygnssutils 并运行三个主 CLI 的 `-h`。  
- [ ] 区分源表探活与挂载点订阅。  
- [ ] 说明何时需要 GGA。  
- [ ] 搭一个 loopback 单挂载点试验。  
- [ ] 说出与 BNC、NtripCaster、RTKLIB、PyTECGg 的分工。  
- [ ] 列出至少 8 个坑位与处理。  
- [ ] 把实时流接到「转 RINEX → 本仓 TEC 教程」的路径上。

若以上清单可勾选，路径 C 第一站完成；请回到 [README.md](./README.md) 选择下一站（BNC 或 NtripCaster 或 RTKLIB）。

---

## 21. 补充场景矩阵（便于检索）

| 场景关键词 | 章节 |
|---|---|
| 开箱板卡 | §1.2 A · §4.6 |
| 课程 CORS | §1.2 B · §4.4 · §9.5 |
| cron 录流 | §1.2 C · §18 |
| 回归测试 | §1.2 D · §4.7 |
| VRS | §2.4 · §4.3 · §7.2 |
| HTTPS | §4.11 |
| RTKLIB | §4.9 · §6 |
| 安全 | §2.8 · §9.6 |
| 选型 | §8 |

---

## 22. 补充：消息类型速查（RTCM，非完备）

> 完整定义以 RTCM 标准为准；下表仅助记。

| 类型 | 粗意 |
|---|---|
| 1004 | GPS 旧式观测（遗留） |
| 1005/1006 | 站坐标 |
| 1019 | GPS 星历（有的流夹带） |
| 1033 | 接收机天线描述 |
| 1074–1077 | GPS MSM |
| 1084–1087 | GLONASS MSM |
| 1094–1097 | Galileo MSM |
| 1114–1117 | QZSS MSM |
| 1124–1127 | BDS MSM |
| 1230 | GLONASS 码偏等 |

若日志中只见改正、不见 MSM：你订的是「改正流」而非「原始观测流」。

---

## 23. 补充：SPARTN 相关注意

- 确认账号套餐真的包含 SPARTN。  
- 某些服务需要解密密钥与日期参数（上游 CLI 有相关选项时再配）。  
- 不要假设 SPARTN 消息可用看 RTCM 的同一套「类型号直觉」。  
- 电离层课题仍更常落在双频 RINEX；SPARTN 更贴近定位服务。

---

## 24. 补充：教室网络限制下的预案

| 限制 | 预案 |
|---|---|
| 只放行 80/443 | 问管理员开 2101，或用 HTTPS 443 caster |
| 禁止学生机出站 | 教师机做 caster，内网订阅 |
| 无线不稳定 | 有线演示；录播文件重放 |
| 一人账号限一并发 | 教师统一录流再分发文件（注意 ToS） |

---

## 25. 补充：质量指标（联调期）

- **连接成功率：** 24h 内自动重连成功比例。  
- **平均码率：** 字节/秒。  
- **消息多样性：** 独特 RTCM 类型数。  
- **GGA 合规：** 应发次数 vs 实发次数。  
- **断流 MTTF：** 平均无故障时间。

把这些写进实验课评分表，比「是否画出图」更反映工程能力。

---

## 26. 最终指针

- 上游：<https://github.com/semuconsulting/pygnssutils>  
- 文档：<https://www.semuconsulting.com/pygnssutils>  
- 本仓索引：[README.md](./README.md)  
- 下一步常见：[bnc.md](./bnc.md) · [bkg-ntripcaster.md](./bkg-ntripcaster.md) · [rtklib.md](./rtklib.md) · [georinex.md](./georinex.md)

---

*文档维护：Ionosphere-GNSS-OpenSource `docs/software/`。发现 CLI 更名请优先对上游发 PR/issue，并同步本页。*

## 27. 详解 FAQ（扩写）

### 27.1 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.2 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.3 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.4 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.5 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.6 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.7 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.8 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.9 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.10 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.11 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.12 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.13 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.14 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.15 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.16 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.17 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.18 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.19 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.20 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.21 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.22 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.23 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.24 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.25 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.26 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.27 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.28 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.29 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.30 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.31 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.32 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.33 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.34 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.35 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.36 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.37 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.38 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.39 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.40 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.41 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.42 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.43 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.44 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.45 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.46 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.47 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.48 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.49 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.50 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.51 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.52 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.53 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.54 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.55 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.56 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.57 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.58 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.59 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.60 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.61 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.62 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.63 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.64 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.65 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.66 能把 NMEA 位置当差分源吗？

**短答：** 差分源通常是基站观测/改正；NMEA 位置不能替代 RTCM 观测消息。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.67 学校代理如何设置？

**短答：** HTTPS_PROXY 等对部分连接生效情况因实现而异；常需允许直连 caster 或专用隧道。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.68 怎样测码率？

**短答：** 对录制文件 `wc -c` 除以时长；或用管道计数字节。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.69 消息时间跳跃？

**短答：** 源站重启或网络重连；定位引擎需重收敛；录包分析时按时间分段。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.70 可否用于商业产品？

**短答：** BSD-3-Clause 对代码宽松，但差分数据 ToS、出口管制、责任另论；咨询法务。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.71 可以同时订两个挂载点吗？

**短答：** 开两个进程或在应用层写两个 GNSSNTRIPClient 实例；CLI 单进程一般一挂载点。注意账号并发限制。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.72 为什么 BNC 能连本包不能？

**短答：** 核对版本、挂载点字符串、是否自动 GGA、TLS。把两端日志时间对齐比较。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.73 如何确认 MSM 含相位？

**短答：** 查 RTCM 类型与内容；或转 RINEX 后看 L 观测量。不要仅凭类型号臆测所有单元格都有值。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.74 树莓派能跑吗？

**短答：** 可以；注意串口稳定与散热；生产播发仍更推荐专用 caster。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

### 27.75 是否支持 IPv6？

**短答：** 以上游 GNSSSocketServer 的 ipprot 等参数为准；先在文档确认再规划。

**展开说明：** 在实际实验室里，这类问题通常不是孤立出现的，而是和网络、账号并发、接收机配置、以及学生对 NTRIP 概念的误解缠在一起。建议把现象记录为「可复现步骤」：同一主机、同一挂载点、同一客户端版本、同一时间窗，只改一个变量。若改密码即失败，归鉴权；若改坐标即失败，归 VRS 合约；若改客户端即失败，归实现差异。把结论写回团队知识库，避免下一届同学重复踩坑。

**建议操作顺序：**（1）最小复现；（2）交叉客户端；（3）对照源表；（4）再怀疑本机防火墙。不要一上来重装系统或升级所有包，那样会一次引入多个变量。

**与本仓其他文档的关联：** 若最终目标是 TEC，请尽早从「联调成功」转入 RINEX 与 [georinex.md](./georinex.md)；若最终目标是定位，转入 [rtklib.md](./rtklib.md)；若要对外服务，转入 [bkg-ntripcaster.md](./bkg-ntripcaster.md)。

**课堂提问示例：** 让学生解释为什么「源表能看、订阅失败」不一定是密码错误；让学生设计一次只改 GGA 间隔的对照实验并预测曲线。

