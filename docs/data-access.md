# GNSS 数据获取说明（写给初学者）

本页配合 [`lists/10-gnss-datasets.md`](../lists/10-gnss-datasets.md) 使用，解释常见登录门槛、IGS 目录结构，以及目录里「注册方式」徽章怎么读。

## 注册方式徽章怎么读

| 字段值 | 列表显示 | 含义 |
|---|---|---|
| `open` | 开放下载 | 多数产品可直接 HTTP/HTTPS/匿名拉取，无需个人账号 |
| `form_register` | 网页注册 | 需在门户自助创建账号（如 NASA Earthdata），一般即时可用 |
| `email_register` | 邮件申请 | 向维护方发邮件说明用途后开通 |
| `account_approval` | 账号审批 | 提交申请后需人工审核，可能数日 |
| `institution_only` | 机构限定 | 面向合作机构/成员国网络，个人用户通常走镜像或公开子集 |
| `unknown` | 未确认 | 页面可访问，但获取门槛未在本轮核验中完全确认 |

条目中的 `registration_zh` 是**原创短提示**，概括怎么注册/申请，不是网站原文拷贝。政策会变，以下载页当前说明为准。

## NASA Earthdata / CDDIS 典型流程

1. 打开 [Earthdata Login](https://urs.earthdata.nasa.gov/) 注册免费账号（邮箱验证）。
2. 首次访问 [CDDIS GNSS 归档](https://cddis.nasa.gov/archive/gnss/) 时，用同一账号登录，并在授权页允许 CDDIS 应用访问。
3. 浏览器可浏览目录；批量下载常用 `https://` 或 `ftps://gdc.cddis.eosdis.nasa.gov/`（需账号，旧匿名 FTP 已停）。
4. 脚本下载请用 Earthdata 用户名/密码或 `.netrc`，遵守 NASA 数据使用条款；大流量注意限速与断点续传。

CDDIS 是 IGS 全球数据中心之一，观测、导航、SP3/CLK、IONEX、偏差等常从这里取。

## IGS 数据目录在装什么（obs / nav / sp3 / clk / ionex）

以 CDDIS 为例（其他 IGS 数据中心结构相近，路径略有差异）：

| 类型 | 常见路径概念 | 内容 |
|---|---|---|
| 观测 OBS | `gnss/data/daily/YYYY/DDD/` 等 | 测站 RINEX 观测（常 Hatanaka 压缩 `.crx` + gzip） |
| 导航 NAV | 同日目录或 `brdc` 广播星历树 | 广播星历（多星座合文件或分系统） |
| 精密轨道 SP3 | `gnss/products/WWWW/` | 分析中心 / 综合精密轨道 |
| 钟差 CLK | 同上产品周目录 | 卫星/接收机钟差产品 |
| 电离层 IONEX | `gnss/products/ionex/YYYY/DDD/` | GIM（VTEC 格网）与相关 ROTI 等 |
| 偏差 bias/DCB | `gnss/products/bias/` 等 | 码偏差、OSB 等 |

文件名近年从短名过渡到长名（约 GPS 周 2238 起），例如最终综合 GIM：`IGS0OPSFIN_…_GIM.INX.gz`。下载前对照 [IGS Products](https://igs.org/products/) 与 [Data Access](https://igs.org/data-access/)。

## 其他常见门户一句话

- **EarthScope / 原 UNAVCO**：北美及全球合作站 GNSS 归档，门户已并入 EarthScope；旧 unavco.org 链接多会跳转。
- **BKG / IGS RTS**：实时 RTCM/SSR 多走 NTRIP caster；账号或挂载点规则见 BKG 与 IGS RTS 页。
- **VMF**：对流层映射格网在 TU Wien 数据目录；源码在 `/codes`（本目录软件类另有条目）。
- **COSMIC/CDAAC**：掩星廓线常需 CDAAC 账号；部分汇总也可走 Earthdata 相关集合。
- **GIRO / DIDBase**：测高仪数据需按 UML 门户注册流程；与 GNSS TEC 对比时注意时间与穿透点定义。

更细的逐站说明见 `lists/10-gnss-datasets.md` 各条目「如何获取」。
