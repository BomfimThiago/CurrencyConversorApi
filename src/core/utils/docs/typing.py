from typing import NotRequired, TypedDict

from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers


class Docs(TypedDict):
    request: NotRequired[type[serializers.Serializer] | None]
    responses: object
    summary: str
    tags: list[str]
    examples: NotRequired[list[OpenApiExample]]
    methods: list[str]
