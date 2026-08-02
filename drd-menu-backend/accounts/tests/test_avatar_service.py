from PIL import Image
from io import BytesIO
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import UserAvatarModel

UserModel = get_user_model()


class ResizeAvatarTests(TestCase):
    def create_avatar(self, size=(2000, 1000), extension="png"):
        user = UserModel.objects.create_user(
            username="pouria",
        )

        file = BytesIO()

        Image.new(
            "RGB",
            size,
            color="red",
        ).save(file, extension.upper())

        file.seek(0)

        avatar = UserAvatarModel.objects.create(
            user=user,
            image=SimpleUploadedFile(
                f"avatar.{extension}",
                file.read(),
                content_type=f"image/{extension}",
            ),
        )

        return avatar

    def test_resize_large_image(self):
        avatar = self.create_avatar()

        image = Image.open(avatar.image)

        self.assertLessEqual(image.width, 512)
        self.assertLessEqual(image.height, 512)

    def test_keep_aspect_ratio(self):
        avatar = self.create_avatar(
            size=(2000, 1000),
        )

        image = Image.open(avatar.image)

        ratio = image.width / image.height

        self.assertAlmostEqual(
            ratio,
            2,
            delta=0.1,
        )

    def test_square_image(self):
        avatar = self.create_avatar(
            size=(3000, 3000),
        )

        image = Image.open(avatar.image)

        self.assertEqual(image.width, 512)
        self.assertEqual(image.height, 512)

    def test_small_image_not_upscaled(self):
        avatar = self.create_avatar(
            size=(100, 100),
        )

        image = Image.open(avatar.image)

        self.assertEqual(image.width, 100)
        self.assertEqual(image.height, 100)
