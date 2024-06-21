from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer


class ResetPasswordRequestSerializer(serializers.Serializer):
    password = serializers.CharField(trim_whitespace=False)


class ResetPasswordResponseSerializer(BaseResponseSerializer):
    pass
