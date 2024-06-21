from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from authentication.enums.docs import Tags
from authentication.enums.messages import AuthMessages
from core.utils.docs.typing import Docs

from .serializers import TokenRefreshRequestSerializer, TokenRefreshResponseSerializer

WRONG_CREDENTIALS_RESPONSE = OpenApiExample(
    AuthMessages.WRONG_CREDENTIALS.value,
    value={"detail": AuthMessages.WRONG_CREDENTIALS.value},
    response_only=True,
    status_codes=["401"],
)

docs: Docs = {
    "methods": ["POST"],
    "request": TokenRefreshRequestSerializer,
    "responses": {
        status.HTTP_200_OK: TokenRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Refresh Token",
    "tags": [Tags.AUTHENTICATION.value],
}
