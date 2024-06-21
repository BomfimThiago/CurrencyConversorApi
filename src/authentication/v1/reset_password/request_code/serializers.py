from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer


class ResetPasswordRequestCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordRequestCodeResponseSerializer(BaseResponseSerializer):
    pass
