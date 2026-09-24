#!/usr/bin/env python3
"""Merge gnss-datasets portals into PROJECTS.json and regenerate docs/lists."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
# Ensure research/ is importable for sync_readme_counts (root or -m invocation).
import sys
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_readme_counts import sync_readme_counts
from _idempotent_io import append_notes_section, write_json_if_changed, write_text_if_changed
from _merge_fields import merge_project_fields

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
    lines.append(f"> **{len(items)}** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区")
    lines.append("")
    lines.append(meta["blurb"])
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

    write_text_if_changed(LISTS / meta["file"], "\n".join(lines).rstrip() + "\n")


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
    write_text_if_changed(DOCS / "data-access.md", text)


def main() -> None:
    catalog = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    portals = json.loads(PORTALS_PATH.read_text(encoding="utf-8"))
    projects = catalog["projects"]

    by_url = {norm_url(p["url"]): p for p in projects}
    existing_names = {p["name"] for p in projects}

    added = []
    updated = []
    skipped = []
    for f in portals:
        nu = norm_url(f["url"])
        if nu in by_url:
            incoming = {
                "license": f.get("license") or "",
                "language": f.get("language") or "",
                "provenance": f.get("provenance") or "",
                "desc_zh": f.get("one_liner_zh") or f.get("desc_zh") or "",
                "one_liner_zh": f.get("one_liner_zh") or "",
                "analysis_zh": f.get("analysis_zh") or "",
                "host": f.get("host") or "",
            }
            changed = merge_project_fields(by_url[nu], incoming)
            if changed:
                updated.append((f["name"], changed))
                print("UPDATE", f["name"], ",".join(changed))
                skipped.append((f["name"], "dup_url_enriched", f["url"]))
            else:
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
        by_url[nu] = entry
        existing_names.add(entry["name"])
        added.append(entry["name"])

    if not added and not updated:
        print("ADDED", 0)
        print("UPDATED", 0)
        print("SKIPPED", len(skipped))
        print("TOTAL", len(projects))
        print("SKIP_WRITE (no new portals; leave lists/categories/NOTES/PROJECTS/README untouched)")
        return

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
    write_json_if_changed(PROJECTS_PATH, catalog)

    # regenerate ALL lists (so counts stay consistent) — only rewrite gnss-datasets fully custom;
    # for others, lightly refresh header counts by reusing existing files would drift.
    # Safer: regenerate all categories with same table style as before.
    for cat, meta in CAT_META.items():
        write_list_generic(cat, meta, projects)

    write_data_access_doc()

    # categories.md
    cat_doc = []
    cat_doc.append("# 分类说明")
    cat_doc.append("")
    cat_doc.append("按「要解决什么问题」划分，不按编程语言。")
    cat_doc.append("")
    cat_doc.append("典型路径：数据/格式（RINEX/RTCM）→ 质检 → 电离层 TEC/GIM/闪烁、对流层 ZTD/PWV，或精密定位 RTK/PPP（常配合轨道钟差）；车载/机器人再接 GNSS/INS。另线：GNSS-SDR、手机原始测量 App。")
    cat_doc.append("")
    cat_doc.append("## 来源标记（provenance）")
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
    write_text_if_changed(DOCS / "categories.md", "\n".join(cat_doc))

    # README: sync counts only (preserve navigational template)
    sync_readme_counts(ROOT)

    total = len(projects)
    append_notes_section(
        ROOT / "NOTES.md",
        "## GNSS 数据源类扩充（2026-09-14）",
        f"- 新增类别 `gnss-datasets` → `lists/10-gnss-datasets.md`\n"
        f"- 写入 `research/data_portals.json`，本轮合并新增 **{len(added)}**\n"
        f"- 说明文档：`docs/data-access.md`（Earthdata/CDDIS、IGS 目录、注册徽章）\n"
        f"- 注册方式统计：{dict(reg_counts)}\n"
        f"- 未 git push\n\n"
        f"当前总条目：**{total}**（gnss-datasets={counts.get('gnss-datasets',0)}）\n",
    )

    print("ADDED", len(added))
    print("UPDATED", len(updated))
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
