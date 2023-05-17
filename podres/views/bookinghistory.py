from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking
from datetime import datetime

class BookingHistoryView(LoginRequiredMixin, View):
    template_name = 'booking_history.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        today = datetime.now()

        past = Booking.objects.filter(date=today.date()).exclude(hour__gt=today.hour)
        past = past | Booking.objects.filter(date__lt=today.date())
        past = past.order_by('date', 'hour')

        context = {
            'bookings': past
        }
        return render(request, 'booking_history.html', context)
