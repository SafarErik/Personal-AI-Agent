from dataclasses import dataclass


@dataclass(slots=True)
class TelegramMessage:
    update_id: int
    chat_id: int
    text: str
    chat_type: str = "private"
    username: str | None = None
