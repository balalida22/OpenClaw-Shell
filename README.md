# MVP Terminal AI Agent

A minimal terminal agent that can use either a local LLM (via [Ollama](https://ollama.com)) or Claude via the [Anthropic API](https://www.anthropic.com/). It streams command output and asks for confirmation before executing anything.

---

## Features

- Local execution via Ollama (no cloud keys needed)
- Claude API support (requires `ANTHROPIC_API_KEY`)
- Confirms every command with the user before executing
- Streams live command output as it runs
- Fully configurable via markdown prompt and skill files
- Multi-turn conversation loop with command feedback

---

## Requirements

- Ubuntu Linux (targeted)
- Python (see `pyproject.toml`)
- Ollama installed and running (only needed for local models)
- For Claude models: an Anthropic API key (`ANTHROPIC_API_KEY`)

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ollama-terminal-agent
   cd ollama-terminal-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Pull a model (Ollama mode only)**

   If you are using a local model (i.e., `MODEL` does not start with `claude-`):

   ```bash
   ollama pull mistral-nemo:12b
   ```

4. **Configure the agent**

   - `agent.md` — system prompt defining the agent's behaviour and response format
   - `SKILL.md` — skills/tools the agent knows about (file system, git, networking, etc.)

---

## Usage
```bash
uv run main.py
```

The agent will prompt you for input. For each command the model wants to run, you will be asked to confirm before it executes:

```
User > download the audio from this youtube video: https://youtu.be/...

[Run Command?] yt-dlp -x --audio-format mp3 https://youtu.be/... [y/N] y
[youtube] Extracting URL...
[download] 100% ...
```

---

## Response Format

The agent uses a structured format defined in `agent.md`:

| Prefix | Meaning |
|--------|---------|
| `COMMAND: <cmd>` | Agent wants to run a shell command |
| `FINISH: <summary>` | Task is complete |

---

## Project Structure

```
.
├── main.py       # Main agent loop
├── agent.md       # System prompt
├── SKILL.md       # Skill definitions
└── .env           # Optional env vars (e.g., ANTHROPIC_API_KEY, MODEL)
```

---

## Configuration
The agent picks the backend based on `MODEL`:
- `MODEL` starts with `claude-` -> uses Claude (Anthropic API)
- otherwise -> uses the local Ollama backend

`MODEL` can be set either by editing `MODEL = ...` in `main.py` or by creating a `.env` file in this folder.

### `.env` (recommended)

Create `./.env`:

```bash
# Claude mode:
MODEL=claude-haiku-4-5
ANTHROPIC_API_KEY=your_key_here
```

### Local Ollama mode

```bash
MODEL=qwen3:8b
```

---

## Disclaimer

This agent executes real shell commands on your machine. Always read the proposed command before typing `y`. Do not run untrusted prompt inputs.