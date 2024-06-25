from typing import Any

from core.models import User
from core.utils.use_cases.base import BaseUseCase
from transactions.models import Transaction
from transactions.services.exchangerate import ExchangeRatesAPI


class CreateUserTransactionUseCase(BaseUseCase):
    def execute(self, user: User, **transaction_data: Any) -> Transaction:
        """
        Register a new transaction
        Params:
            transaction_data: The user transaction info
        Returns: The registered Transaction instance
        """
        rates = ExchangeRatesAPI.get_exchange_rates()
        converted_amount, exchange_rate = ExchangeRatesAPI.convert_currency_via_eur(
            transaction_data["source_currency"],
            transaction_data["target_currency"],
            transaction_data["source_amount"],
            rates,
        )

        create_payload = {
            **transaction_data,
            "user": user,
            "converted_amount": converted_amount,
            "exchange_rate": exchange_rate,
        }

        return Transaction.objects.create(**create_payload)
