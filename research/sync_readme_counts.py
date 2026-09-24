#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync live PROJECTS.json counts into README.md without rebuilding the old catalog wall.

Preserve path (README already has 「三条路」): update badges, classification table,
and provenance numbers only.

Restore path (legacy overwrite): rewrite the navigational README template with
live counts so accidental regenerations can recover.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT_DEFAULT = Path(__file__).resolve().parents[1]

# category key → (Chinese label as shown in compact table, list filename)
CATEGORY_META: list[tuple[str, str, str]] = [
    ("ionosphere", "电离层", "01-ionosphere.md"),
    ("troposphere", "对流层", "02-troposphere.md"),
    ("gnss-data", "GNSS 数据与格式", "03-gnss-data.md"),
    ("gnss-positioning", "精密定位", "04-gnss-positioning.md"),
    ("orbit-clock", "轨道与钟差", "05-orbit-clock.md"),
    ("navigation-ins", "导航", "06-navigation-ins.md"),
    ("gnss-sdr", "软件接收机", "07-gnss-sdr.md"),
    ("mobile-apps", "移动应用", "08-mobile-apps.md"),
    ("tools-learning", "学习工具", "09-tools-learning.md"),
    ("gnss-datasets", "数据源门户", "10-gnss-datasets.md"),
]

NAV_MARKER = "三条路"


def _load_counts(root: Path) -> tuple[int, dict[str, int], dict[str, int]]:
    catalog = json.loads((root / "PROJECTS.json").read_text(encoding="utf-8"))
    projects = catalog.get("projects") or []
    n = int(catalog.get("project_count") or len(projects))
    categories = catalog.get("counts_by_category")
    if not isinstance(categories, dict) or not categories:
        categories = dict(Counter(p.get("category") for p in projects if isinstance(p, dict)))
    else:
        categories = {k: int(v) for k, v in categories.items()}
    provenance = catalog.get("provenance_counts")
    if not isinstance(provenance, dict) or not provenance:
        provenance = dict(
            Counter(p.get("provenance") for p in projects if isinstance(p, dict) and p.get("provenance"))
        )
    else:
        provenance = {k: int(v) for k, v in provenance.items()}
    return n, categories, provenance


def _nav_template(n: int, categories: dict[str, int], provenance: dict[str, int]) -> str:
    """Navigational README matching main after ca3680a, filled with live counts."""
    off = provenance.get("official", 0)
    acad = provenance.get("academic_lab", 0)
    comm = provenance.get("personal_community", 0)
    portals = categories.get("gnss-datasets", 0)

    rows: list[str] = []
    for key, label, list_file in CATEGORY_META:
        num = list_file.split("-", 1)[0]
        count = categories.get(key, 0)
        if key == "gnss-datasets":
            rows.append(f"| **{label}** | [{num}](./lists/{list_file}) | {count} |")
        else:
            rows.append(f"| {label} | [{num}](./lists/{list_file}) | {count} |")
    rows.append(f"| **合计** | [PROJECTS.json](./PROJECTS.json) | **{n}** |")
    table = "\n".join(rows)

    return f"""# Ionosphere-GNSS-OpenSource

**电离层 · GNSS · 导航开源索引**（链接精选，不是代码大合集）

[![Projects](https://img.shields.io/badge/verified%20projects-{n}-blue.svg)](./PROJECTS.json)
[![CC0](https://img.shields.io/badge/catalog-CC0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Datasets](https://img.shields.io/badge/data%20portals-{portals}-teal.svg)](./lists/10-gnss-datasets.md)

<p align="center">
  <img src="./docs/tutorials/images/fig-phenomena-gallery.png" alt="Ionosphere phenomena gallery" width="920"/>
</p>

<p align="center"><sub>自绘示意（日夜 TEC · 气泡闪烁 · TID · Ne 剖面）· CC0 · 非实测产品图</sub></p>

---

## 三条路（先选路）

| | 目标 | 入口 |
|:---:|---|---|
| **A** | 弄懂 TEC / 闪烁 / 磁暴长什么样 | [教程](./docs/tutorials/README.md) · [现象课 19–23](./docs/tutorials/19-phenomena-overview.md) |
| **B** | 下载 RINEX / IONEX / CORS / 实时流 | [数据怎么下](./docs/data-access.md) · [数据源列表](./lists/10-gnss-datasets.md) |
| **C** | 选开源软件动手算 | [软件怎么用](./docs/software/README.md) · 下方分类表 · [`PROJECTS.json`](./PROJECTS.json) |

---

## 现象一眼看懂

| 现象 | 图 | 课文 |
|---|---|---|
| 日夜 TEC + EIA | ![](./docs/tutorials/images/fig-tec-day-night.png) | [21 赤道异常](./docs/tutorials/21-equatorial-anomaly-bubbles.md) |
| 等离子体气泡 / 闪烁 | ![](./docs/tutorials/images/fig-scintillation-bubbles.png) | [05 闪烁](./docs/tutorials/05-scintillation-roti.md) |
| TID 行波 | ![](./docs/tutorials/images/fig-tid-wavefront.png) | [22 TID](./docs/tutorials/22-tid-traveling-disturbances.md) |
| 磁暴残差 | ![](./docs/tutorials/images/fig-storm-quiet-residual.png) | [20 磁暴](./docs/tutorials/20-storm-tec-analysis.md) |
| 耀斑突增 | ![](./docs/tutorials/images/fig-flare-sudden-ionize.png) | [23 耀斑日食](./docs/tutorials/23-flare-eclipse-special.md) |
| Ne 高度剖面 | ![](./docs/tutorials/images/fig-ne-profile-layers.png) | [01 基础](./docs/tutorials/01-ionosphere-tec-basics.md) |
| 双频 → TEC | ![](./docs/tutorials/images/fig-dualfreq-tec.png) | [02 双频](./docs/tutorials/02-gnss-dualfreq-tec.md) |
| ROTI 示意 | ![](./docs/tutorials/images/fig-roti-map-schematic.png) | [05 闪烁](./docs/tutorials/05-scintillation-roti.md) |

---

## 软件 / 数据分类

| 分类 | 列表 | 数 |
|---|---|---:|
{table}

标记：🏷️ 官方 / 高校实验室 / 个人社区 · 官方 {off} · 高校 {acad} · 社区 {comm} · 细则 [categories.md](./docs/categories.md)

---

## 许可

目录文本与元数据 [CC0](https://creativecommons.org/publicdomain/zero/1.0/)。上游软件与数据仍按各自条款。
"""


