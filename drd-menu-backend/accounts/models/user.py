import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from core import validators
from core.normalizers import normalize_phone_number

from accounts.managers import UserManager
from accounts.enums import UserRole, UserStatus


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model authenticated by Iranian phone number.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user.",
    )

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[validators.model_phone_number_validator],
        help_text="Iranian mobile number in the format 09XXXXXXXXX.",
        error_messages={
            "unique": "A user with this phone number already exists.",
        },
    )

    # -------------------------------------------------------------------------
    # Personal information
    # -------------------------------------------------------------------------

    first_name = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="User's first name.",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="User's last name.",
    )

    # -------------------------------------------------------------------------
    # Account
    # -------------------------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        db_index=True,
        help_text="Current account status.",
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        db_index=True,
        help_text="User role used for authorization.",
    )

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the user was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the user was last updated.",
    )

    # -------------------------------------------------------------------------
    # Manager
    # -------------------------------------------------------------------------

    objects = UserManager()

    # -------------------------------------------------------------------------
    # Authentication configuration
    # -------------------------------------------------------------------------

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS: list[str] = []

    # -------------------------------------------------------------------------
    # Django permissions
    # -------------------------------------------------------------------------

    @property
    def is_staff(self) -> bool:
        """
        Return whether the user can access the Django admin site.
        """
        return self.is_superuser or self.role in {
            UserRole.ADMIN,
            UserRole.SUPERUSER,
        }

    @property
    def is_active(self) -> bool:  # type: ignore
        """
        Return whether the user account is active.
        """
        return self.status == UserStatus.ACTIVE

    # -------------------------------------------------------------------------
    # Display helpers
    # -------------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        """
        Return the user's full display name.
        """
        return " ".join(
            part
            for part in (
                self.first_name.strip(),
                self.last_name.strip(),
            )
            if part
        )

    def __str__(self) -> str:
        if self.full_name.strip():
            return f"{self.full_name} ({self.phone_number})"

        return self.phone_number

    # -------------------------------------------------------------------------
    # Model lifecycle
    # -------------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Normalize the phone number before saving.
        """
        if self.phone_number:
            self.phone_number = normalize_phone_number(
                self.phone_number,
            )

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-created_at",)
