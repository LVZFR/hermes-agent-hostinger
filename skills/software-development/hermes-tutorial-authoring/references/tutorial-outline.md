# Proven beginner-tutorial outline for Hermes Agent

This is the lesson-by-lesson structure that worked for a beginner audience. Reproduce with modifications. Pull all commands from `skill_view(name="hermes-agent")` — do not write them from memory.

## Front matter
- One-line definition: open-source AI agent by Nous Research; runs in terminal, messaging apps, IDEs; uses TOOL CALLING to *do* things, not just chat.
- "How to think about Hermes" mental-model section + the 4-layer table (Persona/Memory/Skills/Config). This table is referenced again in the debugging section.

## Lessons (numbered, why-before-how, copy-paste commands)

0. **Install & first run** — `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`; `hermes`; `hermes chat -q "…"`; `hermes setup`; `hermes doctor`. Verify: `hermes --version`.
1. **Talk to it & read what it's doing** — give a task that triggers a tool (e.g. read a file). Teach `/verbose`, `/reasoning show`, `/usage` so the user can SEE tool calls — the evidence trail for debugging.
2. **Slash commands** — `/new`, `/model`, `/tools`, `/skill <name>`, `/help`, `/undo`, `/retry`, `/quit`. Pitfall: tool/skill changes need `/new`.
3. **Tools & toolsets** — `hermes tools`, `hermes tools list`, `enable/disable`. List the daily-use toolsets (terminal, file, web, browser, code_execution, memory, delegation, cronjob). Debug tip: missing capability = disabled toolset or missing `.env` key.
4. **Memory** — tell it facts in chat; user-profile vs memory stores; what does NOT go in memory (task progress → use session history / `session_search`). `hermes memory status/setup`.
5. **Skills** — `hermes skills list/search/install/browse`; `/skill <name>`. Emphasize the self-improving payoff: it saves procedures and gets better at the user's recurring tasks.
6. **Customizing the persona (SOUL.md)** — at `$HERMES_HOME/SOUL.md`; injected every turn; changes behavior everywhere & permanently; takes effect next session. Show a short concise/educational example.
7. **Gateway (Telegram/Discord/Slack)** — `hermes gateway setup/run/install/status`. Telegram gotcha: user must press Start first; bot can't initiate.
8. **Cron** — `hermes cron create "0 9 * * *"`, `list`, `run`, `pause`, `remove`. Schedules: cron syntax, durations (`30m`/`2h`), phrases (`every monday 9am`).
9. **Profiles** — `hermes profile list/create/use`, `hermes --profile NAME chat`. Fully isolated config/sessions/skills/memory.

## Back matter
- **Key paths cheat sheet** with the `$HERMES_HOME` vs `~/.hermes` caveat (run `hermes config path` / `env-path`).
- **Debugging checklist** mapping symptoms → the 4 layers: wrong tone→SOUL.md; forgot a fact→memory; missing capability→toolset/.env; change didn't apply→`/new` or restart; weird answers→`/verbose` + `/reasoning show`; anything broken→`hermes doctor` then `~/.hermes/logs/`.
- **Where to go next** tailored to the user's stated interests.
