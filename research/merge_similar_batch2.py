#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge batch-2 similar finds into PROJECTS.json; normalize incomplete entries; regenerate docs."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path("/workspace/ionosphere-gnss-catalog")
PROJECTS_PATH = ROOT / "PROJECTS.json"
SIMILAR_PATH = ROOT / "research" / "similar_finds.json"
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

# Batch-2 NEW entries (all URLs verified via gh api / curl 2026-09-14)
NEW_ENTRIES = [
    {
        "name": "cssrlib",
        "url": "https://github.com/hirokawa/cssrlib",
        "one_liner_zh": "Python 开源 PPP/PPP-RTK 工具包（CLAS/HAS/BDS PPP/IGS SSR）",
        "analysis_zh": "基于 RTKLIB 思路的 Python 工具包，解码 Compact SSR、RTCM/IGS SSR 等，对接 QZSS CLAS、Galileo HAS、北斗 PPP 与 IGS 服务做 PPP/PPP-RTK/RTK 教学与试验。附 Colab 教程，适合快速理解开放增强服务。实时生产与完好性需自测；与 MADOCALIB/CLASLIB/MRTKLIB 的 C 实现对照选型。",
        "language": "Jupyter Notebook",
        "license": "MIT",
        "category": "gnss-positioning",
        "subcategory": "PPP/PPP-RTK",
        "stars": 211,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["core", "similar-2026-09-14"],
    },
    {
        "name": "cssrlib-data",
        "url": "https://github.com/hirokawa/cssrlib-data",
        "one_liner_zh": "CSSRlib 配套样例脚本与数据集",
        "analysis_zh": "为 CSSRlib 提供样例脚本与试验数据，便于复现 CLAS/HAS 等开放 PPP/PPP-RTK 流程。适合跟着教程跑通改正接入与定位。不是改正产品中心；长期业务数据请接 IGS/各服务官方归档。",
        "language": "Python",
        "license": "NOASSERTION",
        "category": "gnss-datasets",
        "subcategory": "PPP/PPP-RTK样例",
        "stars": 44,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "PocketSDR",
        "url": "https://github.com/tomojitakasu/PocketSDR",
        "one_liner_zh": "Tomoji Takasu 开源 GNSS 软件接收机（多星座多频 SDR）",
        "analysis_zh": "RTKLIB 作者推出的开源 GNSS SDR：配套 Pocket SDR FE 前端与 Python/C/C++ 应用，覆盖 GPS/GLONASS/Galileo/QZSS/BDS/NavIC/SBAS 多频信号，可做捕获、跟踪、导航电文与 PVT。适合信号层教学与前端联调。精密 PPP/RTK 解算仍常外接 RTKLIB 系；硬件前端需另行采购或自备。",
        "language": "C",
        "license": "NOASSERTION",
        "category": "gnss-sdr",
        "subcategory": "软件接收机",
        "stars": 515,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["core", "similar-2026-09-14"],
    },
    {
        "name": "uNavTools",
        "url": "https://github.com/IvAn190/uNavTools",
        "one_liner_zh": "u-blox→RINEX 工具集，内置基于 CSSRlib 的 RTK/PPP",
        "analysis_zh": "命令行工具把 u-blox 原始数据转到 RINEX，并借助 CSSRlib 提供 RTK/PPP 模块，适合低成本板卡到开放增强服务的试验链。工程联调与教学友好。完好性、多频模糊度固定与测地级产品化仍弱于 PRIDE/Ginan/MRTKLIB。",
        "language": "Python",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RINEX工具",
        "stars": 10,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "PPP-RTK-Beechan",
        "url": "https://github.com/MichaelBeechan/PPP-RTK",
        "one_liner_zh": "C 实现的 SPP/RTD/PPP/RTK/PPP-RTK 与 RAIM 试验库",
        "analysis_zh": "汇总 SPP、RTD、PPP、RTK、PPP-RTK 及 RAIM/ARAIM 等模块的 C 试验工程，便于对照课本读导航完好性与差分流程。适合算法学习。文档与维护节奏需自查；生产部署请优先成熟套件并做回归。",
        "language": "C",
        "license": "",
        "category": "gnss-positioning",
        "subcategory": "PPP/PPP-RTK",
        "stars": 26,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "Easy4PTK",
        "url": "https://github.com/alxanderjiang/Easy4PTK",
        "one_liner_zh": "易移植的多星座 PPP-RTK Python 工具箱",
        "analysis_zh": "Python/Jupyter 实现的多星座 PPP-RTK 试验箱，强调可读与易移植，便于改状态估计与改正接入。适合教学与方法原型。性能与电文覆盖通常弱于 cssrlib/MRTKLIB；产线应用需交叉验证。",
        "language": "Jupyter Notebook",
        "license": "",
        "category": "gnss-positioning",
        "subcategory": "PPP/PPP-RTK",
        "stars": 5,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "AETHER",
        "url": "https://github.com/LiZhengXiao99/AETHER",
        "one_liner_zh": "PPP-RTK 用区域 STEC/VTEC/ZWD/ZTD 大气建模",
        "analysis_zh": "从 GNSS 观测抽取大气延迟，构建区域 STEC/VTEC 与 ZWD/ZTD 模型以增强 PPP-RTK。适合研究大气约束对收敛与精度的影响。依赖测站网密度与初始解质量；不是通用全球 GIM 服务。",
        "language": "C++",
        "license": "GPL-3.0",
        "category": "ionosphere",
        "subcategory": "电离层与PPP",
        "stars": 6,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "DeepPredTEC",
        "url": "https://github.com/vtsuperdarn/DeepPredTEC",
        "one_liner_zh": "深度学习预报 GPS TEC 图（SuperDARN 相关）",
        "analysis_zh": "用深度学习对 GPS TEC 图做时空预报的开源实现，面向空间天气与电离层研究。适合复现论文结构与对比基线。工程同化与多源融合需自建；输入网格、缺失填充与评估指标要与业务 GIM 对齐。",
        "language": "Python",
        "license": "MIT",
        "category": "ionosphere",
        "subcategory": "TEC预报",
        "stars": 13,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "gnss-scintillation-simulator_2-param",
        "url": "https://github.com/cu-sense-lab/gnss-scintillation-simulator_2-param",
        "one_liner_zh": "CU Sense Lab 两参数 GNSS 闪烁仿真器",
        "analysis_zh": "科罗拉多大学 Sense Lab 发布的两参数版 GNSS 闪烁仿真，相对原版简化相位/幅度扰动建模，便于接收机与信号处理试验。适合教学与算法压力测试。真实赤道/极区场景请结合实测 ISMR 与原版多参数模型对照。",
        "language": "MATLAB",
        "license": "",
        "category": "ionosphere",
        "subcategory": "闪烁",
        "stars": 6,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "PPP-RTK-Ionosphere",
        "url": "https://github.com/nickdaychen/PPP-RTK-Ionosphere",
        "one_liner_zh": "MATLAB 侧 PPP-RTK 与电离层相关试验代码",
        "analysis_zh": "围绕 PPP-RTK 与电离层约束/改正的 MATLAB 试验代码，便于改映射与随机模型做对比实验。适合课堂与方法验证。仓库说明偏少，输入产品与参考真值需自行准备；实时流处理不是主场。",
        "language": "MATLAB",
        "license": "",
        "category": "ionosphere",
        "subcategory": "电离层与PPP",
        "stars": 7,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "pwv_kpno",
        "url": "https://github.com/mwvgroup/pwv_kpno",
        "one_liner_zh": "基于 SuomiNet GPS 的可定制站点 PWV 大气透过率模型",
        "analysis_zh": "用 SuomiNet 等 GPS 反演的 PWV 驱动 MODTRAN 类大气透过率，默认服务 Kitt Peak，也可扩展到其它站点。面向天文测光改正与 GNSS 气象交叉验证。不是从 RINEX 估 ZWD 的 PPP 引擎；站点扩展需配置与文献引用。",
        "language": "Python",
        "license": "GPL-3.0",
        "category": "troposphere",
        "subcategory": "GNSS气象/PWV",
        "stars": 11,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "geodezyx",
        "url": "https://github.com/IPGP/geodezyx",
        "one_liner_zh": "IPGP 大地测量/地球物理 Python 工具箱（含对流层/PWV）",
        "analysis_zh": "巴黎地球物理研究所维护的 Python 工具箱，覆盖时间序列、坐标与大气模块（如 ZWD→PWV、GPT/VMF 相关接口）。适合把 GNSS 气象量快速接到地球物理脚本。完整精密定位请另接专用引擎；依赖与网格文件需按文档准备。",
        "language": "Python",
        "license": "LGPL-3.0",
        "category": "troposphere",
        "subcategory": "GNSS气象/PWV",
        "stars": 33,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "gnssr-raspberry",
        "url": "https://github.com/ITC-Water-Resources/gnssr-raspberry",
        "one_liner_zh": "树莓派上的 GNSS 反射测量（ITC 水资源）",
        "analysis_zh": "ITC Water Resources 在树莓派上跑 GNSS-R/反射测量的实验工程，面向低成本水文站。适合野外原型与教学演示。星标较少、文档因版本而异；水位产品建议对照 gnssrefl 与大地型天线结果。",
        "language": "Python",
        "license": "",
        "category": "troposphere",
        "subcategory": "GNSS-IR",
        "stars": 3,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "PyRINEX",
        "url": "https://github.com/geumjin99/PyRINEX",
        "one_liner_zh": "多用途 Python RINEX 读写与质量分析包",
        "analysis_zh": "面向 RINEX 2/3 的 Python 包，支持批处理、多路径与周跳等质量相关分析，可作为 TEQC/Anubis 之外的脚本化 QC 选项。适合自动化质控流水线。指标定义与报告格式因版本而异，正式归档前请与 Anubis/GFZRNX 交叉核对。",
        "language": "Python",
        "license": "",
        "category": "gnss-data",
        "subcategory": "多路径/QC",
        "stars": 16,
        "provenance": "academic_lab",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "AgOpenNtripCaster",
        "url": "https://github.com/AgOpenGPS-Official/AgOpenNtripCaster",
        "one_liner_zh": "AgOpenGPS 生态的开源 NTRIP Caster（C#）",
        "analysis_zh": "面向农业自动驾驶/AgOpenGPS 社区的 NTRIP 播发端，便于自建差分播发。适合农场站与 DIY CORS。运维与安全加固弱于 BKG 商用级 caster；公网部署需自行处理认证与带宽。",
        "language": "C#",
        "license": "",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "stars": 10,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "ntripcaster-docker-bkg",
        "url": "https://github.com/goblimey/ntripcaster",
        "one_liner_zh": "容器化构建与运行 BKG NTRIP Caster 的 Docker 方案",
        "analysis_zh": "提供 Dockerfile 与说明，方便构建运行经典 BKG NTRIP Caster，降低在自有服务器上部署播发端的门槛。适合运维试验。上游 BKG 许可与版本需单独遵守；生产环境还要做监控、TLS 与用户管理。",
        "language": "C",
        "license": "GPL-3.0",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "stars": 139,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "ntripcaster-libev",
        "url": "https://github.com/tisyang/ntripcaster",
        "one_liner_zh": "基于 libev 的高性能 NTRIP Broadcaster（C）",
        "analysis_zh": "用 C + libev 实现的 NTRIP 播发端，强调事件驱动与吞吐，适合自建 CORS 中继试验。与同作者 cors-relay 可搭配。协议兼容与管理界面因版本而异，公网服务请自行加固。",
        "language": "C",
        "license": "BSD-3-Clause",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "stars": 68,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "baidu-ntripcaster",
        "url": "https://github.com/baidu/ntripcaster",
        "one_liner_zh": "百度开源的 NTRIP Caster 实现",
        "analysis_zh": "百度公开的 NTRIP Caster 相关实现，可作自建播发与协议学习参考。适合对照 BKG/社区实现看消息路由。文档与许可声明以仓库为准；生产选用前做压力与安全测试。",
        "language": "C",
        "license": "NOASSERTION",
        "category": "gnss-data",
        "subcategory": "RTCM/NTRIP",
        "stars": 46,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "ublox_dgnss",
        "url": "https://github.com/aussierobots/ublox_dgnss",
        "one_liner_zh": "ROS2 u-blox UBX 驱动（F9P/F9R/X20P 差分与移动基站）",
        "analysis_zh": "面向 ROS2 的 u-blox UBX USB 驱动，支持 ZED-F9P/F9R/X20P 等高精度模块，含差分与 moving-base 配置。适合机器人/车载室外定位联调。不是测地级 PPP 引擎；精密解算请外接 RTKLIB 或科研软件。",
        "language": "C++",
        "license": "Apache-2.0",
        "category": "navigation-ins",
        "subcategory": "GNSS/INS",
        "stars": 86,
        "provenance": "personal_community",
        "host": "github",
        "markers": ["similar-2026-09-14"],
    },
    {
        "name": "PPP-Wizard",
        "url": "http://www.ppp-wizard.net/",
        "one_liner_zh": "CNES PPP-WIZARD：整数模糊度 PPP-AR 演示与产品门户",
        "analysis_zh": "法国空间研究中心（CNES）PPP-WIZARD 项目门户，介绍零差整数模糊度 PPP-AR 演示软件、SSR 计算与日产品/监测入口。适合了解 CNES 实时 PPP-AR 路线并申请软件包。源码不在本页直接 git 克隆；获取方式与许可以官网说明为准，并与 IGS 实时流配合使用。",
        "language": "C++",
        "license": "see upstream",
        "category": "gnss-positioning",
        "subcategory": "PPP/PPP-AR",
        "stars": None,
        "provenance": "official",
        "host": "official_site",
        "markers": ["core", "similar-2026-09-14"],
    },
]


