from typing import Optional

from django.contrib.auth.models import BaseUserManager

from accounts.enums import UserRole, UserStatus
from accounts.normalizers import (
    normalize_phone_number,
    normalize_username,
)


class UserManager(BaseUserManager):
    """Custom manager responsible for creating and normalizing users."""

    def create_user(
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields,
    ):
        """
        Create and return a regular user.

        Args:
            username: Username used for authentication.
            password: Optional password. If omitted, an unusable password is set.
            **extra_fields: Additional model fields.

        Returns:
            UserModel
        """

        if not username:
            raise ValueError("The username field must be set.")

        username = normalize_username(username)

        phone_number = extra_fields.get("phone_number")
        if phone_number:
            extra_fields["phone_number"] = normalize_phone_number(phone_number)

        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        extra_fields.setdefault("role", UserRole.USER)
        extra_fields.setdefault("status", UserStatus.ACTIVE)

        user = self.model(
            username=username,
            **extra_fields,
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username: str,
        password: Optional[str] = None,
        **extra_fields,
    ):
        """
        Create and return a superuser.
        """

        if not password:
            raise ValueError("Superusers must have a password.")

        extra_fields.setdefault("role", UserRole.SUPERUSER)
        extra_fields.setdefault("status", UserStatus.ACTIVE)

        extra_fields.setdefault("email_verified", True)
        extra_fields.setdefault("phone_number_verified", True)

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, username):
        """
        Allow authentication using a normalized username.
        """

        username = normalize_username(username)

        return self.get(username=username)
