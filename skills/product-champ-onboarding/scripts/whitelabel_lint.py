#!/usr/bin/env python3
"""Check owner-facing files for platform names that must never be shown.

The banned terms live only in the internal file references/sources.md, on the
line that starts with BANNED_TERMS:. This script reads them from there, so no
other file in this skill has to spell them out.

Usage:
  python whitelabel_lint.py <file-or-folder> [more paths]
  python whitelabel_lint.py --text "a chat reply to check"
Exit code 0 means clean. Exit code 1 means at least one banned term was found.
"""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
INTERNAL = SKILL / "references" / "sources.md"
TEXT_TYPES = {".html", ".htm", ".md", ".txt", ".json", ".csv", ".py", ".yaml", ".yml"}


def banned_terms():
    for line in INTERNAL.read_text(encoding="utf-8").splitlines():
        if line.startswith("BANNED_TERMS:"):
            return [t.strip() for t in line.split(":", 1)[1].split(",") if t.strip()]
    sys.exit("BANNED_TERMS line not found in references/sources.md")


def pattern(terms):
    parts = []
    for t in terms:
        esc = re.escape(t).replace(r"\ ", r"[\s_-]*")
        parts.append(r"(?<![A-Za-z])%s(?![a-z])" % esc if len(t) <= 4 else esc)
    return re.compile("|".join(parts), re.I)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    rx = pattern(banned_terms())
    hits = []
    if args[0] == "--text":
        for m in rx.finditer(" ".join(args[1:])):
            hits.append(("(text)", 0, m.group(0)))
    else:
        files = []
        for a in args:
            p = Path(a)
            files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]
        for f in files:
            if f.resolve() == INTERNAL.resolve() or f.suffix.lower() not in TEXT_TYPES:
                continue
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for m in rx.finditer(line):
                    hits.append((str(f), n, m.group(0)))
    if hits:
        print("NOT CLEAN: %d banned term(s) found" % len(hits))
        for f, n, w in hits[:40]:
            print("  %s:%s  %s" % (f, n, w))
        sys.exit(1)
    print("CLEAN: no banned platform terms found")


if __name__ == "__main__":
    main()
