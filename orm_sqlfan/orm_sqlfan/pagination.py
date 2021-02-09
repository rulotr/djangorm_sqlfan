from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE_SIZE = 4

class CustomPagination(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'enlace': {
                'siguiente': self.get_next_link(),
                'anterior': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'resultado': data
        })