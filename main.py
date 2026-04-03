from pathlib import Path
from dotenv import load_dotenv
import argparse

from openclaw_shell import *

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

MODEL = os.getenv("MODEL", "qwen3.5:9b")

config = Config(
    base_dir=BASE_DIR,
    session_dir=BASE_DIR / "runtime" / "sessions",
    workspace_dir=BASE_DIR / "runtime" / "workspace",
)

if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="MVP AI agent shell")
    parser.add_argument("-m", "--model", help="The name of the model to chat with.", )
    args = parser.parse_args()
    model = args.model or MODEL
    print("Using model", model)

    # Start a session
    s = Session(model=model, config=config)
    # s = Session.load_from_file(BASE_DIR / "runtime" / "sessions" / "e7b84b5d-3423-49bb-8965-bac3c0631063.json")

    print("[Commands: 'exit' to quit, 'reset' to clear history]")
    while True:
        pct = round((s.token_used / s.config.context) * 100, 1)
        user_input = input(f"\n[User({pct}%)] ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            s.reset()
            continue
        if not user_input:
            continue
        s.send_user_message(user_input)
        while True:
            reply = chat_with_model(s)
            # print(f"<DEBUG> {reply} <DEBUG>\n")

            if reply.strip().startswith(s.config.finish_prefix):
                finish_message = reply.strip().split(s.config.finish_prefix, 1)[1].strip()
                print(f"\n[Agent] {finish_message}")
                break

            if s.config.command_key in reply:
                command = reply.strip().split(s.config.command_key, 1)[1].strip()
                command_result = confirm_and_run(command=command, config=s.config)
                s.send_user_message(f"EXECUTED {command_result}")
            else:
                s.send_user_message("""Invalid format.
You must reply with one of either `COMMAND: <cmd>` or `FINISH: <msg>`.
The word `FINISH` or `COMMAND` should be capitalized and the colon must not be dropped.
Try again."""
                )
        # print(messages)