---
name: quiz-result-vsl-starter
description: Map a quiz whose result pages deliver, pitch, and book.
version: 1.0.0
author: Truly Authentic Marketing
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hire-your-ai-agent, quiz, vsl, booking, ai-studio, day-3]
    related_skills: [offer-clarity-starter, lead-magnet-idea-starter, convert-follow-up-loop, dream-customer-avatar-starter]
---

# Quiz Result VSL Starter

This skill is step 3 of the Day 3 chain in the Hire Your AI Agent challenge from Truly Authentic Marketing (TAM). It maps a short quiz that delivers the lead magnet the ad promised. Then it writes each result page in a fixed order: the promised item first, then a short VSL, then a booking calendar with one call to action. A VSL is a video sales letter: a short video where the owner explains the offer in their own words. At the end it writes the build prompt the owner pastes into AI Studio in Product Champ.

It drafts. It does not build, publish, send, or change any account.

## When to Use

- The owner has an approved One Offer Sheet (`offer-clarity-starter`) and an approved Promise Card (`lead-magnet-idea-starter`).
- The owner wants a quiz that delivers what the ad promised, then invites the right people to book.

## Prerequisites

- The One Offer Sheet and the Promise Card. If either is missing, run that skill first. Do not guess.
- The Company Brain and the customer profile.
- A booking calendar link from the owner's Product Champ account, or the words "calendar not ready". Use [PLACEHOLDER] if it is not ready.
- The owner's real proof, or [REAL PROOF NEEDED].

## Procedure

1. Read the One Offer Sheet, the Promise Card, the Company Brain, and the customer profile. Say back the promise in one line. Done when the owner agrees.
2. Map the quiz. Keep it short.
   - Title and first screen: repeat the Promise Card sentence word for word.
   - 5 to 7 questions, one per screen, multiple choice. Base them on what the customer profile says buyers care about. Include one question about timing or readiness (for example: right now, within a month, later, just looking).
   - Do not ask for private details. The only contact fields are first name, email, and a checkbox to agree to emails. Add phone only if the owner wants texts and has a texting setup.
3. Set simple scoring. Each answer adds 0 to 3 points toward a group. Write the rule in one sentence, then show a small table of answer, points, and group. Done when a person can work out any result by hand.
4. Make 2 or 3 result groups. Give each a name and a plain description. Always include a gentle group for "just looking" or "not ready yet" so no one is pushed.
5. Write each result page in this exact order:
   1. **The delivered item.** First thing on the page, big and clear. For a guide, the download or view button. For an event, the registration link with the date, time, and time zone. Use the Promise Card words.
   2. **A short note** that connects the result group to the next step (2 or 3 lines).
   3. **The VSL.** A 60 to 120 second script (format below) with a place for the video.
   4. **The booking block.** A heading, one line of what the call is for, the owner's Product Champ booking calendar, and ONE call to action button or line. Same call to action on every group, except the "not ready" group, which gets a softer one (for example, a free resource or a reminder email).
6. Write the VSL script for each group, or one shared script plus a short group intro line. Use the format below. Show it with the word count and the estimated time (about 130 words per minute). Done when each script fits 60 to 120 seconds.
7. Write the follow up email for each group (short, tied to the Promise Card). Point to `convert-follow-up-loop` for the full follow up plan.
8. Show the whole map as a preview: questions, scoring, groups, result pages, scripts, emails. Ask what is wrong. Fix it. Done when the owner says "approved".
9. Tell the owner to record the VSL on a phone using the script. Share these tips: sit near a window, hold the phone at eye level, speak like you would to one person, read from the script on a second screen or note, and keep each take under two minutes. Remind the owner that the page can go live with a [VIDEO COMING] note until the video exists. Nothing is uploaded or published without the owner's OK.
10. After approval, write ONE build prompt for AI Studio (format below). Show it. The owner pastes it into AI Studio.
11. Remind the owner of the next steps from the challenge guide: in AI Studio type `Connect forms to my CRM`, publish, test with a fake lead, and take every result at least once.

## VSL script format (60 to 120 seconds)

Plain words. Short sentences. Spoken, not written.

