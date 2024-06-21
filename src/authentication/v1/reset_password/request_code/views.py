from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import ResetPasswordMessages

from .docs import docs
from .serializers import (
    ResetPasswordRequestCodeRequestSerializer,
    ResetPasswordRequestCodeResponseSerializer,
)
from .use_case import ResetPasswordRequestCodeUseCase


class ResetPasswordRequestCode(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """
        Return access and refresh token for the user if the user's email and password are correct
        """
        serializer = ResetPasswordRequestCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ResetPasswordRequestCodeUseCase().execute(
            email=serializer.validated_data["email"]
        )
        response_body = ResetPasswordRequestCodeResponseSerializer(
            {
                "message": ResetPasswordMessages.RESET_PASSWORD_REQUEST_CODE_SUCCESSFULLY.value
            }
        ).data
        return Response(
            response_body,
            status=status.HTTP_200_OK,
        )
