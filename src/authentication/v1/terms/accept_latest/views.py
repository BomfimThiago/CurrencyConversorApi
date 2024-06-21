from django.http import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import TermsMessages
from core.models import User

from .docs import docs
from .serializers import TermsAcceptLatestResponseSerializer
from .use_case import AcceptLatestTermOfAgreementUseCase


class AuthenticatedHttpRequest(HttpRequest):
    user: User


class TermsAcceptance(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**docs)
    def post(self, request: AuthenticatedHttpRequest) -> Response:
        """
        Accept the latest Terms of Agreement.
        """
        user = request.user
        AcceptLatestTermOfAgreementUseCase().execute(user=user)
        response_body = TermsAcceptLatestResponseSerializer(
            {"message": TermsMessages.ACCEPTED_TERMS_OF_AGREEMENT_SUCCESSFULLY}
        ).data
        return Response(
            response_body,
            status=status.HTTP_201_CREATED,
        )
