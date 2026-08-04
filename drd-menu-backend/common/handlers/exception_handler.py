import logging

from django.conf import settings
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .codes import ErrorCode

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = exception_handler(
        exc,
        context,
    )

    if response is None:

        if isinstance(exc, IntegrityError):

            logger.warning(
                "IntegrityError: %s",
                str(exc),
                exc_info=True,
            )

            return Response(
                {
                    "detail": ("Database constraint violation."),
                    "code": ErrorCode.DATABASE_ERROR,
                },
                status=status.HTTP_409_CONFLICT,
            )

        logger.error(
            "Unhandled Exception: %s",
            str(exc),
            exc_info=True,
        )

        return Response(
            {
                "detail": (str(exc) if settings.DEBUG else "Server error occurred."),
                "code": ErrorCode.SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    status_code = response.status_code

    if status_code == 400:
        code = ErrorCode.VALIDATION_ERROR

    elif status_code == 401:
        code = ErrorCode.NOT_AUTHENTICATED

    elif status_code == 403:
        code = ErrorCode.PERMISSION_DENIED

    elif status_code == 404:
        code = ErrorCode.NOT_FOUND

    elif status_code == 429:
        code = ErrorCode.TOO_MANY_REQUESTS

    else:
        code = None

    if isinstance(response.data, dict):

        response.data["code"] = code

    return response
