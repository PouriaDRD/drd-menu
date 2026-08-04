from PIL import Image
from io import BytesIO
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import UserAvatarModel

UserModel = get_user_model()


def create_image():
    """
    Create test avatar image.
    """

    file = BytesIO()

    Image.new(
        "RGB",
        (100, 100),
        color="red",
    ).save(
        file,
        "PNG",
    )

    file.seek(0)

    return SimpleUploadedFile(
        "avatar.png",
        file.read(),
        content_type="image/png",
    )


class UserAvatarConstraintTests(TestCase):
    """
    Tests database constraints for UserAvatarModel.
    """

    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="pouria",
            password="123456",
        )

    def test_user_can_have_multiple_avatars(self):
        """
        User can have multiple non-primary avatars.
        """

        UserAvatarModel.objects.create(
            user=self.user,
            image=create_image(),
            is_primary=False,
        )

        UserAvatarModel.objects.create(
            user=self.user,
            image=create_image(),
            is_primary=False,
        )

        self.assertEqual(
            self.user.avatars.count(),  # type: ignore
            2,
        )

    def test_user_can_have_only_one_primary_avatar(self):
        """
        User always has only one primary avatar.
        """

        first_avatar = UserAvatarModel.objects.create(
            user=self.user,
            image=create_image(),
            is_primary=True,
        )

        second_avatar = UserAvatarModel.objects.create(
            user=self.user,
            image=create_image(),
            is_primary=True,
        )

        first_avatar.refresh_from_db()
        second_avatar.refresh_from_db()

        self.assertFalse(
            first_avatar.is_primary,
        )

        self.assertTrue(
            second_avatar.is_primary,
        )

    def test_multiple_users_can_have_primary_avatar(self):
        """
        Different users can have their own primary avatar.
        """

        another_user = UserModel.objects.create_user(
            username="ali",
            password="123456",
        )

        UserAvatarModel.objects.create(
            user=self.user,
            image=create_image(),
            is_primary=True,
        )

        UserAvatarModel.objects.create(
            user=another_user,
            image=create_image(),
            is_primary=True,
        )

        self.assertEqual(
            UserAvatarModel.objects.filter(
                is_primary=True,
            ).count(),
            2,
        )
