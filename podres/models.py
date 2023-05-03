from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Building(models.TextChoices):
    A = 'A', 'Building A'
    B = 'B', 'Building B'
    C = 'C', 'Building C'
    D = 'D', 'Building D'
    E = 'E', 'Building E'
    F = 'F', 'Building F'


class Floor(models.TextChoices):
    ZERO = '0', 'Ground floor'
    ONE = '1', 'First floor'
    TWO = '2', 'Second floor'
    THREE = '3', 'Third floor'
    FOUR = '4', 'Fourth floor'
    FIVE = '5', 'Fifth floor'


class Side(models.TextChoices):
    NO = 'n', 'No side'
    LEFT = 'a', 'Left side'
    RIGHT = 'b', 'Right side'


# TODO:
# delete null=True from all models
# delete defalut=None from all models
# add validators to all models

class ServiceType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    hour_min = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    hour_max = models.IntegerField(default=23, validators=[MinValueValidator(0), MaxValueValidator(23)])

    def __str__(self):
        return self.name

    def clean(self):
        if self.hour_min > self.hour_max:
            raise ValidationError('Hour min must be less than hour max')


class Service(models.Model):
    name = models.CharField(max_length=50, default="")
    is_available = models.BooleanField(default=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Service {self.name} of type {self.service_type.name}"


class Room(models.Model):
    block = models.CharField(max_length=1, choices=Building.choices, default=Building.A)
    floor = models.CharField(max_length=1, choices=Floor.choices, default=Floor.ZERO)
    side = models.CharField(max_length=1, choices=Side.choices, default=Side.NO)
    room = models.CharField(max_length=4, default="")

    def __str__(self):
        return f"Room {self.block} {self.room} {self.side}"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=None, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, null=True)
    date = models.DateField()
    hour = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])

    def __str__(self):
        if self.service:
            return f"Booking for {self.service.name} from {self.date}"
