from django.contrib.auth import authenticate

from authentication.exceptions.user import UserNotFound
from authentication.utils.jwt import get_tokens_for_user
from core.utils.use_cases.base import BaseUseCase


class SigninUseCase(BaseUseCase):
    def execute(self, email: str, password: str) -> dict:
        """
        Authenticate the user and returns its new token
        Params:
            email: The user's email
            password: The user's password
        Returns: The refreshed token
        """
        user = authenticate(email=email, password=password)
        if not user:
            raise UserNotFound()
        return get_tokens_for_user(user)
