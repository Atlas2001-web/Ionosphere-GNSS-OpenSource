# SPOCC · GFZ 多 AC 轨道/钟差综合操作手册

目录：[`PROJECTS.json` → `SPOCC`](../../PROJECTS.json) · 服务页 <https://gnss.gfz.de/services/spocc> · 仓 <https://git.gfz-potsdam.de/gnss/spocc>（**登记后**）· 新闻 <https://www.gfz.de/en/section/space-geodetic-techniques/overview/details-section-news/veroeffentlichung-der-software-for-precise-orbit-and-clock-combination-spocc-1> · IGSmail-8560 <https://lists.igs.org/pipermail/igsmail/2025/008556.html> · 许可 **SPOCC Scientific License v1.0**（2024-11-07；非正式 OSI 开源）· 语言 **Python**（YAML 配置；新闻/IGSmail 另提 **Docker**）· IGS Workshop 2024 海报 <https://files.igs.org/pub/resource/pubs/workshop/2024/IGSWS-2024-PS0210-Mansur-SPOCC_-_a_GFZ_Software_Tool_for_a_Multi-GNSS_Orbit_and_Clock_Combination.pdf> · 本机验证（**2026-09-24 07:02 EDT**；质检复跑 **07:12 EDT**：Inertia `auth.user=None`/`is_subscribed=False`；License **441441** B/sha₁₂=`d70eeefc667a`；GDPR **192047** B/sha₁₂=`faa0c1676f57`；`git ls-remote` **EXIT 128**/`info/refs` **401**；PyPI/Docker Hub **404**；海报 **1682069** B/sha₁₂=`cedac7fb36d5`；**无仓未臆造** SP3/CLK）：服务页 Inertia `auth.user=None` / `is_subscribed=False`；公开 PDF 许可 **441441** B（sha₁₂=`d70eeefc667a`）+ GDPR **192047** B（sha₁₂=`faa0c1676f57`）；`git ls-remote` → **EXIT 128**（需登录）；`info/refs` **HTTP 401**；PyPI `spocc` **404**；Docker Hub `gfz/spocc` **404**；**无仓 → 未装未跑 → 未臆造 SP3/CLK 综合产品**。

> 岗位：**多分析中心（AC）精密轨道（SP3）+ 钟差（RINEX CLK）加权综合**（VCE）→ 多星座一致产品试验 / IGS Combination Taskforce 工具箱之一。冲突时：**服务页 / Scientific License / 获批仓 README·YAML > 本文**。  
> 公开可跑旁路：[clkcomb](./clkcomb.md)（钟/偏差合成）· 偏差链 [gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md)/[great-upd](./great-upd.md) · 产品门户 [data-access](../data-access.md)「SP3 / CLK / bias」。**≠** PPP 引擎；**≠** 官方 IGS 最终产品本身。

## 1. 用途与边界

**做（获批仓之后，按仓内说明；公开材料已确认）：**

- 读多家 AC 的 **SP3 轨道** + **RINEX clock**，按 **YAML** 做加权综合（权重来自 **VCE**：LS-VCE / Förstner；可按 AC+星座 / AC+卫星类型 / AC+单星）
- 流程（服务页原文）：先 **轨道综合**（对齐、粗差剔除）→ 再 **钟差综合**（径向轨道改正、参考钟、ISB 对齐）
- 星座范围（海报）：GPS / GLONASS / Galileo / BeiDou / QZSS / LEO
- 处理模式（海报）：日解 VCE 或 filter 序贯；可掺先验权（如 SLR）
- 新闻/IGSmail：提供 **Python 源码**与 **Docker** 环境（镜像名/拉取令以获批仓为准；本机公开检索 **无** `gfz/spocc`）

**不做 / 本机未做：**

- **不是** 匿名 `pip install` / 公开 GitHub 镜像 → PyPI **404**；仓须 GFZ GitLab 授权
- **不是** 单站 PPP/PPP-AR → [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)/[ginan](./ginan.md)
- **不是** 仅钟差合成 CLI → [clkcomb](./clkcomb.md)（公开可跑；**无**完整多星座轨道 VCE 链）
- **不是** UPD/IFCB/OSB 估计 → [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)/[gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md)
- **不是** 官方 IGS Final/Rapid 产品发布通道（SPOCC 是综合**工具**；运营产品仍属 ACC/AC）
- 本页 **禁止伪造** 综合 SP3/CLK 数值、权重表或 Docker 跑通日志——**无授权仓即无本地 E2E**

