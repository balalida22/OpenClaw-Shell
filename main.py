from pathlib import Path
from dotenv import load_dotenv
import argparse

from openclaw_shell import *

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

MODEL = os.getenv("MODEL", "qwen3:8b")

config = Config(base_dir=BASE_DIR, model=MODEL)

if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="MVP AI agent shell")
    parser.add_argument("-m", "--model", help="The name of the model to chat with.", )
    args = parser.parse_args()
    config.model = args.model
    print("Using model", config.model)

    # Start a session
    tokens_used, messages = reset(config)

    print("[Commands: 'exit' to quit, 'reset' to clear history]")
    while True:
        pct = round((tokens_used / config.context) * 100, 1)
        user_input = input(f"\n[User({pct}%)] ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            tokens_used, messages = reset(config)
            continue
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})
        while True:
            response = chat_with_model(messages, config)
            tokens_used = response.get("prompt_tokens", tokens_used) or tokens_used
            reply = response.get("reply", "")
            # print(f"<DEBUG> {reply} <DEBUG>\n")
            messages.append({"role": "assistant", "content": reply})

            if reply.strip().startswith(config.finish_prefix):
                finish_message = reply.strip().split(config.finish_prefix, 1)[1].strip()
                print(f"\n[Agent] {finish_message}")
                break

            if config.command_key in reply:
                command = reply.strip().split(config.command_key, 1)[1].strip()
                command_result = confirm_and_run(command=command, config=config)
                messages.append({"role": "user", "content": f"EXECUTED {command_result}"})
            else:
                messages.append({
                    "role": "user",
                    "content": """Invalid format.
                        You must reply with one of either `COMMAND: <cmd>` or `FINISH: <msg>`.
                        The word `FINISH` or `COMMAND` should be capitalized and the colon must not be dropped.
                        Try again."""
                })
        # print(messages)