def _update_nav_counts(text: str, n: int, categories: dict[str, int], provenance: dict[str, int]) -> str:
    """In-place count updates for the navigational README."""
    portals = categories.get("gnss-datasets", 0)
    off = provenance.get("official", 0)
    acad = provenance.get("academic_lab", 0)
    comm = provenance.get("personal_community", 0)

    out = text
    out = re.sub(
        r"verified%20projects-\d+",
        f"verified%20projects-{n}",
        out,
        count=1,
    )
    out = re.sub(
        r"data%20portals-\d+",
        f"data%20portals-{portals}",
        out,
        count=1,
    )

    for key, label, list_file in CATEGORY_META:
        count = categories.get(key, 0)
        num = list_file.split("-", 1)[0]
        # Match bold or plain label; keep link cell; replace trailing count.
        pattern = (
            rf"(\| (?:\*\*)?{re.escape(label)}(?:\*\*)? \| "
            rf"\[{re.escape(num)}\]\(\./lists/{re.escape(list_file)}\) \| )\d+( \|)"
        )
        out, nsub = re.subn(pattern, rf"\g<1>{count}\2", out, count=1)
        if nsub == 0:
            # Fallback: label + list path anywhere on the row
            pattern2 = (
                rf"(\| (?:\*\*)?{re.escape(label)}(?:\*\*)? \| "
                rf"\[[^\]]*\]\(\./lists/{re.escape(list_file)}\) \| )\d+( \|)"
            )
            out = re.sub(pattern2, rf"\g<1>{count}\2", out, count=1)

    out = re.sub(
        r"(\| \*\*合计\*\* \| \[PROJECTS\.json\]\(\./PROJECTS\.json\) \| )\*\*\d+\*\*( \|)",
        rf"\g<1>**{n}**\2",
        out,
        count=1,
    )
    out = re.sub(
        r"官方 \d+ · 高校 \d+ · 社区 \d+",
        f"官方 {off} · 高校 {acad} · 社区 {comm}",
        out,
        count=1,
    )
    return out


def sync_readme_counts(root: Path | None = None) -> dict[str, Any]:
    """Sync PROJECTS.json counts into README.md. Preserve nav; restore if legacy.

    Returns dict with keys: n, categories, provenance, mode ('preserve'|'restore'), changed.
    """
    root = Path(root) if root is not None else ROOT_DEFAULT
    n, categories, provenance = _load_counts(root)
    readme_path = root / "README.md"
    previous = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    if NAV_MARKER in previous:
        mode = "preserve"
        updated = _update_nav_counts(previous, n, categories, provenance)
    else:
        mode = "restore"
        updated = _nav_template(n, categories, provenance)
        if not updated.endswith("\n"):
            updated += "\n"

    if not updated.endswith("\n"):
        updated += "\n"

    changed = updated != previous
    if changed:
        readme_path.write_text(updated, encoding="utf-8")

    return {
        "n": n,
        "categories": dict(categories),
        "provenance": dict(provenance),
        "mode": mode,
        "changed": changed,
    }


if __name__ == "__main__":
    stats = sync_readme_counts()
    print(
        f"mode={stats['mode']} changed={stats['changed']} n={stats['n']} "
        f"portals={stats['categories'].get('gnss-datasets')} "
        f"prov={stats['provenance']}"
    )
