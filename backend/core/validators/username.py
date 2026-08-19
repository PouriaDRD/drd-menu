import re
from rest_framework.exceptions import ValidationError
from ..normalizers import normalize_username

USERNAME_REGEX = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def username_validator(username: str):
    """
    Rules:
    - First character must be a letter
    - Only English letters, digits and underscore

    Normalize username before validation.

    Example:
    ali.reza -> AliReza
    ali reza -> AliReza
    Ali Reza -> AliReza

    Return:
    AliReza

    Raise:
    ValidationError if username is invalid.
    """

    if not username:
        raise ValidationError("Username is required.")

    normalized_username = normalize_username(username)

    if not USERNAME_REGEX.fullmatch(normalized_username):
        raise ValidationError(
            "Username must start with a letter and contain only English letters, numbers and underscore."
        )

    return normalized_username
