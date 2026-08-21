import logging

from django.utils import timezone
from django.db import transaction
from django.contrib.auth import authenticate

from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from .token import TokenService
from .login_history import LoginHistoryService
from accounts.repositories import UserRepository
from core.normalizers import normalize_phone_number

logger = logging.getLogger("AuthService")


class AuthService:
    """
    Service layer for authentication business logic.
    Handles all business rules, validations, and orchestrates repository operations.
    """

    # Services
    token_service = TokenService
    login_history_service = LoginHistoryService

    # Repositories
    user_repo = UserRepository

    @classmethod
    def login(cls, phone_number: str, password: str, request: Request, **extra_fields):
        """
        Login user with phone number and password.

        Args:
            phone_number: The phone number to login.
            password: The password to login.
            request: The HTTP request object.

        Returns:
            Authentication response.

        Raises:
            ValidationError: If phone number or password is invalid.
        """
        phone_number = normalize_phone_number(phone_number)

        try:
            user = authenticate(
                request=request,  # type: ignore
                phone_number=phone_number,
                password=password,
            )

            if not user:
                cls.handle_failed_login(
                    phone_number=phone_number,
                    request=request,
                    reason="نام کاربری یا رمز عبور اشتباه است.",
                )

                return None

            cls.update_last_login(user)
            cls.login_history_service.log_success(user, request)

            return cls.auth_response(user)

        except ValidationError:
            return None

        except Exception as e:
            logger.exception(e)
            return None

    @classmethod
    def handle_failed_login(cls, phone_number: str, request: Request, reason: str):
        """
        Handle failed login.

        Args:
            phone_number: The phone_number that attempted to login.
            request: The HTTP request object.
            reason: Reason for login failure.

        """

        cls.login_history_service.log_failed(phone_number, request, reason)

    @classmethod
    def auth_response(cls, user):
        """
        Generate authentication response.

        Args:
            user: The authenticated user.

        Returns:
            Authentication response.
        """
        return {
            "user": str(user),
            **cls.token_service.generate(user),
        }

    @classmethod
    @transaction.atomic
    def update_last_login(cls, user):
        """
        Update last login time for user.
        """
        user.last_login = timezone.now()
        cls.user_repo.save(user, update_fields=["last_login"])
