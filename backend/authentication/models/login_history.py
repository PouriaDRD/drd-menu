import uuid

from django.db import models

from accounts.models import UserModel


class LoginHistoryModel(models.Model):
    """
    User login activity history.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="login_histories",
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the user's device.",
    )

    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="User agent of the user's device.",
    )

    device = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Device type of the user's device.",
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Browser of the user's device.",
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Operating system of the user's device.",
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country of the user's device.",
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City of the user's device.",
    )

    is_successful = models.BooleanField(
        default=True,
    )

    failure_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Failure reason of the user's device.",
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "login_histories"

        ordering = [
            "-created_at",
        ]

        verbose_name = "Login History"

        verbose_name_plural = "Login Histories"

    def __str__(self):
        return f"{self.user} - {self.created_at}"
