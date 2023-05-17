from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, reverse
from podres.models import Service, Booking, Booker
from datetime import date


class CreateBookingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def validate(self, service, day, month, year, hour):
        today = date.today()
        if hour < service.service_type.hour_min or hour > service.service_type.hour_max:
            raise Exception('Hour out of range')

        if date(year, month, day) < today:
            raise Exception('Date in the past')

        if date(year, month, day) == today and hour < today.hour:
            raise Exception('Hour in the past')

        bookings = Booking.objects.filter(service=service, date=date(year, month, day))

        for booking in bookings:
            if booking.hour <= hour < booking.hour + booking.service.service_type.block_size:
                raise Exception('Booking already exists')

        return True

    def get(self, request, serviceid, day, month, year, hour):
        service = Service.objects.get(id=serviceid)

        try:
            self.validate(service, day, month, year, hour)
        except Exception as e:
            print(e)
            return redirect("%s?date=%d-%d-%d" % (reverse("service_detail", kwargs={"pk": serviceid}), day, month, year))

        booker = Booker.objects.get(user=request.user)

        booking = Booking(
            booker=booker,
            service=service,
            date=date(year, month, day),
            hour=hour
        )

        booking.save()
        return redirect("%s?date=%d-%d-%d" % (reverse("service_detail", kwargs={"pk": serviceid}), day, month, year))
