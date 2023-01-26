from django.db import models


class Service(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


class ServiceInstance(models.Model):
    label = models.CharField(max_length=20, help_text='Enter name')

    def __str__(self):
        return self.label


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