1. **Hook (about 8 seconds).** Name the person and the thing they just got. Example shape: "Thanks for taking the quiz. Your [item] is right above this video."
2. **Their situation (about 15 seconds).** Describe, in the customer's own words from the profile, what they are dealing with.
3. **A different way to see it (about 20 seconds).** One idea that helps them see the problem more clearly. Teach, do not scold.
4. **The offer (about 25 seconds).** Who it is for, the result, what is included. Use the One Offer Sheet only.
5. **Proof (about 10 seconds).** One real proof line from the owner, or `[REAL PROOF NEEDED]`. Never invent it.
6. **Who it is not for (about 7 seconds).** Be honest about fit.
7. **One call to action (about 10 seconds).** Point down to the calendar. One action only.

## AI Studio build prompt (the last thing you write)

Fill in every bracket from the approved map. Keep it as one block the owner can paste.

```text
Build a React (Vite) project: a short quiz funnel for [BUSINESS NAME].
Brand: [COLORS AND FONT, from the Company Brain, or "clean and simple"]. Mobile first.
First screen: the title "[TITLE]", the promise "[PROMISE CARD SENTENCE]", and a Start button.
Questions, one per screen, with progress and a Back button:
[LIST EVERY QUESTION AND EVERY ANSWER]
Scoring: [SCORING RULE AND TABLE]. Result groups: [GROUP NAMES].
After the last question, show a form with first name, email, and a checkbox "I agree to get emails from [BUSINESS NAME]". Do not ask for anything else.
Then show the result page for the person's group. Each result page has these parts, in this order:
1. The delivered item first: [FOR EACH GROUP: the item, button text, and link or [PLACEHOLDER]].
2. A short note: [TEXT].
3. A video area for the VSL with the title "[VIDEO TITLE]". Until a video link is added, show the line "Video coming soon".
4. A booking section with the heading "[HEADING]", the line "[WHAT THE CALL IS FOR]", my Product Champ booking calendar [CALENDAR EMBED OR LINK, or leave a clear spot for it], and one button "[CALL TO ACTION]".
Page text for each group: [PASTE THE APPROVED TEXT].
Keep the layout simple and easy to read on a phone. No fake reviews, no made up numbers.
After the build, I will type: Connect forms to my CRM.
```

## Output

1. Quiz map: title, first screen, questions, scoring rule and table, result groups.
2. One result page per group, in the fixed order, with its VSL script, word count, and time.
3. One follow up email per group.
4. The recording tips.
5. The AI Studio build prompt.
6. A short check list: Promise Card words match on every page, one call to action per page, every proof line real or a placeholder.

## Regulated industries

If the business is in health, medical, mental health, wellness care, or finance:

- Keep every result page educational. Teach, explain, and point to the owner's service as a next step. No cure, treatment, diagnosis, savings, or outcome claims. No before and after claims.
- Do not call a result a diagnosis or a score of someone's health or money situation. Name groups by interest, goal, or readiness, not by condition.
- Add an emergency line to each result page and to the VSL where it fits, such as "If this is an emergency, call your local emergency number."
- Keep health and money details OUT of quiz answers. Ask about goals, topics, and timing instead. Collect only name and email unless the owner has an approved, compliant setup for more.
- Ask the owner to have their own compliance contact review the pages, scripts, and emails before anything goes live.

## Pitfalls

- A result page that starts with a sales pitch breaks the promise. The delivered item always comes first.
- Do not pile on calls to action. One per page.
- An event link without a date, time, and time zone confuses people. Include all three.
- If the booking calendar is not ready, leave a clear [PLACEHOLDER] and tell the owner to finish the calendar in Product Champ before publishing.
- Long scripts lose viewers. Cut to 120 seconds at most.

## Verification

- The owner can take the quiz in the preview and reach every result group.
- Each result page shows the promised item first, then the video area, then the calendar and one call to action.
- The first screen and every result page repeat the Promise Card words.
- The owner reads each VSL out loud and times it. It lands between 60 and 120 seconds.
- Nothing was published or sent. The owner approved each piece.

## Guardrails

- Read the owner's Company Brain first. If there is none, ask the owner to paste one or run `company-brain-starter` before you draft.
- Never invent facts, proof, prices, reviews, results, awards, locations, policies, or guarantees. If something is missing, write `[PLACEHOLDER]` and ask for it. Where proof is unsupported, write `[REAL PROOF NEEDED]`.
- Draft only. Do not send, publish, post, message leads, change records in any account, connect new accounts, or spend money without the owner's explicit approval of the exact action.
- Never ask the owner to paste a password, token, or API key into the chat. Point them to the provider's secure sign in screen or a private settings file on their own computer.
- Keep the writing plain, at a seventh grade reading level. Avoid hype words. Do not use em dashes or en dashes.
