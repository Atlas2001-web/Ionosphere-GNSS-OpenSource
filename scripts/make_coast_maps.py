#!/usr/bin/env python3
"""Generate coastline basemap teaching schematics (cartopy + Natural Earth).

Synthetic ionosphere fields only — not real event products.
Output: docs/tutorials/images/fig-*-coast.png

Usage (from repo root):
  /workspace/iono-figs/.venv/bin/python scripts/make_coast_maps.py
  # or: .venv/bin/python scripts/make_coast_maps.py  (if cartopy installed)
"""
from __future__ import annotations

from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

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
    }
)

FOOT = "schematic · CC0"
PROJ = ccrs.PlateCarree()


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def _basemap(ax, extent=None, pale_land=True) -> None:
    if extent is not None:
        ax.set_extent(extent, crs=PROJ)
    if pale_land:
        ax.add_feature(cfeature.OCEAN, facecolor="#e8f4fc", zorder=0)
        ax.add_feature(cfeature.LAND, facecolor="#f5f0e6", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, edgecolor="#333333", zorder=3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3, edgecolor="#888888", linestyle=":", zorder=3)
    gl = ax.gridlines(draw_labels=True, linewidth=0.4, color="gray", alpha=0.45, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False


def _footer(fig: plt.Figure) -> None:
    fig.text(0.5, 0.01, FOOT, ha="center", va="bottom", fontsize=8, color="#666666")


# ---------------------------------------------------------------------------
# 1. Global synthetic VTEC with daytime EIA-ish pattern
# ---------------------------------------------------------------------------
def fig_vtec_global_coast() -> None:
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-90, 90, 181)
    Lon, Lat = np.meshgrid(lon, lat)

    # Daytime hemisphere centered near lon=0 (noon schematic)
    day = 0.5 * (1 + np.cos(np.deg2rad(Lon)))  # 1 at lon=0, 0 at ±180
    day = np.clip(day, 0, 1)

    # Background Chapman-like lat dependence + EIA twin crests ~±15°
    base = 8 + 22 * day * np.exp(-((Lat) / 55) ** 2)
    crest_n = 18 * day * np.exp(-((Lat - 15) / 8) ** 2) * np.exp(-((Lon - 0) / 70) ** 2)
    crest_s = 18 * day * np.exp(-((Lat + 15) / 8) ** 2) * np.exp(-((Lon - 0) / 70) ** 2)
    trough = -6 * day * np.exp(-(Lat / 6) ** 2) * np.exp(-(Lon / 80) ** 2)
    vtec = base + crest_n + crest_s + trough
    vtec = np.clip(vtec, 0, None)

    fig = plt.figure(figsize=(10.5, 5.2))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-180, 180, -70, 70])
    mesh = ax.pcolormesh(
        Lon, Lat, vtec, transform=PROJ, cmap="YlOrRd", shading="auto", zorder=1, alpha=0.85
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.78)
    cb.set_label("VTEC (TECU, schematic)")
    ax.set_title("Global VTEC + coastlines (schematic) — daytime EIA-ish")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-vtec-global-coast.png")


