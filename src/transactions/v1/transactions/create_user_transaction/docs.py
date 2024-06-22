from rest_framework import status

from core.utils.docs.typing import Docs
from transactions.enums.docs import Tags

from .serializers import (
    CreateUserTransactionRequestSerializer,
    CreateUseTransactionResponseSerializer,
)

docs: Docs = {
    "request": CreateUserTransactionRequestSerializer,
    "responses": {status.HTTP_201_CREATED: CreateUseTransactionResponseSerializer},
    "summary": "Create User Transaction",
    "tags": [Tags.TRANSACTION.value],
    "methods": ["POST"],
}
