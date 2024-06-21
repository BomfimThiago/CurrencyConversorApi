from rest_framework_simplejwt.exceptions import AuthenticationFailed

from authentication.enums.codes import ErrorCodes
from authentication.enums.messages import AuthMessages


class InvalidToken(AuthenticationFailed):
    def __init__(self, detail=AuthMessages.TOKEN_INVALID.value):
        super().__init__(detail, ErrorCodes.TOKEN_NOT_VALID.value)
