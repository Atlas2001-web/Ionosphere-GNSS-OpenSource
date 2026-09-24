#!/usr/bin/env python3
"""Merge web_finds, assign provenance/host to all projects, regenerate docs."""
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
from _idempotent_io import (
    append_notes_section,
    projects_substantively_equal,
    write_json_if_changed,
    write_text_if_changed,
)
from _merge_fields import merge_project_fields

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT / "PROJECTS.json"
WEB_FINDS = ROOT / "research" / "web_finds.json"
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
}

# GitHub org/user → provenance
OFFICIAL_OWNERS = {
    "geoscienceaustralia",
    "noaa-ngs",
    "google",
    "nlsfi",
    "embrace-inpe",
    "esa",
    "esa-navigate",
}
ACADEMIC_OWNERS = {
    "great-whu",
    "i2nav-whu",
    "pridelab",
    "sgl-ut",
    "ipnl-polyu",
    "gnss-lab",
    "stanford-navlab",
    "borglab",
    "oresat",
    "hkust-aerial-robotics",
    "jin-whu",
    "cssrg-kmitl",
    "gnss-sdr",
    "kristinemlarson",
    "geospace-code",
    "space-physics",
    "victoriyaforsythe",
    "insarlab",
    "ymcmrs",
    "whigg",
    "ucas-liuchunbo",
    "gyh-whu",
    "zhangwhu",
    "mayharrywang",
    "salmoshu",
    "h-shiono",
    "xiaogongwei",
    "zhufenggnss",
    "yxw027",
    "danipascual",  # GNSS-SDR related academic
    "gogps-project",
    "navlab",
    "cttc",
}

ENRICH = {
    "BNC": {
        "license": "GPL-3.0",
        "provenance": "official",
        "host": "official_site",
        "language": "C++",
        "one_liner_zh": "BKG 开源多流 Ntrip 客户端：收 RTCM 并可做实时 PPP",
        "analysis_zh": "德国 BKG 维护的开源多流 NTRIP 客户端，解码 RTCM 2/3，支持实时 PPP、高采样 RINEX 与质量编辑，提供 GUI 与批处理。源码 GPL-3，官方二进制见 BKG FTP。面向实时站运维与教研；微服务化部署需自行封装。",
        "desc_zh": "BKG Ntrip Client：多流接收与实时 PPP（GPL）",
    },
    "RNXCMP": {
        "license": "GSI terms (cite Hatanaka 2008)",
        "provenance": "official",
        "host": "official_site",
        "language": "C",
        "one_liner_zh": "日本地理院官方 Hatanaka/CompactRINEX 压缩与恢复工具",
        "analysis_zh": "GSI 的 RNXCMP（RNX2CRX/CRX2RNX）将 RINEX 2/3/4 观测与 CompactRINEX 互转，是 IGS 数据交换事实标准。官网提供多平台二进制与源码包，使用须遵循地理院条款并引用文献。GitHub 多为镜像，校验请用本页发行。",
        "desc_zh": "日本地理院 RNXCMP：Hatanaka 压缩官方工具",
    },
    "Anubis": {
        "license": "GPL-3.0 (Free); Pro commercial",
        "provenance": "personal_community",
        "host": "official_site",
        "language": "C++",
        "url": "https://gnutsoftware.com/software/anubis/",
        "one_liner_zh": "G-Nut/Anubis：多 GNSS RINEX/RTCM 质量检查（Free 开源）",
        "analysis_zh": "面向数据中心与用户的多星座观测质检工具，支持 RINEX 2/3 与 RTCM 元数据/定量/定性检查及简易 SPP。Free 档提供 Linux 源码（GPL-3）；Pro/实时为商业版。teqc EOL 后常用替代之一，本身不是精密定位引擎。",
        "desc_zh": "RINEX/RTCM 质量检查（Free 开源，Pro 商业）",
    },
    "TU-Wien-VMF-GPT-codes": {
        "license": "TU Wien site terms",
        "provenance": "official",
        "host": "official_site",
        "one_liner_zh": "TU Wien 官方 VMF1/VMF3/GPT/GMF 源码与格网目录",
        "analysis_zh": "维也纳工大公开的 VMF1/VMF3、GPT/GPT2w/GPT3、GMF、Saastamoinen 等 Fortran/MATLAB/C++ 实现与格网文件，是对流层映射与气象先验的权威入口。目录持续更新（含 vmf3_grid 等）。预报产品获取常需遵循站点注册要求；可与 STD_SWD_Calc 等脚本联用。",
    },
    "EGNOS-Toolkit": {
        "license": "EUPL",
        "provenance": "personal_community",
        "host": "sourceforge",
        "language": "C/C++",
        "one_liner_zh": "SourceForge EGNOS Toolkit：SBAS/EGNOS 消息与接收算法工具",
        "analysis_zh": "基于 EGNOS SDK 的 Linux/UNIX 移植，处理 SISNET、EMS 文件并实现用户端 SBAS 算法，许可 EUPL。托管于 SourceForge，更新偏旧。现代多星座 SBAS/HAS 研究需结合新文档与其他开源栈。",
    },
}

