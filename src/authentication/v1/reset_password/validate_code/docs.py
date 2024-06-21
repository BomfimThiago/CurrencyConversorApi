from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from authentication.enums.docs import Tags
from authentication.enums.messages import ResetPasswordMessages
from core.utils.docs.typing import Docs

from .serializers import (
    ResetPasswordValidateCodeRequestSerializer,
    ResetPasswordValidateCodeResponseSerializer,
)

INVALID_RESET_PASSWORD_CODE_RESPONSE = OpenApiExample(
    ResetPasswordMessages.RESET_PASSWORD_SUBMIT_INVALID_CODE.value,
    value={"detail": ResetPasswordMessages.RESET_PASSWORD_SUBMIT_INVALID_CODE.value},
    response_only=True,
    status_codes=["403"],
)

RESET_PASSWORD_REQUEST_NOT_FOUND_RESPONSE = OpenApiExample(
    ResetPasswordMessages.RESET_PASSWORD_REQUEST_NOT_FOUND.value,
    value={"detail": ResetPasswordMessages.RESET_PASSWORD_REQUEST_NOT_FOUND.value},
    response_only=True,
    status_codes=["404"],
)


docs: Docs = {
    "request": ResetPasswordValidateCodeRequestSerializer,
    "responses": {
        status.HTTP_200_OK: ResetPasswordValidateCodeResponseSerializer,
        status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
    },
    "summary": "Reset password validate code",
    "tags": [Tags.RESET_PASSWORD.value],
    "examples": [
        INVALID_RESET_PASSWORD_CODE_RESPONSE,
        RESET_PASSWORD_REQUEST_NOT_FOUND_RESPONSE,
    ],
    "methods": ["POST"],
}
