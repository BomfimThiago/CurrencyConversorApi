from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import AuthMessages

from .docs import docs
from .serializers import SignoutRequestSerializer, SignoutResponseSerializer
from .use_case import SignoutUseCase


class Signout(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """Blocklist the refresh_token given in the payload"""
        serializer = SignoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.data["refresh_token"]
        SignoutUseCase().execute(refresh_token)
        response_body = SignoutResponseSerializer(
            {"message": AuthMessages.LOGOUT_SUCCESSFUL.value}
        ).data
        return Response(
            response_body,
            status=status.HTTP_204_NO_CONTENT,
        )
