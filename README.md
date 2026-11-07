# Hire Your AI Agent Starter Skills

Four free starter skills for Hermes, from Truly Authentic Marketing. They go with the Hire Your AI Agent challenge: 3 days to install Hermes, hire an AI employee in Product Champ, and build a quiz lead magnet.

Each skill drafts and plans. None of them sends, publishes, spends, or changes an account without your approval.

## The skills

| Skill | Day | What it does |
|---|---|---|
| `company-brain-starter` | Day 1 | Interviews you one question at a time, reads your website, shows a preview, then saves a starter Company Brain. Ends with a summary and your 3 biggest gaps. |
| `dream-customer-avatar-starter` | Day 2 | Interviews you and writes one customer profile. Gives you a block to paste into your Product Champ AI employee. |
| `convert-follow-up-loop` | Day 2 and 3 | Maps how a lead is captured, answered, qualified, booked, and followed up. Drafts the quiz follow up messages. |
| `organic-content-engine` | After Day 3 | Turns one buyer question into a week of posts that point to your quiz. |

## Install

You need the Hermes desktop app: https://hermes-agent.nousresearch.com/desktop

The easy way: open a new Hermes chat and paste this prompt.

```text
Install these four free starter skills from the public repo https://github.com/keepinitgreen93/hire-your-ai-agent-starter-skills. Use these exact paths with "hermes skills install <path> --yes" and do not change them:
keepinitgreen93/hire-your-ai-agent-starter-skills/skills/company-brain-starter
keepinitgreen93/hire-your-ai-agent-starter-skills/skills/dream-customer-avatar-starter
keepinitgreen93/hire-your-ai-agent-starter-skills/skills/convert-follow-up-loop
keepinitgreen93/hire-your-ai-agent-starter-skills/skills/organic-content-engine
Confirm each one is installed. If one fails, show me the exact command to run myself and keep going.
```

If Hermes cannot install a skill, it will show you the exact command. You can also run the commands yourself. Open a terminal (PowerShell on Windows, Terminal on a Mac) and paste these four lines:

```text
hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/company-brain-starter --yes
hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/dream-customer-avatar-starter --yes
hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/convert-follow-up-loop --yes
hermes skills install keepinitgreen93/hire-your-ai-agent-starter-skills/skills/organic-content-engine --yes
```

Then start a new Hermes chat. Ask: "Which of my installed skills came from Truly Authentic Marketing?"

To install one skill, run only its line.

## Tools these skills use

- Hermes desktop app, running on your own Claude subscription.
- Product Champ, TAM's white label of HighLevel. Hermes connects through HighLevel's official MCP server (https://services.leadconnectorhq.com/mcp/) with a Private Integration Token and your Location ID. Start read only. Keep the token private. Never paste it into a chat.
- Composio, for other apps.
- Firecrawl, or the Hermes web tools, to read your website.

## Safety rules built into every skill

- No sends, posts, spend, or account changes without your yes.
- No made up proof, reviews, prices, or results. Gaps are marked `[PLACEHOLDER]` or `[REAL PROOF NEEDED]`.
- No passwords, tokens, or keys in chat.

## Check the skills yourself

```text
python scripts/validate_library.py
```

## Need a hand?

Feeling stuck or want it set up with you? [Here is how we can help.](https://docs.google.com/document/d/1WA1I6jKwomToqweTzdFSOvQb0Kc-mzja-r56Iojj4nk/edit)

## License

MIT. See LICENSE.
