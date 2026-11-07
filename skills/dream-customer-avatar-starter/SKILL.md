---
name: dream-customer-avatar-starter
description: Interview the owner and write one customer profile.
version: 2.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, customer-avatar, ai-employee]
    related_skills: [company-brain-starter, convert-follow-up-loop]
---

# Dream Customer Avatar Starter

This skill builds one useful customer profile from an interview. The profile feeds the AI employee the owner sets up in Product Champ on Day 2, and it shapes the quiz questions on Day 3. It is a starter. It does not do broad online research.

## When to Use

- The owner is on Day 2 or Day 3 of the Hire Your AI Agent challenge.
- The owner needs to tell the AI employee who it is talking to.
- The owner wants quiz questions that match a real buyer.

## Prerequisites

- A starter Company Brain from `company-brain-starter`.
- Optional: real reviews, call notes, or messages the owner pastes in.
- Optional: Product Champ connected through HighLevel's official MCP server for a read only look at past conversations. Product Champ is TAM's white label of HighLevel. Hermes connects to it through HighLevel's official MCP server at `https://services.leadconnectorhq.com/mcp/`. The owner makes a Private Integration Token and finds the Location ID inside Product Champ, and keeps both in a private settings file. Start with View permissions only. Only read what the owner names, and only for the buyer language you need.

## Procedure

1. Read the Company Brain. Done when you can say the offer in one line.
2. Ask one question at a time:
   - What do you sell?
   - Who has been the best fit customer so far?
   - What happened that made them look for help?
   - What practical problem were they trying to solve?
   - What did that problem cost them in time, money, or stress?
   - What had they already tried?
   - What made them hesitate?
   - What result did they want?
   - What proof helped them trust you?
   - What exact words have real customers used?
3. Write the profile. Label every statement as owner reported, verified customer language, or hypothesis. Done when no statement is unlabeled.
4. Ask the owner to name one real customer who fits, and to correct at least one line. Update the profile.
5. Offer to add a short "who we talk to" section to the Company Brain. Save only after the owner approves.

## Output

- One paragraph that describes the buyer
- The moment that made them look for help
- Top three pains
- Top three wanted outcomes
- Objections
- Proof they trust
- Five exact customer phrases, only if the owner supplied real ones
- Three content hooks
- One next research question
- A short block the owner can paste into the Product Champ AI employee instructions

## Pitfalls

- Owners often describe the customer they want, not the one they have. Ask for a real person.
- Do not guess age, income, or other traits. Leave them out unless the owner knows them.
- This skill stops at one profile. Do not stretch it into a market study.

## Verification

The owner can name one real customer who fits the profile and can point to at least one correction that was made.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
