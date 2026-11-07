---
name: company-brain-starter
description: Interview the owner and build a starter Company Brain.
version: 2.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, company-brain, onboarding]
    related_skills: [dream-customer-avatar-starter, convert-follow-up-loop, organic-content-engine]
---

# Company Brain Starter

This skill turns Hermes into a Chief of Staff for one session. It interviews the owner, reads the owner's website, and builds a starter Company Brain: a folder of plain notes that Hermes reads before it works. It is Day 1 of the Hire Your AI Agent challenge from Truly Authentic Marketing (TAM). It does not connect any account.

## When to Use

- The owner is on Day 1 of the Hire Your AI Agent challenge.
- The owner says AI writing sounds generic and wants a business specific source of truth.
- The owner says "set up my Company Brain" or asks for the quick setup.

Do not use it to pull private data from other tools. It only uses what the owner says and what is public on the owner's website.

## Prerequisites

- Hermes desktop app (https://hermes-agent.nousresearch.com/desktop) running on the owner's Claude subscription.
- The owner's website address, or the words "no website yet".
- Optional: Firecrawl through Composio. If it is not connected, use Hermes web tools. If neither works, ask the owner to paste the homepage, services, and about copy.

## Procedure

1. Check the installed skills. Tell the owner whether the four starter skills are installed: `company-brain-starter`, `dream-customer-avatar-starter`, `convert-follow-up-loop`, and `organic-content-engine`. If any are missing, give the install line from the README of this repo and keep going. Done when the owner knows which of the four are present.
2. Ask for the business name, website address, and main service area.
3. Pull the website with Firecrawl or Hermes web tools. Summarize what it says about who the business helps, what it sells, and how it talks. Use it to confirm and fill gaps, never to overwrite what the owner says. Done when you have a short website summary or a pasted substitute.
4. Interview the owner one question at a time. Wait for each answer. If an answer is thin, ask one follow up. Cover:
   - Who do you help?
   - What problem do they come to you with?
   - What do you do differently?
   - What do customers say after working with you?
   - What proof is real and safe to use?
   - What do you never want the AI to say?
   - What do you want to reach this quarter?
5. Draft these files for a folder called `Company Brain`: overview, goals, ideal customer, products and services, voice and tone, and proof. Add buyer questions, approved calls to action, and a do not say list when the owner gave enough to fill them.
6. Show a preview of every file. Ask the owner what is wrong. Fix it. Save only after the owner approves. Done when the owner says yes to the preview.
7. End with a short summary of what you learned about the business, the offer, and the ideal client. Then name the 3 biggest gaps to fill next.

## Output

1. `Company Brain v1` preview, then the saved files.
2. Summary of the business, offer, and ideal client.
3. The 3 biggest gaps.
4. A note that `dream-customer-avatar-starter` and `convert-follow-up-loop` are ready for Day 2 and Day 3, and `organic-content-engine` is ready once the quiz is live.

## Pitfalls

- Long answers pile up. Summarize back in one line before you move on.
- A website can be out of date. Ask the owner if prices or services changed.
- Do not paste owner secrets into the Company Brain. Keep tokens and passwords out of it.

## Verification

Ask the owner to say what the Company Brain says about their business, offer, and ideal client. Hermes should be able to repeat all three without asking again.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
