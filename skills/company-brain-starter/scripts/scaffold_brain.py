#!/usr/bin/env python3
"""Company Brain scaffold: plan, build, and check.

Used by the company-brain-starter skill AFTER the owner has answered the
interview and approved the folder plan. Standard library only.

  python scaffold_brain.py plan  --answers answers.json --parent <folder>
  python scaffold_brain.py build --answers answers.json --parent <folder>
  python scaffold_brain.py check --brain <Company Brain folder>

The script never reads or writes anything outside --parent (build) or --brain (check).
It never overwrites an existing file. It never asks for or stores passwords.
"""
import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

VAULT = "Company Brain"
DELIV = "Deliverables"
PERSONAL_VAULT = "Personal Brain"
LIMIT_BYTES = 5 * 1024 * 1024

BLOCKED_EXT = (
    "mp4 mov avi mkv webm m4v wmv flv mpg mpeg "
    "mp3 wav m4a aac flac ogg opus aiff "
    "png jpg jpeg gif webp heic heif svg bmp tif tiff psd ai raw "
    "pdf zip 7z rar tar gz tgz bz2 iso dmg exe msi "
    "ppt pptx key "
    "pem key p12 pfx"
).split()
BLOCKED_EXT = sorted(set(BLOCKED_EXT))

CLOUDS = {
    "google-drive": "Google Drive",
    "onedrive": "OneDrive",
    "dropbox": "Dropbox",
    "icloud": "iCloud Drive",
    "github": "a private GitHub repository (Obsidian Git)",
    "obsidian-sync": "Obsidian Sync",
    "none": "no cloud yet",
}


def slug(text, max_words=5):
    words = re.findall(r"[a-z0-9]+", str(text).lower())
    return "-".join(words[:max_words]) or "untitled"


def load_answers(path):
    a = json.loads(Path(path).read_text(encoding="utf-8"))
    a.setdefault("clients", [])
    a.setdefault("personal", False)
    a.setdefault("cloud", "none")
    a.setdefault("users", "just-me")  # just-me | my-devices | other-people
    a.setdefault("goals", [])
    a.setdefault("tools", {})
    a.setdefault("never_say", "")
    a["clients"] = [c for c in a["clients"] if str(c).strip()]
    a["goals"] = [g for g in a["goals"] if str(g).strip()][:3]
    if a["cloud"] not in CLOUDS:
        sys.exit("cloud must be one of: " + ", ".join(CLOUDS))
    if a["users"] not in ("just-me", "my-devices", "other-people"):
        sys.exit("users must be just-me, my-devices, or other-people")
    return a


def layout(a, parent):
    """Return the full plan: dict of relative paths inside each root."""
    parent = Path(parent)
    biz = slug(a["business_name"], 4)
    clients = [(c, slug(c, 4)) for c in a["clients"]]
    goals = [(g, slug(g, 5)) for g in a["goals"]]
    owners = [biz] + [s for _, s in clients]
    if len(set(owners)) != len(owners) or "personal" in owners:
        raise ValueError("Owner folder names collide. Ask for distinct business and client labels.")
    if len(set(s for _, s in goals)) != len(goals):
        raise ValueError("Project folder names collide. Ask for distinct short project names.")
    separate_personal = a["personal"] and a["users"] == "other-people"
    plan = {
        "parent": parent,
        "vault": parent / VAULT,
        "deliv": parent / DELIV,
        "personal_vault": (parent / PERSONAL_VAULT) if separate_personal else None,
        "biz": biz,
        "clients": clients,
        "goals": goals,
        "separate_personal": separate_personal,
    }
    return plan


def personal_projects():
    return ["family", "health", "money"]


