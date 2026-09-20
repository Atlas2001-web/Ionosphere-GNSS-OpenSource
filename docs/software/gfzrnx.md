# GFZRNX

目录：[`PROJECTS.json` → `GFZRNX`](../../PROJECTS.json) · 产品页 <https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox> · 手册 <https://gnss.git-pages.gfz-potsdam.de/gfzrnx/> · 下载 <https://gnss.gfz-potsdam.de/services/gfzrnx>

## 用途

- GFZ **RINEX 检查/转换工具箱**（手册常见 2.2.x）。纯 CLI。支持 OBS/NAV/MET、RINEX 2/3/4。
- 典型：小时拼日、1 Hz 抽 30 s、筛系统/观测量、头与历元检查。
- **用：** 进 Python/定位/ROTI 前的预处理。  
- **不用：** 算 TEC/ROTI → [georinex](./georinex.md)/[oasis-roti](./oasis-roti.md)/[ionomoni](./ionomoni.md)；QC 报表 → [anubis](./anubis.md)。TEQC 已基本停更。

## 安装

1. 打开 [服务页](https://gnss.gfz-potsdam.de/services/gfzrnx) 按许可申请/下载平台二进制。
2. 科研教学非例行可走科学伙伴免费许可；例行业务需商业许可——以 EULA 为准。
3. 将可执行文件（`gfzrnx` 或 `gfzrnx_lx` 等）加入 `PATH`。

```bash
gfzrnx -h | head
```

## 快速上手

路径为占位符。Unix 通配多由 **shell** 展开。

```bash
# 1) 检查并写出
gfzrnx -finp data/SITE0010.24o -fout data/SITE0010_chk.24o -chk -kv

# 2) 抽稀到 30 s
gfzrnx -finp data/SITE0010.24o -fout data/SITE0010_30s.24o -smp 30 -kv

# 3) 小时文件拼日文件
gfzrnx -finp data/SITE001{a..x}.24o -fout data/SITE0010.24o -kv
# 省内存：-splice_direct；加速追加：-try_append <秒>（以 -h 为准）

# 4) 选系统/观测量并按 RINEX3 规则命名
gfzrnx -finp data/SITE0010.24o \
  -fout data/::RX3::00,XXX \
  -satsys G \
  -ot L1C,L2W,C1C,C2W \
  -vo 3

# 5) 统计
gfzrnx -finp data/SITE0010.24o -stk_obs > data/SITE0010_stk.txt
gfzrnx -finp data/SITE0010.24o -stk_epo 3600 > data/SITE0010_epo.txt
```

**预期：** 写出目标 RINEX；`-kv` 保持主版本；失败信息在 STDERR（或 `-errlog`）。

## 输入 / 输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS/NAV/MET（2/3/4）；多文件列表；亦可 STDIN（单文件） |
| 输出 | 处理后的 RINEX、统计文本、`-meta`、`-tab` 等 |
| 日志 | 默认 STDERR；`-errlog file` 可追加 |

输出主版本：与输入一致用 `-kv`，强制用 `-vo`。

## 常用参数

| 参数 | 作用 |
|---|---|
| `-finp` / `-fout` | 输入 / 输出 |
| `-chk` | 检查 |
| `-smp` | 抽稀间隔（秒） |
| `-satsys` / `-ot` | 系统 / 观测量 |
| `-kv` / `-vo` | 保持 / 指定版本 |
| `-f` | 允许覆盖 |
| `-splice_direct` | 省内存拼接 |

## 接到工作流哪一步

- 清洗后读 Python → [georinex](./georinex.md) · [02](../tutorials/02-gnss-dualfreq-tec.md)
- ROTI/扰动 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md)
- 站网 QC → [anubis](./anubis.md)
- 数据来源 → [data-access](../data-access.md)

## 常见问题

| 现象 | 处理 |
|---|---|
| 通配没展开 | shell/Windows 行为不同；显式列文件 |
| 内存很大 | 试 `-splice_direct` |
| 不愿覆盖 | 加 `-f` |
| 抽稀后 LLI 怪 | 查 `-smp_lli_shift`（以 `-h` 为准） |
| 许可边界 | 例行生产前再读 EULA |
| 只要 QC 报告 | [anubis](./anubis.md) |

## 相关工具

[anubis](./anubis.md) · [georinex](./georinex.md) · [oasis-roti](./oasis-roti.md)

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
