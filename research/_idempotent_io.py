"""Idempotent file helpers for research merge/apply pipelines.

When ADDED=0 (or content unchanged), callers should skip rewriting
lists/*, docs/categories.md, NOTES.md, PROJECTS.json. README count
sync stays in sync_readme_counts (already write-if-changed).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_text_if_changed(path: Path, text: str, *, encoding: str = "utf-8") -> bool:
    """Write text only if different from on-disk content. Returns True if wrote."""
    if not text.endswith("\n"):
        text = text + "\n"
    previous = path.read_text(encoding=encoding) if path.exists() else None
    if previous == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding)
    return True


def write_json_if_changed(path: Path, obj: Any, *, encoding: str = "utf-8") -> bool:
    """Dump JSON (indent=2, ensure_ascii=False, trailing newline) only if changed."""
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    return write_text_if_changed(path, text, encoding=encoding)


def append_notes_section(notes_path: Path, heading: str, body: str, *, encoding: str = "utf-8") -> bool:
    """Append a NOTES section once. Skip if ``heading`` already appears in the file.

    ``heading`` should be the markdown H2 line, e.g. ``## 例行检索补录（2026-09-23）``.
    ``body`` is the rest of the section (may start with blank lines); trailing
    whitespace is normalized.
    """
    heading = heading.strip()
    existing = notes_path.read_text(encoding=encoding) if notes_path.exists() else ""
    if heading in existing:
        return False
    block = body.strip("\n")
    if not block.startswith(heading):
        block = heading + "\n\n" + block
    new_text = existing.rstrip() + "\n\n" + block + "\n"
    notes_path.write_text(new_text, encoding=encoding)
    return True


def projects_substantively_equal(a: list[dict], b: list[dict]) -> bool:
    """Deep-compare project lists (JSON-stable, order-insensitive by url/name)."""

    def key(p: dict) -> tuple:
        return (str(p.get("url") or ""), str(p.get("name") or ""))

    sa = sorted(a, key=key)
    sb = sorted(b, key=key)
    return json.dumps(sa, ensure_ascii=False, sort_keys=True) == json.dumps(
        sb, ensure_ascii=False, sort_keys=True
    )
