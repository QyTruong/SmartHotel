from rest_framework import serializers
from smarthotel.models import Room, RoomCategory, Service, User, BookingRoom, ServiceCategory, BookingService


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url

        return data

class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = ['id', 'name', 'price']

class RoomSerializer(ImageSerializer):
    room_category = RoomCategorySerializer()

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'is_available', 'image', 'room_category']

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name']

class ServiceSerializer(ImageSerializer):
    service_category = ServiceCategorySerializer()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description','price', 'image', 'service_category']

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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['avatar'] = instance.avatar.url if instance.avatar else ''

        return data

class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = ['id', 'user', 'room','price_per_night', 'start_date', 'end_date', 'check_in', 'check_out']

class BookingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingService
        fields = ['id', 'user', 'service', 'price']


