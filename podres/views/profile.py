from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from podres.models import Booking, Booker


class ProfileView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        booker = Booker.objects.get(user=request.user)
        bookings = Booking.objects.filter(booker=booker).order_by('date', 'hour')

        context = {
            'bookings': bookings
        }

        return render(request, 'profile.html', context)
