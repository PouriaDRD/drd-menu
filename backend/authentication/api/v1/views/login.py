import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from authentication.api.v1.serializers import LoginSerializer

logger = logging.getLogger("LoginAPIView")


@extend_schema(
    tags=["Authentication"],
    summary="User login",
    description="""
Authenticate user with username and password.

On successful authentication, returns access and refresh tokens.

Possible errors:
- Invalid credentials
- Validation errors
- Too many login attempts
""",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login successful.",
        ),
        400: OpenApiResponse(
            description="Invalid credentials.",
        ),
        429: OpenApiResponse(
            description="Too many login attempts.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Login Example",
            value={
                "phone_number": "09123456789",
                "password": "********",
            },
            request_only=True,
        ),
        OpenApiExample(
            name="Invalid Credentials",
            value={
                "success": False,
                "code": "VALIDATION_ERROR",
                "message": "Validation failed.",
                "data": [],
                "errors": {
                    "phone_number": [
                        {
                            "message": "شماره موبایل یا رمز عبور اشتباه است.",
                            "code": "INVALID_CREDENTIALS",
                        }
                    ]
                },
            },
            response_only=True,
            status_codes=[
                "400",
            ],
        ),
    ],
)
class LoginAPIView(GenericAPIView):
    """
    User login endpoint.
    """

    serializer_class = LoginSerializer

    permission_classes = [AllowAny]

    throttle_scope = "login"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    http_method_names = [
        "post",
    ]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        auth_result = serializer.validated_data["auth_result"]

        return Response(
            data={
                "user": auth_result["user"],
                "access": auth_result["access"],
                "refresh": auth_result["refresh"],
                "access_expires_at": auth_result["access_expires_at"],
                "refresh_expires_at": auth_result["refresh_expires_at"],
            },
            status=status.HTTP_200_OK,
        )
