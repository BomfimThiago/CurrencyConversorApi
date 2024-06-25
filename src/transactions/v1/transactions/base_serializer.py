from rest_framework import serializers

from transactions.models import Transaction


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
