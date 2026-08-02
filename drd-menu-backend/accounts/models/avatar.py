import uuid

from django.db import models, transaction
from django.db.models import Q
from django_cleanup import cleanup
from django.contrib.auth import get_user_model

from accounts.validators.avatar import (
    avatar_validator,
    resize_avatar,
)

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

        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_primary=True),
                name="unique_primary_avatar_per_user",
            )
        ]

    def __str__(self):
        return f"{self.user.username} avatar"

    def save(self, *args, **kwargs):
        """
        Save avatar.

        Rules:
        - First uploaded avatar becomes primary automatically.
        - Only one primary avatar is allowed per user.
        - Image is resized before saving.
        """

        with transaction.atomic():

            is_new = self._state.adding

            if is_new and not self.user.avatars.exists():  # type: ignore
                self.is_primary = True

            if self.is_primary:
                (
                    UserAvatarModel.objects.filter(
                        user=self.user,
                        is_primary=True,
                    )
                    .exclude(
                        pk=self.pk,
                    )
                    .update(
                        is_primary=False,
                    )
                )

            if self.image:
                self.image = resize_avatar(
                    self.image,
                )

            super().save(
                *args,
                **kwargs,
            )
