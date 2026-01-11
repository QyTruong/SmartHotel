from urllib import request

from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RoomCategory, Room, BookingRoom, User, Service, BookingService, Booking
from .paginators import ServicePagination, RoomPagination
from .serializers import RoomCategorySerializer, RoomSerializer, UserSerializer, ServiceCategorySerializer, \
    ServiceSerializer, BookingRoomSerializer, BookingDetailSerializer, BookingSerializer


class RoomCategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer

class RoomView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Room.objects.filter(active=True)
    serializer_class = RoomSerializer
    pagination_class = RoomPagination

    def get_queryset(self):
        queryset = self.queryset

        max_price = self.request.query_params.get('max_price')

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            busy_rooms = BookingRoom.objects.filter(
                booking__status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED
                ],
                start_date__lte=end_date,
                end_date__gte=start_date,
            ).values('room_id')

            queryset = Room.objects.filter(active=True).exclude(id__in=busy_rooms)

        if max_price:
            queryset = queryset.filter(room_category__price__lte=max_price)


        cate_id = self.request.query_params.get('room_category_id')
        if cate_id:
            queryset = queryset.filter(room_category_id=cate_id)

        return queryset


class ServiceCategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceCategorySerializer


class ServiceView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
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


class BookingView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        booking = Booking.objects.filter(user=request.user)
        serializer = BookingDetailSerializer(booking, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        booking = Booking.objects.filter(user=request.user, pk=pk)
        serializer = BookingDetailSerializer(booking, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        booking = Booking.objects.filter(user=request.user, pk=pk).first()

        if booking.status == Booking.Status.CANCELED or not booking:
            return Response({'error': 'Đăng ký này không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status != Booking.Status.PENDING:
            return Response({'message': 'Đăng ký này đã được thanh toán, không thể hủy'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.CANCELED
        booking.save()

        return Response({'message': 'Hủy đăng ký thành công'}, status=status.HTTP_204_NO_CONTENT)


