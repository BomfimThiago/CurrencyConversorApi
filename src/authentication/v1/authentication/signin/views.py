from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import AuthMessages

from .docs import docs
from .serializers import SigninRequestSerializer, SigninResponseSerializer
from .use_case import SigninUseCase


class Signin(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """
        Return access and refresh token for the user if the user's email and password are correct
        """
        serializer = SigninRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = SigninUseCase().execute(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        response_body = SigninResponseSerializer(
            {
                "message": AuthMessages.LOGIN_SUCCESSFUL.value,
                "data": token_data,
            }
        ).data
        return Response(
            response_body,
            status=status.HTTP_200_OK,
        )
