import json

import httpx

from personal_ai_agent.telegram.client import TelegramClient


async def test_get_updates_calls_expected_bot_api_endpoint() -> None:
    captured: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["payload"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={"ok": True, "result": [{"update_id": 1}]},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.telegram.org/bottest-token/",
    ) as http_client:
        client = TelegramClient(token="test-token", http_client=http_client)
        updates = await client.get_updates(offset=42, timeout=7)

    assert updates == [{"update_id": 1}]
    assert captured == {
        "path": "/bottest-token/getUpdates",
        "payload": {"offset": 42, "timeout": 7},
    }
