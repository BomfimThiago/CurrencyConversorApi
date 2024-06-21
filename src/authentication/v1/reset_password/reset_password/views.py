from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import ResetPasswordMessages

from .docs import docs
from .serializers import ResetPasswordRequestSerializer, ResetPasswordResponseSerializer
from .use_case import ResetPasswordUseCase


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**docs)
    def post(self, request: Request, uidb64: str, token: str) -> Response:
        """Set a new password to the user if the token is valid"""
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ResetPasswordUseCase().execute(
            uidb64=uidb64, token=token, password=serializer.validated_data["password"]
        )
        response_body = ResetPasswordResponseSerializer(
            {"message": ResetPasswordMessages.RESET_PASSWORD_SUCCESSFULLY.value}
        ).data
        return Response(response_body, status=status.HTTP_200_OK)
