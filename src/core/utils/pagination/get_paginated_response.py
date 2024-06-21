from typing import Any, Type

from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


def get_paginated_response(
    pagination_class: Type[BasePagination],
    serializer_class: Type[serializers.Serializer],
    queryset: QuerySet[Any],
    request: Request,
    view: APIView | None,
    message: str,
):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)
    return Response(data={**serializer.data, "message": message})
