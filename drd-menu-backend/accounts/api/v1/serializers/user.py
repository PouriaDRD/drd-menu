from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.handlers.codes import ErrorCode
from accounts.normalizers.user import (
    normalize_phone_number,
    normalize_username,
)

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating the authenticated user's profile.
    """

    class Meta:
        model = UserModel

        fields = (
            "id",
            "role",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "full_name",
            "status",
            "last_login",
            "created_at",
        )

        read_only_fields = (
            "id",
            "role",
            "status",
            "is_active",
            "is_superuser",
            "last_login",
            "updated_at",
            "created_at",
        )

    def validate(self, attrs):
        """
        Normalize user inputs before model validation.
        """

        username = attrs.get("username")
        if username is not None:
            attrs["username"] = normalize_username(username)

        phone_number = attrs.get("phone_number")
        if phone_number:
            attrs["phone_number"] = normalize_phone_number(phone_number)

        return attrs

    def validate_username(self, value):
        user = self.instance

        if UserModel.objects.exclude(pk=user.pk).filter(username=value).exists():  # type: ignore
            raise serializers.ValidationError(
                {
                    "message": "This username already exists.",
                    "code": ErrorCode.USERNAME_ALREADY_EXISTS,
                }
            )

        return value

    def validate_email(self, value):
        if not value:
            return value

        user = self.instance

        if UserModel.objects.exclude(pk=user.pk).filter(email=value).exists():  # type: ignore
            raise serializers.ValidationError(
                {
                    "message": "This email already exists.",
                    "code": ErrorCode.EMAIL_ALREADY_EXISTS,
                }
            )

        return value

    def validate_phone_number(self, value):
        if not value:
            return value

        user = self.instance

        if UserModel.objects.exclude(pk=user.pk).filter(phone_number=value).exists():  # type: ignore
            raise serializers.ValidationError(
                {
                    "message": "This phone number already exists.",
                    "code": ErrorCode.PHONE_ALREADY_EXISTS,
                }
            )

        return value
