#!/usr/bin/env python3
"""Render the owner's readiness or setup report as one readable HTML file.

Standard library only. No network. Every text value is escaped, so raw
markdown or code never reaches the owner.

Usage:
  python build_report.py --data report-data.json --out report.html
"""
import argparse
import html
import json
import sys
from pathlib import Path

STATUSES = ["READY", "NEEDS OWNER", "BLOCKED", "CAN'T TELL"]
CSS = """
:root{--ink:#17202a;--muted:#5d6b78;--line:#dfe5ea;--bg:#f6f8fa;--ok:#1d7a46;--own:#9a5b00;--blk:#b3261e;--unk:#4a5a6a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
main{max-width:980px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:30px;line-height:1.2;margin:0 0 6px}h2{font-size:21px;margin:44px 0 12px;padding-top:18px;border-top:2px solid var(--ink)}
p{margin:0 0 12px}.meta{color:var(--muted);font-size:14px}.lead{font-size:18px;margin:18px 0 0}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0 0}
.tile{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.tile b{display:block;font-size:30px;line-height:1.1}.tile span{font-size:13px;color:var(--muted);letter-spacing:.04em}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:14.5px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}th{background:#eef2f5;font-size:12.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
tr:last-child td{border-bottom:0}.chip{display:inline-block;white-space:nowrap;font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;color:#fff}
.s0{background:var(--ok)}.s1{background:var(--own)}.s2{background:var(--blk)}.s3{background:var(--unk)}
.area{font-weight:700;white-space:nowrap}.small{color:var(--muted);font-size:13.5px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 10px}
.card h3{margin:0 0 4px;font-size:16px}.q{font-weight:700}ol,ul{margin:0 0 12px 20px;padding:0}li{margin:0 0 6px}
.note{background:#fff8e6;border:1px solid #f0dca4;border-radius:10px;padding:12px 16px;font-size:14.5px}
code{font:13px/1.4 Consolas,Menlo,monospace;background:#eef2f5;padding:1px 5px;border-radius:4px;word-break:break-all}
@media (max-width:720px){.tiles{grid-template-columns:repeat(2,1fr)}table{font-size:13.5px}}
@media print{body{background:#fff}main{padding:0}h2{break-after:avoid}tr,.card{break-inside:avoid}}
"""


def e(v):
    return html.escape("" if v is None else str(v))


def table(headers, rows_html):
    head = "".join("<th>%s</th>" % e(h) for h in headers)
    return "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, "".join(rows_html))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.loads(Path(a.data).read_text(encoding="utf-8"))
    card = d.get("scorecard") or []
    bad = [r for r in card if r.get("status") not in STATUSES]
    if bad:
        sys.exit("unknown status in scorecard: %s" % bad[0].get("status"))
    counts = {s: sum(1 for r in card if r["status"] == s) for s in STATUSES}
    setup = d.get("mode") == "setup"
    title = d.get("title") or ("Product Champ setup report" if setup else "Product Champ readiness report")
    out = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
           "<title>%s: %s</title><style>%s</style></head><body><main>" % (e(title), e(d.get("business")), CSS),
           "<p class='meta'>%s</p><h1>%s</h1><p class='meta'>%s &middot; %s</p>" % (
               e(d.get("business")), e(title), e(d.get("date")), e(d.get("prepared_by") or "Prepared by your AI assistant")),
           "<p class='lead'>%s</p>" % e(d.get("summary"))]
    out.append("<div class='tiles'>" + "".join(
        "<div class='tile'><b>%d</b><span>%s</span></div>" % (counts[s], e(s)) for s in STATUSES) + "</div>")
    if d.get("what_this_means"):
        out.append("<p class='small' style='margin-top:14px'>%s</p>" % e(d["what_this_means"]))

    if d.get("fixed"):
        out.append("<h2>What was fixed</h2><p>Each change was read back from the account after it was saved.</p>")
        out.append(table(["Setting", "Before", "After", "Where the value came from"], [
            "<tr><td class='area'>%s</td><td>%s</td><td>%s</td><td class='small'>%s</td></tr>" % (
                e(r.get("what")), e(r.get("before") or "(empty)"), e(r.get("after")), e(r.get("source"))) for r in d["fixed"]]))

    if d.get("needs_owner"):
        out.append("<h2>Questions only you can answer</h2><p>Nothing below was guessed. Each one stays as it is until you answer.</p>")
        for i, r in enumerate(d["needs_owner"], 1):
            out.append("<div class='card'><h3>%d. %s</h3><p class='small'>%s</p>%s</div>" % (
                i, e(r.get("question")), e(r.get("why")),
                ("<p class='small'>What we found: %s</p>" % e(r["found"])) if r.get("found") else ""))

    out.append("<h2>Scorecard</h2>")
    out.append(table(["Area", "Item", "Status", "What we found", "What is needed"], [
        "<tr><td class='area'>%s</td><td>%s</td><td><span class='chip s%d'>%s</span></td><td>%s</td><td>%s</td></tr>" % (
            e(r.get("area")), e(r.get("item")), STATUSES.index(r["status"]), e(r["status"]), e(r.get("detail")), e(r.get("needed")))
        for r in card]))

    if d.get("suggested"):
        out.append("<h2>Suggested, not applied</h2><p>These need a decision or a change we did not make.</p>")
        out.append(table(["Suggestion", "Why", "How"], [
            "<tr><td class='area' style='white-space:normal'>%s</td><td>%s</td><td>%s</td></tr>" % (
                e(r.get("what")), e(r.get("why")), e(r.get("how"))) for r in d["suggested"]]))

    if d.get("ready_to_turn_on"):
        out.append("<h2>Ready to turn on, needs your yes</h2><p>These were left off. Nothing here was switched on.</p>")
        out.append(table(["Item", "What it does", "Before you say yes"], [
            "<tr><td class='area' style='white-space:normal'>%s</td><td>%s</td><td>%s</td></tr>" % (
                e(r.get("item")), e(r.get("what_it_does")), e(r.get("before_yes"))) for r in d["ready_to_turn_on"]]))

    if d.get("compliance"):
        out.append("<h2>Texting and compliance steps</h2>")
        out.append(table(["Step", "Status", "Detail"], [
            "<tr><td class='area' style='white-space:normal'>%s</td><td><span class='chip s%d'>%s</span></td><td>%s</td></tr>" % (
                e(r.get("step")), STATUSES.index(r["status"]), e(r["status"]), e(r.get("detail"))) for r in d["compliance"]]))
        out.append("<p class='note' style='margin-top:12px'>Phone carriers decide whether a texting registration is approved. "
                   "Approval is never guaranteed. This report is not legal advice.</p>")

    rb = d.get("rollback")
    if rb:
        out.append("<h2>How to undo these changes</h2><p>A full copy of the settings was saved before the first change.</p>")
        out.append("<p>Backup folder: <code>%s</code></p><ol>%s</ol>" % (
            e(rb.get("backup_folder")), "".join("<li>%s</li>" % e(s) for s in rb.get("steps") or [])))

    if d.get("not_done"):
        out.append("<h2>What was not done</h2><ul>%s</ul>" % "".join("<li>%s</li>" % e(s) for s in d["not_done"]))
    if d.get("next_step"):
        out.append("<h2>Your next step</h2><p>%s</p>" % e(d["next_step"]))
    out.append("</main></body></html>")
    Path(a.out).write_text("\n".join(out), encoding="utf-8")
    print("report written:", a.out, "| scorecard:", ", ".join("%s %d" % (s, counts[s]) for s in STATUSES))


if __name__ == "__main__":
    main()
