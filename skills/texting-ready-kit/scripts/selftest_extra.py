#!/usr/bin/env python3
"""Extra checks for the Texting Ready Kit, run by selftest.py.

Fills the three templates with a made-up sample business in a temporary
folder, then proves check_documents.py passes the filled files and catches
the unfilled ones. No network. Standard library only.

Usage: python selftest.py   (this file is loaded by it)
"""
import importlib.util
import io
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
DISCLAIMER = "This template is a starting point, not legal advice. Have an attorney review it for your state and industry."
SAMPLE = {
    "LEGAL BUSINESS NAME": "Sunny Day Landscaping LLC",
    "DBA NAME": "Sunny Day Landscaping",
    "BUSINESS NAME": "Sunny Day Landscaping",
    "WEBSITE URL": "https://www.sunnyday-landscaping.example",
    "PRIVACY POLICY URL": "https://www.sunnyday-landscaping.example/privacy-policy",
    "TERMS URL": "https://www.sunnyday-landscaping.example/terms",
    "BUSINESS ADDRESS": "100 Garden Way, Springfield, IL 62701",
    "BUSINESS PHONE": "(217) 555-0142",
    "BUSINESS EMAIL": "hello@sunnyday-landscaping.example",
    "EFFECTIVE DATE": "January 5, 2027",
    "STATE": "Illinois",
    "MESSAGE FREQUENCY": "Message frequency varies. You may get up to 8 messages a month.",
}


def run(script, *args):
    """Run one helper in this process and capture what it prints."""
    spec = importlib.util.spec_from_file_location(script[:-3], HERE / script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    old_argv, old_out = sys.argv, sys.stdout
    sys.argv, sys.stdout = [str(HERE / script)] + [str(a) for a in args], io.StringIO()
    code = 0
    try:
        mod.main()
    except SystemExit as e:
        if isinstance(e.code, str):
            sys.stdout.write(e.code)
            code = 1
        else:
            code = e.code or 0
    finally:
        out = sys.stdout.getvalue()
        sys.argv, sys.stdout = old_argv, old_out
    return code, out


def fill(text, start_marker=None):
    text = text.replace("\r\n", "\n")
    if start_marker and start_marker in text:
        text = text.split(start_marker, 1)[1]
        text = text.split("\n", 1)[1]
    text = re.sub(r"\([^()]*\b[Dd]elete\b[^()]*\)", "", text)
    text = "\n".join(l for l in text.split("\n") if not l.startswith("OPTIONAL:"))
    return re.sub(r"\[([A-Z][A-Z0-9 ,'./&-]*)\]", lambda m: SAMPLE.get(m.group(1), "sample text"), text)


def main():
    owner_files = [
        "templates/privacy-policy-template.md", "templates/terms-of-service-template.md",
        "templates/opt-in-form-language.md", "references/hermes-prompts.md", "references/presubmit-checklist.md",
    ]
    for rel in owner_files:
        assert DISCLAIMER in (SKILL / rel).read_text(encoding="utf-8"), "the disclaimer line is missing from %s" % rel
    head = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for must in ("never guaranteed", "not legal advice", "explicit approval", "Do not submit during a trial by default"):
        assert must in head, "SKILL.md lost a required safety line: %s" % must

    with tempfile.TemporaryDirectory(prefix="trk-selftest-") as tmp:
        root = Path(tmp)
        raw = {n: (SKILL / "templates" / n).read_text(encoding="utf-8") for n in (
            "privacy-policy-template.md", "terms-of-service-template.md", "opt-in-form-language.md")}
        privacy, terms, optin = root / "privacy-policy.md", root / "terms-of-service.md", root / "opt-in.md"
        privacy.write_text(fill(raw["privacy-policy-template.md"], "=== START OF POLICY ==="), encoding="utf-8")
        terms.write_text(fill(raw["terms-of-service-template.md"], "=== START OF TERMS ==="), encoding="utf-8")
        optin.write_text(fill(raw["opt-in-form-language.md"]), encoding="utf-8")

        code, out = run("check_documents.py", "--privacy", privacy, "--terms", terms, "--optin", optin)
        assert code == 0 and "DOCUMENTS OK" in out, "filled sample documents should pass:\n" + out

        unfilled = root / "unfilled.md"
        unfilled.write_text(raw["privacy-policy-template.md"], encoding="utf-8")
        code, out = run("check_documents.py", "--privacy", unfilled, "--terms", terms)
        assert code == 1 and "blank not filled in" in out, "an unfilled template must be caught"

        open_item = root / "open.md"
        open_item.write_text(privacy.read_text(encoding="utf-8") + "\nRetention: [NEEDS OWNER]\n", encoding="utf-8")
        code, out = run("check_documents.py", "--privacy", open_item, "--terms", terms)
        assert code == 0 and "NEEDS OWNER" in out, "a NEEDS OWNER item must be listed without failing"

        wrong = root / "wrong.md"
        wrong.write_text(terms.read_text(encoding="utf-8").replace("(217) 555-0142", "(217) 555-0199"), encoding="utf-8")
        code, out = run("check_documents.py", "--privacy", privacy, "--terms", wrong)
        assert code == 1 and "do not match" in out, "different phone numbers must be caught"

        shared = root / "shared.md"
        shared.write_text(privacy.read_text(encoding="utf-8") + "\nWe may sell our customer lists to partners.\n", encoding="utf-8")
        code, out = run("check_documents.py", "--privacy", shared, "--terms", terms)
        assert code == 1 and "lists" in out, "list selling wording must be caught"

        code, out = run("whitelabel_lint.py", privacy, terms, optin)
        assert code == 0 and "CLEAN" in out, "sample documents must pass the white label check:\n" + out
        terms_line = [l for l in (SKILL / "references" / "sources.md").read_text(encoding="utf-8").splitlines()
                      if l.startswith("BANNED_TERMS:")]
        assert terms_line, "the internal sources file lost its BANNED_TERMS line"
        first = terms_line[0].split(":", 1)[1].split(",")[0].strip()
        dirty = root / "dirty.md"
        dirty.write_text("Log in to %s to continue." % first, encoding="utf-8")
        code, out = run("whitelabel_lint.py", dirty)
        assert code == 1, "the white label check must catch a banned name"
        code, out = run("whitelabel_lint.py", SKILL)
        assert code == 0, "files outside the internal sources file must be clean:\n" + out


if __name__ == "__main__":
    main()
    print("EXTRA CHECKS PASSED")
