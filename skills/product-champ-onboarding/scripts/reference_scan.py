#!/usr/bin/env python3
"""Find what each workflow needs from the account, and what is missing.

Reads a folder of read-only exports saved by the agent. Makes no network calls
and changes nothing. Standard library only.

Expected layout (file names are matched loosely):
  custom-values*.json     list of {name, fieldKey, value}
  custom-fields*.json     list of {id, name, fieldKey}
  calendars.json pipelines.json forms.json surveys.json users.json links*.json
  workflows/<id>.json           one workflow document (name, status, steps)
  workflows/<id>.triggers.json  optional trigger list for that workflow
  <any folder with "template" in its name>/<id>.json|.html   message bodies

Usage:
  python reference_scan.py --inventory <folder> --out <result.json>
"""
import argparse
import json
import re
import sys
from pathlib import Path

TAG = re.compile(r"\{\{\s*([a-zA-Z_]+)\.([a-zA-Z0-9_.]+)\s*\}\}")
STANDARD_CONTACT = {
    "id", "name", "first_name", "last_name", "full_name", "email", "phone", "phone_raw",
    "company_name", "full_address", "address1", "city", "state", "country", "postal_code",
    "timezone", "date_of_birth", "source", "website", "tags", "type", "date_added",
}
PLACEHOLDER = re.compile(
    r"(\[[A-Z][^\]]*\]|\{\{|\byour[ _-](business|company|name|phone|email|website|link|url|logo)\b|"
    r"example\.com|lorem ipsum|\btbd\b|placeholder|xxxx|555[-. ]?01\d{2}|123[-. ]456[-. ]7890|"
    r"insert here|change me|coming soon)", re.I)
ID_KEYS = {
    "template_id": "template", "pipeline_id": "pipeline", "pipeline_stage_id": "stage",
    "workflow_id": "workflow", "calendar_id": "calendar", "calendarId": "calendar",
    "form_id": "form", "formId": "form", "survey_id": "survey", "userId": "user",
    "user_id": "user", "assigned_to": "user", "assignedTo": "user",
}
COND_FIELDS = {
    "form.id": "form", "survey.id": "survey", "calendar.id": "calendar", "link.id": "link",
    "workflow.id": "workflow", "opportunity.pipelineId": "pipeline",
    "opportunity.pipelineStageId": "stage", "contact.customFields": "custom_field",
}


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def rows(obj, want):
    """Find the first list of dicts that carries the wanted key, at any depth."""
    if isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj) and any(want in x for x in obj):
            return obj
        for x in obj:
            r = rows(x, want)
            if r:
                return r
    elif isinstance(obj, dict):
        for v in obj.values():
            r = rows(v, want)
            if r:
                return r
    return []


