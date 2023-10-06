from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from podres.models import Booking
from datetime import datetime
from django.contrib import messages
from django.utils.translation import activate, get_language, gettext_lazy as _

class BookingListView(LoginRequiredMixin, View):
    template_name = 'booking_list.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if not request.user.is_staff:
            messages.add_message(request, messages.INFO, _("You are not authorized to do this action."))
            return redirect(reverse("service_list"))

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
