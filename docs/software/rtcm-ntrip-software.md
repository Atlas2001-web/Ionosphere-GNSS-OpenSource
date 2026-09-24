# RTCM-Ntrip-Software · 官方 RTCM NTRIP 软件门户操作手册

目录：[`PROJECTS.json` → `RTCM-Ntrip-Software`](../../PROJECTS.json) · 门户 <https://software.rtcm-ntrip.org/>（HTTP 亦可）· Trac **1.6** · WikiStart **Last modified 2024-05-16 10:52:26 +02**（≈ **2024-05-16 04:52 EDT**）· 本机复抓 **2026-09-24 06:19–06:21 EDT**：首页 **9539** B / HTTP **200**；`svn info` trunk **Revision 11044**，Last Changed **r11043** @ **2026-09-23 06:03 EDT** · 许可随组件（多为 **GPL**；Professional Caster **另订**） · **质检复跑** 2026-09-24 06:24 EDT（首页 **9539** B/**200**/Trac **1.6**；WikiStart **May 16, 2024, 10:52:26 AM**；`svn info` **Revision 11044** / LCR **11043** / **2026-09-23 06:03:12 -0400**；BKG `bnc`/`download`/`bkgcaster` 皆 **200**（bnc⇄download 同 **22675** B）；页面 **BNC v2.13.7**；`bnchelp.html`+`/browser/.../tags` **429**；SSR **256/257/258/259**；Sourcetable **2011-12-16**；交叉 [bnc](./bnc.md)/[bkg-ntripcaster](./bkg-ntripcaster.md)/[ntripstreams](./ntripstreams.md)/[rtcm3torinex](./rtcm3torinex.md)/[ntripcaster-libev](./ntripcaster-libev.md)）

> 岗位：当 **索引页**——分清门户上有什么、发行物在哪下、以及已有短硬手册该点哪篇。冲突时：**门户 WikiStart / BKG 下载页 / 各组件 `-h` > 本文**。本页 **不** 替代 [bnc](./bnc.md) / [bkg-ntripcaster](./bkg-ntripcaster.md) 的逐步操作。

## 1. 用途与边界

**做：**

- 浏览 NTRIP 相关开源组件的 **开发门户**（Wiki / Tickets / Timeline / SVN）
- 用 `guest`/`guest` 检出 trunk，对照标签与 changelog
- 选型：客户端 / 上传 / 转换 / 播发器 / 仅协议库 该走哪条下载链

**不做：**

- **不是** 二进制一站式安装器（发行包在 **BKG** 下载页，见下）
- **不是** RTCM 标准文本免费站（标准件在 RTCM 商店购买）
- **不** 重复已短硬组件的端到端命令 → 见第 3 节交叉表
- **不** 提供账号口令或绕过 caster 鉴权

一句话：`software.rtcm-ntrip.org` = **BKG/RTCM 系 NTRIP 开源 Trac 门户**；日常装包请去 BKG，日常用法请去各组件手册。

| 术语 | 含义 |
| --- | --- |
| WikiStart | 门户首页欢迎页（组件清单 + SVN 一句命令） |
| trunk | SVN 开发树；本机 **r11044** |
| tags/`BNC_2.13.x` | BNC 发行标签；浏览器可见至 **BNC_2.13.7** |
| BKG download | <https://igs.bkg.bund.de/ntrip/download> 等；**预编译发布**主入口 |
| Professional Caster | 商业/订购档播发器；Trac 作 **bug-tracker**，源码不在公开 trunk 白嫖 |

## 2. 门户上有什么（本机抓取）

WikiStart（2026-09-24 与 WebFetch 一致）写明：

**中央开发平台：**

| 组件 | 门户说法 | 本仓手册 |
| --- | --- | --- |
| **BNC** | 主推多功能客户端 | [bnc](./bnc.md)（本机验过 **2.13.7**） |
| **POSIX ntripserver** | 上传流到 caster | 见 SVN `trunk/ntripserver`（本页只索引；操作以源码 `-h`/wiki 为准） |
| **POSIX ntripclient** | 轻量订流客户端 | 见 SVN `trunk/ntripclient`；脚本主力亦可 [ntrip-client](./ntrip-client.md) / [pygnssutils](./pygnssutils.md) |
| **NDF** | 传输格式（wiki `/wiki/NDF`） | 无单独短硬篇；协议细节读 wiki |

**历史 / 过时：**

