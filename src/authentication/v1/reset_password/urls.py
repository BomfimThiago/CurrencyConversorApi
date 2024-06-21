from django.urls import path

from .request_code.views import ResetPasswordRequestCode
from .reset_password.views import ResetPassword
from .validate_code.views import ResetPasswordValidateCode

urls = [
    path(
        "reset-password/request-code",
        ResetPasswordRequestCode.as_view(),
        name="reset-password-request-code",
    ),
    path(
        "reset-password/validate-code",
        ResetPasswordValidateCode.as_view(),
        name="reset-password-validate-code",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>",
        ResetPassword.as_view(),
        name="reset-password",
    ),
]
