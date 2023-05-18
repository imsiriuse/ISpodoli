from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking, Service
from datetime import datetime
from django.conf import settings

class BookingListView(LoginRequiredMixin, View):
    template_name = 'booking_list.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if not request.user.is_staff:
            services = Service.objects.filter(is_available=True)
            return render(request, 'service_list.html', {'services': services, 'media_url': settings.MEDIA_URL})

        today = datetime.now()

        pending = Booking.objects.filter(date=today.date(), hour__gt=today.hour)
        pending = pending | Booking.objects.filter(date__gt=today.date())
        pending = pending.order_by('date', 'hour')

        ongoing = Booking.objects.filter(date=today.date())
        ongoing = filter(lambda x: x.hour <= today.hour < x.hour + x.service.service_type.block_size, ongoing)

        past = Booking.objects.filter(date=today.date()).exclude(hour__gt=today.hour)
        past = past | Booking.objects.filter(date__lt=today.date())
        past = past.order_by('date', 'hour')

        context = {
            'pending': pending,
            'ongoing': ongoing,
            'bookings': past,
        }

        return render(request, 'booking_list.html', context)
