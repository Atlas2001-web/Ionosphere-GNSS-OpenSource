# BNC（BKG Ntrip Client）

目录：[`PROJECTS.json` → `BNC`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bnc> · FTP <https://igs.bkg.bund.de/root_ftp/NTRIP/software/BNC/> · GPL-3.0

## 用途

- BKG 官方 **多流 NTRIP 客户端**（Qt GUI + 批处理）。
- 订阅挂载点、解码 RTCM/SSR、端口转发、落盘 RINEX、可选实时 PPP。
- 轻量单流脚本 → [pygnssutils](./pygnssutils.md)；自建播发 → [bkg-ntripcaster](./bkg-ntripcaster.md)。

## 安装

1. 从官网/FTP 取平台包（Linux AppImage/deb、Windows 安装包等）。
2. Linux 注意 Qt 依赖；启动 GUI 出现主窗口即成功。
3. GUI 调通后保存配置，无头批处理：

```bash
bnc --help 2>/dev/null || echo "用官方入口启动 GUI"
bnc --conf /path/to/my.bnc
```

公共 caster 或可匿名；CORS/商业流自备账号。遵守数据提供方条款。

## 快速上手

1. **Add Caster / 拉源表** → 看到 mountpoint 列表。
2. **勾选挂载点** → Log 出现 `Connection established` / RTCM 消息号。
3. **RINEX 落盘**（可选）→ 目标目录文件字节递增。
4. **端口转发**（可选）→ 供 RTKLIB `str2str`/`rtkrcv`。
5. **实时 PPP**（可选）→ 需匹配 SSR；失败时先关 PPP，只验证拉流。

```bash
bnc --conf ~/bnc/lab.bnc
ls -l ~/rinex_out/
```

**预期：** 源表非空；有解码日志；落盘非 0 字节。源表空/401 = 网络或账号问题。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | Caster、mountpoint、口令；可选串口/TCP |
| 输出 | 实时流、转发端口、RINEX/原始日志、可选 PPP 轨迹 |
| 不做 | 事后校准 TEC/ROTI（落盘后交给其他工具） |

## 常用参数

GUI 为主。关键项：Caster host/port（常见 2101）、Mountpoints、RINEX 目录与版本、Outages/SSL、PPP（无 SSR 勿开）、`--conf`。

## 接到工作流哪一步

- 路径 C：拉流 → 落盘 → [georinex](./georinex.md)/[anubis](./anubis.md) → TEC/ROTI 或 [rtklib](./rtklib.md)
- 实验室小 caster：[pygnssutils](./pygnssutils.md)
- 生产播发：[bkg-ntripcaster](./bkg-ntripcaster.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 源表空 | 防火墙/主机；用 `gnssntripclient` 交叉探活 |
| 401/403 | 口令或挂载点权限 |
| 有字节无解码 | 消息号不符；换挂载点 |
| PPP 乱跳 | 无 SSR/龄期大；先关 PPP |
| 只要脚本拉一流 | [pygnssutils](./pygnssutils.md) |
| 配置丢失 | 备份 `.bnc`；无头模式用绝对路径 |

## 相关工具

[pygnssutils](./pygnssutils.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) · [rtklib](./rtklib.md) · [georinex](./georinex.md)

## 操作检查清单

1. GUI 能打开主窗口。  
2. 源表非空且含目标挂载点。  
3. Log 出现 RTCM 消息号（或明确的解码错误）。  
4. 若落盘：目标文件字节随时间增加。  
5. 若转发：本机端口可被 `str2str`/`rtkrcv` 连上。  
6. 无 SSR 时 PPP 开关保持关闭。  
7. 备份 `.bnc` 配置到版本库外安全位置。

## 预期 I/O 示例

| 步骤 | 期望 |
|---|---|
| 拉源表 | 文本行含 mountpoint、格式、载波 |
| 订阅 60 s | 日志持续刷新；无长时间静默 |
| RINEX 落盘 | `.obs`/`.rnx` 大小 > 0 且递增 |
| 鉴权失败 | 401/403，不应假装有数据 |

## 操作检查清单

1. 安装/编译后，帮助命令（`-h`/`-H`/`--help`）可运行。  
2. 用官方 example 或最小样例跑通，再换自己的数据。  
3. 确认输入时间覆盖、路径、权限。  
4. 保留日志；失败时只改一个变量重试。  
5. 参数以本机帮助/上游 README 为准（本文可能滞后）。  
6. 产出文件非空且时间戳更新。  
7. 接到下一工具前做格式抽查（`head`/`wc`/`grep`）。

## 预期 I/O 速查

| 阶段 | 成功判据 |
|---|---|
| 安装 | 可执行文件或 `import` 成功 |
| 冒烟 | example 退出码 0 或生成预期文件 |
| 正式跑 | 输出目录有目标产品且体量合理 |
| 失败 | 日志指出缺文件/鉴权/覆盖问题，而非静默空结果 |