| 组件 | 门户说法 | 本仓手册 |
| --- | --- | --- |
| **BNS** | historic，**已被 BNC 替代** | 勿新开项目；概念见门户 `/wiki/BNS` |
| **rtcm3torinex** | **obsolete**，功能 **已含在 BNC** | [rtcm3torinex](./rtcm3torinex.md)（仍可 SVN 编译；新部署优先 BNC） |

**Bug-tracker：**

| 组件 | 说明 | 本仓手册 |
| --- | --- | --- |
| **Professional BKG caster** | Trac 建单 `component=Professional Caster`；源码/包 **订购** | [bkg-ntripcaster](./bkg-ntripcaster.md)（订购与手册链以 BKG 页为准） |

**附加信息页：**

| 页 | URL | 本机笔记 |
| --- | --- | --- |
| NTRIP sourcetable 概述 | `/wiki/Sourcetable` | CAS/NET/STR 三类记录；页脚 **Last modified 2011-12-16**（概念仍有效，细节以现行 NTRIP 标准为准） |
| Assigned SSR Provider IDs | `/wiki/SSRProvider` | 例：BKG **256**、EUREF **257**、IGS **258**、NRCan **259**…（表会更新，引用前打开现页） |
| TitleIndex | `/wiki/TitleIndex` | 可见 BNC、BNS、NDF、SSRProvider、Sourcetable、ntripclient、ntripserver、rtcm3torinex 等 |

**源码浏览（本机 WebFetch `/browser/ntrip/trunk`，2026-09-24）：**

| 目录 | 浏览器显示要点 |
| --- | --- |
| `BNC/` | Last change **r11043**（约 24 h 前）：RTCM3Decoder 相关 |
| `ntripserver/` | **r10685**（约 15 months；2025-07-01 时间线） |
| `ntripclient/` / `rtcm3torinex/` / `BNS/` / `clock_and_orbit/` | 末变多停在 **r9404**（2021-04-14） |
| `GnssCenter/` / `misc/` | 更旧；`misc` 注释含 REMOVE obsolete |
| `tags/` | 浏览器注 **r11044**：BNC **2.13.7 → 2.13.7.1** bugfix（拼写 “bersion” 为上游 changelog 原文笔误） |

反复刷新 `/browser/...` 可能 **HTTP 429**（写作 + 质检复跑 06:24 EDT 均出现）——属门户限流，不是“目录消失”。

## 3. 已文档化手册 vs 门户条目

| 你要… | 门户角色 | 打开手册 |
| --- | --- | --- |
| 多流 GUI / 录盘 / REQC / PPP | 开发树 + 帮助 HTML | [bnc](./bnc.md) |
| 自建多用户播发 | 订购 + 手册 | [bkg-ntripcaster](./bkg-ntripcaster.md) |
| RTCM3→RINEX 单流小工具 | obsolete 源码 | [rtcm3torinex](./rtcm3torinex.md) |
| Python 订流 / 小 caster | （非本 SVN） | [pygnssutils](./pygnssutils.md) / [ntripstreams](./ntripstreams.md) |
| Rust NTRIP example CLI | （非本 SVN） | [ntrip-client](./ntrip-client.md) |
| 仅解码 RTCM3 帧 | （非本 SVN） | [pyrtcm](./pyrtcm.md) |
| 源表浏览 / 按距筛 | （非本 SVN） | [ntripbrowser](./ntripbrowser.md) |
| 实验室轻量播发 / 中继 | （社区） | [ntripcaster-libev](./ntripcaster-libev.md) / [cors-relay](./cors-relay.md) |
| **本页** | 门户地图 + 下载选型 | — |

## 4. 下载该点哪（版本/日期事实）

### 4.1 源码（门户）

```bash
svn checkout --username guest --password guest \
  https://software.rtcm-ntrip.org/svn/trunk
svn info https://software.rtcm-ntrip.org/svn/trunk \
  --username guest --password guest | grep -E 'Revision|Last Changed'
# 本机 2026-09-24 06:21 EDT；质检复跑 06:24 EDT 同：
# Revision: 11044
# Last Changed Rev: 11043
# Last Changed Date: 2026-09-23 06:03:12 -0400 (EDT)
```

只要 BNC：

```bash
svn checkout --username guest --password guest \
  https://software.rtcm-ntrip.org/svn/trunk/BNC
```

在线帮助（BNC 手册常链到此）：  
`https://software.rtcm-ntrip.org/export/HEAD/ntrip/trunk/BNC/src/bnchelp.html`  
质检复跑 06:24 EDT：该 export 与 `/browser/ntrip/tags` 均曾 **HTTP 429**（限流）——改用已落盘帮助或稍后再抓，勿当“文件消失”。

### 4.2 发行二进制（BKG，不是 Trac 附件栏）

