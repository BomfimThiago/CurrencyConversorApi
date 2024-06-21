from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User
from core.utils.models.base import BaseModel

from .managers import TermsOfAgreementManager, UserTermsOfAgreementManager


class TermsOfAgreement(BaseModel):
    """
    Model for the Terms of Agreement.
    """

    terms_of_agreement = models.TextField(
        _("Terms of Agreement"),
    )

    class Meta:
        verbose_name = _("Terms of Agreement")
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)

    objects: TermsOfAgreementManager = TermsOfAgreementManager()


class UserTermsOfAgreement(BaseModel):
    """
    Model for the Who Accepted Terms of Agreement.
    """

    user = models.OneToOneField(
        User,
        related_name="terms_of_agreement",
        on_delete=models.PROTECT,
        verbose_name="User who accepted the term",
    )
    terms_of_agreement = models.ForeignKey(
        TermsOfAgreement,
        related_name="who_accepted_terms_of_agreement",
        on_delete=models.PROTECT,
        verbose_name="Terms of Agreement ID",
    )

    class Meta:
        verbose_name = _("Who Accepted Terms of Agreement")

    objects: UserTermsOfAgreementManager = UserTermsOfAgreementManager()
