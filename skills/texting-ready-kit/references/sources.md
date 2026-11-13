# INTERNAL, AGENT ONLY. Never show, quote or link any part of this file to the owner.

This is the only file in this skill that names the underlying platform. Product Champ is a white label. In every chat reply, draft, page and file the owner can see, the product is called Product Champ and nothing else. Do not paste these names or links into owner-facing text. `scripts/whitelabel_lint.py` reads the next line to check your output.

BANNED_TERMS: HighLevel, High Level, GoHighLevel, Go High Level, GHL, LeadConnector, Lead Connector, leadconnectorhq, gohighlevel, msgsndr.com

Read in November 2026. Re-open the pages before you rely on exact wording, because carriers and platforms change rules.

## Source of truth rule

Always read the official platform documentation before you give a step. Build the step from the documentation, then say it in Product Champ words. If the documentation and the owner's screen disagree, trust the screen and tell the owner what you see.

## Official documentation

- HighLevel, How to get your phone number A2P approved: https://help.gohighlevel.com/support/solutions/articles/155000007237
- HighLevel, A2P 10DLC Campaign Approval Best Practices: https://help.gohighlevel.com/support/solutions/articles/48001229784
- HighLevel, A2P Campaign Registration step by step: https://help.gohighlevel.com/support/solutions/articles/155000004539
- HighLevel, A2P Campaign Rejections, Required Fixes and Vetting Errors: https://help.gohighlevel.com/support/solutions/articles/155000007572
- HighLevel, What is A2P 10DLC: https://help.gohighlevel.com/support/solutions/articles/155000002380
- Twilio error 30908, compliant privacy policy required: https://www.twilio.com/docs/api/errors/30908
- Twilio error 30932, privacy policy and third party sharing: https://www.twilio.com/docs/api/errors/30932
- Twilio error 30896, opt-in error: https://www.twilio.com/docs/api/errors/30896
- Twilio error 30924, consent language: https://www.twilio.com/docs/api/errors/30924
- Twilio error 30925, unchecked by default: https://www.twilio.com/docs/api/errors/30925
- Twilio, gather the required business information: https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info
- CTIA Messaging Principles and Best Practices (2017 text): https://api.ctia.org/docs/default-source/default-document-library/170119-ctia-messaging-principles-and-best-practices.pdf

Carrier and registry names (Twilio, CTIA, The Campaign Registry) are not white label names, but there is no reason to bring them up with the owner. Say "phone carriers" and "the registration review".

## Billing notes (say these only in Product Champ words)

- On an account provided by an agency, the platform charges the agency wallet first and then tries to rebill the sub-account wallet. Sub-account wallet rebilling does not remove the agency's exposure: a rebill that fails leaves the agency with the cost.
- Before a submission, the points to confirm are the agency's phone and A2P rebilling settings, the member's payment method and wallet funding, and who bears a failed rebill. The owner confirms these with their Product Champ support contact. The agent does not look for or open provider-level screens.
- Owner-facing wording for all of this is in step 9 of `SKILL.md`. Use that wording.

## Not confirmed. Say so plainly if the owner asks.

- The latest CTIA wording. Only the 2017 text could be read.
- Rules published directly by The Campaign Registry. The platform and Twilio apply them, so this kit follows their pages.
- Exact fee amounts. Read the current pricing on screen in the account. Never quote an amount from memory.
- A written rule that says "paid plan first." The platform documentation says an active account is needed. Waiting for the paid plan is this kit's safe default, not a quoted platform rule.
- State laws, HIPAA and industry rules. An attorney must check those.
