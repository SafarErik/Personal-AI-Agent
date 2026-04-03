import asyncio
import logging
from typing import Any

from personal_ai_agent.telegram.handlers import TelegramMessageHandler
from personal_ai_agent.telegram.models import TelegramMessage

logger = logging.getLogger(__name__)


def extract_message(update: dict[str, Any]) -> TelegramMessage | None:
    payload = update.get("message") or update.get("edited_message")
    if not isinstance(payload, dict):
        return None

    chat = payload.get("chat")
    text = payload.get("text")
    if not isinstance(chat, dict) or "id" not in chat or not isinstance(text, str):
        return None

    sender = payload.get("from") or {}
    username = sender.get("username") if isinstance(sender, dict) else None

    return TelegramMessage(
        update_id=int(update["update_id"]),
        chat_id=int(chat["id"]),
        text=text,
        chat_type=str(chat.get("type", "private")),
        username=username,
    )


class TelegramPollingService:
    def __init__(
        self,
        client: Any,
        handler: TelegramMessageHandler,
        *,
        poll_timeout_seconds: int = 10,
        idle_delay_seconds: float = 1.0,
    ) -> None:
        self._client = client
        self._handler = handler
        self._poll_timeout_seconds = poll_timeout_seconds
        self._idle_delay_seconds = idle_delay_seconds
        self._offset: int | None = None
        self._stop_event = asyncio.Event()

    @property
    def offset(self) -> int | None:
        return self._offset

    async def poll_once(self) -> None:
        updates = await self._client.get_updates(
            offset=self._offset,
            timeout=self._poll_timeout_seconds,
        )

        for update in updates:
            update_id = int(update["update_id"])
            self._offset = update_id + 1

            message = extract_message(update)
            if message is None:
                continue

            reply = self._handler.build_reply(message)
            if reply:
                await self._client.send_message(message.chat_id, reply)

    async def run_forever(self) -> None:
        while not self._stop_event.is_set():
            try:
                await self.poll_once()
            except Exception:
                logger.exception("Telegram polling cycle failed")

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self._idle_delay_seconds,
                )
            except TimeoutError:
                continue

    async def stop(self) -> None:
        self._stop_event.set()
