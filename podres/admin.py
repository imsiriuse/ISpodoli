from django.contrib import admin
from podres.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class BookerInline(admin.StackedInline):
    model = Booker
    can_delete = False
    verbose_name_plural = 'bookers'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (BookerInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Ban)