# ---------------------------------------------------------------------------
# 2. Regional equatorial TEC — twin crests + trough
# ---------------------------------------------------------------------------
def fig_eia_tec_map_coast() -> None:
    lon = np.linspace(-60, 60, 241)
    lat = np.linspace(-40, 40, 161)
    Lon, Lat = np.meshgrid(lon, lat)

    # Afternoon EIA over Atlantic/Africa belt
    day = np.exp(-((Lon - 10) / 45) ** 2)
    bg = 12 + 8 * day * np.exp(-(Lat / 40) ** 2)
    cn = 28 * day * np.exp(-((Lat - 12) / 6) ** 2)
    cs = 26 * day * np.exp(-((Lat + 14) / 6.5) ** 2)
    tr = -10 * day * np.exp(-(Lat / 5) ** 2)
    tec = bg + cn + cs + tr

    fig = plt.figure(figsize=(9.0, 6.0))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-60, 60, -40, 40])
    mesh = ax.contourf(Lon, Lat, tec, levels=18, transform=PROJ, cmap="turbo", zorder=1, alpha=0.88)
    ax.contour(
        Lon, Lat, tec, levels=8, transform=PROJ, colors="k", linewidths=0.35, alpha=0.35, zorder=2
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cb.set_label("TEC (TECU, schematic)")
    ax.set_title("Equatorial Ionization Anomaly — twin crests + trough (schematic)")
    ax.axhline(0, color="green", ls="--", lw=0.8, alpha=0.6, zorder=4)
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-eia-tec-map-coast.png")


# ---------------------------------------------------------------------------
# 3. ROTI spatial hotspots — equatorial after-sunset patches
# ---------------------------------------------------------------------------
def fig_roti_hotspots_coast() -> None:
    lon = np.linspace(-90, 0, 181)
    lat = np.linspace(-30, 30, 121)
    Lon, Lat = np.meshgrid(lon, lat)

    # Quiet background
    roti = 0.08 + 0.04 * np.random.default_rng(42).random(Lon.shape)

    # After-sunset hotspot clusters (lon ~ -50..-20, near ±10–20°)
    patches = [
        (-45, 12, 8, 5, 1.4),
        (-38, -15, 7, 4.5, 1.2),
        (-55, 8, 6, 4, 1.0),
        (-30, 18, 5, 3.5, 0.9),
        (-42, -8, 9, 3, 1.1),
        (-25, -18, 6, 4, 0.85),
    ]
    for lon0, lat0, sx, sy, amp in patches:
        roti += amp * np.exp(-(((Lon - lon0) / sx) ** 2 + ((Lat - lat0) / sy) ** 2))

    fig = plt.figure(figsize=(9.0, 5.8))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-90, 0, -30, 30])
    mesh = ax.pcolormesh(
        Lon, Lat, roti, transform=PROJ, cmap="hot_r", shading="auto", zorder=1, alpha=0.9, vmin=0, vmax=1.6
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cb.set_label("ROTI (TECU/min, schematic)")
    ax.set_title("ROTI hotspots — equatorial after-sunset patches (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-roti-hotspots-coast.png")


# ---------------------------------------------------------------------------
# 4. Storm-minus-quiet ΔTEC — RdBu_r diverging
# ---------------------------------------------------------------------------
def fig_storm_tec_diff_coast() -> None:
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-70, 70, 141)
    Lon, Lat = np.meshgrid(lon, lat)

    # Positive storm effect mid-latitudes dayside; negative trough / depletion zones
    pos = 12 * np.exp(-((Lat - 40) / 18) ** 2) * np.exp(-((Lon - 20) / 60) ** 2)
    pos += 10 * np.exp(-((Lat + 35) / 16) ** 2) * np.exp(-((Lon + 40) / 55) ** 2)
    neg = -14 * np.exp(-((Lat - 55) / 12) ** 2) * np.exp(-((Lon - 100) / 50) ** 2)
    neg += -9 * np.exp(-(Lat / 25) ** 2) * np.exp(-((Lon + 90) / 70) ** 2)
    # Mild EIA enhancement remnant
    eia = 6 * (
        np.exp(-((Lat - 15) / 8) ** 2) + np.exp(-((Lat + 15) / 8) ** 2)
    ) * np.exp(-(Lon / 80) ** 2)
    dtec = pos + neg + eia

    fig = plt.figure(figsize=(10.5, 5.0))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-180, 180, -70, 70])
    vmax = 15
    mesh = ax.pcolormesh(
        Lon,
        Lat,
        dtec,
        transform=PROJ,
        cmap="RdBu_r",
        shading="auto",
        zorder=1,
        alpha=0.88,
        vmin=-vmax,
        vmax=vmax,
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.78)
    cb.set_label("ΔTEC storm−quiet (TECU, schematic)")
    ax.set_title("Storm-minus-quiet ΔTEC map (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-storm-tec-diff-coast.png")


