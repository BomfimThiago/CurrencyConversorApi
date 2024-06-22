from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.enums.messages import TransactionMessages
from transactions.v1.transactions.create_user_transaction.use_case import (
    CreateUserTransactionUseCase,
)

from .docs import docs
from .serializers import (
    CreateUserTransactionRequestSerializer,
    CreateUseTransactionResponseSerializer,
)


class CreateUserTransactionView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**docs)
    def post(self, request: Request) -> Response:
        """
        Register a new user transaction and return the user's transaction data
        """
        serializer = CreateUserTransactionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = CreateUserTransactionUseCase().execute(
            user=request.user, **serializer.validated_data
        )
        response_body = CreateUseTransactionResponseSerializer(
            {
                "message": TransactionMessages.CREATE_TRANSACTION_SUCCESSFULLY.value,
                "data": {"transaction": transaction},
            }
        ).data
        return Response(
            response_body,
            status=status.HTTP_201_CREATED,
        )
