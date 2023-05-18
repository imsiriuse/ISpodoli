from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, reverse, render
from podres.models import Service, Booking, Booker
from datetime import datetime, date, timedelta
from django.contrib import messages
from podres.enums import RestrictionType

class CreateBookingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def restriction_check(self, service, booker, day, month, year):
        if booker.user.is_staff:
            return None

        if service.service_type.restriction_type == RestrictionType.NO:
            return None

        if service.service_type.restriction_type == RestrictionType.DAY:
            bookings = Booking.objects.filter(service=service, booker=booker, date=date(year, month, day))
            if len(bookings) >= service.service_type.restriction_value:
                return "More bookings than allowed, max " + str(service.service_type.restriction_value) + " hours per day"

        if service.service_type.restriction_type == RestrictionType.WEEK:
            today = datetime(year, month, day)
            weekday = today.weekday()
            start_of_week = today - timedelta(days=weekday)
            end_of_week = start_of_week + timedelta(days=6)

            bookings = Booking.objects.filter(service=service, booker=booker)
            bookings = bookings.filter(date__gte=start_of_week, date__lte=end_of_week)

            if len(bookings) >= service.service_type.restriction_value:
                return "More bookings than allowed, max " + str(service.service_type.restriction_value) + " days per week"

        return None

    def validate(self, service, day, month, year, hour):
        today = datetime.now()
        if hour < service.service_type.hour_min or hour > service.service_type.hour_max:
            return "Hour out of range"

        if date(year, month, day) < today.date():
            return "Date in the past"

        if date(year, month, day) == today.date() and hour < today.hour:
            return "Hour in the past"

        for booking in Booking.objects.filter(service=service, date=date(year, month, day)):
            if booking.hour <= hour < booking.hour + booking.service.service_type.block_size:
                return "Hour already booked"

        return None

    def get(self, request, serviceid, day, month, year, hour):
        reverse_redirect = "%s?date=%d-%d-%d" % (reverse("service_detail", kwargs={"pk": serviceid}), day, month, year)

        service = Service.objects.get(id=serviceid)

        validation = self.validate(service, day, month, year, hour)
        if validation:
            messages.add_message(request, messages.INFO, validation)
            return redirect(reverse_redirect)

        booker = Booker.objects.get(user=request.user)

        restriction_check = self.restriction_check(service, booker, day, month, year)
        if restriction_check:
            messages.add_message(request, messages.INFO, restriction_check)
            return redirect(reverse_redirect)

        booking = Booking(
            booker=booker,
            service=service,
            date=date(year, month, day),
            hour=hour
        )

        booking.save()

        return redirect(reverse_redirect)
