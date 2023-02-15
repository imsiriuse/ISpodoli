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


class ServiceType(models.Model):
    name = models.CharField(max_length=50)
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
    name = models.CharField(max_length=50)
    room_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.name} of type {self.room_type}"


class Booking(models.Model):
    room = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()

    def __str__(self):
        return f"Booking for room {self.room} from {self.start_date} by {self.user}"
