#!/usr/bin/env python3
"""Original CC0 teaching schematics: fountain EIA, storm phases, S4 scintillation."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Ellipse, FancyBboxPatch
import matplotlib.patches as mpatches

OUT = Path(__file__).resolve().parents[1] / "docs" / "tutorials" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "axes.unicode_minus": False,
})

# Colorblind-friendly palette (match storm residual fig)
BLUE = "#2874a6"
GREEN = "#2ca25f"
RED = "#b22222"
ORANGE = "#e67e22"
LIGHT_BLUE = "#5dade2"
LIGHT_RED = "#e74c3c"
GREY = "#7f8c8d"


def fig_fountain_eia():
    """Side-view latitude–height cartoon: E×B uplift → fountain → EIA twin crests."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    lat = np.linspace(-40, 40, 500)

    # Background ionosphere band (F-region)
    ax.axhspan(200, 500, color="#d6eaf8", alpha=0.55, zorder=0)
    ax.axhspan(90, 200, color="#eaf2f8", alpha=0.4, zorder=0)

    # Magnetic equator
    ax.axvline(0, color=GREY, ls=":", lw=1.2, zorder=1)

    # Equatorial plasma uplift path (fountain core) — schematic density blobs
    # Rising plume near equator
    for h0, w, alpha in [(280, 4.5, 0.55), (340, 5.5, 0.45), (400, 7.0, 0.35)]:
        ell = Ellipse((0, h0), width=w, height=55, facecolor=LIGHT_BLUE,
                      edgecolor=BLUE, lw=1.5, alpha=alpha, zorder=2)
        ax.add_patch(ell)

    # Twin crests at ~±15–18° (higher Ne blobs lower than apex)
    for sign in (-1, 1):
        crest = Ellipse((sign * 17, 300), width=14, height=90,
                        facecolor="#f5b041", edgecolor=ORANGE, lw=1.8,
                        alpha=0.55, zorder=3)
        ax.add_patch(crest)

    # E×B upward arrows near equator (lower F)
    for dx in (-3.5, 0, 3.5):
        ax.annotate(
            "", xy=(dx, 360), xytext=(dx, 220),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.0,
                            mutation_scale=14),
            zorder=5,
        )
    ax.text(0, 195, r"$E\times B$ uplift", ha="center", va="top",
            color=RED, fontsize=10, fontweight="bold")

    # Fountain divergence arrows (plasma flows poleward / downward)
    ax.annotate(
        "", xy=(-16, 310), xytext=(-5, 400),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0,
                        mutation_scale=14, connectionstyle="arc3,rad=0.25"),
        zorder=5,
    )
    ax.annotate(
        "", xy=(16, 310), xytext=(5, 400),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0,
                        mutation_scale=14, connectionstyle="arc3,rad=-0.25"),
        zorder=5,
    )
    ax.text(0, 455, "plasma fountain", ha="center", va="bottom",
            color=BLUE, fontsize=10)

    # Crest labels
    ax.text(-17, 300, "EIA\ncrest", ha="center", va="center",
            fontsize=9, color="#7d3c00", fontweight="bold", zorder=6)
    ax.text(17, 300, "EIA\ncrest", ha="center", va="center",
            fontsize=9, color="#7d3c00", fontweight="bold", zorder=6)

    # Ground / height cues
    ax.axhline(0, color="#27ae60", lw=2.5, solid_capstyle="butt")
    ax.text(0, 12, "ground / magnetic equator", ha="center", va="bottom",
            color="#1e8449", fontsize=9)

    ax.set_xlim(-40, 40)
    ax.set_ylim(0, 520)
    ax.set_xlabel("Magnetic latitude (°)")
    ax.set_ylabel("Altitude (km)")
    ax.set_title("Equatorial fountain → EIA twin crests (schematic)")
    ax.grid(True, alpha=0.25)
    ax.text(0.01, 0.02, "schematic · CC0", transform=ax.transAxes,
            fontsize=8, color=GREY, va="bottom")

    fig.tight_layout()
    path = OUT / "fig-fountain-eia.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def fig_storm_phases_tec():
    """Dual time-series: positive-phase enhancement vs negative-phase depletion."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True)
    fig.patch.set_facecolor("white")

    t = np.linspace(0, 48, 481)
    # Quiet diurnal baseline (two days)
    quiet = 20 + 8 * np.sin(2 * np.pi * (t - 6) / 24)

    # Storm onset ~ hour 12
    onset = 12.0
    # Positive phase: enhancement for ~12 h after onset
    pos_env = np.where(
        t >= onset,
        7.5 * np.exp(-((t - (onset + 6)) / 5.5) ** 2),
        0.0,
    )
    # Negative phase: depletion starting later, lasting longer
    neg_env = np.where(
        t >= onset + 10,
        -9.0 * (1 - np.exp(-(t - (onset + 10)) / 4.0)) * np.exp(-(t - (onset + 18)) / 14.0),
        0.0,
    )
    # Combine into one storm day curve for context strip, but show phases in bands
    storm = quiet + pos_env + neg_env

    # --- Panel 1: Positive phase ---
    ax1.set_facecolor("white")
    ax1.plot(t, quiet, color=GREEN, lw=2.0, label="Quiet baseline")
    storm_pos = quiet + pos_env
    ax1.plot(t, storm_pos, color=RED, lw=2.2, label="Storm (positive phase)")
    ax1.fill_between(t, quiet, storm_pos, where=storm_pos >= quiet,
                     color=LIGHT_RED, alpha=0.35, label="Enhancement")
    ax1.axvline(onset, color=ORANGE, ls=":", lw=1.5)
    ax1.text(onset + 0.4, 30.5, "onset", color=ORANGE, fontsize=9, va="top")
    ax1.set_ylabel("VTEC (schematic TECU)")
    ax1.set_title("Storm phases in TEC (schematic)")
    ax1.set_ylim(8, 36)
    ax1.legend(loc="upper right", fontsize=9, ncol=3, framealpha=0.95)
    ax1.grid(True, alpha=0.25)
    ax1.text(0.01, 0.92, "Positive phase", transform=ax1.transAxes,
             fontsize=10, color=RED, fontweight="bold", va="top")

    # --- Panel 2: Negative phase ---
    ax2.set_facecolor("white")
    ax2.plot(t, quiet, color=GREEN, lw=2.0, label="Quiet baseline")
    storm_neg = quiet + neg_env
    # Also show full storm for continuity in lower panel
    ax2.plot(t, storm, color=RED, lw=2.2, label="Storm day")
    ax2.fill_between(t, quiet, storm_neg, where=storm_neg <= quiet,
                     color=LIGHT_BLUE, alpha=0.4, label="Depletion")
    ax2.axvline(onset, color=ORANGE, ls=":", lw=1.5)
    ax2.set_xlabel("Time (hours)")
    ax2.set_ylabel("VTEC (schematic TECU)")
    ax2.set_ylim(8, 36)
    ax2.legend(loc="upper right", fontsize=9, ncol=3, framealpha=0.95)
    ax2.grid(True, alpha=0.25)
    ax2.text(0.01, 0.92, "Negative phase", transform=ax2.transAxes,
             fontsize=10, color=BLUE, fontweight="bold", va="top")
    ax2.text(0.01, 0.02, "schematic · CC0", transform=ax2.transAxes,
             fontsize=8, color=GREY, va="bottom")

    fig.tight_layout()
    path = OUT / "fig-storm-phases-tec.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def fig_s4_scint():
    """Multi-frequency S4 index: synthetic L1/L2/L5 traces vs time."""
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    rng = np.random.default_rng(42)
    t = np.linspace(0, 60, 601)  # minutes

    # Quiet baseline then scintillation burst ~20–40 min
    envelope = 0.08 + 0.55 * np.exp(-((t - 30) / 7.5) ** 2)
    # Higher frequency → generally lower S4 for same irregularities (diffraction)
    # L1 ~1575 MHz, L2 ~1227, L5 ~1176 → L5/L2 stronger than L1
    noise = rng.standard_normal(len(t))
    # smooth noise a bit
    kernel = np.ones(7) / 7
    noise = np.convolve(noise, kernel, mode="same")

    s4_l1 = np.clip(envelope * 0.55 + 0.04 * np.abs(noise), 0, 1.2)
    s4_l2 = np.clip(envelope * 0.85 + 0.05 * np.abs(noise * 1.1), 0, 1.2)
    s4_l5 = np.clip(envelope * 1.00 + 0.055 * np.abs(noise * 1.15), 0, 1.2)

    ax.plot(t, s4_l1, color=GREEN, lw=2.0, label="L1 (1575 MHz)")
    ax.plot(t, s4_l2, color=BLUE, lw=2.0, label="L2 (1227 MHz)")
    ax.plot(t, s4_l5, color=RED, lw=2.0, label="L5 (1176 MHz)")

    # Mild fill under L5 burst to highlight event
    ax.fill_between(t, 0, s4_l5, where=(t > 18) & (t < 42),
                    color=LIGHT_RED, alpha=0.12, zorder=0)

    ax.axhline(0.3, color=GREY, ls="--", lw=1.0, alpha=0.8)
    ax.text(1.0, 0.32, "moderate", color=GREY, fontsize=8, va="bottom")
    ax.axhline(0.6, color=GREY, ls="--", lw=1.0, alpha=0.8)
    ax.text(1.0, 0.62, "strong", color=GREY, fontsize=8, va="bottom")

    ax.set_xlim(0, 60)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel(r"$S_4$ index (schematic)")
    ax.set_title("Multi-frequency scintillation index $S_4$ (schematic)")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.25)
    ax.text(0.01, 0.02, "schematic · CC0", transform=ax.transAxes,
            fontsize=8, color=GREY, va="bottom")

    fig.tight_layout()
    path = OUT / "fig-s4-scint.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def main():
    paths = [fig_fountain_eia(), fig_storm_phases_tec(), fig_s4_scint()]
    for p in paths:
        print(f"wrote {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
