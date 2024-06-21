from authentication.exceptions.term import TermNotFound
from authentication.models import TermsOfAgreement, UserTermsOfAgreement
from core.models import User
from core.utils.use_cases.base import BaseUseCase


class AcceptLatestTermOfAgreementUseCase(BaseUseCase):
    def execute(self, user: User) -> TermsOfAgreement:
        """
        Accept the Terms of Agreement
        Returns: The accepted Terms of Agreement instance
        """
        last_terms_of_agreement = TermsOfAgreement.objects.get_latest()
        if last_terms_of_agreement:
            return UserTermsOfAgreement.objects.accept_term_of_agreement(
                user=user, terms_of_agreement=last_terms_of_agreement
            )
        raise TermNotFound()
