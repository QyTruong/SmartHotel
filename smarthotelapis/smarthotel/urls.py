from django.urls import path, re_path, include
from . import views
from rest_framework.routers import DefaultRouter

r = DefaultRouter()
r.register('room-categories', views.RoomCategoryView, basename='room-category')
r.register('rooms', views.RoomView, basename='room')
r.register('service-categories', views.ServiceCategoryView, basename='service-category')
r.register('services', views.ServiceView, basename='service')
r.register('users', views.UserView, basename='user')

urlpatterns = [
    path('', include(r.urls)),
]