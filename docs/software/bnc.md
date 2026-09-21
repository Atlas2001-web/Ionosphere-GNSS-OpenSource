# BNC（BKG Ntrip Client）

目录：[`PROJECTS.json` → `BNC`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bnc> · FTP <https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/> · GPL-3.0

> 操作手册。祈使句。GUI 标签随版本微调；以你安装包的帮助 / PDF 为准。账号与口令禁止提交 git。

---

## 用途与边界

**用：**

- BKG 官方 **多流 NTRIP 客户端**（Qt GUI + 可批处理配置）。
- 订阅挂载点、解码 RTCM / SSR、**端口转发**、**落盘 RINEX / 原始流**、可选实时 PPP。
- 实验室 / 业务上同时盯多路 CORS、SSR、电台转 TCP 的默认重型客户端。

**不用 / 边界：**

- 轻量**脚本单流**拉流 → [pygnssutils](./pygnssutils.md)（`gnssntripclient` 等）。
- **自建播发** caster → [bkg-ntripcaster](./bkg-ntripcaster.md)。
- 事后校准 TEC / ROTI → 落盘后交给 [georinex](./georinex.md)/[pytecgg](./pytecgg.md)/[oasis-roti](./oasis-roti.md)。PyTECGg = **viventriglia**。
- 球谐 GIM 求解 → 非本工具；[sh-gim](./sh-gim.md) 仅边界说明。
- 把 BNC 当 QC PDF 工具 → [anubis](./anubis.md)。

一句话：BNC = **实时接入与录盘枢纽**；科学产品在落盘之后。

---

## 安装（多平台 + 报错）

### 获取二进制

1. 打开官网或 FTP 目录，选平台包（Linux AppImage/deb、Windows 安装包、macOS 视供应情况）。  
2. 校验下载大小；过小可能是 HTML 错误页。  
3. 阅读包内许可与 README。

### Linux

```bash
# AppImage 示例
chmod +x BNC-*.AppImage
./BNC-*.AppImage
# deb 示例
sudo dpkg -i bnc_*.deb || sudo apt -f install -y
# 缺 Qt 库时：
sudo apt install -y libqt5widgets5 libqt5network5 libqt5core5a
# 可执行名可能是 bnc / BNC；which 确认
command -v bnc || command -v BNC || echo "用 AppImage 路径启动"
```

无头服务器：先在有显示器的机器生成 `.bnc` 配置，再：

```bash
bnc --conf /opt/bnc/lab.bnc
# 或
./BNC-*.AppImage --conf /opt/bnc/lab.bnc
```

### Windows

1. 运行官方安装包。  
2. 开始菜单启动 BNC。  
3. 防火墙首次放行「专用网络」。  
4. 配置保存到用户目录；备份 `.bnc` 到加密盘，不要进公开仓库。

### macOS

按官网包说明安装；若缺 Qt，按包依赖文档处理。Gatekeeper 拦截时走系统「仍要打开」流程（单位策略优先）。

### 安装期常见报错

| 现象 | 处理 |
|---|---|
| AppImage 无法运行 | `chmod +x`；装 `fuse`/`libfuse2`（视发行版） |
| `error while loading shared libraries: libQt5*` | 装对应 Qt5 包 |
| GUI 闪退 | 查 OpenGL/远程 X11；先本地桌面 |
| 无头立刻退出 | 必须 `--conf`；先在 GUI 调通 |
| 杀毒误报 | 对照官方哈希；单位白名单 |
| 旧配置打不开 | 版本不兼容；用新版本 GUI 重建关键页 |

### 安装验收

```bash
# GUI：主窗口出现，菜单可点
# CLI：
bnc --help 2>&1 | head -n 20 || true
ls -l ~/bnc_configs/lab.bnc   # 你保存后的路径
```

---

## 快速冒烟（15 分钟）

1. **启动 GUI** → 主窗口可见。  
2. **Add Caster / 拉源表** → 填 host（常见端口 **2101**）→ 拉源表成功。  
3. **源表非空** → 能看到 mountpoint、格式、载波说明。  
4. **勾选一个公开/已授权挂载点** → Start。  
5. **Log** → 出现 `Connection established` 或持续 RTCM 消息号。  
6. **可选 RINEX 落盘** → 目标目录文件字节递增。  

```bash
# 无头复跑（配置已保存）
bnc --conf ~/bnc_configs/lab.bnc
# 另开终端
watch -n 2 'ls -l ~/rinex_out/ | tail'
```

**失败判据：** 源表空、401/403、长时间无字节、落盘 0 字节 —— 见坑节，先别开 PPP。

---

## 完整工作流

### 工作流 A：单站 OBS 落盘 → 事后 TEC / ROTI

对应索引路径 C → A；教程 [02](../tutorials/02-gnss-dualfreq-tec.md)/[16](../tutorials/16-practice-one-day-tec.md)。

```text
GUI:
  Caster 设定 → 选 mountpoint → RINEX 面板：目录、版本、采样
  → Start → 跑 ≥ 10 min
```

```bash
ls -lh ~/rinex_out/
head -n 8 ~/rinex_out/*.obs 2>/dev/null || head -n 8 ~/rinex_out/*.rnx
# 完整性
python -m georinex.gtime ~/rinex_out/YOURFILE.obs
# 下游
# gfzrnx / anubis / pytecgg / oasis-roti …
```

**期望：** RINEX 头合法；`gtime` 覆盖录制时段；字节随时间增。

### 工作流 B：端口转发 → RTKLIB 实时 RTK

```text
BNC: 输出 → TCP 端口（例 2102）转发 RTCM
RTKLIB: str2str / rtkrcv / RTKNAVI 订 localhost:2102
```

```bash
# 验证端口有数据（示例）
timeout 5 nc -v 127.0.0.1 2102 | wc -c
# >0 再开 rtkrcv
```

先事后文件 RTK 冒烟（[rtklib](./rtklib.md)），再接实时。

### 工作流 C：多流并行录盘（站点网）

1. 源表多选挂载点。  
2. 每流独立 RINEX 命名（含站名）。  
3. 磁盘配额：`df -h`；1 Hz 多站极易写满。  
4. 日志轮转：定期停-备-启或按手册设。  

```bash
du -sh ~/rinex_out
find ~/rinex_out -type f -size 0   # 应为空结果
```

### 工作流 D：SSR / 实时 PPP（可选）

1. 确认挂载点确为 SSR 且与客户端模式匹配。  
2. 先关 PPP，只验证 SSR 消息入 Log。  
3. 再开 PPP；轨迹乱跳 → 立即关，查龄期与产品。  
4. 科研精密坐标仍走事后 [pride-pppar](./pride-pppar.md)。

### 工作流 E：配置即代码（无头批处理）

```bash
mkdir -p ~/bnc_configs /var/log/bnc
# GUI 调通后 Save As ~/bnc_configs/lab.bnc
bnc --conf /home/$USER/bnc_configs/lab.bnc >> /var/log/bnc/lab.log 2>&1 &
echo $! > /var/run/user/$UID/bnc_lab.pid
# 停止
kill $(cat /var/run/user/$UID/bnc_lab.pid)
```

systemd 单元自行编写时：`Restart=on-failure`；`WorkingDirectory` 指向可写录盘目录。

### 工作流 F：与 pygnssutils 交叉探活

```bash
# 源表 / 单流不通时
gnssntripclient -h 2>/dev/null | head
# 用同一 caster host:port 与挂载点做独立客户端验证
# 若 pygnssutils 通而 BNC 不通 → 查 BNC 代理/SSL/配置；反之查脚本 URL
```

---

## 输入 / 输出与字段表

### 输入

| 项 | 说明 |
|---|---|
| Caster host/port | 常见 2101；TLS 按提供方 |
| mountpoint | 大小写敏感 |
| user/password | NTRIP 鉴权；匿名视源而定 |
| 串口 / TCP | 本地接收机接入（若启用） |
| `.bnc` 配置 | 批处理入口 |

### 输出

| 产物 | 说明 | 下游 |
|---|---|---|
| 实时解码日志 | 消息号、状态 | 排障 |
| RINEX OBS/NAV | 落盘 | georinex / gfzrnx / anubis / pytecgg |
| 原始 RTCM 日志 | 可选 | 回放 / 取证 |
| TCP/串口转发 | 实时 | RTKLIB |
| PPP 轨迹 | 可选 | 仅作粗看 |

### Log 字段（示意，随版本）

| 关键词 | 含义 | 动作 |
|---|---|---|
| Connection established | 链路通 | 继续看消息 |
| 401/403 | 鉴权失败 | 改口令/权限 |
| Get data timeout | 静默 | 查网络/挂载点 |
| RTCM 1004/1077/… | 消息类型 | 确认是否需要的 MSM/SSR |
| SSL error | TLS | 证书/时间/旗标 |

---

## 常用参数 / GUI 关键页

| 页 / 项 | 操作要点 |
|---|---|
| Network / Caster | host、port、代理、SSL |
| Mountpoints | 勾选、用户名密码、NMEA 若需 VRS |
| RINEX | 目录、版本 2/3、采样、文件切片 |
| Outages | 断流告警阈值 |
| PPP | 无 SSR 保持关 |
| Miscellaneous | 日志路径、自动启动 |
| `--conf` | 无头加载 |

命令行旗标以 `--help` 为准；不要假设所有平台包都暴露相同 CLI。

---

## 接到 tutorials / 工作流哪一步

| 场景 | 位置 | 链接 |
|---|---|---|
| 实时差分 / 实验室 CORS | 工作流 B | [rtklib](./rtklib.md) · 索引路径 C |
| 录盘后一日 TEC | A | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) · [pytecgg](./pytecgg.md) |
| 录盘后 ROTI | A | [05](../tutorials/05-scintillation-roti.md) |
| 自建 caster | 不用 BNC 播发 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 脚本探活 | F | [pygnssutils](./pygnssutils.md) |
| 定位受扰动 | 实时固定率 + ROTI | [06](../tutorials/06-iono-positioning.md) |

