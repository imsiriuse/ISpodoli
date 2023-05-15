from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking
from datetime import datetime

class BookingListView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        today = datetime.now()
        ongoing = Booking.objects.filter(date=today.date(), hour=today.hour).order_by('date', 'hour')
        pending = Booking.objects.filter(date__gte=today.date())
        pending = pending.exclude(date=today.date(), hour__lte=today.hour).order_by('date', 'hour')

        context = {
            'ongoing': ongoing,
            'pending': pending
        }
        return render(request, 'booking_list.html', context)
