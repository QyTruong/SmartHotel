from django.urls import path, re_path, include
from . import views
from rest_framework.routers import DefaultRouter

r = DefaultRouter()
r.register('categories', views.CategoryView, basename='category')
r.register('rooms', views.RoomView, basename='room')
r.register('services', views.ServiceView, basename='service')
r.register('users', views.UserView, basename='user')

urlpatterns = [
    path('', include(r.urls)),
]