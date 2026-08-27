from django.db.models import QuerySet
from authentication.models import LoginHistoryModel


class LoginHistoryRepository:
    """
    Login history repository.
    """

    @staticmethod
    def create(**data) -> LoginHistoryModel:
        return LoginHistoryModel.objects.create(**data)

    @staticmethod
    def get_user_login_histories(user_id) -> QuerySet[LoginHistoryModel]:
        return (
            LoginHistoryModel.objects.filter(
                user_id=user_id,
            )
            .select_related(
                "user",
            )
            .order_by(
                "-created_at",
                "-id",
            )
        )
