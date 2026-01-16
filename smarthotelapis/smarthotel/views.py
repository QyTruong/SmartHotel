from django.utils import timezone
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RoomCategory, Room, BookingRoom, User, Service, Booking, Receipt
from .paginators import ServicePagination, RoomPagination
from .serializers import RoomCategorySerializer, RoomSerializer, UserSerializer, ServiceCategorySerializer, \
    ServiceSerializer, BookingSerializer


class RoomCategoryView(viewsets.ViewSet, generics.ListAPIView):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer

class RoomView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Room.objects.filter(active=True)
    serializer_class = RoomSerializer
    pagination_class = RoomPagination

    def get_queryset(self):
        queryset = self.queryset

        kw = self.request.query_params.get('kw')

        max_price = self.request.query_params.get('max_price')

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if kw:
            queryset = queryset.filter(name__icontains=kw)

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


class BookingView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @action(methods=['get'], url_path='my-bookings', detail=False)
    def get_bookings(self, request):
        queryset = self.get_queryset()
        return Response({
            'count': queryset.count(),
            'bookings': BookingSerializer(queryset, many=True).data
        })


    @action(methods=['delete'], url_path='cancel', detail=True)
    def cancel(self, request, pk):
        booking = Booking.objects.filter(pk=pk).first()

        if not booking:
            return Response({'error': 'Đăng ký không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == Booking.Status.CANCELED:
            return Response({'error': 'Đăng ký đã được hủy trước đó'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status == Booking.Status.CONFIRMED:
            return Response({'error': 'Không thể hủy đăng ký đã được thanh toán'}, status=status.HTTP_400_BAD_REQUEST)


        booking.status = Booking.Status.CANCELED
        booking.save()

        return Response({'message': 'Hủy đăng ký thành công'}, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['post'], detail=True, url_path='pay')
    def pay(self, request, pk):
        booking = Booking.objects.filter(user=request.user, pk=pk).first()

        if not booking:
            return Response({'error': 'Đăng ký không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == Booking.Status.CONFIRMED:
            return Response({'error': 'Đăng ký này đã được thanh toán, không thể thanh toán nữa'}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status == Booking.Status.CANCELED:
            return Response({'error': 'Đăng ký này đã bị hủy, không thể thanh toán'}, status=status.HTTP_400_BAD_REQUEST)


        receipt = booking.receipt
        payment_method = request.data.get('payment_method')

        receipt.payment_method = payment_method
        receipt.payment_status = Receipt.PaymentStatus.PAID
        receipt.payment_date = timezone.now()
        receipt.save()

        booking.status = Booking.Status.CONFIRMED
        booking.save()

        return Response({
            'message': 'Thanh toán thành công',
            'total_amount': receipt.total_amount,
            'payment_amount': receipt.payment_method
        }, status=status.HTTP_200_OK)


