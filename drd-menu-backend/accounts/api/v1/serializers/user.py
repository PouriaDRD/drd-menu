from rest_framework import serializers

from common.handlers.codes import ErrorCode

from accounts.models import UserModel
from accounts.normalizers.user import (
    normalize_phone_number,
    normalize_username,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving authenticated user profile.
    """

    class Meta:
        model = UserModel

        fields = (
            "id",
            "role",
            "username",
            "email",
            "email_verified",
            "phone_number",
            "phone_number_verified",
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
            "email_verified",
            "phone_number_verified",
            "is_active",
            "is_superuser",
            "last_login",
            "created_at",
        )

    def validate(self, attrs):
        """
        Normalize user inputs before validation.
        """

        username = attrs.get("username")

        if username is not None:
            attrs["username"] = normalize_username(
                username,
            )

        phone_number = attrs.get("phone_number")

        if phone_number:
            attrs["phone_number"] = normalize_phone_number(
                phone_number,
            )

        return attrs

    def validate_username(self, value):
        """
        Validate username uniqueness.
        """

        queryset = UserModel.objects.exclude(
            pk=self.instance.pk,  # type: ignore
        )

        if queryset.filter(
            username=value,
        ).exists():

            raise serializers.ValidationError(
                {
                    "message": "This username already exists.",
                    "code": ErrorCode.USERNAME_ALREADY_EXISTS,
                }
            )

        return value

    def validate_email(self, value):
        """
        Validate email uniqueness.
        """

        if not value:
            return value

        queryset = UserModel.objects.exclude(
            pk=self.instance.pk,  # type: ignore
        )

        if queryset.filter(
            email=value,
        ).exists():

            raise serializers.ValidationError(
                {
                    "message": "This email already exists.",
                    "code": ErrorCode.EMAIL_ALREADY_EXISTS,
                }
            )

        return value

    def validate_phone_number(self, value):
        """
        Validate phone number uniqueness.
        """

        if not value:
            return value

        queryset = UserModel.objects.exclude(
            pk=self.instance.pk,  # type: ignore
        )

        if queryset.filter(
            phone_number=value,
        ).exists():

            raise serializers.ValidationError(
                {
                    "message": "This phone number already exists.",
                    "code": ErrorCode.PHONE_ALREADY_EXISTS,
                }
            )

        return value

    def update(self, instance, validated_data):
        """
        Update user profile.

        If email or phone number changes,
        related verification status will be reset.
        """

        old_email = instance.email
        old_phone_number = instance.phone_number

        new_email = validated_data.get(
            "email",
            old_email,
        )

        new_phone_number = validated_data.get(
            "phone_number",
            old_phone_number,
        )

        # Email changed
        if old_email != new_email:

            instance.email_verified = False

        # Phone changed
        if old_phone_number != new_phone_number:

            instance.phone_number_verified = False

        return super().update(
            instance,
            validated_data,
        )
