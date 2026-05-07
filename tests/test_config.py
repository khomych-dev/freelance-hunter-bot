from config.settings import Settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("TELEGRAM_TOKEN", "mock_telegram_token")
    monkeypatch.setenv("FREELANCEHUNT_URL", "https://example.com")
    monkeypatch.setenv("PARSE_INTERVAL_SECONDS", "600")

    settings = Settings()

    assert settings.TELEGRAM_TOKEN == "mock_telegram_token"
    assert settings.FREELANCEHUNT_URL == "https://example.com"
    assert settings.PARSE_INTERVAL_SECONDS == 600
