# PPP-Wizard · CNES 整数零差 PPP-AR 操作手册

目录：[`PROJECTS.json` → `PPP-Wizard`](../../PROJECTS.json) · 门户 <http://www.ppp-wizard.net/> · 实时产品 <http://www.ppp-wizard.net/products/REAL_TIME/> · 联系 `contact_ppp@cnes.fr` · 许可 **上游未在门户明示（历史包为研究/非商业）** · **PROJECTS.json 无 GitHub 镜像** · 本机验证：`package.html` **404**（客户端需向 CNES 索取；本机**未**获包、**未**跑 PPP 解）；REAL_TIME **`cnt24373`**（2026-09-23）SP3/CLK/BIA 可下：SP3 **288** 历元 / **109** 星（G31+R19+E27+C32）；CLK `AS` **1 883 520** 行；BIA ≈**2.27 M** 行（`SOFTWARE PPP-Wizard`）· 2026-09-24 05:36 EDT · **质检复跑** 2026-09-24 05:41 EDT（`package.html` **404**；SP3 **288**/109=G31+R19+E27+C32/`ORBIT IGS20 IGU CNES`；CLK `AS` **1883520**；BIA **2268516** 行/`SOFTWARE PPP-Wizard`；解压大小 SP3≈**1.9 MB**/CLK≈**144 MB**/BIA≈**200 MB**；**无客户端包**未跑 PPP）

> 岗位：CNES **零差整数模糊度 PPP-AR** 示范（SSR 计算 + IGS-RTS 播发 + 用户端）。冲突时：**门户页 / IGS RTS 说明 / 你手中的 CNES 包 README > 本文**。发表级事后 PPP-AR → [pride-pppar](./pride-pppar.md)；轻量 CLI → [rtklib](./rtklib.md)；GA YAML → [ginan](./ginan.md)；武大 XML → [great-pvt](./great-pvt.md)。

## 1. 用途与边界

**做：**

- 证明 **undifferenced / integer** PPP-AR（相位偏差 + 轨道钟差 SSR）可在全球、无近参考站条件下到厘米级
- 门户侧：SSR 计算、Network/PPP Monitoring、Daily / REAL_TIME 产品（SP3+CLK+BIA；含 IONO/TROPO 子树）
- IGS 实时流：历史 CLK9x；现多记 **SSRA00CNE0 / SSRC00CNE0** 等（以 caster sourcetable 为准）
- 用户端（若申请到包）：改 RTKLIB/BNC 的轻量 C/C++ PPP 库 + 示例（ION GNSS 2015 述 v1.2）

**不做：**

- **不是** 开箱 `git clone` 即编的引擎——`package.html` **404**；PROJECTS.json **无** GitHub 镜像；勿把第三方残缺 fork 当官方
- **不是** 区域大气增强 / 密站网 RTK → [rtklib](./rtklib.md) / [claslib](./claslib.md)
- **不是** STEC/ROTI 产品链 → [pytecgg](./pytecgg.md) / [oasis-roti](./oasis-roti.md)
- 本页 **不能** 提供本机固定解坐标——无客户端包

一句话：PPP-Wizard = **CNES 整数 PPP-AR 示范门户 + SSR/偏差产品**；开源用户端需向 CNES 申请，CI 机通常只能验产品 I/O。

| 术语 | 含义 |
| --- | --- |
| PPP-WIZARD | Precise Point Positioning With Integer and Zero-difference Ambiguity Resolution Demonstrator |
| SSR | State Space Representation：轨道/钟差等低带宽改正 |
| OSB / BIA | 观测值相关码/相位偏差（Bias-SINEX）；AR 必需 |
| `cntWWWD` / `c2tWWWD` | REAL_TIME 日文件前缀（新 `cnt*`，旧档 `c2t*`）；`WWWD`≈GPS 周+星期 |
| CLK91 / SSRA00CNE0 | 历史/现行 CNES RTS 挂载名（以 sourcetable 为准） |

## 2. 安装 / 获取

### 2.1 诚实现状（2026-09）

| 组件 | 状态 |
| --- | --- |
| 门户首页 / SSR / Daily / Links | **HTTP 200** |
| `package.html`（历史下载页） | **404** |
| GitHub 官方镜像 | **PROJECTS.json 无条目** |
| REAL_TIME SP3/CLK/BIA | **可匿名 HTTP 下载**（本机已验 `cnt24373`） |
| IGS-RTS 挂载 | 需 IGS 账号；流名以 caster sourcetable 为准 |
| 用户端源码/Win 静态包 | 邮件 `contact_ppp@cnes.fr`；许可以回信/包内为准 |

