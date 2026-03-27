"""
Interactive MVP agent runner.

The agent reads prompt context from `agent.md` and `SKILL.md`, then loops over
user input, calling `ollama.chat()` and executing commands returned as:
`COMMAND: <shell command>`.
"""

from __future__ import annotations

import subprocess
from typing import Any

import ollama

MODEL = "qwen3:8b"

MAX_CHARS = 3000
CONTEXT = 1_024_000
CHARS_PER_TOKEN_ESTIMATE = 4

FINISH_PREFIX = "FINISH:"
COMMAND_KEY = "COMMAND:"


def _load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


system_prompt = _load_text("agent.md") + _load_text("SKILL.md")
tokens_used: float = len(system_prompt) / CHARS_PER_TOKEN_ESTIMATE
messages: list[dict[str, str]] = []

def truncate_output(output: str, max_chars: int = MAX_CHARS) -> str:
    if len(output) <= max_chars:
        return output
    half = max_chars // 2
    omitted = len(output) - max_chars
    return output[:half] + f"\n\n... ({omitted} chars omitted) ...\n\n" + output[-half:]


def confirm_and_run(command: str, verbose: bool = True) -> str:
    choice = input(f"\n[Run Command?] {command} [y/N] ").strip().lower()
    if choice != "y":
        return "User chose not to execute the command."
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output_lines = []
    for line in process.stdout:
        output_lines.append(line)
        if verbose:
            print(line, end="", flush=True)
    process.wait()
    return_code = process.returncode
    output = truncate_output("".join(output_lines))
    return output if output else f"(exit code {return_code}, no output)"


def reset() -> tuple[float, list[dict[str, str]]]:
    """Reset conversation history and token usage estimation."""
    new_tokens_used = len(system_prompt) / CHARS_PER_TOKEN_ESTIMATE
    new_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
    ]
    return new_tokens_used, new_messages


tokens_used, messages = reset()

print("[Commands: 'exit' to quit, 'reset' to clear history]")
while True:
    pct = round((tokens_used / CONTEXT) * 100, 1)
    user_input = input(f"\n[User({pct}%)] ")
    if user_input.lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    if user_input.lower() == "reset":
        tokens_used, messages = reset()
        continue
    if not user_input:
        continue
    messages.append({"role": "user", "content": user_input})
    while True:
        response: dict[str, Any] = ollama.chat(
            model=MODEL,
            messages=messages,
            # options={"temperature": 0.1},
            think=True,
        )

        tokens_used = response.get("prompt_eval_count", tokens_used)
        reply = response["message"]["content"]
        messages.append({"role": "assistant", "content": reply})

        if reply.strip().startswith(FINISH_PREFIX):
            finish_message = reply.strip().split(FINISH_PREFIX, 1)[1].strip()
            print(f"\n[Agent] {finish_message}")
            break

        if COMMAND_KEY in reply:
            command = reply.strip().split(COMMAND_KEY, 1)[1].strip()
            command_result = confirm_and_run(command=command, verbose=True)
            messages.append({"role": "user", "content": f"EXECUTED {command_result}"})
        else:
            messages.append({"role": "user", "content": "Invalid format. You must reply with either COMMAND: <cmd> or FINISH: <msg>. Try again."})
    # print(messages)