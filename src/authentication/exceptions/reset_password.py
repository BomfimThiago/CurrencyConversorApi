from rest_framework.exceptions import AuthenticationFailed, NotFound

from authentication.enums.codes import ErrorCodes
from authentication.enums.messages import ResetPasswordMessages


class ResetPasswordRequestNotFound(NotFound):
    def __init__(
        self, detail=ResetPasswordMessages.RESET_PASSWORD_REQUEST_NOT_FOUND.value
    ):
        super().__init__(detail, ErrorCodes.RESET_PASSWOD_NOT_FOUND.value)


class ResetPasswordInvalidCode(AuthenticationFailed):
    def __init__(
        self, detail=ResetPasswordMessages.RESET_PASSWORD_SUBMIT_INVALID_CODE.value
    ):
        super().__init__(detail, ErrorCodes.RESET_PASSWOD_INVALID_CODE.value)
