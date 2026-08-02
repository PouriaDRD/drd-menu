import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


from config.settings.app_config import config

MAX_SIZE = (512, 512)


MAX_AVATAR_SIZE_NUMBER = int(config.media.max_avatar_size)

MAX_AVATAR_SIZE = MAX_AVATAR_SIZE_NUMBER * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
}


def avatar_validator(file):
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


def resize_avatar(instance):
    """
    Resize avatar image so that it fits inside 512x512.
    """

    if not instance.image:
        return

    image = Image.open(instance.image)

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)

    output = BytesIO()

    extension = instance.image.name.lower().split(".")[-1]

    if extension in ("jpg", "jpeg"):
        image.save(
            output,
            format="JPEG",
            quality=95,
            optimize=True,
        )

    elif extension == "png":
        image.save(
            output,
            format="PNG",
            optimize=True,
        )

    elif extension == "gif":
        image.save(
            output,
            format="GIF",
        )

    output.seek(0)

    instance.image.save(
        instance.image.name,
        ContentFile(output.read()),
        save=False,
    )

    super(instance.__class__, instance).save(update_fields=["image"])
