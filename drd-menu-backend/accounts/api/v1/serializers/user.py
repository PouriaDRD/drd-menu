from rest_framework import serializers


from accounts.models import UserModel
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
