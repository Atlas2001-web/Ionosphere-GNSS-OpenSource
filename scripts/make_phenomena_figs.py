#!/usr/bin/env python3
"""Generate original CC0 teaching schematics for ionospheric phenomena.

Outputs PNGs under docs/tutorials/images/ (high DPI, white/light bg).
Bilingual short labels (中文 / English). Re-run anytime to regenerate:

    python3 scripts/make_phenomena_figs.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials" / "images"
DPI = 180

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Noto Sans CJK SC",
            "Noto Sans CJK JP",
            "DejaVu Sans",
            "Arial",
            "sans-serif",
        ],
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "none",
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#222222",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "text.color": "#222222",
        "grid.color": "#dddddd",
        "grid.linewidth": 0.8,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
    }
)

C_DAY = "#c45c26"
C_NIGHT = "#1f4e78"
C_ACCENT = "#2a9d8f"
C_ALERT = "#d62828"
C_SOFT = "#6c757d"
C_FILL = "#e8f1f8"


def _save(fig: plt.Figure, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")
    return path


def fig_tec_day_night() -> Path:
    lat = np.linspace(-60, 60, 401)

    def eia_like(amp: float, trough: float, crest_lat: float = 15.0) -> np.ndarray:
        base = amp * 0.35 * np.exp(-((lat / 55.0) ** 2))
        crest_n = amp * np.exp(-(((lat - crest_lat) / 9.0) ** 2))
        crest_s = amp * np.exp(-(((lat + crest_lat) / 9.0) ** 2))
        trough_term = trough * np.exp(-((lat / 6.0) ** 2))
        return base + crest_n + crest_s - trough_term + 8.0

    day = eia_like(amp=32.0, trough=12.0)
    night = eia_like(amp=10.0, trough=2.5) + 4.0 * np.exp(-((lat / 40.0) ** 2))

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.plot(lat, day, color=C_DAY, lw=2.6, label="昼 / Day")
    ax.plot(lat, night, color=C_NIGHT, lw=2.6, ls="--", label="夜 / Night")
    ax.axvline(0, color="#aaaaaa", ls=":", lw=1.2)
    ax.fill_between(lat, night, day, where=day >= night, color=C_DAY, alpha=0.08)

    ax.set_xlim(-60, 60)
    ax.set_ylim(0, 55)
    ax.set_xlabel("磁纬 Mag. latitude (°)")
    ax.set_ylabel("相对 VTEC / Relative VTEC (schematic)")
    ax.set_title("日夜 TEC 随纬度示意  ·  Day vs Night TEC vs Latitude")
    ax.grid(True, alpha=0.55)
    ax.legend(loc="upper right", frameon=True, fancybox=False, edgecolor="#cccccc")
    ax.annotate(
        "赤道槽\nequator trough",
        xy=(0, float(day[np.argmin(np.abs(lat))])),
        xytext=(8, 18),
        fontsize=8.5,
        color=C_SOFT,
        arrowprops=dict(arrowstyle="->", color=C_SOFT, lw=1.0),
    )
    ax.text(0.02, 0.04, "示意 / schematic · CC0", transform=ax.transAxes, fontsize=7.5, color=C_SOFT)
    fig.tight_layout()
    return _save(fig, "fig-tec-day-night.png")


def fig_scintillation_bubbles() -> Path:
    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        "赤道等离子体泡与闪烁示意  ·  Equatorial Plasma Bubbles / Scintillation",
        pad=12,
    )

    ground = FancyBboxPatch(
        (0.3, 0.25),
        9.4,
        0.55,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#d9ead3",
        edgecolor="#6aa84f",
        lw=1.2,
    )
    ax.add_patch(ground)
    ax.text(5.0, 0.52, "地面接收机 GNSS Rx  ·  Ground receivers", ha="center", va="center", fontsize=9)

    slab = FancyBboxPatch(
        (0.4, 3.6),
        9.2,
        1.55,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="#cfe2f3",
        edgecolor="#3d85c6",
        lw=1.3,
        alpha=0.85,
    )
    ax.add_patch(slab)
    ax.text(1.55, 5.0, "F 层 / F-region", fontsize=9, color=C_NIGHT, weight="bold")

    bubble_centers = [(3.0, 4.35), (5.1, 4.55), (7.2, 4.25)]
    for cx, cy in bubble_centers:
        e = Ellipse(
            (cx, cy),
            width=1.05,
            height=1.65,
            facecolor="#fff9e6",
            edgecolor="#e69138",
            lw=1.6,
            ls="--",
            alpha=0.95,
        )
        ax.add_patch(e)
        ax.text(cx, cy, "泡\nEPB", ha="center", va="center", fontsize=8, color="#b45f06")

    ax.plot([5.0, 5.0], [0.9, 3.55], color="#aaaaaa", ls=":", lw=1.2)
    ax.text(5.05, 2.3, "磁赤道\nmag. eq.", fontsize=7.5, color=C_SOFT, ha="left")

    sats = [(2.2, 5.85), (5.0, 5.95), (7.8, 5.85)]
    rxs = [(2.4, 0.8), (5.0, 0.8), (7.6, 0.8)]
    for (sx, sy), (rx, ry) in zip(sats, rxs):
        ax.plot(sx, sy, marker="^", markersize=11, color="#674ea7", zorder=5)
        t = np.linspace(0, 1, 80)
        x = sx + (rx - sx) * t
        y = sy + (ry - sy) * t
        wobble = 0.12 * np.sin(18 * np.pi * t) * np.exp(-((t - 0.45) ** 2) / 0.02)
        ax.plot(x + wobble, y, color=C_ALERT, lw=1.35, alpha=0.85)

    ax.text(0.55, 5.85, "GNSS 卫星", fontsize=8, color="#674ea7")
    ax.text(8.55, 5.85, "satellites", fontsize=8, color="#674ea7")

    note = (
        "低密度等离子体泡切断射线 → 相位/幅度闪烁\n"
        "Depleted bubbles along ray path → S4 / σφ scintillation"
    )
    ax.text(
        5.0,
        1.55,
        note,
        ha="center",
        va="center",
        fontsize=8.5,
        color="#333333",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fff3cd", edgecolor="#f0c36d", lw=1.0),
    )
    ax.text(0.35, 0.05, "示意 / schematic · CC0", fontsize=7.5, color=C_SOFT)
    fig.tight_layout()
    return _save(fig, "fig-scintillation-bubbles.png")


def fig_tid_wavefront() -> Path:
    lon = np.linspace(-20, 20, 240)
    lat = np.linspace(-15, 15, 180)
    Lon, Lat = np.meshgrid(lon, lat)

    k = 2 * np.pi / 12.0
    phase = k * (0.85 * Lon + 0.35 * Lat)
    residual = 3.2 * np.sin(phase) * np.exp(-((Lat / 18.0) ** 2)) * np.exp(-((Lon / 28.0) ** 2))

    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    levels = np.linspace(-3.5, 3.5, 15)
    cf = ax.contourf(Lon, Lat, residual, levels=levels, cmap="RdBu_r", extend="both")
    cs = ax.contour(Lon, Lat, residual, levels=[-2, -1, 0, 1, 2], colors="#444444", linewidths=0.7)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%g")

    for y0 in (-6, 0, 6):
        ax.annotate(
            "",
            xy=(12, y0 + 2.2),
            xytext=(-8, y0 - 1.5),
            arrowprops=dict(arrowstyle="->", color="#222222", lw=1.4, connectionstyle="arc3,rad=0.05"),
        )
    ax.text(10.5, 10.5, "波前推进\nwavefront", fontsize=8.5, color="#222222", ha="center")

    cbar = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("ΔTEC 残差 / TEC residual (TECU, schematic)")

    ax.set_xlabel("经度相对 / Relative longitude (°)")
    ax.set_ylabel("纬度相对 / Relative latitude (°)")
    ax.set_title("TID 波前示意（TEC 残差场） ·  TID Wavefronts on TEC Residual")
    ax.set_aspect("equal")
    ax.text(
        0.02,
        0.03,
        "行进式电离层扰动 Traveling Ionospheric Disturbance · CC0",
        transform=ax.transAxes,
        fontsize=7.5,
        color="#444444",
    )
    fig.tight_layout()
    return _save(fig, "fig-tid-wavefront.png")


def fig_ne_profile_layers() -> Path:
    h = np.linspace(50, 800, 900)

    def chapman(h0: float, nm: float, H: float) -> np.ndarray:
        z = (h - h0) / H
        with np.errstate(over="ignore", invalid="ignore"):
            ne = nm * np.exp(0.5 * (1.0 - z - np.exp(-z)))
        return np.nan_to_num(ne, nan=0.0, posinf=0.0, neginf=0.0)

    ne = (
        chapman(75, 0.8e10, 8)
        + chapman(110, 1.5e11, 12)
        + chapman(180, 2.5e11, 30)
        + chapman(300, 9.0e11, 55)
    )
    ne = np.maximum(ne, 1e8)

    fig, ax = plt.subplots(figsize=(6.6, 7.2))
    ax.plot(ne / 1e11, h, color=C_NIGHT, lw=2.6)
    ax.fill_betweenx(h, 0, ne / 1e11, color=C_FILL, alpha=0.7)

    bands = [
        (60, 90, "#fce4d6"),
        (90, 150, "#d9ead3"),
        (150, 220, "#cfe2f3"),
        (220, 600, "#d0e2ff"),
    ]
    for y0, y1, color in bands:
        ax.axhspan(y0, y1, color=color, alpha=0.35, zorder=0)

    annotations = [
        (75, "D 层\nD-region", 0.9),
        (110, "E 层\nE-region", 2.0),
        (180, "F1", 3.2),
        (300, "F2 峰 NmF2\nF2 peak", 9.5),
    ]
    for hy, label, nx in annotations:
        ax.annotate(
            label,
            xy=(nx, hy),
            xytext=(nx + 2.8, hy + (40 if hy < 250 else -30)),
            fontsize=8.5,
            color="#333333",
            arrowprops=dict(arrowstyle="->", color=C_SOFT, lw=1.0),
        )

    ax.set_xlabel(r"电子密度 $N_e$ / Electron density ($10^{11}$ m$^{-3}$, schematic)")
    ax.set_ylabel("高度 Altitude (km)")
    ax.set_title("电离层电子密度剖面  ·  $N_e$ vs Altitude (D/E/F)")
    ax.set_xlim(0, 14)
    ax.set_ylim(50, 800)
    ax.grid(True, alpha=0.5)
    ax.text(
        0.02,
        0.02,
        "示意昼侧剖面 daytime schematic · CC0",
        transform=ax.transAxes,
        fontsize=7.5,
        color=C_SOFT,
    )
    fig.tight_layout()
    return _save(fig, "fig-ne-profile-layers.png")


def fig_flare_sudden_ionize() -> Path:
    t = np.linspace(-30, 90, 600)

    # Smooth soft X-ray flare pulse (no step artifacts)
    flare = 0.05 + 0.95 * np.exp(-0.5 * ((t - 0.0) / 5.5) ** 2)
    # Asymmetric decay for t>0
    flare = np.where(
        t > 0,
        0.05 + 0.95 * np.exp(-t / 12.0) * np.exp(-0.5 * ((np.minimum(t, 0)) / 5.5) ** 2),
        flare,
    )
    # Cleaner asymmetric: rise fast, decay slow
    rise = np.exp(-0.5 * ((np.minimum(t, 0)) / 4.0) ** 2)
    decay = np.exp(-np.maximum(t, 0) / 14.0)
    flare = 0.05 + 0.95 * rise * decay

    # D-region absorption / SID — peaks slightly after X-ray, slow recovery
    abs_rise = np.exp(-0.5 * ((np.minimum(t - 2, 0)) / 5.0) ** 2)
    abs_decay = np.exp(-np.maximum(t - 2, 0) / 28.0)
    absorption = 0.12 + 0.88 * abs_rise * abs_decay

    # Dayside TEC bump — broader, delayed
    tec_rise = np.exp(-0.5 * ((np.minimum(t - 5, 0)) / 8.0) ** 2)
    tec_decay = np.exp(-np.maximum(t - 5, 0) / 22.0)
    tec_bump = 0.2 + 1.8 * tec_rise * tec_decay

    fig, axes = plt.subplots(3, 1, figsize=(8.2, 7.0), sharex=True)

    axes[0].plot(t, flare, color="#e69138", lw=2.4)
    axes[0].fill_between(t, 0, flare, color="#fce5cd", alpha=0.7)
    axes[0].axvline(0, color=C_ALERT, ls="--", lw=1.2)
    axes[0].set_ylabel("软 X 射线\nSoft X-ray\n(rel.)")
    axes[0].set_title("太阳耀斑突发电离扰动示意  ·  Solar Flare SID Schematic")
    axes[0].text(2, 0.85, "耀斑峰值\nflare peak", fontsize=8, color=C_ALERT)
    axes[0].grid(True, alpha=0.5)
    axes[0].set_ylim(0, 1.15)

    axes[1].plot(t, absorption, color=C_ALERT, lw=2.4)
    axes[1].fill_between(t, 0.12, absorption, where=absorption >= 0.12, color="#f4cccc", alpha=0.55)
    axes[1].axvline(0, color=C_ALERT, ls="--", lw=1.2)
    axes[1].set_ylabel("D 层吸收\nD-region abs.\n(rel.)")
    axes[1].annotate(
        "SID：短波衰减 / VLF 相位跳\nHF fade & VLF phase advance",
        xy=(5, float(absorption.max())),
        xytext=(35, 0.75),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color=C_SOFT),
    )
    axes[1].grid(True, alpha=0.5)
    axes[1].set_ylim(0, 1.2)

    axes[2].plot(t, tec_bump, color=C_NIGHT, lw=2.4)
    axes[2].fill_between(t, 0.2, tec_bump, where=tec_bump >= 0.2, color=C_FILL, alpha=0.7)
    axes[2].axvline(0, color=C_ALERT, ls="--", lw=1.2)
    axes[2].set_ylabel("ΔTEC\n(TECU, sch.)")
    axes[2].set_xlabel("相对耀斑峰值时间 Time from flare peak (min)")
    axes[2].annotate(
        "日侧 TEC 短暂增强\ndayside TEC bump",
        xy=(8, float(tec_bump.max())),
        xytext=(40, 1.5),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color=C_SOFT),
    )
    axes[2].grid(True, alpha=0.5)
    axes[2].set_ylim(0, 2.4)
    axes[2].set_xlim(-30, 90)
    axes[2].text(
        0.01,
        0.05,
        "示意 / schematic · CC0",
        transform=axes[2].transAxes,
        fontsize=7.5,
        color=C_SOFT,
    )
    fig.tight_layout()
    return _save(fig, "fig-flare-sudden-ionize.png")


def fig_roti_time_series() -> Path:
    rng = np.random.default_rng(42)
    t = np.linspace(0, 24, 24 * 60)

    quiet = 0.08 + 0.03 * np.sin(2 * np.pi * t / 24) + 0.015 * rng.standard_normal(t.size)
    quiet = np.clip(quiet, 0.02, None)

    base = 0.10 + 0.04 * np.sin(2 * np.pi * t / 24)
    burst = np.zeros_like(t)
    mask = (t >= 19.0) & (t <= 23.2)
    burst[mask] = 0.9 * np.exp(-0.5 * ((t[mask] - 21.0) / 0.9) ** 2)
    spikes = np.zeros_like(t)
    for ts in [19.4, 19.9, 20.4, 20.8, 21.2, 21.7, 22.1, 22.6]:
        spikes += 0.55 * np.exp(-0.5 * ((t - ts) / 0.07) ** 2)
    noise = 0.04 * rng.standard_normal(t.size)
    scale = burst / (burst.max() + 1e-6)
    disturbed = np.clip(base + burst + spikes * scale + noise, 0.02, None)

    fig, axes = plt.subplots(2, 1, figsize=(8.4, 5.6), sharex=True)

    axes[0].plot(t, quiet, color=C_ACCENT, lw=1.2)
    axes[0].axhline(0.25, color="#aaaaaa", ls=":", lw=1.0)
    axes[0].set_ylabel("ROTI\n(TECU/min)")
    axes[0].set_title("安静 vs 扰动 ROTI 时间序列示意  ·  Quiet vs Disturbed ROTI")
    axes[0].text(
        0.01, 0.88, "安静日 Quiet", transform=axes[0].transAxes, fontsize=10, color=C_ACCENT, weight="bold"
    )
    axes[0].set_ylim(0, 1.6)
    axes[0].grid(True, alpha=0.5)

    axes[1].plot(t, disturbed, color=C_ALERT, lw=1.15)
    axes[1].axvspan(19.0, 23.2, color="#fce5cd", alpha=0.55, zorder=0)
    axes[1].axhline(0.25, color="#aaaaaa", ls=":", lw=1.0)
    axes[1].set_ylabel("ROTI\n(TECU/min)")
    axes[1].set_xlabel("地方时 Local time (h)")
    axes[1].text(
        0.01,
        0.88,
        "扰动日 Disturbed（日落后赤道泡窗口）",
        transform=axes[1].transAxes,
        fontsize=10,
        color=C_ALERT,
        weight="bold",
    )
    axes[1].annotate(
        "日落后闪烁窗\npost-sunset EPB window",
        xy=(21.0, 1.15),
        xytext=(8.5, 1.25),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color="#b45f06"),
        color="#b45f06",
    )
    axes[1].set_ylim(0, 1.6)
    axes[1].set_xlim(0, 24)
    axes[1].set_xticks([0, 4, 8, 12, 16, 18, 20, 22, 24])
    axes[1].grid(True, alpha=0.5)
    axes[1].text(
        0.01,
        0.05,
        "阈值：示意阈值，非实测  ·  schematic thresholds · CC0",
        transform=axes[1].transAxes,
        fontsize=7.5,
        color=C_SOFT,
    )
    fig.tight_layout()
    return _save(fig, "fig-roti-time-series.png")


def fig_phenomena_gallery(paths: list[Path]) -> Path:
    """Optional 2x3 collage of the six schematics (also CC0)."""
    from matplotlib.image import imread

    fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.2))
    titles = [
        "Day/Night TEC",
        "EPB / Scintillation",
        "TID wavefronts",
        "Ne profile D/E/F",
        "Flare SID",
        "Quiet vs ROTI",
    ]
    for ax, path, title in zip(axes.ravel(), paths, titles):
        ax.imshow(imread(path))
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle("电离层现象教学图集  ·  Ionosphere phenomena gallery (CC0)", fontsize=13, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, "fig-phenomena-gallery.png")


def main() -> None:
    paths = [
        fig_tec_day_night(),
        fig_scintillation_bubbles(),
        fig_tid_wavefront(),
        fig_ne_profile_layers(),
        fig_flare_sudden_ionize(),
        fig_roti_time_series(),
    ]
    fig_phenomena_gallery(paths)
    print(f"done: {len(paths)} + gallery → {OUT}")


if __name__ == "__main__":
    main()
