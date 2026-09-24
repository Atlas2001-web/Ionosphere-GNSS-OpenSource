# BNC · BKG Ntrip Client 操作手册

目录：[`PROJECTS.json` → `BNC`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bnc> · FTP <https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/> · 帮助 <https://software.rtcm-ntrip.org/export/HEAD/ntrip/trunk/BNC/src/bnchelp.html> · GPL-3.0 · 本机验证 **BNC 2.13.7**（`bnc --help` / REQC 真跑）

> 岗位：多流 NTRIP **订阅 + 录盘/转发**。本页只把「一个挂载点 → 一份 RINEX」跑通；**不做 PPP 长文**。账号口令禁止进 git。GUI 标签随版本微调，以你安装包帮助为准。

## 1. 用途与边界

**做：** 拉源表、订挂载点、解码 RTCM、落盘 RINEX/原始流、TCP 转发到本机 RTKLIB。

**不做：** 脚本单流探活主力（→ [pygnssutils](./pygnssutils.md)）；自建播发（→ [bkg-ntripcaster](./bkg-ntripcaster.md)）；校准 TEC/ROTI（落盘后 → [georinex](./georinex.md)/[pytecgg](./pytecgg.md)/[oasis-roti](./oasis-roti.md)）；QC PDF（→ [anubis](./anubis.md)）。

## 2. 安装

1. 从官网或 FTP 取对应平台包（Linux AppImage/deb、Windows 安装包）。
2. 核对文件大小；过小可能是 HTML 错误页。

```bash
# Debian 打包（本机验证过）
mkdir -p ~/bnc && cd ~/bnc
curl -fsSL -o bnc.zip \
  https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/bnc-2.13.7-debian13.zip
file bnc.zip; unzip -t bnc.zip
unzip -q bnc.zip && chmod +x bnc-2.13.7
sudo apt-get install -y libqt5svg5 libqt5widgets5 libqt5network5 libqt5gui5
./bnc-2.13.7 --version
# Linux AppImage
chmod +x BNC-*.AppImage
./BNC-*.AppImage
# deb
sudo dpkg -i bnc_*.deb || sudo apt -f install -y
sudo apt install -y libqt5widgets5 libqt5network5 libqt5core5a   # 缺 Qt 时
command -v bnc || command -v BNC || echo "用 AppImage 路径"
```

无头机器：先在有显示器的机子 GUI 调通并 Save → 拷贝 `.bnc`：

```bash
bnc --conf /opt/bnc/lab.bnc
# 或 ./BNC-*.AppImage --conf /opt/bnc/lab.bnc
# 批处理无窗（示例，以 --help 为准）：
# bnc --conf lab.bnc --nw
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| AppImage 无法执行 | 无执行位 / 缺 fuse | `chmod +x`；装 `libfuse2` |
| `libQt5*` missing | 缺 Qt 运行库 | 装上表 Qt5 包 |
| 无头立刻退出 | 未给 conf | 必须 `--conf`；先 GUI 生成 |
| 旧 `.bnc` 打不开 | 大版本不兼容 | 新 GUI 重建关键页 |


---

## 3A. 端到端（推荐冒烟）：离线 REQC 拼接四段 15 min → 1 h / 30 s

不依赖公网 NTRIP。本机 **BNC 2.13.7** 真跑通。发行包 `Example_Configs`：

```bash
cd ~/bnc/Example_Configs
mkdir -p Output
../bnc-2.13.7 -nw -conf /dev/null \
  -key reqcAction Edit/Concatenate \
  -key reqcObsFile 'Input/BRUX00BEL_S_2021125*_15M_01S_MO.rnx' \
  -key reqcRnxVersion 3 \
  -key reqcSampling '30 sec' \
  -key reqcStartDateTime 1967-11-02T00:00:00 \
  -key reqcEndDateTime 2099-01-01T00:00:00 \
  -key reqcNewMarkerName BRUX_MARKER \
  -key reqcOutLogFile Output/RinexConcat.log \
  -key reqcOutObsFile Output/BRUX00BEL_S_20211251100_01H_30S_MO.rnx
```

| 键 / 旗标 | 含义 |
| --- | --- |
| `--nw` | 无窗口批处理 |
| `--conf /dev/null` | 空底配置；其余 `--key` 覆盖 |
| `reqcAction` | `Edit/Concatenate` 或 `Analyze` |
| `reqcObsFile` | 输入 OBS；**通配符必须引号** |
| `reqcRnxVersion` | 输出主版本 2/3/4 |
| `reqcSampling` | 例 `30 sec` |
| `reqcNewMarkerName` | 改 MARKER NAME |
| `reqcOutLogFile` / `reqcOutObsFile` | 日志与输出 |

**本机真实日志（截断，2026-09-23）：**

```text
------------------------------------------------------------------------------
RINEX File Editing
------------------------------------------------------------------------------
Program           : BNC 2.13.7
RINEX Version     : 3.05
Sampling          : 30 sec
Input Obs Files   : Input/BRUX00BEL_S_2021125*_15M_01S_MO.rnx
------------------------------------------------------------------------------
Input Obs File: ...11:00:00 ... start: 2021-05-05 11:00:00
Input Obs File: ...11:15:00 ... start: 2021-05-05 11:15:00
Input Obs File: ...11:30:00 ... start: 2021-05-05 11:30:00
Input Obs File: ...11:45:00 ... start: 2021-05-05 11:45:00
```

**输出头 + 统计：** `grep -c '^>'` → **120** 历元。

```text
     3.05           OBSERVATION DATA    M                   RINEX VERSION / TYPE
BNC 2.13.7          box                 20260923 124250 UTC PGM / RUN BY / DATE
BRUX_MARK                                                   MARKER NAME
  4027881.6280   306998.5370  4919498.9840                  APPROX POSITION XYZ
    30.000                                                  INTERVAL
  2021     5     5    11     0    0.0000000     GPS         TIME OF FIRST OBS
```

安装验收也可用：

```bash
./bnc-2.13.7 --version   # → BNC 2.13.7
./bnc-2.13.7 --help | head -n 12
```

`--help` 开头真输出：`Usage:` / `--nw` / `--version` / `--conf` / `--key`。


## 3. 端到端：一个挂载点录成 RINEX

目标：订 **一个** OBS 流，写出 RINEX，用 shell 确认字节与头。公开资源目录见 <https://igs.bkg.bund.de/ntrip/#rtcm-obs>。示例账户仅用于官方 Example_Configs（`Example`/`Configs`）——生产请用你自己的注册账号。

### 3.1 GUI 逐步（点哪里）

1. **启动** BNC → 主窗口出现。
2. **File → Open Options / New**：准备保存为例如 `~/bnc_configs/one_mount.bnc`。
3. **Network 面板**（若在代理后）：填 HTTP 代理 host/port；否则留空。系统钟用 NTP 校准（TLS 对时间敏感）。
4. **Add Stream → Caster**（或 Streams 区 Add）：
   - Host：caster 主机名（例：`products.igs-ip.net` 或提供方给出的地址）
   - Port：常见 **2101**（TLS 端口按提供方）
   - Ntrip 版本：按源要求选 v1/v2
   - User / Password：已授权账号；匿名源可留空
   - 点 **Get Table**（拉源表）
5. **源表**：在列表里选中目标 **mountpoint**（大小写必须与表中一致）→ OK。Streams 画布应出现一行该挂载点。
6. **RINEX Observations 面板**（名称随版本：RINEX / RINEX Observations）：
   - **Directory**：已存在的目录，例 `/data/rinex/lab`（先 `mkdir -p`）
   - **File interval**：切片长度，例 `15 min` / `1 hour` / `1 day`
   - **Sampling**：`0` = 每个历元都写；或设秒数抽稀
   - **Version**：3 或 4（按下游工具）
   - 可选 skeleton / 站名规则：文件名通常取挂载点前 4 字符作站 ID
7. **RINEX Ephemeris**（可选）：若还要 NAV，另订星历挂载点或勾选对应选项；只做观测录盘可先关。
8. **PPP 相关页：全部保持关闭**（本任务不需要）。
9. **Log 面板**：设日志文件路径，例 `/data/rinex/lab/bnc.log`，便于事后 `tail`。
10. 点 **Save Options** / 另存 `one_mount.bnc`（`chmod 600`）。
11. 点 **Start**（不是只改字段就离开）。
12. 盯 **Log** ≥ 60–120 秒；同时另开终端看目录。

```bash
mkdir -p /data/rinex/lab ~/bnc_configs
watch -n 2 'ls -l /data/rinex/lab | tail'
# 或：
tail -f /data/rinex/lab/bnc.log
```

13. 确认非 0 文件后 **Stop** → File → Quit → 再 Save（把最终状态写回磁盘 conf）。
14. 无头复跑：

```bash
bnc --conf ~/bnc_configs/one_mount.bnc
# 验证
head -n 8 /data/rinex/lab/*.rnx /data/rinex/lab/*.obs 2>/dev/null | head -n 40
python -m georinex.time /data/rinex/lab/你的文件.rnx
```

**期望：** `head` 见 `RINEX VERSION / TYPE`；`georinex.time` 给出覆盖录制时段的起止；`ls -l` 字节随时间增大。

### 3.2 官方示例捷径

包内 `Example_Configs/RinexObs.bnc`：多流 → 15 min / 1 Hz RINEX（版本随包说明为 3 或 4）。复制整个 `Example_Configs`（含 Input/Output 子目录），替换口令后：

```bash
bnc --conf Example_Configs/RinexObs.bnc
# 批处理无窗示例（以包内脚本为准）：
# bnc --conf RinexObs.bnc --nw
```

### 3.3 可选：转发到本机 RTKLIB（仍不做 PPP）

1. 在 BNC 输出/转发页设 **TCP server** 端口，例 `2102`，格式 RTCM3。
2. 验证：`timeout 5 nc -v 127.0.0.1 2102 | wc -c` → 应 `>0`。
3. RTKLIB：`str2str` 或 RTKNAVI 订 `tcpcli://127.0.0.1:2102`。
4. **先**用落盘 RINEX 走 [rtklib](./rtklib.md) 事后冒烟，再接实时。

### 3.4 配置三层（避免“我改了怎么没生效”）

BNC 维护三层选项：

1. GUI 输入框  
2. **Start 之后**的活动配置  
3. 磁盘上的 `.bnc`

改完 GUI 必须 **Start** 才进入活动层；要持久化必须 **Save Options**。部分项支持 **Reread Configuration** 热加载（如 mountPoints、部分 sampling）——以帮助文档列表为准。

## 4. Log 行含义（操作向）

| Log 关键词 / 形态 | 含义 | 动作 |
| --- | --- | --- |
| `Connection established` | TCP/NTRIP 会话建立 | 继续看是否有消息号 |
| `401` / `Unauthorized` / `403` | 鉴权失败 | 改 user/pass；查账号流数限额 |
| `Get data timeout` / `Stream timeout` | 长时间无字节 | `nc -vz host 2101`；换网络；查维护公告 |
| `SSL` / `handshake failed` | TLS 失败 | 校时 NTP；查证书；试提供方非 TLS 端口 |
| `RTCM 1004` 等 | 传统观测消息 | 旧流仍见；确认是否你要的格式 |
| `RTCM 1074`–`1077` 等 | GPS MSM | 现代 CORS 常见 |
| `108x` / `109x` / `112x` | 其它星座 MSM | 多星座需求时核对 |
| `1005` / `1006` | 站坐标消息 | 基准信息 |
| `1057`–`1068` 等 SSR | 轨道钟差改正 | **仅当你故意订 SSR 时才需要**；录 OBS 可忽略 |
| 写盘 / `Disk` / write error | 磁盘满或权限 | 立刻 Stop；`df -h`；改 Directory 权限 |
| 挂载点占用 / concurrency | 账号并发上限 | 停其它客户端；换账号 |

消息号用于确认「连对了流」，不是 TEC 产品。

## 5. 输入 / 输出

| 输入 | 说明 |
| --- | --- |
| Caster host:port | 常见 2101 |
| mountpoint | 大小写敏感 |
| user/password | NTRIP 鉴权 |
| `.bnc` | 批处理入口 |

| 输出 | 下游 |
| --- | --- |
| RINEX OBS/NAV | [georinex](./georinex.md) / [gfzrnx](./gfzrnx.md) / [anubis](./anubis.md) / [pytecgg](./pytecgg.md) |
| 原始 RTCM 日志 | 回放/取证 |
| TCP 转发 | [rtklib](./rtklib.md) |
| Log | 本页第 4 节 |

## 6. 接到哪一步

| 场景 | 本页 | 下游 |
| --- | --- | --- |
| 录盘后一日 TEC | §3 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [pytecgg](./pytecgg.md) |
| 录盘后 ROTI | §3 | [oasis-roti](./oasis-roti.md) |
| 实时 RTK | §3.3 | [rtklib](./rtklib.md) |
| 脚本探活对比 | — | [pygnssutils](./pygnssutils.md) |
| 自建 caster | 不用 BNC 播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |

## 7. 坑（现象 → 原因 → 修复）

| # | 现象 | 原因 | 修复 |
| --- | --- | --- | --- |
| 1 | 源表空 | 防火墙/DNS/代理 | `nc -vz host 2101`；`getent hosts host`；填 Network 代理 |
| 2 | 401/403 | 口令错或无权限 | 改密；查并发限额；勿把口令贴聊天 |
| 3 | 有连接无文件 | RINEX Directory 未设或未 Start | 设 Directory；Save；Start；`ls -l` |
| 4 | 有字节无 RINEX 头 | 订错流（非观测）或解码失败 | 对源表 format 列；Log 看消息号 |
| 5 | 文件一直 0 字节 | 权限/只读 NFS | `touch /data/rinex/lab/t`；换本地盘 |
| 6 | 挂载点找不到 | 大小写/空格 | 从源表复制粘贴 |
| 7 | VRS 无数据 | 未送 NMEA 近似位置 | 按提供方要求开 NMEA/坐标 |
| 8 | 改了采样不生效 | 只改了 GUI 未进活动配置 | Stop → 改 → Save → Start；或 Reread |
| 9 | 无头与 GUI 行为不同 | conf 路径错/旧文件 | 绝对路径 `--conf`；`ls -l` conf mtime |
| 10 | 转发端口无数据 | 端口被占或未开转发 | `ss -ltnp | grep 2102`；检查转发页 |
| 11 | 磁盘写满 | 多站 1 Hz | `df -h`；加大 File interval 抽稀；减站 |
| 12 | Windows 休眠断流 | 电源策略 | 录制机禁止休眠 |
| 13 | 把 BNC 当 TEC 引擎 | 链选错 | 落盘后 [pytecgg](./pytecgg.md)（viventriglia） |
| 14 | 口令进了 git | conf 误提交 | `chmod 600`；gitignore；轮换口令 |

## 8. 选型

| 需求 | 选 |
| --- | --- |
| 多流 GUI 录盘/转发 | **BNC** |
| 一行命令拉一流 | **pygnssutils** |
| 自建播发 | **BKG NtripCaster** |
| 事后定位 | **RTKLIB / PRIDE-PPPAR** |

## 9. 相关

[pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · 教程 [06](../tutorials/06-iono-positioning.md)
