from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from accounts.validators.user import (
    username_validator,
    phone_number_validator,
)


class UsernameValidatorTests(SimpleTestCase):
    def test_valid_username(self):
        username_validator("pouria")
        username_validator("pouria_123")
        username_validator("A1")

    def test_start_with_number(self):
        with self.assertRaises(ValidationError):
            username_validator("1pouria")

    def test_contains_dash(self):
        with self.assertRaises(ValidationError):
            username_validator("pouria-test")

    def test_contains_space(self):
        with self.assertRaises(ValidationError):
            username_validator("pouria test")

    def test_contains_persian(self):
        with self.assertRaises(ValidationError):
            username_validator("پوریا")


class PhoneValidatorTests(SimpleTestCase):
    def test_valid_phone(self):
        phone_number_validator("09121234567")

    def test_not_start_with_09(self):
        with self.assertRaises(ValidationError):
            phone_number_validator("08121234567")

    def test_short(self):
        with self.assertRaises(ValidationError):
            phone_number_validator("0912123")

    def test_long(self):
        with self.assertRaises(ValidationError):
            phone_number_validator("091212345678")

    def test_contains_letters(self):
        with self.assertRaises(ValidationError):
            phone_number_validator("0912abcd567")
