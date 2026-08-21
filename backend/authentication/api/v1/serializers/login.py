from rest_framework import serializers

from core.renderers.codes import ErrorCode
from core.normalizers import normalize_phone_number
from authentication.services import AuthService


class LoginSerializer(serializers.Serializer):

    auth_service = AuthService

    phone_number = serializers.CharField(
        max_length=11,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    def validate_phone_number(self, value):
        return normalize_phone_number(value)

    def validate(self, attrs):

        phone_number = attrs["phone_number"]

        password = attrs["password"]

        auth_result = self.auth_service.login(
            phone_number=phone_number,
            password=password,
            request=self.context["request"],
        )

        if auth_result is None:
            raise serializers.ValidationError(
                {
                    "phone_number": [
                        {
                            "message": "شماره موبایل یا رمز عبور اشتباه است.",
                            "code": ErrorCode.INVALID_CREDENTIALS,
                        }
                    ]
                }
            )

        attrs["auth_result"] = auth_result

        return attrs
