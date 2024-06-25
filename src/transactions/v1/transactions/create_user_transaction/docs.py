from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from core.utils.docs.typing import Docs
from transactions.enums.docs import Tags
from transactions.enums.messages import TransactionMessages

from .serializers import (
    CreateUserTransactionRequestSerializer,
    CreateUseTransactionResponseSerializer,
)

SOURCE_AMOUNT_MUST_BE_POSITIVE_RESPONSE = OpenApiExample(
    TransactionMessages.SOURCE_AMOUNT_MUST_BE_POSITIVE.value,
    value={"detail": TransactionMessages.SOURCE_AMOUNT_MUST_BE_POSITIVE.value},
    response_only=True,
    status_codes=["400"],
)


docs: Docs = {
    "request": CreateUserTransactionRequestSerializer,
    "responses": {
        status.HTTP_201_CREATED: CreateUseTransactionResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
    },
    "summary": "Create User Transaction",
    "tags": [Tags.TRANSACTION.value],
    "examples": [
        SOURCE_AMOUNT_MUST_BE_POSITIVE_RESPONSE,
    ],
    "methods": ["POST"],
}