### 2.2 本机可做：拉一日 REAL_TIME 产品

```bash
mkdir -p ~/iono_ops/ppp-wizard-products && cd ~/iono_ops/ppp-wizard-products
curl -sL -A 'Mozilla/5.0' 'http://www.ppp-wizard.net/products/REAL_TIME/' \
  | rg -o 'cnt[0-9]+\.(sp3|clk|bia)\.gz' | sort -u | tail
# 本机例：cnt24373 = GPS 周 2437 星期三 = 2026-09-23
for ext in sp3.gz clk.gz bia.gz; do
  curl -L -A 'Mozilla/5.0' -O "http://www.ppp-wizard.net/products/REAL_TIME/cnt24373.$ext"
done
gunzip -kf cnt24373.sp3.gz cnt24373.clk.gz cnt24373.bia.gz
head -n 25 cnt24373.sp3
rg -n "SOFTWARE|CONTACT|%=BIA" cnt24373.bia | head
```

**本机结果（写作 2026-09-24 05:36 EDT；质检复跑 05:41 EDT，字节以复跑为准）：**

| 文件 | 大小（解压后） | 探针 |
| --- | ---: | --- |
| `cnt24373.sp3` | ≈1.9 MB | **288** 历元 / **109** 星；`*  2026  9 23  0  0` → `23 55`；`ORBIT IGS20 IGU CNES` |
| `cnt24373.clk` | ≈144 MB | `AS` **1 883 520** 行 |
| `cnt24373.bia` | ≈200 MB | Bias-SINEX **2 268 516** 行；`SOFTWARE PPP-Wizard`；`CONTACT contact_ppp@cnes.fr` |

目录内仍有旧前缀 `c2t*`（如 2018 归档）与 `*_backup`；选文件先 `head` SP3 纪元，勿按文件名排序当“最新科学日”。

### 2.3 申请用户端（有包之后）

ION GNSS 2015 文（门户 Articles）描述包内大致含：PPP 库；改过的 RTKLIB/BNC；流采集与独立可执行文件；文档与示例。能力摘要：GPS(+GLO) 码相；GPS AR（相位偏差电文）；RAIM；单频 SBAS 电离层；断线后再收敛；多接收机。

```bash
# 伪流程——以你收到的压缩包说明为准
tar xf ppp-wizard-*.tar.gz && cd ppp-wizard-*/ && ls
# 读 README / licence；按文档链 RTKLIB 或独立 rover
```

**无包时不要臆造可执行文件名或固定率数字。**

## 3. 端到端

### 3.1 产品 I/O（本机已跑，无 PPP 引擎）

```bash
python3 - <<'PY'
from pathlib import Path
sp3 = Path('cnt24373.sp3').read_text(errors='replace').splitlines()
epochs = [l for l in sp3 if l.startswith('*')]
sats = sorted({l[1:4].strip() for l in sp3 if l.startswith('P')})
print('epochs', len(epochs), 'sats', len(sats))
print('G', sum(s.startswith('G') for s in sats),
      'R', sum(s.startswith('R') for s in sats),
      'E', sum(s.startswith('E') for s in sats),
      'C', sum(s.startswith('C') for s in sats))
print('first', epochs[0].strip()); print('last', epochs[-1].strip())
PY
```

期望量级：288 历元 / ≥100 星；首末同日 `00:00`…`23:55`。

### 3.2 产品 → 开源 PPP 引擎（旁路，推荐）

```bash
# 例：PRIDE PPP-AR / rtklib rnx2rtkp 浮点冒烟 / ginan pea / great-pvt XML
# 细节见各手册；勿照抄未验证坐标
```

