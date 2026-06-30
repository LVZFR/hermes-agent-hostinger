[hermes-agent-hostinger_README.md](https://github.com/user-attachments/files/29492258/hermes-agent-hostinger_README.md)

# Hermes Agent — Self-Hosted Agent Gateway

An autonomous agent gateway running on a Hostinger Ubuntu VPS. Provides the
LLM backend, skill registry, and messaging-platform dispatch that higher-level
agent applications (such as Forge) run on top of.

## Components
- **Gateway** — message routing and platform dispatch
- **Skill registry** — loadable skills injected into agent turns
- **LLM backend** — pluggable model integration (Ollama / OpenRouter)
- **Telegram adapter** — bot interface with auth and allow-listing

## Tech Stack
Python · Linux (Ubuntu) · Ollama / OpenRouter · Telegram Bot API · systemd

*Self-hosted infrastructure project exploring agent frameworks and
LLM backend integration on bare-metal/VPS Linux.*
