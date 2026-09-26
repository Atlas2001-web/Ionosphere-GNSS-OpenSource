"""Shared field-merge helpers for catalog merge/apply pipelines.

EXISTING-ENTRY RULE (batch 47, hardened at the root)
----------------------------------------------------
Once a project is in PROJECTS.json, its curated fields belong to QC, not to
the finds file it was originally ingested from. Stale finds files
(routine_finds_*.json, similar_finds.json, more_finds.json, new_finds.json,
web_finds.json, ...) still carry pre-QC provenance / license / language /
blurbs; re-running their merge scripts must NOT revert QC decisions.

Therefore, for an entry that ALREADY exists in the catalog:
  * a PROTECTED field (see PROTECTED_FIELDS) is only written when the stored
    value is a gap -- key missing or blank string ""; a non-empty stored
    value is NEVER overwritten -- no rank "upgrades" (provenance), no
    "stronger" license, no "richer" Chinese blurb, no category/url moves;
  * an explicit JSON ``null`` on an existing entry is a QC verdict, not a
    gap (convention since batch 41: ``license: null`` = verified no licence
    / not determinable, ``language: null`` = website/data, no code), so it
    is also never filled -- e.g. PPP-Wizard license null must not become
    "see upstream" again;
  * placeholder values ("see upstream README", "unspecified", NOASSERTION,
    ...) never fill anything, even a real gap;
  * to change a curated field on an existing entry, edit PROJECTS.json in a
    QC commit -- not by editing a finds file and re-running a merge.

NEW entries (norm_url not yet in the catalog) are unaffected: merge scripts
build them from the finds record with full values, as before.

RETIRED URLS: entries QC removed or merged into another entry (and old URLs
that QC rewrote) are listed in RETIRED_URLS; merge scripts must skip them
when adding "new" entries (``is_retired(url)``), otherwise a stale finds
file silently re-adds a deleted/merged project.

Interface is unchanged: ``merge_project_fields(existing, incoming, *,
fields=None) -> list[str]`` and ``prefer_enrichment_value(field, old, new)``.
Scripts that write existing entries without these helpers must use
``set_if_empty`` (or equivalent) for PROTECTED_FIELDS.
"""
from __future__ import annotations

from typing import Any, Iterable

# QC / enrichment fields that routine merges must not wipe (kept for callers).
ENRICHMENT_FIELDS: tuple[str, ...] = (
    "license",
    "language",
    "provenance",
    "desc_zh",
    "one_liner_zh",
    "analysis_zh",
)

# Structural fields owned by QC once an entry exists: fill-if-empty only.
FILL_IF_EMPTY_FIELDS: tuple[str, ...] = (
    "host",
    "category",
    "subcategory",
    "url",
)

# Every field covered by the existing-entry rule.
PROTECTED_FIELDS: tuple[str, ...] = ENRICHMENT_FIELDS + FILL_IF_EMPTY_FIELDS


_PLACEHOLDERS = {
    "noassertion",
    "none",
    "unknown",
    "unspecified",
    "n/a",
    "na",
    "null",
    "other",
    "see upstream",
    "see-upstream",
    "seeupstream",
    "see upstream readme",
    "see readme",
}


