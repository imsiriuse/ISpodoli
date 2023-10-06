from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, reverse, get_object_or_404
from podres.models import Booker, Booking, Ban
from datetime import datetime
from django.contrib import messages
from django.utils.translation import activate, get_language, gettext_lazy as _

class UserDetailView(LoginRequiredMixin, View):
    template_name = 'user_detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def get(request, pk):
        if not request.user.is_staff:
            messages.add_message(request, messages.INFO, _("You are not authorized to do this action."))
            return redirect(reverse("service_list"))

        booker = get_object_or_404(Booker, id=pk)

        today = datetime.now()

        pending = Booking.objects.filter(date=today.date(), hour__gt=today.hour, booker=booker)
        pending = pending | Booking.objects.filter(date__gt=today.date(), booker=booker)
        pending = pending.order_by('date', 'hour')

        ongoing = Booking.objects.filter(date=today.date(), booker=booker)
        ongoing = filter(lambda x: x.hour <= today.hour < x.hour + x.service.service_type.block_size, ongoing)

        past = Booking.objects.filter(date=today.date(), booker=booker).exclude(hour__gt=today.hour)
        past = past | Booking.objects.filter(date__lt=today.date(), booker=booker)
        past = past.order_by('date', 'hour')

        bans = Ban.objects.filter(booker=booker)

        context = {
            'booker': booker,
            'pending': pending,
            'ongoing': ongoing,
            'past': past,
            'bans': bans,
        }

        return render(request, 'user_detail.html', context)
