from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt import views

from .docs import docs
from .serializers import TokenRefreshRequestSerializer


@extend_schema(**docs)
class TokenRefreshView(views.TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = TokenRefreshRequestSerializer
