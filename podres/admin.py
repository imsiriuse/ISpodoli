from django.contrib import admin
from .models import ServiceType, Service, Booking, Room

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Room)
