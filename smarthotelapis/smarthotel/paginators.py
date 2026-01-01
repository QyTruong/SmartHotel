from rest_framework.pagination import PageNumberPagination

class RoomPagination(PageNumberPagination):
    page_size = 2

class ServicePagination(PageNumberPagination):
    page_size = 5