import logging
from typing import cast
from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

logger = logging.getLogger("TokenRefreshAPIView")


@extend_schema(
    tags=["Authentication"],
    summary="Refresh JWT tokens",
    description="""
Generate a new JWT access token using a valid refresh token.

If refresh token rotation is enabled, a new refresh token is also returned.
""",
    request=TokenRefreshSerializer,
)
class TokenRefreshAPIView(GenericAPIView):
    """
    Refresh JWT access token.
    """

    http_method_names = ["post"]

    permission_classes = [AllowAny]

    serializer_class = TokenRefreshSerializer

    throttle_scope = "refresh-token"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            access_lifetime = cast(
                timedelta,
                api_settings.ACCESS_TOKEN_LIFETIME,
            )
            access_expires_at = timezone.now() + access_lifetime

            refresh_lifetime = cast(
                timedelta,
                api_settings.REFRESH_TOKEN_LIFETIME,
            )
            refresh_expires_at = timezone.now() + refresh_lifetime

            logger.info("Token refreshed successfully. user=%s", str(request.user))

            return Response(
                data={
                    "access": serializer.validated_data["access"],
                    "access_expires_at": access_expires_at.isoformat(),
                    "refresh": serializer.validated_data["refresh"],
                    "refresh_expires_at": refresh_expires_at.isoformat(),
                },
                status=status.HTTP_200_OK,
            )
        except TokenError:
            raise ValidationError({"refresh": "Invalid or expired refresh token."})
