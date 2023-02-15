from django.contrib import admin
from .models import ServiceType, Service, Booking

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Booking)
