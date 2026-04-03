from uuid import UUID, uuid4
from dataclasses import dataclass
from pathlib import Path
import os
import json
from typing import Any, Self

from .configuration import Config

@dataclass
class Session:
    config: Config
    id: UUID
    model: str
    session_file: str
    messages: list[dict[str, str]]
    token_used: int

    def __init__(self, model: str, config: Config, id: UUID = uuid4(), messages: list[dict[str, str]] | None = None, token_used: int | None = None):
        self.config = config
        self.id = id
        self.model = model
        # Ensure runtime paths exist on first run.
        self.config.session_dir.mkdir(parents=True, exist_ok=True)
        self.config.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = str(config.session_dir / (str(self.id) + ".json"))
        os.chdir(self.config.workspace_dir)
        if messages is None or token_used is None:
            print(f"Initialized session {self.id}")
            self.reset()
            self.save_to_file()
        else:
            self.messages = messages
            self.token_used = token_used
            print(f"Loaded session {self.id}")

    def _load_text(self, path: str) -> str:
        with open(self.config.base_dir / path, "r", encoding="utf-8") as f:
            return f.read()

    def load_system_prompt(self):
        system_prompt = self._load_text("agent.md") + self._load_text("SKILL.md")
        return system_prompt

    def reset(self):
        """Reset conversation history and token usage estimation."""
        system_prompt = self.load_system_prompt()
        self.token_used = int(len(system_prompt) / self.config.chars_per_token_estimate)
        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "Hello! How can I assist you today?"},
        ]
    
    def send_user_message(self, msg: str):
        self.messages.append({"role": "user", "content": msg})
        self.token_used += int(len(msg) / self.config.chars_per_token_estimate)
        self.save_to_file()

    def save_to_file(self):
        Path(self.session_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, "w") as file:
            # TODO: Currently, the thinking processes are not stored in messages. Update this later.
            json.dump(
                {
                    "id": str(self.id),
                    "config": self.config.serialize(),
                    "model": self.model,
                    "token-used": int(self.token_used),
                    "messages": self.messages,
                },
                file
            )

    def load_from_file(path: str) -> Self:
        with open(path, "r") as file:
            obj = json.load(file)
            model = obj["model"]
            config = Config.construct(obj["config"])
            session = Session(model=model, config=config, id=obj["id"], messages=obj["messages"], token_used=obj["token-used"])
            return session

