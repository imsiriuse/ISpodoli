from django.db import models
from django.urls import reverse


class Service(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')
    calendar = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.label


class ServiceInstance(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')
    service = models.ForeignKey(Service, on_delete=models.RESTRICT, null=False)
    active = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['label']

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


class Restriction(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class CalendarType(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class Reservation(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class User(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class TimeBlock(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class BlockSize(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class UserRestriction(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label
