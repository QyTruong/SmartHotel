from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RoomCategory, Room, BookingRoom, User, Service
from .paginators import ServicePagination, RoomPagination
from .serializers import RoomCategorySerializer, RoomSerializer, UserSerializer, BookingRoomSerializer, \
    ServiceSerializer, ServiceCategorySerializer


class RoomCategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer

class RoomView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Room.objects.filter(active=True)
    serializer_class = RoomSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = RoomPagination

    def get_queryset(self):
        queryset = self.queryset

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:

            booking = BookingRoom.objects.values('room_id')\
                        .filter(start_date__lte=end_date, end_date__gt=start_date, active=True)

            queryset = queryset.exclude(id__in=booking)

        if min_price:
            queryset = queryset.filter(room_category__price__gte=min_price)

        if max_price:
            queryset = queryset.filter(room_category__price__lte=max_price)


        cate_id = self.request.query_params.get('room_category_id')
        if cate_id:
            queryset = queryset.filter(room_category_id=cate_id)

        return queryset

    @action(methods=['patch'], url_path="update-status", detail=True)
    def update_room_status(self, request, pk):
        room = self.get_object()
        s = RoomSerializer(room, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()

        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

class ServiceCategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = ServicePagination


class UserView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        user = request.user

        if request.method.__eq__('PATCH'):
            s = UserSerializer(user, data=request.data, partial=True)
            s.is_valid(raise_exception=True)
            user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='booking-rooms', detail=True, permission_classes=[permissions.IsAuthenticated])
    def get_booking_rooms(self, request, pk):
        booking_rooms = self.get_object().bookingroom_set.filter(active=True)

        return Response(BookingRoomSerializer(booking_rooms, many=True).data, status=status.HTTP_200_OK)


class BookingRoomView(viewsets.ViewSet, generics.CreateAPIView):
    pass

