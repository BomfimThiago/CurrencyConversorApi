from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from authentication.exceptions.user import UserNotFound
from core.models import User
from core.utils.use_cases.base import BaseUseCase


class ResetPasswordUseCase(BaseUseCase):
    def _get_user_by_uidb64(self, uidb64: str) -> User | None:
        """
        Get the user by its encoded base 64 UID
        Params:
            uidb64: The user's base 64 UID
        Returns: The user that matches the base64 UID
        """
        uid = urlsafe_base64_decode(uidb64).decode()
        return User.objects.filter(pk=uid).first()

    def _set_password(self, user: User, password: str) -> None:
        """
        Set a password to the user
        Params:
            user: The user that will have the password set
            password: The password that is going to be set to the user
        """
        user.set_password(password)
        user.save()

    def execute(self, uidb64: str, token: str, password: str) -> None:
        """
        Validate the token and update the user's password
        Params:
            uidb64: Encrypted primary key
            token: Reset password authentication token
            password: The user's new password
        """
        user = self._get_user_by_uidb64(uidb64)
        if user and default_token_generator.check_token(user, token):
            return self._set_password(user, password)
        raise UserNotFound()
