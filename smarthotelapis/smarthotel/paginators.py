from rest_framework.pagination import PageNumberPagination

class RoomPagination(PageNumberPagination):
    page_size = 5

class ServicePagination(PageNumberPagination):
    page_size = 5