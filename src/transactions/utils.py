from django.contrib.auth.models import AbstractBaseUser

from transactions.models import Transaction


def get_transactions_for_user(user: AbstractBaseUser) -> dict:
    """
    Get translations for the user
    Params:
        user: The user from which the translation belong to
    Returns: The user's transactions
    """
    transactions = Transaction.objects.filter(user=user)
    return transactions
