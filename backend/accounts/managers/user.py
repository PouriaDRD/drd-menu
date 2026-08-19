from typing import Any

from django.contrib.auth.models import BaseUserManager

from accounts.enums import UserRole, UserStatus
from core.normalizers import normalize_phone_number


class UserManager(BaseUserManager):
    """
    Manager for the custom UserModel.

    Phone numbers are normalized before being used for authentication
    or persisted in the database.
    """

    def create_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and return a regular user.

        Args:
            phone_number: Phone number used for authentication.
            password: Optional password. If omitted, an unusable password
                is assigned.
            **extra_fields: Additional user model fields.

        Returns:
            UserModel: The newly created user.

        Raises:
            ValueError: If phone_number is not provided.
        """
        if not phone_number:
            raise ValueError("The phone_number field must be set.")

        phone_number = normalize_phone_number(phone_number)

        extra_fields.setdefault("role", UserRole.USER)
        extra_fields.setdefault("status", UserStatus.ACTIVE)

        user = self.model(
            phone_number=phone_number,
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
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and return a Django superuser.

        Args:
            phone_number: Phone number used for authentication.
            password: Password required for a superuser.
            **extra_fields: Additional user model fields.

        Returns:
            UserModel: The newly created superuser.

        Raises:
            ValueError: If phone_number or password is not provided.
        """
        if not phone_number:
            raise ValueError("Superusers must have a phone number.")

        if not password:
            raise ValueError("Superusers must have a password.")

        extra_fields.setdefault("role", UserRole.SUPERUSER)
        extra_fields.setdefault("status", UserStatus.ACTIVE)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusers must have is_superuser=True.")

        return self.create_user(
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )

    def get_by_natural_key(self, username: str):
        """
        Retrieve a user using a normalized phone number.

        ``username`` is kept as the parameter name to remain compatible
        with Django's BaseUserManager type signature. Since this project
        uses ``phone_number`` as USERNAME_FIELD, the value represents
        the user's phone number.
        """
        phone_number = normalize_phone_number(username)

        return self.get(phone_number=phone_number)
