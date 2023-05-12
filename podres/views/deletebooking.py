from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from podres.models import Booking, Booker


class DeleteBookingView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        booking = Booking.objects.get(id=pk)

        if booking.booker.user != request.user:
            return redirect(request.META.get('HTTP_REFERER'))

        booking.delete()

        return redirect(request.META.get('HTTP_REFERER'))
