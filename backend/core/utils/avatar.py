import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

MAX_SIZE = (512, 512)


def resize_avatar(file: ContentFile) -> ContentFile:
    """
    Resize avatar image to maximum 512x512.
    """

    image = Image.open(file)

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    image.thumbnail(
        MAX_SIZE,
        Image.Resampling.LANCZOS,
    )

    output = BytesIO()

    extension = os.path.splitext(file.name)[1].lower()

    if extension in (".jpg", ".jpeg"):
        image.save(
            output,
            format="JPEG",
            quality=95,
            optimize=True,
        )

    elif extension == ".png":
        image.save(
            output,
            format="PNG",
            optimize=True,
        )

    elif extension == ".gif":
        image.save(
            output,
            format="GIF",
        )

    output.seek(0)

    return ContentFile(
        output.read(),
        name=file.name,
    )
