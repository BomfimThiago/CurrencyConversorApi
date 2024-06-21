from django.contrib import admin

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "modified",
        "id",
        "user",
        "source_currency",
        "target_currency",
        "source_amount",
        "converted_amount",
        "exchange_rate",
    )
    list_filter = ("created", "modified", "user")
