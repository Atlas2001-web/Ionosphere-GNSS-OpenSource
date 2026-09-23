#!/usr/bin/env python3
"""Gap-fill teaching schematics (CC0, matplotlib; one cartopy coast map).

Outputs under docs/tutorials/images/:
  fig-catalog-nav.png
  fig-gim-grid-ipps-coast.png
  fig-pseudorange-to-stec.png
  fig-iri-vs-ionosonde.png
  fig-ionogram-trace.png
  fig-gnss-ro-geometry.png
  fig-dcb-sat-rx-split.png
  fig-singlefreq-vs-dualfreq.png

Usage (repo root):
  .venv/bin/python scripts/make_gap_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials" / "images"

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.unicode_minus": False,
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
)

FOOT = "schematic · CC0"
BLUE = "#2874a6"
GREEN = "#2ca25f"
RED = "#b22222"
ORANGE = "#e67e22"
PURPLE = "#8e44ad"
GREY = "#7f8c8d"
TEAL = "#148f77"
LIGHT_BLUE = "#5dade2"
LIGHT_RED = "#e74c3c"
GOLD = "#f1c40f"


def _save(fig: plt.Figure, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
    return path


def _footer(fig: plt.Figure, y: float = 0.01) -> None:
    fig.text(0.5, y, FOOT, ha="center", va="bottom", fontsize=8, color="#666666")


# ---------------------------------------------------------------------------
# 1. Catalog navigation — CARD tiles (not a flowchart)
# ---------------------------------------------------------------------------
def fig_catalog_nav() -> None:
    fig, ax = plt.subplots(figsize=(10.2, 6.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title(
        "PROJECTS.json / lists — catalog as cards (find by question)",
        fontsize=13, pad=8, fontweight="bold",
    )

    cards = [
        # (x, y, w, h, title, subtitle, color)
        (0.3, 4.6, 3.0, 1.5, "lists/01-ionosphere", "TEC · GIM · scint · IRI", BLUE),
        (3.5, 4.6, 3.0, 1.5, "lists/04-positioning", "RTKLIB · PPP · IF/GF", TEAL),
        (6.7, 4.6, 3.0, 1.5, "lists/10-datasets", "RINEX · IONEX · portals", ORANGE),
        (0.3, 2.7, 3.0, 1.5, "docs/categories.md", "category boundaries", PURPLE),
        (3.5, 2.7, 3.0, 1.5, "PROJECTS.json", "~611 machine entries", RED),
        (6.7, 2.7, 3.0, 1.5, "docs/software/", "install · minimal run", GREEN),
        (0.3, 0.8, 4.6, 1.5, "docs/tutorials/ 01–23", "classroom: mechanism → formula → signature", LIGHT_BLUE),
        (5.2, 0.8, 4.5, 1.5, "CONTRIBUTING.md", "add a link entry — do not vendor code", GREY),
    ]

    for x, y, w, h, title, sub, color in cards:
        box = FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.15",
            facecolor="white", edgecolor=color, linewidth=2.2, zorder=2,
        )
        ax.add_patch(box)
        # colored header strip
        strip = FancyBboxPatch(
            (x, y + h - 0.45), w, 0.45, boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=color, edgecolor=color, linewidth=0, zorder=3, alpha=0.92,
        )
        ax.add_patch(strip)
        ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="center",
                color="white", fontsize=10, fontweight="bold", zorder=4)
        ax.text(x + w / 2, y + 0.55, sub, ha="center", va="center",
                color="#333333", fontsize=9, zorder=4)

    ax.text(
        5.0, 0.25,
        "Pick a card by research question → open list → clone upstream. Index ≠ package mirror.",
        ha="center", va="center", fontsize=9, color="#444444", style="italic",
    )
    _footer(fig, y=0.005)
    fig.subplots_adjust(bottom=0.05, top=0.92)
    _save(fig, "fig-catalog-nav.png")


# ---------------------------------------------------------------------------
# 2. GIM grid + multi-station IPPs with coastlines
# ---------------------------------------------------------------------------
def fig_gim_grid_ipps_coast() -> None:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(10.0, 5.8))
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    # East Asia / West Pacific regional teaching window
    extent = [95, 145, 5, 45]
    ax.set_extent(extent, crs=proj)
    ax.add_feature(cfeature.OCEAN, facecolor="#e8f4fc", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="#f5f0e6", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.7, edgecolor="#333333", zorder=3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor="#888888", linestyle=":", zorder=3)
    gl = ax.gridlines(draw_labels=True, linewidth=0.35, color="gray", alpha=0.4, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    # GIM-like 2.5°×5° style grid (schematic spacing)
    for lon in np.arange(95, 146, 5):
        ax.plot([lon, lon], [5, 45], transform=proj, color="#aab7b8",
                lw=0.55, alpha=0.7, zorder=2)
    for lat in np.arange(5, 46, 2.5):
        ax.plot([95, 145], [lat, lat], transform=proj, color="#aab7b8",
                lw=0.55, alpha=0.7, zorder=2)

    # Synthetic stations denser on land
    rng = np.random.default_rng(7)
    stations = [
        (116.4, 39.9), (121.5, 31.2), (113.3, 23.1), (104.1, 30.7),
        (108.9, 34.3), (126.6, 45.7), (118.1, 24.5), (120.3, 22.6),
        (139.7, 35.7), (135.5, 34.7), (129.0, 35.2), (100.5, 13.8),
        (106.8, 10.8), (103.8, 1.3), (101.7, 3.1), (114.2, 22.3),
    ]
    # Extra synthetic land dots
    extra = []
    for _ in range(18):
        lon = float(rng.uniform(100, 140))
        lat = float(rng.uniform(10, 42))
        extra.append((lon, lat))
    stations = stations + extra

    # IPP arcs: each station fans out to several pierce points
    colors_st = plt.cm.tab10(np.linspace(0, 1, 10))
    for i, (slon, slat) in enumerate(stations[:16]):
        ax.plot(slon, slat, marker="^", ms=7, color="#1e8449",
                markeredgecolor="white", markeredgewidth=0.4, transform=proj, zorder=6)
        n_ipp = 5
        for k in range(n_ipp):
            az = rng.uniform(0, 2 * np.pi)
            dist = rng.uniform(2.5, 8.0)  # degrees-ish
            ilon = slon + dist * np.cos(az)
            ilat = slat + dist * np.sin(az) * 0.7
            if not (96 < ilon < 144 and 6 < ilat < 44):
                continue
            ax.plot([slon, ilon], [slat, ilat], transform=proj,
                    color=colors_st[i % 10], lw=0.7, alpha=0.45, zorder=4)
            ax.plot(ilon, ilat, "o", ms=3.2, color=colors_st[i % 10],
                    alpha=0.85, transform=proj, zorder=5)

    # Legend proxies
    ax.plot([], [], "^", color="#1e8449", ms=7, label="GNSS stations")
    ax.plot([], [], "o", color=BLUE, ms=4, label="IPPs (pierce points)")
    ax.plot([], [], color="#aab7b8", lw=1.2, label="GIM grid (schematic)")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.92)

    ax.set_title("Multi-station IPPs + GIM grid over coastlines (schematic)", fontsize=12)
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-gim-grid-ipps-coast.png")


# ---------------------------------------------------------------------------
# 3. Pseudorange → STEC (equations as annotated time series; no flowchart)
# ---------------------------------------------------------------------------
def fig_pseudorange_to_stec() -> None:
    rng = np.random.default_rng(21)
    t = np.linspace(0, 4.0, 400)  # hours
    # Smooth STEC arc (TECU)
    stec_true = 18 + 12 * np.sin(np.pi * t / 4) ** 1.2 + 3 * np.sin(2 * np.pi * t / 3)
    # Dual-freq delays (m): I ∝ STEC/f²
    # α ≈ 9.52 TECU/m for P1−P2 → STEC on GPS L1/L2
    alpha = 9.52
    # I1 ≈ 40.3*STEC_e16 / f1² → use engineering: GF_m = STEC/α
    gf_m = stec_true / alpha
    noise = 0.08 * rng.standard_normal(t.size)
    p1_minus_p2 = gf_m + noise  # meters, noisy code GF
    stec_est = alpha * p1_minus_p2

    fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.2), sharex=True,
                             gridspec_kw={"height_ratios": [1.0, 1.15], "hspace": 0.12})

    ax0, ax1 = axes
    ax0.plot(t, p1_minus_p2, color=ORANGE, lw=1.1, label=r"$P_1-P_2$ (m, code GF)")
    ax0.axhline(0, color=GREY, lw=0.6)
    ax0.set_ylabel(r"$P_1-P_2$  [m]")
    ax0.set_title(r"Dual-frequency pseudorange $\rightarrow$ STEC  (schematic)", fontsize=12)
    ax0.legend(loc="upper left", fontsize=9)
    ax0.grid(True, alpha=0.3)
    ax0.text(
        0.98, 0.08,
        r"$P_1-P_2 \approx 40.3\,\mathrm{STEC}\!\left(\frac{1}{f_1^2}-\frac{1}{f_2^2}\right)$",
        transform=ax0.transAxes, ha="right", va="bottom", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff8e7", edgecolor=ORANGE, alpha=0.95),
    )

    ax1.plot(t, stec_true, color=BLUE, lw=2.0, label="true STEC (schematic)")
    ax1.plot(t, stec_est, color=LIGHT_RED, lw=0.9, alpha=0.85, label=r"$\alpha\,(P_1-P_2)$ estimate")
    ax1.set_xlabel("time [h]")
    ax1.set_ylabel("STEC [TECU]")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.text(
        0.98, 0.08,
        r"$\mathrm{STEC}\approx\alpha\,(P_1-P_2),\quad \alpha\sim9.52\,\mathrm{TECU/m}$",
        transform=ax1.transAxes, ha="right", va="bottom", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#eaf2f8", edgecolor=BLUE, alpha=0.95),
    )

    _footer(fig)
    fig.subplots_adjust(bottom=0.08, top=0.93)
    _save(fig, "fig-pseudorange-to-stec.png")


# ---------------------------------------------------------------------------
# 4. IRI climate Ne(h) vs ionosonde profile
# ---------------------------------------------------------------------------
def fig_iri_vs_ionosonde() -> None:
    h = np.linspace(90, 600, 400)

    def chapman(hm, Nm, H, h):
        z = (h - hm) / H
        return Nm * np.exp(0.5 * (1 - z - np.exp(-z)))

    # IRI-like smooth climate (F2 + F1 + E bumps)
    iri = (
        chapman(300, 1.05e12, 55, h)
        + chapman(180, 2.2e11, 28, h)
        + chapman(110, 1.4e11, 12, h)
    )
    # Ionosonde: similar but peak shifted + bottomside structure + noise above hm
    iono = (
        chapman(285, 1.25e12, 48, h)
        + chapman(175, 2.8e11, 24, h)
        + chapman(108, 1.6e11, 10, h)
    )
    # topside: ionosonde usually stops near peak / incomplete
    mask_top = h > 320
    iono = iono.copy()
    iono[mask_top] = np.nan
    # add small ripple on bottomside
    iono = iono * (1 + 0.04 * np.sin(h / 9))

    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    ax.plot(iri / 1e11, h, color=BLUE, lw=2.4, label="IRI climate $N_e(h)$")
    ax.plot(iono / 1e11, h, color=ORANGE, lw=2.0, label="ionosonde inverted $N_e(h)$")
    ax.fill_betweenx(h, iri / 1e11, where=~np.isnan(iono), color=BLUE, alpha=0.06)

    # mark peaks
    i_iri = int(np.argmax(iri))
    i_io = int(np.nanargmax(iono))
    ax.plot(iri[i_iri] / 1e11, h[i_iri], "o", color=BLUE, ms=7)
    ax.plot(iono[i_io] / 1e11, h[i_io], "s", color=ORANGE, ms=7)
    ax.annotate(
        r"IRI $h_mF2$",
        xy=(iri[i_iri] / 1e11, h[i_iri]), xytext=(iri[i_iri] / 1e11 + 2.5, h[i_iri] + 40),
        fontsize=9, color=BLUE,
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0),
    )
    ax.annotate(
        r"iono $h_mF2$",
        xy=(iono[i_io] / 1e11, h[i_io]), xytext=(iono[i_io] / 1e11 + 2.0, h[i_io] - 55),
        fontsize=9, color=ORANGE,
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0),
    )

    ax.axhline(320, color=GREY, ls=":", lw=1.0)
    ax.text(0.3, 330, "ionosonde often ends near / below peak",
            fontsize=8, color=GREY, va="bottom")

    ax.set_xlabel(r"$N_e$  [$10^{11}$ m$^{-3}$]")
    ax.set_ylabel("height [km]")
    ax.set_ylim(90, 600)
    ax.set_xlim(0, 16)
    ax.set_title("Climate model vs ionosonde profile (schematic)", fontsize=12)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.text(
        0.02, 0.02,
        "Same local time/lat class ≠ identical peak — climate mean vs one sounding.",
        transform=ax.transAxes, fontsize=8, color="#444444",
    )
    _footer(fig)
    fig.subplots_adjust(bottom=0.08)
    _save(fig, "fig-iri-vs-ionosonde.png")


# ---------------------------------------------------------------------------
# 5a. Ionogram O/X traces
# ---------------------------------------------------------------------------
def fig_ionogram_trace() -> None:
    # Virtual height vs frequency for O and X modes
    f_o = np.linspace(1.5, 8.8, 300)
    # Echo virtual height rises toward critical frequency
    h_o = 95 + 40 * (f_o / 3) + 180 / np.maximum(8.9 - f_o, 0.15) ** 0.55
    # cusp near foF2
    h_o = np.clip(h_o, 90, 520)

    f_x = f_o + 0.55  # X roughly shifted
    h_x = 100 + 38 * (f_x / 3.2) + 200 / np.maximum(9.5 - f_x, 0.18) ** 0.55
    h_x = np.clip(h_x, 95, 540)

    # E-layer ledge
    f_e = np.linspace(1.5, 3.4, 80)
    h_e = 105 + 8 * (f_e - 1.5) + 25 / np.maximum(3.5 - f_e, 0.2)

    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.plot(f_o, h_o, color=BLUE, lw=2.2, label="O-mode trace")
    ax.plot(f_x, h_x, color=RED, lw=2.0, ls="--", label="X-mode trace")
    ax.plot(f_e, h_e, color=GREEN, lw=1.8, label="E-region ledge")

    # Critical frequency marks
    foF2, fxF2 = 8.8, 9.4
    ax.axvline(foF2, color=BLUE, ls=":", lw=1.2, alpha=0.8)
    ax.axvline(fxF2, color=RED, ls=":", lw=1.2, alpha=0.8)
    ax.text(foF2 - 0.15, 480, r"$f_oF2$", color=BLUE, ha="right", fontsize=10, fontweight="bold")
    ax.text(fxF2 + 0.15, 500, r"$f_xF2$", color=RED, ha="left", fontsize=10, fontweight="bold")

    ax.set_xlabel("frequency [MHz]")
    ax.set_ylabel("virtual height $h'$ [km]")
    ax.set_xlim(1.2, 11)
    ax.set_ylim(80, 560)
    ax.set_title("Ionogram traces (O / X) — schematic", fontsize=12)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.text(
        0.98, 0.05,
        r"$h'$ from round-trip delay — not geometric altitude",
        transform=ax.transAxes, ha="right", fontsize=8, color="#444444",
        style="italic",
    )
    _footer(fig)
    fig.subplots_adjust(bottom=0.08)
    _save(fig, "fig-ionogram-trace.png")


# ---------------------------------------------------------------------------
# 5b. GNSS radio occultation geometry
# ---------------------------------------------------------------------------
def fig_gnss_ro_geometry() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 6.0))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.35, 1.55)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("GNSS radio occultation geometry (schematic)", fontsize=12, pad=6)

    earth = Circle((0, 0), 1.0, facecolor="#d5f5e3", edgecolor=GREEN, lw=2.0, zorder=1)
    ax.add_patch(earth)
    # atmosphere shell
    atm = Circle((0, 0), 1.12, facecolor="none", edgecolor=LIGHT_BLUE, lw=1.5,
                 ls="--", zorder=1)
    ax.add_patch(atm)
    ax.text(0, -0.15, "Earth", ha="center", color="#1e8449", fontsize=11, fontweight="bold")

    # LEO on left, GNSS on right-high
    leo = np.array([-1.35, 0.55])
    gnss = np.array([1.45, 1.15])
    ax.plot(*leo, "o", color=ORANGE, ms=11, zorder=5)
    ax.plot(*gnss, "^", color=PURPLE, ms=14, zorder=5)
    ax.text(leo[0] - 0.05, leo[1] + 0.12, "LEO Rx", color=ORANGE,
            fontsize=10, ha="right", fontweight="bold")
    ax.text(gnss[0] + 0.05, gnss[1] + 0.08, "GNSS Tx", color=PURPLE,
            fontsize=10, ha="left", fontweight="bold")

    # Straight line and bent path near limb
    ax.plot([leo[0], gnss[0]], [leo[1], gnss[1]], color=GREY, lw=1.0, ls=":",
            alpha=0.7, zorder=2, label="vacuum straight")
    # Bent ray: quadratic near tangent
    tt = np.linspace(0, 1, 200)
    xs = leo[0] + tt * (gnss[0] - leo[0])
    ys = leo[1] + tt * (gnss[1] - leo[1])
    # push toward Earth near closest approach
    mid = 0.48
    bump = 0.18 * np.exp(-((tt - mid) / 0.18) ** 2)
    # direction toward origin from mid point
    mx, my = xs[int(mid * 199)], ys[int(mid * 199)]
    rn = np.hypot(mx, my)
    ys_b = ys - bump * (my / rn) * 1.6
    xs_b = xs - bump * (mx / rn) * 1.6
    ax.plot(xs_b, ys_b, color=RED, lw=2.2, zorder=3)

    # Tangent / occultation point
    idx = int(np.argmin(np.hypot(xs_b, ys_b)))
    tp = np.array([xs_b[idx], ys_b[idx]])
    ax.plot(*tp, "o", color=RED, ms=8, zorder=6)
    ax.annotate(
        "tangent point\n(onion slice)",
        xy=tp, xytext=(0.15, -0.95),
        fontsize=9, color=RED, ha="center",
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
    )

    ax.plot([], [], color=RED, lw=2.2, label="refracted LEO←GNSS ray")
    ax.plot([], [], color=LIGHT_BLUE, lw=1.5, ls="--", label="ionosphere shell")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92)

    ax.text(
        0, -1.28,
        "Side-looking limb path → Ne(h) retrieval; geometry ≠ vertical ionosonde.",
        ha="center", fontsize=9, color="#444444",
    )
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-gnss-ro-geometry.png")


# ---------------------------------------------------------------------------
# 6. Satellite vs receiver DCB split
# ---------------------------------------------------------------------------
def fig_dcb_sat_rx_split() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.8),
                             gridspec_kw={"width_ratios": [1.15, 1.0], "wspace": 0.28})

    # Left: stacked bar contribution cartoon
    ax = axes[0]
    cats = ["sat DCB", "rx DCB", "true STEC\n(signal)"]
    # Convert ns-ish bias to TECU-equivalent schematic
    vals = np.array([4.5, 3.0, 22.0])
    colors = [ORANGE, PURPLE, BLUE]
    bottom = 0.0
    for v, c, lab in zip(vals, colors, cats):
        ax.bar(0, v, bottom=bottom, color=c, width=0.55, edgecolor="white", lw=1.2, label=lab)
        ax.text(0, bottom + v / 2, f"{v:.1f} TECU-eq", ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
        bottom += v
    ax.axhline(vals[2], color=BLUE, ls="--", lw=1.2, alpha=0.7)
    ax.annotate(
        "observed GF level\n= STEC + DCB_sat + DCB_rx",
        xy=(0.28, bottom), xytext=(0.7, bottom - 2),
        fontsize=9, color="#333",
        arrowprops=dict(arrowstyle="->", color=GREY),
    )
    ax.set_xlim(-0.7, 1.3)
    ax.set_ylim(0, 34)
    ax.set_xticks([])
    ax.set_ylabel("equivalent TEC [TECU, schematic]")
    ax.set_title("Who pads the STEC zero point?", fontsize=11)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)

    # Right: two satellites, one receiver — shared rx, different sat
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis("off")
    ax2.set_title("Split across links (same rx)", fontsize=11)

    # receiver
    ax2.plot(5, 1.2, "s", color=PURPLE, ms=18, zorder=5)
    ax2.text(5, 0.55, "Receiver\nDCB shared", ha="center", va="top",
             color=PURPLE, fontsize=9, fontweight="bold")

    # two sats
    for x, name, dcb in [(2.2, "Sat A", "+2.1"), (7.8, "Sat B", "−1.4")]:
        ax2.plot(x, 6.5, "^", color=ORANGE, ms=16, zorder=5)
        ax2.text(x, 7.15, f"{name}\nDCB {dcb} ns", ha="center", va="bottom",
                 color=ORANGE, fontsize=9, fontweight="bold")
        ax2.plot([x, 5], [6.5, 1.2], color=BLUE, lw=1.6, alpha=0.7)
        ax2.text((x + 5) / 2 + (0.3 if x < 5 else -0.3), 3.8,
                 "GF link", color=BLUE, fontsize=8, rotation=55 if x < 5 else -55)

    ax2.text(
        5, 2.6,
        "Sat DCB differs per PRN;\nRx DCB common → network\nseparability needs a datum.",
        ha="center", va="center", fontsize=8.5, color="#333",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fef9e7", edgecolor=ORANGE),
    )

    fig.suptitle("Satellite vs receiver DCB split (schematic)", fontsize=13, y=0.98)
    _footer(fig)
    fig.subplots_adjust(bottom=0.08, top=0.88)
    _save(fig, "fig-dcb-sat-rx-split.png")


# ---------------------------------------------------------------------------
# 7. Single-freq model guess vs dual-freq measure
# ---------------------------------------------------------------------------
def fig_singlefreq_vs_dualfreq() -> None:
    t = np.linspace(0, 24, 289)
    # "truth" STEC-driven delay on L1 (m)
    truth = 4.0 + 3.5 * np.sin(2 * np.pi * (t - 6) / 24) ** 2
    truth = np.clip(truth, 0.8, None)
    # single-freq broadcast-like model: smooth, underestimates afternoon
    model = 3.2 + 2.0 * np.sin(2 * np.pi * (t - 5) / 24) ** 2
    # dual-freq measure: truth + small noise
    rng = np.random.default_rng(3)
    dual = truth + 0.12 * rng.standard_normal(t.size)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6), sharey=True)

    ax = axes[0]
    ax.plot(t, truth, color=GREY, lw=1.8, ls="--", label="true $I_{L1}$ (schematic)")
    ax.plot(t, model, color=ORANGE, lw=2.2, label="single-freq model guess")
    ax.fill_between(t, model, truth, color=ORANGE, alpha=0.18, label="residual mist")
    ax.set_title("Single-frequency: guess with a model", fontsize=11)
    ax.set_xlabel("local time [h]")
    ax.set_ylabel(r"L1 iono delay $I$ [m]")
    ax.set_xlim(0, 24)
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.text(0.5, 0.05, "Klobuchar / NeQuick-G class\n→ residual still in position",
            transform=ax.transAxes, ha="center", fontsize=8, color="#555555")

    ax2 = axes[1]
    ax2.plot(t, truth, color=GREY, lw=1.8, ls="--", label="true $I_{L1}$")
    ax2.plot(t, dual, color=BLUE, lw=1.4, alpha=0.9, label="dual-freq measure (GF→I)")
    ax2.set_title("Dual-frequency: measure the mist", fontsize=11)
    ax2.set_xlabel("local time [h]")
    ax2.set_xlim(0, 24)
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.text(0.5, 0.05, "Same sky, second frequency\n→ STEC/I from observations",
             transform=ax2.transAxes, ha="center", fontsize=8, color="#555555")

    fig.suptitle("Guess vs measure: single-freq model vs dual-freq GNSS", fontsize=13, y=1.01)
    _footer(fig)
    fig.subplots_adjust(bottom=0.12, top=0.88, wspace=0.12)
    _save(fig, "fig-singlefreq-vs-dualfreq.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_catalog_nav()
    fig_gim_grid_ipps_coast()
    fig_pseudorange_to_stec()
    fig_iri_vs_ionosonde()
    fig_ionogram_trace()
    fig_gnss_ro_geometry()
    fig_dcb_sat_rx_split()
    fig_singlefreq_vs_dualfreq()
    print("done: 8 gap figures")


if __name__ == "__main__":
    main()
