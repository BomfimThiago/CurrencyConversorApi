import jwt
from django.conf import settings
from jwt.exceptions import DecodeError, ExpiredSignatureError

from authentication.utils.jwt import api_settings
from core.models import User


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        authorization = request.META.get("HTTP_AUTHORIZATION", None)
        if authorization and "Bearer" in authorization:
            try:
                access_token = authorization.split("Bearer ")[1]
                token_data = jwt.decode(
                    str(access_token),
                    settings.SIMPLE_JWT.get("SIGNING_KEY"),
                    api_settings.ALGORITHM,
                )
            except (ExpiredSignatureError, DecodeError, IndexError):
                return response

            user_id = token_data.get("user").get("id")
            user = User.objects.get(id=user_id)
            response.user = user
        return response
