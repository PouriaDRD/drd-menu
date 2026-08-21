import logging
from typing import Any

from django.utils.translation import gettext
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


# =============================================================================
# API ERROR CODES
# =============================================================================

VALIDATION_ERROR = "VALIDATION_ERROR"
AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
PERMISSION_ERROR = "PERMISSION_ERROR"
NOT_FOUND_ERROR = "NOT_FOUND"
METHOD_NOT_ALLOWED_ERROR = "METHOD_NOT_ALLOWED"
THROTTLED_ERROR = "THROTTLED"
CONFLICT_ERROR = "CONFLICT"
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
BAD_REQUEST_ERROR = "BAD_REQUEST"
ERROR = "ERROR"


def get_exception_code(
    exc: Exception,
    response: Response,
) -> str:
    """
    Return a stable API-level error code.

    These codes are intended for frontend logic and
    must not depend on translated messages.
    """

    status_code = response.status_code

    if status_code == status.HTTP_400_BAD_REQUEST:
        return VALIDATION_ERROR

    if status_code == status.HTTP_401_UNAUTHORIZED:
        return AUTHENTICATION_ERROR

    if status_code == status.HTTP_403_FORBIDDEN:
        return PERMISSION_ERROR

    if status_code == status.HTTP_404_NOT_FOUND:
        return NOT_FOUND_ERROR

    if status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        return METHOD_NOT_ALLOWED_ERROR

    if status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        return THROTTLED_ERROR

    if status_code == status.HTTP_409_CONFLICT:
        return CONFLICT_ERROR

    return ERROR


def get_request_context(
    context: dict[str, Any],
) -> dict[str, str]:
    """
    Extract safe request information for logging.
    """

    request = context.get("request")
    view = context.get("view")
    exception = context.get("exception")

    return {
        "view": (view.__class__.__name__ if view is not None else "UnknownView"),
        "method": (request.method if request is not None else "UNKNOWN"),
        "path": (request.path if request is not None else "UNKNOWN"),
        "exception_type": (
            type(exception).__name__ if exception is not None else "UnknownException"
        ),
    }


def custom_exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    """
    Centralized exception handler.

    Responsibilities:

    - Delegate DRF exceptions to DRF.
    - Add stable API-level error codes.
    - Convert IntegrityError into HTTP 409.
    - Convert unexpected exceptions into HTTP 500.
    - Preserve DRF field-level error codes.
    - Keep internal exception details out of production responses.
    """

    # ================================================================
    # STANDARD DRF EXCEPTIONS
    # ================================================================

    response = exception_handler(
        exc,
        context,
    )

    if response is not None:
        existing_data = response.data

        if isinstance(existing_data, dict):
            response.data = {
                "code": get_exception_code(
                    exc,
                    response,
                ),
                **existing_data,
            }

        else:
            response.data = {
                "code": get_exception_code(
                    exc,
                    response,
                ),
                "detail": existing_data,
            }

        return response

    # ================================================================
    # LOGGING CONTEXT
    # ================================================================

    log_context = get_request_context(
        {
            **context,
            "exception": exc,
        },
    )

    # ================================================================
    # DATABASE INTEGRITY ERROR
    # ================================================================

    if isinstance(exc, IntegrityError):
        logger.warning(
            "Database integrity error.",
            extra=log_context,
            exc_info=True,
        )

        return Response(
            {
                "code": CONFLICT_ERROR,
                "detail": gettext("A database conflict occurred."),
            },
            status=status.HTTP_409_CONFLICT,
        )

    # ================================================================
    # UNEXPECTED SERVER ERROR
    # ================================================================

    logger.error(
        "Unhandled exception in API request.",
        extra=log_context,
        exc_info=True,
    )

    return Response(
        {
            "code": INTERNAL_SERVER_ERROR,
            "detail": gettext("A server error occurred. " "Please contact support."),
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