---

## 可操作坑（≥12）

1. **源表空当「没站」** — 先查防火墙、DNS、代理；用 `nc -vz host 2101`。  
2. **401/403 反复试密码写进聊天记录** — 改密；用本地密管。  
3. **有字节无解码** — 挂载点格式与期望不符；换 MSM / 传统 RTCM。  
4. **PPP 乱跳却猛调模糊度** — 先关 PPP，查 SSR 龄期。  
5. **1 Hz 多站写满磁盘** — 监控 `df`；降采样或切片。  
6. **配置丢失** — 定期备份 `.bnc`；无头用绝对路径。  
7. **VRS 未送 NMEA** — 近端近似坐标按提供方要求配置。  
8. **TLS 时间错** — NTP 同步系统钟。  
9. **只开 GUI 演示未落盘** — 事后无文件可复现；录盘开关要开。  
10. **转发端口被占用** — `ss -ltnp | grep 2102`。  
11. **把 BNC 当 TEC 引擎** — 错；落盘后换 pytecgg（viventriglia）。  
12. **挂载点大小写错误** — 精确复制源表。  
13. **公司代理仅 GUI 通 CLI 不通** — 统一环境变量 `http_proxy`。  
14. **Windows 休眠断流** — 电源策略「永不休眠」于录制机。  
15. **录制中改配置未保存** — Save 后再 Restart。  
16. **合规** — 遵守数据提供方 ToS；勿对外二次播发除非获授权。

