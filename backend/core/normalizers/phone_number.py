import re
from rest_framework.exceptions import ValidationError

from .digits import normalize_digits


def normalize_phone_number(phone: str) -> str:
    """
    Examples

    +989121234567 -> 09121234567
    00989121234567 -> 09121234567
    989121234567 -> 09121234567
    ۰۹۱۲۱۲۳۴۵۶۷ -> 09121234567
    """

    if not phone:
        raise ValidationError("Phone number is required.")

    phone = normalize_digits(phone)

    phone = re.sub(r"[\s\-()]", "", phone)

    if phone.startswith("+98"):
        phone = "0" + phone[3:]

    elif phone.startswith("0098"):
        phone = "0" + phone[4:]

    elif phone.startswith("98"):
        phone = "0" + phone[2:]

    return phone
