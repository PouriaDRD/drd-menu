from .base import *

DEBUG = False
ENABLE_DEBUG_TOOLBAR = False


# ---------------------------------------------------------------
# Django REST Framework Configuration
# ---------------------------------------------------------------
REST_FRAMEWORK = {
    # Schema
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Renderers
    "DEFAULT_RENDERER_CLASSES": [
        "core.renderers.api_renderer.ApiRenderer",
    ],
    # Exception Handler
    "EXCEPTION_HANDLER": "core.renderers.exception_handler.custom_exception_handler",
    # Permissions
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Throttling
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/minute",
        "user": "120/minute",
        "login": "5/minute",
        "logout": "5/minute",
        "register": "5/minute",
        "refresh-token": "5/minute",
    },
    # Versioning
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": [
        "v1",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}
