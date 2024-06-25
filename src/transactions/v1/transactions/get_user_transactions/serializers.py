from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer
from transactions.v1.transactions.base_serializer import TransactionSerializer


class GetUserTransactionsResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="GetUserTransactionsResponseSerializer",
        fields={"transaction": TransactionSerializer()},
    )
