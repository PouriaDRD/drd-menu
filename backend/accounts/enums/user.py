from django.db import models


class UserRole(models.TextChoices):
    USER = "user", "User"
    ADMIN = "admin", "Admin"
    SUPERUSER = "superuser", "Superuser"


class UserStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    BANNED = "banned", "Banned"
    INACTIVE = "inactive", "Inactive"
