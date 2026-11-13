---
name: organic-content-engine
description: Use when planning a week of posts. Draft one content set.
version: 2.1.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, content, organic]
    related_skills: [company-brain-starter, dream-customer-avatar-starter]
---

# Organic Content Engine

This skill turns one real buyer question, job story, or proof point into a week of organic posts that help buyers find, trust, and choose the business. Use it after the Day 3 quiz is live, to bring people to the quiz. It writes drafts. The owner posts them.

## When to Use

- The quiz lead magnet from Day 3 is built and the owner wants people to find it.
- The owner has one buyer question to answer and wants a full set of posts from it.
- The owner is stuck on what to post this week.

## What is in this skill

Everything this skill needs is inside its own folder. It needs no account, no outside file and no extra tool to run.

- `SKILL.md`: this file. The questions, the steps and the output format.
- `scripts/selftest.py`: checks that the skill folder is complete on this computer. Run `python <skill-dir>/scripts/selftest.py`, where `<skill-dir>` is the folder `skill_view` reports for this skill. Quote the path.

It works best after the skills named under Prerequisites. All of them come in the same free starter set. If one is not installed, do not stop. Ask the owner to paste what that skill would have saved, or ask its questions yourself, and mark anything unknown `[PLACEHOLDER]`.

## Prerequisites

- A starter Company Brain and ideally the customer profile.
- One buyer question or topic.
- The quiz link, if the posts should point to it.
- Optional: photos, brand colors, real proof. Optional: example posts the owner likes. Use Firecrawl or Hermes web tools only on public pages the owner names.

## Procedure

1. Read the Company Brain. Pull out voice, service area, proof, offers, and top objections. Done when you can state the voice in one line.
2. Mark the topic as cold, warm, or hot buyer interest.
3. Write the weekly set:
   - 1 Google Business Profile post
   - 1 short website answer that an AI search tool could quote
   - 1 email
   - 3 social posts from different angles
   - 1 carousel outline
   - 1 image prompt for the owner's preferred image tool
4. End every piece with one clear next step, such as taking the quiz.
5. Flag missing proof or details instead of filling them in.
6. Give the owner an approval checklist.

## Output

```markdown
# Weekly Organic Content Set

## Source idea
...

## Buyer temperature map
- Cold:
- Warm:
- Hot:

## Google Business Profile post
...

## Website answer
...

## Email
...

## Social posts
1.
2.
3.

## Carousel outline
Slide 1:
Slide 2:

## Image prompt
...

## Approval checklist
- [ ] Facts checked
- [ ] Proof is real
- [ ] Call to action is right
- [ ] Ready for the owner to post by hand
```

## Pitfalls

- One topic per week. Do not mix topics in one set.
- Do not copy another business's posts. Use examples only to learn the format.
- Health, legal, and money topics need the owner's careful review before anything is posted.
- Do not say a post will bring leads. Say what it is meant to do.

## Verification

The owner reads each draft, can point to the real fact behind each claim, and can post at least three pieces without rewriting them.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
