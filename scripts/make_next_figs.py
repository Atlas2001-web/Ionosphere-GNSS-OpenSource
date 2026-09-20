#!/usr/bin/env python3
"""Original CC0 teaching schematics: auroral oval, eclipse TEC hole, penetrating E-field."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Circle, Wedge
from matplotlib.colors import LinearSegmentedColormap

OUT = Path(__file__).resolve().parents[1] / "docs" / "tutorials" / "images"
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
PURPLE = "#8e44ad"
GREY = "#7f8c8d"
GOLD = "#f4d03f"


def fig_aurora_oval():
    """Polar magnetic-latitude / local-time view: auroral oval, nightside thicker."""
    fig, ax = plt.subplots(figsize=(7.2, 7.0), subplot_kw=dict(projection="polar"))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#0b1a2b")

    # θ = 0 at midnight (nightside bottom-ish); increase clockwise toward dawn
    # Use standard: 0 at top = noon (dayside), clockwise = local time
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Colatitude from magnetic pole: 0 at pole, outer = lower latitude
    # Oval centered ~67–72° MLAT → colat ~18–23°; nightside wider (to ~60°)
    theta = np.linspace(0, 2 * np.pi, 721)

    # Dayside (noon θ=0): thinner; nightside (midnight θ=π): thicker / equatorward
    # cos(θ): noon=+1, midnight=-1
    # noon band ~73–68 MLAT; midnight ~71–58 MLAT
    mlat_inner = 72 + 1.0 * np.cos(theta)
    mlat_outer = 63 + 5.0 * np.cos(theta)

    colat_inner = 90.0 - mlat_inner
    colat_outer = 90.0 - mlat_outer

    # Soft glow fill between edges
    for frac in np.linspace(0.15, 1.0, 8):
        ci = colat_inner + (colat_outer - colat_inner) * (0.5 - 0.5 * frac)
        co = colat_inner + (colat_outer - colat_inner) * (0.5 + 0.5 * frac)
        # Use fill between via polygon strips
        ax.fill_between(
            theta, ci, co,
            color="#39ff14" if frac > 0.55 else "#7dcea0",
            alpha=0.08 + 0.07 * frac,
            zorder=2,
        )

    # Bright core ribbon
    colat_core = 0.55 * colat_inner + 0.45 * colat_outer
    ax.plot(theta, colat_core, color="#adff2f", lw=2.2, alpha=0.95, zorder=4)
    ax.plot(theta, colat_inner, color="#58d68d", lw=1.0, alpha=0.7, zorder=3)
    ax.plot(theta, colat_outer, color="#58d68d", lw=1.0, alpha=0.7, zorder=3)

    # Magnetic pole marker
    ax.plot(0, 0, "o", color="white", ms=7, zorder=6)
    ax.text(0.15, 2.5, "mag.\npole", color="white", fontsize=8, ha="left", va="bottom")

    # LT labels
    ax.set_xticks(np.deg2rad([0, 90, 180, 270]))
    ax.set_xticklabels(["12 LT\n(dayside)", "18 LT", "00 LT\n(nightside)", "06 LT"],
                       fontsize=9, color="0.25")
    ax.set_ylim(0, 35)
    ax.set_yticks([10, 20, 30])
    ax.set_yticklabels(["80°", "70°", "60° MLAT"], fontsize=8, color="0.35")
    ax.tick_params(colors="0.35")
    ax.grid(True, color="0.55", alpha=0.35, lw=0.6)

    # Annotate nightside thicker
    ax.annotate(
        "thicker\nnightside",
        xy=(np.pi, 28),
        xytext=(np.pi * 0.72, 33),
        color="#f7dc6f", fontsize=9, ha="center",
        arrowprops=dict(arrowstyle="-|>", color="#f7dc6f", lw=1.2),
        zorder=7,
    )

    ax.set_title("Auroral oval (schematic)", pad=18, color="0.15")
    fig.text(0.02, 0.02, "schematic · CC0", fontsize=8, color=GREY)

    path = OUT / "fig-aurora-oval.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_eclipse_tec_hole():
    """Lat–lon synthetic VTEC map with moon-shadow depletion (TEC hole)."""
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    lon = np.linspace(-60, 60, 241)
    lat = np.linspace(-40, 40, 161)
    LON, LAT = np.meshgrid(lon, lat)

    # Background day-side-ish VTEC with mild EIA
    vtec = (
        22
        + 10 * np.exp(-0.5 * ((LAT - 16) / 9) ** 2)
        + 10 * np.exp(-0.5 * ((LAT + 16) / 9) ** 2)
        - 4 * np.exp(-0.5 * (LAT / 6) ** 2)
        + 4 * np.cos(np.deg2rad(LON / 2))
    )

    # Eclipse path (diagonal band) and TEC hole depletion
    # Path centerline: lat ≈ 0.35 * lon
    path_lat = 0.28 * LON
    dist = LAT - path_lat
    along = LON  # progress along path
    # Elongated Gaussian hole along path
    hole = 14 * np.exp(
        -0.5 * (dist / 5.5) ** 2
        - 0.5 * ((along - 5) / 22) ** 2
    )
    vtec = vtec - hole

    cmap = LinearSegmentedColormap.from_list(
        "tec",
        ["#1a5276", "#2874a6", "#5dade2", "#a9dfbf", "#f9e79f", "#f5b041", "#e74c3c"],
    )
    pcm = ax.pcolormesh(LON, LAT, vtec, shading="auto", cmap=cmap, vmin=8, vmax=38)

    # Mark eclipse path and umbra tip
    path_lons = np.linspace(-35, 45, 80)
    path_lats = 0.28 * path_lons
    ax.plot(path_lons, path_lats, color="0.2", lw=1.2, ls="--", alpha=0.7,
            label="eclipse path")
    # Moon shadow / umbra marker
    ax.add_patch(Circle((5, 0.28 * 5), 4.5, facecolor="0.15", edgecolor="white",
                        lw=1.2, alpha=0.55, zorder=5))
    ax.annotate(
        "TEC hole",
        xy=(5, 1.4), xytext=(22, -22),
        fontsize=10, color="#1a5276", fontweight="bold",
        arrowprops=dict(arrowstyle="-|>", color="#1a5276", lw=1.5),
        zorder=6,
    )

    cbar = fig.colorbar(pcm, ax=ax, pad=0.02, fraction=0.046)
    cbar.set_label("VTEC (schematic TECU)")

    ax.set_xlim(-60, 60)
    ax.set_ylim(-40, 40)
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Eclipse TEC hole (schematic)")
    ax.grid(True, alpha=0.25, color="white", lw=0.6)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.text(0.01, 0.02, "schematic · CC0", transform=ax.transAxes,
            fontsize=8, color=GREY, va="bottom")

    fig.tight_layout()
    path = OUT / "fig-eclipse-tec-hole.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def fig_penetrating_efield():
    """PPEF idea: interplanetary E penetrates to equatorial ionosphere (arrows + uplift)."""
    fig, axes = plt.subplots(
        1, 2, figsize=(10.0, 4.6),
        gridspec_kw=dict(width_ratios=[1.15, 1.0], wspace=0.28),
    )
    fig.patch.set_facecolor("white")

    # --- Left: latitude schematic with penetrating E arrows ---
    ax = axes[0]
    ax.set_facecolor("white")

    # Earth / ionosphere band
    ax.axhspan(0, 1.0, color="#d5f5e3", alpha=0.5, zorder=0)
    ax.axhspan(1.0, 3.2, color="#d6eaf8", alpha=0.55, zorder=0)  # ionosphere
    ax.axhline(1.0, color=GREEN, lw=1.5)
    ax.text(0, 0.35, "Earth", ha="center", color="#1e8449", fontsize=9)

    # High-latitude / polar caps
    for sign, label in [(-1, "N polar"), (1, "S polar")]:
        ax.add_patch(Ellipse((sign * 7.5, 2.4), width=3.2, height=1.4,
                             facecolor="#aed6f1", edgecolor=BLUE, lw=1.5,
                             alpha=0.7, zorder=2))
        ax.text(sign * 7.5, 2.4, label, ha="center", va="center",
                fontsize=8, color=BLUE, fontweight="bold")

    # Equatorial F-region blob
    ax.add_patch(Ellipse((0, 2.0), width=3.5, height=1.1,
                         facecolor="#f5b041", edgecolor=ORANGE, lw=1.6,
                         alpha=0.55, zorder=2))
    ax.text(0, 2.0, "equatorial\nF region", ha="center", va="center",
            fontsize=8, color="#7d3c00", fontweight="bold")

    # IMF / magnetosphere E hint at top
    ax.text(0, 3.55, r"IMF / magnetospheric $E$ (prompt)",
            ha="center", va="bottom", color=PURPLE, fontsize=9, fontweight="bold")

    # Penetrating E arrows from both polar regions toward equator
    for x0, rad in [(-7.2, 0.2), (7.2, -0.2)]:
        ax.annotate(
            "",
            xy=(np.sign(x0) * 1.8, 2.15),
            xytext=(x0, 2.55),
            arrowprops=dict(
                arrowstyle="-|>", color=PURPLE, lw=2.2, mutation_scale=14,
                connectionstyle=f"arc3,rad={rad}",
            ),
            zorder=5,
        )

    # Vertical E×B uplift at equator (consequence)
    ax.annotate(
        "", xy=(0, 2.85), xytext=(0, 1.45),
        arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.0, mutation_scale=13),
        zorder=5,
    )
    ax.text(1.15, 2.15, r"$E\times B$" + "\nuplift", color=RED, fontsize=8,
            va="center", ha="left")

    ax.text(0, 1.15, "PPEF → equator", ha="center", fontsize=9,
            color=PURPLE, fontweight="bold")

    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 3.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Penetrating E → equator")
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.01, 0.02, "schematic · CC0", transform=ax.transAxes,
            fontsize=8, color=GREY, va="bottom")

    # --- Right: sudden equatorial uplift proxy time series ---
    ax2 = axes[1]
    ax2.set_facecolor("white")
    t = np.linspace(0, 6, 601)  # hours
    # Quiet baseline with mild diurnal
    base = 18 + 1.2 * np.sin(2 * np.pi * t / 24)
    # Sudden PPEF-driven uplift / TEC jump at t=2 h
    onset = 2.0
    jump = np.where(
        t >= onset,
        9.0 * (1 - np.exp(-(t - onset) / 0.18)) * np.exp(-(t - onset) / 2.2),
        0.0,
    )
    eq = base + jump

    ax2.plot(t, base, color=GREEN, lw=1.8, ls="--", label="Quiet")
    ax2.plot(t, eq, color=RED, lw=2.2, label="PPEF response")
    ax2.fill_between(t, base, eq, where=eq >= base, color=LIGHT_RED, alpha=0.3)
    ax2.axvline(onset, color=ORANGE, ls=":", lw=1.5)
    ax2.text(onset + 0.08, 28.5, "prompt\npenetration", color=ORANGE,
             fontsize=8, va="top")

    ax2.set_xlim(0, 6)
    ax2.set_ylim(14, 32)
    ax2.set_xlabel("Time (hours)")
    ax2.set_ylabel("Equatorial VTEC proxy (TECU)")
    ax2.set_title("Sudden equatorial uplift")
    ax2.legend(loc="upper right", fontsize=9)
    ax2.grid(True, alpha=0.25)

    fig.suptitle("Penetrating electric field (schematic)", fontsize=13, y=0.98)

    path = OUT / "fig-penetrating-efield.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def main():
    paths = [fig_aurora_oval(), fig_eclipse_tec_hole(), fig_penetrating_efield()]
    for p in paths:
        print(f"wrote {p} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
