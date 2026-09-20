# GFZRNX · RINEX 检查 / 拼接 / 抽稀

目录条目：[`PROJECTS.json` → `GFZRNX`](../../PROJECTS.json) · 产品页 <https://www.gfz.de/en/section/space-geodetic-techniques/data-products-services/gfzrnx-gnss-toolbox>  
用户手册：<https://gnss.git-pages.gfz-potsdam.de/gfzrnx/> · 下载：<https://gnss.gfz-potsdam.de/services/gfzrnx> · 列表：[03 GNSS 数据](../../lists/03-gnss-data.md)

## 作用与场景

**它是什么**：GFZ 的 **RINEX 转换与处理工具箱**（用户指南常见版号 **2.2.x**）。纯命令行。支持观测 / 导航 / 气象 RINEX **2 / 3 / 4**。

**它解决什么**：小时文件要拼日文件、1 Hz 要抽成 30 s、只留某系统/观测量、头信息与历元形式检查——放进 Python / 定位 / ROTI 流水线之前先做**预处理与质检**。

**何时用：** 数据中心或个人站网的 RINEX 清洗。  
**何时不用：** 要算 TEC/ROTI → [georinex](./georinex.md) / [oasis-roti](./oasis-roti.md) / [ionomoni](./ionomoni.md)；要出 QC 报表 → [anubis](./anubis.md)。老工具 TEQC 已基本停更，新流水线优先 GFZRNX + Anubis。

## 安装

1. 打开 [GFZRNX 服务页](https://gnss.gfz-potsdam.de/services/gfzrnx)，按许可申请/下载对应平台二进制。  
2. **科研教学非例行**可走科学伙伴免费许可；**例行业务**需商业许可——以官网 EULA 为准。  
3. 将可执行文件（文档常写作 `gfzrnx`，实际可能是 `gfzrnx_lx` 等）加入 `PATH`。

```bash
gfzrnx -h | head
```

## 最小可跑命令

路径为占位符。Unix 下通配多由 **shell** 展开；Windows 下部分通配由程序处理（见手册）。

**1）检查并写出**

```bash
gfzrnx -finp data/SITE0010.24o -fout data/SITE0010_chk.24o -chk -kv
```

**2）抽稀到 30 s**

```bash
gfzrnx -finp data/SITE0010.24o -fout data/SITE0010_30s.24o -smp 30 -kv
```

**3）小时文件拼日文件**

```bash
gfzrnx -finp data/SITE001{a..x}.24o -fout data/SITE0010.24o -kv
# 省内存：-splice_direct；加速追加：-try_append <秒>（以 -h 为准）
```

**4）选系统 / 观测量并按 RINEX 3 规则命名**

```bash
gfzrnx -finp data/SITE0010.24o \
  -fout data/::RX3::00,XXX \
  -satsys G \
  -ot L1C,L2W,C1C,C2W \
  -vo 3
# 观测量名与国家码 XXX 以站数据及当前手册为准
```

**5）统计**

```bash
gfzrnx -finp data/SITE0010.24o -stk_obs > data/SITE0010_stk.txt
gfzrnx -finp data/SITE0010.24o -stk_epo 3600 > data/SITE0010_epo.txt
```

## 输入输出

| 方向 | 内容 |
|---|---|
| 输入 | RINEX OBS/NAV/MET（2.x/3.x/4.x）；多文件列表；亦可 STDIN（单文件） |
| 输出 | 处理后的 RINEX、统计文本、元数据（`-meta`）、表格化观测（`-tab`）等 |
| 日志 | 默认 STDERR；`-errlog file` 可追加到文件 |

输出主版本策略见手册；与输入主版本一致用 `-kv`，强制 2/3/4 用 `-vo`。

## 常见坑

| 现象 | 可能原因 | 怎么处理 |
|---|---|---|
| 通配没展开 | shell / Windows 行为不同 | 读手册 Filename Expansion；或显式列文件 |
| 内存很大 | 默认 splice 为做头统计会进 RAM | 试 `-splice_direct` / `-direct`（会牺牲部分头统计） |
| 不愿覆盖 | 默认不覆盖已存在文件 | 加 `-f` |
| 抽稀后 LLI 怪 | 采样与标志位移 | 查阅 `-smp_lli_shift`（名称以 `-h` 为准） |
| 许可边界 | 免费范围有限 | 例行生产前再读 EULA |
| 只要 QC 报告 | 工具定位不同 | 看 [anubis](./anubis.md) |

## 接到哪一步分析

- 清洗后读进 Python → [georinex](./georinex.md) · [02 双频 TEC](../tutorials/02-gnss-dualfreq-tec.md)  
- 算 ROTI / 扰动 → [oasis-roti](./oasis-roti.md) · [ionomoni](./ionomoni.md) · [05](../tutorials/05-scintillation-roti.md)  
- 站网 QC 报告 → [anubis](./anubis.md)  
- 数据从哪来 → [数据怎么下](../data-access.md)

## 目录指针

- `PROJECTS.json`：`GFZRNX` · 相关：`GFZRNX-UserGuide`、`TEQC`
