from rest_framework import serializers

from authentication.models import TermsOfAgreement
from core.utils.serializer.base import BaseResponseSerializer
from core.utils.serializer.inline_serializer import inline_serializer


class TermsGetResponseTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfAgreement
        fields = ("id", "terms_of_agreement", "created")


class TermsGetResponseSerializer(BaseResponseSerializer):
    data = inline_serializer(
        name="TermsGetDataResponseSerializer",
        fields={"terms": TermsGetResponseTermsSerializer()},
    )
