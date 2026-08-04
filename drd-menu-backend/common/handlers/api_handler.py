import copy

from django.utils.translation import gettext as _
from rest_framework.renderers import JSONRenderer

from .codes import ErrorCode


def normalize_errors(errors):
    """
    Convert DRF errors into frontend-friendly format.
    """

    if not isinstance(errors, dict):
        return errors

    result = {}

    for field, messages in errors.items():

        if isinstance(messages, list) and messages:

            error = messages[0]

            if isinstance(error, dict):
                result[field] = error

            else:
                result[field] = {
                    "message": str(error),
                    "code": ErrorCode.VALIDATION_ERROR,
                }

        else:
            result[field] = messages

    return result


def extract_message(data, status_code):

    if not data:
        return None

    if isinstance(data, dict):

        if "detail" in data:
            return data["detail"]

        if "message" in data:
            return data["message"]

        if not str(status_code).startswith("2"):

            for field, errors in data.items():

                if field != "non_field_errors":

                    if isinstance(errors, list) and errors:

                        if isinstance(errors[0], dict):
                            return errors[0].get("message")

                        return str(errors[0])

            if "non_field_errors" in data:
                return str(data["non_field_errors"][0])

    if str(status_code).startswith("2"):
        return _("Operation successful")

    return _("An error occurred")


class ApiRenderer(JSONRenderer):

    charset = "utf-8"

    def render(
        self,
        data,
        accepted_media_type=None,
        renderer_context=None,
    ):

        response = {
            "status": True,
            "code": None,
            "message": None,
            "data": data or [],
        }

        if renderer_context:

            status_code = renderer_context["response"].status_code

            if str(status_code).startswith("2"):

                response["message"] = extract_message(
                    data,
                    status_code,
                )

            else:

                errors_data = copy.deepcopy(data)

                response["status"] = False

                response["code"] = (
                    data.get(
                        "code",
                        ErrorCode.VALIDATION_ERROR,
                    )
                    if isinstance(data, dict)
                    else ErrorCode.VALIDATION_ERROR
                )

                response["message"] = extract_message(
                    data,
                    status_code,
                )

                response["errors"] = normalize_errors(errors_data)

                response["data"] = []

        return super().render(
            response,
            accepted_media_type,
            renderer_context,
        )
