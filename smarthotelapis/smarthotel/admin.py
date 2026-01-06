from django.contrib import admin
from .models import RoomCategory, Room, ServiceCategory, Service, User, BookingRoom
from django.contrib.auth.models import Group, Permission


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
admin_site.register(RoomCategory)
admin_site.register(Room, RoomAdmin)
admin_site.register(ServiceCategory)
admin_site.register(Service)