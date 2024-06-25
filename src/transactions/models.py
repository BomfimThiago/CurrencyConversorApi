from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
from core.utils.models.base import BaseModel

CURRENCY_CHOICES = [
    ("BRL", "Brazilian Real"),
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("JPY", "Japanese Yen"),
]


class Transaction(BaseModel):
    """
    Model for storing user transactions.
    """

    user = models.ForeignKey(
        User,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name=_("The User who is associated to this transaction"),
    )
    source_currency = models.CharField(
        verbose_name=_("Source Currency"), max_length=3, choices=CURRENCY_CHOICES
    )
    target_currency = models.CharField(
        verbose_name=_("Target Currency"), max_length=3, choices=CURRENCY_CHOICES
    )
    source_amount = models.DecimalField(
        verbose_name=_("Source Amount"), max_digits=10, decimal_places=2
    )
    converted_amount = models.DecimalField(
        verbose_name=_("Converted Amount"), max_digits=10, decimal_places=2
    )
    exchange_rate = models.DecimalField(
        verbose_name=_("Exchange Rate"), max_digits=10, decimal_places=6
    )

    class Meta:
        verbose_name = _("Transactions")
        ordering = ["-created"]

    def __str__(self):
        return _(f"Transaction {self.id} - User {self.user.username}")

    def clean(self):
        # target currency and source can not be of other type then the choices
        # source amount can not be negative
        pass
