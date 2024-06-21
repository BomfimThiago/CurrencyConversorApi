from rest_framework import serializers


class BaseResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
