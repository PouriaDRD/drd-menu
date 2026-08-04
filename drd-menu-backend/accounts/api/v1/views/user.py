import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import RetrieveUpdateAPIView

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from ..serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Retrieve and update authenticated user's profile.
    """

    http_method_names = [
        "get",
        "put",
        "patch",
    ]

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    throttle_scope = "user"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    def get_object(self):  # type: ignore
        """
        Return authenticated user instance.
        """

        return self.request.user

    @extend_schema(
        tags=["Accounts"],
        operation_id="get_current_user_profile",
        summary="Get current user profile",
        description=(
            "Returns the authenticated user's profile information.\n\n"
            "The response includes:\n"
            "- Basic account information\n"
            "- Contact information\n"
            "- Account role and status\n"
            "- Account timestamps\n\n"
            "Authentication is required."
        ),
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description=("User profile retrieved successfully."),
            ),
            401: OpenApiResponse(
                description=("Authentication credentials were not provided."),
            ),
            429: OpenApiResponse(
                description=("Too many requests. Rate limit exceeded."),
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve authenticated user's profile.
        """

        serializer = self.get_serializer(self.get_object())

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Accounts"],
        operation_id="update_current_user_profile",
        summary="Update current user profile",
        description=(
            "Updates editable fields of the authenticated user.\n\n"
            "Editable fields:\n"
            "- username\n"
            "- email\n"
            "- phone_number\n"
            "- first_name\n"
            "- last_name\n\n"
            "Username validation rules:\n"
            "- Must start with an English letter.\n"
            "- Only English letters, numbers and underscore (_) are allowed.\n"
            "- Persian characters are not accepted.\n\n"
            "Phone number validation rules:\n"
            "- Iranian mobile numbers only.\n"
            "- Stored format: 09XXXXXXXXX.\n"
            "- Supports input formats:\n"
            "  - 09121234567\n"
            "  - +989121234567\n"
            "  - 00989121234567\n\n"
            "Normalization:\n"
            "- Persian and Arabic digits are converted to English digits.\n"
            "- Phone number prefixes (+98, 0098, 98) are normalized.\n\n"
            "Protected fields:\n"
            "- role cannot be changed.\n"
            "- status cannot be changed.\n"
            "- permissions cannot be changed.\n\n"
            "Validation errors include a unique error code "
            "for frontend handling."
        ),
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description=("User profile updated successfully."),
            ),
            400: OpenApiResponse(
                description=(
                    "Validation error.\n\n"
                    "Example error codes:\n"
                    "- USERNAME_ALREADY_EXISTS\n"
                    "- EMAIL_ALREADY_EXISTS\n"
                    "- PHONE_ALREADY_EXISTS\n"
                    "- VALIDATION_ERROR"
                ),
            ),
            401: OpenApiResponse(
                description=("Authentication required."),
            ),
            429: OpenApiResponse(
                description=("Too many requests."),
            ),
        },
        examples=[
            OpenApiExample(
                name="Update Profile Example",
                value={
                    "username": "pouria_drd",
                    "email": "pouria@example.com",
                    "phone_number": "+989121234567",
                    "first_name": "Pouria",
                    "last_name": "Darandi",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Phone Number Normalization Example",
                value={
                    "phone_number": "۰۹۱۲۱۲۳۴۵۶۷",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Validation Error Example",
                value={
                    "status": False,
                    "code": "VALIDATION_ERROR",
                    "message": ("This username already exists."),
                    "data": [],
                    "errors": {
                        "username": {
                            "message": ("This username already exists."),
                            "code": ("USERNAME_ALREADY_EXISTS"),
                        }
                    },
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    def update(self, request, *args, **kwargs):
        """
        Replace authenticated user's editable profile fields.
        """

        try:
            response = super().update(
                request,
                *args,
                **kwargs,
            )

            logger.info(
                "User profile updated successfully. user=%s",
                request.user.id,
            )

            return response

        except Exception:
            logger.exception(
                "Failed to update user profile. user=%s",
                request.user.id,
            )

            raise

    @extend_schema(
        tags=["Accounts"],
        operation_id="partial_update_current_user_profile",
        summary="Partially update current user profile",
        description=(
            "Partially updates authenticated user's profile.\n\n"
            "Only provided fields will be updated.\n\n"
            "Validation and normalization rules are the same "
            "as the PUT endpoint."
        ),
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description=("User profile updated successfully."),
            ),
            400: OpenApiResponse(
                description=("Validation error with field error codes."),
            ),
            401: OpenApiResponse(
                description=("Authentication required."),
            ),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Handle PATCH requests.
        """

        return super().partial_update(
            request,
            *args,
            **kwargs,
        )
