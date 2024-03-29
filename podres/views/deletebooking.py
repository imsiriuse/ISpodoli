from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from podres.models import Booking
from django.contrib import messages


class DeleteBookingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        booking = Booking.objects.get(id=pk)

        if booking.booker.user == request.user or request.user.is_staff:
            booking.delete()
        else:
            messages.add_message(request, messages.INFO, "You are not authorized to do this action.")

        return redirect(request.META.get('HTTP_REFERER'))
