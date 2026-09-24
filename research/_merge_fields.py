"""Shared field-merge helpers for catalog merge/apply pipelines.

Hard rule: never let empty/weak incoming values overwrite non-empty
enrichment already on an existing PROJECTS.json entry (license,
language, provenance, Chinese blurbs). Stronger/non-empty incoming
may still fill gaps or upgrade weak values.
"""
from __future__ import annotations

from typing import Any, Iterable

# QC / enrichment fields that routine merges must not wipe.
ENRICHMENT_FIELDS: tuple[str, ...] = (
    "license",
    "language",
    "provenance",
    "desc_zh",
    "one_liner_zh",
    "analysis_zh",
)

# Optional structural fields: fill-if-empty only (never clobber).
FILL_IF_EMPTY_FIELDS: tuple[str, ...] = (
    "host",
)

_PROVENANCE_RANK = {
    "personal_community": 1,
    "academic_lab": 2,
    "official": 3,
}

_WEAK_LICENSE = {
    "",
    "noassertion",
    "none",
    "unknown",
    "n/a",
    "na",
    "null",
    "see upstream",
    "see-upstream",
    "seeupstream",
}


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _license_rank(value: Any) -> int:
    if _is_empty(value):
        return 0
    s = str(value).strip()
    if s.lower() in _WEAK_LICENSE:
        return 1
    return 3  # SPDX / concrete license string


def _provenance_rank(value: Any) -> int:
    if _is_empty(value):
        return 0
    return _PROVENANCE_RANK.get(str(value).strip(), 1)


def _zh_rank(value: Any) -> int:
    if _is_empty(value):
        return 0
    return len(str(value).strip())


def prefer_enrichment_value(field: str, old: Any, new: Any) -> Any:
    """Choose the value to keep for an enrichment field.

    Hard rule: empty/weak ``new`` never replaces non-empty ``old``.
    When both are usable, prefer the richer / higher-rank value; for
    Chinese blurbs, prefer existing QC text when both are non-trivial.
    """
    if field == "license":
        if _license_rank(new) > _license_rank(old):
            return new
        return old if not _is_empty(old) else new

    if field == "provenance":
        # Never downgrade (e.g. official → personal_community).
        if _provenance_rank(new) > _provenance_rank(old):
            return new
        return old if not _is_empty(old) else new

    if field in ("desc_zh", "one_liner_zh", "analysis_zh"):
        if _is_empty(new):
            return old
        if _is_empty(old):
            return new
        # Both non-empty: keep existing QC unless it is trivially short
        # (placeholder) and incoming is clearly richer.
        old_s, new_s = str(old).strip(), str(new).strip()
        if _zh_rank(old_s) < 8 and _zh_rank(new_s) > _zh_rank(old_s):
            return new_s
        return old

    if field in ("language", "host"):
        if _is_empty(new):
            return old
        if _is_empty(old):
            return new
        return old  # both set: keep existing

    # Default: never empty-overwrite; otherwise keep old when both set.
    if _is_empty(new):
        return old
    if _is_empty(old):
        return new
    return old


def merge_project_fields(
    existing: dict,
    incoming: dict,
    *,
    fields: Iterable[str] | None = None,
) -> list[str]:
    """Merge enrichment fields from ``incoming`` into ``existing`` in-place.

    Only fields present as keys in ``incoming`` are considered. Returns the
    list of field names whose stored value changed.
    """
    use_fields = tuple(fields) if fields is not None else (ENRICHMENT_FIELDS + FILL_IF_EMPTY_FIELDS)
    changed: list[str] = []
    for field in use_fields:
        if field not in incoming:
            continue
        old = existing.get(field) if field in existing else None
        new = incoming.get(field)
        kept = prefer_enrichment_value(field, old, new)
        if field not in existing:
            if _is_empty(kept):
                continue
            existing[field] = kept
            changed.append(field)
            continue
        if kept != existing.get(field):
            existing[field] = kept
            changed.append(field)
    return changed
