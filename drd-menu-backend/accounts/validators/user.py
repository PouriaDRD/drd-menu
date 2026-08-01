import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

USERNAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
PHONE_REGEX = re.compile(r"^09\d{9}$")


def username_validator(value: str):
    """
    Rules:
    - First character must be a letter
    - Only English letters, digits and underscore
    """

    if not value:
        return

    if not USERNAME_REGEX.fullmatch(value):
        raise ValidationError(
            "Username must start with a letter and contain only English letters, numbers and underscore."
        )


def phone_number_validator(value: str):
    """
    Rules:
    09XXXXXXXXX
    """

    if not value:
        return

    if not PHONE_REGEX.fullmatch(value):
        raise ValidationError(
            "Phone number must start with 09 and contain exactly 11 digits."
        )


email_validator = EmailValidator()
