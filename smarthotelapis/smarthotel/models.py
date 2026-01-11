from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class RoomCategory(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name

class Room(BaseModel):
    name = models.CharField(max_length=50, null=False)
    image = CloudinaryField(null=True)
    description = models.TextField(null=True)
    room_category = models.ForeignKey(RoomCategory, related_name='rooms', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ServiceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Service(BaseModel):
    name = models.CharField(max_length=50)
    image = CloudinaryField(null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    service_category = models.ForeignKey(ServiceCategory, related_name='services', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Booking(BaseModel):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELED = "CANCELED"

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    expires_at = models.DateTimeField(null=True, blank=True)

class Receipt(BaseModel):
    class PaymentStatus(models.TextChoices):
        UNPAID = "UNPAID"
        PAID = "PAID"

    class PaymentMethod(models.TextChoices):
        E_WALLET = "E_WALLET"
        CASH = "CASH"
        CARD = "CARD"

    booking = models.OneToOneField(Booking, on_delete=models.RESTRICT)
    total_amount = models.DecimalField(decimal_places=2, max_digits=12)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)


class BookingRoom(BaseModel):
    room = models.ForeignKey(Room, related_name='booking_rooms', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='booking_rooms',on_delete=models.CASCADE)

    price_per_night = models.DecimalField(decimal_places=2, max_digits=12)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)


class BookingService(BaseModel):
    service = models.ForeignKey(Service, related_name='booking_services', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='booking_services', on_delete=models.CASCADE)

    unit_price = models.DecimalField(decimal_places=2, max_digits=12)
    quantity = models.IntegerField(default=1)
    check_in = models.DateTimeField(null=True, blank=True)

