# BKG NtripCaster · 专业 NTRIP 播发操作手册

目录：[`PROJECTS.json` → `BKG-NtripCaster`](../../PROJECTS.json) · 官网 <https://igs.bkg.bund.de/ntrip/bkgcaster> · 总览 <https://igs.bkg.bund.de/ntrip/index> · FTP：`NTRIP/software/NtripCaster/` · GPL

> 面向 **Linux 上多客户端 NTRIP v1/v2 播发** 的岗位。只做流分发与鉴权，不解码内容，不做 VRS。参数以包内手册与 `*.dist` 注释为准。

## 1. 用途与边界

### 1.1 一句话

BKG Professional NtripCaster 让你在实验室/课程/小型 CORS 场景成为 NTRIP 播发站：源表、用户组、挂载点 ACL、中继。

### 1.2 应该用

- 多用户、多挂载点播发
- 中继远端流到本地挂载点
- 与 BNC / RTKLIB / 手簿联调

### 1.3 不应该用

- 五分钟单挂载点演示 → [pygnssutils](./pygnssutils.md) `gnssserver`
- 多流 GUI 收流/录 RINEX → [bnc](./bnc.md)
- TEC/ROTI/PPP 计算
- 指望 Caster「自动选最近基站 / VRS」

### 1.4 与电离层工作的关系

Caster 解决「实时流怎么播」；科研产品仍在落盘转 RINEX 之后（路径 A/B）。

## 2. 多平台安装

### 2.1 要求

- **仅 Linux**（以官网为准）
- 编译链：`configure` / `make`
- 配置文件必须是 **LF**（禁止记事本 CRLF）

### 2.2 编译安装

```bash
# 从 BKG FTP 下载 ntripcaster-*.tar.bz2（版本以目录为准）
bunzip2 ntripcaster-*.tar.bz2 && tar xf ntripcaster-*.tar
cd ntripcaster-*
./configure --prefix=$HOME/ntripcaster
make -j"$(nproc)"
make install
```

### 2.3 配置落地

```bash
CONF=$HOME/ntripcaster/conf   # 以实际布局为准
cd "$CONF"
for f in ntripcaster.conf sourcetable.dat users.aut groups.aut clientmounts.aut sourcemounts.aut; do
  test -f ${f}.dist && cp ${f}.dist $f
done
dos2unix ntripcaster.conf sourcetable.dat *.aut 2>/dev/null || true
chmod 600 users.aut groups.aut *.aut
```

### 2.4 报错表

| 现象 | 处理 |
| --- | --- |
| configure 缺库 | 按 README 装依赖 |
| CRLF 怪错 | dos2unix |
| 端口占用 | `ss -lptn | grep 2101` |
| 权限 | 非 root 家目录安装；防火墙 |

## 3. 完整逐步命令与期望输出

### 3.1 编辑 conf

```bash
# ntripcaster.conf：port（常 2101）、日志路径、max 连接
grep -E 'port|log|max' ntripcaster.conf | head
```

### 3.2 源表最小 STR 行

按手册列序添加挂载点；字段少一个就会「源表怪」或客户端解析失败。

### 3.3 账号与 ACL

```text
users.aut:     user:password
groups.aut:    group:user1,user2
clientmounts.aut / sourcemounts.aut: 挂载点读写权限
```

### 3.4 启动与探活

```bash
./ntripcaster start
./ntripcaster status 2>/dev/null || true
gnssntripclient --server 127.0.0.1 --port 2101 --verbosity 2 | tee logs/sourcetable.txt
```

**期望：** 进程在；源表有 STR；授权用户可订；未授权拒绝。

### 3.5 客户端订流

```bash
gnssntripclient --server 127.0.0.1 --port 2101 --mountpoint LOCAL1 \
  --ntripuser lab --ntrippassword 'strong' --datatype RTCM --verbosity 2
```

### 3.6 中继（语法以手册为准）

```bash
# 示意
relay pull -i user:pass -m /LOCAL1 remote.example:2101/REMOTE0
```

### 3.7 停止/重启

