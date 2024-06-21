from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer


class SigninRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)


class SigninResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="SigninResponseDataSerializer",
        fields={
            "access_token": serializers.CharField(),
            "refresh_token": serializers.CharField(),
        },
    )
