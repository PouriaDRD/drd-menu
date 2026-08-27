import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from authentication.services import LoginHistoryService

logger = logging.getLogger("authentication.backend")

UserModel = get_user_model()


class LoginHistoryBackend(ModelBackend):
    """
    Authentication backend that uses Django's standard ModelBackend
    while recording successful and failed login attempts.

    This backend does not change Django's authentication behavior.
    """

    login_history_service = LoginHistoryService

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = kwargs.get(
            UserModel.USERNAME_FIELD,
            username,
        )

        user = None

        try:
            user = super().authenticate(
                request=request,
                username=username,
                password=password,
                **kwargs,
            )

            if user is not None:
                self._log_success(
                    user=user,
                    request=request,
                )

                return user

            self._log_failed(
                identifier=identifier,
                request=request,
                reason="INVALID_CREDENTIALS",
            )

            return None

        except Exception:
            logger.exception(
                "Unexpected error during authentication for identifier=%s",
                identifier,
            )

            # Logging must never affect authentication.
            return user

    @classmethod
    def _log_success(cls, user, request):
        try:
            cls.login_history_service.log_success(
                user=user,
                request=request,
            )
        except Exception:
            logger.exception(
                "Failed to record successful login history for user_id=%s",
                user.pk,
            )

    @classmethod
    def _log_failed(cls, identifier, request, reason):
        if not identifier:
            return

        try:
            cls.login_history_service.log_failed(
                phone_number=str(identifier),
                request=request,
                reason=reason,
            )
        except Exception:
            logger.exception(
                "Failed to record failed login history for identifier=%s",
                identifier,
            )
