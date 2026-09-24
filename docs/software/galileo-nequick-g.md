# Galileo-NeQuick-G · GSC 官方 NeQuick-G C 源码操作手册

目录：[`PROJECTS.json` → `Galileo-NeQuick-G`](../../PROJECTS.json) · GSC 源码页 <https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code> · 条款/下载闸 <https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/nequick-g-source-code/nequick-g-terms-and> · 许可 **EUPL-1.2**（条款页：European Union Public Licence v. 1.2）（条款页全文）· 语言 **C11** · ICD PDF 公开可达（本机 **8461196** B，`%PDF-1.7`）· 本机验证（**2026-09-24 06:42 EDT**；质检复跑 **06:47 EDT**：ICD **8461196** B/`%PDF-1.7`；源码页 archive href **0**；条款页 EUPL×**9**/encrypted×**1**/password×**4**）：源码页 **无** `.zip`/`.tar` 匿名链；条款写明 **登录 → 接受 EUPL → 密码加密 zip → ≤7 日邮件口令**；**无账号 → 未下载、未编译、未臆造 TEC**；≠ [nequickg](./nequickg.md)（社区 Python）≠ [nequick2-ictp](./nequick2-ictp.md)（ICTP NeQuick **2**）

> 岗位：拿 **Galileo 单频电离层改正**的 **JRC 参考 C 实现**做产品/认证向量。冲突时：**GSC 页 / 获批包 README / ICD > 本文**。脚本教学先走已短硬 [nequickg](./nequickg.md)（**勿复制**其 Medium 表/TEC stdout；官方 C≠社区 Python）；气候态 NeQuick2 → [nequick2-ictp](./nequick2-ictp.md)；IRI 金标准 → [iri-fortran](./iri-fortran.md)。

## 1. 用途与边界

**做（获批包之后，按包内说明）：**

- JRC **`src/lib`** 库 + 测试驱动（`src`）实现 Galileo **NeQuick-G**
- 包内 **MODIP / CCIR**、按编译器分的 **make**、`.cfg`、Perl（`.pl`）——以 GSC 页目录描述为准
- 按 ICD 用广播 **`ai0/ai1/ai2`** 估单频电离层延迟

**不做 / 本机未做：**

- **不是** 社区 Python [nequickg](./nequickg.md)（`tpl2go/NequickG`；已 Medium 表真跑）
- **不是** ICTP **NeQuick 2**（R12/F10.7）→ [nequick2-ictp](./nequick2-ictp.md)
- **不是** IRI 气候态 → [iri-fortran](./iri-fortran.md)
- **不是** 读 IONEX / 实测 STEC → [ionex.md](./ionex.md) / [pytecgg](./pytecgg.md)
- 本页 **禁止伪造** `gcc`/`make` 日志或 TEC——**无加密包即无本地 E2E 可报**

一句话：Galileo-NeQuick-G = **GSC 门禁的官方 C11 参考实现**；未获批前用 ICD + 社区 Python 推进，勿把镜像当权威。

| 术语 | 含义 |
| --- | --- |
| NeQuick-G | Galileo OS 单频电离层改正变体；入口 **ai0/ai1/ai2** |
| NeQuick 2 | ICTP/ITU 气候态；入口 **R12 或 F10.7** |
| JRC library | 页述 `src/lib`；性能讨论见 MDPI 文（页外链） |
| EUPL-1.2 | 条款页嵌入的欧洲公共许可；须登录后勾选接受 |
| 加密 zip | 接受条款后下载；口令 **另邮 ≤7 日**；勿把口令交给第三方 |

## 2. vs 社区 Python / NeQuick2 / IRI（勿混仓）

