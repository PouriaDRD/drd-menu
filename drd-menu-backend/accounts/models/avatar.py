import uuid

from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from django_cleanup import cleanup

from accounts.validators.avatar import (
    avatar_validator,
    resize_avatar,
)

UserModel = get_user_model()


def avatar_upload_path(instance, filename):
    """
    Generate avatar upload path.

    Example:
        users/avatars/<user_id>/<avatar_id>.png
    """

    extension = filename.rsplit(".", 1)[-1].lower()

    return f"users/avatars/" f"{instance.user.id}/" f"{instance.id}.{extension}"


@cleanup.select
class UserAvatarModel(models.Model):
    """
    Stores user avatar images.

    A user can have multiple avatars,
    but only one avatar can be primary.
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
        help_text="User who owns this avatar.",
    )

    image = models.ImageField(
        upload_to=avatar_upload_path,
        validators=[
            avatar_validator,
        ],
        help_text=(
            "Avatar image. "
            "Allowed formats: JPG, JPEG, PNG, GIF. "
            "Maximum dimensions will be resized to 512x512."
        ),
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text=("Defines whether this avatar is the user's primary avatar."),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Avatar creation time.",
    )

    class Meta:
        verbose_name = "User Avatar"
        verbose_name_plural = "User Avatars"

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                ],
                condition=Q(
                    is_primary=True,
                ),
                name="unique_primary_avatar_per_user",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "is_primary",
                ],
            ),
            models.Index(
                fields=[
                    "created_at",
                ],
            ),
        ]

    def save(self, *args, **kwargs):
        """
        Save avatar and resize image only when image changes.
        """

        if self.pk:
            old_instance = UserAvatarModel.objects.filter(
                pk=self.pk,
            ).first()

            if old_instance and old_instance.image != self.image:
                self.image = resize_avatar(
                    self.image,
                )

        else:
            if self.image:
                self.image = resize_avatar(
                    self.image,
                )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} avatar"
