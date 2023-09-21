from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking, Booker, Ban
from datetime import date
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.conf import settings
import locale

class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def get(request):
        booker = Booker.objects.get(user=request.user)
        bookings = Booking.objects.filter(booker=booker).order_by('date', 'hour')
        bans = Ban.objects.filter(booker=booker, start_date__lte=date.today()).order_by('-start_date')

        context = {
            'bookings': bookings,
            'bans': bans,
        }

        return render(request, 'profile.html', context)
