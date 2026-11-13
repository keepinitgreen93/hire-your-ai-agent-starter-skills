#!/usr/bin/env python3
"""Confirm a backup folder is complete enough to allow a write.

Usage:
  python backup_check.py <backup-folder> [--allow-missing workflows]
Prints BACKUP OK and exits 0, or lists what is wrong and exits 1.
Standard library only. Reads files, changes nothing.
"""
import json
import sys
from pathlib import Path

REQUIRED = ["business-profile", "custom-values", "custom-fields", "calendars"]


def is_error(text):
    head = text[:600]
    flat = head.replace(" ", "")
    return any(k in flat for k in ('"_isError"', '"_httpError"', '"_exception"', '"success":false'))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    allow = sys.argv[sys.argv.index("--allow-missing") + 1].split(",") if "--allow-missing" in sys.argv else []
    if not args:
        sys.exit(__doc__)
    root = Path(args[0])
    problems = []
    if not root.is_dir():
        sys.exit("NOT OK: folder not found")
    for name in REQUIRED:
        found = sorted(root.glob(name + "*.json"))
        if not found:
            problems.append("missing %s export" % name)
            continue
        f = found[0]
        text = f.read_text(encoding="utf-8", errors="replace")
        if f.stat().st_size < 20:
            problems.append("%s is empty" % f.name)
        elif is_error(text):
            problems.append("%s holds an error, not data" % f.name)
        else:
            try:
                json.loads(text)
            except Exception:
                problems.append("%s is not valid JSON" % f.name)
    wf = root / "workflows"
    docs = [p for p in wf.glob("*.json") if not p.name.endswith(".triggers.json")] if wf.is_dir() else []
    if not docs and "workflows" not in allow:
        problems.append("no workflow documents saved. If they cannot be read, do not edit workflows, and pass --allow-missing workflows")
    for p in docs:
        if p.stat().st_size < 20 or is_error(p.read_text(encoding="utf-8", errors="replace")):
            problems.append("workflow %s is empty or an error" % p.stem)
    total = sum(1 for p in root.rglob("*") if p.is_file())
    if problems:
        print("NOT OK: do not write anything yet")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("BACKUP OK: %d files, %d workflow documents, required exports readable" % (total, len(docs)))


if __name__ == "__main__":
    main()
