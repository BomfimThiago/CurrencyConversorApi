from rest_framework.exceptions import NotFound

from authentication.enums.codes import ErrorCodes
from authentication.enums.messages import TermsMessages


class TermNotFound(NotFound):
    def __init__(self, detail=TermsMessages.ACCEPTED_TERMS_OF_AGREEMENT_NOT_FOUND.value):
        super().__init__(detail, ErrorCodes.TERMS_NOT_FOUND.value)