def norm_url(u: str) -> str:
    return (u or "").rstrip("/").lower()


def one_liner(p: dict) -> str:
    return p.get("one_liner_zh") or p.get("desc_zh") or p.get("name")


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


def finalize_new(f: dict) -> dict:
    ol = f["one_liner_zh"]
    return {
        "name": f["name"],
        "url": f["url"],
        "desc_zh": ol,
        "analysis_zh": f["analysis_zh"],
        "language": f.get("language") or "",
        "license": f.get("license") or "",
        "category": f["category"],
        "subcategory": f.get("subcategory") or "",
        "markers": f.get("markers") or [],
        "stars_approx": f.get("stars"),
        "source": "similar-finds-batch2-2026-09-14",
        "featured": "core" in (f.get("markers") or []),
        "user_relation": "none",
        "host": f["host"],
        "provenance": f["provenance"],
        "one_liner_zh": ol,
    }


def normalize_incomplete(p: dict) -> dict:
    """Ensure desc_zh / stars_approx / source / featured / user_relation exist."""
    if "one_liner_zh" not in p and p.get("desc_zh"):
        p["one_liner_zh"] = p["desc_zh"]
    if "desc_zh" not in p:
        p["desc_zh"] = p.get("one_liner_zh") or p["name"]
    if "stars_approx" not in p and "stars" in p:
        p["stars_approx"] = p.get("stars")
    if "source" not in p:
        p["source"] = "similar-finds-2026-09-14"
    if "featured" not in p:
        p["featured"] = "core" in (p.get("markers") or [])
    if "user_relation" not in p:
        p["user_relation"] = "none"
    return p


