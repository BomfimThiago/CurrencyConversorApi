from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer


class SignoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class SignoutResponseSerializer(BaseResponseSerializer):
    pass