# Prefer official upstream for known mirrors
URL_REWRITE = {
    "https://github.com/nunojpg/ntripserver": {
        "url": "http://software.rtcm-ntrip.org/wiki/ntripserver",
        "provenance": "official",
        "host": "official_site",
        "license": "GPL",
        "one_liner_zh": "BKG POSIX ntripserver：把本地 GNSS 流推到 NTRIP 播发器",
        "analysis_zh": "RTCM-Ntrip 官方仓库中的 POSIX ntripserver，用于将接收机或文件流上传至 NtripCaster。源码见 software.rtcm-ntrip.org 浏览器。轻量适合嵌入式/服务器脚本；完整 GUI 与 PPP 请用 BNC。GitHub 上存在社区镜像。",
        "desc_zh": "BKG 官方 POSIX NTRIP 服务器端工具",
    },
    "https://github.com/nunojpg/ntripclient": {
        "url": "http://software.rtcm-ntrip.org/wiki/ntripclient",
        "provenance": "official",
        "host": "official_site",
        "license": "GPL",
        "one_liner_zh": "BKG POSIX ntripclient：命令行拉取 NTRIP 数据流",
        "analysis_zh": "官方轻量 NTRIP 客户端，从播发器订阅 RTCM 等流并写到标准输出或端口。源码位于 RTCM-Ntrip trunk。适合脚本化取流；需要解码/PPP/GUI 时改用 BNC。",
        "desc_zh": "BKG 官方 POSIX NTRIP 客户端",
    },
    "https://github.com/nunojpg/rtcm3torinex": {
        "url": "http://software.rtcm-ntrip.org/wiki/rtcm3torinex",
        "provenance": "official",
        "host": "official_site",
        "license": "GPL",
        "one_liner_zh": "BKG rtcm3torinex：RTCM3 流转 RINEX 的官方小工具",
        "analysis_zh": "RTCM-Ntrip 项目提供的 RTCM 3 到 RINEX 转换工具，便于把实时流转成事后文件。说明与附件见官方 wiki。功能聚焦转换；质检与编辑需搭配 Anubis/GFZRNX 等。",
        "desc_zh": "官方 RTCM3→RINEX 转换工具",
    },
}


def norm_url(u: str) -> str:
    if not u:
        return ""
    u = u.strip()
    u = re.sub(r"^http://", "https://", u, flags=re.I)
    # keep software.rtcm-ntrip.org as http-capable but normalize for dedup carefully
    if "software.rtcm-ntrip.org" in u.lower():
        u = u.replace("https://", "http://")
    u = u.rstrip("/")
    u = re.sub(r"\.git$", "", u, flags=re.I)
    return u.lower()


def detect_host(url: str) -> str:
    ul = url.lower()
    if "github.com" in ul:
        return "github"
    if "gitlab.com" in ul:
        return "gitlab"
    if "sourceforge.net" in ul:
        return "sourceforge"
    if any(
        d in ul
        for d in (
            "bkg.bund.de",
            "gsi.go.jp",
            "noaa.gov",
            "geodesy.noaa.gov",
            "unavco.org",
            "earthscope.org",
            "tuwien.ac.at",
            "irimodel.org",
            "gsc-europa.eu",
            "esa.int",
            "gfz.de",
            "gfz-potsdam.de",
            "ictp.it",
            "igs.org",
            "rtcm-ntrip.org",
            "upc.edu",
            "colorado.edu",
            "itu.int",
            "vdatum.noaa.gov",
            "gpsbabel.org",
            "gpsd.io",
            "pecny.cz",
            "gnutsoftware.com",
        )
    ):
        return "official_site"
    return "other"


def detect_provenance(url: str, name: str = "") -> str:
    ul = url.lower()
    m = re.match(r"https?://github\.com/([^/]+)/", ul)
    if m:
        owner = m.group(1).lower()
        if owner in OFFICIAL_OWNERS:
            return "official"
        if owner in ACADEMIC_OWNERS:
            return "academic_lab"
        return "personal_community"
    m = re.match(r"https?://gitlab\.com/([^/]+)/", ul)
    if m:
        owner = m.group(1).lower()
        if owner in {"earthscope", "gnss-sdr", "sgl-ut"}:
            return "official" if owner == "earthscope" else "academic_lab"
        if owner == "gpsd":
            return "personal_community"
        return "personal_community"
    # official site domains
    if any(
        d in ul
        for d in (
            "bkg.bund.de",
            "gsi.go.jp",
            "noaa.gov",
            "geodesy.noaa.gov",
            "unavco.org",
            "irimodel.org",
            "gsc-europa.eu",
            "esa.int",
            "gfz.de",
            "tuwien.ac.at",
            "ictp.it",
            "igs.org",
            "rtcm-ntrip.org",
            "vdatum.noaa.gov",
            "itu.int",
        )
    ):
        return "official"
    if any(d in ul for d in ("upc.edu", "colorado.edu", "pecny.cz", "gage.upc.edu")):
        return "academic_lab"
    if "gnutsoftware.com" in ul or "gpsbabel.org" in ul or "gpsd.io" in ul:
        return "personal_community"
    if "sourceforge.net" in ul:
        return "personal_community"
    return "personal_community"


