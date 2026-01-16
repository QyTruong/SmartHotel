
from django.db.models import Sum
from django.contrib import admin
from django.utils import timezone
from django.db.models import DateField
from django.template.response import TemplateResponse
from .models import RoomCategory, Room, ServiceCategory, Service, User, BookingRoom, BookingService, Booking, Receipt
from django.contrib.auth.models import Group, Permission
from django.urls import path
from django.db.models.functions import  Cast, ExtractMonth


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
        year = request.GET.get('year')
        if not year:
            year = timezone.now().year

        revenue_by_month = Receipt.objects.filter(payment_status=Receipt.PaymentStatus.PAID, payment_date__year=year)\
                            .annotate(month=ExtractMonth(Cast('payment_date', DateField())))\
                            .values('month')\
                            .annotate(total_revenue=Sum('total_amount'))\
                            .order_by('month')


        return TemplateResponse(request, 'admin/revenue_stats.html',
                                {'revenue_by_month': revenue_by_month})


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