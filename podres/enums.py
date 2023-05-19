from django.db import models

MAX_DAYS_AHEAD = 31

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


class RestrictionType(models.TextChoices):
    NO = 'n', 'No restriction'
    DAY = 'd', 'Day restriction'
    WEEK = 'w', 'Week restriction'
