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
    Extract a DRF error code from an ErrorDetail instance.

    Falls back to ``error`` when no code is available.
    """
    code = getattr(error, "code", None)

    if code is None:
        return "error"

    return str(code)


def normalize_error_item(error: Any) -> dict[str, str]:
    """
    Convert a single DRF error into a frontend-friendly structure.

    Example:

        ErrorDetail(
            "This field is required.",
            code="required",
        )

    becomes:

        {
            "message": "This field is required.",
            "code": "required",
        }
    """
    return {
        "message": stringify(error),
        "code": get_error_code(error),
    }


def normalize_error_value(value: Any) -> list[dict[str, str]]:
    """
    Normalize an error value into a list of structured errors.
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
    Normalize DRF errors into a predictable structure for the frontend.

    Example input:

        {
            "phone_number": [
                ErrorDetail(
                    "A user with this phone number already exists.",
                    code="unique",
                )
            ],
            "first_name": [
                ErrorDetail(
                    "This field is required.",
                    code="required",
                )
            ],
        }

    Example output:

        {
            "phone_number": [
                {
                    "message": "A user with this phone number already exists.",
                    "code": "unique",
                }
            ],
            "first_name": [
                {
                    "message": "This field is required.",
                    "code": "required",
                }
            ],
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


def extract_message(
    data: Any,
    *,
    success: bool,
) -> str:
    """
    Extract the top-level API message.

    For success responses:
        1. Explicit message
        2. Generic success message

    For error responses:
        1. Explicit message
        2. Detail
        3. Validation failed
        4. Generic error
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

    Explicit ``code`` values provided by the view or exception handler
    always take priority.
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


def extract_data(data: Any) -> Any:
    """
    Extract the actual API data from a successful response.

    If the response contains a ``data`` key, that value is returned.

    This allows views to return either:

        Response(serializer.data)

    or:

        Response({
            "message": "...",
            "data": serializer.data,
        })

    without creating duplicated/nested data structures.
    """
    if isinstance(data, Mapping) and "data" in data:
        return data["data"]

    return data if data is not None else []


class ApiRenderer(JSONRenderer):
    """
    Global JSON renderer for the API.

    Success response:

        {
            "status": true,
            "code": "SUCCESS",
            "message": "...",
            "data": {...},
            "errors": null
        }

    Error response:

        {
            "status": false,
            "code": "VALIDATION_ERROR",
            "message": "Validation failed.",
            "data": [],
            "errors": {
                "phone_number": [
                    {
                        "message": "...",
                        "code": "unique"
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
        Render every API response using the project's standard structure.
        """
        if renderer_context is None:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )

        response = renderer_context["response"]
        status_code = response.status_code

        # ---------------------------------------------------------------------
        # 204 No Content
        # ---------------------------------------------------------------------

        if status_code == 204:
            return b""

        success = is_success_status(status_code)

        # ---------------------------------------------------------------------
        # Success
        # ---------------------------------------------------------------------

        if success:
            payload = {
                "status": True,
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

        # ---------------------------------------------------------------------
        # Error
        # ---------------------------------------------------------------------

        payload = {
            "status": False,
            "code": extract_code(
                data,
                success=False,
            ),
            "message": extract_message(
                data,
                success=False,
            ),
            "data": [],
            "errors": normalize_errors(data),
        }

        return super().render(
            payload,
            accepted_media_type,
            renderer_context,
        )
