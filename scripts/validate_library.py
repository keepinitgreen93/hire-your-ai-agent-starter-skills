"""Check every skill in this repo before it ships.

Usage:
  python scripts/validate_library.py              check files, then run each skill's self test
  python scripts/validate_library.py --no-selftest   check files only

Standard library only. Works on Windows, macOS and Linux.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("name", "description", "version", "author", "license", "platforms")
FOLDERS = ("references", "templates", "scripts", "assets")
TEXT_TYPES = {".md", ".py", ".json", ".txt", ".html", ".yaml", ".yml", ".csv"}
INTERNAL_NAME = "sources.md"
FORBIDDEN = [
    r"[A-Za-z]:[\\/]+Users[\\/]",
    r"/Users/[A-Za-z0-9_.-]+/",
    r"/home/[A-Za-z0-9_.-]+/",
    r"tam-aios",
    r"Company Brain[/\\]brain",
    r"BEGIN (RSA|OPENSSH|EC) PRIVATE KEY",
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"pit-[0-9a-f]{8}-",
    r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}",
    r"gravity engine",
    r"\$197",
    r"five.day|5.day",
    r"content to clients",
    "\u2014",
    "\u2013",
]


def parse_frontmatter(text):
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
        m = re.match(r"^\s+related_skills:\s*\[(.*)\]\s*$", line)
        if m:
            data["related_skills"] = [s.strip() for s in m.group(1).split(",") if s.strip()]
    return data


def white_label_pattern():
    """The names that only an internal sources file may hold are read from one, never spelled out here."""
    for src in sorted(ROOT.glob("skills/*/references/" + INTERNAL_NAME)):
        for line in src.read_text(encoding="utf-8").splitlines():
            if line.startswith("BANNED_TERMS:"):
                parts = []
                for t in [t.strip() for t in line.split(":", 1)[1].split(",") if t.strip()]:
                    esc = re.escape(t).replace(r"\ ", r"[\s_-]*")
                    parts.append(r"(?<![A-Za-z])%s(?![a-z])" % esc if len(t) <= 4 else esc)
                return re.compile("|".join(parts), re.I)
    return None


errors = []
files = sorted(ROOT.glob("skills/*/SKILL.md"))
names = {p.parent.name for p in files}
master = (ROOT / "scripts" / "skill_selftest.py").read_text(encoding="utf-8").replace("\r\n", "\n")
white = white_label_pattern()
if white is None:
    errors.append("no BANNED_TERMS line found in any skills/*/references/sources.md")
if not files:
    errors.append("No SKILL.md files found")

for path in files:
    skill = path.parent
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}: invalid frontmatter")
        continue
    for key in REQUIRED:
        if not fm.get(key):
            errors.append(f"{rel}: missing {key}")
    if fm.get("name") and skill.name != fm["name"]:
        errors.append(f"{rel}: folder/name mismatch ({fm['name']})")
    desc = fm.get("description", "")
    if len(desc) > 60:
        errors.append(f"{rel}: description over 60 characters")
    if not (desc.startswith("Use when") and desc.endswith(".")):
        errors.append(f"{rel}: description must start with 'Use when' and end with a period")
    for other in fm.get("related_skills", []):
        if other not in names:
            errors.append(f"{rel}: related skill {other} is not in this repo")
    if "## What is in this skill" not in text:
        errors.append(f"{rel}: missing 'What is in this skill' section")
    if not re.search(r"\[REAL PROOF NEEDED\]|Never fabricate|Never invent", text, re.I):
        errors.append(f"{rel}: missing proof guardrail")
    if "explicit approval" not in text.lower():
        errors.append(f"{rel}: missing external-action approval gate")
    for mention in sorted(set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text))):
        if mention.endswith(("-starter", "-kit", "-loop", "-engine", "-onboarding")) and mention not in names:
            errors.append(f"{rel}: points to a skill that is not in this repo ({mention})")
    selftest = skill / "scripts" / "selftest.py"
    if not selftest.is_file():
        errors.append(f"{rel}: scripts/selftest.py is missing")
    elif selftest.read_text(encoding="utf-8").replace("\r\n", "\n") != master:
        errors.append(f"{rel}: scripts/selftest.py differs from scripts/skill_selftest.py. Copy it again")
    for f in sorted(skill.rglob("*")):
        if not f.is_file() or "__pycache__" in f.parts:
            continue
        frel = f.relative_to(ROOT).as_posix()
        inner = f.relative_to(skill).as_posix()
        if "/" in inner and inner.split("/")[0] not in FOLDERS:
            errors.append(f"{frel}: outside the standard folders ({', '.join(FOLDERS)})")
        if f.suffix.lower() not in TEXT_TYPES:
            errors.append(f"{frel}: unexpected file type in a skill")
            continue
        body = f.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN:
            if re.search(pattern, body, re.I):
                errors.append(f"{frel}: forbidden pattern {pattern!r}")
        if white and not (f.name == INTERNAL_NAME and f.parent.name == "references"):
            hit = white.search(body)
            if hit:
                errors.append(f"{frel}: names the underlying platform ({hit.group(0)}). Only references/sources.md may")

for extra in [ROOT / "README.md"]:
    body = extra.read_text(encoding="utf-8")
    for pattern in FORBIDDEN:
        if re.search(pattern, body, re.I):
            errors.append(f"{extra.name}: forbidden pattern {pattern!r}")
    if white and white.search(body):
        errors.append(f"{extra.name}: names the underlying platform. Say Product Champ")
    for name in sorted(names):
        line = f"hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/{name} --yes"
        if line not in body:
            errors.append(f"{extra.name}: missing the install line for {name}")

if not errors and "--no-selftest" not in sys.argv:
    for path in files:
        r = subprocess.run([sys.executable, str(path.parent / "scripts" / "selftest.py")], capture_output=True, text=True)
        if r.returncode != 0 or "SELFTEST PASSED" not in r.stdout:
            errors.append(f"{path.parent.name}: self test failed\n{r.stdout.strip()}\n{r.stderr.strip()}")
        else:
            print(r.stdout.strip())

if errors:
    print("VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(files)} skills")
