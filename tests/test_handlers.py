from personal_ai_agent.telegram.handlers import TelegramMessageHandler
from personal_ai_agent.telegram.models import TelegramMessage


def test_ping_command_returns_pong() -> None:
    handler = TelegramMessageHandler()

    reply = handler.build_reply(
        TelegramMessage(update_id=1, chat_id=100, text="/ping")
    )

    assert reply == "pong"


def test_disallowed_chat_receives_access_message() -> None:
    handler = TelegramMessageHandler(allowed_chat_ids=[123])

    reply = handler.build_reply(
        TelegramMessage(update_id=1, chat_id=999, text="hello")
    )

    assert reply == "This chat is not allowed for this bot."
