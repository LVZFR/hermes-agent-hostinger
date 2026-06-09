# Hermes Agent — A Beginner's Tutorial

> An open-source AI agent by Nous Research that runs in your terminal, in messaging apps (Telegram, Discord, Slack…), and in your IDE. It uses **tool calling** to actually *do* things on your machine — run commands, read/write files, search the web — not just chat.

This guide takes you from zero to a working, customized agent. Each lesson states **what** you'll do and **why** it matters. Copy the commands as-is.

---

## How to think about Hermes (mental model)

Before commands, here's the model. Hermes is a loop:

1. You send a message.
2. Hermes builds a **system prompt** (its identity + your memory + loaded skills + environment facts).
3. The LLM decides: reply with text, OR call a **tool** (run a command, read a file, search the web).
4. If it calls a tool, the result is fed back in and the loop repeats — until it has an answer.

Four things shape its behavior, and it's worth knowing which is which because they're edited differently:

| Layer | What it is | Where it lives | How you change it |
|---|---|---|---|
| **Persona (SOUL.md)** | Its personality/voice | `$HERMES_HOME/SOUL.md` | Edit the file |
| **Memory** | Durable facts about you & your environment | `memories/` | The `memory` tool / auto-saved |
| **Skills** | Reusable procedures it loads on demand | `skills/` | `hermes skills …` |
| **Config** | Models, tools, providers, platforms | `~/.hermes/config.yaml` + `.env` | `hermes config …` |

Keep this table in mind — most "why did it do that?" questions trace back to one of these four layers.

---

## Lesson 0 — Install & first run

**Why:** You need the `hermes` binary on your PATH before anything else.

```bash
# Install (Linux / macOS / WSL)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Start an interactive chat (this is the default command)
hermes

# Or fire a single question and exit (non-interactive)
hermes chat -q "What is the capital of France?"

# Run the setup wizard if you want guided configuration
hermes setup

# Health check — run this any time something feels broken
hermes doctor
```

**Verify it worked:** `hermes --version` prints a version. `hermes doctor` reports green.

---

## Lesson 1 — Talk to it, and read what it's doing

**Why:** The whole point of an agent (vs. a chatbot) is that it runs tools. Learn to *watch* that happen so you can debug.

Start a session with `hermes`, then try:

```
Read the file ~/.bashrc and tell me what aliases I have.
```

Watch the output. You'll see it call the **`read_file`** tool, get the contents, then summarize. If you ever wonder *why* it answered a certain way, the tool calls are the evidence trail.

Useful in-session toggles for visibility:

```
/verbose          # cycle how much tool detail is shown: off → new → all → verbose
/reasoning show   # show the model's reasoning (set to "hide" to turn off)
/usage            # token usage for this session
```

---

## Lesson 2 — Slash commands (your in-session control panel)

**Why:** Slash commands control the session without leaving chat. These are the ones a beginner uses daily.

```
/new            # start a fresh session (clears context)
/model          # show or change the LLM model
/tools          # enable/disable tools
/skill <name>   # load a specific skill into this session
/help           # full, always-current list
/undo           # remove the last exchange
/retry          # resend your last message
/quit           # exit
```

**Pitfall:** Tool and skill changes take effect on a **new session** (`/new`), not mid-conversation. This is deliberate — it keeps the prompt cache intact (cheaper, faster). If you enable a tool and it "doesn't show up," run `/new`.

---

## Lesson 3 — Tools & toolsets (what the agent can actually do)

**Why:** Tools are the agent's hands. If a capability is missing, it's usually a disabled toolset or a missing API key — not a broken agent.

```bash
hermes tools             # interactive enable/disable UI
hermes tools list        # show every tool + status
hermes tools enable web  # turn on web search + extraction
hermes tools disable browser
```

Common toolsets worth knowing:

- **`terminal`** — run shell commands & manage processes
- **`file`** — read / write / search / patch files
- **`web`** — web search + page extraction (`search` is the search-only subset)
- **`browser`** — full browser automation
- **`code_execution`** — sandboxed Python
- **`memory`** — persistent cross-session memory
- **`delegation`** — spawn subagents for parallel subtasks
- **`cronjob`** — schedule recurring tasks

**Debug tip:** If a tool exists but errors, check `.env` for a required API key (`hermes config env-path` prints the file location), then `hermes doctor`.

---

## Lesson 4 — Memory (so you don't repeat yourself)

**Why:** Hermes remembers facts about you across sessions. This is what makes it feel like *your* agent, not a fresh stranger each time.

Just tell it things in chat:

```
Remember that I prefer concise answers and I use Python with type hints.
```

It saves that to memory, and it's injected into every future session. Two stores exist:

- **user profile** — who you are (name, role, preferences)
- **memory** — environment facts, conventions, lessons learned

**What NOT to expect in memory:** task progress or "what did we do last week." That lives in **session history**, searchable via the `session_search` tool — ask "what were we working on with the X project?" and it digs through past transcripts.

Manage the memory backend:

```bash
hermes memory status
hermes memory setup
```

---

## Lesson 5 — Skills (the self-improving part)

