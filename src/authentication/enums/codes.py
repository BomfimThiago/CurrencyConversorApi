from enum import Enum


class ErrorCodes(Enum):
    USER_NOT_FOUND = "user_not_found"
    USER_INACTIVE = "user_inactive"
    TOKEN_NOT_VALID = "token_not_valid"
    RESET_PASSWOD_NOT_FOUND = "reset_password_request_not_found"
    RESET_PASSWOD_INVALID_CODE = "reset_password_invalid_code"
    TERMS_NOT_FOUND = "terms_not_found"
