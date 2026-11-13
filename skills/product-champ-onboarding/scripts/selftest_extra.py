#!/usr/bin/env python3
"""Extra checks for Product Champ Onboarding, run by selftest.py.

Builds a made-up sample account in a temporary folder, then checks the scan,
the backup check, the report and the white label check.
No network, no account access. Standard library only.

Usage: python selftest.py   (this file is loaded by it)
"""
import importlib.util
import io
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent


class Result:
    def __init__(self, code, out):
        self.returncode, self.stdout, self.stderr = code, out, out


def run(script, *args):
    """Run one helper in this same process and capture what it prints."""
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
    return Result(code, out)


def main():
    with tempfile.TemporaryDirectory(prefix="pco-selftest-") as tmp:
        root = Path(tmp)
        inv = root / "inventory"
        (inv / "workflows").mkdir(parents=True)
        (inv / "templates").mkdir()
        w = lambda name, obj: (inv / name).write_text(json.dumps(obj), encoding="utf-8")
        w("business-profile.json", {"location": {"name": "Sunny Day Landscaping", "timezone": "America/Chicago"}})
        w("custom-values.json", {"customValues": [
            {"id": "v1", "name": "Business Short Name", "fieldKey": "{{ custom_values.business_short_name }}"},
            {"id": "v2", "name": "Main Phone", "fieldKey": "{{ custom_values.main_phone }}", "value": "(555) 201-7788"},
            {"id": "v3", "name": "Booking Link", "fieldKey": "{{ custom_values.booking_link }}", "value": "[YOUR LINK]"},
            {"id": "v4", "name": "Unused Banner", "fieldKey": "{{ custom_values.unused_banner }}"}]})
        w("custom-fields.json", {"customFields": [{"id": "f1aaaaaaaaaaaaaaaaaa", "name": "Yard Size", "fieldKey": "contact.yard_size"}]})
        w("calendars.json", {"calendars": [{"id": "cal12345678", "name": "Estimate Visit"}]})
        w("pipelines.json", {"pipelines": [{"id": "pipe1234567", "name": "Leads", "stages": [{"id": "stage123456", "name": "New"}]}]})
        w("links.json", {"links": [{"id": "link1234567", "redirectTo": "{{ custom_values.review_link }}"}]})
        w("workflows/wf-live-0001.json", {"name": "Missed call text back", "status": "published", "workflowData": {"templates": [
            {"id": "a1", "type": "sms", "attributes": {"body": "Hi from {{custom_values.business_short_name}}. Book here: {{ custom_values.booking_link }} Yard: {{contact.yard_size}} {{contact.first_name}}"}},
            {"id": "a2", "type": "sms", "attributes": {"template_id": "tplgone00001"}},
            {"id": "a3", "type": "create_opportunity", "attributes": {"pipeline_id": "pipezzzzzzz", "pipeline_stage_id": "stage123456"}}]}})
        w("workflows/wf-live-0001.triggers.json", [{"type": "call_status", "active": True, "conditions": []}])
        w("workflows/wf-draft-0002.json", {"name": "Holiday note", "status": "draft", "workflowData": {"templates": [
            {"id": "b1", "type": "email", "attributes": {"template_id": "tplok0000001", "html": "{{custom_values.main_phone}} {{contact.shoe_size}}"}}]}})
        w("templates/tplgone00001.json", {"_httpError": 400, "_body": "Template does not exist"})
        w("templates/tplok0000001.json", {"template": {"body": "Call {{custom_values.main_phone}}"}})

        r = run("reference_scan.py", "--inventory", inv, "--out", root / "scan.json")
        assert r.returncode == 0, r.stderr
        scan = json.loads((root / "scan.json").read_text(encoding="utf-8"))
        need = {v["key"]: v for v in scan["must_fill"]}
        assert need["business_short_name"]["state"] == "blank" and need["business_short_name"]["used_live"]
        assert need["booking_link"]["state"] == "placeholder"
        assert need["review_link"]["state"] == "not_defined"
        assert "main_phone" not in need and "unused_banner" not in need
        assert scan["must_fill"][0]["used_live"], "live items must come first"
        assert scan["summary"]["missing_templates"] == 1
        assert any(d["kind"] == "pipeline" for d in scan["dangling_ids"])
        assert [u["key"] for u in scan["unknown_contact_fields"]] == ["shoe_size"]
        assert scan["summary"]["live_workflows_not_ready"] == 1

        assert run("backup_check.py", inv).returncode == 0
        (inv / "custom-values.json").write_text("", encoding="utf-8")
        bad = run("backup_check.py", inv)
        assert bad.returncode == 1 and "NOT OK" in bad.stdout

        report = root / "report.html"
        r = run("build_report.py", "--data", SKILL / "templates" / "report-data.example.json", "--out", report)
        assert r.returncode == 0, r.stderr
        page = report.read_text(encoding="utf-8")
        assert "<table>" in page and "NEEDS OWNER" in page and "**" not in page and "\n# " not in page

        assert run("whitelabel_lint.py", report).returncode == 0, "report must be clean"
        terms = [l for l in (SKILL / "references" / "sources.md").read_text(encoding="utf-8").splitlines() if l.startswith("BANNED_TERMS:")]
        first = terms[0].split(":", 1)[1].split(",")[0].strip()
        dirty = root / "dirty.html"
        dirty.write_text("<p>Log in to %s to continue.</p>" % first, encoding="utf-8")
        assert run("whitelabel_lint.py", dirty).returncode == 1, "lint must catch a banned term"
        whole = run("whitelabel_lint.py", SKILL)
        assert whole.returncode == 0, "skill files outside the internal file must be clean:\n" + whole.stdout

        head = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        desc = re.search(r"^description:\s*(.+)$", head, re.M).group(1).strip().strip("\"'")
        assert len(desc) <= 60 and desc.endswith("."), "description must be 60 characters or fewer"
        for f in SKILL.rglob("*"):
            if f.is_file() and f.suffix in (".md", ".py", ".json"):
                text = f.read_text(encoding="utf-8")
                assert "\u2014" not in text and "\u2013" not in text, "long dash found in %s" % f.name


if __name__ == "__main__":
    main()
    print("EXTRA CHECKS PASSED")