def tree_text(a, p):
    lines = []
    v = VAULT
    lines.append(f"{v}/   (notes and knowledge only, your source of truth)")
    lines.append("  README.md, AGENTS.md, SYNC.md, .gitignore, .githooks/pre-commit")
    lines.append("  brain/")
    lines.append("    _index.md, _log.md")
    lines.append("    business/   overview, goals, ideal customer, voice and tone, proof")
    lines.append("    offers/     products and services")
    if p["clients"]:
        lines.append("    clients/    " + ", ".join(s + ".md" for _, s in p["clients"]))
    lines.append("    processes/  decisions/  people/")
    lines.append("  raw/          inbox for anything you want filed later")
    lines.append("  workspace/")
    lines.append(f"    {p['biz']}/")
    for _, gs in p["goals"]:
        lines.append(f"      {gs}/README.md")
    for _, cs in p["clients"]:
        lines.append(f"    {cs}/getting-started/README.md")
    if a["personal"] and not p["separate_personal"]:
        lines.append("    personal/   (private, never shared with client work)")
        for pr in personal_projects():
            lines.append(f"      {pr}/README.md")
    lines.append("")
    lines.append(f"{DELIV}/   (big files only, NOT in the notes sync)")
    lines.append("  README.md")
    lines.append(f"  {p['biz']}/")
    for _, gs in p["goals"]:
        lines.append(f"    {gs}/")
    for _, cs in p["clients"]:
        lines.append(f"  {cs}/getting-started/")
    if a["personal"]:
        lines.append("  personal/")
        for pr in personal_projects():
            lines.append(f"    {pr}/")
    if p["separate_personal"]:
        lines.append("")
        lines.append(f"{PERSONAL_VAULT}/   (separate from the Company Brain, because others use it)")
        lines.append("  README.md, .gitignore")
        for pr in personal_projects():
            lines.append(f"  {pr}/README.md")
    return "\n".join(lines)


# ----------------------------- templates -----------------------------