```bash
./ntripcaster stop
./ntripcaster restart
```

改 ACL 后不要假设一定热更新——以 status/日志为准。

### 3.8 与源端推流联调

源端用 BKG `ntripserver`、接收机 NTRIP server、或其它推流工具；Caster 侧 `sourcemounts.aut` 必须允许该源账号。

### 3.9 教学：与 pygnssutils 对照

| 步骤 | 工具 |
| --- | --- |
| 5 分钟本机 | gnssserver |
| 多人 ACL/中继 | **本 Caster** |

## 4. 参数与文件字段表

| 文件 | 作用 |
| --- | --- |
| `ntripcaster.conf` | 端口、连接数、日志 |
| `sourcetable.dat` | 源表 STR/CAS/NET |
| `users.aut` / `groups.aut` | 账号 |
| `clientmounts.aut` | 客户端 ACL |
| `sourcemounts.aut` | 源端 ACL |

### 输入 / 输出

| 方向 | 内容 |
| --- | --- |
| 输入 | 上游 NTRIP/TCP、本地推流 |
| 输出 | NTRIP 服务、源表、日志 |
| 不做 | 解码、VRS、TEC |

## 5. 接到电离层 / GNSS 哪一步

路径 C 播发端；客户端用 pygnssutils/BNC/RTKLIB；落盘科研回 A/B。

## 5b. 链接表

