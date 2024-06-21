from rest_framework_simplejwt.exceptions import TokenError

from authentication.exceptions.jwt import InvalidToken
from authentication.utils.jwt import RefreshToken
from core.utils.use_cases.base import BaseUseCase


class SignoutUseCase(BaseUseCase):
    def execute(self, refresh_token: str) -> None:
        """
        Blocklist the refresh_tokenj
        Params:
            refresh_token: The token that'll be blocklisted
        """
        try:
            # Todo: Add layer to util
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            raise InvalidToken()
