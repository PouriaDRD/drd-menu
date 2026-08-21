from rest_framework import serializers


from accounts.models import UserModel
from core.renderers.codes import ErrorCode
from core.normalizers import normalize_phone_number


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating the authenticated user's profile.
    """

    class Meta:
        model = UserModel

        fields = (
            "id",
            "role",
            "phone_number",
            "first_name",
            "last_name",
            "full_name",
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

        phone_number = attrs.get("phone_number")
        if phone_number:
            attrs["phone_number"] = normalize_phone_number(phone_number)

        return attrs


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile fields.
    """

    class Meta:
        model = UserModel

        fields = (
            "first_name",
            "last_name",
        )

    def validate_first_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                {
                    "message": "First name is too short.",
                    "code": ErrorCode.FIRST_NAME_TOO_SHORT,
                }
            )

        return value

    def validate_last_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                {
                    "message": "Last name is too short.",
                    "code": ErrorCode.LAST_NAME_TOO_SHORT,
                }
            )

        return value
