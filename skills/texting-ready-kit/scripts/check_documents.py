#!/usr/bin/env python3
"""Check a filled Privacy Policy, Terms of Service and opt-in wording.

It looks for blanks that were never filled, template directions that were
left in, required lines that are missing, and contact details that do not
match between the two documents. It reads files and changes nothing.
Standard library only. No network.

Usage:
  python check_documents.py --privacy privacy-policy.md --terms terms-of-service.md
  python check_documents.py --privacy <file> --terms <file> --optin <file>

Prints DOCUMENTS OK and exits 0, or NOT READY with a list and exits 1.
Items marked [NEEDS OWNER] are listed but do not fail the check.
This is a wording check. It is not legal advice and it cannot promise
that a phone carrier will approve a registration.
"""
import argparse
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
BLANK = re.compile(r"\[([A-Z][A-Z0-9 ,'./&-]*)\]")
KEEP_IN_SAMPLES = {"OFFER", "LINK"}
DIRECTIONS = [
    (re.compile(r"\([^()]*\b[Dd]elete (these|this|if)\b[^()]*\)"), "a template direction in brackets was left in"),
    (re.compile(r"How to fill this in"), "the 'How to fill this in' part was left in"),
    (re.compile(r"=== START OF"), "the START line was left in"),
    (re.compile(r"^OPTIONAL:", re.M), "a line that starts with OPTIONAL was left in"),
]
LIST_SELLING = re.compile(r"\b(buy|bought|purchas\w*|rent\w*|sell\w*)\s+(\w+\s+){0,4}(lists?|leads)\b", re.I)
FREE_MAIL = re.compile(r"@(gmail|yahoo|hotmail|outlook|aol|icloud|live|msn)\.", re.I)
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)\(?\d{3}\)?[ .-]?\d{3}[ .-]\d{4}(?!\d)")

NEEDS = {
    "privacy": [
        (r"not\s+(be\s+)?shar\w*[^.]{0,160}third\s+parties[^.]{0,60}affiliates[^.]{0,80}(marketing|promotional)",
         "the sentence that mobile information is not shared with third parties or affiliates for marketing or promotional purposes"),
        (r"\bSTOP\b", "how to opt out with STOP"),
        (r"\bHELP\b", "how to get help with HELP"),
        (r"message and data rates may apply", "the words 'Message and data rates may apply'"),
        (r"message frequency|messages? (a|per) month", "how often messages are sent"),
    ],
    "terms": [
        (r"\bSTOP\b", "how to stop with STOP"),
        (r"\bHELP\b", "how to get help with HELP"),
        (r"message and data rates may apply", "the words 'Message and data rates may apply'"),
        (r"message frequency|messages? (a|per) month", "how often messages are sent"),
        (r"not a condition of", "that consent is not a condition of any purchase"),
        (r"carriers are not liable", "that carriers are not liable for delayed or undelivered messages"),
        (r"privacy policy", "a pointer to the Privacy Policy"),
    ],
    "optin": [
        (r"\bSTOP\b", "STOP"),
        (r"\bHELP\b", "HELP"),
        (r"message and data rates may apply", "the words 'Message and data rates may apply'"),
        (r"frequency", "message frequency"),
        (r"not a condition of", "that consent is not a condition of any purchase"),
        (r"privacy policy", "a link to the Privacy Policy"),
        (r"terms", "a link to the Terms"),
    ],
}


def internal_terms():
    src = SKILL / "references" / "sources.md"
    if not src.is_file():
        return None
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("BANNED_TERMS:"):
            terms = [t.strip() for t in line.split(":", 1)[1].split(",") if t.strip()]
            parts = []
            for t in terms:
                esc = re.escape(t).replace(r"\ ", r"[\s_-]*")
                parts.append(r"(?<![A-Za-z])%s(?![a-z])" % esc if len(t) <= 4 else esc)
            return re.compile("|".join(parts), re.I)
    return None


def check_one(kind, path, problems, open_items, rx_names):
    label = {"privacy": "Privacy Policy", "terms": "Terms", "optin": "Opt-in wording"}[kind]
    p = Path(path)
    if not p.is_file():
        problems.append("%s: file not found: %s" % (label, path))
        return ""
    text = p.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 200:
        problems.append("%s: the file is almost empty" % label)
    for m in BLANK.finditer(text):
        word = m.group(1).strip()
        if word.startswith("NEEDS OWNER"):
            open_items.append("%s: %s" % (label, m.group(0)))
        elif kind == "optin" and word in KEEP_IN_SAMPLES:
            continue
        else:
            problems.append("%s: blank not filled in: %s" % (label, m.group(0)))
    for rx, why in DIRECTIONS:
        if rx.search(text):
            problems.append("%s: %s" % (label, why))
    for pattern, what in NEEDS[kind]:
        if not re.search(pattern, text, re.I | re.S):
            problems.append("%s: missing %s" % (label, what))
    if kind == "privacy" and LIST_SELLING.search(text):
        problems.append("%s: has wording about buying, selling or renting lists. Remove it" % label)
    if FREE_MAIL.search(text):
        problems.append("%s: uses a free email address. Use an address on the business's own domain" % label)
    if rx_names:
        hit = rx_names.search(text)
        if hit:
            problems.append("%s: names something the owner should not see (%s). Say Product Champ" % (label, hit.group(0)))
    return text


def digits(found):
    return {re.sub(r"\D", "", f) for f in found}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--privacy", required=True, help="the filled Privacy Policy file")
    ap.add_argument("--terms", required=True, help="the filled Terms of Service file")
    ap.add_argument("--optin", help="the filled opt-in wording file (optional)")
    a = ap.parse_args()
    problems, open_items = [], []
    rx_names = internal_terms()
    privacy = check_one("privacy", a.privacy, problems, open_items, rx_names)
    terms = check_one("terms", a.terms, problems, open_items, rx_names)
    if a.optin:
        check_one("optin", a.optin, problems, open_items, rx_names)
    if privacy and terms:
        if {e.lower() for e in EMAIL.findall(privacy)} != {e.lower() for e in EMAIL.findall(terms)}:
            problems.append("The email addresses in the Privacy Policy and the Terms do not match")
        if digits(PHONE.findall(privacy)) != digits(PHONE.findall(terms)):
            problems.append("The phone numbers in the Privacy Policy and the Terms do not match")
    problems = list(dict.fromkeys(problems))
    open_items = list(dict.fromkeys(open_items))
    if open_items:
        print("Still open, only the owner can answer (%d):" % len(open_items))
        for item in open_items:
            print("  -", item)
    if problems:
        print("NOT READY: %d thing(s) to fix" % len(problems))
        for p in problems:
            print("  -", p)
        sys.exit(1)
    tail = ", with %d [NEEDS OWNER] item(s) still open" % len(open_items) if open_items else ""
    print("DOCUMENTS OK%s. Carriers decide approval. This is not legal advice." % tail)


if __name__ == "__main__":
    main()