# norm_url (rstrip("/").lower()) -> why it is no longer a catalog URL.
RETIRED_URLS: dict[str, str] = {
    "https://igs.bkg.bund.de/root_ftp/ntrip/software/caster": "merged into BKG-NtripCaster (batch 43)",
    "https://www.gfz.de/en/section/space-geodetic-techniques/overview/details-section-news/veroeffentlichung-der-software-for-precise-orbit-and-clock-combination-spocc-1": "merged into SPOCC (batch 43)",
    "https://lists.igs.org/pipermail/igsmail/2025/008556.html": "merged into SPOCC (batch 43)",
    "https://github.com/ohm1122/ionex-downloader": "removed: empty repository (0472f42)",
    "https://github.com/gnssnexus/rinex": "retired URL (QC)",
    "https://github.com/ohm1122/ionkit-nh": "retired URL (QC)",
    "https://github.com/ohm1122/oasis": "retired URL (QC)",
    "http://geoweb.mit.edu/gg": "URL rewritten by QC",
    "http://software.rtcm-ntrip.org/wiki/bns": "URL rewritten by QC",
    "http://software.rtcm-ntrip.org/wiki/ntripclient": "URL rewritten by QC",
    "http://software.rtcm-ntrip.org/wiki/ntripserver": "URL rewritten by QC",
    "http://software.rtcm-ntrip.org": "URL rewritten by QC",
    "http://software.rtcm-ntrip.org/wiki/rtcm3torinex": "URL rewritten by QC",
    "https://github.com/stenseng/biscef": "URL rewritten by QC",
    "https://seemala.blogspot.com/2024/04/gps-tec-analysis-program-version-35.html": "URL rewritten by QC",
    "https://github.com/yxw027/segmentscomputation": "URL rewritten by QC",
    "http://www.ep.sci.hokudai.ac.jp/~heki/software.htm": "URL rewritten by QC",
    "https://www.aiub.unibe.ch/download": "URL rewritten by QC (batch 54: permanent redirect, CODE-AIUB-Product-Download)",
    "https://www.epncb.oma.be": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-CB)",
    "https://epncb.oma.be/ftp/obs": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-Obs-FTP)",
    "https://isdc.gfz-potsdam.de": "URL rewritten by QC (batch 54: permanent redirect, GFZ-ISDC)",
    "https://isdc.gfz-potsdam.de/gnss-products": "URL rewritten by QC (batch 54: permanent redirect, GFZ-ISDC-GNSS-Products)",
    "https://kp.gfz-potsdam.de/en": "URL rewritten by QC (batch 54: permanent redirect, GFZ-Kp-Index)",
    "https://www.swpc.noaa.gov": "URL rewritten by QC (batch 54: permanent redirect, NOAA-SWPC)",
    "https://www.swpc.noaa.gov/products/planetary-k-index": "URL rewritten by QC (batch 54: permanent redirect, NOAA-SWPC-Planetary-K)",
    "https://www.unavco.org/software": "URL rewritten by QC (batch 54: permanent redirect, UNAVCO-Software-Portal)",
    "https://www.intermagnet.org": "URL rewritten by QC (batch 54: permanent redirect, INTERMAGNET)",
    "https://magnetometers.bc.edu": "URL rewritten by QC (batch 54: permanent redirect, AMBER-Magnetometers)",
    "https://openmadrigal.org": "URL rewritten by QC (batch 54: permanent redirect, OpenMadrigal)",
    "https://www.ga.gov.au/scientific-topics/positioning-navigation/geodesy/auspos": "URL rewritten by QC (batch 54: permanent redirect, AUSPOS)",
    "https://www.enri.go.jp/eng/index.html": "URL rewritten by QC (batch 54: permanent redirect, ENRI-Japan)",
    "https://www.icao.int/safety/pbn/pages/overview.aspx": "URL rewritten by QC (batch 54: permanent redirect, ICAO-PBN)",
    "https://igs.org/wg/bias": "URL rewritten by QC (batch 54: permanent redirect, IGS-Bias-Calibration-WG)",
    "https://www.ngdc.noaa.gov/geomag/wmm": "URL rewritten by QC (batch 54: permanent redirect, NOAA-WMM-Portal)",
    "https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap": "URL rewritten by QC (batch 54: permanent redirect, SWPC-D-RAP)",
    "https://www.swpc.noaa.gov/products/wsa-enlil-solar-wind-prediction": "URL rewritten by QC (batch 54: permanent redirect, SWPC-WSA-Enlil)",
    "https://www.swpc.noaa.gov/products/goes-x-ray-flux": "URL rewritten by QC (batch 54: permanent redirect, SWPC-GOES-Xray)",
    "https://www.swpc.noaa.gov/products/solar-cycle-progression": "URL rewritten by QC (batch 54: permanent redirect, SWPC-Solar-Cycle)",
    "https://kp.gfz-potsdam.de/en/data": "URL rewritten by QC (batch 54: permanent redirect, GFZ-Kp-Data)",
    "https://www.ngdc.noaa.gov/geomag/geomag.shtml": "URL rewritten by QC (batch 54: permanent redirect, NGDC-Geomagnetism)",
    "https://www.swpc.noaa.gov/products/ace-real-time-solar-wind": "URL rewritten by QC (batch 54: permanent redirect, SWPC-ACE-RTSW)",
    "https://www.ngdc.noaa.gov/stp/satellite/goes": "URL rewritten by QC (batch 54: permanent redirect, NGDC-GOES-Satellite)",
    "https://www.swpc.noaa.gov/products/real-time-solar-wind": "URL rewritten by QC (batch 54: permanent redirect, SWPC-Real-Time-Solar-Wind)",
    "https://www.swpc.noaa.gov/products/goes-proton-flux": "URL rewritten by QC (batch 54: permanent redirect, SWPC-GOES-Proton-Flux)",
    "https://www.epncb.oma.be/_productsservices/troposphere": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-Troposphere)",
    "https://www.epncb.oma.be/_networkdata/data_access": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-Data-Access)",
    "https://www.ngdc.noaa.gov/geomag/emm": "URL rewritten by QC (batch 54: permanent redirect, NOAA-EMM)",
    "https://www.psmsl.org": "URL rewritten by QC (batch 54: permanent redirect, PSMSL)",
    "https://www.swpc.noaa.gov/products/solar-synoptic-map": "URL rewritten by QC (batch 54: permanent redirect, SWPC-Solar-Synoptic-Map)",
    "https://www.swpc.noaa.gov/products/solar-and-geophysical-event-reports": "URL rewritten by QC (batch 54: permanent redirect, SWPC-Solar-Geophysical-Event-Reports)",
    "https://www.epncb.oma.be/_networkdata/stationlist.php": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-StationList)",
    "https://www.epncb.oma.be/_productsservices/coordinates": "URL rewritten by QC (batch 54: permanent redirect, EUREF-EPN-Coordinates)",
    "https://egnos-user-support.essp-sas.eu": "removed: pure duplicate of EGNOS-GSC-User-Support (301 -> egnos.gsc-europa.eu, batch 54)",
    "https://github.com/w2naf/darntids": "URL rewritten by QC (batch 64: repo deprecated, README points to successor w2naf-academia/DARNtids)",
    "https://github.com/sgl-ut/gpstk": "removed: pure duplicate of gnsstk (archived; README says renamed to GNSSTK and split into gnsstk + gnsstk-apps, batch 64)",
    "https://github.com/kristinemlarson/gnssir_python": "removed: pure duplicate of gnssrefl (archived; README says deprecated, use gnssrefl instead, batch 64)",
}


