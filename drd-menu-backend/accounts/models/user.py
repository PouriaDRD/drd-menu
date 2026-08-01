import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.enums import UserRole, UserStatus
from accounts.managers import UserManager
from accounts.validators import user


class UserModel(AbstractBaseUser, PermissionsMixin):
    """Custom user model used for authentication."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user.",
    )

    # Authentication username
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[user.username_validator],
        help_text=(
            "Required. Must start with an English letter and may contain only "
            "English letters, numbers and underscore (_)."
        ),
        error_messages={
            "unique": "A user with this username already exists.",
        },
    )

    # Optional email address
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        validators=[user.email_validator],
        help_text="Optional. Must be a valid email address.",
        error_messages={
            "unique": "A user with this email already exists.",
        },
    )
    email_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the email address has been verified.",
    )

    # Optional mobile number
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        validators=[user.phone_number_validator],
        help_text=("Optional. Iranian mobile number in the format 09XXXXXXXXX."),
        error_messages={
            "unique": "A user with this phone number already exists.",
        },
    )
    phone_number_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the phone number has been verified.",
    )

    # Personal information
    first_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional first name.",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional last name.",
    )

    # User account status
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
        db_index=True,
        help_text="Current account status.",
    )

    # User role
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        db_index=True,
        help_text="Role used for permissions.",
    )

    # Audit fields
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last modification time.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation time.",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"

    @property
    def is_staff(self) -> bool:
        """Return whether the user has access to Django admin."""
        return self.is_superuser or self.role in (
            UserRole.ADMIN,
            UserRole.SUPERUSER,
        )

    @property
    def is_active(self) -> bool:  # type: ignore
        """Return whether the account is active."""
        return self.status == UserStatus.ACTIVE

    @property
    def full_name(self) -> str:
        """Return the user's display name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-created_at",)
