# GNSS 数据怎么下

配合 [`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md)。本页只答三件事：**要什么 → 去哪下 → 要不要注册**。

![STEC / VTEC 产品从观测来（本仓库自制）](./tutorials/images/fig-stec-vtec-shell.png)

想先看现象长什么样？→ [README 现象画廊](../README.md)

## 一屏决策

| 你想要 | 优先门户 | 注册 |
|---|---|:---:|
| 全球 RINEX / 广播星历 | [CDDIS](https://cddis.nasa.gov/archive/gnss/) · [BKG](https://igs.bkg.bund.de/) · [ESA GSSC](https://gssc.esa.int/) | 网页 / 视中心 |
| SP3 / CLK / 偏差 | CDDIS `gnss/products/` · [IGS files](https://files.igs.org/) | 同左 |
| GIM / IONEX | CDDIS `ionex` · CODE / UPC 等 | 视源 |
| 高采样率（闪烁 / 同震） | [CDDIS high-rate](https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/high-rate_data.html) · `cddis-highrate-downloader` | Earthdata |
| 区域 CORS | GeoNet · IBGE · NOAA CORS · 各国网 | 视网络 |
| 实时 RTCM / SSR | BKG / IGS RTS（NTRIP） | 账号或挂载点 |
| 掩星 RO | CDAAC · ROM SAF · AWS GNSS-RO | 账号 / 开放 |
| 地磁指数 | [Kyoto WDC](https://wdc.kugi.kyoto-u.ac.jp/) · INTERMAGNET · SuperMAG | 开放 / 注册 |
| 闪烁 ISMR | [ISMR Query Tool](https://ismrquerytool.fct.unesp.br/) · `ismr_downloader` | 网页注册 |

逐站细节与注册字段 → [`10-gnss-datasets.md`](../lists/10-gnss-datasets.md)。

## 注册徽章（列表里怎么读）

| 字段 | 列表显示 | 含义 |
|---|---|---|
| `open` | 开放下载 | 可直接拉，无需个人账号 |
| `form_register` | 网页注册 | 自助开账号（如 Earthdata），一般即时 |
| `email_register` | 邮件申请 | 发邮件说明用途后开通 |
| `account_approval` | 账号审批 | 人工审核，可能数日 |
| `institution_only` | 机构限定 | 合作机构；个人多走镜像 / 公开子集 |
| `unknown` | 未确认 | 页可开，门槛未完全核验 |

`registration_zh` 是原创短提示，不是网站原文。**政策以当前下载页为准。**

## CDDIS / Earthdata（最常用）

| 步 | 做什么 |
|---:|---|
| 1 | [Earthdata Login](https://urs.earthdata.nasa.gov/) 免费注册并验证邮箱 |
| 2 | 开 [CDDIS GNSS 归档](https://cddis.nasa.gov/archive/gnss/)，登录并授权 CDDIS |
| 3 | 批量用 `https://` 或 `ftps://gdc.cddis.eosdis.nasa.gov/`（旧匿名 FTP 已停）；脚本用账号或 `.netrc`，限速 + 断点续传 |

## IGS 目录里装什么

| 类型 | 路径概念（CDDIS） | 内容 |
|---|---|---|
| OBS | `gnss/data/daily/YYYY/DDD/` | RINEX（常 `.crx.gz`） |
| NAV | 同日或 `brdc` | 广播星历 |
| SP3 / CLK | `gnss/products/WWWW/` | 精密轨道 / 钟差 |
| IONEX | `gnss/products/ionex/YYYY/DDD/` | GIM（VTEC 格网） |
| bias / DCB | `gnss/products/bias/` 等 | 码偏差、OSB |

约 GPS 周 2238 起多用长文件名（如 `IGS0OPSFIN_…_GIM.INX.gz`）。对照 [IGS Products](https://igs.org/products/) · [Data Access](https://igs.org/data-access/)。

## 其他门户（一句）

| 门户 | 一句 |
|---|---|
| **EarthScope**（原 UNAVCO） | 北美及合作站；旧链接多跳转 |
| **BKG / IGS RTS** | 实时走 NTRIP |
| **VMF** | TU Wien 对流层格网 |
| **CDAAC / COSMIC** | 掩星常需账号 |
| **GIRO / DIDBase** | 测高仪；与 GNSS TEC 对比时对齐时间与穿透点 |

## 相关教程与软件

下完数据后常接：

| 目标 | 去哪 |
|---|---|
| 双频 STEC / 一日练习 | [02](./tutorials/02-gnss-dualfreq-tec.md) · [16](./tutorials/16-practice-one-day-tec.md) |
| 读 GIM / IONEX | [03](./tutorials/03-gim-ionex.md) · [ionex-gim](./software/ionex-gim.md) |
| 目录怎么用 | [08](./tutorials/08-how-to-use-this-catalog.md) |
| RINEX 读盘 / QC | [georinex](./software/georinex.md) · [anubis](./software/anubis.md) |
| 软件短文总索引 | [software/README](./software/README.md) · [tutorials/README](./tutorials/README.md) |
