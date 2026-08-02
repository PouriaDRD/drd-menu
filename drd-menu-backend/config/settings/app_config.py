"""
Application configuration module.

This module loads all environment variables
and provides centralized access to settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

# Project root (directory containing manage.py and .env)
ROOT_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE, override=False)


@dataclass(frozen=True)
class AppConfig:
    """
    Application configuration.
    """

    debug: bool
    app_name: str
    base_url: str
    admin_url: str
    secret_key: str


@dataclass(frozen=True)
class InternationalizationConfig:
    """
    Internationalization configuration.
    """

    language_code: str
    time_zone: str
    use_i18n: bool
    use_tz: bool


@dataclass(frozen=True)
class AuthConfig:
    """
    Authentication configuration.
    """

    access_token_lifetime: int
    refresh_token_lifetime: int


@dataclass(frozen=True)
class CorsConfig:
    """
    CORS configuration.
    """

    internal_ips: list
    allowed_hosts: list
    allowed_origins: list
    trusted_origins: list
    allow_credentials: bool


@dataclass(frozen=True)
class DatabaseConfig:
    """
    Database configuration.
    """

    use_sqlite: bool
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int


@dataclass(frozen=True)
class MediaConfig:
    """
    Media configuration.
    """

    max_avatar_size: int


class Config:
    """
    Main application configuration class.
    """

    def __init__(self) -> None:
        """
        Initialize all application settings.
        """

        self.app = AppConfig(
            debug=self._get_bool("DEBUG"),
            app_name=self._get_required("APP_NAME"),
            base_url=self._get_required("BASE_URL"),
            admin_url=self._get_required("ADMIN_URL"),
            secret_key=self._get_required("SECRET_KEY"),
        )

        self.i18n = InternationalizationConfig(
            language_code=self._get_required("LANGUAGE_CODE"),
            time_zone=self._get_required("TIME_ZONE"),
            use_i18n=self._get_bool("USE_I18N"),
            use_tz=self._get_bool("USE_TZ"),
        )

        self.media = MediaConfig(
            max_avatar_size=self._get_int("MAX_AVATAR_SIZE_NUMBER"),
        )

        self.auth = AuthConfig(
            access_token_lifetime=self._get_int("ACCESS_TOKEN_LIFETIME"),
            refresh_token_lifetime=self._get_int("REFRESH_TOKEN_LIFETIME"),
        )

        self.cors = CorsConfig(
            allow_credentials=self._get_bool("CORS_ALLOW_CREDENTIALS"),
            allowed_origins=self._get_list("CORS_ALLOWED_ORIGINS"),
            trusted_origins=self._get_list("CSRF_TRUSTED_ORIGINS"),
            internal_ips=self._get_list("INTERNAL_IPS"),
            allowed_hosts=self._get_list("ALLOWED_HOSTS"),
        )

        self.database = DatabaseConfig(
            use_sqlite=self._get_bool("USE_SQLITE"),
            db_name=self._get_required("DB_NAME"),
            db_user=self._get_required("DB_USER"),
            db_password=self._get_required("DB_PASSWORD"),
            db_host=self._get_required("DB_HOST"),
            db_port=self._get_int("DB_PORT"),
        )

    @staticmethod
    def _get_required(key: str) -> str:
        """
        Get required environment variable.

        Args:
            key: Environment variable name.

        Returns:
            str: Environment variable value.

        Raises:
            ValueError: If variable is missing.
        """

        value = os.getenv(key)

        if not value:
            raise ValueError(f"{key} is missing in .env")

        return value

    @staticmethod
    def _get_list(key: str) -> list:
        """
        Get list environment variable.

        Args:
            key: Environment variable name.

        Returns:
            list: Parsed list value.
        """

        value = Config._get_required(key)

        return [item.strip() for item in value.split(",") if item.strip()]

    @staticmethod
    def _get_bool(key: str) -> bool:
        """
        Get boolean environment variable.

        Args:
            key: Environment variable name.

        Returns:
            bool: Parsed boolean value.
        """

        return os.getenv(key, "False").strip().lower() in (
            "true",
            "1",
            "yes",
            "on",
        )

    @staticmethod
    def _get_int(key: str) -> int:
        """
        Get integer environment variable.

        Args:
            key: Environment variable name.

        Returns:
            int: Parsed integer value.
        """

        value = Config._get_required(key)

        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"{key} must be an integer") from exc


# Global configuration instance
config = Config()
