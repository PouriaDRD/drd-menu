from django.test import TestCase

from accounts.models import UserModel
from accounts.enums import UserRole


class UserModelTests(TestCase):
    def test_full_name(self):
        user = UserModel.objects.create(
            username="pouria",
            first_name="Pouria",
            last_name="Darandi",
        )

        self.assertEqual(
            user.full_name,
            "Pouria Darandi",
        )

    def test_full_name_fallback(self):
        user = UserModel.objects.create(
            username="pouria",
        )

        self.assertEqual(
            user.full_name,
            "pouria",
        )

    def test_is_staff_for_superuser(self):
        user = UserModel.objects.create(
            username="admin",
            is_superuser=True,
        )

        self.assertTrue(user.is_staff)

    def test_is_staff_for_admin_role(self):
        user = UserModel.objects.create(
            username="admin",
            role=UserRole.ADMIN,
        )

        self.assertTrue(user.is_staff)

    def test_is_staff_for_normal_user(self):
        user = UserModel.objects.create(
            username="user",
        )

        self.assertFalse(user.is_staff)

    def test_str(self):
        user = UserModel.objects.create(
            username="pouria",
        )

        self.assertEqual(str(user), "pouria")
