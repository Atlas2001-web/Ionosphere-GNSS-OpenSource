#!/usr/bin/env python3
"""Merge gnss-datasets portals into PROJECTS.json and regenerate docs/lists."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT / "PROJECTS.json"
PORTALS_PATH = ROOT / "research" / "data_portals.json"
LISTS = ROOT / "lists"
DOCS = ROOT / "docs"

REG_BADGE = {
    "open": "开放下载",
    "email_register": "邮件申请",
    "form_register": "网页注册",
    "account_approval": "账号审批",
    "institution_only": "机构限定",
    "unknown": "未确认",
}

CAT_META = {
    "ionosphere": {
        "title": "电离层 / Ionosphere",
        "file": "01-ionosphere.md",
        "blurb": "研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与 IRI/NeQuick 等模型对比；也包括 ROTI/闪烁与层析。",
        "who": "研究地球电离层电子含量与扰动：从 GNSS 双频观测估计 STEC/VTEC，构建 GIM，或与…",
    },
    "troposphere": {
        "title": "对流层 / Troposphere",
        "file": "02-troposphere.md",
        "blurb": "中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，以及与湿延迟相关的反射测量（GNSS-IR）。",
        "who": "中性大气延迟与 GNSS 气象：ZTD/ZHD/ZWD、VMF/GPT 映射、可降水量 PWV，…",
    },
    "gnss-data": {
        "title": "GNSS 数据与格式 / GNSS Data I/O",
        "file": "03-gnss-data.md",
        "blurb": "RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与 IGS 产品下载——所有解算的上游。",
        "who": "RINEX/SP3/CLK/ANTEX、RTCM/NTRIP、Hatanaka 压缩、质量检查与…",
    },
    "gnss-positioning": {
        "title": "精密定位 / Precise Positioning",
        "file": "04-gnss-positioning.md",
        "blurb": "SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优化定位。",
        "who": "SPP、DGPS、RTK/PPK、PPP/PPP-AR、网络 RTK 客户端，以及因子图等现代优…",
    },
    "orbit-clock": {
        "title": "轨道与钟差 / Orbit & Clock",
        "file": "05-orbit-clock.md",
        "blurb": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在大型套件中。",
        "who": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。",
    },
    "navigation-ins": {
        "title": "导航 / GNSS-INS",
        "file": "06-navigation-ins.md",
        "blurb": "GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。",
        "who": "GNSS 与 IMU（及视觉等）松/紧组合，车载与机器人户外定位。",
    },
    "gnss-sdr": {
        "title": "软件接收机与信号 / GNSS-SDR",
        "file": "07-gnss-sdr.md",
        "blurb": "从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。",
        "who": "从 IQ/采样到 PVT 的软件接收机，以及信号仿真与监控工具。",
    },
    "mobile-apps": {
        "title": "移动与嵌入式应用 / Mobile Apps",
        "file": "08-mobile-apps.md",
        "blurb": "手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。",
        "who": "手机/嵌入式上的 GNSS 测试、原始测量记录与简易定位。",
    },
    "tools-learning": {
        "title": "学习资源与工具 / Tools & Learning",
        "file": "09-tools-learning.md",
        "blurb": "awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。",
        "who": "awesome 列表、中文源码笔记、数据集、可见性可视化、SBAS/认证相关学习工具。",
    },
    "gnss-datasets": {
        "title": "GNSS 数据源 / GNSS Data Sources",
        "file": "10-gnss-datasets.md",
        "blurb": "已核验的 GNSS 相关数据门户与产品库：RINEX 观测/导航、SP3/CLK、IONEX/GIM、对流层格网、偏差产品、实时流、CORS 区域网、掩星与空间天气等。侧重「去哪里拿数据」，不是软件工具。",
        "who": "需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。",
    },
}


def norm_url(u: str) -> str:
    if not u:
        return ""
    u = u.strip()
    u = re.sub(r"^http://", "https://", u, flags=re.I)
    if "software.rtcm-ntrip.org" in u.lower():
        u = u.replace("https://", "http://")
    u = u.rstrip("/")
    u = re.sub(r"\.git$", "", u, flags=re.I)
    return u.lower()


def one_liner(p: dict) -> str:
    return p.get("one_liner_zh") or p.get("desc_zh") or p["name"]


def provenance_badge(prov: str) -> str:
    return {
        "official": "🏷️ 官方",
        "academic_lab": "🏷️ 高校实验室",
        "personal_community": "🏷️ 个人社区",
    }.get(prov, "🏷️ 个人社区")


def marker_text(p: dict) -> str:
    parts = [provenance_badge(p.get("provenance", "personal_community"))]
    ms = set(p.get("markers") or [])
    rel = p.get("user_relation")
    if rel == "owned" or "owned" in ms:
        parts.append("🚩")
    if rel == "forked" or "fork" in ms:
        parts.append("🔀 Fork")
    if rel == "starred" or "starred" in ms:
        parts.append("★ Star")
    if "core" in ms:
        parts.append("核心")
    return " · ".join(parts)


def stars_cell(p: dict) -> str:
    s = p.get("stars_approx")
    if s is None:
        s = p.get("stars")
    if s is None:
        return "—"
    return str(s)


def write_list_generic(cat: str, meta: dict, projects: list) -> None:
    items = [p for p in projects if p["category"] == cat]
    by_sub = defaultdict(list)
    for p in items:
        by_sub[p.get("subcategory") or "其他"].append(p)

    lines = [f"# {meta['title']}"]
    lines.append(f"> 共 **{len(items)}** 个已收录项目。本文件为链接索引，不含第三方源码。")
    lines.append("")
    lines.append(f"**这类做什么？** {meta['blurb']}")
    lines.append("")
    lines.append("来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。")
    lines.append("")

    for sub in sorted(by_sub.keys()):
        lines.append(f"## {sub}")
        lines.append("")
        if cat == "gnss-datasets":
            lines.append("| 项目 | 一句话 | 注册方式 | 标记 |")
            lines.append("|---|---|---|---|")
            for p in sorted(by_sub[sub], key=lambda x: x["name"].lower()):
                reg = REG_BADGE.get(p.get("registration") or "unknown", "未确认")
                lines.append(
                    f"| [{p['name']}]({p['url']}) | {one_liner(p)} | {reg} | {marker_text(p)} |"
                )
        else:
            lines.append("| 项目 | 一句话 | 语言 | ★ | 标记 |")
            lines.append("|---|---|---|---:|---|")
            for p in sorted(by_sub[sub], key=lambda x: (-(x.get("stars_approx") or 0), x["name"].lower())):
                lines.append(
                    f"| [{p['name']}]({p['url']}) | {one_liner(p)} | {p.get('language') or '—'} | {stars_cell(p)} | {marker_text(p)} |"
                )
        lines.append("")
        lines.append("### 详细说明")
        lines.append("")
        for p in sorted(by_sub[sub], key=lambda x: x["name"].lower()):
            if p.get("user_relation") == "owned" or "owned" in (p.get("markers") or []):
                lines.append(f"#### [{p['name']}]({p['url']})  ")
                lines.append(f"*{marker_text(p)}*")
                lines.append("")
                lines.append("维护者自有仓库，本索引仅作分类收录，不作详细介绍。请直接查看上游 README。")
                lines.append("")
                continue
            lines.append(f"#### [{p['name']}]({p['url']})  ")
            lines.append(f"*{marker_text(p)}*")
            lines.append("")
            if cat == "gnss-datasets":
                reg = p.get("registration") or "unknown"
                reg_zh = REG_BADGE.get(reg, "未确认")
                lines.append(
                    f"注册：`{reg}`（{reg_zh}） · 宿主：{p.get('host','—')} · 来源：{p.get('provenance','—')}"
                )
                lines.append("")
                if p.get("registration_zh"):
                    lines.append(f"**如何获取：** {p['registration_zh']}")
                    lines.append("")
                lines.append(p.get("analysis_zh") or one_liner(p))
                lines.append("")
            else:
                lic = p.get("license") or "—"
                lang = p.get("language") or "—"
                lines.append(f"语言：{lang} · 许可：{lic} · 星标约：{stars_cell(p)} · 宿主：{p.get('host','—')}")
                lines.append("")
                lines.append(p.get("analysis_zh") or one_liner(p))
                lines.append("")

    (LISTS / meta["file"]).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_data_access_doc() -> None:
    text = """# GNSS 数据获取说明（写给初学者）

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
"""
    (DOCS / "data-access.md").write_text(text, encoding="utf-8")


def main() -> None:
    catalog = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    portals = json.loads(PORTALS_PATH.read_text(encoding="utf-8"))
    projects = catalog["projects"]

    existing_urls = {norm_url(p["url"]) for p in projects}
    existing_names = {p["name"] for p in projects}

    added = []
    skipped = []
    for f in portals:
        nu = norm_url(f["url"])
        if nu in existing_urls:
            skipped.append((f["name"], "dup_url", f["url"]))
            continue
        if f["name"] in existing_names:
            skipped.append((f["name"], "dup_name", f["url"]))
            continue
        analysis = f["analysis_zh"]
        n = len(analysis)
        if n < 150 or n > 280:
            print(f"WARN length {n} for {f['name']}: {analysis[:40]}...")

        entry = {
            "name": f["name"],
            "url": f["url"],
            "desc_zh": f.get("one_liner_zh") or f["name"],
            "analysis_zh": analysis,
            "language": f.get("language") or "data-portal",
            "license": f.get("license") or "portal-terms",
            "category": "gnss-datasets",
            "subcategory": f.get("subcategory") or "其他",
            "markers": f.get("markers") or [],
            "stars_approx": None,
            "source": "data-portal verified 2026-09-14",
            "featured": "core" in (f.get("markers") or []),
            "user_relation": "none",
            "one_liner_zh": f.get("one_liner_zh") or "",
            "provenance": f.get("provenance") or "official",
            "host": f.get("host") or "official_site",
            "registration": f.get("registration") or "unknown",
            "registration_zh": f.get("registration_zh") or "",
        }
        projects.append(entry)
        existing_urls.add(nu)
        existing_names.add(entry["name"])
        added.append(entry["name"])

    cat_order = list(CAT_META.keys())
    projects.sort(
        key=lambda p: (
            cat_order.index(p["category"]) if p["category"] in cat_order else 99,
            p["name"].lower(),
        )
    )

    counts = Counter(p["category"] for p in projects)
    prov_counts = Counter(p.get("provenance") for p in projects)
    reg_counts = Counter(
        p.get("registration") for p in projects if p.get("category") == "gnss-datasets"
    )

    catalog["projects"] = projects
    catalog["project_count"] = len(projects)
    catalog["counts_by_category"] = {k: counts.get(k, 0) for k in cat_order}
    catalog["generated"] = date.today().isoformat()
    catalog["provenance_counts"] = {
        "official": prov_counts.get("official", 0),
        "academic_lab": prov_counts.get("academic_lab", 0),
        "personal_community": prov_counts.get("personal_community", 0),
    }
    # keep SH-GIM note
    if "SH-GIM" not in (catalog.get("note") or ""):
        catalog["note"] = (
            catalog.get("note")
            or "SH-GIM-proprietary is private and intentionally omitted from public lists."
        )
    PROJECTS_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # regenerate ALL lists (so counts stay consistent) — only rewrite gnss-datasets fully custom;
    # for others, lightly refresh header counts by reusing existing files would drift.
    # Safer: regenerate all categories with same table style as before.
    for cat, meta in CAT_META.items():
        write_list_generic(cat, meta, projects)

    write_data_access_doc()

    # categories.md
    cat_doc = []
    cat_doc.append("# 分类说明（写给初学者）")
    cat_doc.append("")
    cat_doc.append("本索引按「你要解决什么问题」划分，而不是按编程语言。下面用白话说明每一类在 GNSS 工作流里的位置。")
    cat_doc.append("")
    cat_doc.append("```")
    cat_doc.append("数据门户(RINEX/SP3/IONEX/CORS) ──► 格式工具/质检")
    cat_doc.append("         │")
    cat_doc.append("         ├─► 电离层 TEC/GIM / 闪烁指标")
    cat_doc.append("         ├─► 对流层 ZTD/PWV / VMF")
    cat_doc.append("         └─► 精密定位 RTK/PPP ──► 轨道钟差产品")
    cat_doc.append("                    │")
    cat_doc.append("                    └─► GNSS/INS / 视觉组合导航")
    cat_doc.append("")
    cat_doc.append("另线：GNSS-SDR（从无线电采样到伪距/相位）；手机 App（原始测量采集）")
    cat_doc.append("```")
    cat_doc.append("")
    cat_doc.append("## 来源 / 维护方标记（provenance）")
    cat_doc.append("")
    cat_doc.append("每条项目在 `PROJECTS.json` 中带有 `provenance` 字段，列表里显示为徽章：")
    cat_doc.append("")
    cat_doc.append("| 值 | 徽章 | 含义 |")
    cat_doc.append("|---|---|---|")
    cat_doc.append("| `official` | 🏷️ 官方 | 政府机构、国家实验室、国际联盟或官方服务站点维护的发行（如 ESA/GSC、BKG、NOAA/NGS、GSI、IGS 工具、TU Wien VMF、GFZ、EarthScope/UNAVCO 等） |")
    cat_doc.append("| `academic_lab` | 🏷️ 高校实验室 | 大学或研究所课题组发布、但并非国家测绘/航天主管部门官网的软件（如 UPC gAGE、武大 GREAT、CU Boulder SoftGPS 配套页等） |")
    cat_doc.append("| `personal_community` | 🏷️ 个人社区 | 个人开发者、小型社区团队或公司开源档（含 Anubis Free、多数 GitHub 个人仓等） |")
    cat_doc.append("")
    cat_doc.append("另有 `host` 字段标明托管位置：`github` / `gitlab` / `sourceforge` / `official_site` / `other`。")
    cat_doc.append("")
    cat_doc.append("数据源类（`gnss-datasets`）另有 `registration` 字段，说明见 [`data-access.md`](./data-access.md)。")
    cat_doc.append("")
    cat_doc.append("> 同一上游若存在 GitHub 镜像，目录优先保留**官方站点** URL，并在分析中注明镜像。")
    cat_doc.append("")

    for cat, meta in CAT_META.items():
        cat_doc.append(f"## `{cat}` — {meta['title'].split(' / ')[0]}")
        cat_doc.append("")
        cat_doc.append(meta["blurb"])
        cat_doc.append("")
        cat_doc.append(f"- 列表文件：[`lists/{meta['file']}`](../lists/{meta['file']})")
        cat_doc.append(f"- 当前条目数：**{counts.get(cat, 0)}**")
        cat_doc.append("")

    cat_doc.append("## 与用户仓库的关系标记")
    cat_doc.append("")
    cat_doc.append("| 标记 | 含义 |")
    cat_doc.append("|---|---|")
    cat_doc.append("| 🚩 自有 / owned | 维护者自有公开仓库（仅链接，不写详细介绍） |")
    cat_doc.append("| 🔀 Fork / fork | 维护者已 fork，表中仍列**上游** URL |")
    cat_doc.append("| ★ Star / starred | 出现在维护者 GitHub stars 中的种子 |")
    cat_doc.append("| 核心 / core | 本目录推荐优先阅读的代表性项目 |")
    cat_doc.append("")
    cat_doc.append("> 私有仓库（如 `SH-GIM-proprietary`）**不会**出现在公开索引中。")
    cat_doc.append("")
    (DOCS / "categories.md").write_text("\n".join(cat_doc), encoding="utf-8")

    # README
    total = len(projects)
    readme = []
    readme.append("# Ionosphere-GNSS-OpenSource")
    readme.append("")
    readme.append("**电离层 · 对流层 · GNSS · 导航（PNT）开源软件与数据源精选索引**  ")
    readme.append("Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation / Data portals")
    readme.append("")
    readme.append(f"[![Projects](https://img.shields.io/badge/verified%20projects-{total}-blue.svg)](./PROJECTS.json)")
    readme.append("[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)")
    readme.append("")
    readme.append("> **这是链接索引（curated index），不是代码大合集。**  ")
    readme.append("> 所有条目均为已核对的公开 URL；需要时请前往**上游仓库**克隆并遵守其许可证。")
    readme.append("")
    readme.append("---")
    readme.append("")
    readme.append("## 如何使用")
    readme.append("")
    readme.append("1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  ")
    readme.append("2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  ")
    readme.append("3. 数据门户登录与 IGS 目录说明：[docs/data-access.md](./docs/data-access.md)  ")
    readme.append("4. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json) · 数据源稿：[`research/data_portals.json`](./research/data_portals.json)  ")
    readme.append("5. 克隆上游，不要把第三方源码拷进本仓库")
    readme.append("")
    readme.append("### 标记")
    readme.append("")
    readme.append("| 标记 | 含义 |")
    readme.append("|:---:|---|")
    readme.append("| 🏷️ 官方 | 政府/机构/联盟官方发行 |")
    readme.append("| 🏷️ 高校实验室 | 大学课题组维护 |")
    readme.append("| 🏷️ 个人社区 | 个人或小团队/社区 |")
    readme.append("| 🚩 | 维护者自有公开仓库（仅收录链接，不写详细介绍） |")
    readme.append("| 🔀 | 维护者已 fork（表中列上游；fork 地址见项目页） |")
    readme.append("| ★ | 维护者 GitHub 星标种子 |")
    readme.append("| 核心 | 建议优先阅读 |")
    readme.append("")
    readme.append(
        f"来源统计：官方 **{prov_counts.get('official',0)}** · 高校实验室 **{prov_counts.get('academic_lab',0)}** · 个人社区 **{prov_counts.get('personal_community',0)}**"
    )
    readme.append("")
    readme.append("---")
    readme.append("")
    readme.append("## 分类一览")
    readme.append("")
    readme.append("| 分类 | 适合谁 | 列表 | 数量 |")
    readme.append("|---|---|---|---:|")
    for cat, meta in CAT_META.items():
        short = meta["title"].split(" / ")[0]
        readme.append(
            f"| **{short}** `{cat}` | {meta['who']} | [{meta['file']}](./lists/{meta['file']}) | {counts.get(cat, 0)} |"
        )
    readme.append(f"| **合计** | | [`PROJECTS.json`](./PROJECTS.json) | **{total}** |")
    readme.append("")
    readme.append("---")
    readme.append("")

    for cat, meta in CAT_META.items():
        items = [p for p in projects if p["category"] == cat]
        featured = [p for p in items if "core" in (p.get("markers") or []) or p.get("featured")]
        if not featured:
            featured = sorted(items, key=lambda x: (-(x.get("stars_approx") or 0), x["name"]))[:6]
        else:
            featured = featured[:8]
        readme.append(f"## {meta['title']}")
        readme.append("")
        readme.append(meta["blurb"])
        readme.append("")
        readme.append(f"完整列表与逐项分析 → [{meta['file']}](./lists/{meta['file']})")
        if cat == "gnss-datasets":
            readme.append("")
            readme.append("获取门槛说明 → [docs/data-access.md](./docs/data-access.md)")
        readme.append("")
        if cat == "ionosphere":
            readme.append(
                "本轮 IRI/GIRO 补录：[PyIRTAM](https://github.com/victoriyaforsythe/PyIRTAM) · "
                "[iricore](https://github.com/MIST-Experiment/iricore) · "
                "[IRTAM Fortran 读入器](https://giro.uml.edu/GAMBIT/IrtamReader_Fortran_V1.0.zip) · "
                "[SAO Explorer](https://ulcar.uml.edu/SAO-X/) · "
                "[ionex_reader](https://github.com/bbrawar/ionex_reader)"
            )
            readme.append("")
        readme.append("| 项目 | 简介 | 标记 |")
        readme.append("|---|---|---|")
        for p in featured:
            readme.append(f"| [{p['name']}]({p['url']}) | {one_liner(p)} | {marker_text(p)} |")
        readme.append("")

    readme.append("---")
    readme.append("")
    readme.append("## 许可与免责")
    readme.append("")
    readme.append(
        "本目录文本采用 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)。"
        "各上游项目保留其原许可证；闭源免费工具在条目中标注 `proprietary-freeware`；"
        "数据门户请遵守各站点使用条款与引用要求。"
    )
    readme.append("")
    (ROOT / "README.md").write_text("\n".join(readme), encoding="utf-8")

    notes_path = ROOT / "NOTES.md"
    notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    append = f"""

## GNSS 数据源类扩充（2026-09-14）

- 新增类别 `gnss-datasets` → `lists/10-gnss-datasets.md`
- 写入 `research/data_portals.json`，本轮合并新增 **{len(added)}**
- 说明文档：`docs/data-access.md`（Earthdata/CDDIS、IGS 目录、注册徽章）
- 注册方式统计：{dict(reg_counts)}
- 未 git push

当前总条目：**{total}**（gnss-datasets={counts.get('gnss-datasets',0)}）
"""
    notes_path.write_text(notes.rstrip() + append, encoding="utf-8")

    print("ADDED", len(added))
    print("SKIPPED", len(skipped))
    print("TOTAL", total)
    print("GNSS_DATASETS", counts.get("gnss-datasets", 0))
    print("REGISTRATION", dict(reg_counts))
    print("PROVENANCE", dict(prov_counts))
    for a in added:
        print(" +", a)
    for s in skipped:
        print(" skip", s)


if __name__ == "__main__":
    main()