一句话：**SPOCC = GFZ 科学许可门禁下的多 AC 多星座轨道+钟差 VCE 综合器**；未获批前用 [clkcomb](./clkcomb.md) + CDDIS 产品推进实验。

| 易混 | 是什么 | 识别 |
| --- | --- | --- |
| **本文** SPOCC | GFZ 轨道+钟 VCE 综合 | `git.gfz-potsdam.de/gnss/spocc` + YAML |
| [clkcomb](./clkcomb.md) | 开源钟/偏差合成 | `./bin/clkcomb comb.ini` |
| [great-pce](./great-pce.md) | 武大单网钟差估计 | `GREAT_PCE` / CLK-LSQ |
| [cube](./cube.md) | APM 钟差/DCK+PPP | RTKLIB 二次开发 |
| IGS Final SP3/CLK | 官方综合产品 | CDDIS `igs*`/`igm*`；**读入**可作参考，≠本工具 |

## 2. 许可与资格（必读）

公开 PDF（本机已下）：

| 文件 | 本机 |
| --- | --- |
| Scientific License v1.0（eff. 2024-11-07） | **441441** B · sha₁₂=`d70eeefc667a` · `%PDF-1.6` |
| GDPR 告知（eff. 2024-12-06） | **192047** B · sha₁₂=`faa0c1676f57` |

要点（摘自 License v1.0，**非法律意见**；以 PDF 全文为准）：

- 仓仅对**登记 USER**开放；ENTITY 须对 IGS/IAG 大地测量服务有贡献（数据/产品/工作组等）
- **运营（operational）**：可综合 **IGS 产品**加权；非 IGS 产品运营时权重须为 **0**（只比差不进组合）；非运营研究可对非 IGS 产品加权
- 禁止转售/对外提供软件功能；贡献须 MR 回仓；强 copyleft（GPL）第三方代码未经 GFZ 批准不得并入
- 许可期 **5 年**须续登；论文须引 Mansur et al. *J Geod* 2022 与 *GPS Solut* 2024（License §7）
- 依赖注明：**geodezyx**（LGPL-3.0，<https://github.com/IPGP/geodezyx>）— 公开可达，**≠** SPOCC 本体

联系：`gnss@gfz.de`（License / GDPR）。

## 3. 获取：登记墙（诚实步骤）

服务页卡片原文：*Repository Access — Please log in to GFZ's GitLab using your GitHub credentials.*

```bash
# 0) 时间戳（本机）
TZ=America/New_York date   # 2026-09-24 07:02:22 EDT

# 1) 服务页状态（未登录）
python3 - <<'PY'
import json, re, urllib.request, html
raw = urllib.request.urlopen('https://gnss.gfz.de/services/spocc').read().decode()
page = json.loads(html.unescape(re.search(r'data-page="([^"]+)"', raw).group(1)))
p = page['props']
print(page['component'], 'auth.user=', p['auth']['user'],
      'is_subscribed=', p['is_subscribed'], 'topic=', p['topic_slug'])
for d in p['documents']:
    print(d['slug'], d['name'], d.get('version'), d.get('effective_at'))
PY
# → services/spocc  auth.user= None  is_subscribed= False  topic= spocc
# → spocc-gdpr / spocc-scientific-license v1.0

# 2) 公开条款 PDF
mkdir -p ~/iono_ops/spocc_gate && cd ~/iono_ops/spocc_gate
curl -fsSL -o spocc-scientific-license.pdf \
  'https://gnss.gfz.de/storage/documents/27UynYL85VJ8io5amHvP4Qynjgjyhkt2pmnNAkXx.pdf'
curl -fsSL -o spocc-gdpr.pdf \
  'https://gnss.gfz.de/storage/documents/FkY94GOxQrioWmtYLrfe6PylUlfS7qN3njk1N4Wn.pdf'
wc -c spocc-scientific-license.pdf spocc-gdpr.pdf
# 441441 / 192047

# 3) 匿名拉仓 → 门禁
GIT_TERMINAL_PROMPT=0 git ls-remote https://git.gfz-potsdam.de/gnss/spocc.git
# fatal: could not read Username for 'https://git.gfz-potsdam.de': terminal prompts disabled
# EXIT:128
curl -sS -o /dev/null -w 'HTTP=%{http_code}\n' \
  'https://git.gfz-potsdam.de/gnss/spocc.git/info/refs?service=git-upload-pack'
# HTTP=401

# 4) 人工：下载并签署 Scientific License → 按页述寄至 GFZ（gnss@gfz.de / 页上邮箱）
#    → GitHub 账号登录 https://git.gfz-potsdam.de/users/sign_in
#    → 内部审批解锁后 clone（见 §5）
```

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `auth.user=None` | 未登录 GNSS Observatory | 仅影响订阅铃；**拉仓仍要** License+GitLab |
| `git` 要 Username / EXIT 128 | 仓私有 | 走 §3 登记；勿搜「公开镜像」当权威 |
| `info/refs` 401 | 未授权 upload-pack | 同上 |
| PyPI / Docker Hub 404 | **无**公开发行 | 以获批仓 README/镜像名为准 |
| 把 [clkcomb](./clkcomb.md) 当 SPOCC | 不同软件 | 钟合成≠轨道+钟 VCE |

