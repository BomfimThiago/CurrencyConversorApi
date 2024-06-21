from typing import Any

from core.models import User
from core.utils.use_cases.base import BaseUseCase


class SignupUseCase(BaseUseCase):
    def execute(self, **user_data: Any) -> User:
        """
        Register a new user
        Params:
            user_data: The user registration info
        Returns: The registered User instance
        """
        return User.objects.create_user(**user_data)
