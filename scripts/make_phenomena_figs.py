#!/usr/bin/env python3
"""Regenerate CC0 ionosphere-phenomena teaching figures into docs/tutorials/images/."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'docs' / 'tutorials' / 'images'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.size': 11, 'axes.titlesize': 13, 'figure.dpi': 160, 'savefig.dpi': 160, 'axes.unicode_minus': False})

def main():
    lat = np.linspace(-60, 60, 400)
    day = 18 + 22*np.exp(-((lat-15)/12)**2) + 22*np.exp(-((lat+15)/12)**2) + 8*np.exp(-(lat/40)**2)
    night = 6 + 5*np.exp(-((lat-12)/18)**2) + 5*np.exp(-((lat+12)/18)**2)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.fill_between(lat, 0, day, color='#ffb347', alpha=0.35, label='Day')
    ax.plot(lat, day, color='#e67e22', lw=2.2)
    ax.fill_between(lat, 0, night, color='#5dade2', alpha=0.35, label='Night')
    ax.plot(lat, night, color='#2874a6', lw=2.2)
    ax.axvline(0, color='k', ls=':', lw=1)
    ax.set_xlim(-60, 60); ax.set_ylim(0, 55)
    ax.set_xlabel('Magnetic latitude (°)'); ax.set_ylabel('VTEC (TECU, schematic)')
    ax.set_title('Day / Night TEC vs latitude (EIA twin peaks)')
    ax.legend(loc='upper right'); ax.grid(True, alpha=0.25)
    fig.tight_layout(); fig.savefig(OUT/'fig-tec-day-night.png'); plt.close()

    x = np.linspace(-30, 30, 300); y = np.linspace(-20, 20, 200)
    X, Y = np.meshgrid(x, y)
    Z = 30*np.exp(-(X/25)**2)*np.exp(-((Y-2)/14)**2)
    for cx, cy, a, b in [(-8, 3, 3.2, 7), (-2, 1, 2.5, 6), (5, 2.5, 3.5, 8), (12, 0.5, 2.2, 5)]:
        Z *= 1 - 0.85*np.exp(-((X-cx)/a)**2 - ((Y-cy)/b)**2)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='magma', aspect='auto', vmin=0, vmax=35)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02).set_label('VTEC (TECU)')
    ax.set_xlabel('Longitude offset (°)'); ax.set_ylabel('Latitude offset (°)')
    ax.set_title('Equatorial plasma bubbles → TEC depletions')
    fig.tight_layout(); fig.savefig(OUT/'fig-scintillation-bubbles.png'); plt.close()

    xg = np.linspace(0, 2000, 400); tg = np.linspace(0, 120, 240)
    XG, TG = np.meshgrid(xg, tg)
    res = 2.5*np.sin(2*np.pi*(XG/450 - TG/35))*np.exp(-((TG-50)/55)**2)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    im = ax.imshow(res, extent=[0, 2000, 0, 120], origin='lower', aspect='auto', cmap='RdBu_r', vmin=-3, vmax=3)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02).set_label('ΔTEC (TECU)')
    ax.set_xlabel('Horizontal distance (km)'); ax.set_ylabel('Time (min)')
    ax.set_title('TID wavefronts in TEC residual field')
    fig.tight_layout(); fig.savefig(OUT/'fig-tid-wavefront.png'); plt.close()

    h = np.linspace(60, 600, 500)
    def chapman(hh, hmax, Nm, H):
        z = (hh-hmax)/H
        return Nm*np.exp(0.5*(1 - z - np.exp(-z)))
    Ne = chapman(h, 110, 1.2e11, 15) + chapman(h, 220, 4e11, 35) + chapman(h, 320, 1.1e12, 55)
    fig, ax = plt.subplots(figsize=(5.2, 6))
    ax.plot(Ne/1e12, h, color='#1abc9c', lw=2.5)
    ax.fill_betweenx(h, 0, Ne/1e12, color='#1abc9c', alpha=0.2)
    ax.set_xlabel(r'$N_e$ ($10^{12}$ m$^{-3}$)'); ax.set_ylabel('Altitude (km)')
    ax.set_title('Electron density profile (D/E/F)')
    ax.set_ylim(60, 600); ax.set_xlim(0, 1.4)
    for y0, y1, lab, c in [(60, 90, 'D', '#95a5a6'), (90, 140, 'E', '#3498db'), (140, 600, 'F', '#9b59b6')]:
        ax.axhspan(y0, y1, color=c, alpha=0.08)
        ax.text(1.25, (y0+y1)/2, lab, va='center', ha='center', fontsize=14, color=c, fontweight='bold')
    ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT/'fig-ne-profile-layers.png'); plt.close()

    t = np.linspace(-30, 90, 400)
    quiet = np.full_like(t, 12.0)
    flare = 12 + 22*(1/(1+np.exp(-(t-1)/1.2)))*np.exp(-np.clip(t,0,None)/18)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, quiet, '--', color='gray', lw=1.8, label='Quiet')
    ax.plot(t, flare, color='#c0392b', lw=2.4, label='Flare')
    ax.fill_between(t, quiet, flare, where=flare>quiet, color='#e74c3c', alpha=0.25)
    ax.axvline(0, color='orange', ls=':', label='X-ray onset')
    ax.set_xlabel('Minutes relative to flare peak'); ax.set_ylabel('VTEC / absorption proxy')
    ax.set_title('Solar flare sudden ionospheric effect')
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT/'fig-flare-sudden-ionize.png'); plt.close()

    t = np.arange(0, 180, 1)
    rng = np.random.default_rng(3)
    quiet_r = 0.15 + 0.05*rng.standard_normal(len(t))
    storm_r = quiet_r.copy(); storm_r[60:120] += 0.9*np.abs(np.sin(np.linspace(0, 4*np.pi, 60))) + 0.3*rng.random(60)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(t, np.clip(quiet_r,0,None), color='#27ae60', lw=1.6, label='Quiet ROTI')
    ax.plot(t, np.clip(storm_r,0,None), color='#8e44ad', lw=1.8, label='Disturbed ROTI')
    ax.set_xlabel('Time (min)'); ax.set_ylabel('ROTI (TECU/min)')
    ax.set_title('ROTI: quiet vs disturbed')
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(OUT/'fig-roti-time-series.png'); plt.close()

    fig, axes = plt.subplots(1, 4, figsize=(12, 2.8))
    axes[0].plot(lat, day, color='#e67e22'); axes[0].plot(lat, night, color='#2874a6')
    axes[0].set_title('Day/Night'); axes[0].set_xticks([]); axes[0].set_yticks([])
    axes[1].imshow(Z, cmap='magma', aspect='auto'); axes[1].set_title('Bubbles'); axes[1].axis('off')
    axes[2].imshow(res, cmap='RdBu_r', aspect='auto'); axes[2].set_title('TID'); axes[2].axis('off')
    axes[3].plot(Ne/1e12, h, color='#1abc9c'); axes[3].set_title('Ne profile'); axes[3].set_xticks([]); axes[3].set_yticks([])
    fig.suptitle('Ionosphere phenomena gallery (CC0 schematics)', y=1.05)
    fig.tight_layout(); fig.savefig(OUT/'fig-phenomena-gallery.png', bbox_inches='tight'); plt.close()
    print('wrote figures to', OUT)

if __name__ == '__main__':
    main()
