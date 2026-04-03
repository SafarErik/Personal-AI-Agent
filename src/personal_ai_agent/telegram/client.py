import httpx


class TelegramAPIError(RuntimeError):
    """Raised when the Telegram Bot API returns an error."""


class TelegramClient:
    def __init__(
        self,
        token: str,
        api_base_url: str = "https://api.telegram.org",
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            base_url=f"{api_base_url.rstrip('/')}/bot{token}/",
            timeout=30.0,
        )

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def get_updates(
        self,
        *,
        offset: int | None = None,
        timeout: int = 10,
    ) -> list[dict]:
        payload: dict[str, int] = {"timeout": timeout}
        if offset is not None:
            payload["offset"] = offset

        data = await self._post("getUpdates", payload)
        result = data.get("result", [])
        return result if isinstance(result, list) else []

    async def send_message(self, chat_id: int, text: str) -> dict:
        data = await self._post(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
            },
        )
        return data.get("result", {})

    async def _post(self, endpoint: str, payload: dict) -> dict:
        response = await self._client.post(endpoint, json=payload)
        response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            description = data.get("description", "Unknown Telegram API error")
            raise TelegramAPIError(description)

        return data
