from django.db.models import QuerySet

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from authentication.models import LoginHistoryModel
from authentication.repositories import LoginHistoryRepository
from authentication.api.v1.serializers.login_history import (
    LoginHistorySerializer,
)


@extend_schema(
    tags=[
        "Authentication",
    ],
    summary="Get login history",
    description="""
Retrieve the authenticated user's login history.

This endpoint returns login attempts recorded by the authentication
system, including:

- Login status
- IP address
- Device type and family
- Browser and browser version
- Operating system and version
- Country and country code
- Region and city
- Latitude and longitude
- Login attempt timestamps

Only login history belonging to the currently authenticated user
is returned.

This endpoint is read-only. Login history records cannot be created,
updated, or deleted through the API.
""",
    responses={
        200: OpenApiResponse(
            response=LoginHistorySerializer(
                many=True,
            ),
            description="Login history retrieved successfully.",
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided or are invalid.",
        ),
    },
    examples=[
        OpenApiExample(
            name="Successful Login",
            value={
                "id": "406a818d-b313-4688-bd3d-2b27d17e26fc",
                "user": "4c8df53d-20ae-4c0b-a4a2-15dfcd4b5823",
                "is_successful": True,
                "failure_reason": None,
                "ip_address": "185.10.20.30",
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                ),
                "device": "PC",
                "device_family": None,
                "browser": "Chrome",
                "browser_version": "151.0.0",
                "operating_system": "Windows",
                "operating_system_version": "10",
                "country": "Iran",
                "country_code": "IR",
                "region": "Tehran",
                "city": "Tehran",
                "latitude": 35.6892,
                "longitude": 51.3890,
                "created_at": "2026-08-27T20:05:50.337104Z",
                "updated_at": "2026-08-27T20:05:50.337104Z",
            },
            response_only=True,
            status_codes=[
                "200",
            ],
        ),
        OpenApiExample(
            name="Localhost Login",
            value={
                "id": "406a818d-b313-4688-bd3d-2b27d17e26fc",
                "user": "4c8df53d-20ae-4c0b-a4a2-15dfcd4b5823",
                "is_successful": True,
                "failure_reason": None,
                "ip_address": "127.0.0.1",
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
                ),
                "device": "PC",
                "device_family": None,
                "browser": "Chrome",
                "browser_version": "151.0.0",
                "operating_system": "Windows",
                "operating_system_version": "10",
                "country": None,
                "country_code": None,
                "region": None,
                "city": None,
                "latitude": None,
                "longitude": None,
                "created_at": "2026-08-27T20:05:50.337104Z",
                "updated_at": "2026-08-27T20:05:50.337104Z",
            },
            response_only=True,
            status_codes=[
                "200",
            ],
        ),
        OpenApiExample(
            name="Unauthorized",
            value={"detail": "Authentication credentials were not provided."},
            response_only=True,
            status_codes=[
                "401",
            ],
        ),
    ],
)
class LoginHistoryAPIView(GenericAPIView):
    """
    Return login history of the authenticated user.
    """

    serializer_class = LoginHistorySerializer

    permission_classes = [
        IsAuthenticated,
    ]

    http_method_names = [
        "get",
    ]

    def get_queryset(self) -> QuerySet[LoginHistoryModel]:  # type: ignore
        """
        Return login history belonging only to the authenticated user.

        The user relation is selected in the same query to avoid
        unnecessary database queries when serializing the response.
        """

        return LoginHistoryRepository.get_user_login_histories(str(self.request.user.id))  # type: ignore

    def get(self, request: Request, *args, **kwargs):
        """
        Return the authenticated user's login history.
        """

        queryset = self.get_queryset()

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
