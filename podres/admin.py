# from django.contrib import admin
# from .models import ServiceType, Service
#
#
# @admin.register(Service)
# class ServiceInstanceAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields': ('label', 'service')
#         }),
#         ('Availability', {
#             'fields': ('active', 'closed')
#         }),
#     )
#
#
# class ServiceInstanceInline(admin.TabularInline):
#     model = Service
#
#
# @admin.register(ServiceType)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('label', 'calendar')
#     fields = ['label', 'calendar']
#     inlines = [ServiceInstanceInline]
from django.contrib import admin
from .models import RoomType, Room, Booking, BannedUser

class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_date', 'end_date')
    list_filter = ('user', 'room')
    search_fields = ('user__username', 'room__room_number')

admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BannedUser)
