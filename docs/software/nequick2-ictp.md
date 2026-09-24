# NeQuick2-ICTP · ICTP NeQuick 2 源码申请页操作手册

目录：[`PROJECTS.json` → `NeQuick2-ICTP`](../../PROJECTS.json) · 源码申请页 <https://t-ict4d.ictp.it/nequick2/source-code> · 模型简介 <https://t-ict4d.ictp.it/nequick2/nequick-model> · Web 试算 <https://t-ict4d.ictp.it/nequick2/nequick-2-web-model> · 许可 **scientific distribution（邮件申请）** · 语言 **Fortran**（官方包描述）· 本机验证：**源码页无匿名下载链**；确认联系人 **bnava@ictp.it** / **yenca@ictp.it**；**未获包 → 未编译、未臆造 TEC**；公开 Web 表单可达（端点坐标 + R12/F10.7）· 2026-09-24 06:12 EDT · **质检复跑** 2026-09-24 06:15 EDT（申请页再拉：正文含 FORTRAN/ITU/modip；mailto **bnava@ictp.it** / **yenca@ictp.it**；**无** `.zip`/`.tar` 匿名链；Web 表单 lat/lon/elev + R12∈[0,150]/F10.7∈[63,193]；Terms 可达；**仍无包 → 未编译、未臆造 TEC stdout**；≠ [nequickg](./nequickg.md)）

> 岗位：拿 **ITU 气候态 NeQuick 2**（穿电离层路径 Ne + TEC）做科研对照。冲突时：**ICTP 页 / 获批包内 README > 本文**。Galileo **广播三系数**改正 → 已短硬 [nequickg](./nequickg.md)（社区 Python）或 GSC/JRC **NeQuick-G C**（登记）。概念课 [04](../tutorials/04-iri-nequick.md)。

## 1. 用途与边界

**做（获批包之后，按维护者说明）：**

- 气候态电子密度（高度 / 地理纬经）与任意地–卫直线上的 **sTEC / 剖面积分**
- 太阳活动入口：**R12** 或 **F10.7**（与 Galileo `ai0/ai1/ai2` **不是同一套输入**）
- ITU-R 系数、太阳活动与 modip 等数据文件（源码页写明包内含这些）

**不做 / 本机未做：**

- **不是** Galileo 单频 **NeQuick-G** → [nequickg](./nequickg.md)；产品链用 GSC 官方 C（见该篇 §6）
- **不是** IRI 气候态 → [iri-fortran](./iri-fortran.md) / [iri2016](./iri2016.md) / [pyiri](./pyiri.md)
- **不是** 读 IONEX / 校准 GNSS TEC → [ionex-gim](./ionex-gim.md) / [pytecgg](./pytecgg.md)
- 本页 **禁止伪造** `gfortran` 日志或 TEC 数字——**无源码包即无本地 E2E 可报**
- 本页 **不** 声称拥有 SH-GIM / PyTECGg

一句话：NeQuick2-ICTP = **邮件门禁的官方 NeQuick 2 Fortran 发行入口**；未获批前只能走 Web 试算或改用已开源的 NeQuick-G / IRI。

| 术语 | 含义 |
| --- | --- |
| NeQuick 2 | ICTP T/ICT4D 气候态快速电子密度模型（Nava et al., 2008） |
| NeQuick-G | Galileo **ICD 广播改正**变体；输入 `ai0/ai1/ai2` |
| R12 / F10.7 | 月均黑子数 / 10.7 cm 流量；Web 页提示 R12∈[0,150]、F10.7∈[63,193] |
| MODIP | 修正磁倾角；包内系数文件支撑 |
| 半 Epstein 层 | 底侧多锚点 + 顶侧厚度经验式（简介页） |

## 2. NeQuick 2 vs NeQuick-G（勿混仓）

