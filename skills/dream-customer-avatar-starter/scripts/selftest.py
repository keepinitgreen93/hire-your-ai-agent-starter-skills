#!/usr/bin/env python3
"""Check that this skill folder is complete and works on this computer.

It reads only the files inside this skill's own folder. It makes no network
calls and changes nothing outside a temporary folder that it removes.
Standard library only. Works on Windows, macOS and Linux.

Usage:
  python selftest.py          run the checks
  python selftest.py --help   show this help

Prints SELFTEST PASSED and exits 0, or lists what is wrong and exits 1.
"""
import ast
import importlib.util
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
FOLDERS = ("references", "templates", "scripts", "assets")
TEXT_TYPES = {".md", ".py", ".json", ".txt", ".html", ".yaml", ".yml", ".csv"}
REQUIRED_KEYS = ("name", "description", "version", "author", "license", "platforms")
MACHINE_PATH = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]|/Users/[A-Za-z0-9_.-]+/|/home/[A-Za-z0-9_.-]+/")
LISTED_PATH = re.compile(r"`((?:references|templates|scripts|assets)/[A-Za-z0-9_./-]+)`")
LONG_DASHES = ("\u2014", "\u2013")


def frontmatter(text):
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    data = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip().strip("\"'")
    return data


def skill_files():
    out = []
    for f in sorted(SKILL.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
            out.append(f)
    return out


def banned_terms():
    src = SKILL / "references" / "sources.md"
    if not src.is_file():
        return src, []
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("BANNED_TERMS:"):
            return src, [t.strip() for t in line.split(":", 1)[1].split(",") if t.strip()]
    return src, []


def term_pattern(terms):
    parts = []
    for t in terms:
        esc = re.escape(t).replace(r"\ ", r"[\s_-]*")
        parts.append(r"(?<![A-Za-z])%s(?![a-z])" % esc if len(t) <= 4 else esc)
    return re.compile("|".join(parts), re.I)


def check(problems):
    main_file = SKILL / "SKILL.md"
    if not main_file.is_file():
        problems.append("SKILL.md is missing")
        return 0
    text = main_file.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        problems.append("SKILL.md has no valid frontmatter block")
        fm = {}
    for key in REQUIRED_KEYS:
        if not fm.get(key):
            problems.append("frontmatter is missing %s" % key)
    desc = fm.get("description", "")
    if len(desc) > 60:
        problems.append("description is %d characters, the limit is 60" % len(desc))
    if desc and not (desc.startswith("Use when") and desc.endswith(".")):
        problems.append("description must start with 'Use when' and end with a period")
    if "## What is in this skill" not in text:
        problems.append("SKILL.md has no 'What is in this skill' section")

    files = skill_files()
    names = {f.relative_to(SKILL).as_posix() for f in files}
    docs = [f for f in files if f.suffix == ".md"]
    for doc in docs:
        for rel in sorted(set(LISTED_PATH.findall(doc.read_text(encoding="utf-8")))):
            if rel.rstrip("/.") not in names and not (SKILL / rel).is_dir():
                problems.append("%s mentions %s, which is not in this skill folder" % (doc.name, rel))
    for rel in sorted(names):
        if rel.split("/")[0] in FOLDERS and rel not in text:
            problems.append("%s is in the folder but not listed in SKILL.md" % rel)
        if "/" in rel and rel.split("/")[0] not in FOLDERS:
            problems.append("%s is outside the standard folders (%s)" % (rel, ", ".join(FOLDERS)))

    internal, terms = banned_terms()
    rx = term_pattern(terms) if terms else None
    for f in files:
        if f.suffix.lower() not in TEXT_TYPES:
            continue
        body = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(SKILL).as_posix()
        if MACHINE_PATH.search(body):
            problems.append("%s holds a path from one person's computer" % rel)
        if any(d in body for d in LONG_DASHES):
            problems.append("%s holds a long dash" % rel)
        if rx and f.resolve() != internal.resolve():
            hit = rx.search(body)
            if hit:
                problems.append("%s names something only the internal sources file may name (%s)" % (rel, hit.group(0)))

    std = getattr(sys, "stdlib_module_names", None)
    local = {f.stem for f in files if f.suffix == ".py"}
    for f in files:
        if f.suffix != ".py":
            continue
        rel = f.relative_to(SKILL).as_posix()
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError as err:
            problems.append("%s does not parse: %s" % (rel, err))
            continue
        if std is None:
            continue
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module]
            for mod in mods:
                top = mod.split(".")[0]
                if top not in std and top not in local:
                    problems.append("%s needs %s, which does not come with Python" % (rel, top))
    return len(files)


def run_extra(problems):
    extra = Path(__file__).resolve().parent / "selftest_extra.py"
    if not extra.is_file():
        return
    spec = importlib.util.spec_from_file_location("selftest_extra", extra)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        mod.main()
    except AssertionError as err:
        problems.append("helper test failed: %s" % (err or "an expected result did not match"))
    except SystemExit as err:
        if err.code not in (0, None):
            problems.append("helper test stopped: %s" % err.code)
    except Exception as err:
        problems.append("helper test crashed: %s: %s" % (type(err).__name__, err))


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip())
        return
    problems = []
    count = check(problems)
    if not problems:
        run_extra(problems)
    if problems:
        print("SELFTEST FAILED: %s" % SKILL.name)
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("SELFTEST PASSED: %s, %d files checked" % (SKILL.name, count))


if __name__ == "__main__":
    main()
