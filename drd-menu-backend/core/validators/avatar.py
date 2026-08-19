import os
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


from core.app_config import config

MAX_SIZE = (512, 512)


MAX_AVATAR_SIZE_NUMBER = int(config.media.max_avatar_size)

MAX_AVATAR_SIZE = MAX_AVATAR_SIZE_NUMBER * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
}


def avatar_validator(file: ContentFile):
    """
    Validate avatar file size and extension.
    """

    extension = os.path.splitext(file.name)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only JPG, JPEG, PNG and GIF images are allowed.")

    if file.size > MAX_AVATAR_SIZE:
        raise ValidationError(
            f"Avatar size must not exceed {MAX_AVATAR_SIZE_NUMBER} MB."
        )
