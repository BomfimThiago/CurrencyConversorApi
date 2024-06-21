from rest_framework.exceptions import NotFound

from authentication.enums.codes import ErrorCodes
from authentication.enums.messages import AuthMessages


class UserNotFound(NotFound):
    def __init__(self, detail=AuthMessages.USER_NOT_FOUND.value):
        super().__init__(detail, ErrorCodes.USER_NOT_FOUND.value)
