from django.contrib.auth.models import User
from django.db import models


class CalendarType(models.TextChoices):
    DAILY = 'D', 'Daily'
    WEEKLY = 'W', 'Weekly'
    MONTHLY = 'M', 'Monthly'


class BlockSize(models.TextChoices):
    HOUR = 'H', 'Hour'
    HALF_HOUR = '30', 'Half hour'
    DOUBLE_HOUR = '2H', 'Double hour'
    DAY = 'D', 'Day'
    WEEK = 'W', 'Week'


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


class ServiceType(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.TextField()
    block_size = models.CharField(
        max_length=2,
        choices=BlockSize.choices,
        default=BlockSize.HOUR,
    )

    calendar_type = models.CharField(
        max_length=1,
        choices=CalendarType.choices,
        default=CalendarType.DAILY,
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, default="")
    is_available = models.BooleanField(default=True)
    room_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"Room {self.name} of type {self.room_type}"


class Room(models.Model):
    block = models.CharField(max_length=1, choices=Building.choices, default=Building.A)
    floor = models.CharField(max_length=1, choices=Floor.choices, default=Floor.ZERO)
    side = models.CharField(max_length=1, choices=Side.choices, default=Side.NO)
    room = models.CharField(max_length=4, default="")

    def __str__(self):
        return f"Room {self.block} {self.room} {self.side}"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, null=True)
    start_date = models.DateField()

    def __str__(self):
        if self.service:
            return f"Booking for {self.service.name} from {self.start_date}"
