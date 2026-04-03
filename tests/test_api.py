from fastapi.testclient import TestClient

from personal_ai_agent.config import Settings
from personal_ai_agent.main import create_app


def test_health_endpoint_returns_ok() -> None:
    app = create_app(
        Settings(
            APP_ENVIRONMENT="test",
            TELEGRAM_POLLING_ENABLED=False,
        )
    )

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "test",
        "app_name": "Personal AI Agent",
    }


def test_telegram_status_reports_unconfigured_bot() -> None:
    app = create_app(
        Settings(
            APP_ENVIRONMENT="test",
            TELEGRAM_POLLING_ENABLED=False,
        )
    )

    with TestClient(app) as client:
        response = client.get("/telegram/status")

    assert response.status_code == 200
    assert response.json() == {
        "configured": False,
        "polling_enabled": False,
        "allowed_chat_ids": [],
    }
