from rest_framework import serializers
from rest_framework_simplejwt import serializers as simplejwt_serializers

from authentication.utils.jwt import refresh_token


class TokenRefreshRequestSerializer(simplejwt_serializers.TokenRefreshSerializer):
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        return refresh_token(attrs["refresh"])


class TokenRefreshResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
