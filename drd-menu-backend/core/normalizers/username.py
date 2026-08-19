from rest_framework.exceptions import ValidationError

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"

DIGIT_TRANSLATION = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ENGLISH_DIGITS + ENGLISH_DIGITS,
)


def normalize_username(username: str) -> str:
    """
    - Persian/Arabic digits -> English digits
    - Trim spaces
    """

    if not username:
        raise ValidationError("Username is required.")

    username = username.strip()
    username = username.translate(DIGIT_TRANSLATION)

    return username