# ---------------------------------------------------------------------------
# 5. Low-latitude scintillation / plasma-bubble belt
# ---------------------------------------------------------------------------
def fig_bubble_belt_coast() -> None:
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-40, 40, 161)
    Lon, Lat = np.meshgrid(lon, lat)

    # Belt envelope ~±20° magnetic approx geographic
    belt = np.exp(-(np.abs(Lat) - 12) ** 2 / (2 * 7**2))
    # Stronger after local sunset — schematically west of noon meridian (lon>30 weak, lon<-20 strong)
    sunset_w = 0.3 + 0.7 * (0.5 * (1 - np.tanh((Lon + 10) / 40)))
    # Discrete bubble-like longitude modulation
    bubbles = 0.55 + 0.45 * np.sin(np.deg2rad(3.5 * Lon)) ** 2 * np.sin(np.deg2rad(Lon + 40)) ** 2
    s4 = 0.05 + 0.85 * belt * sunset_w * bubbles
    # Extra patches over Americas / Africa / SE Asia
    for lon0, lat0, amp in [(-50, 8, 0.35), (-40, -12, 0.3), (10, 5, 0.28), (100, -8, 0.32), (120, 10, 0.3)]:
        s4 += amp * np.exp(-(((Lon - lon0) / 18) ** 2 + ((Lat - lat0) / 6) ** 2))
    s4 = np.clip(s4, 0, 1.2)

    fig = plt.figure(figsize=(10.5, 4.6))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-180, 180, -40, 40])
    mesh = ax.pcolormesh(
        Lon, Lat, s4, transform=PROJ, cmap="magma", shading="auto", zorder=1, alpha=0.9, vmin=0, vmax=1.1
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.82)
    cb.set_label("S4 index (schematic)")
    ax.set_title("Low-latitude scintillation / plasma-bubble belt (schematic)")
    ax.axhline(0, color="cyan", ls="--", lw=0.7, alpha=0.5, zorder=4)
    _footer(fig)
    fig.subplots_adjust(bottom=0.07)
    _save(fig, "fig-bubble-belt-coast.png")


# ---------------------------------------------------------------------------
# 6. IPP ground-track arcs over a region
# ---------------------------------------------------------------------------
def fig_ipp_tracks_coast() -> None:
    # East Asia / West Pacific region
    extent = [100, 150, 10, 50]

    fig = plt.figure(figsize=(8.5, 6.5))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=extent)

    rng = np.random.default_rng(7)
    colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628"]
    # Receiver sites
    rx = [(116.4, 39.9, "BJ"), (121.5, 31.2, "SH"), (113.3, 23.1, "GZ"), (139.7, 35.7, "TK")]
    for lon, lat, lab in rx:
        ax.plot(lon, lat, "k^", ms=8, transform=PROJ, zorder=6)
        ax.text(lon + 0.8, lat + 0.6, lab, fontsize=8, transform=PROJ, zorder=6)

    # Synthetic IPP arcs (great-circle-ish polylines)
    for i, color in enumerate(colors):
        lon0 = 105 + 8 * i + rng.uniform(-2, 2)
        lat0 = 15 + rng.uniform(-3, 5)
        t = np.linspace(0, 1, 80)
        # Arc sweeping NE
        lon_arc = lon0 + 28 * t + 3 * np.sin(2 * np.pi * t)
        lat_arc = lat0 + 22 * t + 2.5 * np.sin(np.pi * t + i)
        # clip roughly to extent
        mask = (lon_arc > 98) & (lon_arc < 152) & (lat_arc > 8) & (lat_arc < 52)
        ax.plot(
            lon_arc[mask],
            lat_arc[mask],
            "-",
            color=color,
            lw=1.8,
            transform=PROJ,
            zorder=5,
            label=f"PRN {10 + i}",
            alpha=0.9,
        )
        # sample IPP dots
        idx = np.where(mask)[0][::12]
        ax.scatter(lon_arc[idx], lat_arc[idx], s=18, c=color, transform=PROJ, zorder=5, edgecolors="white", linewidths=0.4)

    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.set_title("IPP ground-track arcs — satellite pass geometry (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-ipp-tracks-coast.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_vtec_global_coast()
    fig_eia_tec_map_coast()
    fig_roti_hotspots_coast()
    fig_storm_tec_diff_coast()
    fig_bubble_belt_coast()
    fig_ipp_tracks_coast()
    print("done: 6 coastline basemap figures")


if __name__ == "__main__":
    main()
