from personal_ai_agent.telegram.models import TelegramMessage


class TelegramMessageHandler:
    def __init__(self, allowed_chat_ids: list[int] | None = None) -> None:
        self._allowed_chat_ids = set(allowed_chat_ids or [])

    def build_reply(self, message: TelegramMessage) -> str | None:
        if self._allowed_chat_ids and message.chat_id not in self._allowed_chat_ids:
            return "This chat is not allowed for this bot."

        text = message.text.strip()
        if not text:
            return None

        if text == "/start":
            return (
                "Personal AI Agent is online.\n"
                "Current phase: Telegram transport validation.\n"
                "Next blocks: crawler, Gemini, memory."
            )

        if text == "/help":
            return "Commands: /start, /help, /ping"

        if text == "/ping":
            return "pong"

        return (
            "Message received: "
            f"{text}\n"
            "LLM and crawler are not wired in yet."
        )
