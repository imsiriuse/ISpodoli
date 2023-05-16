from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking
from datetime import datetime

class BookingHistoryView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        today = datetime.now()

        past = Booking.objects.filter(date=today.date())
        past = past | Booking.objects.filter(date__lt=today.date())
        past = past.order_by('date', 'hour')
        past = filter(lambda x: x.hour + x.hour + x.service.service_type.block_size < today.hour, past)

        context = {
            'bookings': past
        }
        return render(request, 'booking_history.html', context)
