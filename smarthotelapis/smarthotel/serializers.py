from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
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
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'avatar', 'email', 'groups']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_groups(self, user):
        return list(user.groups.values_list('name', flat=True))

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user

    def update(self, instance, validated_data):
        keys = set(validated_data.keys())
        if keys - {'first_name', 'last_name', 'email', 'phone'}:
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
        fields = ['id', 'booking_rooms', 'booking_services']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        booking_rooms_data = validated_data.pop('booking_rooms')
        booking_services_data = validated_data.pop('booking_services')

        booking = Booking.objects.create(user=user, expires_at=timezone.now() + timedelta(minutes=30))

        room_total_amount = 0
        for br in booking_rooms_data:
            nights = (br['end_date'] - br['start_date']).days
            room_total_amount += br['price_per_night'] * nights

            BookingRoom.objects.create(booking=booking, **br)
            
        service_total_amount = 0
        for bs in booking_services_data:
            service_total_amount += bs['unit_price'] * bs['quantity']
            
            BookingService.objects.create(booking=booking, **bs)
            
        total_amount = room_total_amount + service_total_amount

        Receipt.objects.create(booking=booking, total_amount=total_amount)

        return booking

class BookingDetailSerializer(serializers.ModelSerializer):
    booking_rooms = BookingRoomSerializer(many=True, read_only=True)
    booking_services = BookingServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_rooms', 'booking_services', 'status', 'expires_at']










