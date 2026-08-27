import os
from pathlib import Path
from datetime import timedelta

from ..app_config import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

GEOIP_PATH = BASE_DIR / "geoip"

SECRET_KEY = config.app.secret_key

USE_SQLITE = config.database.use_sqlite


AUTH_USER_MODEL = "accounts.UserModel"

AUTHENTICATION_BACKENDS = [
    "authentication.backends.LoginHistoryBackend",
    # "django.contrib.auth.backends.ModelBackend",
]


# ---------------------------------------------------------------
# Installed Apps Configuration
# ---------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "django_cleanup.apps.CleanupSelectedConfig",
    "drf_spectacular",
]

LOCAL_APPS = [
    "accounts",
    "authentication",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ---------------------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------
# URL Configuration
# ---------------------------------------------------------------
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------
LANGUAGE_CODE = config.i18n.language_code

TIME_ZONE = config.i18n.time_zone

USE_I18N = config.i18n.use_i18n

USE_TZ = config.i18n.use_tz

# ---------------------------------------------------------------
# Static & Media Files
# ---------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# ---------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = config.cors.allow_credentials
CORS_ALLOWED_ORIGINS = config.cors.allowed_origins
CSRF_TRUSTED_ORIGINS = config.cors.trusted_origins

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


INTERNAL_IPS = config.cors.internal_ips
ALLOWED_HOSTS = config.cors.allowed_hosts


# ---------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------
if not USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.database.db_name,
            "USER": config.database.db_user,
            "PASSWORD": config.database.db_password,
            "HOST": config.database.db_host,
            "PORT": config.database.db_port,
        }
    }
else:
    if config.app.debug:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "dev_db.sqlite3",
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "prod_db.sqlite3",
            }
        }

# ---------------------------------------------------------------
# Simple JWT Configuration
# ---------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config.auth.access_token_lifetime),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config.auth.refresh_token_lifetime),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "UPDATE_LAST_LOGIN": True,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ---------------------------------------------------------------
# Django REST Framework Spectacular Configuration
# ---------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": f"{config.app.app_name} API",
    "DESCRIPTION": f"{config.app.app_name} API Documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# =============================================================================
# Logging
# =============================================================================

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # =========================================================================
    # Formatters
    # =========================================================================
    "formatters": {
        "verbose": {
            "format": ("{asctime} {levelname} " "[{module}:{lineno}] {message}"),
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {
            "format": ("{asctime} {levelname} {message}"),
            "style": "{",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    # =========================================================================
    # Filters
    # =========================================================================
    "filters": {
        "info_only": {
            "()": "core.logging.ExactLevelFilter",
            "level": 20,
        },
        "warning_only": {
            "()": "core.logging.ExactLevelFilter",
            "level": 30,
        },
    },
    # =========================================================================
    # Handlers
    # =========================================================================
    "handlers": {
        # ---------------------------------------------------------------------
        # INFO
        # ---------------------------------------------------------------------
        "info_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "info.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": [
                "info_only",
            ],
        },
        # ---------------------------------------------------------------------
        # WARNING
        # ---------------------------------------------------------------------
        "warning_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "warning.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": [
                "warning_only",
            ],
        },
        # ---------------------------------------------------------------------
        # ERROR
        # ---------------------------------------------------------------------
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "error.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        # ---------------------------------------------------------------------
        # Console
        # ---------------------------------------------------------------------
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    # =========================================================================
    # Loggers
    # =========================================================================
    "loggers": {
        # ---------------------------------------------------------------------
        # Application logs
        # ---------------------------------------------------------------------
        "": {
            "handlers": [
                "console",
                "info_file",
                "warning_file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        # ---------------------------------------------------------------------
        # Django
        # ---------------------------------------------------------------------
        "django": {
            "handlers": [
                "console",
                "info_file",
                "warning_file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        # ---------------------------------------------------------------------
        # Django request errors
        # ---------------------------------------------------------------------
        "django.request": {
            "handlers": [
                "error_file",
                "console",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        # ---------------------------------------------------------------------
        # Django development server
        # ---------------------------------------------------------------------
        "django.server": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": False,
        },
    },
}