**Why:** A skill is a saved *procedure* — a markdown document with steps, commands, and pitfalls. When a task matches, Hermes loads the skill and follows it. This is how the agent gets better at *your* recurring tasks over time.

```bash
hermes skills list             # what's installed
hermes skills search github    # search the skills hub
hermes skills install <id>     # install one (id or a direct …/SKILL.md URL)
hermes skills browse           # browse everything available
```

In-session, force-load one with `/skill <name>`.

**The payoff:** After Hermes solves something tricky, it can save the approach as a new skill. Next time, it doesn't re-derive it — it just loads the skill. Over weeks, your install accumulates expertise tuned to your environment.

For you specifically (RPA + GitHub + Python), browse the `github` skills — there are ready-made ones for PR workflows, code review, and repo management.

---

## Lesson 6 — Customizing the persona (SOUL.md)

**Why:** `SOUL.md` is the personality layer injected into the system prompt every turn. Editing it changes how the agent behaves **everywhere, permanently** — unlike memory (facts) or skills (procedures).

```bash
# Find it (it's at $HERMES_HOME/SOUL.md, e.g. /opt/data/SOUL.md)
hermes config path        # shows config dir; SOUL.md sits alongside

# Edit it in your editor
$EDITOR $HERMES_HOME/SOUL.md
```

Keep the first line (its identity) and add behavior directives. Example — a concise, educational persona:

```markdown
You are Hermes Agent, created by Nous Research.

## Voice
Be concise, direct, and educational. No fluff. Lead with the answer,
then the reasoning. Explain WHY before HOW. Show the steps you take so
the user can follow your logic and debug your responses.
```

**Takes effect:** on the next session/restart (the persona is read at startup).

---

## Lesson 7 — Connect to Telegram (or Discord, Slack…)

**Why:** The "gateway" lets the same agent — with full tool access — run inside a messaging app. You can text your agent from your phone.

```bash
hermes gateway setup     # configure a platform (interactive)
hermes gateway run       # run in the foreground (good for testing)
hermes gateway install   # install as a background service
hermes gateway status    # is it running?
```

**Telegram gotcha (very common):** A bot **cannot start a conversation** — *you* must open the bot in Telegram and press **Start** / send any message first. Until you do, the bot's channel directory is empty and it can't message you. If config looks correct but nothing happens: (1) is the gateway actually running? (2) did you message the bot first? (3) is your numeric Telegram user ID in the allowed-users list?

---

## Lesson 8 — Scheduled tasks (cron)

**Why:** Hermes can run jobs on a schedule and deliver results to you — a daily briefing, a repo-watch, a reminder.

```bash
hermes cron create "0 9 * * *"   # daily at 9am (then follow prompts)
hermes cron list                 # see jobs
hermes cron run <id>             # trigger now
hermes cron pause <id>
hermes cron remove <id>
```

Schedules accept cron syntax (`0 9 * * *`), durations (`30m`, `2h`), or phrases (`every monday 9am`).

---

## Lesson 9 — Profiles (multiple independent agents)

**Why:** A profile is a fully isolated Hermes instance — its own config, sessions, skills, and memory. Use one for work, one for a personal project, one for experiments — they never bleed into each other.

```bash
hermes profile list
hermes profile create work
hermes profile use work         # set as default
hermes --profile work chat      # one-off use
```

---

## Key paths cheat sheet

```
$HERMES_HOME/SOUL.md        # the persona you edit
~/.hermes/config.yaml       # main config (models, tools, platforms)
~/.hermes/.env              # API keys & secrets
$HERMES_HOME/skills/        # installed skills
$HERMES_HOME/memories/      # memory files
~/.hermes/state.db          # session history (SQLite, full-text searchable)
~/.hermes/logs/             # gateway & error logs
```

> Note: `$HERMES_HOME` may differ from `~/.hermes`. On this install it's a separate dir. Run `hermes config path` and `hermes config env-path` to see the real locations.

---

## Debugging checklist (the "why is it doing that?" flowchart)

1. **Wrong personality / tone?** → `SOUL.md`. Edit it, start a new session.
2. **Forgot something about me?** → Memory. Tell it to remember, or check `hermes memory status`.
3. **Missing a capability?** → Toolset disabled (`hermes tools list`) or missing API key (`.env`).
4. **Change didn't apply?** → Tools/skills need `/new`; config needs a restart; gateway needs `/restart`.
5. **Wrong answers / weird behavior?** → `/verbose` and `/reasoning show` to see the tool calls and reasoning trail.
6. **Anything broken?** → `hermes doctor` first, then check `~/.hermes/logs/`.

---

## Where to go next

```bash
hermes --help          # all CLI commands
/help                  # all slash commands (in-session)
hermes skills browse   # find skills for your workflows
hermes insights        # your usage analytics
```

For your goals (RPA → automation, Cyber Security, Python, GitHub):
- Wire up the **`github`** skills for PR and repo workflows.
- Use **cron** to schedule recurring security/automation checks.
- Use **profiles** to keep coursework, experiments, and real work separate.

---

*Built as a beginner walkthrough of Hermes Agent. Commands verified against the local install's CLI reference.*
