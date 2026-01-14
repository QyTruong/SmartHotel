def get_room_revenue_stats(request):
    room_revenue = BookingRoom.objects.filter(booking__status='CONFIRMED', booking__receipt__payment_status='PAID') \
        .annotate(
        nights=Func(F('end_date'), F('start_date'), function='DATEDIFF', output_field=IntegerField()
                    )
    ) \
        .annotate(
        revenue=F('nights') * F('price_per_night'),
    ) \
        .values('room__id', 'room__name') \
        .annotate(total_revenue=Sum('revenue'))