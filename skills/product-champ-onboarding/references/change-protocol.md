# Change protocol: backup, verified fill, read back, change log, undo

Follow this every time you change the account. It was proven on a live account. The order matters.

## 1. Back up before the first write

1. Ask the owner for a folder they approve for the backup and the report. Create `backup-<date>-<time>` inside it.
2. Save a fresh export of everything you might touch and everything that depends on it: business profile, custom values, custom fields, calendars with their notifications, pipelines, forms, users, phone numbers, every workflow document with its triggers, and every message template a workflow step points at.
3. Run `python <skill-dir>/scripts/backup_check.py <backup-folder>` through `terminal`. It must print BACKUP OK. If a required file is missing, empty or holds an error, stop. No backup, no write.
4. Tell the owner the folder path. The backup can hold private business settings. It stays on the owner's computer and never goes into the Company Brain, a chat or a shared drive.

## 2. Verified facts only

A value may be written only when it comes from one of these, and you can name which:

- the account's own settings, such as the business profile, the account's phone number or the sending domain
- the owner's live website, fetched today, with the page returning normally
- the owner's Company Brain
- the owner's answer in this chat

Never invent or guess hours, addresses, phone numbers, prices, links, names, offers or testimonials. When two sources disagree, write nothing and ask. Places a message will be delivered to, such as a notification email or a notification number, always need the owner's answer, even when a likely value is visible. A value you cannot verify stays unchanged and goes on the NEEDS OWNER list with the exact question.

## 3. One batch, shown first

Show the owner one table: setting name, current value, proposed value, where the proposed value came from. Ask for a clear yes to that exact batch. A yes covers that batch only. Any change to the batch needs a new yes.

Update existing values. Do not create a new custom value when one with that meaning exists. Keep each value's name exactly as it is, because renaming can change its key and break every message that uses it.

## 4. Write, read back, log

For each item, in order:

1. Read the live value again. If it changed since the backup, stop and tell the owner.
2. Write it.
3. Read it back and compare it with the approved value, character for character.
4. Append one line to `change-log.jsonl` in the approved folder: time, type, setting, before, after, source, write result, read-back result.
5. Stop on the first failure. Do not retry a write whose result is unclear until a read shows what happened.

## 5. Workflows need extra care

- Never publish a draft workflow and never switch on a trigger that is off. Fix the content, leave it off, and list it under "Ready to turn on, needs your yes".
- In a published workflow, change only a broken or empty reference: a custom value, custom field, calendar, pipeline or link. Do not rewrite message wording. List wording suggestions separately.
- Before saving a workflow, re-read it and confirm the version matches the backup.
- Carry every workflow-level setting through the save, including the default sender fields and the note record. A save that leaves these out can clear them. After saving, compare every field outside the step you changed with the backup. If anything else changed, put it back from the backup at once and log both saves.
- If a save returns a validation error, stop on that workflow. Read it back, confirm nothing changed, and report it. Do not delete the step that failed validation.
- If your connection cannot save workflows, do not look for another way in. Write the exact fix as a suggestion.

## 6. After the batch

1. Export the changed items again and run `reference_scan.py` on the new export. Report the before and after numbers.
2. Confirm that every setting outside the approved batch is unchanged.
3. Build the setup report with `build_report.py`. Include what was fixed, what is suggested but not applied, the NEEDS OWNER questions, what is ready to turn on, and how to undo.

## 7. Undo

To undo a custom value, write the "before" value from `change-log.jsonl` back and read it back. A blank "before" means clear the value. To undo a workflow change, save the backed up document for that workflow with the current version number, then read it back. Undo only what this run changed. Never overwrite a change the owner made later.

## Never, even with a general "go ahead"

No send, schedule or test send of any email, text or direct message. No adding, tagging, enrolling or deleting contacts. No texting registration or Trust Center submission. No purchase or anything that costs money. No deleting. No change to a sending domain's saved default sender. No new users or tokens created by the agent. Each of these needs its own explicit yes for the exact action, and registration is not submitted during a trial by default.
