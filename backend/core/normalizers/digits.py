PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"

DIGIT_TRANSLATION = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ENGLISH_DIGITS + ENGLISH_DIGITS,
)


def normalize_digits(digits: str | int):
    """
    Normalize digits to english digits.
    Examples

    ۱۲۳۴۵۶۷ -> 1234567
    """

    digits = str(digits).strip()
    return digits.translate(DIGIT_TRANSLATION)
