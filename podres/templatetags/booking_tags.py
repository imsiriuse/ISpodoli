from django import template
from ..enums import BookingStatus
from datetime import datetime

register = template.Library()

@register.filter(name='get_status')
def get_status(value):
    date = value.date
    hour = value.hour

    today = datetime.now()

    if date == today.date():
        if hour == today.hour:
            return BookingStatus.ONGOING
        if hour < today.hour:
            return BookingStatus.PAST
        if hour > today.hour:
            return BookingStatus.PENDING

    if date < today.date():
        return BookingStatus.PAST

    return BookingStatus.PENDING

@register.filter(name='hour_to_time')
def hour_to_time(value):
    if value < 10:
        return f'0{value}:00'
    else:
        return f'{value}:00'
