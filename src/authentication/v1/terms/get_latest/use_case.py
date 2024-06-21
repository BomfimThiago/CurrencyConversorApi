from authentication.exceptions.term import TermNotFound
from authentication.models import TermsOfAgreement
from core.utils.use_cases.base import BaseUseCase


class GetLastAgreementUseCase(BaseUseCase):
    def execute(self) -> TermsOfAgreement | None:
        """
        Get the latest Terms of Agreement
        Returns: The latest Terms of Agreement instance
        """
        term = TermsOfAgreement.objects.get_latest()
        if not term:
            raise TermNotFound()
        return term
