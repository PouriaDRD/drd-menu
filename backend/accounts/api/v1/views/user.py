import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from ..serializers import UserSerializer, UserProfileUpdateSerializer

logger = logging.getLogger(__name__)


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    """
    Retrieve authenticated user's profile.

    Supported methods:
    - GET: Retrieve current user profile.
    """

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    throttle_scope = "user"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    http_method_names = [
        "get",
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
        description=("Returns authenticated user's profile information."),
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description=("User profile retrieved successfully."),
            ),
            401: OpenApiResponse(
                description=("Authentication required."),
            ),
            429: OpenApiResponse(
                description=("Too many requests."),
            ),
        },
    )
    def get(self, request: Request, *args, **kwargs):
        """
        Retrieve authenticated user's profile.
        """
        logger.info("User profile retrieved successfully. user=%s", str(request.user))
        return self.retrieve(request, *args, **kwargs)


class UserProfileUpdateAPIView(UpdateAPIView):
    """
    Update authenticated user's profile.

    Supported methods:
    - PATCH: Partially update current user profile.
    """

    serializer_class = UserProfileUpdateSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    throttle_scope = "user"

    throttle_classes = [
        ScopedRateThrottle,
    ]

    http_method_names = [
        "patch",
    ]

    def get_object(self):  # type: ignore
        """
        Return authenticated user instance.
        """
        return self.request.user

    @extend_schema(
        tags=["Accounts"],
        operation_id="update_current_user_profile",
        summary="Update current user profile",
        description=("Partially updates the authenticated user's profile information."),
        request=UserProfileUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=UserProfileUpdateSerializer,
                description=("User profile updated successfully."),
            ),
            400: OpenApiResponse(
                description=("Validation error. Invalid data provided."),
            ),
            401: OpenApiResponse(
                description=("Authentication required."),
            ),
            429: OpenApiResponse(
                description=("Too many requests."),
            ),
        },
    )
    def patch(self, request: Request, *args, **kwargs):
        """
        Partially update authenticated user's profile.
        """
        logger.info("User profile updated successfully. user=%s", str(request.user))
        return self.partial_update(request, *args, **kwargs)
