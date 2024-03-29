from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, reverse
from podres.models import Service, Booking, Booker, Ban
from datetime import datetime, date, timedelta
from django.contrib import messages
from podres.enums import RestrictionType
from podres.enums import MAX_DAYS_AHEAD

class CreateBookingView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @staticmethod
    def ban_check(booker):
        bans = Ban.objects.filter(booker=booker, start_date__lte=date.today()).order_by('-start_date')
        bans = filter(lambda x: x.start_date + timedelta(x.duration) > date.today(), bans)

        if any(bans) > 0:
            for ban in bans:
                messages.add_message(request, messages.INFO, "You are banned until " + str(ban.start_date + timedelta(ban.duration)))
            return True

        return False

    @staticmethod
    def restriction_check(service, booker, day, month, year):
        if booker.user.is_staff:
            return False

        if service.service_type.restriction_type == RestrictionType.NO:
            return False

        if service.service_type.restriction_type == RestrictionType.DAY:
            bookings = Booking.objects.filter(service=service, booker=booker, date=date(year, month, day))
            if len(bookings) >= service.service_type.restriction_value:
                messages.add_message(request, messages.INFO, "More bookings than allowed, max " + str(service.service_type.restriction_value) + " hours per day")
                return True

        if service.service_type.restriction_type == RestrictionType.WEEK:
            today = datetime(year, month, day)
            weekday = today.weekday()
            start_of_week = today - timedelta(days=weekday)
            end_of_week = start_of_week + timedelta(days=6)

            bookings = Booking.objects.filter(service=service, booker=booker)
            bookings = bookings.filter(date__gte=start_of_week, date__lte=end_of_week)

            if len(bookings) >= service.service_type.restriction_value:
                messages.add_message(request, messages.INFO, "More bookings than allowed, max " + str(service.service_type.restriction_value) + " hours per week")
                return True
        return False

    @staticmethod
    def validate(service, day, month, year, hour):
        today = datetime.now()
        if hour < service.service_type.hour_min or hour > service.service_type.hour_max:
            messages.add_message(request, messages.INFO, "Hour out of range, from " + str(service.service_type.hour_min) + " to " + str(service.service_type.hour_max))
            return True

        if date(year, month, day) < today.date():
            messages.add_message(request, messages.INFO, "Date in the past")
            return True

        if date(year, month, day) == today.date() and hour < today.hour:
            messages.add_message(request, messages.INFO, "Hour in the past")
            return True

        if date(year, month, day) > today.date() + timedelta(days=MAX_DAYS_AHEAD):
            messages.add_message(request, messages.INFO, "Date too far in the future, max " + str(MAX_DAYS_AHEAD) + " days ahead")
            return True

        for booking in Booking.objects.filter(service=service, date=date(year, month, day)):
            if booking.hour <= hour < booking.hour + booking.service.service_type.block_size:
                messages.add_message(request, messages.INFO, "Hour already booked")
                return True

        return False

    def get(self, request, serviceid, day, month, year, hour):
        reverse_redirect = "%s?date=%d-%d-%d" % (reverse("service_detail", kwargs={"pk": serviceid}), day, month, year)

        service = Service.objects.get(id=serviceid)
        booker = Booker.objects.get(user=request.user)

        if self.validate(service, day, month, year, hour):
            return redirect(reverse_redirect)

        if self.restriction_check(service, booker, day, month, year):
            return redirect(reverse_redirect)

        if self.ban_check(booker):
            return redirect(reverse_redirect)

        booking = Booking(
            booker=booker,
            service=service,
            date=date(year, month, day),
            hour=hour
        )

        booking.save()

        return redirect(reverse_redirect)
