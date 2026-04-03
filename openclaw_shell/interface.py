"""
Interactive MVP agent runner.

The agent reads prompt context from `agent.md` and `SKILL.md`, then loops over
user input, calling either Ollama (local) or Claude API and executing commands returned as:
`COMMAND: <shell command>`.
"""


import os
import subprocess
from typing import Any

import asyncio
import anthropic
import ollama
import colorama

from .configuration import Config

def _load_text(path: str, config: Config) -> str:
    with open(config.base_dir / path, "r", encoding="utf-8") as f:
        return f.read()


def _is_claude_model(model: str) -> bool:
    return model.startswith("claude-")


def _chat_with_ollama(chat_messages: list[dict[str, str]], config: Config) -> dict[str, Any]:
    response: dict[str, Any] = ollama.chat(
        model=config.model,
        messages=chat_messages,
        # options={"temperature": 0.1},
        think=config.think,
    )
    return {
        "reply": response["message"]["content"],
        "prompt_tokens": response.get("prompt_eval_count"),
    }

async def _stream_chat_with_ollama(chat_messages: list[dict[str, str]], config: Config) -> dict[str, Any]:
    reply = ""
    prompt_tokens = 0
    is_thinking = config.think

    if is_thinking:
        if config.stylize_with_colorama:
            print(colorama.Style.DIM, end="")
        print("Thinking:")

    async for part in await ollama.AsyncClient().chat(
        model=config.model,
        messages=chat_messages,
        # options={"temperature": 0.1},
        think=config.think,
        stream=True
    ):
        reply += part["message"]["content"]
        if part.get("prompt_eval_count") is int:
            prompt_tokens += part.get("prompt_eval_count")
        if is_thinking and "thinking" in part["message"]:
            print(part["message"]["thinking"], end="", flush=True)
        elif is_thinking:
            is_thinking = False
            if config.stylize_with_colorama:
                print(colorama.Style.RESET_ALL)
                print()
        else:
            # TODO: the first token might have some characters missing. Fix it.
            print(part["message"]["content"], end="", flush=True)
    print()
    return {
        "reply": reply,
        "prompt_tokens": prompt_tokens,
    }

def _chat_with_claude(chat_messages: list[dict[str, str]], config: Config) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Set it before using Claude models."
        )

    system_parts = [m["content"] for m in chat_messages if m["role"] == "system"]
    non_system_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in chat_messages
        if m["role"] in {"user", "assistant"}
    ]

    if not non_system_messages:
        non_system_messages = [{"role": "user", "content": "Hello."}]

    client = anthropic.Anthropic(api_key=api_key)
    kwargs: dict[str, Any] = {
        "model": config.model,
        "messages": non_system_messages,
        "max_tokens": 1024,
    }
    if system_parts:
        kwargs["system"] = "\n\n".join(system_parts)

    response = client.messages.create(**kwargs)
    reply_text = "".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    )
    input_tokens = getattr(response.usage, "input_tokens", None)
    return {"reply": reply_text, "prompt_tokens": input_tokens}


def chat_with_model(chat_messages: list[dict[str, str]], config: Config) -> dict[str, Any]:
    """Call the correct backend based on the model name."""
    if _is_claude_model(config.model):
        return _chat_with_claude(chat_messages, config)
    return asyncio.run(_stream_chat_with_ollama(chat_messages, config))

def load_system_prompt(config: Config):
    system_prompt = _load_text("agent.md", config) + _load_text("SKILL.md", config)
    return system_prompt

def truncate_output(output: str, max_chars: int) -> str:
    if len(output) <= max_chars:
        return output
    half = max_chars // 2
    omitted = len(output) - max_chars
    return output[:half] + f"\n\n... ({omitted} chars omitted) ...\n\n" + output[-half:]


def confirm_and_run(command: str, config: Config) -> str:
    msg = (
        colorama.Fore.YELLOW
        + "\n[Run Command?] "
        + colorama.Fore.CYAN
        + command
        + colorama.Style.RESET_ALL
        + colorama.Fore.YELLOW
        + " [y/N] "
        + colorama.Style.RESET_ALL
    ) if config.stylize_with_colorama else f"\n[Run Command?] {command} [y/N] "
    choice = input(msg).strip().lower()
    if choice != "y":
        msg = (colorama.Fore.YELLOW + "Please give a reason: " + colorama.Style.RESET_ALL) if config.stylize_with_colorama else "Please give a reason: "
        reason = input(msg).strip().lower()
        return f"User chose not to execute the command. Reason: {'unspecified' if reason == '' else reason}."
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
        if config.verbose:
            print(line, end="", flush=True)
    process.wait()
    return_code = process.returncode
    output = truncate_output("".join(output_lines), config.max_chars)
    return output if output else f"(exit code {return_code}, no output)"


def reset(config: Config) -> tuple[float, list[dict[str, str]]]:
    """Reset conversation history and token usage estimation."""
    system_prompt = load_system_prompt(config)
    new_tokens_used = len(system_prompt) / config.chars_per_token_estimate
    new_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
    ]
    return new_tokens_used, new_messages

