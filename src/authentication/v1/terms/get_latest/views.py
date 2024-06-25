from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.enums.messages import TermsMessages

from .docs import get_latest
from .serializers import TermsGetResponseSerializer
from .use_case import GetLastAgreementUseCase


class TermsOfAgreements(APIView):
    permission_classes = [AllowAny]

    @extend_schema(**get_latest)
    def get(self, request: Request) -> Response:
        """
        Get the latest Terms of Agreement.
        """
        terms_of_agreement = GetLastAgreementUseCase().execute()
        response_body = TermsGetResponseSerializer(
            {
                "message": TermsMessages.GET_TERMS_OF_AGREEMENT_SUCCESSFULLY,
                "data": {
                    "terms": terms_of_agreement,
                },
            }
        ).data
        return Response(
            response_body,
            status=status.HTTP_200_OK,
        )
