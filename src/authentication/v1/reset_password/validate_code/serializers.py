from rest_framework import serializers


class ResetPasswordValidateCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResetPasswordValidateCodeResponseSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
