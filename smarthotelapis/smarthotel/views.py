from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Room, BookingRoom, User
from .paginators import ServicePagination, RoomPagination
from .serializers import CategorySerializer, RoomSerializer, UserSerializer


class CategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RoomView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Room.objects.filter(active=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = RoomPagination

    def get_queryset(self):
        queryset = self.queryset

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            booking = BookingRoom.objects.values('room_id')\
                        .filter(start_date__lte=end_date,end_date__gt=start_date)

            queryset = queryset.exclude(id__in=booking)

        if min_price:
            queryset = queryset.filter(category__price__gte=min_price)

        if max_price:
            queryset = queryset.filter(category__price__lte=max_price)


        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset


class ServiceView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Room.objects.filter(active=True)
    serializer_class = RoomSerializer
    pagination_class = ServicePagination


class UserView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__('PATCH'):
            for key, value in request.data.items():
                if key in ['first_name', 'last_name', 'email']:
                    setattr(user, key, value)

            user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)