#!/usr/bin/env python3
"""Generate coastline basemap teaching schematics (cartopy + Natural Earth).

Synthetic ionosphere fields only — not real event products.
Output: docs/tutorials/images/fig-*-coast.png

Usage (from repo root):
  .venv/bin/python scripts/make_coast_maps.py
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




# ---------------------------------------------------------------------------
# 7. TID wavefronts — ΔTEC ridges (mid-latitudes)
# ---------------------------------------------------------------------------
def fig_tid_wavefront_coast() -> None:
    # Continental US / North Atlantic mid-latitudes
    lon = np.linspace(-120, -40, 321)
    lat = np.linspace(25, 60, 141)
    Lon, Lat = np.meshgrid(lon, lat)

    # Quiet background + propagating MSTID-like ridges (SW–NE fronts)
    bg = 0.3 * np.exp(-((Lat - 42) / 25) ** 2)
    # Phase: wavevector pointing ~SE, fronts elongated NE–SW
    kx, ky = 0.18, -0.12  # deg^-1 schematic
    phase = kx * (Lon + 80) + ky * (Lat - 40)
    ridges = 4.5 * np.sin(2 * np.pi * phase) * np.exp(-((Lat - 42) / 18) ** 2)
    ridges *= np.exp(-((Lon + 85) / 45) ** 2)
    # Second packet slightly offset
    phase2 = kx * (Lon + 95) + ky * (Lat - 38) + 0.7
    ridges += 2.8 * np.sin(2 * np.pi * phase2) * np.exp(-((Lat - 40) / 16) ** 2)
    ridges *= np.exp(-((Lon + 70) / 50) ** 2)
    dtec = bg + ridges

    fig = plt.figure(figsize=(9.2, 5.8))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-120, -40, 25, 60])
    vmax = 5.5
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
    ax.contour(
        Lon, Lat, dtec, levels=[-3, -1.5, 1.5, 3], transform=PROJ,
        colors="k", linewidths=0.4, alpha=0.35, zorder=2,
    )
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cb.set_label("ΔTEC (TECU, schematic)")
    ax.annotate(
        "propagation →",
        xy=(-55, 35),
        xytext=(-72, 30),
        fontsize=9,
        color="#333333",
        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2),
        transform=PROJ,
        zorder=5,
    )
    ax.set_title("TID wavefronts — mid-latitude ΔTEC ridges (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-tid-wavefront-coast.png")


# ---------------------------------------------------------------------------
# 8. Auroral oval / high-latitude precipitation belt
# ---------------------------------------------------------------------------
def fig_aurora_oval_coast() -> None:
    # North polar stereographic view
    fig = plt.figure(figsize=(7.5, 7.5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.NorthPolarStereo(central_longitude=0))
    ax.set_extent([-180, 180, 50, 90], crs=PROJ)
    ax.add_feature(cfeature.OCEAN, facecolor="#e8f4fc", zorder=0)
    ax.add_feature(cfeature.LAND, facecolor="#f5f0e6", zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.55, edgecolor="#333333", zorder=3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.25, edgecolor="#888888", linestyle=":", zorder=3)
    gl = ax.gridlines(draw_labels=True, linewidth=0.4, color="gray", alpha=0.45, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False

    # Build oval intensity on a lon/lat grid (geomagnetic approx ≈ geographic for schematic)
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(50, 90, 81)
    Lon, Lat = np.meshgrid(lon, lat)
    # Colatitude from pole; oval peak ~67–72° MLAT (schematic geographic)
    colat = 90.0 - Lat
    # Mild day–night asymmetry: nightside (lon~180) broader / stronger
    night = 0.55 + 0.45 * (0.5 * (1 - np.cos(np.deg2rad(Lon))))  # stronger near ±180
    # Gaussian ring around ~22° colatitude (~68° lat)
    ring = np.exp(-((colat - 22) / 4.5) ** 2)
    # Weaker dayside cusp bump near lon=0, lat~75
    cusp = 0.35 * np.exp(-((Lat - 76) / 4) ** 2) * np.exp(-(Lon / 35) ** 2)
    precip = (0.15 + 0.95 * ring * night + cusp) * np.clip((Lat - 52) / 8, 0, 1)
    precip = np.clip(precip, 0, 1.2)

    mesh = ax.pcolormesh(
        Lon, Lat, precip, transform=PROJ, cmap="plasma", shading="auto",
        zorder=1, alpha=0.85, vmin=0, vmax=1.1,
    )
    # Guide rings at 60° / 70°
    for lat0 in (60, 70):
        th = np.linspace(0, 360, 361)
        ax.plot(th, np.full_like(th, lat0, dtype=float), transform=PROJ,
                color="cyan", ls="--", lw=0.7, alpha=0.55, zorder=4)
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.05, shrink=0.72)
    cb.set_label("Precipitation intensity (schematic)")
    ax.set_title("Auroral oval — high-latitude precipitation belt (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.05)
    _save(fig, "fig-aurora-oval-coast.png")


# ---------------------------------------------------------------------------
# 9. Eclipse path TEC depletion "hole"
# ---------------------------------------------------------------------------
def fig_eclipse_tec_hole_coast() -> None:
    # Americas / Atlantic belt for a total-solar-eclipse-like path
    lon = np.linspace(-130, -40, 361)
    lat = np.linspace(5, 55, 201)
    Lon, Lat = np.meshgrid(lon, lat)

    # Quiet daytime TEC background
    day = np.exp(-((Lon + 90) / 55) ** 2)
    tec = 18 + 20 * day * np.exp(-((Lat - 25) / 35) ** 2)

    # Eclipse path centerline (parametric curve SW → NE across CONUS/Mexico)
    # Hole: elongated Gaussian trough along path
    path_lat = 18 + 0.32 * (Lon + 115) + 0.002 * (Lon + 100) ** 2
    along = np.exp(-((Lon + 95) / 38) ** 2)  # active segment
    hole = -22 * along * np.exp(-((Lat - path_lat) / 3.8) ** 2)
    # Slightly wider penumbra
    penumbra = -8 * along * np.exp(-((Lat - path_lat) / 8) ** 2)
    tec = np.clip(tec + hole + penumbra, 0, None)

    fig = plt.figure(figsize=(9.5, 6.2))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-130, -40, 5, 55])
    mesh = ax.pcolormesh(
        Lon, Lat, tec, transform=PROJ, cmap="YlGnBu_r", shading="auto",
        zorder=1, alpha=0.88, vmin=0, vmax=40,
    )
    # Path centerline annotation
    lon_path = np.linspace(-120, -55, 120)
    lat_path = 18 + 0.32 * (lon_path + 115) + 0.002 * (lon_path + 100) ** 2
    ax.plot(lon_path, lat_path, color="#c0392b", lw=2.0, transform=PROJ, zorder=5, label="totality path")
    ax.plot(lon_path, lat_path, color="#c0392b", lw=8.0, alpha=0.15, transform=PROJ, zorder=4)
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cb.set_label("TEC (TECU, schematic)")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.set_title("Eclipse path TEC depletion hole (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-eclipse-tec-hole-coast.png")


# ---------------------------------------------------------------------------
# 10. Solar flare sudden ionization / HF blackout dayside footprint
# ---------------------------------------------------------------------------
def fig_flare_sudden_coast() -> None:
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-70, 70, 141)
    Lon, Lat = np.meshgrid(lon, lat)

    # Subsolar point at lon=0 schematic; dayside HF absorption / D-region ionization
    mu = np.cos(np.deg2rad(Lon)) * np.cos(np.deg2rad(Lat))  # rough SZA cosine at equinox noon@0
    mu = np.clip(mu, 0, 1)
    # Sudden ionospheric disturbance intensity ∝ soft X-ray × mu^k
    sid = mu ** 1.15
    # Stronger near subsolar
    sid *= np.exp(-(Lat / 70) ** 2)
    # Nightside essentially zero
    sid = np.where(mu > 0.02, sid, 0.0)

    fig = plt.figure(figsize=(10.5, 5.0))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-180, 180, -70, 70])
    mesh = ax.pcolormesh(
        Lon, Lat, sid, transform=PROJ, cmap="YlOrRd", shading="auto",
        zorder=1, alpha=0.88, vmin=0, vmax=1.0,
    )
    # Terminator lines (dusk/dawn at ±90°)
    ax.axvline(90, color="#1a5276", ls="--", lw=1.0, alpha=0.7, zorder=4)
    ax.axvline(-90, color="#1a5276", ls="--", lw=1.0, alpha=0.7, zorder=4)
    ax.plot(0, 0, marker="*", markersize=14, color="gold", markeredgecolor="#333",
            transform=PROJ, zorder=5, label="subsolar")
    ax.text(5, 4, "subsolar", fontsize=8, color="#333", transform=PROJ, zorder=5)
    ax.text(92, 55, "dawn", fontsize=8, color="#1a5276", transform=PROJ, zorder=5)
    ax.text(-108, 55, "dusk", fontsize=8, color="#1a5276", transform=PROJ, zorder=5)
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.78)
    cb.set_label("SID / HF absorption (schematic)")
    ax.set_title("Solar flare sudden ionization — dayside HF blackout footprint (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-flare-sudden-coast.png")


# ---------------------------------------------------------------------------
# 11. Magnetic equator + EIA crest latitudes (tropical belt)
# ---------------------------------------------------------------------------
def fig_magnetic_equator_coast() -> None:
    lon = np.linspace(-180, 180, 361)
    lat = np.linspace(-40, 40, 161)
    Lon, Lat = np.meshgrid(lon, lat)

    # Approximate magnetic equator: mild sinusoidal offset from geographic
    # (schematic — not IGRF): lat_meq ≈ 8*sin(lon+20°) + 2*sin(2*(lon))
    lat_meq = 8.0 * np.sin(np.deg2rad(Lon + 20)) + 2.0 * np.sin(np.deg2rad(2 * Lon))
    # EIA crests ~±15° magnetic latitude from magnetic equator
    crest_off = 15.0
    lat_cn = lat_meq + crest_off
    lat_cs = lat_meq - crest_off

    # Soft TEC field peaking at crests for context
    day = 0.5 * (1 + np.cos(np.deg2rad(Lon - 20)))
    day = np.clip(day, 0.15, 1)
    dist_n = Lat - lat_cn
    dist_s = Lat - lat_cs
    dist_eq = Lat - lat_meq
    tec = 10 + 8 * day * np.exp(-(dist_eq / 28) ** 2)
    tec += 22 * day * np.exp(-(dist_n / 6) ** 2)
    tec += 20 * day * np.exp(-(dist_s / 6.5) ** 2)
    tec -= 7 * day * np.exp(-(dist_eq / 5) ** 2)

    fig = plt.figure(figsize=(10.5, 4.8))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-180, 180, -40, 40])
    mesh = ax.pcolormesh(
        Lon, Lat, tec, transform=PROJ, cmap="turbo", shading="auto",
        zorder=1, alpha=0.82, vmin=5, vmax=45,
    )
    lon_line = np.linspace(-180, 180, 361)
    meq = 8.0 * np.sin(np.deg2rad(lon_line + 20)) + 2.0 * np.sin(np.deg2rad(2 * lon_line))
    ax.plot(lon_line, meq, color="white", lw=2.4, transform=PROJ, zorder=5, label="magnetic equator")
    ax.plot(lon_line, meq, color="#e74c3c", lw=1.4, transform=PROJ, zorder=5)
    ax.plot(lon_line, meq + crest_off, color="#f1c40f", lw=1.3, ls="--", transform=PROJ, zorder=5, label="EIA crest (±15° mag)")
    ax.plot(lon_line, meq - crest_off, color="#f1c40f", lw=1.3, ls="--", transform=PROJ, zorder=5)
    ax.axhline(0, color="0.4", ls=":", lw=0.7, alpha=0.6, zorder=4)
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.82)
    cb.set_label("TEC (TECU, schematic)")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.92)
    ax.set_title("Magnetic equator + EIA crest latitudes (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.07)
    _save(fig, "fig-magnetic-equator-coast.png")


# ---------------------------------------------------------------------------
# 12. Dusk terminator + post-sunset equatorial irregularity corridor
# ---------------------------------------------------------------------------
def fig_terminator_tec_coast() -> None:
    # Africa / Atlantic / Americas dusk sector
    lon = np.linspace(-80, 40, 241)
    lat = np.linspace(-35, 35, 141)
    Lon, Lat = np.meshgrid(lon, lat)

    # Local dusk terminator near lon ≈ -10 (schematic)
    term_lon = -10.0
    # Post-sunset west of terminator: EPB / irregularity corridor
    post = 0.5 * (1 - np.tanh((Lon - term_lon) / 6))  # 1 west, 0 east
    belt = np.exp(-(np.abs(Lat) - 10) ** 2 / (2 * 8**2))
    # Longitudinal bubble modulation
    bubbles = 0.5 + 0.5 * np.sin(np.deg2rad(4 * Lon + 30)) ** 2
    irreg = 0.05 + 0.95 * post * belt * bubbles
    for lon0, lat0, amp in [(-35, 8, 0.35), (-25, -12, 0.3), (-45, 5, 0.28), (5, -6, 0.22)]:
        irreg += amp * post * np.exp(-(((Lon - lon0) / 10) ** 2 + ((Lat - lat0) / 5) ** 2))
    irreg = np.clip(irreg, 0, 1.25)

    fig = plt.figure(figsize=(9.5, 5.8))
    ax = fig.add_subplot(1, 1, 1, projection=PROJ)
    _basemap(ax, extent=[-80, 40, -35, 35])
    mesh = ax.pcolormesh(
        Lon, Lat, irreg, transform=PROJ, cmap="inferno", shading="auto",
        zorder=1, alpha=0.9, vmin=0, vmax=1.15,
    )
    # Terminator line
    ax.axvline(term_lon, color="cyan", ls="-", lw=2.0, alpha=0.85, zorder=5, label="dusk terminator")
    ax.axvline(term_lon, color="cyan", ls="-", lw=8.0, alpha=0.12, zorder=4)
    ax.text(term_lon + 2, 30, "day →", fontsize=9, color="#1a5276", transform=PROJ, zorder=5)
    ax.text(term_lon - 22, 30, "← night / EPB", fontsize=9, color="cyan", transform=PROJ, zorder=5)
    ax.axhline(0, color="white", ls="--", lw=0.7, alpha=0.5, zorder=4)
    cb = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02, shrink=0.85)
    cb.set_label("Irregularity index (schematic)")
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)
    ax.set_title("Dusk terminator + post-sunset equatorial irregularity corridor (schematic)")
    _footer(fig)
    fig.subplots_adjust(bottom=0.06)
    _save(fig, "fig-terminator-tec-coast.png")

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # First batch
    fig_vtec_global_coast()
    fig_eia_tec_map_coast()
    fig_roti_hotspots_coast()
    fig_storm_tec_diff_coast()
    fig_bubble_belt_coast()
    fig_ipp_tracks_coast()
    # Second batch
    fig_tid_wavefront_coast()
    fig_aurora_oval_coast()
    fig_eclipse_tec_hole_coast()
    fig_flare_sudden_coast()
    fig_magnetic_equator_coast()
    fig_terminator_tec_coast()
    print("done: 12 coastline basemap figures")


if __name__ == "__main__":
    main()
