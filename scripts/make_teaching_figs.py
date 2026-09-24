#!/usr/bin/env python3
"""Additional teaching schematics for tutorials 19–23.

Synthetic CC0 figures (matplotlib). Not real event data.
Usage (repo root):
  .venv/bin/python scripts/make_teaching_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials" / "images"

mpl.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.unicode_minus": False,
        "figure.dpi": 140,
        "savefig.dpi": 140,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.6,
    }
)

FOOT = "schematic · CC0"
BLUE = "#2874a6"
GREEN = "#2ca25f"
RED = "#b22222"
ORANGE = "#e67e22"
PURPLE = "#8e44ad"
GREY = "#7f8c8d"
LIGHT_BLUE = "#5dade2"
LIGHT_RED = "#e74c3c"


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def fig_ipp_pierce_point() -> None:
    """Satellite–receiver ray intersecting thin shell at IPP."""
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    ax.set_xlim(-1.2, 10.5)
    ax.set_ylim(-0.4, 7.2)
    ax.axis("off")
    ax.set_title("IPP / pierce-point geometry (thin shell)", fontsize=12, pad=6)

    # Earth arc
    earth = patches.Arc((4.5, -6.5), 18, 18, theta1=55, theta2=125,
                        color=GREEN, lw=2.5)
    ax.add_patch(earth)
    ax.plot([1.2, 7.8], [0.15, 0.15], color=GREEN, lw=2.0)
    ax.text(4.5, -0.15, "ground / Earth surface", ha="center", va="top",
            color="#1e8449", fontsize=9)

    # Receiver
    ax.plot(3.0, 0.35, "o", color="#1e8449", ms=10, zorder=5)
    ax.text(3.0, 0.55, "Rx", ha="center", va="bottom", fontsize=10,
            fontweight="bold", color="#1e8449")

    # Thin shell
    ax.plot([0.4, 9.2], [3.6, 3.6], color=BLUE, lw=2.2, ls="--")
    ax.fill_between([0.4, 9.2], 3.35, 3.85, color="#d6eaf8", alpha=0.55, zorder=0)
    ax.text(9.0, 3.95, "thin shell ~350–450 km", ha="right", va="bottom",
            color=BLUE, fontsize=9)

    # Satellite
    ax.plot(8.6, 6.4, "^", color=PURPLE, ms=14, zorder=5)
    ax.text(8.6, 6.7, "GNSS sat", ha="center", va="bottom", color=PURPLE, fontsize=9)

    # Ray Rx -> sat
    ax.plot([3.0, 8.6], [0.35, 6.4], color=RED, lw=2.0, zorder=3)
    # IPP at intersection with shell y=3.6
    # line: (x-3)/(8.6-3) = (y-0.35)/(6.4-0.35)
    t = (3.6 - 0.35) / (6.4 - 0.35)
    ipp_x = 3.0 + t * (8.6 - 3.0)
    ax.plot(ipp_x, 3.6, "o", color=ORANGE, ms=12, zorder=6,
            markeredgecolor="white", markeredgewidth=1.2)
    ax.annotate(
        "IPP\npierce point",
        xy=(ipp_x, 3.6), xytext=(ipp_x - 2.4, 4.8),
        fontsize=10, color=ORANGE, fontweight="bold", ha="center",
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4),
    )

    # Zenith angle mark
    ax.plot([3.0, 3.0], [0.35, 5.5], color=GREY, ls=":", lw=1.2)
    ax.text(3.15, 2.2, r"$\chi$ / elev.", color=GREY, fontsize=9)

    ax.text(
        5.2, 1.4,
        "STEC along ray → map to VTEC at IPP",
        ha="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fff8e7", edgecolor=ORANGE),
    )
    ax.text(0.02, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color=GREY)
    _save(fig, "fig-ipp-pierce-point.png")


def fig_chapman_layer() -> None:
    """Chapman production / Ne profile vs height."""
    h = np.linspace(80, 520, 500)
    hm, H, Nm = 300.0, 50.0, 1.0
    z = (h - hm) / H
    ne = Nm * np.exp(0.5 * (1.0 - z - np.exp(-z)))
    # production rate peak slightly below hm for teaching
    q = 0.85 * np.exp(1.0 - z - np.exp(-z))  # classic Chapman q

    fig, ax = plt.subplots(figsize=(5.4, 6.6))
    ax.plot(ne, h, color=BLUE, lw=2.4, label=r"$N_e$ (Chapman)")
    ax.plot(q, h, color=ORANGE, lw=2.0, ls="--", label=r"production $q$")
    ax.axhline(hm, color=GREY, ls=":", lw=1.0)
    ax.plot(Nm, hm, "o", color=RED, ms=8, zorder=5)
    ax.annotate(
        r"$h_m$, $N_m$",
        xy=(Nm, hm), xytext=(0.55, 380),
        fontsize=10, color=RED,
        arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2),
    )
    ax.fill_betweenx(h, 0, ne, color=BLUE, alpha=0.12)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(80, 520)
    ax.set_xlabel("Relative $N_e$ / $q$ (schematic)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("Chapman layer profile (schematic)")
    ax.legend(loc="upper right", fontsize=9)
    ax.text(0.02, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color=GREY)
    _save(fig, "fig-chapman-layer.png")


def fig_dst_kp_timeline() -> None:
    """Synthetic Dst/SYM-H and Kp with storm windows."""
    t = np.linspace(0, 72, 721)  # hours
    # Quiet then storm: sudden commencement ~18 h, main phase trough ~28 h
    dst = -8 + 4 * np.sin(2 * np.pi * t / 24)
    sc = 18.0
    main = 28.0
    # SSC bump
    dst = dst + 25 * np.exp(-0.5 * ((t - sc) / 1.2) ** 2)
    # Main phase trough
    trough = -95 * np.exp(-0.5 * ((t - main) / 5.5) ** 2)
    # Recovery
    recovery = np.where(
        t > main,
        -40 * np.exp(-(t - main) / 22.0) * (1 - np.exp(-(t - main) / 4.0)),
        0.0,
    )
    dst = dst + trough + recovery

    # Kp stepwise (3-h bars feel)
    kp = np.zeros_like(t)
    for i, tt in enumerate(t):
        if tt < 15:
            kp[i] = 1.5 + 0.3 * np.sin(tt)
        elif tt < 20:
            kp[i] = 4.0
        elif tt < 36:
            kp[i] = 7.0 - 0.05 * (tt - 20)
        elif tt < 48:
            kp[i] = 4.5
        else:
            kp[i] = 2.5
    # quantize to 3-h feel
    kp = np.round(kp * 3) / 3

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.8, 5.4), sharex=True)
    ax1.plot(t, dst, color=BLUE, lw=2.0)
    ax1.axhline(0, color=GREY, lw=0.8)
    ax1.axvspan(sc - 1, main + 2, color="#f5cba7", alpha=0.45, label="main-phase window")
    ax1.axvspan(main + 2, 55, color="#d6eaf8", alpha=0.4, label="recovery")
    ax1.axvline(main, color=RED, ls="--", lw=1.2)
    ax1.annotate("SYM-H / Dst min", xy=(main, dst[np.argmin(np.abs(t - main))]),
                 xytext=(38, -40),
                 arrowprops=dict(arrowstyle="-|>", color=RED),
                 color=RED, fontsize=9)
    ax1.set_ylabel("SYM-H / Dst (nT, sch.)")
    ax1.set_ylim(-120, 40)
    ax1.set_title("Dst / Kp timeline vs disturbance windows")
    ax1.legend(loc="lower right", fontsize=8)
    ax1.text(0.02, 0.92, "ring-current index", transform=ax1.transAxes,
             color=BLUE, fontsize=9, fontweight="bold", va="top")

    # Kp as step bars
    edges = np.arange(0, 73, 3)
    kp_bar = []
    for a, b in zip(edges[:-1], edges[1:]):
        mid = 0.5 * (a + b)
        kp_bar.append(kp[np.argmin(np.abs(t - mid))])
    ax2.bar(edges[:-1], kp_bar, width=2.7, align="edge", color=ORANGE,
            edgecolor="white", alpha=0.85)
    ax2.axhline(5, color=GREY, ls=":", lw=1.0)
    ax2.text(1, 5.15, "Kp≈5", color=GREY, fontsize=8)
    ax2.set_ylabel("Kp (schematic)")
    ax2.set_xlabel("Time (hours)")
    ax2.set_xlim(0, 72)
    ax2.set_ylim(0, 9)
    ax2.text(0.02, 0.04, FOOT, transform=ax2.transAxes, fontsize=8, color=GREY)
    fig.tight_layout()
    _save(fig, "fig-dst-kp-timeline.png")


def fig_dualfreq_tec() -> None:
    """Geometry-free dual-frequency combination → STEC idea."""
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.4),
                             gridspec_kw=dict(width_ratios=[1.05, 1.0], wspace=0.32))

    # Left: two frequencies, iono delay ~ 1/f^2
    ax = axes[0]
    f = np.linspace(1.1, 1.7, 200)  # GHz
    # relative delay
    delay = (1.575 / f) ** 2
    ax.plot(f, delay, color=BLUE, lw=2.2)
    for freq, lab, c in [(1.575, "L1", GREEN), (1.227, "L2", RED), (1.176, "L5", ORANGE)]:
        d = (1.575 / freq) ** 2
        ax.plot(freq, d, "o", color=c, ms=9, zorder=5)
        ax.annotate(lab, xy=(freq, d), xytext=(freq + 0.02, d + 0.12),
                    color=c, fontsize=10, fontweight="bold")
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel(r"Iono delay $\propto 1/f^2$ (rel.)")
    ax.set_title("Frequency dependence")
    ax.set_xlim(1.05, 1.75)
    ax.set_ylim(0.8, 2.1)
    ax.text(0.02, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color=GREY)

    # Right: geometry-free combo schematic
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.set_title("Geometry-free → STEC")
    boxes = [
        (0.5, 7.2, 4.0, 1.6, "L1 phase/code\n$P_1$ / $\\Phi_1$", GREEN),
        (5.5, 7.2, 4.0, 1.6, "L2 phase/code\n$P_2$ / $\\Phi_2$", RED),
        (2.0, 4.0, 6.0, 1.8, r"GF: $P_2-P_1$ or $\Phi_1-\Phi_2$" "\n(geometry cancels)", BLUE),
        (2.0, 1.0, 6.0, 1.6, r"$\propto$ STEC (+ biases)", ORANGE),
    ]
    for x, y, w, h, txt, c in boxes:
        ax2.add_patch(patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.08",
            facecolor="white", edgecolor=c, lw=2.0,
        ))
        ax2.text(x + w / 2, y + h / 2, txt, ha="center", va="center",
                 fontsize=9, color=c, fontweight="bold")
    ax2.annotate("", xy=(5, 5.8), xytext=(2.5, 7.2),
                 arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4))
    ax2.annotate("", xy=(5, 5.8), xytext=(7.5, 7.2),
                 arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4))
    ax2.annotate("", xy=(5, 2.6), xytext=(5, 4.0),
                 arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4))

    fig.suptitle("Dual-frequency TEC (geometry-free) schematic", fontsize=12, y=1.02)
    _save(fig, "fig-dualfreq-tec.png")


def fig_mapping_function() -> None:
    """STEC → VTEC via thin-shell mapping function vs elevation."""
    elev = np.linspace(10, 90, 200)
    # simple single-layer mapping: M(e) = 1/sqrt(1 - (Re/(Re+H) cos e)^2)
    Re, H = 6371.0, 350.0
    zenith = np.deg2rad(90 - elev)
    ratio = Re / (Re + H)
    M = 1.0 / np.sqrt(1.0 - (ratio * np.sin(zenith)) ** 2)
    # STEC = M * VTEC; show both curves for fixed VTEC=20
    vtec = 20.0
    stec = M * vtec

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 4.2),
                                   gridspec_kw=dict(wspace=0.32))

    ax1.plot(elev, M, color=BLUE, lw=2.2)
    ax1.axhline(1.0, color=GREY, ls=":", lw=1.0)
    ax1.set_xlabel("Elevation (°)")
    ax1.set_ylabel(r"Mapping $M(e)$ = STEC/VTEC")
    ax1.set_title("Thin-shell mapping function")
    ax1.set_xlim(10, 90)
    ax1.set_ylim(0.9, 3.2)
    ax1.annotate("low elev.\n→ large M", xy=(15, M[np.argmin(np.abs(elev - 15))]),
                 xytext=(35, 2.7),
                 arrowprops=dict(arrowstyle="-|>", color=ORANGE),
                 color=ORANGE, fontsize=9)

    ax2.plot(elev, stec, color=RED, lw=2.2, label="STEC")
    ax2.axhline(vtec, color=GREEN, lw=2.0, ls="--", label="VTEC=20 TECU")
    ax2.fill_between(elev, vtec, stec, color=LIGHT_RED, alpha=0.2)
    ax2.set_xlabel("Elevation (°)")
    ax2.set_ylabel("TEC (TECU, schematic)")
    ax2.set_title(r"STEC $= M(e)\times$ VTEC")
    ax2.set_xlim(10, 90)
    ax2.set_ylim(15, 65)
    ax2.legend(loc="upper right", fontsize=9)
    ax2.text(0.02, 0.02, FOOT, transform=ax2.transAxes, fontsize=8, color=GREY)

    fig.suptitle("STEC → VTEC mapping (thin shell)", fontsize=12, y=1.02)
    _save(fig, "fig-mapping-function.png")


def fig_phase_scint() -> None:
    """Phase scintillation: carrier phase jitter time series + σφ idea."""
    rng = np.random.default_rng(21)
    t = np.linspace(0, 10, 2000)  # minutes
    # Quiet then burst
    env = 0.05 + 1.8 * np.exp(-0.5 * ((t - 5.2) / 0.9) ** 2)
    noise = rng.standard_normal(t.size)
    # colored noise
    kernel = np.ones(5) / 5
    noise = np.convolve(noise, kernel, mode="same")
    phase = env * noise  # radians schematic
    # also a slow ramp (detrend idea)
    phase = phase + 0.02 * (t - 5)

    # rolling sigma
    win = 50
    sig = np.array([
        np.std(phase[max(0, i - win): i + 1]) for i in range(t.size)
    ])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 5.0), sharex=True)
    ax1.plot(t, phase, color=BLUE, lw=0.8)
    ax1.axvspan(4.0, 6.5, color="#f5cba7", alpha=0.4)
    ax1.set_ylabel(r"Carrier phase residual (rad, sch.)")
    ax1.set_title("Phase scintillation (schematic)")
    ax1.text(0.02, 0.88, "phase jitter burst", transform=ax1.transAxes,
             color=ORANGE, fontsize=9, fontweight="bold")

    ax2.plot(t, sig, color=RED, lw=1.8, label=r"$\sigma_\varphi$ (rolling)")
    ax2.axhline(0.5, color=GREY, ls="--", lw=1.0)
    ax2.text(0.2, 0.52, r"elevated $\sigma_\varphi$", color=GREY, fontsize=8)
    ax2.set_xlabel("Time (min)")
    ax2.set_ylabel(r"$\sigma_\varphi$ (rad, sch.)")
    ax2.set_xlim(0, 10)
    ax2.legend(loc="upper right", fontsize=9)
    ax2.text(0.02, 0.04, FOOT, transform=ax2.transAxes, fontsize=8, color=GREY)
    fig.tight_layout()
    _save(fig, "fig-phase-scint.png")


def fig_tec_gradient() -> None:
    """Horizontal TEC gradient / bubble wall steep gradient."""
    lon = np.linspace(-15, 15, 300)
    lat = np.linspace(-20, 20, 240)
    LON, LAT = np.meshgrid(lon, lat)

    # Background EIA-ish
    tec = (
        18
        + 12 * np.exp(-0.5 * ((LAT - 15) / 6) ** 2)
        + 12 * np.exp(-0.5 * ((LAT + 15) / 6) ** 2)
        - 3 * np.exp(-0.5 * (LAT / 5) ** 2)
    )
    # Depletion channel (bubble) along longitude near lon=0, elongated in lat
    wall = 14 * np.exp(-0.5 * (LON / 1.8) ** 2) * (1 - 0.35 * (LAT / 20) ** 2)
    tec = tec - wall

    # Gradient magnitude
    gy, gx = np.gradient(tec, lat[1] - lat[0], lon[1] - lon[0])
    gmag = np.hypot(gx, gy)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.4),
                                   gridspec_kw=dict(wspace=0.28))
    cmap = LinearSegmentedColormap.from_list(
        "tec", ["#1a5276", "#5dade2", "#a9dfbf", "#f9e79f", "#e74c3c"],
    )
    pcm1 = ax1.pcolormesh(LON, LAT, tec, shading="auto", cmap=cmap, vmin=5, vmax=35)
    ax1.axvline(0, color="white", ls="--", lw=1.0, alpha=0.7)
    ax1.set_title("VTEC with bubble channel")
    ax1.set_xlabel("Relative lon (°)")
    ax1.set_ylabel("Relative lat (°)")
    fig.colorbar(pcm1, ax=ax1, fraction=0.046, pad=0.04, label="VTEC (TECU)")
    ax1.annotate("depletion\nchannel", xy=(0, 0), xytext=(6, -12),
                 color="white", fontsize=9, fontweight="bold",
                 arrowprops=dict(arrowstyle="-|>", color="white", lw=1.2))

    pcm2 = ax2.pcolormesh(LON, LAT, gmag, shading="auto", cmap="inferno",
                          vmin=0, vmax=np.percentile(gmag, 99))
    ax2.set_title(r"$|\nabla$ TEC$|$ (bubble walls)")
    ax2.set_xlabel("Relative lon (°)")
    ax2.set_ylabel("Relative lat (°)")
    fig.colorbar(pcm2, ax=ax2, fraction=0.046, pad=0.04, label="TECU/°")
    ax2.annotate("steep walls\n→ ROTI / scint", xy=(-2, 5), xytext=(-12, 12),
                 color="white", fontsize=9,
                 arrowprops=dict(arrowstyle="-|>", color="white", lw=1.2))
    ax2.text(0.02, 0.02, FOOT, transform=ax2.transAxes, fontsize=8, color="0.85")

    fig.suptitle("TEC horizontal gradient / EPB boundary (schematic)", fontsize=12, y=1.02)
    _save(fig, "fig-tec-gradient.png")


def main() -> None:
    print(f"OUT = {OUT}")
    fig_ipp_pierce_point()
    fig_chapman_layer()
    fig_dst_kp_timeline()
    fig_dualfreq_tec()
    fig_mapping_function()
    fig_phase_scint()
    fig_tec_gradient()
    print("done.")


if __name__ == "__main__":
    main()
