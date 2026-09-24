#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge routine_finds_20260924j.json into PROJECTS.json and regenerate docs.

CRITICAL hygiene (round 4):
- Only APPEND projects whose norm_url is not already in the catalog.
- Do NOT rewrite existing project objects wholesale from finds.
- When regenerating lists, read the updated projects array as-is —
  never blank license/provenance/desc_zh/analysis_zh/one_liner_zh.
- Any accidental update path must keep old non-empty values when
  incoming is empty/missing: if old.get(k) and not new.get(k): keep old.
  (Also enforced via research._merge_fields.merge_project_fields.)
"""
from __future__ import annotations

import json
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
FINDS_PATH = ROOT / "research" / "routine_finds_20260924j.json"
LISTS = ROOT / "lists"
DOCS = ROOT / "docs"

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
        "blurb": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立开源小库较少，能力多集成在 Ginan、PRIDE-PPPAR、GROOPS 等大型套件中，本类刻意保持精简、不注水。",
        "who": "精密轨道确定、卫星钟差与相位偏差（UPD/OSB）等产品生成；独立小库较少，多见于大型套件。",
    },
    "navigation-ins": {
        "title": "导航 / Navigation & INS",
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
        "title": "GNSS 数据源 / GNSS Datasets",
        "file": "10-gnss-datasets.md",
        "blurb": "需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。",
        "who": "需要下载 RINEX/SP3/IONEX/CORS/实时流等 GNSS 数据产品的科研与工程用户。",
    },
}

PROV_BADGE = {
    "official": "🏷️ 官方",
    "academic_lab": "🏷️ 高校实验室",
    "personal_community": "🏷️ 个人社区",
}


def norm_url(u: str) -> str:
    return u.rstrip("/").lower()


def one_liner(p: dict) -> str:
    return p.get("one_liner_zh") or p.get("desc_zh") or p["name"]


def stars_cell(p: dict) -> str:
    s = p.get("stars_approx")
    if s is None:
        s = p.get("stars")
    if s is None:
        return "—"
    return str(s)


def marker_text(p: dict) -> str:
    parts = []
    prov = p.get("provenance")
    if prov in PROV_BADGE:
        parts.append(PROV_BADGE[prov])
    markers = p.get("markers") or []
    if p.get("user_relation") == "owned" or "owned" in markers:
        parts.append("🚩")
    if "fork" in markers or p.get("user_relation") == "fork":
        parts.append("🔀")
    if "starred" in markers or p.get("user_relation") == "starred":
        parts.append("★")
    if "core" in markers or p.get("featured"):
        parts.append("核心")
    return " ".join(parts) if parts else "—"


def finalize_new(f: dict) -> dict:
    """Pass through full schema entries; fill defaults if missing."""
    ol = f.get("one_liner_zh") or f.get("desc_zh") or f["name"]
    e = {
        "name": f["name"],
        "url": f["url"],
        "desc_zh": f.get("desc_zh") or ol,
        "analysis_zh": f["analysis_zh"],
        "language": f.get("language") or "",
        "license": f.get("license") or "",
        "category": f["category"],
        "subcategory": f.get("subcategory") or "",
        "markers": f.get("markers") or ["routine-2026-09-24j"],
        "stars_approx": f.get("stars_approx", f.get("stars")),
        "source": f.get("source") or "routine-finds-20260924j",
        "featured": bool(f.get("featured")) or ("core" in (f.get("markers") or [])),
        "user_relation": f.get("user_relation") or "none",
        "host": f["host"],
        "provenance": f["provenance"],
        "one_liner_zh": ol,
    }
    for opt in ("registration", "registration_zh"):
        if opt in f:
            e[opt] = f[opt]
    return e


def regenerate_lists(projects):
    for cat, meta in CAT_META.items():
        items = [p for p in projects if p["category"] == cat]
        by_sub = defaultdict(list)
        for p in items:
            by_sub[p.get("subcategory") or "其他"].append(p)

        lines = [
            f"# {meta['title']}",
            f"> **{len(items)}** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区",
            "",
            meta["blurb"],
            "",
        ]

        sub_order = []
        for p in items:
            sc = p.get("subcategory") or "其他"
            if sc not in sub_order:
                sub_order.append(sc)

        for sub in sub_order:
            group = by_sub[sub]

            def sort_key(x):
                star = x.get("stars_approx")
                if star is None:
                    star = x.get("stars") or 0
                sh = 0 if x["name"] == "SH-GIM" else 1
                return (sh, -star, x["name"].lower())

            group_sorted = sorted(group, key=sort_key)
            lines.append(f"## {sub}")
            lines.append("")
            lines.append("| 项目 | 一句话 | 语言 | ★ | 标记 |")
            lines.append("|---|---|---|---:|---|")
            for p in group_sorted:
                lines.append(
                    f"| [{p['name']}]({p['url']}) | {one_liner(p)} | {p.get('language') or '—'} | {stars_cell(p)} | {marker_text(p)} |"
                )
            lines.append("")
            lines.append("### 详细说明")
            lines.append("")
            for p in group_sorted:
                lines.append(f"#### [{p['name']}]({p['url']})  ")
                lines.append(f"*{marker_text(p)}*")
                lines.append("")
                if p.get("user_relation") == "owned" or "owned" in (p.get("markers") or []):
                    lines.append("维护者自有仓库，本索引仅作分类收录，不作详细介绍。请直接查看上游 README。")
                    lines.append("")
                    continue
                lic = p.get("license") or "—"
                lang = p.get("language") or "—"
                lines.append(f"语言：{lang} · 许可：{lic} · 星标约：{stars_cell(p)} · 宿主：{p.get('host', '—')}")
                lines.append("")
                lines.append(p.get("analysis_zh") or one_liner(p))
                lines.append("")

        write_text_if_changed(LISTS / meta["file"], "\n".join(lines).rstrip() + "\n")


def regenerate_categories(counts):
    cat_doc = [
        "# 分类说明",
        "",
        "按「要解决什么问题」划分，不按编程语言。",
        "",
        "典型路径：数据/格式（RINEX/RTCM）→ 质检 → 电离层 TEC/GIM/闪烁、对流层 ZTD/PWV，或精密定位 RTK/PPP（常配合轨道钟差）；车载/机器人再接 GNSS/INS。另线：GNSS-SDR、手机原始测量 App。",
        "",
        "## 来源标记（provenance）",
        "",
        "每条项目在 `PROJECTS.json` 中带有 `provenance` 字段，列表里显示为徽章：",
        "",
        "| 值 | 徽章 | 含义 |",
        "|---|---|---|",
        "| `official` | 🏷️ 官方 | 政府机构、国家实验室、国际联盟或官方服务站点维护的发行（如 ESA/GSC、BKG、NOAA/NGS、GSI、IGS 工具、TU Wien VMF、GFZ、EarthScope/UNAVCO 等） |",
        "| `academic_lab` | 🏷️ 高校实验室 | 大学或研究所课题组发布、但并非国家测绘/航天主管部门官网的软件（如 UPC gAGE、武大 GREAT、CU Boulder SoftGPS 配套页等） |",
        "| `personal_community` | 🏷️ 个人社区 | 个人开发者、小型社区团队或公司开源档（含 Anubis Free、多数 GitHub 个人仓等） |",
        "",
        "另有 `host` 字段标明托管位置：`github` / `gitlab` / `sourceforge` / `official_site` / `other`。",
        "",
        "> 同一上游若存在 GitHub 镜像，目录优先保留**官方站点** URL，并在分析中注明镜像。",
        "",
    ]
    for cat, meta in CAT_META.items():
        cat_doc.append(f"## `{cat}` — {meta['title'].split(' / ')[0]}")
        cat_doc.append("")
        cat_doc.append(meta["blurb"])
        cat_doc.append("")
        cat_doc.append(f"- 列表文件：[`lists/{meta['file']}`](../lists/{meta['file']})")
        cat_doc.append(f"- 当前条目数：**{counts.get(cat, 0)}**")
        cat_doc.append("")
    cat_doc += [
        "## 与用户仓库的关系标记",
        "",
        "| 标记 | 含义 |",
        "|---|---|",
        "| 🚩 自有 / owned | 维护者自有公开仓库（仅链接，不写详细介绍） |",
        "| 🔀 Fork / fork | 维护者已 fork，表中仍列**上游** URL |",
        "| ★ Star / starred | 出现在维护者 GitHub stars 中的种子 |",
        "| 核心 / core | 本目录推荐优先阅读的代表性项目 |",
        "",
        "> 私有仓库（如 `SH-GIM-proprietary`）**不会**出现在公开索引中。",
        "",
    ]
    write_text_if_changed(DOCS / "categories.md", "\n".join(cat_doc))


def regenerate_readme(projects, counts, prov_counts):
    """Sync counts into navigational README; never rebuild the old catalog wall."""
    sync_readme_counts(ROOT)


def main():
    catalog = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    projects = catalog["projects"]
    finds = json.loads(FINDS_PATH.read_text(encoding="utf-8"))

    by_url = {norm_url(p["url"]): p for p in projects}
    existing_names = {p["name"] for p in projects}

    added = []
    updated = []
    for raw in finds:
        assert "旨在" not in raw["analysis_zh"] and "赋能" not in raw["analysis_zh"]
        assert "旨在" not in raw["one_liner_zh"] and "赋能" not in raw["one_liner_zh"]
        nu = norm_url(raw["url"])
        if nu in by_url:
            # Append-only preferred; if URL already exists, only fill blanks.
            # Never clobber non-empty enrichment with empty/missing incoming.
            incoming = finalize_new(raw)
            existing = by_url[nu]
            for k, v in list(incoming.items()):
                if existing.get(k) and not v:
                    incoming[k] = existing[k]  # if old.get(k) and not new.get(k): keep old
            changed = merge_project_fields(existing, incoming)
            if changed:
                updated.append((raw["name"], changed))
                print("UPDATE", raw["name"], ",".join(changed))
            else:
                print("SKIP url", raw["name"], raw["url"])
            continue
        if raw["name"] in existing_names:
            print("SKIP name", raw["name"])
            continue
        e = finalize_new(raw)
        nchars = len(e["analysis_zh"])
        if nchars < 120 or nchars > 320:
            print(f"WARN length {e['name']}: {nchars}")
        projects.append(e)
        by_url[nu] = e
        existing_names.add(e["name"])
        added.append(e)

    if not added and not updated:
        print("ADDED", 0)
        print("UPDATED", 0)
        print("TOTAL", len(projects))
        print("SKIP_WRITE (no new entries / no enrichment updates; leave lists/categories/NOTES/PROJECTS/README untouched)")
        return

    counts = Counter(p["category"] for p in projects)
    prov_counts = Counter(p.get("provenance") for p in projects)
    catalog["projects"] = projects
    catalog["project_count"] = len(projects)
    catalog["counts_by_category"] = {k: counts.get(k, 0) for k in CAT_META}
    catalog["provenance_counts"] = {
        "official": prov_counts.get("official", 0),
        "academic_lab": prov_counts.get("academic_lab", 0),
        "personal_community": prov_counts.get("personal_community", 0),
    }
    catalog["generated"] = date.today().isoformat()
    catalog["updated"] = date.today().isoformat()

    write_json_if_changed(PROJECTS_PATH, catalog)

    regenerate_lists(projects)
    regenerate_categories(counts)
    regenerate_readme(projects, counts, prov_counts)

    if added:
        append_notes_section(
            ROOT / "NOTES.md",
            "## 例行检索补录（2026-09-24j）",
            (
                f"- 新增 **{len(added)}** 条（azarashi/QZQSM/libswiftnav/NavAI/ionFR/gps-fpga/gnsshat、ESSP-EGNOS、LINZ、IERS、NOAA-WMM 等）\n"
                + f"- 当前条目：**{catalog['project_count']}**\n"
                + f"- 分类计数：{dict(catalog['counts_by_category'])}\n"
                + f"- 详见 `research/routine_finds_20260924j.json`\n"
            ),
        )

    print("ADDED", len(added))
    print("UPDATED", len(updated))
    print("TOTAL", catalog["project_count"])
    print("COUNTS", dict(catalog["counts_by_category"]))
    print("PROV_NEW", Counter(a["provenance"] for a in added))
    for a in added:
        print(f"  + {a['name']:42s} {a['category']:18s} {a['provenance']:20s} stars={a['stars_approx']}")


if __name__ == "__main__":
    main()
