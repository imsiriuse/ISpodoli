from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking
from datetime import date


class BookingListView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        bookings = Booking.objects.filter(date__gte=date.today()).order_by('date', 'hour')
        if not bookings:
            return render(request, 'booking_list.html', { 'bookings': bookings })

        context = { 'bookings': bookings }
        return render(request, 'booking_list.html', context)
