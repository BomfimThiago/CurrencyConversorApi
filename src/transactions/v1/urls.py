from django.urls import include, path

from .transactions.urls import urls as transactions_urls

urls = [
    path("", include(transactions_urls)),
]
