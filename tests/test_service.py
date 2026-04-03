from personal_ai_agent.telegram.handlers import TelegramMessageHandler
from personal_ai_agent.telegram.service import TelegramPollingService, extract_message


class FakeTelegramClient:
    def __init__(self, updates: list[dict]) -> None:
        self._updates = updates
        self.sent_messages: list[tuple[int, str]] = []

    async def get_updates(self, *, offset: int | None = None, timeout: int = 10) -> list[dict]:
        if offset is None:
            return self._updates
        return [item for item in self._updates if int(item["update_id"]) >= offset]

    async def send_message(self, chat_id: int, text: str) -> None:
        self.sent_messages.append((chat_id, text))


async def test_poll_once_replies_to_supported_messages() -> None:
    client = FakeTelegramClient(
        [
            {
                "update_id": 10,
                "message": {
                    "chat": {"id": 555, "type": "private"},
                    "text": "/ping",
                    "from": {"username": "demo_user"},
                },
            }
        ]
    )
    service = TelegramPollingService(
        client,
        TelegramMessageHandler(),
        poll_timeout_seconds=0,
        idle_delay_seconds=0,
    )

    await service.poll_once()

    assert service.offset == 11
    assert client.sent_messages == [(555, "pong")]


def test_extract_message_ignores_non_text_updates() -> None:
    update = {
        "update_id": 20,
        "message": {
            "chat": {"id": 777, "type": "private"},
            "photo": [{"file_id": "abc"}],
        },
    }

    assert extract_message(update) is None
