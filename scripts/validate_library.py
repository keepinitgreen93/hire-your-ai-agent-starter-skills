from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("name", "description", "version", "author", "license")
FORBIDDEN = [
    r"[A-Za-z]:[\\/]+Users[\\/]",
    r"/Users/[A-Za-z0-9_.-]+/",
    r"tam-aios",
    r"Company Brain[/\\]brain",
    r"BEGIN (RSA|OPENSSH|EC) PRIVATE KEY",
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"pit-[0-9a-f]{8}-",
    r"gravity engine",
    r"\$197",
    r"five.day|5.day",
    r"content to clients",
    "\u2014",
    "\u2013",
]


def parse_frontmatter(text):
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


errors = []
files = sorted(ROOT.glob("skills/*/SKILL.md"))
if not files:
    errors.append("No SKILL.md files found")
for path in files:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}: invalid frontmatter")
        continue
    for key in REQUIRED:
        if not fm.get(key):
            errors.append(f"{rel}: missing {key}")
    if fm.get("name") and path.parent.name != fm["name"]:
        errors.append(f"{rel}: folder/name mismatch ({fm['name']})")
    if len(fm.get("description", "")) > 60:
        errors.append(f"{rel}: description over 60 characters")
    for pattern in FORBIDDEN:
        if re.search(pattern, text, re.I):
            errors.append(f"{rel}: forbidden pattern {pattern!r}")
    if not re.search(r"\[REAL PROOF NEEDED\]|Never fabricate|Never invent", text, re.I):
        errors.append(f"{rel}: missing proof guardrail")
    if "explicit approval" not in text.lower():
        errors.append(f"{rel}: missing external-action approval gate")

if errors:
    print("VALIDATION FAILED")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"VALIDATION PASSED: {len(files)} skills")
