from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from authentication.enums.docs import Tags
from authentication.enums.messages import AuthMessages
from core.utils.docs.typing import Docs

from .serializers import SignoutRequestSerializer

INVALID_ACCESS_TOKEN_RESPONSE = OpenApiExample(
    AuthMessages.INVALID_ACCESS_TOKEN.value,
    value={"detail": AuthMessages.INVALID_ACCESS_TOKEN.value},
    response_only=True,
    status_codes=["401"],
)

docs: Docs = {
    "methods": ["POST"],
    "request": SignoutRequestSerializer,
    "responses": {
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Sign out",
    "tags": [Tags.AUTHENTICATION.value],
    "examples": [INVALID_ACCESS_TOKEN_RESPONSE],
}
