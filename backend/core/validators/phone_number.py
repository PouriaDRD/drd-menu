import re

from rest_framework.exceptions import ValidationError

from ..normalizers import normalize_phone_number

PHONE_REGEX = re.compile(r"^09\d{9}$")


def model_phone_number_validator(phone_number: str) -> None:
    """
    Validate an Iranian phone number.

    Accepted examples after normalization:

        +989121234567
        00989121234567
        989121234567
        09121234567
        ۰۹۱۲۱۲۳۴۵۶۷

    The stored format is:

        09121234567
    """

    if not phone_number:
        raise ValidationError(
            "Phone number is required.",
            code="required",
        )

    normalized_phone_number = normalize_phone_number(phone_number)

    if not PHONE_REGEX.fullmatch(normalized_phone_number):
        raise ValidationError(
            "Phone number must start with 09 and contain exactly 11 digits.",
            code="invalid",
        )


def phone_number_validator(phone_number: str):
    """
    Rules:
    09XXXXXXXXX

    Normalize phone number before validation.

    Example:
    +989121234567 -> 09121234567
    00989121234567 -> 09121234567
    989121234567 -> 09121234567
    ۰۹۱۲۱۲۳۴۵۶۷ -> 09121234567

    Return:
    09121234567

    Raise:
    ValidationError if phone number is invalid.
    """
    if not phone_number:
        raise ValidationError("Phone number is required.")

    normalized_phone_number = normalize_phone_number(phone_number)

    if not PHONE_REGEX.fullmatch(normalized_phone_number):
        raise ValidationError(
            "Phone number must start with 09 and contain exactly 11 digits."
        )

    return normalized_phone_number