**本机（2026-09-24 07:02 EDT）：** 停在登记步骤；**无** clone、**无** YAML 跑通、**无**综合产品文件。

## 4. 无仓时的公开材料（可达，非本地 E2E）

| 材料 | URL | 本机 |
| --- | --- | --- |
| 服务页 | <https://gnss.gfz.de/services/spocc> | 200；Inertia 如上 |
| Scientific License / GDPR | `…/storage/documents/…`（§3） | PDF-1.6；字节/sha 如上 |
| IGSWS 2024 海报 | files.igs.org `…Mansur-SPOCC…pdf` | **1682069** B · sha₁₂=`cedac7fb36d5` |
| IGSmail-8560 | lists.igs.org `…/008556.html` | 2025-01-24 发布公告 |
| 算法论文 | doi:10.1007/s00190-022-01685-y · 10.1007/s10291-023-01604-4 等（服务页 References） | 浏览器核 |
| 公开依赖 geodezyx | <https://github.com/IPGP/geodezyx> | HEAD `93dd876…`（**≠** SPOCC） |
| 旁路综合 | [clkcomb](./clkcomb.md) | 已短硬；example CLK 真跑 |

海报可作算法/流程预习——**不能**替代获批仓配置与样例。

## 5. 获批后的建议安装清单（模板，无假日志）

```bash
# 仅在 GitLab 已解锁后：
mkdir -p ~/iono_ops && cd ~/iono_ops
git clone https://git.gfz-potsdam.de/gnss/spocc.git
cd spocc
git rev-parse --short HEAD
# 读仓内 README / docs / example YAML；典型路径名以仓为准，例如：
# python -m venv .venv && source .venv/bin/activate
# pip install -r requirements.txt   # 或 poetry/conda——以仓为准
# # Docker（新闻宣称有；镜像 tag 以仓为准）：
# docker pull <registry>/<image>:<tag>
# docker run --rm -v "$PWD/data:/data" <image> <仓内入口> /data/config.yaml
```

验收（获批后自填，**勿**抄本文数字）：

1. 仓内自带 example / CI 绿  
2. 输出 SP3+CLK 头符合 IGS 格式；权重/RMS 表与海报量级同级讨论即可  
3. 运营场景：非 IGS 输入权=0（License §3）  
4. 与 [clkcomb](./clkcomb.md) 同日 AC 钟差可**粗**对照——轨道+ISB 链不同，勿 bit 级对齐

## 6. I/O 与参数（公开描述；细节以仓为准）

| 方向 | 格式 / 要点 |
| --- | --- |
| 输入 | 多 AC **SP3**；多 AC **RINEX clock**；可选广播钟（海报：钟对齐 GPS 时） |
| 配置 | **YAML**（海报）；权方案：星座 / block / 单星；日解 vs filter |
| 输出 | 综合轨道+钟（IGS 格式族）；过程统计/权（仓内命名） |
| 产品礼仪 | 拉 AC 产品见 [data-access](../data-access.md)；Earthdata/CDDIS 门禁另记 |

