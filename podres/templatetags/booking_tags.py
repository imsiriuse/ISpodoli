from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='remaining_time')
def remaining_time(value):
    return (timedelta(days=value.duration) - (date.today() - value.start_date)).days

@register.filter(name='date_to_string')
def date_to_string(value):
    return value.strftime("%d-%m-%Y")

def hour_to_time(hour):
    if hour < 10:
        return f'0{hour}:00'
    else:
        return f'{hour}:00'

@register.filter(name='hour_to_time')
def get_interval(value, block_size=1):
    start = value
    if value + block_size > 24:
        end = 24
    else:
        end = value + block_size
    return hour_to_time(start) + ' - ' + hour_to_time(end)
