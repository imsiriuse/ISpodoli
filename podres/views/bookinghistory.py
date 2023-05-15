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
        bookings = Booking.objects.filter(date__lte=today.date())
        bookings = bookings.exclude(date=today.date(), hour__gte=today.hour)
        bookings = bookings.order_by('date', 'hour')

        context = {
            'bookings': bookings
        }
        return render(request, 'booking_history.html', context)
