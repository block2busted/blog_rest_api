from rest_framework import pagination


class ArticleListPagination(pagination.PageNumberPagination):
    page_size = 10