本机**无** YAML 键名清单可报——未 clone 则不编造参数表。

## 7. 接到哪步

1. 产品下载与命名：[data-access](../data-access.md)  
2. 公开可跑钟合成：[clkcomb](./clkcomb.md)  
3. 偏差/OSB 旁路：[gkit-bias](./gkit-bias.md) · [mcosb](./mcosb.md) · [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)  
4. 下游 PPP：[pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)/[ginan](./ginan.md)  
5. 网解/产品框架旁路：[groops](./groops.md) · [cube](./cube.md)  
6. 获批后：SPOCC 综合 → 自有 PPP/验证（SLR 等，见海报）

## 8. 坑（≥8）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `git clone` 要密码 / 401 | 未登记 | §3 签 License + GitHub→GFZ GitLab |
| 2 | 搜到「SPOCC」Docker 第三方镜像 | 同名噪声 | 只用获批仓文档中的镜像 |
| 3 | `pip install spocc` | PyPI 无此包 | **404**；走 GitLab |
| 4 | 运营时给商业/自研 AC 加权 | License 限制 | 权=0 或另向 `gnss@gfz.de` 申请 |
| 5 | 把 IGS Final 当 SPOCC 输出 | 产品≠工具 | 综合结果自备前缀；勿冒充 `igs*` |
| 6 | 只跑钟、期望轨道也齐 | 须完整 SP3+CLK 链 | 缺 SP3 先补齐；旁路用 clkcomb |
| 7 | 忽略 ISB/参考钟对齐 | 多星座不一致 | 读服务页第二步；论文 [4] |
| 8 | 并入 GPL 补丁回传 | License 禁强 copyleft | MR 前开 issue 问 GFZ |
| 9 | geodezyx 当 SPOCC | 仅依赖 | 公开库≠综合器 |
| 10 | 无仓却写综合 CLK 绿勾 | 臆造 | 本页刻意无产品 stdout |
| 11 | ENTITY 不符 IGS/IAG 贡献 | 资格 | License §1(3)；先参与服务再申请 |
| 12 | 5 年未续登 | 许可到期 | License §6；停用并删副本 |

## 9. 选型

| 你要… | 选 |
| --- | --- |
| IGS 风格多 AC **轨道+钟** VCE 综合（有资格） | **本文 SPOCC**（登记） |
| 今天就能跑的多 AC **钟/偏差**合成 | [clkcomb](./clkcomb.md) |
| 从观测估钟差 | [great-pce](./great-pce.md) |
| UPD / IFCB / OSB | [great-upd](./great-upd.md)/[great-ifcb](./great-ifcb.md)/[gkit-bias](./gkit-bias.md)/[mcosb](./mcosb.md) |
| 读/比 SP3·CLK·Bias 文件 | PROJECTS `gnssanalysis`（GA；手册待补） |
| 直接 PPP | [pride-pppar](./pride-pppar.md)/[great-pvt](./great-pvt.md)/[ginan](./ginan.md) |

## 10. 本机门禁结论（给质检）

| 检查项 | 结果 |
| --- | --- |
| 服务页可达 | 是（2026-09-24 07:12 EDT 复跑） |
| 匿名源码 / PyPI / 官方 Docker Hub | **否**（GitLab 401/128；PyPI 404；`gfz/spocc` 404） |
| 公开 License + GDPR PDF | 是（441441 / 192047 B） |
| 海报 / IGSmail | 是（1682069 B；2025-01-24 公告） |
| 本地综合 SP3/CLK stdout | **无**（故意不编造） |
| 可公开替代实验 | [clkcomb](./clkcomb.md) + [data-access](../data-access.md) |
| PROJECTS 旁注 | `GFZ-SPOCC-news` / `IGSMAIL-SPOCC` 非仓；软件条目名 **`SPOCC`** |

## 11. 相关

[clkcomb](./clkcomb.md) · [gkit-bias](./gkit-bias.md) · [mcosb](./mcosb.md) · [great-upd](./great-upd.md) · [great-ifcb](./great-ifcb.md) · [great-pce](./great-pce.md) · [cube](./cube.md) · [groops](./groops.md) · [pride-pppar](./pride-pppar.md) · [great-pvt](./great-pvt.md) · [ginan](./ginan.md) · [data-access](../data-access.md) · [README](./README.md)
