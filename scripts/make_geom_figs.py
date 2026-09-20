#!/usr/bin/env python3
"""Original CC0 geometry / index / measurement schematics (no flowcharts).

Outputs under docs/tutorials/images/:
  fig-ipp-pierce-point.png
  fig-chapman-ne.png
  fig-dst-kp-timeline.png
  fig-dualfreq-tec.png
  fig-mapping-function.png
  fig-roti-map-schematic.png
  fig-phase-scint-time.png
  fig-tec-gradient.png
  fig-gnss-freq-bands.png
  fig-bias-dcb.png

Usage (from repo root):
  /workspace/iono-figs/.venv/bin/python scripts/make_geom_figs.py
  # or: .venv/bin/python scripts/make_geom_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "figure.dpi": 160,
    "savefig.dpi": 160,
    "axes.unicode_minus": False,
})

BLUE = "#2874a6"
GREEN = "#2ca25f"
RED = "#b22222"
ORANGE = "#e67e22"
LIGHT_BLUE = "#5dade2"
LIGHT_RED = "#e74c3c"
GREY = "#7f8c8d"
PURPLE = "#8e44ad"
TEAL = "#148f77"


def _cc0(ax, x=0.01, y=0.02):
    ax.text(x, y, "schematic · CC0", transform=ax.transAxes,
            fontsize=8, color=GREY, va="bottom")


def _save(fig, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_ipp_pierce_point() -> Path:
    """Receiver–satellite ray piercing thin shell at IPP + STEC slant path."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    earth = Circle((0, -0.15), 1.0, facecolor="#d5f5e3", edgecolor=GREEN, lw=2.0, zorder=1)
    ax.add_patch(earth)
    ax.text(0, -0.35, "Earth", ha="center", color="#1e8449", fontsize=10, fontweight="bold")

    shell_r = 1.55
    theta = np.linspace(np.deg2rad(25), np.deg2rad(155), 200)
    ax.plot(shell_r * np.cos(theta), shell_r * np.sin(theta) - 0.15,
            color=BLUE, lw=2.5, zorder=2)
    # faint shell band
    for dr in (-0.06, 0.06):
        ax.plot((shell_r + dr) * np.cos(theta), (shell_r + dr) * np.sin(theta) - 0.15,
                color="#d6eaf8", lw=6, alpha=0.5, zorder=0)
    ax.text(0, shell_r - 0.02, "thin shell H ≈ 350–450 km",
            ha="center", va="bottom", color=BLUE, fontsize=9)

    rx_ang = np.deg2rad(70)
    rx = (1.0 * np.cos(rx_ang), 1.0 * np.sin(rx_ang) - 0.15)
    ax.plot(*rx, "o", color="#1e8449", ms=9, zorder=5)
    ax.text(rx[0] - 0.12, rx[1] - 0.12, "receiver", color="#1e8449",
            fontsize=9, ha="right", va="top")

    sat = (2.35, 2.05)
    ax.plot(*sat, "^", color=ORANGE, ms=14, zorder=5)
    ax.text(sat[0] + 0.05, sat[1] + 0.05, "GNSS sat", color=ORANGE,
            fontsize=9, ha="left", va="bottom")

    ax.plot([rx[0], sat[0]], [rx[1], sat[1]], color=ORANGE, lw=1.8, zorder=3)

    t = np.linspace(0, 1, 400)
    xs = rx[0] + t * (sat[0] - rx[0])
    ys = rx[1] + t * (sat[1] - rx[1])
    dist = np.sqrt(xs**2 + (ys + 0.15)**2)
    idx = int(np.argmin(np.abs(dist - shell_r)))
    ipp = (xs[idx], ys[idx])

    near = np.abs(dist - shell_r) < 0.12
    ax.plot(xs[near], ys[near], color=RED, lw=4.5, alpha=0.55, zorder=4,
            solid_capstyle="round")
    mid_idxs = np.flatnonzero(near)
    mid = mid_idxs[len(mid_idxs) // 2]
    ax.text(xs[mid] - 0.38, ys[mid] + 0.16, "STEC slant path",
            color=RED, fontsize=9, fontweight="bold", rotation=38)

    ax.plot(*ipp, "o", color=PURPLE, ms=11, zorder=6)
    ax.annotate(
        "IPP\n(pierce point)",
        xy=ipp, xytext=(ipp[0] + 0.55, ipp[1] - 0.45),
        fontsize=10, color=PURPLE, fontweight="bold", ha="left",
        arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.5),
        zorder=7,
    )

    cx, cy = 0.0, -0.15
    vdir = np.array([ipp[0] - cx, ipp[1] - cy])
    vdir = vdir / np.linalg.norm(vdir)
    ax.annotate(
        "", xy=ipp + 0.45 * vdir, xytext=ipp,
        arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4),
        zorder=4,
    )
    ax.text(*(ipp + 0.52 * vdir), "local\nvertical", color=GREY, fontsize=8, ha="center")

    ax.annotate(
        "", xy=(rx[0] + 0.55, rx[1] + 0.35), xytext=rx,
        arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.3),
    )
    ax.text(rx[0] + 0.65, rx[1] + 0.28, "elev. E", color=TEAL, fontsize=9)

    ax.set_xlim(-1.6, 2.8)
    ax.set_ylim(-1.35, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Ionospheric pierce point (IPP) on thin shell (schematic)")
    _cc0(ax)
    return _save(fig, "fig-ipp-pierce-point.png")


def fig_chapman_ne() -> Path:
    """Single Chapman Ne(h) emphasizing hmF2 peak (distinct from D/E/F band chart)."""
    fig, ax = plt.subplots(figsize=(6.4, 5.8))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    h = np.linspace(80, 700, 700)
    hmF2 = 300.0
    NmF2 = 1.0
    H = 55.0
    z = (h - hmF2) / H
    ne = NmF2 * np.exp(0.5 * (1.0 - z - np.exp(-z)))
    # faint secondary E bump for context only — no D/E/F band labels
    hmE, HE = 110.0, 14.0
    zE = (h - hmE) / HE
    ne = ne + 0.16 * np.exp(0.5 * (1.0 - zE - np.exp(-zE)))

    ax.fill_betweenx(h, 0, ne, color="#d4e6f1", alpha=0.7, zorder=0)
    ax.plot(ne, h, color=BLUE, lw=2.5, zorder=2)

    ax.axhline(hmF2, color=RED, ls="--", lw=1.5, zorder=1)
    ax.plot(NmF2, hmF2, "o", color=RED, ms=10, zorder=4)
    ax.annotate(
        r"$h_m$F2 peak",
        xy=(NmF2, hmF2),
        xytext=(0.45, 420),
        fontsize=12,
        color=RED,
        fontweight="bold",
        arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6),
        zorder=5,
    )
    ax.text(NmF2 + 0.05, hmF2 - 50, r"$N_m$F2", color=RED, fontsize=10)
    ax.annotate(
        "",
        xy=(0.22, hmF2 + H),
        xytext=(0.22, hmF2),
        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.5),
    )
    ax.text(0.26, hmF2 + H / 2, r"$H$", color=ORANGE, fontsize=11, va="center")

    ax.set_xlabel(r"Electron density $N_e$ (relative)")
    ax.set_ylabel("Altitude (km)")
    ax.set_xlim(0, 1.25)
    ax.set_ylim(80, 700)
    ax.set_title(r"Chapman $N_e(h)$ — F2 peak height $h_m$F2")
    ax.grid(True, alpha=0.25)
    _cc0(ax)
    fig.tight_layout()
    return _save(fig, "fig-chapman-ne.png")