def collect_ids(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("id", "_id") and isinstance(v, str):
                out.add(v)
            collect_ids(v, out)
    elif isinstance(obj, list):
        for x in obj:
            collect_ids(x, out)


def norm_key(field_key):
    k = re.sub(r"[{}\s]", "", field_key or "")
    return k.split(".", 1)[1] if "." in k else k


def value_state(v):
    if v is None or (isinstance(v, str) and not v.strip()):
        return "blank"
    if isinstance(v, str) and PLACEHOLDER.search(v):
        return "placeholder"
    return "filled"


def walk_ids(obj, found):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ID_KEYS and isinstance(v, str) and v:
                found.append((ID_KEYS[k], v))
            walk_ids(v, found)
    elif isinstance(obj, list):
        for x in obj:
            walk_ids(x, found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inv = Path(a.inventory)
    if not inv.is_dir():
        sys.exit("inventory folder not found")

    cv_rows, cf_rows = [], []
    for p in sorted(inv.glob("custom-values*.json")):
        cv_rows = cv_rows or rows(load(p), "fieldKey")
    for p in sorted(inv.glob("custom-fields*.json")):
        cf_rows = cf_rows or rows(load(p), "fieldKey")
    cant_tell = []
    if not cv_rows:
        cant_tell.append("custom values export missing or unreadable")
    if not cf_rows:
        cant_tell.append("custom fields export missing or unreadable")

    # A blank value is often returned with no "value" key at all. Trust that only
    # when at least one other record in the same export does carry the key.
    cv_has_value_key = any("value" in r for r in cv_rows)
    values = {}
    for r in cv_rows:
        key = norm_key(r.get("fieldKey"))
        state = value_state(r.get("value"))
        if state == "blank" and "value" not in r and not cv_has_value_key:
            state = "cant_tell"
        values[key] = {"key": key, "name": r.get("name"), "id": r.get("id"), "state": state,
                       "used_by": [], "used_live": False}
    fields_by_key = {norm_key(r.get("fieldKey")): r for r in cf_rows}
    field_ids = {r.get("id") for r in cf_rows if r.get("id")}

    known = {"calendar": set(), "pipeline": set(), "stage": set(), "form": set(), "survey": set(),
             "user": set(), "link": set(), "workflow": set(), "custom_field": set(field_ids)}
    readable = set()
    for kind, pattern in (("calendar", "calendars.json"), ("form", "forms.json"), ("survey", "surveys.json"),
                          ("user", "users.json"), ("link", "*links*.json")):
        for p in inv.glob(pattern):
            data = load(p)
            if data is not None and not (isinstance(data, dict) and (data.get("_isError") or data.get("error"))):
                collect_ids(data, known[kind])
                readable.add(kind)
    for p in inv.glob("pipelines.json"):
        data = load(p)
        for pl in rows(data, "stages"):
            known["pipeline"].add(pl.get("id"))
            for s in pl.get("stages") or []:
                known["stage"].add(s.get("id"))
        readable.update(("pipeline", "stage"))

    templates = {}
    for d in inv.iterdir():
        if d.is_dir() and "template" in d.name.lower():
            for p in d.iterdir():
                if p.suffix.lower() in (".json", ".html", ".txt"):
                    text = p.read_text(encoding="utf-8", errors="replace")
                    missing = p.suffix == ".json" and bool(re.search(r'"_httpError"|does not exist', text, re.I))
                    templates[p.stem] = {"text": text, "missing": missing}

    wf_dir = inv / "workflows"
    wf_files = [p for p in sorted(wf_dir.glob("*.json")) if not p.name.endswith(".triggers.json")] if wf_dir.is_dir() else []
    if not wf_files:
        cant_tell.append("workflow steps could not be read, so which values each workflow needs is unknown")
    for p in wf_files:
        known["workflow"].add(p.stem)
    readable.add("workflow")

    workflows, missing_templates, dangling, unknown_fields = [], {}, {}, {}
    for p in wf_files:
        doc = load(p) or {}
        name = doc.get("name") or p.stem
        status = (doc.get("status") or "unknown").lower()
        live = status == "published"
        text = json.dumps(doc)
        trig = load(wf_dir / (p.stem + ".triggers.json"))
        trig_list = trig if isinstance(trig, list) else rows(trig, "type") if trig else []
        text += json.dumps(trig_list)
        ids = []
        walk_ids(doc, ids)
        for t in trig_list:
            for c in t.get("conditions") or []:
                f, v = c.get("field"), c.get("value")
                if f in COND_FIELDS and isinstance(v, str):
                    ids.append((COND_FIELDS[f], v))
                m = re.fullmatch(r"contact\.([A-Za-z0-9]{18,24})", f or "")
                if m:
                    ids.append(("custom_field", m.group(1)))
        issues = []
        for kind, ident in ids:
            if kind == "template":
                t = templates.get(ident)
                if t is None:
                    continue  # body not exported: cannot judge
                if t["missing"]:
                    missing_templates.setdefault(ident, []).append({"workflow": name, "status": status})
                    issues.append("step points at a message template that no longer exists")
                else:
                    text += t["text"]
            elif not re.fullmatch(r"[A-Za-z0-9-]{8,40}", ident):
                continue  # a merge tag or keyword, not a record id
            elif kind in readable and ident not in known[kind]:
                dangling.setdefault((kind, ident), []).append({"workflow": name, "status": status})
                issues.append("points at a %s that was not found in this account" % kind.replace("_", " "))
        used_values, blank_values = set(), set()
        for ns, rest in TAG.findall(text):
            ns = ns.lower()
            if ns in ("custom_values", "custom_value"):
                key = rest.split(".")[0]
                used_values.add(key)
                rec = values.get(key)
                if rec is None:
                    values[key] = rec = {"key": key, "name": None, "id": None, "state": "not_defined",
                                         "used_by": [], "used_live": False}
                if not any(u["workflow"] == name for u in rec["used_by"]):
                    rec["used_by"].append({"workflow": name, "status": status})
                rec["used_live"] = rec["used_live"] or live
                if rec["state"] != "filled":
                    blank_values.add(key)
            elif ns == "contact":
                key = rest.split(".")[0]
                if key not in STANDARD_CONTACT and key not in fields_by_key and cf_rows:
                    unknown_fields.setdefault(key, []).append({"workflow": name, "status": status})
        trig_active = [bool(t.get("active")) for t in trig_list]
        workflows.append({"id": p.stem, "name": name, "status": status,
                          "triggers": len(trig_list), "active_triggers": sum(trig_active),
                          "custom_values_used": sorted(used_values), "values_not_ready": sorted(blank_values),
                          "issues": sorted(set(issues))})

    # other settings exports (links, calendars, forms) can also depend on custom values
    for p in sorted(inv.glob("*.json")):
        if p.name.startswith(("custom-values", "custom-fields", "MANIFEST")):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for ns, rest in set(TAG.findall(text)):
            if ns.lower() in ("custom_values", "custom_value"):
                key = rest.split(".")[0]
                rec = values.setdefault(key, {"key": key, "name": None, "id": None, "state": "not_defined",
                                              "used_by": [], "used_live": False})
                rec["used_by"].append({"workflow": "settings file: " + p.stem, "status": "other"})

    # duplicates: same normalized label under different keys
    by_label = {}
    for v in values.values():
        if v["name"]:
            label = re.sub(r"^[a-z]\s*-\s*[a-z ]*:\s*|^[a-z]+\s*-\s*", "", v["name"].strip().lower())
            by_label.setdefault(re.sub(r"[^a-z0-9]+", " ", label).strip(), []).append(v["key"])
    duplicates = [ks for ks in by_label.values() if len(ks) > 1]

    need = [v for v in values.values() if v["used_by"] and v["state"] != "filled"]
    need.sort(key=lambda v: (not v["used_live"], -len(v["used_by"]), v["key"]))
    result = {
        "summary": {
            "workflows_read": len(workflows),
            "workflows_live": sum(w["status"] == "published" for w in workflows),
            "custom_values_total": len([v for v in values.values() if v["state"] != "not_defined"]),
            "custom_values_blank": sum(v["state"] == "blank" for v in values.values()),
            "custom_values_placeholder": sum(v["state"] == "placeholder" for v in values.values()),
            "values_needed_by_live_workflows": sum(v["used_live"] for v in need),
            "values_needed_by_drafts_or_other_settings": sum(not v["used_live"] for v in need),
            "blank_and_unused": sum(1 for v in values.values() if v["state"] == "blank" and not v["used_by"]),
            "missing_templates": len(missing_templates),
            "dangling_ids": len(dangling),
            "unknown_contact_fields": len(unknown_fields),
            "live_workflows_not_ready": sum(1 for w in workflows if w["status"] == "published" and (w["values_not_ready"] or w["issues"])),
        },
        "cant_tell": cant_tell,
        "must_fill": need,
        "custom_values": sorted(values.values(), key=lambda v: v["key"]),
        "duplicates": duplicates,
        "missing_templates": [{"template_id": k, "used_by": v} for k, v in missing_templates.items()],
        "dangling_ids": [{"kind": k[0], "id": k[1], "used_by": v} for k, v in dangling.items()],
        "unknown_contact_fields": [{"key": k, "used_by": v} for k, v in unknown_fields.items()],
        "workflows": workflows,
    }
    Path(a.out).write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result["summary"], indent=1))
    for line in cant_tell:
        print("CAN'T TELL:", line)


if __name__ == "__main__":
    main()