| 场景 | 链接 |
| --- | --- |
| 索引 | [README](./README.md) |
| 数据 | [data-access](../data-access.md) |
| 读盘 | [georinex](./georinex.md) |
| 清洗 | [gfzrnx](./gfzrnx.md) |
| QC | [anubis](./anubis.md) |
| TEC | [pytecgg](./pytecgg.md) |
| ROTI | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| GIM | [ionex-gim](./ionex-gim.md) · [sh-gim](./sh-gim.md) |
| 实时 | [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 定位 | [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) |
| 闪烁仿真 | [iono-scintillation](./iono-scintillation.md) |
| 课 02/16 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 课 05/13/21 | [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 课 06/20 | [06](../tutorials/06-iono-positioning.md) · [20](../tutorials/20-storm-tec-analysis.md) |
| 课 03/10/18 | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 课 09 | [09](../tutorials/09-dcb-biases-deep.md) |


## 6. 可操作坑（≥12）

1. 源表空 — sourcetable 未部署或 STR 格式错。
2. 能连不能订 — clientmounts ACL。
3. CRLF — dos2unix。
4. 2101 冲突 — 与 gnssserver/BNC 错开。
5. 单挂载点演示却上全套 — 换 pygnssutils。
6. 公网默认口令 — 立即被扫。
7. 口令文件世界可读 — chmod 600。
8. 挂载点名与源表不一致 — 字符级核对。
9. 以为会做 VRS — 不会。
10. 日志盘满 — logrotate。
11. IPv4/IPv6 混绑 — 客户端连错。
12. 未保存就 restart — 先写盘。
13. 源端未推流却怪客户端 — 先看源。
14. 防火墙未放行 — 放行端口。
15. 教学口令不轮换 — 课后改密。
16. 播发成功≠RTCM 内容正确 — 内容另验。

## 7. 同类怎么选

| 需求 | 选 |
| --- | --- |
| 正式多用户播发 | **BKG NtripCaster** |
| 脚本单挂载点 | pygnssutils |
| 收流录盘 | BNC |
| 容器化 | 社区 Docker（仍遵 BKG 许可） |

## 8. 场景卡片

### 实验室 CORS
局域网白名单 + 强口令 + 双挂载点（基站 MSM + 测试）。

### 课程
临时账号按日轮换；结束后 stop。

### 中继教研
pull 远端公开流到本地挂载点，供无外网学生机订阅。

## 9. 安全基线

- 默认拒公网；必须公网则 IP 白名单 + 强口令 + 监控失败登录
- TLS 按手册评估
- RTCM 可能含近似坐标——按数据政策

## 10. 命令一页纸

```bash
./ntripcaster start|stop|restart|status
gnssntripclient --server 127.0.0.1 --port 2101 --verbosity 2
dos2unix *.conf *.dat *.aut
```

## 11. 端到端剧本

安装 → 复制 dist → 改 conf/源表/账号 → start → 拉源表 → 订流 → 故意错误口令验证拒绝 → 记录。

## 12. 日志关键字

| 关键字 | 处置 |
| --- | --- |
| bind / address in use | 换端口 |
| auth fail | 账号/ACL |
| sourcetable | 行格式 |

## 13. sourcetable 概念

STR/CAS/NET；严格按手册列序；经纬度为挂载点大致位置。

## 14. 与客户端契约

| 客户端 | 用途 |
| --- | --- |
| gnssntripclient | 脚本探活 |
| BNC | 多流运维 |
| RTKLIB str2str | 管道 |
| 手簿 | 外业 |

## 15. 合规

GPL；公网服务另遵单位网络安全规定。

## 16. 快速失败矩阵

| 症状 | 先查 |
| --- | --- |
| 命令找不到 | PATH/venv/编译产物 |
| 空输出 | 时间覆盖/过滤/模式 |
| 鉴权失败 | 口令/ACL |
| OOM | 切窗/抽稀/降并行 |
| NaN 全日 | 双频/弧段/星历 |
| 与文献差一个量级 | 窗口/单位/时间系 |

## 17. 移交与复现信息模板

```text
DATE / HOST / TOOL_VERSION / CMD(口令打码) / INPUT_SHA256 / CONFIG / LOG / OK|FAIL / NEXT_TOOL / NOTES
```

## 18. 接到本仓库其它页的检查表

- [ ] 边界已读
- [ ] 安装验收
- [ ] 冒烟通过
- [ ] 日志保留
- [ ] 产出非空
- [ ] 下游已选定
- [ ] 版本入笔记
- [ ] 无越界解读


| 场景 | 链接 |
| --- | --- |
| 索引 | [README](./README.md) |
| 数据 | [data-access](../data-access.md) |
| 读盘 | [georinex](./georinex.md) |
| 清洗 | [gfzrnx](./gfzrnx.md) |
| QC | [anubis](./anubis.md) |
| TEC | [pytecgg](./pytecgg.md) |
| ROTI | [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) |
| GIM | [ionex-gim](./ionex-gim.md) · [sh-gim](./sh-gim.md) |
| 实时 | [pygnssutils](./pygnssutils.md) · [bnc](./bnc.md) · [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 定位 | [rtklib](./rtklib.md) · [pride-pppar](./pride-pppar.md) |
| 闪烁仿真 | [iono-scintillation](./iono-scintillation.md) |
| 课 02/16 | [02](../tutorials/02-gnss-dualfreq-tec.md) · [16](../tutorials/16-practice-one-day-tec.md) |
| 课 05/13/21 | [05](../tutorials/05-scintillation-roti.md) · [13](../tutorials/13-scintillation-modeling.md) · [21](../tutorials/21-equatorial-anomaly-bubbles.md) |
| 课 06/20 | [06](../tutorials/06-iono-positioning.md) · [20](../tutorials/20-storm-tec-analysis.md) |
| 课 03/10/18 | [03](../tutorials/03-gim-ionex.md) · [10](../tutorials/10-build-gim-workflow.md) · [18](../tutorials/18-lab-compare-gims.md) |
| 课 09 | [09](../tutorials/09-dcb-biases-deep.md) |


## 19. 逐步扩写：30 分钟必做

见第 3 节主流程；此处强调：**只改一个变量** 完成一次成功跑通，再批量。

## 20. 场景卡片（扩）

| 卡片 | 动作 |
| --- | --- |
| 新数据首日 | 冒烟 → 门禁 → 科学 |
| 事件日 | 先 QC/完整性再解释物理 |
| 教学 | example → 故意失败 → 修复 |
| 交付 | 复现包 + 版本号 |

## 21. 配方表

| 目标 | 配方 |
| --- | --- |
| 最快验证安装 | 帮助命令 + example |
| 最快验证数据 | head + gtime + 本工具最小窗 |
| 生产批 | 金样配置 + 日批脚本 + 汇总 CSV |

## 22. 输入抽样

```bash
ls -la data/; head -n 20 data/* 2>/dev/null | head -n 40
file data/* 2>/dev/null | head
gunzip -t data/*.gz 2>/dev/null || true
python -m georinex.gtime data/SITE.obs 2>/dev/null || true
```

## 23. 输出验收

- [ ] 文件存在且 size 合理
- [ ] 日志无未处理 FATAL
- [ ] 关键字段抽查
- [ ] 时间覆盖符合任务
- [ ] 命令与版本已记录

## 24. 上下游契约

| 上游 | 本工具 | 下游 |
| --- | --- | --- |
| RINEX/流/配置 | 主流程 | 下一手册 |
| Anubis | 可选门禁 | 科学计算 |
| gfzrnx | 可选清洗 | 同左 |

## 25. 故障树

```text
失败 → 安装/PATH → 输入完整性 → 配置旗标 → 权限磁盘 → 网络鉴权 → 算法窗/采样
```

## 26. 日批模板

```bash
#!/usr/bin/env bash
set -euo pipefail
DAY=$1
mkdir -p logs out/$DAY
# 填本工具命令
echo "$DAY $(date -Is)" >> logs/batch_index.txt
```

## 27. 教学口述提纲

边界 → 安装 → 样例 → 故意失败 → 输出关键字 → 下一工具。

## 28. 资源

| 项 | 建议 |
| --- | --- |
| 并行 | 2～4 起测 |
| 1 Hz | 先抽稀 |
| 磁盘 | 预留 2× |

## 29. 升级 checklist

读 Release → 备份配置 → 重装 → 回归 → diff 帮助 → 更新包装脚本 → 记版本。

## 30. 习惯 40 条（节选）

先 which；先 head；先 gunzip -t；先小窗；先单站；先单系统；先默认；先 example；先日志；先备份；先绝对路径；先 df；先 QC；先 gtime；先时间系；先观测码名；先双频成对；先 SP3 同日；先 NAV 覆盖；先 ENV 口令；先环回 NTRIP；先改默认口令；先防火墙；先 lite；先 float；先 LICENSE；先版本号；先声明窗口；先抽查图；先小文件测脚本；先核 DOY；先核站名；先核采样；先核截止角；先核薄壳高；先核参考坐标；先核 ANTEX；先核 RINEX 版本；先排除 HTML；先确认边界。

## 31. 期望 I/O 总表

| 阶段 | 成功 | 失败 |
| --- | --- | --- |
| 安装 | 帮助/import OK | not found |
| 冒烟 | 产物非空 | 空/报错 |
| 正式 | 字段齐全 | 静默空结果 |

## 32. 禁止清单

相对 TEC≠绝对；ROTI≠S4；QC≠科学正确；残差≠STEC；SH-GIM 公开仓≠完整求解；Free≠Pro。

## 33. 参数冲突裁决

本机帮助 > 上游 README > 本手册 > 过期博客。

## A1. 操作时间盒（番茄钟）

25 min 安装验收；25 min example；25 min 自备数据；15 min 写复现包。

### A1.1 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 1 个假设

### A1.2 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 2 个假设

### A1.3 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 3 个假设

### A1.4 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 4 个假设

### A1.5 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 5 个假设

### A1.6 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 6 个假设

### A1.7 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 7 个假设

### A1.8 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 8 个假设

### A1.9 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 9 个假设

### A1.10 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 10 个假设

### A1.11 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 11 个假设

### A1.12 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 12 个假设

### A1.13 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 13 个假设

### A1.14 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 14 个假设

### A1.15 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 15 个假设

### A1.16 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 16 个假设

### A1.17 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 17 个假设

### A1.18 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 18 个假设

### A1.19 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 19 个假设

### A1.20 检查点

- 命令可复述
- 日志路径已知
- 失败时回到第 20 个假设

## A2. 输入/输出矩阵（扩）

| # | 输入 | 变换 | 输出 | 验收 |
| --- | --- | --- | --- | --- |

| 1 | 数据/配置 1 | 本工具步骤 1 | 产物 1 | size>0 + 关键字 |

| 2 | 数据/配置 2 | 本工具步骤 2 | 产物 2 | size>0 + 关键字 |

| 3 | 数据/配置 3 | 本工具步骤 3 | 产物 3 | size>0 + 关键字 |

| 4 | 数据/配置 4 | 本工具步骤 4 | 产物 4 | size>0 + 关键字 |

| 5 | 数据/配置 5 | 本工具步骤 5 | 产物 5 | size>0 + 关键字 |

| 6 | 数据/配置 6 | 本工具步骤 6 | 产物 6 | size>0 + 关键字 |

| 7 | 数据/配置 7 | 本工具步骤 7 | 产物 7 | size>0 + 关键字 |

| 8 | 数据/配置 8 | 本工具步骤 8 | 产物 8 | size>0 + 关键字 |

| 9 | 数据/配置 9 | 本工具步骤 9 | 产物 9 | size>0 + 关键字 |

| 10 | 数据/配置 10 | 本工具步骤 10 | 产物 10 | size>0 + 关键字 |

| 11 | 数据/配置 11 | 本工具步骤 11 | 产物 11 | size>0 + 关键字 |

| 12 | 数据/配置 12 | 本工具步骤 12 | 产物 12 | size>0 + 关键字 |

| 13 | 数据/配置 13 | 本工具步骤 13 | 产物 13 | size>0 + 关键字 |

| 14 | 数据/配置 14 | 本工具步骤 14 | 产物 14 | size>0 + 关键字 |

| 15 | 数据/配置 15 | 本工具步骤 15 | 产物 15 | size>0 + 关键字 |


## A3. 命令备忘录（复制区）

```bash
# 记录你的真实命令
# CMD1=
# CMD2=
# CMD3=
```


## A4. 对照实验设计

| 实验 | 变量 | 对照组 | 观测量 |
| --- | --- | --- | --- |
| E1 | 采样 | 1 Hz vs 30 s | 产物稳定性 |
| E2 | 系统 | G vs GREC | 完整性 |
| E3 | 窗口 | 默认 vs 加严 | 弧段数 |
| E4 | 截止角 | 10 vs 20 | 噪声 |
| E5 | 时间窗 | 全日 vs 事件窗 | 峰值对齐 |


## A5. 交付给同事的一页纸

1. 工具与版本
2. 一条成功命令
3. 输入样例路径
4. 输出样例路径
5. 三个坑
6. 下一工具链接


## A6. 与路径 A–E 的硬连接

- A TEC：data-access → georinex → anubis/gfzrnx → **pytecgg** → ionex-gim
- B 扰动：RINEX → **ionomoni/oasis** → 教程 05/20
- C 实时：pygnssutils/bnc → **bkg-ntripcaster** → rtklib
- D 坐标：anubis → rtklib → **pride-pppar**
- E GIM：ionex-gim；**sh-gim** 仅边界


## A7. 术语速查

| 术语 | 一句话 |
| --- | --- |
| RINEX | 观测交换格式 |
| RTCM | 实时差分电文 |
| NTRIP | 基于 HTTP 的差分传输 |
| STEC/VTEC | 斜/垂直电子含量 |
| ROTI | TEC 变化率指数 |
| S4 | 振幅闪烁指数（硬件） |
| IPP | 穿刺点 |
| DCB | 码偏差 |
| GIM/IONEX | 全球电离层图交换 |
| PPP-AR | 精密单点+模糊度固定 |
| QC | 质量检查 |
| SP3 | 精密轨道 |


## A8. 文件命名建议

```text
logs/TOOL_SITE_YYYYDDD.log
out/YYYY/DDD/SITE/...
qc/TOOL_config.ok
```


## A9. 回归命令清单

```bash
set -euo pipefail
# 1 help
# 2 example
# 3 assert
echo PASS
```


## A10. 结束语

参数冲突时信本机帮助。越界产品不要硬解释。先门禁后科学。

