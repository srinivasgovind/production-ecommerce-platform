"""Settings: values come from env vars, and bad values fail at startup (fail fast)."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from store.config import Settings


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Run every test in an empty temp folder: no .env there, so only env vars + defaults count."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    monkeypatch.setenv("DB_PASSWORD", "test-only")  # required field; a dummy for unit tests


def test_defaults_when_nothing_is_set() -> None:
    settings = Settings()

    assert settings.app_env == "local"
    assert settings.log_level == "INFO"


def test_reads_env_vars_and_uppercases_log_level(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = Settings()

    assert settings.app_env == "production"
    assert settings.log_level == "DEBUG"


def test_unknown_env_name_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "prod")  # typo: must be "production"

    with pytest.raises(ValidationError) as error:
        Settings()

    assert error.value.errors()[0]["loc"] == ("app_env",)  # failed for THIS reason, not another


def test_missing_db_password_fails_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DB_PASSWORD")

    with pytest.raises(ValidationError) as error:
        Settings()

    assert error.value.errors()[0]["loc"] == ("db_password",)


def test_password_is_hidden_when_printed() -> None:
    settings = Settings()

    assert "test-only" not in repr(settings)  # logs/tracebacks show ********** instead
    assert "test-only" not in str(settings.database_url)