def one_liner(p: dict) -> str:
    return p.get("one_liner_zh") or p.get("desc_zh") or p.get("name")


def provenance_badge(prov: str) -> str:
    return {
        "official": "🏷️ 官方",
        "academic_lab": "🏷️ 高校实验室",
        "personal_community": "🏷️ 个人社区",
    }.get(prov, "🏷️ 个人社区")


def marker_text(p: dict) -> str:
    parts = []
    parts.append(provenance_badge(p.get("provenance", "personal_community")))
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


def main() -> None:
    catalog = json.loads(PROJECTS_PATH.read_text())
    projects = catalog["projects"]
    original_projects = json.loads(json.dumps(projects, ensure_ascii=False))
    finds = json.loads(WEB_FINDS.read_text())

    existing = {norm_url(p["url"]): p for p in projects}
    # also index by name for enrich
    by_name = {p["name"]: p for p in projects}

    added = []
    skipped = []

    for f in finds:
        nu = norm_url(f["url"])
        if nu in existing:
            # enrich existing if same URL — never let empty/weak wipe QC fields
            ep = existing[nu]
            changed = merge_project_fields(ep, f)
            if changed:
                print("UPDATE", f["name"], ",".join(changed))
            skipped.append((f["name"], "dup_url_enriched" if changed else "dup_url", f["url"]))
            continue
        # name collision with different URL → keep both if truly different; skip thin meta if name exists
        if f["name"] in by_name:
            skipped.append((f["name"], "dup_name", f["url"]))
            continue

        entry = {
            "name": f["name"],
            "url": f["url"],
            "desc_zh": f.get("one_liner_zh") or f["name"],
            "analysis_zh": f["analysis_zh"],
            "language": f.get("language") or "",
            "license": f.get("license") or "",
            "category": f["category"],
            "subcategory": f.get("subcategory") or "",
            "markers": f.get("markers") or [],
            "stars_approx": f.get("stars"),
            "source": "web/official verified 2026-09-14",
            "featured": "core" in (f.get("markers") or []),
            "user_relation": "none",
            "one_liner_zh": f.get("one_liner_zh") or "",
            "provenance": f["provenance"],
            "host": f["host"],
        }
        projects.append(entry)
        existing[nu] = entry
        by_name[entry["name"]] = entry
        added.append(entry["name"])

    # Enrich known existing
    for name, fields in ENRICH.items():
        if name in by_name:
            p = by_name[name]
            old_url = p.get("url")
            for k, v in fields.items():
                p[k] = v
            if old_url and norm_url(old_url) != norm_url(p["url"]):
                # update index
                existing.pop(norm_url(old_url), None)
                existing[norm_url(p["url"])] = p

    # URL rewrites for mirrors → official
    for old, fields in URL_REWRITE.items():
        # find by old url
        target = None
        for p in projects:
            if norm_url(p["url"]) == norm_url(old) or p["url"].rstrip("/") == old.rstrip("/"):
                target = p
                break
        if not target:
            # maybe already rewritten
            continue
        oldn = norm_url(target["url"])
        for k, v in fields.items():
            target[k] = v
        existing.pop(oldn, None)
        existing[norm_url(target["url"])] = target

    # Special: keep GitHub gLAB mirror but mark personal; official already added as gLAB-UPC
    if "gLAB" in by_name:
        p = by_name["gLAB"]
        p["provenance"] = "personal_community"
        p["host"] = "github"
        p["desc_zh"] = "gLAB（UPC/ESA）非官方 Git 镜像——请优先用官方下载页"
        p["one_liner_zh"] = "gLAB 非官方镜像；官方发行见 UPC gAGE 下载页"
        if "gLAB-UPC" in by_name:
            p["analysis_zh"] = (
                "社区维护的 gLAB git 镜像，便于版本跟踪；官方二进制/源码与许可以 UPC gAGE 页面为准（本目录另收 gLAB-UPC）。"
                "核心 Apache、GUI LGPL。不要把镜像当作唯一权威来源。"
            )

    # Assign provenance/host to ALL
    for p in projects:
        if not p.get("host"):
            p["host"] = detect_host(p["url"])
        if not p.get("provenance"):
            p["provenance"] = detect_provenance(p["url"], p.get("name", ""))
        # ensure one_liner
        if not p.get("one_liner_zh"):
            p["one_liner_zh"] = p.get("desc_zh") or p["name"]
        # SH-GIM stays link-only
        if p.get("name") == "SH-GIM" or p.get("user_relation") == "owned":
            if "owned" not in (p.get("markers") or []):
                p.setdefault("markers", []).append("owned")

    # Dedup exact normalized URLs (keep first)
    seen = set()
    deduped = []
    for p in projects:
        nu = norm_url(p["url"])
        if nu in seen:
            continue
        seen.add(nu)
        deduped.append(p)
    projects = deduped

    # Sort: category order then name
    cat_order = list(CAT_META.keys())
    projects.sort(key=lambda p: (cat_order.index(p["category"]) if p["category"] in cat_order else 99, p["name"].lower()))

    counts = Counter(p["category"] for p in projects)
    prov_counts = Counter(p.get("provenance") for p in projects)

    # Idempotent: no adds and no substantive field/order changes → skip all writes.
    if not added and projects_substantively_equal(projects, original_projects):
        print("ADDED", 0)
        print("SKIPPED", len(skipped))
        print("TOTAL", len(projects))
        print("SKIP_WRITE (no new entries / no substantive updates)")
        return

    catalog["projects"] = projects
    catalog["project_count"] = len(projects)
    catalog["counts_by_category"] = {k: counts.get(k, 0) for k in cat_order}
    catalog["generated"] = date.today().isoformat()
    catalog["note"] = (
        catalog.get("note")
        or "Curated index of open GNSS/ionosphere software; verify upstream licenses before use."
    )
    write_json_if_changed(PROJECTS_PATH, catalog)

    # --- regenerate lists ---
    for cat, meta in CAT_META.items():
        items = [p for p in projects if p["category"] == cat]
        by_sub = defaultdict(list)
        for p in items:
            by_sub[p.get("subcategory") or "其他"].append(p)

        lines = []
        lines.append(f"# {meta['title'].split(' / ')[0]} / {meta['title'].split(' / ')[-1] if ' / ' in meta['title'] else meta['title']}")
        # simpler title from file naming
        lines = [f"# {meta['title']}"]
        lines.append(f"> **{len(items)}** 项 · 链接索引（无源码）· 🏷️ 官方 / 高校实验室 / 个人社区")
        lines.append("")
        lines.append(meta["blurb"])
        lines.append("")

        for sub in sorted(by_sub.keys()):
            lines.append(f"## {sub}")
            lines.append("")
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
                lic = p.get("license") or "—"
                lang = p.get("language") or "—"
                lines.append(f"语言：{lang} · 许可：{lic} · 星标约：{stars_cell(p)} · 宿主：{p.get('host','—')}")
                lines.append("")
                lines.append(p.get("analysis_zh") or one_liner(p))
                lines.append("")

        write_text_if_changed(LISTS / meta["file"], "\n".join(lines).rstrip() + "\n")

    # --- categories.md ---
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
        "## Web/官方扩充（2026-09-14）",
        f"- 新增经核验的非 GitHub/官方站点条目写入 `research/web_finds.json`（本轮合并新增 **{len(added)}**）\n"
        f"- 全量条目补齐 `provenance`（official / academic_lab / personal_community）与 `host`\n"
        f"- 列表与 README 增加 🏷️ 官方 / 高校实验室 / 个人社区 徽章\n"
        f"- 若干 GitHub 镜像改挂官方上游（ntripserver/client/rtcm3torinex）\n"
        f"- 未 git push\n\n"
        f"来源统计：official={prov_counts.get('official',0)}, academic_lab={prov_counts.get('academic_lab',0)}, personal_community={prov_counts.get('personal_community',0)}\n"
        f"当前总条目：**{total}**\n"
        f"新增名称：{', '.join(added) if added else '(none)'}\n",
    )

    # search log snippet (idempotent by heading)
    append_notes_section(
        ROOT / "research" / "search_log.md",
        "## Web expansion 2026-09-14",
        f"- web_finds.json: {len(finds)} candidates\n"
        f"- merged new: {len(added)}\n"
        f"- skipped: {len(skipped)}\n"
        f"- catalog total: {total}\n"
        f"- provenance: {dict(prov_counts)}\n",
    )

    print("ADDED", len(added))
    print("SKIPPED", len(skipped))
    print("TOTAL", total)
    print("PROVENANCE", dict(prov_counts))
    print("COUNTS", dict(counts))
    for a in added:
        print(" +", a)
    for s in skipped[:20]:
        print(" skip", s)


if __name__ == "__main__":
    main()