对照：[pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [ginan](./ginan.md) · [great-pvt](./great-pvt.md)。

### 3.3 实时链（需 IGS 账号；本机未订流）

1. IGS RTS caster 取 sourcetable，确认 CNES 挂载（`SSRA00CNE0` / `SSRC00CNE0` 等）
2. [bnc](./bnc.md) / [pygnssutils](./pygnssutils.md) / [ntrip-client](./ntrip-client.md) 录流
3. 有用户端则按其 rover 喂 SSR+OBS；否则用支持 SSR/OSB 的引擎回放

## 4. I/O 与关键参数

| 输入 | 说明 |
| --- | --- |
| RINEX OBS（静止站；示范端历史限静止） | 双频码+相；GPS AR 为主 |
| SSR 流或 SP3+CLK | 与偏差产品同一分析中心/一致约定 |
| BIA / OSB | 相位+码偏差；缺则只能浮点 |
| ATX / ERP 等 | 按客户端或旁路引擎要求 |

| 输出 | 含义 |
| --- | --- |
| 实时监控坐标 / 残差 | 门户 Monitoring；用户端本地日志 |
| `cnt*.sp3/.clk/.bia` | 日归档，便于事后复现「实时条件」 |
| IONO/ / TROPO/ | REAL_TIME 子树；电离层/对流层网格类产品 |

## 5. 接到哪步

- 要可克隆的 PPP-AR 发表链 → [pride-pppar](./pride-pppar.md)；GA → [ginan](./ginan.md)；武大 → [great-pvt](./great-pvt.md)；轻量 → [rtklib](./rtklib.md)
- 只要偏差/SSR 概念与 HAS/CLAS/B2b 对照 → [cssrlib](./cssrlib.md) / [haslib](./haslib.md) / [claslib](./claslib.md) / [b2blib](./b2blib.md)
- 工作流 **D**：QC →（可选 CNES 产品）→ [pride-pppar](./pride-pppar.md)；教程 [06](../tutorials/06-iono-positioning.md)
- MATLAB GUI PPP → [rapppid](./rapppid.md)；低成本 MATLAB → [gogps-matlab](./gogps-matlab.md)

## 6. 坑（现象 → 原因 → 一条修复）

| # | 现象 | 原因 | 修复 |
| ---: | --- | --- | --- |
| 1 | `package.html` 404 | 下载页已撤 | 邮件 `contact_ppp@cnes.fr`；或改走 [pride-pppar](./pride-pppar.md) |
| 2 | 找不到官方 GitHub | 本来就没有进目录 | 以门户+邮件为准；勿信来路不明 zip |
| 3 | 只下到 `c2t*` 且历元是 2018 | 旧前缀归档仍挂在目录 | 改下 `cnt*`；`head` SP3 纪元确认 |
| 4 | 只有 SP3/CLK、AR 不起 | 缺相位 OSB | 同下 `*.bia.gz`；引擎打开 bias |
| 5 | 订 CLK91 失败 | 短名已退役/隐藏 | sourcetable 查 `SSRA00CNE0` 等新名 |
| 6 | 浮点好好、一开 AR 飘 | 偏差约定/信号映射错 | 先浮点；核对 OSB 与频点；换 [pride-pppar](./pride-pppar.md) 对照 |
| 7 | 当区域 RTK 用 | 方法不做密网大气 | 改 RTK/CLAS；读门户「NOT regional」 |
| 8 | 商用分发 Wizard 包 | 历史许可偏非商业 | 问 CNES；或换许可清晰引擎 |
| 9 | 监测页中断当产品挂了 | 2022 起网页监控降级 | 直接探 `products/REAL_TIME/` 与 RTS |
| 10 | 把本文探针当“今天你的解” | 产品日≠你的观测日 | 自选与 OBS 匹配的 `cntWWWD` 再解算 |
| 11 | BIA 枪 100 MB+ 磁盘满 | 全日 OSB 巨大 | 只下需要的一天；或流式处理 |
| 12 | 与 [great-pvt](./great-pvt.md) 差很大 | 产品/天线/约束不同 | 同 SP3/CLK/BIA/ATX；比收敛后段 |

## 7. 选型

| 你要… | 用 |
| --- | --- |
| 理解 CNES 整数 PPP-AR / 拉 CNES 偏差产品 | **本文 PPP-Wizard 门户+产品** |
| 开箱克隆的发表级 PPP-AR | [pride-pppar](./pride-pppar.md) |
| GA 现代化 pea | [ginan](./ginan.md) |
| 武大 GREAT XML | [great-pvt](./great-pvt.md) |
| 轻量 CLI 浮点/RTK | [rtklib](./rtklib.md) |

## 8. 相关

[pride-pppar](./pride-pppar.md) · [rtklib](./rtklib.md) · [ginan](./ginan.md) · [great-pvt](./great-pvt.md) · [cssrlib](./cssrlib.md) · [haslib](./haslib.md) · [rapppid](./rapppid.md) · [gogps-matlab](./gogps-matlab.md) · [data-access](../data-access.md) · [README](./README.md)

- 论文入口：门户 [links](http://www.ppp-wizard.net/links.html)（含 Laurichesse ION GNSS 2015 *Open-source PPP Client…*）
- 产品目录条目：`CNES-PPP-WIZARD-Realtime-Products`
