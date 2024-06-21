from drf_spectacular.types import OpenApiTypes
from rest_framework import status

from authentication.enums.docs import Tags
from core.utils.docs.typing import Docs

from .serializers import TermsGetResponseSerializer

get_latest: Docs = {
    "tags": [Tags.TERMS.value],
    "summary": "Get the latest Terms of Agreement.",
    "responses": {
        status.HTTP_200_OK: TermsGetResponseSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
    },
    "methods": ["GET"],
}