| | **本文 GSC C** | [nequickg](./nequickg.md) | [nequick2-ictp](./nequick2-ictp.md) | [iri-fortran](./iri-fortran.md) |
| --- | --- | --- | --- | --- |
| 维护 | GSC / JRC | 社区 GitHub | ICTP 邮件包 | irimodel.org |
| 输入 | **ai0/ai1/ai2** | 同左（移植） | **R12/F10.7** | 月/日/位置/指数 |
| 获取 | **注册 + EUPL + 加密 zip** | 公开 clone | 邮件申请 | 公开 zip |
| 本机短硬 | **登记墙；无编译** | Medium 表真跑 | 登记墙；无编译 | fort.7 真跑 |
| 适用 | 产品/认证向量 | 脚本/教学 | ITU 气候态研究 | IRI 金标准 |

混用后果：用 F10.7 当 `ai0`、或把社区 Python 当 bit 级认证——论文与接收机都会错。

## 3. 获取：登记墙（诚实步骤）

源码页（2026-09-24 拉取）要点：实现为 **C2011**；含 JRC 库、测试驱动、MODIP/CCIR、make/cfg/pl；**仅对注册用户、经 access request 提供**。

条款页补充：须 **登录** 后勾选接受 **EUPL v1.2**；同意后可下 **password encrypted zip**；**7 日内**邮件收口令；解压用外部工具（7zip/`unzip` 等），**勿**把口令泄露给第三方。

