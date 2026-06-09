---
name: hermes-tutorial-authoring
description: "Author beginner/end-user tutorials, guides, and walkthroughs explaining how to USE Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tutorial, documentation, education, hermes, onboarding, beginner]
    related_skills: [hermes-agent, humanizer]
---

# Authoring Hermes Tutorials & Guides

Use this when the user asks you to produce **educational content about how to USE Hermes Agent** for a human audience — beginner tutorials, onboarding guides, walkthroughs, video scripts, or a tutorial repo. This is distinct from the bundled `hermes-agent` skill, which is about *configuring/extending* Hermes for yourself. Here the deliverable is teaching material for a person.

## Ground-truth sourcing (do this FIRST)

Never write Hermes commands or feature claims from memory. They drift. Source from the install itself, in this order:

1. **`skill_view(name="hermes-agent")`** — the authoritative CLI reference, slash-command list, config paths, toolset table, and pitfalls for THIS install. This is the source of record; copy commands verbatim from it.
2. The official docs (`https://hermes-agent.nousresearch.com/docs/`) for anything the skill doesn't cover. Note: the in-app docs URL `claude-code.nousresearch.com/docs` may resolve to an internal/private address and get blocked by `web_extract` — that's fine, the `hermes-agent` skill is usually sufficient on its own.
3. The live install for real paths: tell the reader to run `hermes config path` and `hermes config env-path`, because `$HERMES_HOME` often differs from `~/.hermes` (e.g. `/opt/data` vs `~/.hermes`). Don't hardcode one.

## Confirm format before writing

"Tutorial" is ambiguous and each format is real work. Use `clarify` to pick ONE before writing: (a) single Markdown file, (b) live in-chat walkthrough with real tool calls, (c) multi-lesson GitHub repo, (d) video/narration script. Writing the wrong format wastes the effort.

## Structure that works for beginners

1. **Mental model first.** Open with how Hermes actually works (the tool-calling loop) and the 4-layer table that beginners confuse:

   | Layer | What it is | Where | How to change |
   |---|---|---|---|
   | Persona (SOUL.md) | Personality/voice | `$HERMES_HOME/SOUL.md` | Edit the file |
   | Memory | Durable facts about user/env | `memories/` | `memory` tool / auto |
   | Skills | Reusable procedures | `skills/` | `hermes skills …` |
   | Config | Models, tools, providers, platforms | `~/.hermes/config.yaml` + `.env` | `hermes config …` |

   This table also powers the debugging section — most "why did it do that?" questions map to one of these four layers.

2. **Numbered lessons, copy-paste commands.** Install → chat → slash commands → tools → memory → skills → SOUL.md → gateway → cron → profiles. Each lesson states WHY before the commands.

3. **Bake in the two beginner trip-wires:**
   - Tool/skill changes apply on a NEW session (`/new`), not mid-conversation (prompt-cache reasons). Enabling a tool that "doesn't show up" = forgot to `/new`.
   - Telegram bots CANNOT start a conversation — the user must open the bot and press **Start** first, or the channel directory stays empty and the bot can't message them.

4. **Close with a debugging checklist** mapping symptoms → the 4 layers, plus `hermes doctor` and `~/.hermes/logs/`.

See `references/tutorial-outline.md` for the full lesson-by-lesson outline used as a proven starting template.

## Writing style for THIS user (Don)

Don explicitly wants — and set his SOUL.md to enforce — a specific voice. Tutorials for him MUST follow it:

- **Concise, direct, educational. No fluff, no filler, no flattery.** Lead with the answer/command, then the reasoning.
- **Why before how.** State the reason for each step before the step, so he can follow the intent.
- **Show the steps/process** so he can debug — expose assumptions and decision points. He values being able to spot where something went wrong.
- **Brief.** Shortest wording that still conveys why + steps + result. Short paragraphs, tight bullets over long prose.
- **Tailor the closing** to his interests when relevant: RPA→automation, Cyber Security, Python, GitHub (e.g. point him at the `github-*` skills, cron for recurring checks, profiles for separating coursework from real work).

## Pitfalls

- Don't mirror the upstream docs wholesale — a tutorial is curated, not a doc dump. Pick the 10 things a beginner needs.
- Don't invent slash commands or flags. If unsure, it's in the `hermes-agent` skill or `/help`; check, don't guess.
- Telegram markdown: no pipe tables — they get rewritten. Prefer labeled key:value or bullet lists when the output lands in chat (a saved `.md` file is fine with tables).
