from django.urls import path, re_path, include
from . import views
from rest_framework.routers import DefaultRouter

r = DefaultRouter()

urlpatterns = [
    path('', include(r.urls)),
]