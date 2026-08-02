from PIL import Image
from io import BytesIO
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import UserAvatarModel

UserModel = get_user_model()


class UserAvatarModelTests(TestCase):
    def create_image(self):
        file = BytesIO()

        Image.new(
            "RGB",
            (100, 100),
            color="red",
        ).save(file, "PNG")

        file.seek(0)

        return SimpleUploadedFile(
            "avatar.png",
            file.read(),
            content_type="image/png",
        )

    def test_create_avatar(self):
        """
        First avatar should automatically become primary.
        """

        user = UserModel.objects.create_user(
            username="pouria",
        )

        avatar = UserAvatarModel.objects.create(
            user=user,
            image=self.create_image(),
        )

        self.assertTrue(
            avatar.is_primary,
        )

        self.assertEqual(
            avatar.user,
            user,
        )

    def test_avatar_path_contains_user_id(self):
        user = UserModel.objects.create_user(
            username="pouria",
        )

        avatar = UserAvatarModel.objects.create(
            user=user,
            image=self.create_image(),
        )

        self.assertIn(
            str(user.id),  # type: ignore
            avatar.image.name,
        )

    def test_str(self):
        user = UserModel.objects.create_user(
            username="pouria",
        )

        avatar = UserAvatarModel.objects.create(
            user=user,
            image=self.create_image(),
        )

        self.assertEqual(
            str(avatar),
            "pouria avatar",
        )