```bash
# 1) 确认源码页仍无匿名制品（应只有 Request access，没有直链 zip）
curl -fsSL -A 'Mozilla/5.0' -o /tmp/nqg_gsc.html \
  'https://www.gsc-europa.eu/support-to-developers/ionospheric-correction-algorithms/galileo-nequick-g-source-code'
rg -n 'registered users|Request access|src/lib|MODIP|CCIR|\.zip|\.tar' /tmp/nqg_gsc.html

# 2) 读条款（登录后才能勾选接受框）
# https://www.gsc-europa.eu/.../nequick-g-terms-and

# 3) GSC 账号 → Register/Login → 接受 EUPL → 下加密 zip
# 4) 等待口令邮件（页述 ≤7 日）→ 外部工具解压 → 再进 §5
mkdir -p ~/iono_ops/galileo-nequick-g
# cp /path/from/download/*.zip ~/iono_ops/galileo-nequick-g/   # 仅真实获批后
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `curl` 只有 HTML、无 `.zip` | **设计如此** | 走注册；或先用 [nequickg](./nequickg.md) |
| 条款页无勾选框 | 未登录 | `/user/login` 后再开条款 |
| 下了 zip 解不开 | 口令未到 / 用了资源管理器双击 | 等邮件；`7z x`/`unzip` |
| 当公开镜像即官方 | 非 GSC 托管 | 以 GSC 加密包 + EUPL 为准 |

**本机（2026-09-24 06:42 EDT）：** 源码页与条款页 href 扫描 **0** 个 zip/tar；正文含 registered / EUPL / encrypted zip；→ **停止在申请步骤**。

## 4. 无源码时的公开材料（可达，非本地 E2E）

| 材料 | URL | 本机 |
| --- | --- | --- |
| ICD（单频用户电离层改正） | <https://www.gsc-europa.eu/sites/default/files/sites/all/files/Galileo_Ionospheric_Model.pdf>（页内链） | **200**，**8461196** B，`%PDF-1.7` |
| JRC 实现性能论文 | 源码页外链 MDPI `2072-4292/13/2/191` | 本机 `curl` 对该域 **403**（站点策略）；浏览器另核 |
| ESA ESSR 镜像页 | <https://essr.esa.int/project/nequickg-galileo-ionospheric-correction-model> | 亦要 **register**；许可文案为 ESA Community License（与 GSC EUPL **并列登记通道**，勿混许可证假设） |
| 社区 Python | [nequickg](./nequickg.md) | 已短硬；**勿**与官方 C bit 级对齐假设 |

ICD 含步骤与互补文件说明，供自实现对照——**不能**替代获批 JRC 测试向量。

## 5. 获批后的建议编译清单（模板，无假日志）

```bash
cd ~/iono_ops/galileo-nequick-g
# unzip -P '<邮件口令>' NeQuick*.zip && cd <解压根>
# find . -path '*/src/lib*' -o -name '*.c' -o -name 'Makefile*' | head
# ls *modip* *ccir* 2>/dev/null | head
# 按包内对应编译器的 make / README，例如：
# make -f <包内 Makefile>
# ./<test_driver> <包内 cfg / 向量>
```

验收：

1. 跑包内自带测试 / ICD 算例  
2. 同几何可与 [nequickg](./nequickg.md) Medium 表 **粗**对照（允许实现差；产品以官方向量为准）  
3. **不要**与 [nequick2-ictp](./nequick2-ictp.md) / [iri-fortran](./iri-fortran.md) 逐行比 TEC——物理入口不同

## 6. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 仓库搜不到官方 zip | 注册 + 加密分发 | §3；勿造 CDN URL |
| 2 | 用 [nequickg](./nequickg.md) 当认证 | 社区移植 ≠ JRC C | 产品链换本文包 |
| 3 | 把 NeQuick2 的 F10.7 填进 G | 模型族混淆 | ai*↔G；R12/F10.7↔2 |
| 4 | 条款勾不了 | 未登录 | 先 Register/Login |
| 5 | zip 双击失败 | 密码归档 | 外部 7zip/`unzip -P` |
| 6 | 口令外传 | 条款禁止 | 本机保管；轮换账号 |
| 7 | ESSR 与 GSC 许可混谈 | 双通道文案不同 | 引用你实际接受的那份 |
| 8 | CI `curl` 源码页当制品 | HTML≠源码 | 人工 artifact |
| 9 | 与 IRI TEC 差就“判死” | 气候模型族不同 | 并列报告 |
| 10 | 无包却写 `make` 绿勾 | 臆造 | 本页刻意无 stdout |

## 7. 接到哪步

1. 概念：[04-iri-nequick](../tutorials/04-iri-nequick.md)  
2. 可跑脚本：[nequickg](./nequickg.md) → 产品改 **本文**  
3. 气候态 / IRI：[nequick2-ictp](./nequick2-ictp.md) · [iri-fortran](./iri-fortran.md)  
4. 实测 TEC / GIM：[pytecgg](./pytecgg.md) · [ionex.md](./ionex.md) · [gnss-tec](./gnss-tec.md)  
5. 数据礼仪：[data-access](../data-access.md)

## 8. 工作流（短）

1. 打开 GSC 源码页 → **Register/Login** → 条款页勾选 **EUPL-1.2** → 下加密 zip  
2. 等待口令邮件（页述 ≤7 日）→ 外部工具解压到 `~/iono_ops/galileo-nequick-g`  
3. 等待期间：读 ICD PDF；并行跑 [nequickg](./nequickg.md) / [iri-fortran](./iri-fortran.md)  
4. 获批 → 按包内 make/测试驱动验收 → 再接自有射线几何与广播系数  
5. 写结果时标明 **NeQuick-G（GSC C）≠ NeQuick 2（ICTP）≠ 社区 Python**，并引用包版本串 / EUPL

## 9. 本机门禁结论（给质检）

| 检查项 | 结果 |
| --- | --- |
| 源码页可达 | 是（2026-09-24 06:42 EDT） |
| 匿名源码下载 | **否**（0 zip/tar href） |
| 条款：EUPL + 加密 zip + 邮件口令 | 是（须登录勾选） |
| ICD PDF | **8461196** B / PDF-1.7 |
| 本地 `make`/TEC stdout | **无**（故意不编造；质检复跑确认） |
| 可公开替代 | ICD；[nequickg](./nequickg.md)（**勿** bit 级对齐） |
| 同栏目 NTCM-G | GSC 另有 NTCM-G 源码页（**不是**本文）；勿点错下载 |

## 10. 相关

[nequickg](./nequickg.md) · [nequick2-ictp](./nequick2-ictp.md) · [iri-fortran](./iri-fortran.md) · [iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [ionex.md](./ionex.md) · [pytecgg](./pytecgg.md) · [data-access](../data-access.md) · [README](./README.md)