---

## 同类选型

| 需求 | 选 |
|---|---|
| 多流 GUI、录盘、转发 | **BNC** |
| 一行命令拉一流 | **pygnssutils** |
| 自建播发 | **BKG NtripCaster** |
| 事后定位 | **RTKLIB / PRIDE-PPPAR** |
| 事后 TEC | **pytecgg** |

---

## 操作检查清单

1. GUI 可启动或 `--conf` 可跑。  
2. 源表非空。  
3. Log 有连接与消息号。  
4. 落盘字节递增且 `head` 为 RINEX。  
5. 转发端口可被本机客户端连接。  
6. 无 SSR 时 PPP 关闭。  
7. `.bnc` 已备份且密钥未入 git。  
8. 磁盘与时间同步正常。  
9. 交叉工具探活做过一次。  
10. 下游工具已用样例文件冒烟。

---

## 附录 A · 期望 I/O

| 步骤 | 期望 |
|---|---|
| 拉源表 | 文本行含 mountpoint |
| 订阅 60 s | 日志持续刷新 |
| RINEX 落盘 | 大小 > 0 且递增 |
| 鉴权失败 | 明确 401/403 |
| 转发 | `nc` 收到字节 |

---

## 附录 B · 网络探活命令

```bash
nc -vz caster.example.org 2101
curl -I --max-time 10 http://caster.example.org:2101/   # 视服务而定
# DNS
getent hosts caster.example.org
# 本机出口
curl -s ifconfig.me; echo
```

