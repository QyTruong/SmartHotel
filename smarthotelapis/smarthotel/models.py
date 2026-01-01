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

class Category(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name

class Room(BaseModel):
    name = models.CharField(max_length=50, null=False)
    image = CloudinaryField(null=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, related_name='rooms', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Service(BaseModel):
    name = models.CharField(max_length=50)
    image = CloudinaryField(null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BookingRoom(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.RESTRICT,null=True, blank=True)

    price_per_night = models.DecimalField(decimal_places=2, max_digits=12)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)


class BookingService(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.RESTRICT, null=True, blank=True)

    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(decimal_places=2, max_digits=12)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
