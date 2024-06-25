from django.urls import path

from transactions.v1.transactions.create_user_transaction.views import (
    CreateUserTransactionView,
)
from transactions.v1.transactions.get_user_transactions.views import (
    GetUserTransactionsView,
)

urls = [
    path(
        "get-user-transactions",
        GetUserTransactionsView.as_view(),
        name="get-user-transactions",
    ),
    path(
        "create-transaction",
        CreateUserTransactionView.as_view(),
        name="create-transaction",
    ),
]
