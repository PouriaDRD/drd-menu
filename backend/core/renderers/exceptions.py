from rest_framework.exceptions import APIException
from rest_framework import status


class APIValidationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation error."
    default_code = "VALIDATION_ERROR"


class FieldValidationError(APIValidationException):

    def __init__(
        self,
        field: str,
        message: str,
        code: str,
    ):
        self.detail = {
            field: [
                {
                    "message": message,
                    "code": code,
                }
            ]
        }
