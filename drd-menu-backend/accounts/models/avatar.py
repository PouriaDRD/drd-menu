import uuid
from django.db import models
from django_cleanup import cleanup
from django.contrib.auth import get_user_model

from accounts.validators.avatar import avatar_validator, resize_avatar

UserModel = get_user_model()


def avatar_upload_path(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    return f"users/avatars/" f"{instance.user.id}/" f"{instance.id}.{ext}"


@cleanup.select
class UserAvatarModel(models.Model):
    """
    Stores user avatar images.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the avatar.",
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="avatars",
        db_index=True,
        help_text="Owner of this avatar.",
    )

    image = models.ImageField(
        upload_to=avatar_upload_path,
        validators=[avatar_validator],
        help_text="Avatar image.",
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this avatar is the user's primary avatar.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Avatar upload time.",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} avatar"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_avatar(self)
