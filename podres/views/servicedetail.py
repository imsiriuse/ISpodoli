from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from podres.models import Service, Booking
from datetime import date, datetime, timedelta
from podres.enums import MAX_DAYS_AHEAD
from podres.plugins.bookingcalendar import BookingCalendar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class ServiceDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    @staticmethod
    def get_restriction_name(service):
        if service.service_type.restriction_type == 'w':
            return 'week'
        if service.service_type.restriction_type == 'd':
            return 'day'
        return ''

    @staticmethod
    def parse_query(query):
        result = {}
        if 'date' not in query:
            result['date'] = date.today()
        else:
            try:
                result['date'] = datetime.strptime(query['date'], '%d-%m-%Y').date()
            except ValueError:
                result['date'] = date.today()
        return result

    @staticmethod
    def date_valid( act_date):
        if act_date < (date.today() - timedelta(days=MAX_DAYS_AHEAD)) or act_date > (date.today() + timedelta(days=MAX_DAYS_AHEAD)):
            return False
        return True

    @staticmethod
    def timetable(service, today):
        start = service.service_type.hour_min
        end = service.service_type.hour_max
        block_size = service.service_type.block_size

        bookings = Booking.objects.filter(service=service, date=today)
        bookings = filter(lambda b: start <= b.hour <= end, bookings)

        result = [None] * ((end - start + 1)//block_size)

        for booking in bookings:
            result[(booking.hour - start)//block_size] = booking

        return zip(result, range(start, end + 1, block_size))

    def post(self, request, pk):
        pass

    def get(self, request, pk):
        service = get_object_or_404(Service, id=pk)

        queries = self.parse_query(request.GET.dict())
        referer = request.META.get('HTTP_REFERER', None)

        if not service.is_available:
            messages.add_message(request, messages.INFO, "Service is not available")

            if not referer:
                return redirect(reverse("service_list"))
            return referer

        if not self.date_valid(queries['date']):
            messages.add_message(request, messages.INFO, "Calendar is out of range")
            if not referer:
                return redirect(reverse("service_list"))
            return referer

        context = {
            'service': service,
            'calendar': BookingCalendar(
                year=queries['date'].year,
                month=queries['date'].month,
                day=queries['date'].day,
            ),
            'bookings': self.timetable(service, queries['date']),
            'restriction_name': self.get_restriction_name(service),
        }

        return render(request, 'service_detail.html', context)