def gitignore_text(a, p):
    exts = BLOCKED_EXT
    out = []
    out.append("# Notes only. Big files live in the Deliverables folder, never here.")
    out.append("# Secrets and keys")
    out += [".env", ".env.*", "*.env", "secrets*", "credentials*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "id_ed25519*"]
    out.append("")
    out.append("# Video, audio, images, PDFs, zips, slide decks, installers")
    for e in exts:
        if e in ("pem", "key", "p12", "pfx"):
            continue
        out.append(f"*.{e}")
    out.append("")
    out.append("# Obsidian and system files that change on every open")
    out += [".obsidian/workspace.json", ".obsidian/workspaces.json", ".obsidian/cache", ".trash/", ".DS_Store", "Thumbs.db", "desktop.ini"]
    out.append("")
    out.append("# Allow the dummy-proof pointer files")
    if a["personal"] and a["users"] == "other-people" and not p["separate_personal"]:
        out.append("workspace/personal/")
    return "\n".join(out) + "\n"


def precommit_text():
    ext_re = "|".join(BLOCKED_EXT)
    return f"""#!/bin/bash
# Company Brain safety check. Runs before every commit (Obsidian Git included).
# Blocks big files (over 5 MB), blocked file types, and secrets from entering the notes sync.
LIMIT={LIMIT_BYTES}
BLOCKED='\\.({ext_re})$|(^|/)\\.env($|\\.)'
fail=0
while IFS= read -r -d '' f; do
  size=$(git cat-file -s ":$f" 2>/dev/null || echo 0)
  if [ "$size" -gt "$LIMIT" ]; then
    echo "BLOCKED (over 5 MB): $f  -> move it to your Deliverables folder"
    fail=1
  fi
  if echo "$f" | grep -Eiq "$BLOCKED"; then
    echo "BLOCKED (big file type or secret): $f  -> keep it out of the Brain"
    fail=1
  fi
done < <(git diff --cached --name-only --diff-filter=ACM -z)
exit $fail
"""


def readme_vault(a, p):
    today = date.today().isoformat()
    return f"""# Company Brain: {a['business_name']}

Created {today}. This folder is the single source of truth for {a['business_name']}.
It holds notes and knowledge only: markdown and small text files.

## Map

```
{VAULT}/   <- you are here (notes only)
{DELIV}/   <- next to this folder (big files only, not synced)
```

- `brain/` is the compiled knowledge. Start at `brain/_index.md`.
- `raw/` is your inbox. Drop anything here to be filed later.
- `workspace/` holds one folder per project, grouped by who it is for.
- `AGENTS.md` is the rule sheet every AI agent reads first.
- `SYNC.md` explains the backup and how to restore on a new computer.

## Big files

Videos, PDFs, images, zips, slide decks and recordings go in the `{DELIV}` folder next to this one, in the matching folder: `{DELIV}/<owner>/<project>/`.
Each project README in `workspace/` says exactly where its big files live.
"""


def agents_text(a, p):
    personal_rule = ""
    if a["personal"]:
        where = "the separate `Personal Brain` folder" if p["separate_personal"] else "`workspace/personal/`"
        personal_rule = f"""
## Personal area is private

- Personal notes live in {where}.
- Never read, quote, or summarize personal notes while working on business or client tasks.
- Only open the personal area when the owner asks about family, health or money in that same chat.
"""
    return f"""# Rules for AI agents working in this Company Brain

Read this first, every session.

1. Read `brain/_index.md` before you write anything. Search before you create a new page.
2. This folder holds notes only. Never save video, audio, images, PDFs, zips, slide decks or anything over 5 MB here. Save them in the `{DELIV}` folder next to this one, in `<owner>/<project>/`, and put a pointer in the project README.
3. Client work stays separate. When working on one client, read only `brain/business/`, `brain/offers/`, `brain/clients/<that client>.md`, and `workspace/<that client>/`. Do not read other clients' folders.
4. Never save passwords, tokens, API keys or private keys. Point the owner to the provider's own sign in screen.
5. Never invent facts, proof, prices, reviews or results. Write `[PLACEHOLDER]` and ask.
6. Every change to `brain/` gets a line in `brain/_log.md` and an entry in `brain/_index.md`.
7. Ask the owner before you send, publish, spend money, or change anything customers can see.
{personal_rule}"""


def sync_text(a, p):
    cloud = CLOUDS[a["cloud"]]
    steps = {
        "google-drive": f"""### Back up the notes to Google Drive

1. Install Google Drive for desktop from Google and sign in on Google's own page.
2. Open Google Drive for desktop, then Settings, then Preferences. Under "My computer" choose "Add folder".
3. Pick the `{VAULT}` folder and choose to back it up to Drive.
4. For your big files, add the `{DELIV}` folder the same way, as a SEPARATE backup. Never mix the two.
Menu names can change. If a label looks different, follow what Google shows on screen.""",
        "onedrive": f"""### Back up the notes to OneDrive

1. Sign in to OneDrive on Microsoft's own page or app.
2. Open OneDrive settings, then Sync and backup, then Manage backup.
3. Turn on the folder that holds `{VAULT}`. If your whole Documents folder is already backed up, the Brain is covered.
4. Back up the `{DELIV}` folder as a separate choice.
Menu names can change. Follow what Microsoft shows on screen.""",
        "dropbox": f"""### Back up the notes to Dropbox

1. Install the Dropbox app and sign in on Dropbox's own page.
2. Open Dropbox preferences, then Backups (or Backup), then Manage backup, and pick the folder that holds `{VAULT}`.
3. Back up `{DELIV}` as a separate choice.
Menu names can change. Follow what Dropbox shows on screen.""",
        "icloud": f"""### Back up the notes to iCloud Drive

1. Sign in to iCloud on your Mac or on the iCloud app for Windows.
2. Turn on iCloud Drive. On a Mac, also turn on Desktop and Documents folders if your Brain lives there.
3. Make sure `{VAULT}` sits inside a folder iCloud Drive covers.
4. Keep `{DELIV}` covered separately so your big files have their own backup.
Menu names can change. Follow what Apple shows on screen.""",
        "github": f"""### Back up the notes to a private GitHub repository

1. Make a free GitHub account on github.com if you do not have one.
2. On GitHub, create a NEW repository. Name it `company-brain`. Choose **Private**. Leave "Add a README" unchecked.
3. Install Git if Hermes tells you it is missing, and install the Obsidian Git plugin in Obsidian (Settings, Community plugins, Browse, search "Obsidian Git", Install, Enable).
4. Ask Hermes: "Start Git in my Company Brain, turn on the safety check, and connect it to my private repository." Give Hermes the repository address (not a password). Hermes shows you each command first.
5. The first upload opens a sign in window from GitHub. Sign in there. Never paste a token or password into Hermes.
6. Open the repository on github.com and check that it says **Private**.

The safety check (`.githooks/pre-commit`) refuses any commit that contains a big file, a blocked file type, or an `.env` file.""",
        "obsidian-sync": f"""### Back up the notes with Obsidian Sync

1. Obsidian Sync is a paid Obsidian service. Sign in to your Obsidian account inside Obsidian.
2. Open Settings, then Sync, and create a remote vault. Connect `{VAULT}` to it.
3. Under selective sync, check that these are OFF: images, audio, videos, PDFs, and "sync all other types".
4. Use "Excluded folders" for anything you want to keep off the cloud.
Menu names can change. Follow what Obsidian shows on screen.""",
        "none": f"""### No cloud yet

Your Brain stays on this computer for now. Until you pick a cloud:

1. Once a week, copy the `{VAULT}` folder and the `{DELIV}` folder to an external drive.
2. When you choose a cloud later, tell Hermes and it will walk you through the steps. The exclusions below are already in place.""",
    }[a["cloud"]]
    if a["cloud"] in ("google-drive", "onedrive", "dropbox", "icloud"):
        steps = f"""### Your {cloud} backup

1. Install the {cloud} app and sign in on its own screen. Never share passwords in chat.
2. Keep the working Brain and Deliverables OUTSIDE any folder already synced by that app. Documents may already be synced, so check first.
3. Ask Hermes to make a filtered notes snapshot with the skill's export command, then copy that snapshot to a private Company Brain Backups folder in your cloud drive. Only small Markdown and text files are copied. Review their contents first.
4. After each work session, make a new dated snapshot. This is one way backup, not automatic two way editing. Do not edit the backup copy.
5. Keep local files downloaded on each computer. If several devices need live editing, choose Obsidian Sync or private Git instead. Do not combine two sync services on one vault.
6. Copy Deliverables to a separate dated backup folder or an external drive. Do not enable live sync on the working Deliverables folder.
"""
    personal_note = ""
    if a["personal"] and a["users"] == "other-people":
        personal_note = "\n**Personal notes:** they live in the separate `Personal Brain` folder and are not part of the shared Brain. Back that folder up to your own private space only.\n"
    elif a["personal"]:
        personal_note = f"\n**Personal notes:** `workspace/personal/` stays inside your Brain and syncs to your own {cloud}. If other people ever get access, tell Hermes so it can move the personal area out.\n"
    return f"""# Backup, sync and restore

Your local folder is the source of truth. The cloud is a copy.
Cloud choice: {cloud}.

## What syncs and what stays local

| Folder | What is in it | Notes sync | Backup |
|---|---|---|---|
| `{VAULT}` | notes, markdown, small text | Yes | to {cloud} |
| `{DELIV}` | videos, PDFs, images, zips, slide decks, recordings | No, never | its own backup |

## What is always blocked from the notes sync

- Video, audio, images, PDFs, zips, slide decks, installers.
- Any single file over about 5 MB.
- `.env` files, keys and anything that looks like a secret.

The `.gitignore` blocks listed file types and secret filenames in Git, not file size or secrets pasted inside a note. The commit hook blocks files over 5 MB. Cloud apps do not read `.gitignore`; use the filtered export for cloud backups. Obsidian Sync has file type controls but no custom 5 MB rule, so check files before enabling it and keep large notes outside the vault. Review private content before any upload. Sync can spread deletion or mistakes; keep dated backup copies too.
{personal_note}
{steps}

## Back up your big files (Deliverables)

The `{DELIV}` folder is not part of the notes sync. Back it up separately: a cloud drive backup folder, or an external drive. Keep two copies of anything you cannot recreate.

## How to restore on a new computer

1. Install Obsidian and Hermes on the new computer.
2. Get your notes back:
   - Git: install Git, then ask Hermes to "clone my private Company Brain repository into my Documents folder". Sign in when GitHub asks.
   - Google Drive, OneDrive, Dropbox, iCloud: sign in, let the `{VAULT}` folder download, and copy it into Documents.
   - Obsidian Sync: sign in, then choose "Connect to remote vault".
3. Get your big files back from the Deliverables backup and put the folder next to `{VAULT}`, named `{DELIV}`.
4. In Obsidian choose "Open folder as vault" and pick `{VAULT}`.
5. Tell Hermes: "My Company Brain is at this folder. Read AGENTS.md and brain/_index.md." Hermes can use it right away.
6. If you use Git, turn the safety check back on: ask Hermes to run `git config core.hooksPath .githooks` inside the Brain.
"""


def index_text(a, p):
    today = date.today().isoformat()
    lines = [
        "# Brain index", "",
        f"> Every page in `brain/`, one line each. Last updated: {today}", "",
        "## Business",
        "- [[overview]]: what the business is and who it serves",
        "- [[goals]]: top goals and projects right now",
        "- [[ideal-customer]]: who you serve and what they need",
        "- [[voice-and-tone]]: how the business sounds, and what never to say",
        "- [[proof]]: real proof that is safe to use", "",
        "## Offers",
        "- [[products-and-services]]: what you sell", "",
    ]
    if p["clients"]:
        lines.append("## Clients")
        for c, s in p["clients"]:
            lines.append(f"- [[{s}]]: {c}")
        lines.append("")
    lines += ["## Processes", "(none yet)", "", "## Decisions", "(none yet)", "", "## People", "(none yet)", ""]
    return "\n".join(lines)


def log_text(a):
    today = date.today().isoformat()
    return f"""# Brain log

> Newest at the bottom. Format: `## [YYYY-MM-DD] action | subject`

## [{today}] create | Company Brain created by company-brain-starter
- Interview answers saved to the starter pages.
- Cloud choice: {CLOUDS[a['cloud']]}.
"""


def page(title, body, today):
    return f"---\ntitle: {title}\ncreated: {today}\nupdated: {today}\n---\n\n# {title}\n\n{body}\n"


def build(a, parent):
    p = layout(a, parent)
    today = date.today().isoformat()
    created = []
    skipped = []

    def write(path, text, executable=False):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            skipped.append(str(path))
            return
        path.write_text(text, encoding="utf-8", newline="\n")
        if executable:
            try:
                os.chmod(path, 0o755)
            except OSError:
                pass
        created.append(str(path))

    def mkdir(path):
        Path(path).mkdir(parents=True, exist_ok=True)

    v, d = p["vault"], p["deliv"]
    biz = p["biz"]
    tools = a["tools"]
    tools_line = ", ".join(f"{k}: {tools[k]}" for k in tools if tools[k]) or "[PLACEHOLDER]"

    # Vault root
    write(v / "README.md", readme_vault(a, p))
    write(v / "AGENTS.md", agents_text(a, p))
    write(v / "SYNC.md", sync_text(a, p))
    write(v / ".gitignore", gitignore_text(a, p))
    write(v / ".gitattributes", ".githooks/* text eol=lf\n")
    write(v / ".githooks" / "pre-commit", precommit_text(), executable=True)
    write(v / "raw" / "README.md", "# Inbox\n\nDrop notes, pasted emails, meeting notes and ideas here. Hermes files them into `brain/` later and logs it. Notes only: no big files.\n")

    # brain/
    b = v / "brain"
    write(b / "_index.md", index_text(a, p))
    write(b / "_log.md", log_text(a))
    write(b / "business" / "overview.md", page("Overview", f"**Business:** {a['business_name']}\n\n**What we sell:** {a.get('what_sells', '[PLACEHOLDER]')}\n\n**Website:** {a.get('website') or '[PLACEHOLDER]'}\n\n**Main tools:** {tools_line}\n\nRelated: [[goals]], [[ideal-customer]], [[products-and-services]]", today))
    goal_lines = "\n".join(f"{i}. {g}" for i, (g, _) in enumerate(p["goals"], 1)) or "[PLACEHOLDER]"
    write(b / "business" / "goals.md", page("Goals", f"Top goals and projects right now:\n\n{goal_lines}\n\nEach one has a project folder in `workspace/{biz}/`. Related: [[overview]]", today))
    write(b / "business" / "ideal-customer.md", page("Ideal customer", f"**Who we serve:** {a.get('serves', '[PLACEHOLDER]')}\n\nProblems they come with: [PLACEHOLDER]\n\nRelated: [[overview]], [[products-and-services]]", today))
    never = a.get("never_say") or "[PLACEHOLDER]"
    write(b / "business" / "voice-and-tone.md", page("Voice and tone", f"How we sound: [PLACEHOLDER]\n\n**Never say:** {never}\n\nRelated: [[overview]], [[proof]]", today))
    write(b / "business" / "proof.md", page("Proof", "Real results, reviews and examples that are safe to use: [REAL PROOF NEEDED]\n\nRelated: [[overview]], [[voice-and-tone]]", today))
    write(b / "offers" / "products-and-services.md", page("Products and services", f"{a.get('what_sells', '[PLACEHOLDER]')}\n\nPrices and what is included: [PLACEHOLDER]\n\nRelated: [[overview]], [[ideal-customer]]", today))
    for c, s in p["clients"]:
        write(b / "clients" / f"{s}.md", page(c, f"**Client:** {c}\n\nWhat we do for them: [PLACEHOLDER]\n\nProject folder: `workspace/{s}/getting-started/`\nBig files: `{DELIV}/{s}/getting-started/` (next to this Brain folder)\n\nRelated: [[overview]], [[products-and-services]]", today))
    for sub, what in (("processes", "How things get done, step by step."), ("decisions", "Decisions and the reason behind them."), ("people", "Team members, partners and key contacts.")):
        write(b / sub / "_about.md", f"# {sub.capitalize()}\n\n{what} Add a page here when something shows up in two places or matters a lot. List it in `brain/_index.md`.\n")

    # workspace: business
    for g, gs in p["goals"]:
        write(v / "workspace" / biz / gs / "README.md", project_readme(g, "business", biz, gs, a))
        mkdir(d / biz / gs)
    for c, cs in p["clients"]:
        write(v / "workspace" / cs / "getting-started" / "README.md", project_readme(f"{c}: getting started", "client", cs, "getting-started", a))
        mkdir(d / cs / "getting-started")

    # personal
    if a["personal"]:
        if p["separate_personal"]:
            pv = p["personal_vault"]
            write(pv / "README.md", "# Personal Brain\n\nPrivate. Family, health and money notes live here, away from the Company Brain, because other people use the Company Brain. Do not share this folder. Big files go in `Deliverables/personal/<project>/`.\n")
            write(pv / ".gitignore", gitignore_text({**a, "personal": False}, p))
            root = pv
        else:
            root = v / "workspace" / "personal"
        for pr in personal_projects():
            write(root / pr / "README.md", project_readme(f"Personal: {pr}", "personal", "personal", pr, a))
            mkdir(d / "personal" / pr)

    # deliverables root
    write(d / "README.md", f"""# Deliverables

Big files only: videos, PDFs, images, zips, slide decks, recordings.
This folder is NOT part of the notes sync. It sits next to `{VAULT}` and mirrors it:

```
{DELIV}/<business, client or personal>/<project>/
```

Back it up separately (a cloud drive backup folder or an external drive). The notes live in `{VAULT}/workspace/<owner>/<project>/README.md`, and that README points back here.
""")
    return p, created, skipped


def project_readme(title, owner_type, owner, project, a):
    today = date.today().isoformat()
    return f"""# {title}

- **Owner:** {owner_type} ({owner})
- **Created:** {today}
- **Status:** [PLACEHOLDER]
- **Goal:** [PLACEHOLDER]
- **Next step:** [PLACEHOLDER]

## Where the big files live

Videos, PDFs, images, zips, slide decks and recordings for this project live in the Deliverables folder next to this Brain folder:

`Deliverables/{owner}/{project}/`

Keep only notes in this folder.
"""


# ------------------------------- check -------------------------------

def check(brain):
    brain = Path(brain)
    problems = []
    for dirpath, dirnames, filenames in os.walk(brain):
        dirnames[:] = [x for x in dirnames if x not in (".git", ".obsidian")]
        for fn in filenames:
            fp = Path(dirpath) / fn
            rel = fp.relative_to(brain).as_posix()
            ext = fp.suffix.lower().lstrip(".")
            size = fp.stat().st_size
            if size > LIMIT_BYTES:
                problems.append(f"OVER 5 MB: {rel} ({size // 1024} KB) -> move to Deliverables")
            if ext in BLOCKED_EXT and ext not in ("key",):
                problems.append(f"BIG FILE TYPE: {rel} -> move to Deliverables")
            if fn.lower().startswith(".env") or ext in ("pem", "p12", "pfx", "key"):
                problems.append(f"SECRET: {rel} -> remove from the Brain")
    return problems


def export_notes(brain, destination):
    """Create a NEW filtered snapshot, never a live mirror or deletion sync."""
    import shutil
    brain = Path(brain).resolve()
    destination = Path(destination).resolve()
    if destination.exists() or brain == destination or brain in destination.parents:
        raise ValueError("Choose a new snapshot folder outside the Brain.")
    safe = []
    for fp in brain.rglob("*"):
        rel = fp.relative_to(brain)
        if fp.is_symlink() or not fp.is_file():
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        if fp.suffix.lower() not in (".md", ".txt") or fp.stat().st_size > LIMIT_BYTES:
            continue
        if any(word in fp.name.lower() for word in ("secret", "credential", ".env")):
            continue
        safe.append((fp, rel))
    for fp, rel in safe:
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fp, target)
    print(f"Copied {len(safe)} small notes to a new snapshot. No source files changed.")
    print("Review note contents for private information before uploading. This is not a secret scanner.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "build"):
        sp = sub.add_parser(name)
        sp.add_argument("--answers", required=True)
        sp.add_argument("--parent", required=True)
        if name == "build":
            sp.add_argument("--approved", action="store_true", help="Use only after the owner approves the displayed plan")
    sp = sub.add_parser("check")
    sp.add_argument("--brain", required=True)
    sp = sub.add_parser("export")
    sp.add_argument("--brain", required=True)
    sp.add_argument("--destination", required=True)
    args = ap.parse_args()

    if args.cmd == "export":
        export_notes(args.brain, args.destination)
    elif args.cmd == "plan":
        a = load_answers(args.answers)
        p = layout(a, args.parent)
        print(tree_text(a, p))
    elif args.cmd == "build":
        if not args.approved:
            sys.exit("Nothing created. Interview the owner, show the plan, and obtain approval first.")
        a = load_answers(args.answers)
        p, created, skipped = build(a, args.parent)
        print(f"Created {len(created)} files. Skipped {len(skipped)} that already existed.")
        for s in skipped:
            print("  kept existing:", s)
    elif args.cmd == "check":
        problems = check(args.brain)
        if problems:
            print("\n".join(problems))
            sys.exit(1)
        print("File check passed: no oversized files, blocked types or recognized secret filenames. Contents were not scanned.")


if __name__ == "__main__":
    main()
