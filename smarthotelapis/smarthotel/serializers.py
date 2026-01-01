from rest_framework import serializers
from smarthotel.models import Room, Category, Service, User


class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url

        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'price']

class RoomSerializer(ImageSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'is_available', 'image', 'category']

class ServiceSerializer(ImageSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description','price', 'image']

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

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['avatar'] = instance.avatar.url if instance.avatar else ''

        return data





