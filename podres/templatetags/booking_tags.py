from django import template

register = template.Library()

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
