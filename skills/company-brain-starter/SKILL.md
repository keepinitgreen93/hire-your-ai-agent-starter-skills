---
name: company-brain-starter
description: Interview the owner, then build a synced Company Brain.
version: 3.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, company-brain, onboarding, backup]
    related_skills: [dream-customer-avatar-starter, convert-follow-up-loop, organic-content-engine]
---

# Company Brain Starter

This skill turns Hermes into a Chief of Staff for one session. It interviews the owner, then builds a Company Brain: a local folder of plain notes that Hermes reads before it works, organized for the owner's business, clients and personal life. It also sets up a safe cloud backup and keeps big files out of it. It is Day 1 of the Hire Your AI Agent challenge from Truly Authentic Marketing (TAM).

The rule that matters most: **ask first, build second.** Do not create a single folder until the owner has answered the questions and approved the folder plan.

## When to Use

- The owner is on Day 1 of the Hire Your AI Agent challenge.
- The owner says AI writing sounds generic and wants a business specific source of truth.
- The owner says "set up my Company Brain", "set up my brain the right way", or asks for the quick setup.

Do not use it to pull private data from other tools. It only uses what the owner says and what is public on the owner's website.

## Prerequisites

- Hermes desktop app (https://hermes-agent.nousresearch.com/desktop) running on the owner's Claude subscription.
- Python 3 on the owner's computer, to run the folder builder `scaffold_brain.py` (see "Find the builder" below). If Python is missing, build the same tree by hand with Hermes file tools and follow the same plan.
- Optional: Obsidian (https://obsidian.md), a free notebook app, to browse the notes.
- Optional: Firecrawl through Composio. If it is not connected, use Hermes web tools. If neither works, ask the owner to paste the homepage, services and about copy.

## Find the builder

The builder is `scripts/scaffold_brain.py`, next to this SKILL.md. Hermes copies the whole skill folder on install, so it is normally already there. Before Part 2, locate it:

1. Look for `scripts/scaffold_brain.py` inside this skill's folder (the folder `skill_view` reports as `skill_dir`). If it exists, use that full path wherever a step says `python scaffold_brain.py`. Quote the path, it may contain spaces.
2. If it is missing (an older install that copied only SKILL.md), download it from the public repo into the Hermes scratch folder, outside the Brain and outside any repo:
   `https://raw.githubusercontent.com/keepinitgreen93/hire-your-ai-agent-starter-skills/main/skills/company-brain-starter/scripts/scaffold_brain.py`
   Tell the owner what you are downloading and from where. Read the first 40 lines to confirm it is the folder builder before you run it. Reinstalling with `hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/company-brain-starter --yes --force` also restores it.
3. If both fail, tell the owner and build the same tree by hand with Hermes file tools, following the approved plan exactly. Keep the same rules: notes only in the Brain, `Deliverables` outside it, the notes-only `.gitignore`, and no overwriting existing files.

The builder is a plain Python file with no network calls. It only creates folders and files the approved plan lists.

## The model, in one picture

```
Documents/
  Company Brain/   notes and knowledge only. Single source of truth. Synced to the cloud.
  Deliverables/    big files only (video, PDF, images, zips, slide decks, recordings). NOT in the notes sync.
```

- Local first. The folder on the owner's computer is the truth. The cloud is a copy.
- Notes sync. Big files do not. Big files get their own separate backup.
- Every project in the Brain has a README that says where its big files live in Deliverables.
- Personal notes stay private and are never read during business or client tasks.

## Procedure

### Part 1: Interview (ask first)

1. Check the installed skills. Tell the owner whether the seven starter skills are installed: `company-brain-starter`, `dream-customer-avatar-starter`, `convert-follow-up-loop`, `organic-content-engine`, `offer-clarity-starter`, `lead-magnet-idea-starter`, and `quiz-result-vsl-starter`. If any are missing, give the install line from the README of this repo and keep going.
2. Say in two lines what is about to happen: ten short questions, then a preview of the folders, then nothing is built until the owner says yes.
3. Ask these questions **one at a time**, in plain words. Wait for each answer. If an answer is thin, ask one follow up. Say back each answer in one line before the next question. The owner can say "skip" to any question.
   1. What is your business called, and what do you sell?
   2. Who do you serve? Describe your ideal customer.
   3. What is your website address? (Or say "no website yet".)
   4. Do you have clients or customers you serve one by one, like a coach with clients? If yes, tell me a few names. You can skip this.
   5. Do you want a private personal area too, for family, health and money? It stays separate from your business and client work.
   6. What are your main tools? For example your CRM, your email, and where you keep files.
   7. Where do you want your notes backed up? Google Drive, OneDrive, Dropbox, iCloud, GitHub, Obsidian Sync, or none yet.
   8. Will more than one person or computer use this Brain?
   9. What are your top three goals or projects right now?
   10. Is there anything you never want the AI to say or do?
4. If the owner gave a website, read it with Firecrawl or Hermes web tools and summarize who it helps, what it sells and how it talks. Use it to confirm and fill gaps, never to overwrite what the owner said.
5. Save the answers to a scratch file named `answers.json` outside the Brain folder (use the active Hermes scratch folder, never save private answers in the public skill repo; delete the scratch answers after verification). Keys: `business_name`, `what_sells`, `serves`, `website`, `clients` (list of names), `personal` (true or false), `tools` (map of tool kind to name), `cloud` (`google-drive`, `onedrive`, `dropbox`, `icloud`, `github`, `obsidian-sync`, or `none`), `users` (`just-me`, `my-devices`, or `other-people`), `goals` (up to three), `never_say`. Never save passwords, tokens or keys in it. Done when every question is answered or skipped.

### Part 2: Preview and confirm (still nothing built)

6. Decide the location. Default: a local folder with `Company Brain` and `Deliverables` side by side. Check whether Documents is already synced first. If it is, select a local folder outside that sync. Tell the owner the full path. If a `Company Brain` folder already exists there, stop and ask whether to add to it. The builder never overwrites an existing file.
7. Run `python scaffold_brain.py plan --answers <answers.json> --parent <Documents folder>`. It prints the folder tree for these answers and creates nothing. Show it to the owner and explain it in three plain lines: notes folder, big files folder, personal area (if chosen).
8. Show the sync and backup plan in plain words: which cloud, what syncs, what is blocked (video, audio, images, PDFs, zips, anything over about 5 MB, `.env` files and secrets).
9. Ask: "Does this look right? Say yes to build it, or tell me what to change." Change the answers file and run `plan` again until the owner says yes. Done when the owner says yes to the exact tree.

### Part 3: Build

10. Run `python scaffold_brain.py build --answers <answers.json> --parent <Documents folder> --approved`. It builds only what the answers call for: the Brain, the Deliverables folder, project folders with README pointers, `.gitignore`, a commit safety check, `AGENTS.md` and `SYNC.md`.
11. Open the starter pages in `brain/business/` and `brain/offers/`. Fill them with the owner's answers and the website summary. Show a preview of each page. Ask what is wrong. Fix it. Save only after the owner approves. Use `[PLACEHOLDER]` and `[REAL PROOF NEEDED]` for anything unknown.
12. Add a line to `brain/_log.md` and update `brain/_index.md` for every page you add or change.

### Part 4: Backup and sync

For a cloud drive, use the filtered export instead of syncing the working vault directly: `python scaffold_brain.py export --brain <vault> --destination <new dated snapshot folder>`. It copies only Markdown and text under 5 MB, omitting hidden files and known secret filenames. Review contents, then copy the snapshot into the chosen cloud drive folder. Repeat after work sessions. This is a one way backup, not automatic two way sync. For live device sync, use private Git or Obsidian Sync. Never run two sync engines on the same vault. On several devices, finish syncing before editing and take turns on the same note.

Agent instructions are not access controls. Never grant a client agent access to the whole vault. Give it only a scoped folder or approved notes, excluding personal data and other clients. If that tool cannot restrict access, do not give it vault access. Confirm sharing and separate account permissions before connecting other people.


13. Open `SYNC.md` in the Brain and walk the owner through the steps for the cloud they chose, one step at a time. The owner signs in to their own cloud on the provider's own page. Never ask for a password, token or key in chat.
14. For Git: confirm the repository is **Private**, turn on the safety check with `git config core.hooksPath .githooks`, and make the first commit only after the owner says yes. Never push anywhere the owner has not named.
15. For Google Drive, OneDrive, Dropbox and iCloud: these back up whole folders and cannot block file types, so the rule is notes only in the Brain. Run `python scaffold_brain.py check --brain <Company Brain folder>` now, and offer to run it weekly. It lists any big file, blocked type or secret that does not belong. For Obsidian Sync, also turn off images, audio, videos, PDFs and "sync all other types" in the Sync settings.
16. Help the owner set up a separate backup for the `Deliverables` folder (a cloud drive backup folder or an external drive). Never put it in the notes sync.
17. Read the "How to restore on a new computer" section of `SYNC.md` aloud in plain words so the owner knows the way back.

### Part 5: Finish

18. End with a short summary of what you learned about the business, the offer and the ideal client. Then name the 3 biggest gaps to fill next.

## Output

1. The folder plan the owner approved, then the built folders.
2. Starter pages: overview, goals, ideal customer, products and services, voice and tone, proof, plus one page per client if clients were given.
3. `AGENTS.md`, `SYNC.md`, `.gitignore`, and the commit safety check.
4. Summary of the business, offer and ideal client, and the 3 biggest gaps.
5. A note that `dream-customer-avatar-starter` and `convert-follow-up-loop` are ready for Day 2 and Day 3, and `organic-content-engine` is ready once the quiz is live. The three Day 3 skills (`offer-clarity-starter`, `lead-magnet-idea-starter`, `quiz-result-vsl-starter`) run in that order.

## Pitfalls

- Building before the owner says yes. Never do it.
- Long answers pile up. Summarize back in one line before you move on.
- A website can be out of date. Ask the owner if prices or services changed.
- Putting a video, PDF or image in the Brain "just for now". It bloats the sync. Save it in Deliverables and leave a pointer in the project README.
- Putting the personal area in a Brain that other people use. If the owner said others use it, keep personal notes in a separate `Personal Brain` folder (the builder does this).
- Cloud drives (Google Drive, OneDrive, Dropbox, iCloud) do not block file types for you. The weekly check is how you catch strays.
- Do not paste owner secrets into the Brain. Keep tokens and passwords out of it.
- Windows paths with spaces: quote every path.

## Verification

- Run `python scaffold_brain.py check --brain <Company Brain folder>`. It must pass.
- For Git: `git check-ignore -v` on a test video, PDF and `.env` file must show each one as ignored.
- Every project README in the Brain names its `Deliverables/<owner>/<project>/` folder.
- Ask the owner to say what the Company Brain says about their business, offer and ideal client. Hermes should be able to repeat all three without asking again.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, push to any online repository, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Personal notes are never shared with agents working on client tasks. Restrict their file access, not just their prompt. If personal notes need sharing later, require a separate approved private vault first.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