def is_retired(url: Any) -> bool:
    """True if ``url`` was removed/merged/rewritten by QC; do not re-add it."""
    return isinstance(url, str) and url.rstrip("/").lower() in RETIRED_URLS


def _is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() in _PLACEHOLDERS


def _is_gap(existing: dict, field: str) -> bool:
    """True if ``field`` on an existing entry may be filled (missing or "")."""
    if field not in existing:
        return True
    v = existing[field]
    return isinstance(v, str) and not v.strip()


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, dict, tuple)) and not value:
        return True
    return False


def prefer_enrichment_value(field: str, old: Any, new: Any) -> Any:
    """Value to keep for ``field`` on an EXISTING catalog entry.

    Existing ``old`` always wins unless it is a blank string and ``new`` is
    a real (non-placeholder) value. ``old is None`` is treated as a QC
    verdict and kept. (``field`` is accepted for interface compatibility;
    callers that cannot distinguish "missing" from ``None`` should use
    ``merge_project_fields`` / ``set_if_empty`` instead.)
    """
    if isinstance(old, str) and not old.strip() and not _is_empty(new) and not _is_placeholder(new):
        return new
    return old


def set_if_empty(existing: dict, field: str, value: Any) -> bool:
    """Write ``value`` into ``existing[field]`` only if the field is a gap.

    Gap = key missing or blank string. ``None`` (QC verdict) and any
    non-empty value are kept; empty/placeholder ``value`` never writes.

    Returns True if the entry changed. For use by scripts that assign fields
    on existing entries directly instead of via ``merge_project_fields``.
    """
    if _is_gap(existing, field) and not _is_empty(value) and not _is_placeholder(value):
        existing[field] = value
        return True
    return False


def merge_project_fields(
    existing: dict,
    incoming: dict,
    *,
    fields: Iterable[str] | None = None,
) -> list[str]:
    """Merge fields from ``incoming`` into the EXISTING entry, in place.

    Only fields present as keys in ``incoming`` are considered; each is
    fill-if-empty (see module docstring). Returns the list of changed fields.
    """
    use_fields = tuple(fields) if fields is not None else PROTECTED_FIELDS
    changed: list[str] = []
    for field in use_fields:
        if field not in incoming:
            continue
        if set_if_empty(existing, field, incoming.get(field)):
            changed.append(field)
    return changed
