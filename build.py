#!/usr/bin/env python3
"""
Generate radar.csv for Thoughtworks' Build Your Own Radar (BYOR) from Markdown entries.

Layout:
    quadrants/<quadrant-folder>/<entry>.md

Each entry has simple frontmatter followed by a Markdown body:

    ---
    name: Kubernetes
    ring: adopt          # adopt | trial | assess | hold
    ---
    Why it's in this ring, when to avoid it, alternatives...

The quadrant comes from the folder. The body becomes the BYOR description
(converted to HTML). A `description:` field in the frontmatter can be used
instead of a body for one-liners.

`isNew` and `status` are not authored by hand. The previous radar.csv is used
as the baseline: an entry that was not in it is `New`; an entry whose ring moved
towards the centre is `Moved In`; towards the edge is `Moved Out`; otherwise
`No Change`. Delete radar.csv to treat every entry as new.

Usage:
    python build.py            # writes radar.csv
    python build.py --check    # validate only, exit non-zero on problems
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUADRANTS_DIR = ROOT / "quadrants"
OUTPUT = ROOT / "radar.csv"

# Folder name -> quadrant name in the CSV. Order here is the intended quadrant order.
# These match the names radar.thoughtworks.com expects; change them freely if you
# self-host BYOR with custom quadrant names.
QUADRANTS = {
    "techniques": "techniques",
    "tools": "tools",
    "platforms": "platforms",
    "languages-and-framework": "languages & frameworks",
}

# Ring order, innermost first. BYOR accepts "hold" and displays it as "Caution".
RINGS = ["adopt", "trial", "assess", "hold"]

# BYOR's optional movement column. Index into RINGS gives the direction: a lower
# index is closer to the centre.
NEW = "New"
MOVED_IN = "Moved In"
MOVED_OUT = "Moved Out"
NO_CHANGE = "No Change"
STATUSES = [NEW, MOVED_IN, MOVED_OUT, NO_CHANGE]

@dataclass
class Entry:
    path: Path
    name: str
    ring: str
    quadrant: str
    description: str
    status: str = NO_CHANGE

    @property
    def is_new(self) -> bool:
        return self.status == NEW


class EntryError(Exception):
    pass


# --- parsing -----------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)(.*)\Z", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse simple `key: value` frontmatter. Deliberately not full YAML."""
    match = FRONTMATTER_RE.match(text.replace("\r\n", "\n"))
    if not match:
        raise EntryError("missing frontmatter (file must start with a '---' block)")

    raw, body = match.groups()
    fields: dict[str, str] = {}
    for lineno, line in enumerate(raw.splitlines(), start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise EntryError(f"frontmatter line {lineno} is not 'key: value': {line!r}")
        key, value = stripped.split(":", 1)
        value = value.strip()
        # Strip trailing comments on unquoted values.
        if value and value[0] not in "\"'":
            value = value.split(" #", 1)[0].strip()
        # Strip matching quotes.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields, body.strip()


def markdown_to_html(text: str) -> str:
    """Use the `markdown` package if installed, otherwise a minimal fallback."""
    if not text:
        return ""
    try:
        import markdown  # type: ignore
    except ImportError:
        markdown = None

    if markdown is not None:
        return markdown.markdown(text, extensions=["sane_lists"]).strip()

    # Fallback: paragraphs, **bold**, *italic*, `code` and [links](url).
    def inline(s: str) -> str:
        s = html.escape(s, quote=False)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return "".join(f"<p>{inline(' '.join(p.split()))}</p>" for p in paragraphs)


def load_entry(path: Path, quadrant: str) -> Entry:
    fields, body = parse_frontmatter(path.read_text(encoding="utf-8"))

    name = fields.get("name", "").strip()
    if not name:
        raise EntryError("missing 'name'")

    ring = fields.get("ring", "").strip().lower()
    if not ring:
        raise EntryError("missing 'ring'")
    if ring not in RINGS:
        raise EntryError(f"invalid ring {ring!r} (expected one of: {', '.join(RINGS)})")

    if "isNew" in fields or "status" in fields:
        raise EntryError("isNew and status are derived from radar.csv; remove them")

    fm_description = fields.get("description", "").strip()
    if fm_description and body:
        raise EntryError("has both a 'description' field and a body; use one")
    description = markdown_to_html(body or fm_description)
    if not description:
        raise EntryError("no description (add a body or a 'description' field)")

    return Entry(path, name, ring, quadrant, description)


# --- change detection ---------------------------------------------------------


def load_baseline(path: Path) -> dict[str, str]:
    """Read the previous CSV as {name_lower: ring}. Missing file means no baseline."""
    if not path.is_file():
        return {}
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            baseline: dict[str, str] = {}
            for row in reader:
                name = (row.get("name") or "").strip().lower()
                ring = (row.get("ring") or "").strip().lower()
                if name:
                    baseline[name] = ring
            return baseline
    except (OSError, csv.Error, UnicodeDecodeError):
        return {}


def assign_status(entries: list[Entry], baseline: dict[str, str]) -> None:
    """Set each entry's status by comparing its ring to the baseline.

    A missing baseline (no previous radar.csv) makes every entry new.
    """
    for entry in entries:
        previous = baseline.get(entry.name.lower())
        if previous not in RINGS:
            entry.status = NEW
            continue
        old, new = RINGS.index(previous), RINGS.index(entry.ring)
        if new < old:
            entry.status = MOVED_IN
        elif new > old:
            entry.status = MOVED_OUT
        else:
            entry.status = NO_CHANGE


# --- main --------------------------------------------------------------------


def collect_entries() -> tuple[list[Entry], list[str]]:
    errors: list[str] = []
    entries: list[Entry] = []

    if not QUADRANTS_DIR.is_dir():
        return [], [f"{QUADRANTS_DIR.relative_to(ROOT)}/ not found"]

    for folder in sorted(p for p in QUADRANTS_DIR.iterdir() if p.is_dir()):
        if folder.name not in QUADRANTS:
            errors.append(
                f"quadrants/{folder.name}/: unknown quadrant folder "
                f"(expected one of: {', '.join(QUADRANTS)})"
            )
            continue
        for path in sorted(folder.glob("*.md")):
            try:
                entries.append(load_entry(path, QUADRANTS[folder.name]))
            except EntryError as exc:
                errors.append(f"{path.relative_to(ROOT)}: {exc}")

    stray = [p for p in QUADRANTS_DIR.glob("*.md")]
    for path in stray:
        errors.append(f"{path.relative_to(ROOT)}: entries must live in a quadrant folder")

    # Duplicate names (case-insensitive), across all quadrants.
    seen: dict[str, Path] = {}
    for entry in entries:
        key = entry.name.lower()
        if key in seen:
            errors.append(
                f"{entry.path.relative_to(ROOT)}: duplicate name {entry.name!r} "
                f"(also in {seen[key].relative_to(ROOT)})"
            )
        else:
            seen[key] = entry.path

    # BYOR needs all four quadrants to have at least one blip.
    used = {e.quadrant for e in entries}
    missing = [q for q in QUADRANTS.values() if q not in used]
    if entries and missing:
        errors.append(f"BYOR needs entries in all four quadrants; empty: {', '.join(missing)}")
    if not entries and not errors:
        errors.append("no entries found under quadrants/")

    return entries, errors


def sort_key(entry: Entry) -> tuple[int, int, str]:
    # BYOR draws rings (and quadrants) in the order they first appear in the data,
    # so sort by ring first to guarantee adopt is innermost and hold is outermost.
    quadrant_order = list(QUADRANTS.values())
    return (RINGS.index(entry.ring), quadrant_order.index(entry.quadrant), entry.name.lower())


def write_csv(entries: list[Entry], output: Path) -> None:
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(["name", "ring", "quadrant", "isNew", "status", "description"])
        for e in sorted(entries, key=sort_key):
            writer.writerow(
                [e.name, e.ring, e.quadrant, "TRUE" if e.is_new else "FALSE", e.status, e.description]
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a BYOR CSV from Markdown entries.")
    parser.add_argument("--check", action="store_true", help="validate only; don't write the CSV")
    parser.add_argument("-o", "--output", type=Path, default=OUTPUT, help="output path (default: radar.csv)")
    args = parser.parse_args()

    entries, errors = collect_entries()
    if errors:
        print(f"Found {len(errors)} problem(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if args.check:
        print(f"OK: {len(entries)} entries are valid.")
        return 0

    baseline = load_baseline(args.output)
    assign_status(entries, baseline)
    write_csv(entries, args.output)

    rings = {r: sum(e.ring == r for e in entries) for r in RINGS}
    ring_summary = ", ".join(f"{n} {r}" for r, n in rings.items() if n)
    changes = {s: sum(e.status == s for e in entries) for s in STATUSES}
    change_summary = ", ".join(f"{n} {s.lower()}" for s, n in changes.items() if n)
    if not baseline:
        change_summary += " (no previous radar.csv)"
    print(f"Wrote {len(entries)} entries to {args.output.name} ({ring_summary}; {change_summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
