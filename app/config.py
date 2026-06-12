"""Configuration objects loaded from environment variables.

Secrets and environment-specific settings are read from the environment
(optionally via a local ``.env`` file) so that nothing sensitive is ever
committed to source control. See ``.env.example`` for the full list.
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Base configuration shared by every environment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # Database — defaults to a local SQLite file, override with DATABASE_URL
    # (e.g. ``mysql+pymysql://...`` or ``postgresql+psycopg://...``).
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Session / cookie hardening
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE"), False)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # CSRF
    WTF_CSRF_TIME_LIMIT = 3600

    # Pagination
    BOOKINGS_PER_PAGE = int(os.environ.get("BOOKINGS_PER_PAGE", "8"))

    # Branding (surfaced in templates / footer)
    PROJECT_NAME = os.environ.get("PROJECT_NAME", "CineBook")
    THEATRE_NAME = os.environ.get("THEATRE_NAME", "Pallavan Theatre")

    @staticmethod
    def init_app(app) -> None:  # noqa: ANN001
        """Hook for environment-specific initialisation."""


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "testing-secret"


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE"), True)

    @classmethod
    def init_app(cls, app) -> None:  # noqa: ANN001
        Config.init_app(app)
        if app.config["SECRET_KEY"] == "dev-only-change-me":
            raise RuntimeError(
                "SECRET_KEY must be set to a strong random value in production."
            )


_CONFIG_REGISTRY = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def config_by_name(name: str | None) -> type[Config]:
    """Resolve a config class by name, honouring ``FLASK_CONFIG``."""
    resolved = name or os.environ.get("FLASK_CONFIG", "development")
    return _CONFIG_REGISTRY.get(resolved, DevelopmentConfig)
