from django.contrib import admin
from .models import Service, ServiceInstance


@admin.register(ServiceInstance)
class ServiceInstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('label', 'service')
        }),
        ('Availability', {
            'fields': ('active', 'closed')
        }),
    )


class ServiceInstanceInline(admin.TabularInline):
    model = ServiceInstance


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('label', 'calendar')
    fields = ['label', 'calendar']
    inlines = [ServiceInstanceInline]
