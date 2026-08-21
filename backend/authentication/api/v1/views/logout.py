from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from ..serializers import LogoutSerializer

User = get_user_model()


@extend_schema(
    tags=["Authentication"],
    request=LogoutSerializer,
    summary="Logout",
    description="""
Logout the current user.

On successful logout, the refresh token is blacklisted.
""",
    responses={
        204: OpenApiResponse(
            description="Logout successful.",
        ),
        400: OpenApiResponse(
            description="Invalid refresh token.",
        ),
        500: OpenApiResponse(
            description="An unexpected error occurred.",
        ),
    },
)
class LogoutView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "logout"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]  # type: ignore
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
