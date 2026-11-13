#!/usr/bin/env python3
"""Extra checks for Company Brain Starter, run by selftest.py.

Builds a made-up sample Company Brain in a temporary folder and proves the
builder behaves: the plan creates nothing, a build without approval is
refused, an approved build creates the folders, the check catches a file
that is too big, and the export leaves out media and secrets.
No network, no Git needed. Standard library only.

Usage: python selftest.py   (this file is loaded by it)
"""
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(*args):
    """Run the builder in this process and capture what it prints."""
    spec = importlib.util.spec_from_file_location("scaffold_brain", HERE / "scaffold_brain.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    old = sys.argv, sys.stdout, sys.stderr
    sys.argv = [str(HERE / "scaffold_brain.py")] + [str(a) for a in args]
    sys.stdout = sys.stderr = io.StringIO()
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
        sys.argv, sys.stdout, sys.stderr = old
    return code, out


def main():
    with tempfile.TemporaryDirectory(prefix="brain-selftest-") as tmp:
        root = Path(tmp)
        answers = root / "answers.json"
        answers.write_text(json.dumps({
            "business_name": "Sunny Day Landscaping", "what_sells": "Lawn care", "serves": "Homeowners",
            "clients": ["Maple HOA", "Rivera Family"], "personal": True, "cloud": "google-drive",
            "users": "just-me", "goals": ["Spring campaign", "Referral offer", "Hire crew"],
            "tools": {"email": "Email"}}), encoding="utf-8")
        parent = root / "Documents"
        base = ["--answers", answers, "--parent", parent]

        code, out = run("plan", *base)
        assert code == 0 and "Company Brain" in out, "the plan step failed:\n" + out
        assert not parent.exists(), "the plan step created folders"

        code, out = run("build", *base)
        assert code != 0 and not parent.exists(), "a build without approval must be refused"

        code, out = run("build", *base, "--approved")
        assert code == 0, "the approved build failed:\n" + out
        brain = parent / "Company Brain"
        for rel in ("BRAIN-GUIDE.md", "SYNC.md", ".gitignore", "brain/_index.md", "brain/business/overview.md"):
            assert (brain / rel).is_file(), "the build did not create %s" % rel
        assert (parent / "Deliverables").is_dir(), "the Deliverables folder is missing"
        pointers = list((brain / "workspace").rglob("README.md"))
        assert pointers, "no project pointer files were created"
        for p in pointers:
            rel = p.parent.relative_to(brain / "workspace")
            assert ("Deliverables/%s/" % rel.as_posix()) in p.read_text(encoding="utf-8"), "a pointer file does not name its Deliverables folder"

        code, out = run("check", "--brain", brain)
        assert code == 0, "a fresh Brain should pass the check:\n" + out
        (brain / "dummy.mp4").write_text("dummy", encoding="utf-8")
        (brain / ".env").write_text("dummy", encoding="utf-8")
        (brain / "oversized.md").write_bytes(b"x" * (6 * 1024 * 1024))
        code, out = run("check", "--brain", brain)
        assert code != 0, "the check must catch a video, a secret file and a note that is too big"

        export = root / "snapshot"
        code, out = run("export", "--brain", brain, "--destination", export)
        assert code == 0, "the export failed:\n" + out
        assert (export / "brain" / "business" / "overview.md").is_file(), "the export left out the notes"
        for name in ("dummy.mp4", ".env", "oversized.md"):
            assert not (export / name).exists(), "the export copied %s" % name


if __name__ == "__main__":
    main()
    print("EXTRA CHECKS PASSED")
