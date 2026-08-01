from django.test import SimpleTestCase

from accounts.normalizers.user import (
    normalize_phone_number,
    normalize_username,
)


class NormalizePhoneNumberTests(SimpleTestCase):
    def test_normalize_plain_phone(self):
        self.assertEqual(
            normalize_phone_number("09121234567"),
            "09121234567",
        )

    def test_normalize_plus98(self):
        self.assertEqual(
            normalize_phone_number("+989121234567"),
            "09121234567",
        )

    def test_normalize_0098(self):
        self.assertEqual(
            normalize_phone_number("00989121234567"),
            "09121234567",
        )

    def test_normalize_98(self):
        self.assertEqual(
            normalize_phone_number("989121234567"),
            "09121234567",
        )

    def test_normalize_persian_digits(self):
        self.assertEqual(
            normalize_phone_number("۰۹۱۲۱۲۳۴۵۶۷"),
            "09121234567",
        )

    def test_remove_spaces_and_dashes(self):
        self.assertEqual(
            normalize_phone_number("+98 912-123-4567"),
            "09121234567",
        )

    def test_none(self):
        self.assertIsNone(normalize_phone_number(None))  # type: ignore


class NormalizeUsernameTests(SimpleTestCase):
    def test_strip(self):
        self.assertEqual(
            normalize_username("   pouria   "),
            "pouria",
        )

    def test_convert_digits(self):
        self.assertEqual(
            normalize_username("user۱۲۳"),
            "user123",
        )

    def test_none(self):
        self.assertIsNone(normalize_username(None))  # type: ignore
