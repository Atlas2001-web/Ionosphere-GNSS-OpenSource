# BNC · BKG Ntrip Client（实时流 / 差分）

目录条目：[`PROJECTS.json` → `BNC`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bnc>  
源码/二进制 FTP：<https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/>

## 作用与场景

**它是什么**：德国 BKG 维护的开源**多流 NTRIP 客户端**（C++/Qt，GPL）。带 GUI，也可批处理。

**它解决什么**：从 NTRIP 播发器（caster）**订阅** RTCM 等实时流——差分改正、观测流、SSR 等——再送到串口/网络端口、落成 RINEX，或在 BNC 内做**实时 PPP**。做「实时电离层/空间天气」或运维教研时，它是目录里的**核心官方客户端**。

**不负责**：不是事后大批量 RINEX 科学分析库；深度算法研究更常事后用 RINEX + Python/RTKLIB。轻量脚本取流也可看 `ntripclient` / `pygnssutils`，但多流运维与内置 PPP 仍看 BNC。

## 术语｜人话

| 术语 | 人话 |
|---|---|
| NTRIP | 经互联网传 GNSS 流的协议（像「挂载点电台」） |
| caster | 播发服务器；你登录后选 mountpoint |
| mountpoint | 某一路流的名字（如某站 RTCM3） |
| RTCM | 差分/观测/改正的消息标准（2.x / 3.x） |
| SSR | 状态空间改正（轨道钟差等），常用于实时 PPP |
| 批处理模式 | 无界面，靠配置文件在服务器上跑 |

## 安装

1. 打开 [BNC 产品页](https://igs.bkg.bund.de/ntrip/bnc)，按系统下载当前版（文档撰写时常见 **v2.13.x**：Windows MSI、macOS DMG、各 Linux 包，或源码）。  
2. Linux「shared」包需本机 Qt5 等依赖——以页面说明为准。  
3. 校验文件可在同目录 checksum；问题提单见 RTCM-Ntrip wiki。

```bash
# 示例：仅示意下载入口，具体文件名以 FTP/网页当前列表为准
# https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/
bnc --help 2>/dev/null || echo "请从官方包安装后，用 GUI 或批处理入口启动"
```

## 最小可跑流程（GUI）

不发明真实账号；请使用你自己的 caster 凭证或公开挂载点政策允许的流。

1. 启动 BNC → 配置 **NTRIP caster** 主机、端口、用户、密码。  
2. 拉取源表（source table）→ 勾选需要的 **mountpoint**。  
3. 选择输出：  
   - 转发到 TCP/串口（供 RTKLIB `str2str` / 接收机）；或  
   - 记录为 RINEX / 原始流；或  
   - 打开内置 **PPP** 面板（需相应改正流与配置）。  
4. Start；看日志是否「connected / decoding」。

### 批处理骨架

```bash
# 以当前上游手册为准：通常传入配置文件
bnc --conf /path/to/bnc.bnc
# 或官方文档所述的静默/批处理开关（版本间可能不同）
```

配置文件建议先在 GUI 里调通再「另存」，避免手写字段名出错。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | NTRIP 流（RTCM 2/3 等）；也可读 RINEX 做部分 PPP/质检功能（见官网概述） |
| 输出 | 解码后的端口流、落盘文件、实时坐标（若开 PPP）、质量/编辑相关产物 |

电离层用户常见用法：订阅高采样观测或区域改正 → 落盘成 RINEX → 再用 [georinex](./georinex.md) / [OASIS](./oasis-roti.md) 事后分析。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 连不上 caster | 防火墙、账号、端口 2101 等被拦 | 先浏览器/源表工具测通；确认机构网络策略 |
| 源表空 | 用户无权限或 caster 地址错 | 核对机构文档；试 IGS/BKG 公开说明中的入口 |
| 有字节无解码 | 挂载点类型与解码器不匹配 | 换 RTCM 版本设置；看 BNC 日志中的 message 号 |
| 实时 PPP 不收敛 | 缺 SSR/精密改正、动态过大 | 确认订阅了匹配的改正流；静态测试先 |
| 只为下历史 RINEX | 工具选重 | 历史文件走 [data-access](../data-access.md) / CDDIS，不必强行实时 |

## 接到电离层分析哪一步

- 实时数据从哪来 → [数据怎么下](../data-access.md)（NTRIP / IGS RTS 一行）  
- 落盘后算 TEC → [02](../tutorials/02-gnss-dualfreq-tec.md) · [georinex](./georinex.md)  
- 实时定位链路 → [RTKLIB](./rtklib.md) · [06 电离层与定位](../tutorials/06-iono-positioning.md)

## 目录指针

- `PROJECTS.json`：`name=BNC` · `url=https://igs.bkg.bund.de/ntrip/bnc`  
- 相关：`BNC-source-FTP`、`BKG-NtripCaster`、`ntripclient`