---

## 附录 C · RINEX 落盘后质检

```bash
find ~/rinex_out -type f -name '*.obs' -o -name '*.rnx' | while read f; do
  echo "== $f"
  head -n 3 "$f"
  python -m georinex.gtime "$f" 2>/dev/null || true
done
```

---

## 附录 D · systemd 单元示意

```ini
[Unit]
Description=BNC lab recorder
After=network-online.target

[Service]
Type=simple
User=gnss
ExecStart=/usr/local/bin/bnc --conf /opt/bnc/lab.bnc
Restart=on-failure
WorkingDirectory=/data/bnc

[Install]
WantedBy=multi-user.target
```

路径按实机改；先前台跑通再装服务。

---

## 附录 E · 与 RTKLIB 对接检查表

| 项 | 值 |
|---|---|
| BNC 出端口 | 2102 |
| 格式 | RTCM3 |
| RTKLIB 入 | `tcpcli://127.0.0.1:2102` 或等价 |
| 事后对照文件 | 同时段落盘 RINEX |

---

## 附录 F · 故障记录模板

```text
time_utc:
caster:
mount:
bnc_version:
symptom:
log_excerpt:
network_probe:
action:
result:
```

---

## 附录 G · 安全

- `.bnc` 含口令 → 权限 `chmod 600`。  
- 不要把口令写进教程截图。  
- 共享配置前用占位符替换密钥。  
- 公共 Wi-Fi 慎用明文 NTRIP。

---

## 附录 H · 何时不用 BNC

- CI 里拉一次流验证 → pygnssutils。  
- 只做事后 CDDIS 文件 → 直接 data-access，不经 BNC。  
- 需要 caster 服务端 → ntripcaster。

---

## 附录 I · 多日录制运维

```bash
# 每日 00:05 打包前一日
0 0 * * * /usr/local/bin/bnc_rotate.sh
# rotate 脚本：停 BNC → mv 目录 → 启 BNC → 上传/校验
```

先手动演练再 cron。

---

## 附录 J · 版本与文档

- 保留安装包文件名与版本号在 `logs/bnc_version.txt`。  
- 升级前导出配置；升级后重拉源表验证。  
- 许可：GPL-3.0；商业数据流另遵 ToS。

---

## 附录 K · 相关工具

[pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md)


---

## 附录 L · 逐步：从零到第一份 RINEX

1. 安装并启动 BNC。  
2. 新建配置 `lab_first.bnc`。  
3. 输入 caster：`host`、`2101`。  
4. 拉源表；搜索目标站关键字。  
5. 勾选挂载点；填 user/password（若需要）。  
6. RINEX 页：目录 `/data/rinex/first`，版本 3，采样 1 或 30。  
7. Start；盯 Log 120 秒。  
8. `ls -l /data/rinex/first` 确认非 0。  
9. `head` + `georinex.gtime`。  
10. Save 配置；复制到备份盘。  
11. Stop；再 `--conf` 无头启动一次验证。  
12. 将样例文件送入 [gfzrnx](./gfzrnx.md) `-chk`。

---

## 附录 M · 消息号速查（操作向）

| 类型族 | 含义 | 录盘/RTK 含义 |
|---|---|---|
| 1004 等 | 传统 GPS 观测 | 旧流仍见 |
| 1074–1077 等 | MSM GPS | 现代 CORS 常见 |
| 108x/109x/112x | 其它星座 MSM | 多星座 RTK |
| 1057–1068 等 | SSR 轨道钟差等 | 实时 PPP 相关 |
| 1005/1006 | 站坐标 | 基准信息 |

具体编号以 RTCM 标准与源表说明为准；Log 里出现的号用于确认「连对了流」。

---

## 附录 N · 磁盘与采样估算

