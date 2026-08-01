import re

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"

DIGIT_TRANSLATION = str.maketrans(
    PERSIAN_DIGITS + ARABIC_DIGITS,
    ENGLISH_DIGITS + ENGLISH_DIGITS,
)


def normalize_phone_number(phone: str) -> str:
    """
    Examples

    +989121234567 -> 09121234567
    00989121234567 -> 09121234567
    989121234567 -> 09121234567
    ۰۹۱۲۱۲۳۴۵۶۷ -> 09121234567
    """

    if not phone:
        return phone

    phone = phone.strip()
    phone = phone.translate(DIGIT_TRANSLATION)

    phone = re.sub(r"[\s\-()]", "", phone)

    if phone.startswith("+98"):
        phone = "0" + phone[3:]

    elif phone.startswith("0098"):
        phone = "0" + phone[4:]

    elif phone.startswith("98"):
        phone = "0" + phone[2:]

    return phone


def normalize_username(username: str) -> str:
    """
    - Persian/Arabic digits -> English digits
    - Trim spaces
    """

    if not username:
        return username

    username = username.strip()
    username = username.translate(DIGIT_TRANSLATION)

    return username
