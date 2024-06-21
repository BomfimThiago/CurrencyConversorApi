from django.urls import path

from .accept_latest.views import TermsAcceptance
from .get_latest.views import TermsOfAgreements

urls = [
    path("terms", TermsOfAgreements.as_view(), name="terms-of-agreement"),
    path(
        "terms/accept",
        TermsAcceptance.as_view(),
        name="accept-terms-of-agreement",
    ),
]
