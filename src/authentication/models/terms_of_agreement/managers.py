from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class TermsOfAgreementManager(models.Manager):
    def get_latest(self):
        try:
            return self.earliest("created")
        except ObjectDoesNotExist:
            return None


class UserTermsOfAgreementManager(models.Manager):
    def accept_term_of_agreement(self, user, terms_of_agreement):
        return self.update_or_create(
            user=user, defaults={"user": user, "terms_of_agreement": terms_of_agreement}
        )
