from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import User
from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer


class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    full_name = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
        )


class SignupResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="SignupResponseDataSerializer", fields={"user": UserSerializer()}
    )