```text
粗估：单站双频 1 Hz RINEX ≈ 数十 MB/小时量级（随星座/字段变化）
8 站 × 1 Hz × 24 h → 数 GB 级；预留 3× 余量
```

```bash
df -h /data
du -sh /data/rinex
```

超阈：降采样、减站、或只转发不落盘。

---

## 附录 O · 代理环境变量

```bash
export http_proxy=http://proxy.example:8080
export https_proxy=http://proxy.example:8080
export no_proxy=localhost,127.0.0.1
bnc --conf ~/bnc_configs/lab.bnc
```

GUI 内代理页与环境变量勿冲突；改一处后重启客户端。

---

## 附录 P · 验收表（给运维签字）

| 项 | 结果 | 签字 |
|---|---|---|
| 版本已记录 | | |
| 源表成功 | | |
| 60 s 连续解码 | | |
| 落盘非 0 | | |
| gtime 覆盖 | | |
| 密钥未入 git | | |
| 磁盘余量 > 30% | | |
| 无头 `--conf` 成功 | | |

---

## 附录 Q · 与索引路径 C 的对照

```text
pygnssutils 或 BNC → (可选 bkg-ntripcaster) → rtklib
落盘 → georinex / anubis → TEC 或 ROTI（路径 A/B）
```

本页负责「BNC 节点」；上下游手册各自验收。

---

## 附录 R · 常见 Log 一行处理

```text
"Connection established" → 进入观察消息号阶段
"Stream timeout" → ping/nc；换网络；查 caster 维护公告
"SSL handshake failed" → 时间同步；证书；试非 TLS 端口（若提供）
"Mountpoint taken" / 占用类 → 账号并发限制；换账号或停其它客户端
"Disk full" / write error → 立刻 Stop；清盘
```

---

## 附录 S · 相关工具（复述）

[pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [gfzrnx](./gfzrnx.md) · [anubis](./anubis.md) · [pytecgg](./pytecgg.md) · [oasis-roti](./oasis-roti.md)


---

## 附录 T · 命令与点击对照

| 目标 | GUI | CLI / shell |
|---|---|---|
| 启动 | 图标 | `bnc --conf …` |
| 拉源表 | Add Caster → Get | （GUI 完成写入 conf） |
| 开始 | Start | 进程保持运行 |
| 停 | Stop | `kill $(pid)` |
| 看流量 | Log 窗 | `tail -f log` + `ls -l` |
| 验证 RINEX | 文件管理器 | `head` + `georinex.gtime` |

---

## 附录 U · 一页纸验收

1. 安装包版本写入 `logs/bnc_version.txt`。  
2. 源表非空截图或文本保存。  
3. 60 s 解码无长静默。  
4. 落盘文件 `wc -c` > 0。  
5. `georinex.gtime` 成功。  
6. `.bnc` 权限 600 且不在 git。  
7. 转发端口（若用）`nc` 有字节。  
8. PPP 默认关。  
9. 下游 RTKLIB 或 TEC 链冒烟一次。  
10. 磁盘余量检查通过。

完成即宣布「BNC 节点就绪」。


---

## 附录 V · 实验室一次课流程（40 分钟）

| 分钟 | 动作 |
|---|---|
| 0–5 | 启动 BNC，加载课前发的 conf（口令现场填） |
| 5–10 | 拉源表，确认挂载点 |
| 10–25 | 录盘；同时 `watch ls` |
| 25–30 | Stop；`georinex.gtime` |
| 30–40 | 可选：`rnx2rtkp` SPP 或交卷文件 |

教师机提前验证 caster 可达；学生网络勿拦 2101。

---

## 附录 W · 不要做的事

- 不要在无授权下二次广播差分流。  
- 不要把实时 PPP 轨迹当发表坐标。  
- 不要假设所有公开挂载点永久免费匿名。  
- 不要在文档里写真实口令。  
- 不要跳过落盘质检直接跑全日 TEC。


---

## 附录 X · 帮助与上游

- 官网帮助 PDF / 版本说明：随安装包。  
- 问题排查顺序：网络 → 鉴权 → 挂载点 → 磁盘 → 下游。  
- 参数冲突：**以本机帮助为准**。  
- 上游变更后更新本页示例旗标。

**相关工具：** [pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md) · [pytecgg](./pytecgg.md)
