#!/usr/bin/env python3
"""Generate schematic PNGs for tutorials 19–23 (phenomena series).

All figures are synthetic teaching schematics (not real event data).
Output: docs/tutorials/images/*.png

Usage (from repo root):
  .venv/bin/python scripts/make_phenomena_figs.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, patches

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tutorials" / "images"

# Prefer Noto Sans CJK SC; fall back to DejaVu.
_CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
_FONT_NAME = "DejaVu Sans"
if Path(_CJK).exists():
    try:
        font_manager.fontManager.addfont(_CJK)
        # TTC: pick SC face by name if registered
        for f in font_manager.fontManager.ttflist:
            if "Noto Sans CJK SC" in f.name:
                _FONT_NAME = f.name
                break
        else:
            prop = font_manager.FontProperties(fname=_CJK)
            _FONT_NAME = prop.get_name()
    except Exception:
        pass

mpl.rcParams.update(
    {
        "font.family": _FONT_NAME,
        "font.size": 10,
        "axes.unicode_minus": False,
        "figure.dpi": 140,
        "savefig.dpi": 140,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linewidth": 0.6,
    }
)

FOOT = "示意 / schematic • CC0"


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def fig_storm_quiet_residual() -> None:
    t = np.linspace(0, 48, 961)
    quiet = 18 + 5 * np.sin(2 * np.pi * (t - 6) / 24)
    storm = quiet.copy()
    # positive then negative residual after storm onset ~18 h
    pos = (t >= 18) & (t < 30)
    neg = (t >= 30) & (t < 45)
    storm[pos] += 6 * np.sin(np.pi * (t[pos] - 18) / 12) ** 1.2
    storm[neg] -= 5.5 * np.sin(np.pi * (t[neg] - 30) / 15)
    # smooth onset bump
    onset = (t >= 17.5) & (t < 19)
    storm[onset] += 2.5 * ((t[onset] - 17.5) / 1.5)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(t, quiet, color="#2ca02c", lw=2.0, label="Quiet-day baseline")
    ax.plot(t, storm, color="#d62728", lw=2.0, label="Storm day")
    ax.fill_between(
        t, quiet, storm, where=storm >= quiet, interpolate=True,
        color="#ffbbbb", alpha=0.7, label="Positive phase",
    )
    ax.fill_between(
        t, quiet, storm, where=storm < quiet, interpolate=True,
        color="#bbd4ff", alpha=0.7, label="Negative phase",
    )
    ax.set_xlim(0, 48)
    ax.set_ylim(12, 30)
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("VTEC (schematic TECU)")
    ax.set_title("Storm analysis idea: storm – quiet residual")
    ax.legend(loc="upper center", ncol=2, framealpha=0.95)
    ax.text(0.01, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color="0.45")
    _save(fig, "fig-storm-quiet-residual.png")


def fig_eia_twin_crests() -> None:
    lat = np.linspace(-40, 40, 401)
    crest = (
        8
        + 22 * np.exp(-0.5 * ((lat - 16) / 7) ** 2)
        + 22 * np.exp(-0.5 * ((lat + 16) / 7) ** 2)
        - 6 * np.exp(-0.5 * (lat / 5) ** 2)
    )
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(lat, crest, color="#1f77b4", lw=2.4)
    ax.fill_between(lat, 0, crest, color="#1f77b4", alpha=0.15)
    ax.axvline(0, color="0.5", ls=":", lw=1)
    ax.annotate("北峰 N crest", xy=(16, crest[np.argmin(np.abs(lat - 16))]),
                xytext=(22, 32), arrowprops=dict(arrowstyle="->", color="0.4"),
                color="0.3")
    ax.annotate("南峰 S crest", xy=(-16, crest[np.argmin(np.abs(lat + 16))]),
                xytext=(-34, 32), arrowprops=dict(arrowstyle="->", color="0.4"),
                color="0.3")
    ax.annotate("赤道槽 trough", xy=(0, crest[np.argmin(np.abs(lat))]),
                xytext=(4, 8), arrowprops=dict(arrowstyle="->", color="0.4"),
                color="0.3")
    ax.set_xlim(-40, 40)
    ax.set_ylim(0, 40)
    ax.set_xlabel("磁纬 Mag. latitude (°)")
    ax.set_ylabel("相对 VTEC (schematic)")
    ax.set_title("赤道异常 EIA 双峰示意 · Twin crests")
    ax.text(0.01, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color="0.45")
    _save(fig, "fig-eia-twin-crests.png")


def fig_tec_day_night() -> None:
    lat = np.linspace(-60, 60, 601)

    def eia(amp, trough, width=8.5, peak_lat=16.5):
        return (
            trough
            + amp * np.exp(-0.5 * ((lat - peak_lat) / width) ** 2)
            + amp * np.exp(-0.5 * ((lat + peak_lat) / width) ** 2)
            + 4 * np.exp(-0.5 * ((np.abs(lat) - 45) / 18) ** 2)
        )

    day = eia(38, 10)
    night = eia(14, 12)
    # soften night trough difference
    night = night * 0.55 + 8

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.fill_between(lat, night, day, color="#f0c8a8", alpha=0.45)
    ax.plot(lat, day, color="#c45a27", lw=2.2, label="昼 / Day")
    ax.plot(lat, night, color="#1d4570", lw=2.4, ls="--", label="夜 / Night")
    ax.axvline(0, color="0.55", ls=":", lw=1)
    ax.annotate(
        "赤道槽 equator trough",
        xy=(0, day[np.argmin(np.abs(lat))]),
        xytext=(8, 6),
        arrowprops=dict(arrowstyle="->", color="0.45"),
        color="0.4",
        fontsize=9,
    )
    ax.set_xlim(-60, 60)
    ax.set_ylim(0, 55)
    ax.set_xlabel("磁纬 Mag. latitude (°)")
    ax.set_ylabel("相对 VTEC / Relative VTEC (schematic)")
    ax.set_title("日夜 TEC 随纬度示意 · Day vs Night TEC vs Latitude")
    ax.legend(loc="upper right")
    ax.text(0.01, 0.02, FOOT, transform=ax.transAxes, fontsize=8, color="0.45")
    _save(fig, "fig-tec-day-night.png")


def fig_ne_profile_layers() -> None:
    h = np.linspace(50, 800, 900)

    def chapman(hm, Nm, H):
        z = (h - hm) / H
        return Nm * np.exp(0.5 * (1 - z - np.exp(-z)))

    ne = (
        chapman(80, 0.4, 12)
        + chapman(110, 1.6, 18)
        + chapman(200, 4.0, 35)
        + chapman(300, 9.5, 55)
    )

    fig, ax = plt.subplots(figsize=(5.2, 7.0))
    bands = [
        (60, 90, "#f5d5c8", "D"),
        (90, 150, "#e8f0c8", "E"),
        (150, 220, "#d8e8f5", "F1"),
        (220, 600, "#c8dff0", "F2"),
    ]
    for y0, y1, c, _ in bands:
        ax.axhspan(y0, y1, color=c, alpha=0.55, zorder=0)

    ax.plot(ne, h, color="#1d3a6e", lw=2.6, zorder=2)
    labels = [
        (80, "D 层 D-region"),
        (115, "E 层 E-region"),
        (200, "F1"),
        (300, "F2 峰 NmF2 / F2 peak"),
    ]
    for hy, lab in labels:
        ix = np.argmin(np.abs(h - hy))
        ax.annotate(
            lab,
            xy=(ne[ix], h[ix]),
            xytext=(ne[ix] + 2.2, h[ix] + (20 if hy < 250 else -10)),
            arrowprops=dict(arrowstyle="->", color="0.45"),
            color="0.35",
            fontsize=9,
        )
    ax.set_xlim(0, 14)
    ax.set_ylim(50, 800)
    ax.set_xlabel(r"电子密度 $N_e$ / Electron density ($10^{11}\,\mathrm{m}^{-3}$, schematic)")
    ax.set_ylabel("高度 Altitude (km)")
    ax.set_title("电离层电子密度剖面 · $N_e$ vs Altitude (D/E/F)")
    ax.text(0.02, 0.015, "示意昼侧剖面 daytime schematic • CC0",
            transform=ax.transAxes, fontsize=8, color="0.45")
    _save(fig, "fig-ne-profile-layers.png")


def fig_scintillation_bubbles() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("赤道等离子体泡与闪烁示意 · Equatorial Plasma Bubbles / Scintillation",
                 fontsize=12, pad=8)

    # ground
    ax.add_patch(patches.FancyBboxPatch(
        (0.3, 0.4), 9.4, 1.1, boxstyle="round,pad=0.02",
        facecolor="#d9efc7", edgecolor="#6a9a4a", lw=1.2,
    ))
    ax.text(5, 0.95, "地面接收机 GNSS Rx · Ground receivers",
            ha="center", va="center", fontsize=10)

    # F region
    ax.add_patch(patches.FancyBboxPatch(
        (0.3, 4.2), 9.4, 3.2, boxstyle="round,pad=0.02",
        facecolor="#cfe6f5", edgecolor="#6a9ec0", lw=1.2,
    ))
    ax.text(0.55, 7.05, "F层 / F-region", fontsize=10, color="#2a5a7a")

    # bubbles
    for cx in (2.2, 5.0, 7.8):
        e = patches.Ellipse(
            (cx, 5.7), 1.6, 2.2, facecolor="#f7d9b8",
            edgecolor="#c45a27", ls="--", lw=1.5, alpha=0.9,
        )
        ax.add_patch(e)
        ax.text(cx, 5.7, "泡 EPB", ha="center", va="center", fontsize=9, color="#8a3a10")

    # satellites
    sats = [2.2, 5.0, 7.8]
    ax.scatter(sats, [9.2, 9.2, 9.2], marker="^", s=120, c="#6b3fa0", zorder=5)
    ax.text(0.5, 9.2, "GNSS 卫星", fontsize=9, color="#6b3fa0")
    ax.text(8.6, 9.2, "satellites", fontsize=9, color="#6b3fa0")

    # rays with wiggle in F-region
    rng = np.random.default_rng(7)
    for x0 in sats:
        y_lo, y_hi = 1.5, 9.0
        ys = np.linspace(y_lo, y_hi, 200)
        xs = np.full_like(ys, x0)
        in_f = (ys > 4.2) & (ys < 7.4)
        xs[in_f] += 0.18 * np.sin(28 * (ys[in_f] - 4.2)) + 0.05 * rng.normal(size=in_f.sum())
        ax.plot(xs, ys, color="#c0392b", lw=1.6)

    ax.axvline(5.0, color="0.55", ls=":", lw=1)
    ax.text(5.1, 3.6, "磁赤道 mag. eq.", fontsize=8, color="0.4")

    ax.text(
        5, 2.7,
        "低密度等离子体泡切断射线 → 相位/幅度闪烁\n"
        "Depleted bubbles along ray path → S4 / σφ scintillation",
        ha="center", va="center", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3c4", edgecolor="#c45a27"),
    )
    ax.text(0.02, 0.01, FOOT, transform=ax.transAxes, fontsize=8, color="0.45")
    _save(fig, "fig-scintillation-bubbles.png")


def fig_flare_sudden_ionize() -> None:
    t = np.linspace(-30, 90, 601)

    # soft X-ray: rise to peak at 0, then decay
    sxr = np.where(
        t < 0,
        0.05 + 0.95 * np.exp(-((t + 2) / 4) ** 2) * (t > -15),
        np.exp(-t / 12),
    )
    sxr = np.clip(sxr, 0, None)
    # cleaner analytic flare
    rise = np.exp(-0.5 * ((t + 3) / 3.5) ** 2)
    decay = np.where(t >= 0, np.exp(-t / 14), 0)
    sxr = 0.05 + 0.95 * np.where(t < 0, rise / rise.max() if t.min() < 0 else rise, decay)
    sxr = 0.05 + np.where(
        t < 0,
        0.95 * np.exp(-0.5 * ((t + 2.5) / 3.2) ** 2),
        0.95 * np.exp(-t / 13),
    )

    # D-region absorption: follows with slight lag
    abs_d = 0.08 + 0.92 * np.where(
        t < 2,
        np.exp(-0.5 * ((t - 1) / 4) ** 2),
        np.exp(-(t - 2) / 18),
    )
    # TEC bump: broader, slower decay
    dtec = 0.15 + 1.85 * np.where(
        t < 8,
        np.exp(-0.5 * ((t - 6) / 7) ** 2),
        np.exp(-(t - 8) / 28),
    )

    fig, axes = plt.subplots(3, 1, figsize=(7.4, 7.2), sharex=True)
    series = [
        (sxr, "#e67e22", "Soft X-ray (rel.) / 软 X 射线", "耀斑峰值 flare peak", (-8, 1.05)),
        (abs_d, "#c0392b", "D-region abs. (rel.) / D 层吸收",
         "SID: 短波衰减 / VLF 相位跳\nHF fade & VLF phase advance", (25, 0.85)),
        (dtec, "#1a5276", "ΔTEC (TECU, sch.)",
         "日侧 TEC 短暂增强\ndayside TEC bump", (35, 1.6)),
    ]
    for ax, (y, color, ylab, ann, axy) in zip(axes, series):
        ax.plot(t, y, color=color, lw=2.0)
        ax.fill_between(t, 0, y, color=color, alpha=0.22)
        ax.axvline(0, color="#c0392b", ls="--", lw=1.2)
        ax.set_ylabel(ylab, fontsize=9)
        ax.set_ylim(0, y.max() * 1.25)
        ax.annotate(
            ann, xy=(2 if "TEC" in ylab or "D-" in ylab else 0, y[np.argmin(np.abs(t))]),
            xytext=axy,
            arrowprops=dict(arrowstyle="->", color="0.4"),
            color="#a93226" if "flare" in ann else "0.35",
            fontsize=8,
        )
    axes[-1].set_xlabel("相对耀斑峰值时间 Time from flare peak (min)")
    axes[-1].set_xlim(-30, 90)
    axes[0].set_title("太阳耀斑突发电离层扰动示意 • Solar Flare SID Schematic")
    axes[-1].text(0.01, 0.04, FOOT, transform=axes[-1].transAxes, fontsize=8, color="0.45")
    fig.tight_layout()
    _save(fig, "fig-flare-sudden-ionize.png")


def fig_roti_time_series() -> None:
    rng = np.random.default_rng(42)
    lt = np.linspace(0, 24, 1441)  # 1-min
    quiet = 0.04 + 0.025 * rng.normal(size=lt.size)
    quiet = np.clip(quiet, 0, None)

    dist = 0.05 + 0.03 * rng.normal(size=lt.size)
    window = (lt >= 19) & (lt <= 23.2)
    # bursty spikes
    burst = np.zeros_like(lt)
    for peak, amp, w in [(19.6, 0.9, 0.25), (20.4, 1.35, 0.35), (21.1, 1.5, 0.4),
                         (21.8, 1.1, 0.3), (22.5, 0.7, 0.35)]:
        burst += amp * np.exp(-0.5 * ((lt - peak) / w) ** 2)
    noise = np.where(window, 0.15 * np.abs(rng.normal(size=lt.size)), 0)
    dist = np.clip(dist + burst + noise, 0, None)

    fig, axes = plt.subplots(2, 1, figsize=(7.6, 5.4), sharex=True)
    axes[0].plot(lt, quiet, color="#148a80", lw=1.0)
    axes[0].text(0.02, 0.88, "安静日 Quiet", transform=axes[0].transAxes,
                 color="#148a80", fontsize=11, fontweight="bold")
    axes[0].axhline(0.25, color="0.6", ls=":", lw=0.8)
    axes[0].set_ylim(0, 1.55)
    axes[0].set_ylabel("ROTI (TECU/min)")

    axes[1].axvspan(19, 23.2, color="#f5d5b8", alpha=0.55)
    axes[1].plot(lt, dist, color="#c0392b", lw=1.0)
    axes[1].text(0.02, 0.88, "扰动日 Disturbed (日落后赤道泡窗口)",
                 transform=axes[1].transAxes, color="#c0392b", fontsize=11, fontweight="bold")
    axes[1].annotate(
        "日落后闪烁窗 post-sunset EPB window",
        xy=(21.1, 1.45), xytext=(8, 1.2),
        arrowprops=dict(arrowstyle="->", color="#8a4b12"),
        color="#8a4b12", fontsize=9,
    )
    axes[1].axhline(0.25, color="0.6", ls=":", lw=0.8)
    axes[1].set_ylim(0, 1.55)
    axes[1].set_ylabel("ROTI (TECU/min)")
    axes[1].set_xlabel("地方时 Local time (h)")
    axes[1].set_xlim(0, 24)
    axes[0].set_title("安静 vs 扰动 ROTI 时间序列示意 · Quiet vs Disturbed ROTI")
    axes[1].text(0.01, 0.04, FOOT, transform=axes[1].transAxes, fontsize=8, color="0.45")
    fig.tight_layout()
    _save(fig, "fig-roti-time-series.png")


def fig_phenomena_gallery() -> None:
    fig, axes = plt.subplots(1, 4, figsize=(13.5, 3.4))
    fig.suptitle("Ionosphere phenomena gallery (CC0 schematics)", fontsize=13, y=1.02)

    # 1 Day/Night latitude profile
    ax = axes[0]
    x = np.linspace(-1, 1, 200)
    day = 0.35 + 0.9 * np.exp(-((x - 0.35) / 0.22) ** 2) + 0.9 * np.exp(-((x + 0.35) / 0.22) ** 2)
    night = 0.25 + 0.55 * np.exp(-(x / 0.35) ** 2)
    ax.plot(x, day, color="#e67e22", lw=2)
    ax.plot(x, night, color="#1f4e79", lw=2)
    ax.set_title("Day/Night", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])

    # 2 Bubbles heatmap
    ax = axes[1]
    xx = np.linspace(-2, 2, 160)
    yy = np.linspace(-1.2, 1.2, 100)
    X, Y = np.meshgrid(xx, yy)
    field = np.exp(-(X ** 2 / 1.6 + Y ** 2 / 0.55))
    for cx in (-1.0, -0.2, 0.55, 1.15):
        field -= 0.55 * np.exp(-(((X - cx) / 0.18) ** 2 + ((Y) / 0.55) ** 2))
    ax.imshow(field, origin="lower", cmap="magma", aspect="auto")
    ax.set_title("Bubbles", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])

    # 3 TID bands
    ax = axes[2]
    X, Y = np.meshgrid(np.linspace(-2, 2, 160), np.linspace(-1.2, 1.2, 100))
    Z = np.sin(3.2 * X + 2.4 * Y)
    ax.imshow(Z, origin="lower", cmap="RdBu_r", aspect="auto")
    ax.set_title("TID", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])

    # 4 Ne profile
    ax = axes[3]
    h = np.linspace(0, 1, 200)
    ne = 0.08 * np.exp(-((h - 0.18) / 0.06) ** 2) + 0.85 * np.exp(-((h - 0.48) / 0.14) ** 2)
    ax.plot(ne, h, color="#148a80", lw=2.2)
    ax.set_title("Ne profile", fontsize=11)
    ax.set_xticks([]); ax.set_yticks([])
    for a in axes:
        for spine in a.spines.values():
            spine.set_linewidth(1.0)

    fig.text(0.01, 0.01, FOOT, fontsize=8, color="0.45")
    fig.tight_layout()
    _save(fig, "fig-phenomena-gallery.png")


def fig_tid_wavefront_fixed() -> None:
    """Rewrite TID figure (separate from mistaken save in earlier draft)."""
    lon = np.linspace(-20, 20, 240)
    lat = np.linspace(-15, 15, 180)
    Lon, Lat = np.meshgrid(lon, lat)
    k = 2 * np.pi / 12
    Z = 3.2 * np.sin(k * (0.85 * Lon + 0.55 * Lat))

    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    levels = np.linspace(-3.2, 3.2, 17)
    cf = ax.contourf(Lon, Lat, Z, levels=levels, cmap="RdBu_r", extend="both")
    cs = ax.contour(Lon, Lat, Z, levels=[-2, -1, 0, 1, 2], colors="k", linewidths=0.7)
    ax.clabel(cs, fmt="%d", fontsize=8)
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("ΔTEC 残差 / TEC residual (TECU, schematic)")
    for y0 in (-6, 0, 6):
        ax.annotate(
            "",
            xy=(8, y0 + 3),
            xytext=(-2, y0 - 1),
            arrowprops=dict(arrowstyle="->", color="k", lw=1.4),
        )
    ax.text(6.5, 10, "波前推进 wavefront", fontsize=9, color="0.15")
    ax.set_xlabel("经度相对 / Relative longitude (°)")
    ax.set_ylabel("纬度相对 / Relative latitude (°)")
    ax.set_title("TID 波前示意 (TEC 残差场) • TID Wavefronts on TEC Residual")
    ax.set_aspect("equal", adjustable="box")
    ax.text(0.01, 0.02, "行进式电离层扰动 Traveling Ionospheric Disturbance • CC0",
            transform=ax.transAxes, fontsize=8, color="0.35")
    _save(fig, "fig-tid-wavefront.png")


def main() -> None:
    print(f"OUT = {OUT}")
    print(f"font = {_FONT_NAME}")
    fig_storm_quiet_residual()
    fig_eia_twin_crests()
    fig_tec_day_night()
    fig_ne_profile_layers()
    fig_scintillation_bubbles()
    fig_tid_wavefront_fixed()
    fig_flare_sudden_ionize()
    fig_roti_time_series()
    fig_phenomena_gallery()
    print("done.")


if __name__ == "__main__":
    main()
