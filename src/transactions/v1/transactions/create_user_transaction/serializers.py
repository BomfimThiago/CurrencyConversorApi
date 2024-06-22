from rest_framework import serializers

from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer
from transactions.models import CURRENCY_CHOICES, Transaction


class CreateUserTransactionRequestSerializer(serializers.Serializer):
    source_currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    target_currency = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    source_amount = serializers.DecimalField(max_digits=5, decimal_places=2)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "source_currency",
            "source_amount",
            "target_currency",
            "converted_amount",
            "exchange_rate",
            "created",
            "modified",
        )


class CreateUseTransactionResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="CreateUseTransactionResponseSerializer",
        fields={"transaction": TransactionSerializer()},
    )
