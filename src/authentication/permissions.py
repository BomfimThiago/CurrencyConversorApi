from rest_framework import permissions

from .models import TermsOfAgreement, UserTermsOfAgreement


class UserAcceptedTermsOfAgreement(permissions.IsAuthenticated):
    message = "You have to accept the last Terms of Agreement to perform this action."

    def has_permission(self, request, view):
        last_agreement = TermsOfAgreement.objects.get_latest()
        has_accepted_last_term = (
            not last_agreement
            or UserTermsOfAgreement.objects.filter(
                user=request.user, terms_of_agreement=last_agreement
            ).exists()
        )

        return super().has_permission(request, view) and (has_accepted_last_term)
