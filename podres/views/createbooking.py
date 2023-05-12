from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, reverse
from podres.models import Service, Booking, Booker
from datetime import date


class CreateBookingView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, serviceid, day, month, year, hour):
        service = Service.objects.get(id=serviceid)

        if hour < service.service_type.hour_min or hour > service.service_type.hour_max:
            return redirect('service_detail', pk=serviceid)

        booker = Booker.objects.get(user=request.user)

        booking = Booking(
            booker=booker,
            service=service,
            date=date(year, month, day),
            hour=hour
        )

        booking.save()

        previous_page = request.META.get('HTTP_REFERER')
        return redirect(previous_page)
