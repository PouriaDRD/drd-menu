from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.enums import UserRole, UserStatus

UserModel = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        user = UserModel.objects.create_user(
            username="pouria",
            password="123456",
        )

        self.assertEqual(user.username, "pouria")
        self.assertEqual(user.role, UserRole.USER)  # type: ignore
        self.assertEqual(user.status, UserStatus.ACTIVE)  # type: ignore
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("123456"))

    def test_create_user_normalizes_phone(self):
        user = UserModel.objects.create_user(
            username="pouria",
            phone_number="+989121234567",
        )

        self.assertEqual(
            user.phone_number,  # type: ignore
            "09121234567",
        )

    def test_create_user_normalizes_email(self):
        user = UserModel.objects.create_user(
            username="pouria",
            email="Test@Example.COM",
        )

        self.assertEqual(
            user.email,
            "Test@example.com",
        )

    def test_create_superuser(self):
        user = UserModel.objects.create_superuser(
            username="admin",
            password="123456",
        )  # type: ignore

        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, UserRole.SUPERUSER)
        self.assertEqual(user.status, UserStatus.ACTIVE)

    def test_create_superuser_without_password(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(
                username="admin",
            )  # type: ignore

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(
                username="",
            )
