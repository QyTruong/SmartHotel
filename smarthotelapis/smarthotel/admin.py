from itertools import count
from django.db.models import Count, Sum, Expression, ExpressionWrapper, F, Func, IntegerField
from django.contrib import admin
from django.db.models import DateField
from django.template.response import TemplateResponse
from .models import RoomCategory, Room, ServiceCategory, Service, User, BookingRoom, BookingService, Booking, Receipt
from django.contrib.auth.models import Group, Permission
from django.urls import path
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear, Cast, ExtractYear, ExtractMonth, ExtractDay


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


        return TemplateResponse(request, 'admin/occupancy_rate_stats.html', {'room_count': room_count})

    def revenue_stats_view(self, request):
        room_revenue = BookingRoom.objects.filter(booking__status='CONFIRMED', booking__receipt__payment_status='PAID')\

        kw = request.GET.get('kw')
        if kw:
            room_revenue = room_revenue.filter(room__name__icontains=kw)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if from_date:
            room_revenue = room_revenue.filter(booking__receipt__payment_date__gte=from_date)

        if to_date:
            room_revenue = room_revenue.filter(booking__receipt__payment_date__lte=to_date)

        room_revenue = room_revenue.annotate(
            nights=Func(F('end_date'), F('start_date'), function='DATEDIFF', output_field=IntegerField()
            )
        )\
        .annotate(
            revenue=F('nights') * F('price_per_night'),
        )\
        .values('room__id', 'room__name')\
        .annotate(total_revenue=Sum('revenue'))


        return TemplateResponse(request, 'admin/revenue_stats.html', {'room_revenue': room_revenue})


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