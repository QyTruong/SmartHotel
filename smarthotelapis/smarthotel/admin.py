from django.contrib import admin
from .models import Category, Room, Service, User, BookingRoom
from django.contrib.auth.models import Group, Permission


class CategoryAdmin(admin.AdminSite):
    list_display = ['name', 'price']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available']
    search_fields = ['name']
    list_filter = ['id', 'name', 'is_available']



class MyAdminSite(admin.AdminSite):
    site_header = 'SmartHotel Admin'

    def get_urls(self):
        return super().get_urls()

admin_site = MyAdminSite(name='SmartHotel')

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)

admin_site.register(BookingRoom)
admin_site.register(Category)
admin_site.register(Service)
admin_site.register(Room, RoomAdmin)