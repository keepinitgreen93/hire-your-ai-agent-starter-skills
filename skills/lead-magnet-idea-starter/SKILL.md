---
name: lead-magnet-idea-starter
description: Pick one lead magnet or event that leads into the offer.
version: 1.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, lead-magnet, webinar, promise, day-3]
    related_skills: [offer-clarity-starter, dream-customer-avatar-starter, quiz-result-vsl-starter]
---

# Lead Magnet Idea Starter

This skill is step 2 of the Day 3 chain in the Hire Your AI Agent challenge from Truly Authentic Marketing (TAM). A lead magnet is a free, useful thing you give someone in exchange for their contact details. This skill gives the owner 3 to 5 lead magnet ideas that lead naturally into the one offer from `offer-clarity-starter`, scores them, and helps pick one. Then it writes the Promise Card: the exact promise the ad and the quiz must both keep.

The lead magnet can also be an event, such as a webinar or workshop registration. In that case the quiz delivers the registration link.

It drafts. It does not publish, send, or change any account.

## When to Use

- The owner finished `offer-clarity-starter` and has an approved One Offer Sheet.
- The owner asks "what should I give away?"
- The ad says one thing and the quiz says another, and the owner wants them to match.

## Prerequisites

- The approved One Offer Sheet from `offer-clarity-starter`.
- The Company Brain from `company-brain-starter` and the customer profile from `dream-customer-avatar-starter`.
- If the offer sheet is missing, run `offer-clarity-starter` first. Do not guess the offer.

## Procedure

1. Read the One Offer Sheet, the Company Brain, and the customer profile. Say the offer back in one line, and note the Offer type (transactional or transformational). Done when the owner agrees.
2. Ask two short questions, one at a time:
   - What does the buyer worry about or ask right before they buy this offer?
   - Does the owner like to teach live (an event) or would the owner rather give a short guide, checklist, or tool? Is a live event even possible this month?
3. Write 3 to 5 ideas. Mix the formats. For a transactional offer, favor items that speed up the yes, such as a price guide, an availability check, or a prep checklist. For a transformational offer, favor items that teach and build trust, such as a short training, a plan, or a webinar. Include at least one event idea if the owner can teach live. Formats to pick from: checklist, short guide, mini training video, planner or template, event registration (webinar, workshop, class), simple self check that ends in a result.
4. Score each idea from 1 to 5 on these five points. Show the table. Do the math in the table, not in your head.
   - Fit with the offer: does it lead straight to the offer?
   - Buyer pull: would the customer in the profile want it today?
   - Speed to value: can they use it in 10 minutes or less?
   - Ease for the owner: can it be made or hosted this week?
   - Safe to promise: can the owner deliver every word of the promise?
5. Recommend the top scorer. Explain why in two lines. Let the owner choose. Done when ONE lead magnet is picked.
6. If the pick is an event, collect the facts. Ask for each, and write [PLACEHOLDER] for any the owner does not know yet:
   - event name, date, time, and time zone
   - where it happens (online link or place)
   - registration page address
   - whether there is a replay
   - who is speaking and for how long
7. Write the Promise Card (format below). Show it as a preview. The owner approves it before it goes anywhere.
8. Hand off. Tell the owner the next skill is `quiz-result-vsl-starter`, which builds the quiz that delivers this exact promise. Offer to run it now.

## Output

```markdown
# Lead Magnet Ideas
| # | Idea | Format | Fit | Pull | Speed | Ease | Safe | Total |
|---|---|---|---|---|---|---|---|---|

Recommended: #[N], because [two lines].

# Promise Card (approved by the owner)
- Name of the free item:
- The one sentence promise (used in the ad AND at the top of the quiz):
- What they get, exactly:
- How they get it (link, email, text, download):
- When they get it (right after the quiz, or on the event date):
- What it is NOT (so nothing is overpromised):
- Event facts (if an event): date, time, time zone, place or link, replay yes/no
- Offer type (from the One Offer Sheet):
- The next step after it (the offer, from the One Offer Sheet):
```

## The Match Rule

The ad, the first quiz screen, the quiz result page, and the confirmation email must all repeat the Promise Card in the same words. If the ad says "free parent webinar link", the quiz result page must hand over the parent webinar link in the first lines. Never promise one thing in the ad and deliver another thing in the quiz.

## Regulated industries

If the business is in health, medical, mental health, wellness care, or finance:

- Make the lead magnet educational. A webinar or guide can explain, teach, and help people prepare questions for their own professional.
- Do not promise a cure, a treatment result, a diagnosis, savings, or returns. Do not use before and after claims.
- Add an emergency line where it fits, such as "If this is an emergency, call your local emergency number."
- Do not make a quiz that asks for health or money details. Keep the quiz about interests, goals, and timing. Collect only name and email unless the owner has an approved compliant setup.
- Ask the owner to have their own compliance contact review the Promise Card.

## Pitfalls

- Big ideas are slow to make. Prefer the one the owner can finish this week.
- An event only works if the date is real. If no date is set, pick a guide or checklist instead, or keep the date as [PLACEHOLDER] and do not run the ad yet.
- Do not count a "free consult" as a lead magnet. That is the offer's next step, and it comes after the lead magnet.
- Scores are a guide. The owner decides.

## Verification

The owner can read the one sentence promise and say, "I can deliver every word." The Promise Card names the item, how and when it arrives, and what it is not. Every event fact is real or marked [PLACEHOLDER].

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
