from django.urls import path

from transactions.v1.transactions.create_user_transaction.views import (
    CreateUserTransactionView,
)

urls = [
    path(
        "create-transaction",
        CreateUserTransactionView.as_view(),
        name="create-transaction",
    ),
]
