# Ollama Terminal Agent

A minimal, local AI agent that runs in your terminal. Powered by [Ollama](https://ollama.com), it lets a local LLM reason through tasks and execute shell commands on your Ubuntu machine — with your approval every step of the way.

---

## Features

- Runs entirely locally via Ollama — no cloud API keys needed
- Confirms every command with the user before executing
- Streams live command output as it runs
- Fully configurable via markdown prompt and skill files
- Multi-turn conversation loop with command feedback

---

## Requirements

- Ubuntu Linux
- Python 3.8+
- [Ollama](https://ollama.com) installed and running

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ollama-terminal-agent
   cd ollama-terminal-agent
   ```

2. **Install dependencies**
   ```bash
   pip install ollama
   ```

3. **Pull a model**
   ```bash
   ollama pull mistral-nemo:12b
   ```

4. **Configure the agent**

   - `agent.md` — system prompt defining the agent's behaviour and response format
   - `SKILL.md` — skills/tools the agent knows about (file system, git, networking, etc.)

---

## Usage

```bash
python agent.py
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
└── SKILL.md       # Skill definitions
```

---

## Configuration

Change the model by editing this line in `agent.py`:

```python
MODEL = "mistral-nemo:12b"
```

Any model available via `ollama list` can be used.

---

## Disclaimer

This agent executes real shell commands on your machine. Always read the proposed command before typing `y`. Do not run untrusted prompt inputs.