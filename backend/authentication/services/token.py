import datetime

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class TokenService:
    """
    Service layer responsible for generating, sending, validating,
    and enforcing rules for access and refresh tokens.
    """

    @classmethod
    def generate(cls, user: AbstractBaseUser):
        """
        Generates a new access and refresh token for the user.
        """

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        now = timezone.now()

        return {
            "access": str(access),
            "refresh": str(refresh),
            "access_expires_at": cls._safe_iso(now, api_settings.ACCESS_TOKEN_LIFETIME),
            "refresh_expires_at": cls._safe_iso(
                now, api_settings.REFRESH_TOKEN_LIFETIME
            ),
        }

    @staticmethod
    def _safe_iso(dt: datetime.datetime, delta) -> str:
        if isinstance(delta, datetime.timedelta):
            return (dt + delta).isoformat()
        return ""
