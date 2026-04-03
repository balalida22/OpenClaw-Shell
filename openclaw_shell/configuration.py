from dataclasses import dataclass

@dataclass
class Config:
    base_dir: str
    model: str
    max_chars: int = 3000
    context: int = 1_024_000
    chars_per_token_estimate: int = 4
    finish_prefix: str = "FINISH:"
    command_key: str = "COMMAND:"
    verbose: bool = True
    think: bool = True
    stylize_with_colorama: bool = True