from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import AuthMessages

from .docs import docs
from .serializers import SignupRequestSerializer, SignupResponseSerializer
from .use_case import SignupUseCase


class Signup(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """
        Register a new user and return the user's data
        """
        serializer = SignupRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = SignupUseCase().execute(**serializer.validated_data)
        response_body = SignupResponseSerializer(
            {
                "message": AuthMessages.CREATE_USER_SUCCESSFULLY.value,
                "data": {"user": user},
            }
        ).data
        return Response(
            response_body,
            status=status.HTTP_201_CREATED,
        )
