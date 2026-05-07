from config.settings import Settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("TELEGRAM_TOKEN", "mock_telegram_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    monkeypatch.setenv("FREELANCEHUNT_URL", "https://example.com")
    monkeypatch.setenv("FREELANCEHUNT_ENDPOINT", "/projects?skills%5B0%5D=1")
    monkeypatch.setenv("PARSE_INTERVAL_SECONDS", "600")

    settings = Settings()

    assert settings.TELEGRAM_TOKEN == "mock_telegram_token"
    assert settings.TELEGRAM_CHAT_ID == "123456"
    assert settings.FREELANCEHUNT_URL == "https://example.com"
    assert settings.FREELANCEHUNT_ENDPOINT == "/projects?skills%5B0%5D=1"
    assert settings.PARSE_INTERVAL_SECONDS == 600
