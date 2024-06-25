from core.models import User
from core.utils.use_cases.base import BaseUseCase
from transactions.models import Transaction
from transactions.utils import get_transactions_for_user


class GetUserTransactionsUseCase(BaseUseCase):
    def execute(self, user: User) -> Transaction:
        """
        Get transactions for user
        Params:
            transaction_data: The user transaction info
        Returns: The transactions of a user or empty list if user has not transactions yet
        """
        return get_transactions_for_user(user)