def fig_dst_kp_timeline() -> Path:
    """Dual-panel Dst/SYM-H and Kp during a schematic storm."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.0, 5.4), sharex=True)
    fig.patch.set_facecolor("white")

    t = np.linspace(0, 72, 721)
    onset = 18.0
    main = 24.0
    dst = -8 + 4 * np.sin(2 * np.pi * t / 24)
    dst = np.where(t >= onset, dst + 25 * np.exp(-((t - onset) / 1.2) ** 2), dst)
    main_depth = -95 * (1 - np.exp(-(np.clip(t - main, 0, None)) / 3.5))
    recover = np.exp(-(np.clip(t - (main + 10), 0, None)) / 22.0)
    dst = np.where(t >= main, dst + main_depth * recover, dst)

    ax1.set_facecolor("white")
    ax1.plot(t, dst, color=BLUE, lw=2.2, label="Dst / SYM-H proxy")
    ax1.axhline(0, color=GREY, lw=0.8)
    ax1.axvline(onset, color=ORANGE, ls=":", lw=1.4)
    ax1.axvline(main, color=RED, ls=":", lw=1.4)
    ax1.fill_between(t, dst, 0, where=dst < 0, color=LIGHT_BLUE, alpha=0.35)
    ax1.text(onset + 0.4, 28, "SSC", color=ORANGE, fontsize=9)
    ax1.text(main + 0.5, -88, "main-phase\nvalley", color=RED, fontsize=9, va="top")
    ax1.set_ylabel("Dst / SYM-H (nT)")
    ax1.set_ylim(-110, 40)
    ax1.legend(loc="lower right", fontsize=9)
    ax1.grid(True, alpha=0.25)
    ax1.set_title("Geomagnetic indices during a storm (schematic)")

    rng = np.random.default_rng(7)
    edges = np.arange(0, 72, 3)
    kp = np.clip(
        1.5
        + 0.4 * np.sin(2 * np.pi * edges / 24)
        + np.where(edges >= onset, 4.5 * np.exp(-((edges - (main + 2)) / 10) ** 2), 0)
        + 0.35 * rng.standard_normal(len(edges)),
        0, 9,
    )
    colors = [GREEN if k < 4 else (ORANGE if k < 6 else RED) for k in kp]
    ax2.bar(edges, kp, width=2.6, align="edge", color=colors, edgecolor="0.3", lw=0.4)
    ax2.axhline(4, color=GREY, ls="--", lw=1.0)
    ax2.text(1, 4.15, "Kp≈4", color=GREY, fontsize=8)
    ax2.set_xlim(0, 72)
    ax2.set_ylim(0, 9)
    ax2.set_xlabel("Time (hours from quiet start)")
    ax2.set_ylabel("Kp (3 h)")
    ax2.grid(True, alpha=0.25, axis="y")
    _cc0(ax2)

    fig.tight_layout()
    return _save(fig, "fig-dst-kp-timeline.png")


def fig_dualfreq_tec() -> Path:
    """Dual-frequency delay difference → STEC (distinct from geometry-free cartoon)."""
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.6),
                             gridspec_kw=dict(width_ratios=[1.05, 1.0], wspace=0.32))
    fig.patch.set_facecolor("white")

    ax = axes[0]
    ax.set_facecolor("white")
    f = np.linspace(1.0, 1.7, 200)
    stec = 20e16
    I = 40.3 * stec / (f * 1e9) ** 2
    ax.plot(f, I, color=BLUE, lw=2.3)
    marks = [(1.57542, "L1", GREEN), (1.22760, "L2", ORANGE), (1.17645, "L5", TEAL)]
    for ff, lab, col in marks:
        ii = 40.3 * stec / (ff * 1e9) ** 2
        ax.plot(ff, ii, "o", color=col, ms=8)
        ax.annotate(lab, xy=(ff, ii), xytext=(ff + 0.04, ii + 0.25),
                    fontsize=9, color=col)
    # Delta between L1 and L2
    i1 = 40.3 * stec / (1.57542e9) ** 2
    i2 = 40.3 * stec / (1.22760e9) ** 2
    ax.annotate(
        "", xy=(1.22760 - 0.03, i1), xytext=(1.22760 - 0.03, i2),
        arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6),
    )
    ax.text(1.10, (i1 + i2) / 2, r"$\Delta I$", color=RED, fontsize=11,
            fontweight="bold", va="center")
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Group delay I (m) for STEC=20 TECU")
    ax.set_title(r"$I \propto \mathrm{STEC}/f^{2}$")
    ax.grid(True, alpha=0.25)
    _cc0(ax)

    ax2 = axes[1]
    ax2.set_facecolor("white")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    box = FancyBboxPatch(
        (0.5, 5.0), 9.0, 4.0, boxstyle="round,pad=0.2,rounding_size=0.35",
        facecolor="#eaf2f8", edgecolor=BLUE, lw=1.8,
    )
    ax2.add_patch(box)
    ax2.text(
        5.0, 7.6,
        r"$\mathrm{STEC} \propto \dfrac{f_1^{2} f_2^{2}}{f_1^{2}-f_2^{2}}"
        r"\,(I_2 - I_1)$",
        ha="center", va="center", fontsize=12, color="#1a5276",
    )
    ax2.text(5.0, 5.8, "group-delay difference → TEC",
             ha="center", fontsize=11, color=BLUE)

    ax2.barh([3.0], [3.2], height=0.5, left=2.2, color=GREEN, alpha=0.85)
    ax2.barh([1.7], [5.0], height=0.5, left=2.2, color=ORANGE, alpha=0.85)
    ax2.text(1.9, 3.0, r"$I_1$", ha="right", va="center", color=GREEN, fontsize=11)
    ax2.text(1.9, 1.7, r"$I_2$", ha="right", va="center", color=ORANGE, fontsize=11)
    ax2.text(5.0, 0.6, r"$f_1 > f_2$  ⇒  $I_1 < I_2$", ha="center",
             fontsize=10, color=GREY)
    ax2.set_title("Dual-frequency TEC estimate")

    fig.suptitle("Dual-frequency TEC from group delay (schematic)", fontsize=13, y=1.02)
    return _save(fig, "fig-dualfreq-tec.png")


def fig_mapping_function() -> Path:
    """Thin-shell mapping function M(E)."""
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    RE = 6371.0
    elev = np.linspace(5, 90, 400)

    for H, col, ls in [(350, BLUE, "-"), (450, ORANGE, "--")]:
        zprime = np.arcsin((RE / (RE + H)) * np.cos(np.deg2rad(elev)))
        M = 1.0 / np.cos(zprime)
        ax.plot(elev, M, color=col, lw=2.2, ls=ls, label=f"H = {H} km")

    ax.axhline(1.0, color=GREY, lw=0.9, ls=":")
    ax.axvline(15, color=GREY, ls="--", lw=1.0, alpha=0.8)
    ax.text(15.5, 2.55, "typical\ncutoff", color=GREY, fontsize=8, va="top")

    ax.set_xlim(5, 90)
    ax.set_ylim(0.9, 3.2)
    ax.set_xlabel("Elevation angle E (°)")
    ax.set_ylabel(r"Mapping factor $M(E)$")
    ax.set_title(r"Thin-shell mapping: $\mathrm{STEC}\approx M(E)\cdot\mathrm{VTEC}$")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.25)
    ax.text(
        0.50, 0.18,
        r"$M=\left(1-\left(\frac{R_E}{R_E+H}\cos E\right)^2\right)^{-1/2}$",
        transform=ax.transAxes, fontsize=9, color=BLUE,
        bbox=dict(boxstyle="round", facecolor="#eaf2f8", edgecolor=BLUE, alpha=0.9),
    )
    _cc0(ax)
    fig.tight_layout()
    return _save(fig, "fig-mapping-function.png")


def fig_roti_map_schematic() -> Path:
    """Lat–lon schematic ROTI map with equatorial nightside hotspots."""
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    lon = np.linspace(-90, 90, 241)
    lat = np.linspace(-40, 40, 161)
    LON, LAT = np.meshgrid(lon, lat)

    roti = 0.05 + 0.02 * np.cos(np.deg2rad(LON / 3))
    for lon0 in (-35, 20):
        roti += 0.55 * np.exp(
            -0.5 * ((LAT - 8) / 6) ** 2
            - 0.5 * ((LON - lon0) / 12) ** 2
        )
        roti += 0.50 * np.exp(
            -0.5 * ((LAT + 10) / 6.5) ** 2
            - 0.5 * ((LON - lon0 + 3) / 11) ** 2
        )
    rng = np.random.default_rng(3)
    roti += 0.015 * rng.standard_normal(LON.shape)

    cmap = LinearSegmentedColormap.from_list(
        "roti", ["#fef9e7", "#f9e79f", "#f5b041", "#e74c3c", "#6c3483"],
    )
    pcm = ax.pcolormesh(LON, LAT, roti, shading="auto", cmap=cmap, vmin=0, vmax=0.7)
    ax.axhline(0, color="white", ls=":", lw=1.0, alpha=0.7)
    ax.annotate(
        "nightside\nEPB / scint\nhotspots",
        xy=(-35, 8), xytext=(-75, 28),
        fontsize=9, color="#4a235a", fontweight="bold",
        arrowprops=dict(arrowstyle="-|>", color="#4a235a", lw=1.4),
    )
    cbar = fig.colorbar(pcm, ax=ax, pad=0.02, fraction=0.046)
    cbar.set_label("ROTI (schematic TECU/min)")
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("ROTI map schematic (post-sunset equatorial)")
    ax.set_xlim(-90, 90)
    ax.set_ylim(-40, 40)
    ax.grid(True, alpha=0.25, color="white", lw=0.5)
    _cc0(ax)
    fig.tight_layout()
    return _save(fig, "fig-roti-map-schematic.png")


def fig_phase_scint_time() -> Path:
    """Phase scintillation time series with quiet → burst."""
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    rng = np.random.default_rng(11)
    t = np.linspace(0, 10, 2001)
    phi = 0.08 * rng.standard_normal(len(t))
    kernel = np.ones(15) / 15
    phi = np.convolve(phi, kernel, mode="same")
    burst = (t > 3.5) & (t < 7.0)
    env = np.exp(-((t - 5.2) / 1.1) ** 2)
    phi = phi + burst * env * (1.8 * rng.standard_normal(len(t)))
    phi += 0.15 * np.sin(2 * np.pi * t / 4.5)

    ax.plot(t, phi, color=BLUE, lw=1.0)
    ax.axvspan(3.5, 7.0, color=LIGHT_RED, alpha=0.18, label="scintillation window")
    ax.set_xlim(0, 10)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel(r"Phase residual $\delta\phi$ (rad, schematic)")
    ax.set_title("Phase scintillation time series (schematic)")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.25)
    _cc0(ax)
    fig.tight_layout()
    return _save(fig, "fig-phase-scint-time.png")


def fig_tec_gradient() -> Path:
    """Horizontal TEC gradient schematic: profile + ∇TEC."""
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8.5, 5.4), sharex=True,
        gridspec_kw=dict(height_ratios=[1.2, 1.0], hspace=0.08),
    )
    fig.patch.set_facecolor("white")

    x = np.linspace(-800, 800, 801)
    vtec = (
        28
        - 3 * (x / 800) ** 2
        - 12 / (1 + np.exp(-(x + 80) / 18))
        + 12 / (1 + np.exp(-(x - 220) / 22))
    )
    vtec += 1.2 * np.sin(2 * np.pi * x / 280)

    ax1.set_facecolor("white")
    ax1.plot(x, vtec, color=BLUE, lw=2.2)
    ax1.fill_between(x, 10, vtec, color=LIGHT_BLUE, alpha=0.2)
    ax1.axvspan(-140, -20, color=ORANGE, alpha=0.15)
    ax1.text(-80, 31, "steep wall", color=ORANGE, fontsize=9, ha="center")
    ax1.set_ylabel("VTEC (TECU)")
    ax1.set_ylim(10, 34)
    ax1.set_title("Horizontal TEC structure & gradient (schematic)")
    ax1.grid(True, alpha=0.25)

    grad = np.gradient(vtec, x)
    grad100 = grad * 100
    ax2.set_facecolor("white")
    ax2.plot(x, grad100, color=RED, lw=2.0)
    ax2.axhline(0, color=GREY, lw=0.8)
    ax2.fill_between(
        x, 0, grad100, where=np.abs(grad100) > 1.5,
        color=LIGHT_RED, alpha=0.35,
    )
    ax2.set_xlabel("Horizontal distance (km)")
    ax2.set_ylabel(r"$\nabla$TEC (TECU / 100 km)")
    ax2.set_xlim(-800, 800)
    ax2.grid(True, alpha=0.25)
    _cc0(ax2)

    fig.tight_layout()
    return _save(fig, "fig-tec-gradient.png")


def fig_gnss_freq_bands() -> Path:
    """GNSS frequency bands L1/L2/L5 schematic bars."""
    fig, ax = plt.subplots(figsize=(9.0, 4.0))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    bands = [
        ("GPS L5 / Galileo E5a", 1176.45, TEAL),
        ("GPS L2", 1227.60, BLUE),
        ("Galileo E6", 1278.75, PURPLE),
        ("GPS L1 / Galileo E1", 1575.42, RED),
    ]
    for i, (name, f, col) in enumerate(bands):
        ax.barh(i, 40, left=f - 20, height=0.55, color=col, alpha=0.75, edgecolor="0.2")
        ax.text(f, i, f"{name}\n{f:.2f} MHz", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")

    ax.set_yticks([])
    ax.set_xlabel("Frequency (MHz)")
    ax.set_xlim(1100, 1650)
    ax.set_ylim(-0.8, 3.8)
    ax.set_title("Selected GNSS frequency bands (schematic)")
    ax.grid(True, axis="x", alpha=0.3)
    ax.text(
        0.5, -0.18,
        r"Lower $f$ → larger ionospheric delay ($\propto 1/f^{2}$)",
        transform=ax.transAxes, ha="center", color=GREY, fontsize=9,
    )
    _cc0(ax, y=0.04)
    fig.tight_layout()
    return _save(fig, "fig-gnss-freq-bands.png")


def fig_bias_dcb() -> Path:
    """DCB as a vertical offset masquerading as TEC."""
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    t = np.linspace(0, 24, 289)
    true_stec = 12 + 10 * np.sin(2 * np.pi * (t - 6) / 24)
    true_stec = np.clip(true_stec, 4, None)
    dcb_offset = 5.5
    biased = true_stec + dcb_offset

    ax.plot(t, true_stec, color=GREEN, lw=2.3, label="True STEC (schematic)")
    ax.plot(t, biased, color=RED, lw=2.3, label="Uncorrected GF→STEC (+DCB)")
    ax.fill_between(t, true_stec, biased, color=LIGHT_RED, alpha=0.3,
                     label="DCB masquerading as TEC")
    ax.annotate(
        "", xy=(12, true_stec[144] + dcb_offset), xytext=(12, true_stec[144]),
        arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.8),
    )
    ax.text(12.3, true_stec[144] + dcb_offset / 2, "≈ constant\nDCB offset",
            color=PURPLE, fontsize=9, va="center")

    ax.set_xlim(0, 24)
    ax.set_ylim(0, 32)
    ax.set_xlabel("Local time (h)")
    ax.set_ylabel("STEC (TECU)")
    ax.set_title("Differential code bias (DCB) as a TEC-like offset (schematic)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.25)
    _cc0(ax)
    fig.tight_layout()
    return _save(fig, "fig-bias-dcb.png")


def main() -> None:
    paths = [
        fig_ipp_pierce_point(),
        fig_chapman_ne(),
        fig_dst_kp_timeline(),
        fig_dualfreq_tec(),
        fig_mapping_function(),
        fig_roti_map_schematic(),
        fig_phase_scint_time(),
        fig_tec_gradient(),
        fig_gnss_freq_bands(),
        fig_bias_dcb(),
    ]
    for p in paths:
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
