from rest_framework import status

from authentication.enums.docs import Tags
from core.utils.docs.typing import Docs

from .serializers import SignupRequestSerializer, SignupResponseSerializer

docs: Docs = {
    "request": SignupRequestSerializer,
    "responses": {status.HTTP_201_CREATED: SignupResponseSerializer},
    "summary": "Sign up",
    "tags": [Tags.AUTHENTICATION.value],
    "methods": ["POST"],
}
