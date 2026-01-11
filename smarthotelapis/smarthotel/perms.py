from rest_framework.permissions import IsAuthenticated

class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_staff

class BookingRoomOwner(IsAuthenticated):
    def has_object_permission(self, request, view, booking_room):
        return super().has_permission(request, view) and request.user == booking_room.user

class BookingServiceOwner(IsAuthenticated):
    def has_object_permission(self, request, view, booking_service):
        return super().has_permission(request, view) and request.user == booking_service.user