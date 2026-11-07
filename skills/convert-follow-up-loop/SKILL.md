---
name: convert-follow-up-loop
description: Map lead capture, follow up, and booking for one offer.
version: 2.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, follow-up, product-champ, quiz]
    related_skills: [company-brain-starter, dream-customer-avatar-starter]
---

# Convert and Follow Up Loop

This skill maps the simple path from a new lead to a booked call: capture, first reply, qualify, book, and nurture. It supports Day 2 (the AI employee that answers leads) and Day 3 (the quiz lead magnet and its follow up) of the Hire Your AI Agent challenge. It drafts the plan and messages. The owner builds and turns things on.

## When to Use

- The owner is setting up the Product Champ AI employee or the Quiz Submitted follow up.
- The owner asks where leads come from and what happens next.
- The owner wants follow up messages drafted.

## Prerequisites

- A starter Company Brain, and ideally the customer profile from `dream-customer-avatar-starter`.
- The main offer or next step, and a booking link or phone number.
- Optional read only check of Product Champ. Product Champ is TAM's white label of HighLevel. Hermes connects to it through HighLevel's official MCP server at `https://services.leadconnectorhq.com/mcp/`. The owner makes a Private Integration Token and finds the Location ID inside Product Champ, and keeps both in a private settings file. Start with View permissions only. Use it to see what already exists, such as calendars, pipelines, and recent conversations. Do not create, edit, send, or delete anything through it. The owner can add Edit permissions later, one at a time.
- Product Champ is a paid plan after the free 30 day trial. Texting registration is submitted only after the paid plan is active.

## Procedure

1. List every place a lead can come from: website form, quiz, phone calls, texts, Google Business Profile, comments, and direct messages. Done when each source has a row.
2. For each source, write where the lead goes, the first reply, and whether the owner must approve it.
3. Write one or two screening questions that separate serious buyers from people who are only looking.
4. Draft the booking path and the not ready nurture messages.
5. If the quiz is live, draft the follow up for each result tier. Keep each message short and tied to the score.
6. If Product Champ is connected, run a read only check and note what already exists. Done when the plan says what to build and what to reuse.
7. Write a test lead checklist so the owner can check the loop by hand.

## Output

```markdown
# Convert and Follow Up Loop

## Capture map
| Source | Where it goes | First reply | Owner approval needed? |
|---|---|---|---|

## Screening questions
1.
2.

## Booking path
...

## Not ready nurture
Message 1:
Message 2:
Message 3:

## Test lead checklist
- [ ] Submit a test form or test quiz entry
- [ ] The contact shows up in Product Champ
- [ ] The first reply reads right
- [ ] The booking link works
- [ ] The not ready tag or list is right
```

## Pitfalls

- Texting needs the carrier registration to be approved first. Draft the messages, and do not promise texts go out before then.
- Only message people who opted in. Do not draft cold outreach.
- A read only token cannot change anything. If Hermes needs to build, the owner decides whether to add Edit permissions.
- Do not claim the loop works until a test lead has passed through it.

## Verification

The owner submits one fake lead. The contact appears, the first reply draft is right, the booking link works, and the right nurture tag is set.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
