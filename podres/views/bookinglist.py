from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking
from datetime import datetime

class BookingListView(LoginRequiredMixin, View):
    template_name = 'booking_list.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        today = datetime.now()

        pending = Booking.objects.filter(date=today.date(), hour__gt=today.hour)
        pending = pending | Booking.objects.filter(date__gt=today.date())
        pending = pending.order_by('date', 'hour')

        ongoing = Booking.objects.filter(date=today.date())
        ongoing = filter(lambda x: x.hour <= today.hour < x.hour + x.service.service_type.block_size, ongoing)

        context = {
            'pending': pending,
            'ongoing': ongoing,
        }

        return render(request, 'booking_list.html', context)
