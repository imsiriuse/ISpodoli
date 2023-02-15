from django.contrib.auth.models import User
from django.db import models


class CalendarType(models.TextChoices):
    DAILY = 'D', 'Daily'
    WEEKLY = 'W', 'Weekly'
    MONTHLY = 'M', 'Monthly'


class RoomType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    calendar_type = models.CharField(
        max_length=1,
        choices=CalendarType.choices,
        default=CalendarType.DAILY,
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.PositiveIntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    building_mark = models.CharField(max_length=1)
    banned_users = models.ManyToManyField(User, through='BannedUser', related_name='banned_rooms')

    def __str__(self):
        return f"Room {self.room_number}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Booking for room {self.room} from {self.start_date} to {self.end_date}"


class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    banned_from = models.DateField()
    banned_to = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.user} banned from {self.room} from {self.banned_from} to {self.banned_to} for reason: {self.reason}"