| | **NeQuick 2（本篇）** | **NeQuick-G（[nequickg](./nequickg.md)）** |
| --- | --- | --- |
| 维护 | ICTP T/ICT4D | Galileo / GSC（社区 Python 移植另仓） |
| 典型输入 | 月、UT、位置、**R12 或 F10.7** | 月、UT、位置、**ai0/ai1/ai2** |
| 获取 | **邮件申请** Fortran 包 | GitHub / GSC 登记 C |
| 本机短硬状态 | **登记墙；无本地编译** | 已短硬：Medium 表真跑 |
| 适用 | ITU 气候态 / 传播研究 | 单频 Galileo 电离层改正对照 |

混用后果：把 `ai0` 当 F10.7、或把 NeQuick2 TEC 当接收机认证向量——论文与产品都会错。

## 3. 获取：登记墙（诚实步骤）

源码页正文（2026-09-24 拉取）要点：

> 包含模型 Fortran 函数/子程序、ITU 系数、太阳活动与 modip 文件。  
> 科学界可申请当前版本；有意者写信至 **bnava@ictp.it** 或 **yenca@ictp.it**。

```bash
# 1) 本机确认申请页仍在（应看到邮件地址，而不是匿名 zip）
curl -fsSL -A 'Mozilla/5.0' -o /tmp/nq2_src.html \
  'https://t-ict4d.ictp.it/nequick2/source-code'
rg -n 'bnava@ictp.it|yenca@ictp.it|FORTRAN|coefficients|ITU' /tmp/nq2_src.html

# 2) 用机构邮箱写信（勿群发爬虫）。建议正文包含：
#    - 姓名 / 单位 / 用途（科研 TEC / 教学）
#    - 计划平台（Linux + gfortran 版本）
#    - 承诺遵守其 Terms of Use
# 主题示例：Request for NeQuick 2 source code for research use

# 3) 获批后按邮件附件/链接落盘，再进入 §5 编译清单（以下命令在
#    未获包时不要假装已经成功）
mkdir -p ~/iono_ops/nequick2-ictp
# cp /path/from/email/*.zip ~/iono_ops/nequick2-ictp/   # 仅在真实获批后
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `curl` 只有 HTML、无 `.zip` | **设计如此**（非 CDN 开源） | 发邮件；或用 §4 Web |
| 邮箱无回复数日 | 人工分发 | 礼貌跟催一次；同时用 Web / [nequickg](./nequickg.md) 推进其它工作 |
| 把 GitHub 上不明 “NeQuick2” 当官网 | 镜像/改写未经验证 | 以 ICTP 邮件包为准 |

**本机（2026-09-24 06:12 EDT；质检复跑 06:15 EDT 对齐）：** `rg` 命中 `bnava@ictp.it` / `yenca@ictp.it` + FORTRAN/ITU/modip；href 扫描**无** zip/tar；→ **停止在申请步骤**（勿编造 `gfortran` 日志）。

## 4. 无源码时的公开替代：Web Model（可达，非本地 E2E）

```text
https://t-ict4d.ictp.it/nequick2/nequick-2-web-model
```

表单能力（页上字段，本机打开确认存在）：

- 射线两端：纬 / 经 / 高程（km），或方位角 + 仰角 + 卫星轨道高
- 太阳活动：R12 或 F10.7（超范围可能得到未定义密度——页上 ITU-R P.1239 警告）

用途：课前量级感、与获批 Fortran 结果对照。**不能**替代可复现脚本；也**不要**把网页截图数字写进本仓库当“本机 stdout”。

Terms of Use：<https://t-ict4d.ictp.it/nequick2/terms-of-use>（使用 Web / 源码前自核）。

## 5. 获批后的建议编译清单（模板，无假日志）

以下为**到达邮件包之后**的检查单；占位符用真实文件名替换。未获包时整节可跳过。

```bash
cd ~/iono_ops/nequick2-ictp
# unzip -qo NeQuick2_*.zip && cd <解压根>
# find . -name '*.for' -o -name '*.f' -o -name '*.f90' | head
# ls *ccir* *modip* *solar* 2>/dev/null | head
# 按包内 README / Makefile 编译，例如：
# gfortran -O2 -std=legacy -o nequick2 *.for
# ./nequick2 < 包内样例输入 > out.txt && head out.txt
```

验收建议：

1. 用包内自带测试或文献算例（Nava et al., 2008）对 TEC 量级  
2. 同一几何再用 Web Model 粗对照（允许实现/积分差）  
3. **不要**与 [nequickg](./nequickg.md) Medium 表逐行比——输入物理量不同

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | 仓库里搜不到官方 zip | 邮件分发 | 按 §3 写信；勿造镜像 URL |
| 2 | 用 [nequickg](./nequickg.md) 的 `ai0` 驱动“NeQuick2” | 模型变体混淆 | R12/F10.7 ↔ NeQuick2；ai* ↔ NeQuick-G |
| 3 | Web 得 `undefined` / 空密度 | F10.7/R12 超页上范围 | 夹紧到提示区间再算 |
| 4 | 高程单位乱 | 常见米/公里混用 | Web/Fortran 均按文档 **km** 核对 |
| 5 | 获批包缺系数文件 | 只拷了 `.for` | 向维护者确认完整包；对照页述 ITU/modip |
| 6 | `gfortran` 固定格式报错 | 自由/固定格式混用 | 读包内编译说明；试 `-std=legacy` |
| 7 | 把 Web TEC 当论文金标准 | 无版本/无积分设置可引用 | 等 Fortran 包；引用 Nava 2008 + 包版本串 |
| 8 | 与 IRI TEC 差很大就“判死”一方 | 气候模型族不同 | 并列报告；见 [iri-fortran](./iri-fortran.md) |
| 9 | CI 里 `curl` 源码页当制品 | HTML≠源码 | CI 跳过或改人工 artifact |
| 10 | 忽略 Terms of Use | 科学分发有约束 | 打开 terms 页；邮件声明用途 |

## 7. 接到哪步

- 已开源 Galileo 路径：[nequickg](./nequickg.md)（本机可跑）→ 产品改 GSC C  
- IRI 金标准 / Python：[iri-fortran](./iri-fortran.md) · [iri2016](./iri2016.md) · [pyiri](./pyiri.md) · [pyirtam](./pyirtam.md)  
- 实测 TEC / GIM：[pytecgg](./pytecgg.md) · [ionex-gim](./ionex-gim.md) · [gnss-tec](./gnss-tec.md)  
- 概念：[04-iri-nequick](../tutorials/04-iri-nequick.md) · [data-access](../data-access.md)

## 8. 工作流（短）

1. 打开 [source-code](https://t-ict4d.ictp.it/nequick2/source-code) → 邮件 **bnava@ / yenca@** 申请  
2. 等待期间：Web Model 量级试算；并行跑 [nequickg](./nequickg.md) / [iri-fortran](./iri-fortran.md)  
3. 获批 → 按包 README 编译 → 自带算例验收 → 再接入自有射线几何  
4. 写结果时标明 **NeQuick 2（ICTP）≠ NeQuick-G**，并引用 Nava et al. (2008) + 包版本

## 9. 本机门禁结论（给质检）

| 检查项 | 结果 |
| --- | --- |
| 申请页可达 | 是（2026-09-24 06:12 EDT；质检复跑 06:15 EDT） |
| 匿名源码下载 | **否**（无 zip/tar href） |
| 本地 `gfortran` 构建 | **未执行**（无包） |
| 可引用的本机 TEC stdout | **无**（故意不编造） |
| Web 表单字段 | lat/lon/elev；R12 **[0,150]** / F10.7 **[63,193]**（页上 ITU-R P.1239） |
| 可公开替代 | Web Model；开源对照 [nequickg](./nequickg.md)（ai0/ai1/ai2；**勿**逐行比） |
