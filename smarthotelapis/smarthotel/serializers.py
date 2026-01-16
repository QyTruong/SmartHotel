from django.db import transaction
from rest_framework import serializers
from smarthotel.models import Room, RoomCategory, Service, User, BookingRoom, ServiceCategory, BookingService, Booking, \
    Receipt


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url

        return data

class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = '__all__'


class RoomSerializer(ImageSerializer):
    room_category = RoomCategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'image', 'room_category']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name']

class ServiceSerializer(ImageSerializer):
    service_category = ServiceCategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'image', 'service_category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'avatar', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user

    def update(self, instance, validated_data):
        keys = set(validated_data.keys())
        if keys - {'first_name', 'last_name', 'email'}:
            raise serializers.ValidationError({'error': 'Các trường không hợp lệ'})

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else ''

        return data


class BookingRoomSerializer(serializers.ModelSerializer):
    room_name = serializers.SerializerMethodField()

    class Meta:
        model = BookingRoom
        fields = ['room', 'room_name', 'price_per_night', 'start_date', 'end_date']

    def get_room_name(self, obj):
        return obj.room.name


class BookingServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = BookingService
        fields = ['service', 'service_name', 'unit_price', 'quantity']

    def get_service_name(self, obj):
        return obj.service.name


class BookingSerializer(serializers.ModelSerializer):
    booking_rooms = BookingRoomSerializer(many=True)
    booking_services = BookingServiceSerializer(many=True, required=False)

    class Meta:
        model = Booking
        fields = ['id', 'booking_rooms', 'booking_services', 'status']

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        booking_rooms = validated_data.pop('booking_rooms')
        booking_services = validated_data.pop('booking_services')

        booking = Booking.objects.create(user=user)

        room_total_amount = 0
        for br in booking_rooms:
            start_date = br['start_date']
            end_date = br['end_date']
            price_per_night = br['price_per_night']
            room = br['room']


            if start_date > end_date:
                raise serializers.ValidationError({'error': 'Ngày bắt đầu phải trước ngày kết thúc'})

            conflict = BookingRoom.objects.filter(
                room=room, booking__status__in=[Booking.Status.CONFIRMED],
                start_date__lte=end_date, end_date__gte=start_date
            ).exists()

            if conflict:
                raise serializers.ValidationError({'error':
                    f'Phòng {room.name} đã được đặt trong khoảng thời gian {start_date} - {end_date}, '
                    f'Vui lòng đặt phòng hoặc ngày khác'
                })

            nights = (end_date - start_date).days + 1
            room_total_amount += price_per_night * nights

            BookingRoom.objects.create(booking=booking, **br)
            
        service_total_amount = 0
        for bs in booking_services:
            unit_price = bs['unit_price']
            quantity = bs['quantity']
            service = bs['service']

            if quantity <= 0:
                raise serializers.ValidationError(f'Vui lòng biết số lượng dịch vụ {service.name} bạn muốn đặt')

            service_total_amount += unit_price * quantity
            
            BookingService.objects.create(booking=booking, **bs)

            
        total_amount = room_total_amount + service_total_amount

        Receipt.objects.create(booking=booking, total_amount=total_amount)

        return booking











