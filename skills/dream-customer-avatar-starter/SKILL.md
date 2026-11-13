---
name: dream-customer-avatar-starter
description: Use when defining the ideal customer. Write one profile.
version: 2.1.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, customer-avatar, ai-employee]
    related_skills: [company-brain-starter, convert-follow-up-loop, product-champ-onboarding]
---

# Dream Customer Avatar Starter

This skill builds one useful customer profile from an interview. The profile feeds the AI employee the owner sets up in Product Champ on Day 2, and it shapes the quiz questions on Day 3. It is a starter. It does not do broad online research.

## When to Use

- The owner is on Day 2 or Day 3 of the Hire Your AI Agent challenge.
- The owner needs to tell the AI employee who it is talking to.
- The owner wants quiz questions that match a real buyer.

## What is in this skill

Everything this skill needs is inside its own folder. It needs no account, no outside file and no extra tool to run.

- `SKILL.md`: this file. The questions, the steps and the output format.
- `scripts/selftest.py`: checks that the skill folder is complete on this computer. Run `python <skill-dir>/scripts/selftest.py`, where `<skill-dir>` is the folder `skill_view` reports for this skill. Quote the path.

It works best after the skills named under Prerequisites. All of them come in the same free starter set. If one is not installed, do not stop. Ask the owner to paste what that skill would have saved, or ask its questions yourself, and mark anything unknown `[PLACEHOLDER]`.

## Prerequisites

- A starter Company Brain from `company-brain-starter`.
- Optional: real reviews, call notes, or messages the owner pastes in.
- Optional: real buyer wording from past messages. The simple way is for the owner to paste a few real messages with names and private details removed. If the owner already has a Product Champ connection that they chose to let read conversations, you may read only the conversations the owner names, and only for the buyer language you need. The `product-champ-onboarding` skill sets up the connection, and it starts without access to conversations. With no connection, use what the owner pastes.

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
