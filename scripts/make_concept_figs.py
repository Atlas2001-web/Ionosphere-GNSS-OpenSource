#!/usr/bin/env python3
"""Concept schematics for tutorials 01–07, 09 (通俗易懂).

Synthetic CC0 figures (matplotlib). No flowcharts. Cartopy only if map.
Usage (repo root):
  .venv/bin/python scripts/make_concept_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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
        "grid.alpha": 0.28,
        "grid.linewidth": 0.55,
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
TEAL = "#148f77"
GOLD = "#d4ac0d"


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def fig_plasma_freq_vs_ne() -> None:
    """f_p vs N_e (sqrt law) with GNSS band reminder."""
    ne = np.logspace(10, 13, 400)  # m^-3
    # f_p (Hz) ≈ 8.98 * sqrt(Ne_cm-3) * 1e6 ≈ 8.98e-3 * sqrt(Ne_m-3) * 1e6
    # Standard: f_p [Hz] = (1/(2π)) * sqrt(Ne e^2 / (ε0 me)) ≈ 8.98 * sqrt(Ne [m^-3])
    fp_mhz = 8.98e-6 * np.sqrt(ne)  # MHz when Ne in m^-3: 8.98*sqrt(Ne)/1e6
    # Check: Ne=1e12 → sqrt=1e6 → fp=8.98 MHz. Yes with factor 8.98e-6 * sqrt(Ne).

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(ne, fp_mhz, color=BLUE, lw=2.4, label=r"$f_p \propto \sqrt{N_e}$")
    # mark points
    for Ne, label in [(1e11, r"$10^{11}$"), (1e12, r"$10^{12}$"), (4e12, r"$4\times10^{12}$")]:
        fp = 8.98e-6 * np.sqrt(Ne)
        ax.plot(Ne, fp, "o", color=RED, ms=7, zorder=5)
        ax.annotate(
            f"{label}\n→ {fp:.1f} MHz",
            xy=(Ne, fp),
            xytext=(10, 12),
            textcoords="offset points",
            fontsize=8.5,
            color=RED,
        )
    ax.axhspan(1200, 1600, color=GREEN, alpha=0.12, label="GNSS L-band (~1.2–1.6 GHz)")
    ax.text(2e10, 1400, "GNSS carriers ≫ $f_p$\n→ wave passes; delay $\\propto N_e/f^2$",
            fontsize=8.5, color="#1e8449", va="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e10, 1e13)
    ax.set_ylim(0.5, 2e3)
    ax.set_xlabel(r"electron density $N_e$ (m$^{-3}$)")
    ax.set_ylabel(r"plasma frequency $f_p$ (MHz)")
    ax.set_title(r"Plasma frequency vs $N_e$ (cold plasma)", fontsize=12)
    ax.legend(loc="lower right", framealpha=0.92)
    ax.text(0.99, 0.02, FOOT, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.5, color=GREY)
    _save(fig, "fig-plasma-freq-vs-ne.png")


def fig_phase_group_vs_freq() -> None:
    """Phase advance vs group delay vs frequency (same STEC)."""
    stec_tecu = 20.0
    stec = stec_tecu * 1e16  # m^-2
    f = np.linspace(1.0e9, 1.8e9, 400)
    I = 40.3 * stec / f**2  # meters of group delay
    # phase advance magnitude same to first order
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.plot(f / 1e9, I, color=ORANGE, lw=2.5, label=r"group delay $+I$ (code / pseudorange)")
    ax.plot(f / 1e9, -I, color=BLUE, lw=2.5, ls="--",
            label=r"phase advance $-I$ (carrier)")
    ax.axhline(0, color=GREY, lw=0.8)
    for name, ff, c in [("L5", 1.17645, TEAL), ("L2", 1.22760, PURPLE), ("L1", 1.57542, GREEN)]:
        Ii = 40.3 * stec / (ff * 1e9) ** 2
        ax.plot([ff, ff], [-Ii, Ii], color=c, lw=1.2, alpha=0.7)
        ax.plot(ff, Ii, "s", color=c, ms=6)
        ax.plot(ff, -Ii, "o", color=c, ms=6)
        ax.text(ff, Ii + 0.35, name, ha="center", fontsize=8, color=c, fontweight="bold")
    ax.set_xlabel("carrier frequency $f$ (GHz)")
    ax.set_ylabel("equivalent path (m)")
    ax.set_title(rf"Phase vs group: same STEC={stec_tecu:.0f} TECU, opposite signs", fontsize=12)
    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.92)
    ax.text(0.02, 0.98,
            "Look: mirrors about zero · Misread: treating phase delay like code delay",
            transform=ax.transAxes, va="top", fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f8f9f9", ec="#d5d8dc"))
    ax.text(0.99, 0.02, FOOT, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.5, color=GREY)
    _save(fig, "fig-phase-group-vs-freq.png")


def fig_shell_ipp_path() -> None:
    """STEC slant path vs VTEC thin shell + IPP (geometry cartoon)."""
    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.8, 7.2)
    ax.axis("off")
    ax.set_title("STEC path vs VTEC shell + IPP", fontsize=12, pad=8)

    # Earth surface
    ax.plot([0.5, 9.5], [0.3, 0.3], color=GREEN, lw=2.5)
    ax.fill_between([0.5, 9.5], -0.5, 0.3, color="#d5f5e3", alpha=0.5)
    ax.text(5, -0.35, "ground", ha="center", color="#1e8449", fontsize=9)

    # Rx
    ax.plot(2.2, 0.45, "o", color="#1e8449", ms=11, zorder=5)
    ax.text(2.2, 0.7, "Rx", ha="center", fontweight="bold", color="#1e8449")

    # thin shell
    ax.plot([0.8, 10.2], [3.8, 3.8], color=BLUE, lw=2.2, ls="--")
    ax.fill_between([0.8, 10.2], 3.55, 4.05, color="#d6eaf8", alpha=0.55)
    ax.text(10.0, 4.2, "thin shell ~450 km", ha="right", color=BLUE, fontsize=9)

    # satellite
    ax.plot(9.2, 6.5, "^", color=ORANGE, ms=14, zorder=5)
    ax.text(9.2, 6.85, "GNSS sat", ha="center", color=ORANGE, fontsize=9, fontweight="bold")

    # slant ray
    ax.plot([2.2, 9.2], [0.45, 6.5], color=RED, lw=2.0, zorder=4)
    # IPP
    # line: (2.2,0.45) to (9.2,6.5); y=3.8 → t=(3.8-0.45)/(6.5-0.45)
    t = (3.8 - 0.45) / (6.5 - 0.45)
    ippx = 2.2 + t * (9.2 - 2.2)
    ax.plot(ippx, 3.8, "o", color=PURPLE, ms=12, zorder=6)
    ax.text(ippx + 0.25, 3.8, "IPP", color=PURPLE, fontsize=10, fontweight="bold", va="center")

    # VTEC vertical dashed
    ax.plot([ippx, ippx], [0.3, 3.8], color=PURPLE, lw=1.6, ls=":")
    ax.annotate("", xy=(ippx, 3.7), xytext=(ippx, 0.5),
                arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.4))
    ax.text(ippx - 0.15, 2.0, "VTEC", color=PURPLE, fontsize=9, ha="right", rotation=90)

    # STEC label along path
    mid = ((2.2 + 9.2) / 2 - 0.6, (0.45 + 6.5) / 2 + 0.35)
    ax.text(mid[0], mid[1], "STEC = ∫Ne ds\n(slant pipe)", color=RED, fontsize=9,
            rotation=38, fontweight="bold")

    ax.text(0.6, 6.5, r"STEC ≈ M(E) · VTEC", fontsize=11, color="#1a5276",
            bbox=dict(boxstyle="round,pad=0.35", fc="#eaf2f8", ec=BLUE))
    ax.text(0.6, 5.5, "Look: IPP pins slant fog onto map cell\nMisread: STEC = VTEC without mapping",
            fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#fef9e7", ec="#f9e79f"))
    ax.text(10.8, -0.6, FOOT, ha="right", fontsize=7.5, color=GREY)
    _save(fig, "fig-shell-ipp-path.png")


def fig_mapping_me_curve() -> None:
    """Mapping function M(E) vs elevation."""
    # M(E) = 1 / sqrt(1 - (Re/(Re+H) cos E)^2)
    Re = 6371.0
    H = 450.0
    E_deg = np.linspace(5, 90, 200)
    E = np.deg2rad(E_deg)
    ratio = Re / (Re + H)
    M = 1.0 / np.sqrt(1.0 - (ratio * np.cos(E)) ** 2)

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.plot(E_deg, M, color=BLUE, lw=2.6, label=rf"$H={H:.0f}$ km thin-shell $M(E)$")
    for e in (10, 20, 30, 60, 90):
        Ee = np.deg2rad(e)
        Mm = 1.0 / np.sqrt(1.0 - (ratio * np.cos(Ee)) ** 2)
        ax.plot(e, Mm, "o", color=RED, ms=6)
        ax.annotate(f"{Mm:.2f}", xy=(e, Mm), xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=8, color=RED)
    ax.axvline(15, color=ORANGE, ls="--", lw=1.2, alpha=0.8)
    ax.text(15.5, 2.6, "low-elev\namplifies", color=ORANGE, fontsize=8.5)
    ax.set_xlabel("elevation $E$ (deg)")
    ax.set_ylabel(r"mapping $M(E)$  (STEC ≈ M · VTEC)")
    ax.set_title("Thin-shell mapping function $M(E)$", fontsize=12)
    ax.set_xlim(0, 95)
    ax.set_ylim(0.9, 3.2)
    ax.legend(loc="upper right")
    ax.text(0.02, 0.98,
            "Look: steep rise below ~20° · Misread: treating M≈1 at all elevations",
            transform=ax.transAxes, va="top", fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f8f9f9", ec="#d5d8dc"))
    ax.text(0.99, 0.02, FOOT, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.5, color=GREY)
    _save(fig, "fig-mapping-me-curve.png")


def fig_dcb_parallel_shift() -> None:
    """DCB as parallel offset cartoon on STEC time series."""
    t = np.linspace(0, 24, 300)
    true = 8 + 12 * np.exp(-0.5 * ((t - 14) / 3.2) ** 2)  # daytime hump
    bias = 5.0  # TECU
    biased = true + bias

    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(t, true, color=BLUE, lw=2.4, label="truth-like STEC shape")
    ax.plot(t, biased, color=RED, lw=2.4, ls="--", label="raw GF STEC (+DCB offset)")
    ax.fill_between(t, true, biased, color=RED, alpha=0.12)
    # arrow at midday
    ax.annotate(
        "",
        xy=(14, biased[np.argmin(np.abs(t - 14))]),
        xytext=(14, true[np.argmin(np.abs(t - 14))]),
        arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.8),
    )
    ax.text(14.3, 18.5, "+DCB\n(~const TECU)", color=PURPLE, fontsize=9, fontweight="bold")
    ax.set_xlabel("local time (h)")
    ax.set_ylabel("STEC (TECU)")
    ax.set_title("DCB bias: parallel shift, shape preserved", fontsize=12)
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_xlim(0, 24)
    ax.text(0.98, 0.05,
            "Look: whole-day parallel · Misread: calling the offset a storm TEC jump",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#fef9e7", ec="#f9e79f"))
    ax.text(0.01, 0.02, FOOT, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=7.5, color=GREY)
    _save(fig, "fig-dcb-parallel-shift.png")


def fig_iono_free_combo() -> None:
    """Ionosphere-free combination intuition (cancel first-order I)."""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.4))

    # Left: two delays
    ax = axes[0]
    freqs = [1.57542, 1.22760]
    labels = ["L1", "L2"]
    I = [1.62, 2.67]  # for 10 TECU-ish
    colors = [GREEN, PURPLE]
    bars = ax.bar(labels, I, color=colors, width=0.55, edgecolor="k", lw=0.6)
    for b, v in zip(bars, I):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.2f} m",
                ha="center", fontsize=9)
    ax.set_ylabel("first-order iono delay $I$ (m)")
    ax.set_title(r"$I \propto 1/f^2$ (same STEC)", fontsize=11)
    ax.set_ylim(0, 3.5)
    ax.text(0.5, 0.92, r"$I_2 / I_1 = (f_1/f_2)^2$", transform=ax.transAxes,
            ha="center", fontsize=9, color="#1a5276",
            bbox=dict(boxstyle="round", fc="#eaf2f8", ec=BLUE))

    # Right: weighted cancel
    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title("IF recipe (positioning)", fontsize=11)
    box = FancyBboxPatch((0.6, 5.5), 8.8, 3.6, boxstyle="round,pad=0.2",
                         fc="#eafaf1", ec=GREEN, lw=1.5)
    ax.add_patch(box)
    ax.text(5, 8.5, r"$P_{\mathrm{IF}} = \alpha_1 P_1 + \alpha_2 P_2$",
            ha="center", fontsize=12, fontweight="bold", color="#145a32")
    ax.text(5, 7.3, r"choose $\alpha$ so $\alpha_1 I_1 + \alpha_2 I_2 = 0$",
            ha="center", fontsize=10, color="#1e8449")
    ax.text(5, 6.2, "geometry stays · first-order fog cancelled",
            ha="center", fontsize=9.5, color=TEAL)

    box2 = FancyBboxPatch((0.6, 0.8), 8.8, 3.8, boxstyle="round,pad=0.2",
                          fc="#fdedec", ec=RED, lw=1.5)
    ax.add_patch(box2)
    ax.text(5, 3.8, "Cost / not magic", ha="center", fontsize=11,
            fontweight="bold", color=RED)
    ax.text(5, 2.7, "• noise amplified\n• higher-order / DCB remain\n• gives better range, NOT a TEC map",
            ha="center", fontsize=9, color="#922b21", va="top")

    fig.suptitle("Ionosphere-free (IF) combination intuition", fontsize=12.5, y=1.02)
    fig.text(0.99, 0.01, FOOT, ha="right", fontsize=7.5, color=GREY)
    fig.text(0.01, 0.01,
             "Look: weights kill I · Misread: IF output as electron-density photo",
             fontsize=8, color=GREY)
    _save(fig, "fig-iono-free-combo.png")


def fig_chapman_ne_h() -> None:
    """Chapman layer Ne(h) profile for teaching."""
    hm = 300.0  # km
    H = 50.0
    Nm = 1.0e12
    h = np.linspace(100, 700, 500)
    z = (h - hm) / H
    # α-Chapman-like
    Ne = Nm * np.exp(0.5 * (1 - z - np.exp(-z)))

    fig, ax = plt.subplots(figsize=(5.6, 5.8))
    ax.plot(Ne / 1e12, h, color=BLUE, lw=2.6)
    ax.axhline(hm, color=ORANGE, ls="--", lw=1.2)
    ax.plot(Nm / 1e12, hm, "o", color=RED, ms=8)
    ax.text(Nm / 1e12 + 0.05, hm + 15, r"$N_m$, $h_m$", color=RED, fontsize=10)
    ax.annotate(
        "",
        xy=(0.15, hm - H),
        xytext=(0.15, hm + H),
        arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.5),
    )
    ax.text(0.18, hm, "scale H", color=GREEN, fontsize=9, va="center")
    ax.set_xlabel(r"$N_e$ ($10^{12}$ m$^{-3}$)")
    ax.set_ylabel("height $h$ (km)")
    ax.set_title("Chapman-type $N_e(h)$ layer", fontsize=12)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(100, 700)
    ax.text(0.98, 0.04,
            "Look: peak + thickness\nMisread: TEC = peak density",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f8f9f9", ec="#d5d8dc"))
    ax.text(0.02, 0.02, FOOT, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=7.5, color=GREY)
    _save(fig, "fig-chapman-ne-h.png")


def fig_s4_sigmaphi_series() -> None:
    """S4 and sigma_phi time-series schematic on same night."""
    rng = np.random.default_rng(7)
    t = np.linspace(18, 28, 600)  # local hours past noon-ish
    # quiet then event
    envelope = 0.05 + 0.55 * np.exp(-0.5 * ((t - 22.5) / 0.9) ** 2)
    s4 = envelope + 0.03 * rng.standard_normal(t.size)
    s4 = np.clip(s4, 0, None)
    # sigma_phi (rad) similar window but slightly offset
    env2 = 0.08 + 0.9 * np.exp(-0.5 * ((t - 22.7) / 0.85) ** 2)
    sphi = env2 + 0.05 * rng.standard_normal(t.size)
    sphi = np.clip(sphi, 0, None)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 5.2), sharex=True)
    ax1.plot(t, s4, color=ORANGE, lw=1.4)
    ax1.fill_between(t, 0, s4, color=ORANGE, alpha=0.2)
    ax1.axhline(0.3, color=GREY, ls=":", lw=1)
    ax1.set_ylabel(r"$S_4$ (amp)")
    ax1.set_title(r"$S_4$ / $\sigma_\varphi$ night schematic (not real data)", fontsize=12)
    ax1.set_ylim(0, 0.9)
    ax1.text(0.02, 0.9, "amplitude scintillation", transform=ax1.transAxes,
             fontsize=8.5, color=ORANGE, fontweight="bold")

    ax2.plot(t, sphi, color=PURPLE, lw=1.4)
    ax2.fill_between(t, 0, sphi, color=PURPLE, alpha=0.18)
    ax2.set_ylabel(r"$\sigma_\varphi$ (rad)")
    ax2.set_xlabel("local time (h)")
    ax2.set_ylim(0, 1.4)
    ax2.text(0.02, 0.9, "phase scintillation", transform=ax2.transAxes,
             fontsize=8.5, color=PURPLE, fontweight="bold")
    ax2.axvspan(21.5, 24.0, color=RED, alpha=0.08)
    ax2.text(22.7, 1.2, "same event window", ha="center", fontsize=8, color=RED)

    fig.text(0.5, 0.01,
             "Look: co-timed peaks · Misread: high TEC night ⇒ must have high S4",
             ha="center", fontsize=8, color=GREY)
    fig.text(0.99, 0.005, FOOT, ha="right", fontsize=7.5, color=GREY)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    _save(fig, "fig-s4-sigmaphi-series.png")


def fig_single_vs_dual_tec() -> None:
    """Single-frequency guess vs dual-frequency measure TEC."""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2))

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Single frequency: one equation", fontsize=11)
    ax.add_patch(FancyBboxPatch((0.5, 5.8), 9, 3.5, boxstyle="round,pad=0.15",
                                fc="#fef5e7", ec=ORANGE, lw=1.4))
    ax.text(5, 8.5, r"$P_1=\rho + \mathrm{clocks} + T + I_1 + \varepsilon$",
            ha="center", fontsize=10, color="#9a7d0a")
    ax.text(5, 7.2, "ρ, clocks, troposphere, iono tangled",
            ha="center", fontsize=9, color=ORANGE)
    ax.text(5, 6.3, "→ borrow model / GIM (guess & correct)",
            ha="center", fontsize=9.5, fontweight="bold", color="#b9770e")

    ax.add_patch(FancyBboxPatch((0.5, 0.6), 9, 4.4, boxstyle="round,pad=0.15",
                                fc="#f5eef8", ec=PURPLE, lw=1.4))
    ax.text(5, 4.2, "You get a range correction,\nnot a measured electron column.",
            ha="center", fontsize=9.5, color=PURPLE, va="top")
    ax.text(5, 2.2, "Ceiling = model skill\n(Klobuchar / NeQuick-G / GIM)",
            ha="center", fontsize=9, color=GREY)

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Dual frequency: dispersion lever", fontsize=11)
    ax.add_patch(FancyBboxPatch((0.5, 5.8), 9, 3.5, boxstyle="round,pad=0.15",
                                fc="#eafaf1", ec=GREEN, lw=1.4))
    ax.text(5, 8.5, r"$P_1-P_2 \propto (I_1-I_2)$ + DCB",
            ha="center", fontsize=11, color="#145a32", fontweight="bold")
    ax.text(5, 7.3, "geometry / tropo / clocks cancel (1st order)",
            ha="center", fontsize=9, color=TEAL)
    ax.text(5, 6.3, r"→ STEC via $\alpha\,(P_1-P_2)$ (measure fog)",
            ha="center", fontsize=9.5, fontweight="bold", color=GREEN)

    ax.add_patch(FancyBboxPatch((0.5, 0.6), 9, 4.4, boxstyle="round,pad=0.15",
                                fc="#eaf2f8", ec=BLUE, lw=1.4))
    ax.text(5, 4.0, "Still need: DCB, leveling,\ncycle-slip care, mapping→VTEC",
            ha="center", fontsize=9.5, color=BLUE, va="top")
    ax.text(5, 2.0, "Misread: dual-freq ⇒ absolute TEC\nwithout bias handling",
            ha="center", fontsize=8.5, color=GREY)

    fig.suptitle("Single-freq correction vs dual-freq TEC measurement", fontsize=12.5, y=1.02)
    fig.text(0.99, 0.01, FOOT, ha="right", fontsize=7.5, color=GREY)
    _save(fig, "fig-single-vs-dual-tec.png")


def fig_residual_three_faces() -> None:
    """Three residual faces: slow drift / gradient tear / scintillation crash."""
    rng = np.random.default_rng(11)
    t = np.linspace(0, 2, 400)  # hours

    fig, axes = plt.subplots(3, 1, figsize=(7.6, 6.4), sharex=True)

    # slow drift
    ax = axes[0]
    drift = 0.15 * t + 0.05 * np.sin(2 * np.pi * t / 0.7) + 0.02 * rng.standard_normal(t.size)
    ax.plot(t, drift, color=BLUE, lw=1.5)
    ax.set_ylabel("pos. resid. (m)")
    ax.set_title("Residual faces in positioning (schematic)", fontsize=12)
    ax.text(0.01, 0.85, "① slow drift — high TEC / weak model / smooth GIM miss",
            transform=ax.transAxes, fontsize=8.5, color=BLUE, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#eaf2f8", ec=BLUE, alpha=0.9))

    # gradient tear
    ax = axes[1]
    base = 0.02 * rng.standard_normal(t.size)
    tear = base.copy()
    tear[150:280] += np.linspace(0, 0.8, 130) + 0.15 * rng.standard_normal(130)
    tear[280:] += 0.35 + 0.2 * np.sin(8 * np.pi * t[280:]) + 0.1 * rng.standard_normal(t.size - 280)
    ax.plot(t, tear, color=ORANGE, lw=1.3)
    ax.set_ylabel("DD resid. (m)")
    ax.text(0.01, 0.85, "② gradient tear — long baseline / EIA / TID sweep",
            transform=ax.transAxes, fontsize=8.5, color=ORANGE, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#fef5e7", ec=ORANGE, alpha=0.9))

    # scintillation crash
    ax = axes[2]
    quiet = 0.03 * rng.standard_normal(t.size)
    crash = quiet.copy()
    idx = (t > 0.9) & (t < 1.4)
    crash[idx] = 0.6 * rng.standard_normal(idx.sum())
    # dropouts as NaN gaps visually via large spikes then flat
    crash[220:235] = np.nan
    crash[250:270] = np.nan
    ax.plot(t, crash, color=RED, lw=1.1)
    ax.axvspan(0.9, 1.4, color=RED, alpha=0.08)
    ax.set_ylabel("phase / gaps")
    ax.set_xlabel("time (h)")
    ax.text(0.01, 0.85, "③ scintillation crash — cycle slips / loss-of-lock / re-converge",
            transform=ax.transAxes, fontsize=8.5, color=RED, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#fdedec", ec=RED, alpha=0.9))

    fig.text(0.5, 0.005,
             "Look: slope ≠ tear ≠ chatter · Misread: blaming every bad residual on 'the ionosphere' the same way",
             ha="center", fontsize=8, color=GREY)
    fig.text(0.99, 0.0, FOOT, ha="right", fontsize=7.5, color=GREY)
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    _save(fig, "fig-residual-three-faces.png")


def fig_fresnel_scale() -> None:
    """Fresnel scale vs irregularity size intuition (no flowchart)."""
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title(r"Fresnel scale: which 'mesh size' shakes L-band?", fontsize=12)

    # screen
    ax.add_patch(FancyBboxPatch((1.5, 3.2), 9, 1.2, boxstyle="round,pad=0.05",
                                fc="#d6eaf8", ec=BLUE, lw=1.5))
    ax.text(6, 4.5, "phase screen / irregularity layer", ha="center", color=BLUE, fontsize=9)

    # three blob sizes
    for x, r, lab, c in [
        (3.0, 0.15, "too small", GREY),
        (6.0, 0.45, r"~$r_F$ (resonant)", RED),
        (9.0, 1.0, "too smooth", GREY),
    ]:
        circ = patches.Circle((x, 3.8), r, facecolor=c, alpha=0.35, edgecolor=c, lw=1.5)
        ax.add_patch(circ)
        ax.text(x, 2.7, lab, ha="center", fontsize=8.5, color=c, fontweight="bold")

    # ground interference
    xx = np.linspace(1.5, 10.5, 400)
    yy = 1.2 + 0.35 * np.sin(2 * np.pi * (xx - 6) / 1.2) * np.exp(-0.5 * ((xx - 6) / 2.2) ** 2)
    ax.plot(xx, yy, color=ORANGE, lw=2)
    ax.fill_between(xx, 0.5, yy, color=ORANGE, alpha=0.15)
    ax.text(6, 0.55, "ground diffraction pattern (amplitude scintillation)",
            ha="center", fontsize=8.5, color=ORANGE)

    ax.text(0.5, 6.3, r"$r_F \sim \sqrt{\lambda\, z_{\mathrm{eff}}}$",
            fontsize=12, color="#1a5276",
            bbox=dict(boxstyle="round,pad=0.35", fc="#eaf2f8", ec=BLUE))
    ax.text(8.2, 6.1, "Look: size match matters\nMisread: any irregularity ⇒ strong S4",
            fontsize=8, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#fef9e7", ec="#f9e79f"))
    ax.text(11.8, 0.15, FOOT, ha="right", fontsize=7.5, color=GREY)
    _save(fig, "fig-fresnel-scale.png")


def fig_instruments_complement() -> None:
    """Ionosonde vs GNSS TEC vs occultation — what each sees."""
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Three cups of water: ionosonde · GNSS TEC · occultation", fontsize=12)

    # shared Ne profile sketch on left
    h = np.linspace(0, 8, 200)
    ne = 2.2 * np.exp(-0.5 * ((h - 4.2) / 1.1) ** 2)
    ax.fill_betweenx(h, 0.3, 0.3 + ne, color=LIGHT_BLUE, alpha=0.5)
    ax.plot(0.3 + ne, h, color=BLUE, lw=2)
    ax.text(1.6, 9.2, r"$N_e(h)$", color=BLUE, fontsize=10, fontweight="bold")
    ax.plot([0.3, 0.3], [0.2, 8.5], color=GREEN, lw=2)
    ax.text(0.15, 0.0, "ground", fontsize=8, color=GREEN)

    # three panels
    panels = [
        (3.2, "Ionosonde", "peak & below\n($f_oF2$, $h_mF2$)\nvirtual height", ORANGE,
         "echo bounce"),
        (6.4, "GNSS TEC", "full column\nRx→sat\nno height tag", GREEN,
         "slant integral"),
        (9.6, "Radio occultation", "side-cut profile\n$N_e(h)$ slice\nocean OK", PURPLE,
         "LEO limb cut"),
    ]
    for x, title, body, c, tag in panels:
        ax.add_patch(FancyBboxPatch((x - 1.35, 1.5), 2.7, 6.2, boxstyle="round,pad=0.15",
                                    fc="white", ec=c, lw=1.8))
        ax.text(x, 7.2, title, ha="center", fontsize=10, fontweight="bold", color=c)
        ax.text(x, 5.2, body, ha="center", va="center", fontsize=8.5, color="#2c3e50")
        ax.text(x, 2.2, tag, ha="center", fontsize=8, color=c, style="italic")

    ax.text(6, 0.45,
            "Look: different integrals · Misread: numbers must match without aligning the cup",
            ha="center", fontsize=8.5, color=GREY,
            bbox=dict(boxstyle="round,pad=0.3", fc="#f8f9f9", ec="#d5d8dc"))
    ax.text(11.8, 0.1, FOOT, ha="right", fontsize=7.5, color=GREY)
    _save(fig, "fig-instruments-complement.png")


def fig_code_phase_signs() -> None:
    """Code +I vs phase -I twin rulers cartoon."""
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Same electron column · opposite first-order signs", fontsize=12)

    # fog bar
    ax.add_patch(FancyBboxPatch((3.5, 2.4), 5, 1.2, boxstyle="round,pad=0.05",
                                fc="#aed6f1", ec=BLUE, lw=1.5))
    ax.text(6, 3.0, "electron column (STEC)", ha="center", fontsize=10,
            color="#1a5276", fontweight="bold", va="center")

    # code arrow longer
    ax.annotate("", xy=(10.5, 4.8), xytext=(1.5, 4.8),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2))
    ax.text(6, 5.25, "CODE / group: path looks LONGER  (+I)",
            ha="center", fontsize=10, color=ORANGE, fontweight="bold")

    # phase arrow shorter sense
    ax.annotate("", xy=(8.8, 1.2), xytext=(3.2, 1.2),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=2.2))
    ax.text(6, 0.55, "PHASE: path looks SHORTER  (−I)  + unknown ambiguity",
            ha="center", fontsize=10, color=PURPLE, fontweight="bold")

    ax.text(0.4, 5.5, "code\nruler", fontsize=8, color=ORANGE)
    ax.text(0.4, 1.05, "phase\nruler", fontsize=8, color=PURPLE)
    ax.text(11.7, 0.15, FOOT, ha="right", fontsize=7.5, color=GREY)
    ax.text(0.3, 0.2, "Misread: averaging code & phase delays as if same sign",
            fontsize=8, color=GREY)
    _save(fig, "fig-code-phase-signs.png")


def main() -> None:
    fig_plasma_freq_vs_ne()
    fig_phase_group_vs_freq()
    fig_shell_ipp_path()
    fig_mapping_me_curve()
    fig_dcb_parallel_shift()
    fig_iono_free_combo()
    fig_chapman_ne_h()
    fig_s4_sigmaphi_series()
    fig_single_vs_dual_tec()
    fig_residual_three_faces()
    fig_fresnel_scale()
    fig_instruments_complement()
    fig_code_phase_signs()
    print("done.")


if __name__ == "__main__":
    main()
