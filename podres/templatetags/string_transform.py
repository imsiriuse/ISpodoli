from django import template

register = template.Library()

@register.filter(name='hour_to_time')
def hour_to_time(value):
    if value < 10:
        return f'0{value}:00'
    else:
        return f'{value}:00'
