from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import ResetPasswordMessages

from .docs import docs
from .serializers import (
    ResetPasswordValidateCodeRequestSerializer,
    ResetPasswordValidateCodeResponseSerializer,
)
from .use_case import ResetPasswordValidateCodeUseCase


class ResetPasswordValidateCode(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """
        Return a reset password authentication token if the reset password code is valid
        """
        serializer = ResetPasswordValidateCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64, token = ResetPasswordValidateCodeUseCase().execute(
            email=serializer.validated_data["email"],
            code=serializer.validated_data["code"],
        )
        return Response(
            {
                "message": ResetPasswordMessages.RESET_PASSWORD_VALIDATE_CODE_SUCEESSFUL.value,
                "data": ResetPasswordValidateCodeResponseSerializer(
                    {"uidb64": uidb64, "token": token}
                ).data,
            },
            status=status.HTTP_200_OK,
        )