门户原文：*Released versions … at BKG ntrip download pages.*

本机 2026-09-24：

| URL | HTTP | 页面要点 |
| --- | --- | --- |
| <https://igs.bkg.bund.de/ntrip/bnc> | 200 | **BNC v2.13.7**；多平台包 + Source Code C++ GPL；质检复跑页 **22675** B |
| <https://igs.bkg.bund.de/ntrip/download> | 200 | 与 BNC 工具页同构（质检复跑同 **22675** B；勿假设另有“总 zip”） |
| <https://igs.bkg.bund.de/ntrip/bkgcaster> | 200 | Professional Caster：**Order and Delivery**；支持 Ntrip v1/v2；**不**做 VRS/最近站；质检复跑 **20792** B |

FTP 软件树（BNC 手册亦用）：`https://igs.bkg.bund.de/root_ftp/NTRIP/software/`（BNC / caster 子目录）。

### 4.3 其它链

| 资源 | 说明 |
| --- | --- |
| RTCM shop「Ntrip client best practices」 | 门户外链；**付费纸质/电子**，不是 SVN 附件 |
| SSR Provider 申请 | wiki 写联系 rtcm.org 申请全局唯一 ID |

## 5. 接到哪一步

| 目标 | 下一步 |
| --- | --- |
| 马上订一个挂载点落盘 | [bnc](./bnc.md) 或 [pygnssutils](./pygnssutils.md) |
| 自建 caster | [bkg-ntripcaster](./bkg-ntripcaster.md)（订购）或实验室 [ntripcaster-libev](./ntripcaster-libev.md) |
| 只看源表 | [ntripbrowser](./ntripbrowser.md) |
| RTCM 帧级调试 | [pyrtcm](./pyrtcm.md) |
| 数据政策 / 公网 caster | [data-access](../data-access.md) |

## 6. 坑：怎么选对下载（≥8）

1. **把 Trac 当 App Store**——首页几乎不挂“最新 BNC.exe”；二进制在 **BKG ntrip** 页 / FTP。
2. **把 Professional Caster 当成 trunk 里免费目录**——公开树是 BNC/POSIX/…；Caster **订购**（历史 ticket #91 亦指向 BKG 订购页）。
3. **检出整个 `trunk` 以为等于发行版**——trunk **r11044** 可能超前或含实验改动；生产应对齐 BKG 的 **2.13.7**（或标签 `BNC_2.13.7` / 随后的 **2.13.7.1** 说明）。
4. **继续部署 BNS 或独立 rtcm3torinex 当“官方推荐”**——WikiStart 已标 historic / obsolete；新链路用 BNC。
5. **混淆 ntripclient（POSIX C）与本仓 Rust/Python 客户端**——同名不同实现；脚本生态常用 [ntrip-client](./ntrip-client.md) / [pygnssutils](./pygnssutils.md)。
6. **浏览器 429 就改用野镜像源码**——限流时改 `svn` 或等重试；勿从不明 Git 镜当权威。
7. **下载页打开却是 HTML 错误页当 zip**——核对 `file`/`unzip -t` 与体积（见 [bnc](./bnc.md) 安装表）。
8. **以为 sourcetable wiki（2011）= 某公网 caster 现势**——格式概念可用；**挂载列表**向目标 caster 现拉（[ntripbrowser](./ntripbrowser.md)）。
9. **SSR Provider ID 表当改正流本身**——只是服务商标识；改正电文仍要订对应挂载点。
10. **Ntrip best practices PDF 在 SVN**——在 RTCM 商店；门户只外链。
11. **HTTP vs HTTPS**——本机两者可达；脚本固定一种并校证书，避免混用丢 cookie/重定向。
12. **把社区 caster（libev/Node）误记为 RTCM 门户产物**——交叉见 [ntripcaster-libev](./ntripcaster-libev.md)，许可证与运维模型不同。

## 7. 选型（一句话）

| 场景 | 选 |
| --- | --- |
| 查官方 NTRIP 开源地图 / SVN / ticket | **本门户**（本页） |
| 日常多流客户端 | BKG 下 BNC → [bnc](./bnc.md) |
| 营运级播发 | 订购 Professional Caster → [bkg-ntripcaster](./bkg-ntripcaster.md) |
| 实验室快速播发 | [ntripcaster-libev](./ntripcaster-libev.md) / [pygnssutils](./pygnssutils.md) |
| 协议库 / 脚本 | [pyrtcm](./pyrtcm.md) + [ntripstreams](./ntripstreams.md) / [ntrip-client](./ntrip-client.md) |

