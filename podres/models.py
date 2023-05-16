from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from .enums import *

def validate_svg(val):
    if not val.name.endswith('.svg'):
        raise ValidationError('Only svg files allowed')

class ServiceType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    hour_min = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    hour_max = models.IntegerField(default=23, validators=[MinValueValidator(0), MaxValueValidator(23)])
    block_size = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(24)])

    image = models.FileField(
        default=None,
        blank=True,
        upload_to='images/',
        validators=[ validate_svg ],
    )

    def __str__(self):
        return self.name

    def clean(self):
        if self.hour_min > self.hour_max:
            raise ValidationError('Hour min must be less than hour max')


class Service(models.Model):
    name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service_type.name} {self.name}"


class Room(models.Model):
    block = models.CharField(max_length=1, choices=Building.choices, default=Building.A)
    floor = models.CharField(max_length=1, choices=Floor.choices, default=Floor.ZERO)
    side = models.CharField(max_length=1, choices=Side.choices, default=Side.NO)
    room = models.CharField(max_length=4, default="")

    def __str__(self):
        return f"{self.block} {self.room} {self.side}"


class Booker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def clean(self):
        if not self.user:
            raise ValidationError('User must be set')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booker = models.ForeignKey(Booker, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])

    def __str__(self):
        if self.service:
            return f"Booking for {self.service.name} from {self.date}"
