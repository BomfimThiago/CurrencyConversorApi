from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from authentication.enums.docs import Tags
from authentication.enums.messages import AuthMessages
from core.utils.docs.typing import Docs

from .serializers import ResetPasswordRequestSerializer, ResetPasswordResponseSerializer

WRONG_CREDENTIALS_RESPONSE = OpenApiExample(
    AuthMessages.WRONG_CREDENTIALS.value,
    value={"detail": AuthMessages.WRONG_CREDENTIALS.value},
    response_only=True,
    status_codes=["401"],
)


docs: Docs = {
    "request": ResetPasswordRequestSerializer,
    "responses": {
        status.HTTP_200_OK: ResetPasswordResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
    },
    "summary": "Reset password",
    "tags": [Tags.RESET_PASSWORD.value],
    "examples": [WRONG_CREDENTIALS_RESPONSE],
    "methods": ["POST"],
}
