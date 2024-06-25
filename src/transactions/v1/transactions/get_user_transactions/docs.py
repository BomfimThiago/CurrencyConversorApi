from rest_framework import status

from core.utils.docs.typing import Docs
from transactions.enums.docs import Tags

from .serializers import GetUserTransactionsResponseSerializer

docs: Docs = {
    "responses": {
        status.HTTP_200_OK: GetUserTransactionsResponseSerializer,
    },
    "summary": "Get User Transactions",
    "tags": [Tags.TRANSACTION.value],
    "methods": ["GET"],
}
