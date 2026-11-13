# Audit checklist

Read only. Nothing in this file changes the account. Save every export in one inventory folder inside the Hermes scratch area, using the file names below, so `scripts/reference_scan.py` can read them.

## Status words

- **READY**: read from the account and correct. Say what you saw.
- **NEEDS OWNER**: only the owner can answer or decide. Write the exact question and the exact value format you need.
- **BLOCKED**: cannot work until something outside this chat is fixed, such as a missing permission, a missing message template, or a setting only the account provider can change. Name who can fix it.
- **CAN'T TELL**: the connection could not read it. Say what you tried and how the owner can check it on screen. Never turn CAN'T TELL into READY or into a guess.

## What to read, and where to save it

| Item | Save as | What to check |
|---|---|---|
| Business profile | `business-profile.json` | Name, legal name if shown, address, phone, email, website with https, time zone, logo. Compare the address and phone with the live website and with each calendar's meeting location. Three places that disagree is one NEEDS OWNER question, not a fix. |
| Custom values | `custom-values.json` | Count, blank, placeholder text, two values that mean the same thing. |
| Custom fields | `custom-fields.json` | Count by type. A field a workflow needs that does not exist. |
| Calendars | `calendars.json`, one file per calendar if available | Active or not, assigned user, days and hours, length, buffer, meeting location, notifications on or off, confirmation mode. A calendar with no assigned user or no hours cannot take bookings. |
| Pipelines | `pipelines.json` | Names and stages exist. |
| Forms and surveys | `forms.json`, `surveys.json` | Which exist. Form wording is usually not readable through the connection. Mark consent wording CAN'T TELL and check it in the compliance walkthrough. |
| Phone number | `phone-numbers.json` | A number exists, it can text, which user it is linked to. Registration status is not readable. Mark it CAN'T TELL and check on screen. |
| Email sending domain | `email-domain.json` if readable | A dedicated sending domain exists and is active. If a default sender is saved on the domain, that sender wins over any workflow setting. |
| Users | `users.json` | Who has a login and their role. Is there a separate seat for Hermes. |
| Workflows | `workflows/<id>.json` and `workflows/<id>.triggers.json` | Published or draft. Which triggers are on. |
| Message templates | `templates/<id>.json` or `.html` | The text of any template a workflow step points at. A step that points at a template that no longer exists is BLOCKED. |
| Links and chat widgets | `links.json`, `chat-widgets.json` | Saved links that depend on a custom value. Whether any chat widget exists. |

Do not export contacts, conversations, payments, notes or reviews. This audit does not need them.

## Find what the workflows need

Run through `terminal`:

```text
python <skill-dir>/scripts/reference_scan.py --inventory <inventory-folder> --out <inventory-folder>/scan.json
```

Read `scan.json`:

- `must_fill`: custom values a workflow or saved link uses that are blank, placeholder or not defined. Items used by a published workflow come first. This is the fill list.
- `missing_templates`: steps that point at a message template that no longer exists.
- `dangling_ids`: a step or trigger that points at a pipeline, stage, calendar, form, user or workflow that is not in this account.
- `unknown_contact_fields`: a merge field that matches no custom field.
- `duplicates`: custom values with the same meaning under two keys. Never create a third. Ask which one to keep.
- `blank_and_unused` in the summary: blank values nothing depends on. Leave them blank. A high count here is normal for a template account.

## When workflow steps cannot be read

Some accounts do not allow workflow steps to be read through the connection. The scan then prints CAN'T TELL. Do this instead:

1. Report the workflow list by name and status.
2. Report every blank custom value in the core group: business name, short name, main phone, texting number, from email, website, contact page, booking link, review link, privacy and terms links, hours, notification email and number.
3. Ask the owner to open the three workflows they care about most and read you the step names. Check those by hand.
4. Keep "which values each workflow needs" as CAN'T TELL in the scorecard. Do not present the core group as the full answer.

## Stale and conflicting values

The script cannot know if a filled value is out of date. Compare every filled value in the core group with the Company Brain and the live website. A mismatch is NEEDS OWNER with both values shown.

## Scorecard rows

One row per item: area, item, status, what you found, what is needed. Put the exact value needed, or the exact question, in the last column. Count each status with code, not by eye, before you tell the owner the totals.
