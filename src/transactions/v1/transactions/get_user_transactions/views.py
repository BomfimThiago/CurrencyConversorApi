from drf_spectacular.utils import extend_schema
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.pagination.get_paginated_response import get_paginated_response
from core.utils.pagination.page_number_mixin import PageNumberPagination
from transactions.enums.messages import TransactionMessages
from transactions.v1.transactions.base_serializer import TransactionSerializer
from transactions.v1.transactions.get_user_transactions.use_case import (
    GetUserTransactionsUseCase,
)

from .docs import docs


class GetUserTransactionsView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    permission_classes = (IsAuthenticated,)

    @extend_schema(**docs)
    def get(self, request: Request) -> Response:
        """
        Get user transactions data
        """
        transactions = GetUserTransactionsUseCase().execute(user=request.user)
        return get_paginated_response(
            pagination_class=PageNumberPagination,
            serializer_class=TransactionSerializer,
            queryset=transactions,
            request=request,
            view=self,
            message=TransactionMessages.GET_USER_TRANSACTION_SUCCESFULLY.value,
        )
