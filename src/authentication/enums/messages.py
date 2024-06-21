from enum import Enum


class AuthMessages(Enum):
    CREATE_USER_SUCCESSFULLY = "User was created successfully"
    LOGIN_SUCCESSFUL = "Login successful"
    LOGOUT_SUCCESSFUL = "Logout successful"
    WRONG_CREDENTIALS = "Incorrect authentication credentials."
    USER_NOT_FOUND = "User not found"
    INVALID_ACCESS_TOKEN = "Invalid or expired access token."
    TOKEN_INVALID = "Token contained no recognizable user identification"


class ResetPasswordMessages(Enum):
    RESET_PASSWORD_REQUEST_CODE_SUCCESSFULLY = (
        "The reset password code was sent successfully"
    )
    RESET_PASSWORD_VALIDATE_CODE_SUCEESSFUL = "Code validation successful"
    RESET_PASSWORD_SUCCESSFULLY = "The password has been set successfully"
    RESET_PASSWORD_REQUEST_NOT_FOUND = "Password request was not found"
    RESET_PASSWORD_SUBMIT_INVALID_CODE = "The code is expired or has already been used"


class TermsMessages(Enum):
    GET_TERMS_OF_AGREEMENT_SUCCESSFULLY = "Terms of Agreement were found successfully"
    GET_TERMS_OF_AGREEMENT_NOT_FOUND = "Terms of Agreement not found"
    ACCEPTED_TERMS_OF_AGREEMENT_SUCCESSFULLY = (
        "Accepted Terms of Agreement were successfully"
    )
    ACCEPTED_TERMS_OF_AGREEMENT_NOT_FOUND = "Accepted Terms of Agreement not found"
