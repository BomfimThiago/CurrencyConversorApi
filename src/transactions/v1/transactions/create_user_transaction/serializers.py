from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer
from transactions.exceptions.transactions import (
    TransactionSourceAmountMustBePositiveException,
)
from transactions.models import CURRENCY_CHOICES
from transactions.v1.transactions.base_serializer import TransactionSerializer


class CreateUserTransactionRequestSerializer(serializers.Serializer):
    source_currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    target_currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    source_amount = serializers.DecimalField(max_digits=5, decimal_places=2, default=1)

    def validate_source_amount(self, value):
        if value <= 0:
            raise TransactionSourceAmountMustBePositiveException()
        return value


class CreateUseTransactionResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="CreateUseTransactionResponseSerializer",
        fields={"transaction": TransactionSerializer()},
    )