def regenerate_lists(projects):
    for cat, meta in CAT_META.items():
        items = [p for p in projects if p["category"] == cat]
        by_sub = defaultdict(list)
        for p in items:
            by_sub[p.get("subcategory") or "其他"].append(p)

        lines = [
            f"# {meta['title']}",
            f"> 共 **{len(items)}** 个已收录项目。本文件为链接索引，不含第三方源码。",
            "",
            f"**这类做什么？** {meta['blurb']}",
            "",
            "来源标记：🏷️ 官方 = 机构/国家实验室；🏷️ 高校实验室 = 大学课题组；🏷️ 个人社区 = 个人或小团队。",
            "",
        ]

        # keep first-seen subcategory order, but sort SH-GIM first in its subcat
        sub_order = []
        for p in items:
            sc = p.get("subcategory") or "其他"
            if sc not in by_sub:
                continue
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

        (LISTS / meta["file"]).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def regenerate_categories(counts):
    cat_doc = [
        "# 分类说明（写给初学者）",
        "",
        "本索引按「你要解决什么问题」划分，而不是按编程语言。下面用白话说明每一类在 GNSS 工作流里的位置。",
        "",
        "```",
        "数据下载/格式(RINEX,RTCM) ──► 质量检查",
        "         │",
        "         ├─► 电离层 TEC/GIM / 闪烁指标",
        "         ├─► 对流层 ZTD/PWV / VMF",
        "         └─► 精密定位 RTK/PPP ──► 轨道钟差产品",
        "                    │",
        "                    └─► GNSS/INS / 视觉组合导航",
        "",
        "另线：GNSS-SDR（从无线电采样到伪距/相位）；手机 App（原始测量采集）",
        "```",
        "",
        "## 来源 / 维护方标记（provenance）",
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
    (DOCS / "categories.md").write_text("\n".join(cat_doc), encoding="utf-8")


def regenerate_readme(projects, counts, prov_counts):
    total = len(projects)
    readme = [
        "# Ionosphere-GNSS-OpenSource",
        "",
        "**电离层 · 对流层 · GNSS · 导航（PNT）开源软件精选索引**  ",
        "Curated open-source catalog for Ionosphere / Troposphere / GNSS / Navigation",
        "",
        f"[![Projects](https://img.shields.io/badge/verified%20projects-{total}-blue.svg)](./PROJECTS.json)",
        "[![License: CC0](https://img.shields.io/badge/catalog%20license-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)",
        "",
        "> **这是链接索引（curated index），不是代码大合集。**  ",
        "> 所有条目均为已核对的公开 URL；需要时请前往**上游仓库**克隆并遵守其许可证。",
        "",
        "---",
        "",
        "## 如何使用",
        "",
        "1. 先读 [分类说明](./docs/categories.md)，弄清自己处在数据→改正→定位→组合导航的哪一段  ",
        "2. 打开下方对应的 `lists/*.md`，里面有**表格 + 每条项目的详细中文分析**  ",
        "3. 机器可读清单：[`PROJECTS.json`](./PROJECTS.json) · 相似项目检索：[`research/similar_finds.json`](./research/similar_finds.json)  ",
        "4. 克隆上游，不要把第三方源码拷进本仓库",
        "",
        "### 标记",
        "",
        "| 标记 | 含义 |",
        "|:---:|---|",
        "| 🏷️ 官方 | 政府/机构/联盟官方发行 |",
        "| 🏷️ 高校实验室 | 大学课题组维护 |",
        "| 🏷️ 个人社区 | 个人或小团队/社区 |",
        "| 🚩 | 维护者自有公开仓库（仅收录链接，不写详细介绍） |",
        "| 🔀 | 维护者已 fork（表中列上游；fork 地址见项目页） |",
        "| ★ | 维护者 GitHub 星标种子 |",
        "| 核心 | 建议优先阅读 |",
        "",
        f"来源统计：官方 **{prov_counts.get('official',0)}** · 高校实验室 **{prov_counts.get('academic_lab',0)}** · 个人社区 **{prov_counts.get('personal_community',0)}**",
        "",
        "---",
        "",
        "## 分类一览",
        "",
        "| 分类 | 适合谁 | 列表 | 数量 |",
        "|---|---|---|---:|",
    ]
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
            featured = sorted(items, key=lambda x: (-(x.get("stars_approx") or x.get("stars") or 0), x["name"]))[:6]
        else:
            # SH-GIM first for ionosphere
            if cat == "ionosphere":
                featured = sorted(
                    featured,
                    key=lambda p: (0 if p["name"] == "SH-GIM" else 1, 0 if "core" in (p.get("markers") or []) else 1),
                )
            featured = featured[:8]
        readme.append(f"## {meta['title']}")
        readme.append("")
        readme.append(meta["blurb"])
        readme.append("")
        readme.append(f"完整列表与逐项分析 → [{meta['file']}](./lists/{meta['file']})")
        readme.append("")
        readme.append("| 项目 | 简介 | 标记 |")
        readme.append("|---|---|---|")
        for p in featured:
            readme.append(f"| [{p['name']}]({p['url']}) | {one_liner(p)} | {marker_text(p)} |")
        readme.append("")

    readme += [
        "---",
        "",
        "## 许可",
        "",
        "本**目录**以 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 贡献；各上游软件许可证以其仓库为准。",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(readme), encoding="utf-8")


def main():
    catalog = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    projects = catalog["projects"]

    # normalize incomplete
    for p in projects:
        normalize_incomplete(p)

    existing_urls = {norm_url(p["url"]) for p in projects}
    existing_names = {p["name"] for p in projects}

    added = []
    for raw in NEW_ENTRIES:
        # forbid 旨在/赋能
        assert "旨在" not in raw["analysis_zh"] and "赋能" not in raw["analysis_zh"]
        assert "旨在" not in raw["one_liner_zh"] and "赋能" not in raw["one_liner_zh"]
        nu = norm_url(raw["url"])
        if nu in existing_urls:
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
        existing_urls.add(nu)
        existing_names.add(e["name"])
        added.append(e)

    counts = Counter(p["category"] for p in projects)
    prov_counts = Counter(p.get("provenance") for p in projects)
    catalog["projects"] = projects
    catalog["project_count"] = len(projects)
    catalog["counts_by_category"] = {k: counts.get(k, 0) for k in CAT_META}
    catalog["generated"] = date.today().isoformat()

    PROJECTS_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Merge into similar_finds.json: keep prior + append new batch as research record
    prior = []
    if SIMILAR_PATH.exists():
        prior = json.loads(SIMILAR_PATH.read_text(encoding="utf-8"))
    prior_urls = {norm_url(p["url"]) for p in prior}
    for e in added:
        if norm_url(e["url"]) not in prior_urls:
            prior.append(
                {
                    "name": e["name"],
                    "url": e["url"],
                    "category": e["category"],
                    "subcategory": e["subcategory"],
                    "language": e.get("language") or None,
                    "license": e.get("license") or None,
                    "stars": e.get("stars_approx"),
                    "provenance": e["provenance"],
                    "host": e["host"],
                    "one_liner_zh": e["one_liner_zh"],
                    "analysis_zh": e["analysis_zh"],
                    "markers": e.get("markers") or [],
                }
            )
    SIMILAR_PATH.write_text(json.dumps(prior, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    regenerate_lists(projects)
    regenerate_categories(counts)
    regenerate_readme(projects, counts, prov_counts)

    # NOTES append
    notes = ROOT / "NOTES.md"
    notes.write_text(
        notes.read_text(encoding="utf-8").rstrip()
        + f"\n\n## 相似项目补录 batch2（2026-09-14）\n\n"
        + f"- 新增 **{len(added)}** 条（cssrlib/PocketSDR/PPP-Wizard/NTRIP/TEC/PWV 等）\n"
        + f"- 当前条目：**{catalog['project_count']}**\n"
        + f"- 分类计数：{dict(catalog['counts_by_category'])}\n"
        + f"- 详见 `research/similar_finds.json`\n",
        encoding="utf-8",
    )

    print("ADDED", len(added))
    print("TOTAL", catalog["project_count"])
    print("COUNTS", dict(catalog["counts_by_category"]))
    for a in added:
        print(f"  + {a['name']:40s} {a['category']:18s} stars={a['stars_approx']}")


if __name__ == "__main__":
    main()
