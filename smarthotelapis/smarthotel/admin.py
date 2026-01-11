from itertools import count
from django.db.models import Count
from django.contrib import admin
from django.template.response import TemplateResponse

from .models import RoomCategory, Room, ServiceCategory, Service, User, BookingRoom, BookingService, Booking, Receipt
from django.contrib.auth.models import Group, Permission
from django.urls import path

class MyAdminSite(admin.AdminSite):
    site_header = 'SmartHotel Admin'

    def get_urls(self):
        url_stats_list = [
            path('occupancy-rate-stats/', self.occupancy_rate_stats_view),
            path('revenue-stats/', self.revenue_stats_view)
        ]
        return url_stats_list + super().get_urls()

    def occupancy_rate_stats_view(self, request):
        room_count = Room.objects.all().count()
        total_day_by_month = room_count * 30
        total_day_by_quarter = room_count * 30 * 4
        total_day_by_year = room_count * 365

        return TemplateResponse(request, 'admin/occupancy_rate_stats.html', {'room_count': room_count})

    def revenue_stats_view(self, request):
        pass


admin_site = MyAdminSite(name='SmartHotel')

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Permission)

admin_site.register(BookingRoom)
admin_site.register(BookingService)
admin_site.register(RoomCategory)
admin_site.register(Room)
admin_site.register(ServiceCategory)
admin_site.register(Service)
admin_site.register(Booking)
admin_site.register(Receipt)