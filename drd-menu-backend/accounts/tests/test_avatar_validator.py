import os
from PIL import Image
from io import BytesIO
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.validators.avatar import (
    avatar_validator,
    MAX_AVATAR_SIZE,
)


def create_image(
    extension: str = "png",
    size: tuple[int, int] = (100, 100),
) -> SimpleUploadedFile:
    """
    Create a valid in-memory image.
    """

    output = BytesIO()

    image = Image.new(
        "RGB",
        size,
        color="red",
    )

    save_format = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "gif": "GIF",
    }[extension]

    image.save(
        output,
        format=save_format,
    )

    output.seek(0)

    return SimpleUploadedFile(
        f"avatar.{extension}",
        output.read(),
        content_type=f"image/{extension}",
    )


def create_large_image() -> SimpleUploadedFile:
    """
    Create a valid image whose file size exceeds MAX_AVATAR_SIZE.
    """

    width = 3000
    height = 3000

    image = Image.frombytes(
        "RGB",
        (width, height),
        os.urandom(width * height * 3),
    )

    output = BytesIO()

    image.save(
        output,
        format="PNG",
        compress_level=0,
    )

    output.seek(0)

    file = SimpleUploadedFile(
        "avatar.png",
        output.read(),
        content_type="image/png",
    )

    # Ensure the generated file is actually larger than the configured limit.
    assert file.size > MAX_AVATAR_SIZE

    return file


class AvatarValidatorTests(TestCase):
    def test_accepts_png(self):
        avatar_validator(create_image("png"))

    def test_accepts_jpg(self):
        avatar_validator(create_image("jpg"))

    def test_accepts_jpeg(self):
        avatar_validator(create_image("jpeg"))

    def test_accepts_gif(self):
        avatar_validator(create_image("gif"))

    def test_rejects_invalid_extension(self):
        file = SimpleUploadedFile(
            "avatar.webp",
            b"invalid",
            content_type="image/webp",
        )

        with self.assertRaises(ValidationError):
            avatar_validator(file)

    def test_rejects_large_file(self):
        file = create_large_image()

        self.assertGreater(
            file.size,
            MAX_AVATAR_SIZE,
        )

        with self.assertRaises(ValidationError):
            avatar_validator(file)
