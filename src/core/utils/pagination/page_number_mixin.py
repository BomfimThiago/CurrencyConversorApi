from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(_PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_size_query_param = "page_size"

    def get_paginated_data(self, data):
        return OrderedDict(
            [
                ("total", self.page.paginator.count),
                ("current_page", self.page.number),
                ("data", data),
            ]
        )

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("current_page", self.page.number),
                    ("data", data),
                ]
            )
        )
