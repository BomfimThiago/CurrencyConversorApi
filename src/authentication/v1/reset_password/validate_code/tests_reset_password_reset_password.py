from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import NotFound, PermissionDenied

from authentication.enums.messages import ResetPasswordMessages
from authentication.models import Code
from core.utils.use_cases.base import BaseUseCase


class ResetPasswordValidateCodeUseCase(BaseUseCase):
    def _get_reset_password_request(self, email, code):
        """
        Get The reset password request by its email and code
        Params:
            email: the reset password request user's email
            code: the reset password request code
        Returns: The Reset password request with matching user and code
        """
        reset_password_request = Code.objects.filter(
            user__email=email,
            code=code,
            type=Code.RESET_PASSWORD_REQUEST_TYPE,
        ).first()
        if not reset_password_request:
            raise NotFound(ResetPasswordMessages.RESET_PASSWORD_REQUEST_NOT_FOUND)
        if not reset_password_request.is_eligible_for_reset:
            raise PermissionDenied(
                ResetPasswordMessages.RESET_PASSWORD_SUBMIT_INVALID_CODE
            )
        return reset_password_request

    def _set_reset_password_request_used(self, reset_password_request):
        """
        Set password request as used
        Params:
            reset_password_request: the reset password request
        Returns: The updated reset_password_request instance
        """
        reset_password_request.was_used = True
        reset_password_request.save()
        return reset_password_request

    def _get_user_reset_password_auth_data(self, user):
        """
        Get the user request password authentication data
        Params:
            user: The user that will have its password reset
        Returns: tuple containing its unique id encoded in 64 bits and an authentication token
        """
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uidb64, token

    def execute(self, email, code):
        """
        Get password reset authentication data if a reset password request instance exists
        and is eligible for reset
        Params:
            email: The email of the user that will have its password reseted
            code: The code that was sent through Email / SMS that will validate the user
        Returns: A tuple with the user encrypted primary key and a token for its authentication
        """
        reset_password_request = self._get_reset_password_request(email, code)
        reset_password_request = self._set_reset_password_request_used(
            reset_password_request
        )
        user = reset_password_request.user
        return self._get_user_reset_password_auth_data(user)
