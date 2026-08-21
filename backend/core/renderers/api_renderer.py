from collections.abc import Mapping
from typing import Any

from django.utils.translation import gettext
from rest_framework.renderers import JSONRenderer

SUCCESS_STATUS_MIN = 200
SUCCESS_STATUS_MAX = 299

DEFAULT_SUCCESS_CODE = "SUCCESS"
DEFAULT_ERROR_CODE = "ERROR"

VALIDATION_ERROR_CODE = "VALIDATION_ERROR"
UNKNOWN_ERROR_CODE = "UNKNOWN_ERROR"

API_METADATA_KEYS = {
    "code",
    "message",
}


def is_success_status(status_code: int) -> bool:
    """
    Return True when the HTTP status code represents a successful response.
    """

    return SUCCESS_STATUS_MIN <= status_code <= SUCCESS_STATUS_MAX


def stringify(value: Any) -> str:
    """
    Convert a value into a human-readable string.
    """

    if isinstance(value, str):
        return value

    return str(value)


def get_error_code(error: Any) -> str:
    """
    Extract the DRF error code from an ErrorDetail instance.
    """

    code = getattr(error, "code", None)

    if code is None:
        return DEFAULT_ERROR_CODE

    return str(code)


def normalize_error_item(
    error: Any,
) -> dict[str, str]:
    """
    Convert a single DRF error into frontend structure.
    """

    if isinstance(error, Mapping):

        message = error.get("message")

        code = error.get("code")

        return {
            "message": stringify(message) if message else "Validation error.",
            "code": stringify(code) if code else DEFAULT_ERROR_CODE,
        }

    return {
        "message": stringify(error),
        "code": get_error_code(error),
    }


def normalize_error_value(
    value: Any,
) -> list[dict[str, str]]:
    """
    Normalize a single field's errors.

    Supports:

        ErrorDetail(...)
        [ErrorDetail(...), ErrorDetail(...)]
    """

    if isinstance(value, (list, tuple)):
        return [normalize_error_item(error) for error in value]

    return [
        normalize_error_item(value),
    ]


def normalize_errors(
    data: Any,
) -> dict[str, list[dict[str, str]]]:
    """
    Normalize DRF validation errors.

    Example input:

        {
            "email": [
                ErrorDetail(
                    "A user with this email already exists.",
                    code="EMAIL_ALREADY_EXISTS",
                )
            ]
        }

    Example output:

        {
            "email": [
                {
                    "message": "A user with this email already exists.",
                    "code": "EMAIL_ALREADY_EXISTS",
                }
            ]
        }
    """

    if isinstance(data, Mapping):
        return {
            str(field): normalize_error_value(value) for field, value in data.items()
        }

    if data is None:
        return {}

    return {
        "detail": normalize_error_value(data),
    }


def remove_api_metadata(
    data: Any,
) -> Any:
    """
    Remove top-level API metadata before converting
    validation errors.

    The exception handler adds:

        {
            "code": "...",
            ...
        }

    That code belongs to the API response itself and
    must never become a field-level validation error.
    """

    if not isinstance(data, Mapping):
        return data

    return {key: value for key, value in data.items() if key not in API_METADATA_KEYS}


def extract_message(
    data: Any,
    *,
    success: bool,
) -> str:
    """
    Extract the top-level API message.
    """

    if isinstance(data, Mapping):
        message = data.get("message")

        if message:
            return stringify(message)

        if not success:
            detail = data.get("detail")

            if detail:
                if isinstance(detail, (list, tuple)):
                    if detail:
                        return stringify(detail[0])

                return stringify(detail)

            if data:
                return gettext("Validation failed.")

    if success:
        return gettext("Operation completed successfully.")

    return gettext("An error occurred.")


def extract_code(
    data: Any,
    *,
    success: bool,
) -> str:
    """
    Extract the top-level API response code.
    """

    if isinstance(data, Mapping):
        code = data.get("code")

        if code:
            return stringify(code)

    if success:
        return DEFAULT_SUCCESS_CODE

    if isinstance(data, Mapping):
        if "detail" in data:
            return DEFAULT_ERROR_CODE

        if data:
            return VALIDATION_ERROR_CODE

    return UNKNOWN_ERROR_CODE


def extract_data(
    data: Any,
) -> Any:
    """
    Extract the actual API data.
    """

    if isinstance(data, Mapping) and "data" in data:
        return data["data"]

    return data if data is not None else []


class ApiRenderer(JSONRenderer):
    """
    Global JSON renderer for the API.

    Success:

        {
            "success": true,
            "code": "SUCCESS",
            "message": "...",
            "data": {...},
            "errors": null
        }

    Error:

        {
            "success": false,
            "code": "VALIDATION_ERROR",
            "message": "...",
            "data": [],
            "errors": {
                "email": [
                    {
                        "message": "...",
                        "code": "EMAIL_ALREADY_EXISTS"
                    }
                ]
            }
        }
    """

    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict[str, Any] | None = None,
    ) -> bytes:
        """
        Render every API response using the standard envelope.
        """

        if renderer_context is None:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )

        response = renderer_context["response"]

        status_code = response.status_code

        # ================================================================
        # 204 NO CONTENT
        # ================================================================

        if status_code == 204:
            return b""

        success = is_success_status(
            status_code,
        )

        # ================================================================
        # SUCCESS
        # ================================================================

        if success:
            payload = {
                "success": True,
                "code": extract_code(
                    data,
                    success=True,
                ),
                "message": extract_message(
                    data,
                    success=True,
                ),
                "data": extract_data(data),
                "errors": None,
            }

            return super().render(
                payload,
                accepted_media_type,
                renderer_context,
            )

        # ================================================================
        # ERROR
        # ================================================================

        error_data = remove_api_metadata(
            data,
        )

        payload = {
            "success": False,
            "code": extract_code(
                data,
                success=False,
            ),
            "message": extract_message(
                data,
                success=False,
            ),
            "data": [],
            "errors": normalize_errors(
                error_data,
            ),
        }

        return super().render(
            payload,
            accepted_media_type,
            renderer_context,
        )
