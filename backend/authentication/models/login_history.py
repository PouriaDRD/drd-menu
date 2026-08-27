import uuid

from django.db import models

from accounts.models import UserModel


class LoginHistoryModel(models.Model):
    """
    Stores a user's login activity and client information.

    The model keeps both the raw User-Agent and parsed client metadata
    such as browser, operating system, and device information.
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
        help_text="User associated with this login attempt.",
    )

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the user's device.",
    )

    # ------------------------------------------------------------------
    # User Agent
    # ------------------------------------------------------------------

    user_agent = models.TextField(
        null=True,
        blank=True,
        help_text="Raw User-Agent string sent by the client.",
    )

    # ------------------------------------------------------------------
    # Device
    # ------------------------------------------------------------------

    device = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Device type, such as Mobile, Tablet, or PC.",
    )

    device_family = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Device family or model reported by the User-Agent.",
    )

    # ------------------------------------------------------------------
    # Browser
    # ------------------------------------------------------------------

    browser = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Browser name.",
    )

    browser_version = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Browser version.",
    )

    # ------------------------------------------------------------------
    # Operating System
    # ------------------------------------------------------------------

    operating_system = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Operating system name.",
    )

    operating_system_version = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Operating system version.",
    )

    # ------------------------------------------------------------------
    # Geo Location
    # ------------------------------------------------------------------

    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Country resolved from the client's IP address.",
    )

    country_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text="ISO 3166-1 alpha-2 country code.",
    )

    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Region or state resolved from the client's IP address.",
    )

    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="City resolved from the client's IP address.",
    )

    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Approximate latitude resolved from the client's IP address.",
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Approximate longitude resolved from the client's IP address.",
    )

    # ------------------------------------------------------------------
    # Authentication Result
    # ------------------------------------------------------------------

    is_successful = models.BooleanField(
        default=True,
        help_text="Whether the login attempt was successful.",
    )

    failure_reason = models.TextField(
        null=True,
        blank=True,
        help_text="Reason for the login failure.",
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    updated_at = models.DateTimeField(
        auto_now=True,
    )

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

        indexes = [
            models.Index(
                fields=["user", "-created_at"],
                name="login_history_user_date_idx",
            ),
            models.Index(
                fields=["ip_address", "-created_at"],
                name="login_history_ip_date_idx",
            ),
            models.Index(
                fields=["is_successful", "-created_at"],
                name="login_history_status_date_idx",
            ),
        ]

    def __str__(self):
        status = "Success" if self.is_successful else "Failed"

        return f"{self.user} - " f"{status} - " f"{self.created_at}"
