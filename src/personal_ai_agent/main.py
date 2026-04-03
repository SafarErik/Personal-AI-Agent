import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from personal_ai_agent.config import Settings, get_settings
from personal_ai_agent.telegram.client import TelegramClient
from personal_ai_agent.telegram.handlers import TelegramMessageHandler
from personal_ai_agent.telegram.service import TelegramPollingService


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        telegram_client = None
        telegram_service = None
        polling_task = None

        if app_settings.telegram_bot_token:
            telegram_client = TelegramClient(
                token=app_settings.telegram_bot_token,
                api_base_url=app_settings.telegram_api_base_url,
            )
            telegram_service = TelegramPollingService(
                telegram_client,
                TelegramMessageHandler(app_settings.telegram_allowed_chat_ids),
                poll_timeout_seconds=app_settings.telegram_poll_timeout_seconds,
                idle_delay_seconds=app_settings.telegram_poll_interval_seconds,
            )
            if app_settings.telegram_polling_enabled:
                polling_task = asyncio.create_task(telegram_service.run_forever())

        app.state.settings = app_settings
        app.state.telegram_service = telegram_service

        try:
            yield
        finally:
            if telegram_service is not None:
                await telegram_service.stop()

            if polling_task is not None:
                await polling_task

            if telegram_client is not None:
                await telegram_client.close()

    app = FastAPI(title=app_settings.app_name, lifespan=lifespan)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Personal AI Agent backend is running."}

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "environment": app_settings.environment,
            "app_name": app_settings.app_name,
        }

    @app.get("/telegram/status")
    async def telegram_status() -> dict[str, object]:
        return {
            "configured": bool(app_settings.telegram_bot_token),
            "polling_enabled": app_settings.telegram_polling_enabled,
            "allowed_chat_ids": app_settings.telegram_allowed_chat_ids,
        }

    return app


app = create_app()
