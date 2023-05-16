from django.views import View
from django.shortcuts import render, get_object_or_404
from podres.models import Service, Booking
from datetime import date, datetime
from podres.plugins.bookingcalendar import BookingCalendar
from django.contrib.auth.mixins import LoginRequiredMixin
from podres.enums import CalendarType

class ServiceDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'


    def timetable_hour(self, service):
        start = service.service_type.hour_min
        end = service.service_type.hour_max
        today = date.today()

        bookings = Booking.objects.filter(service=service, date=today).order_by('hour')
        bookings = filter(lambda b: start <= b.hour <= end, bookings)

        result = [None] * (end - start + 1)

        for booking in bookings:
            result[booking.hour - start] = booking

        return zip(result, range(start, end + 1))


    def get(self, request, pk):
        service = get_object_or_404(Service, id=pk)

        query = request.GET.dict()

        if 'date' not in query:
            today = date.today()
        else:
            try:
                today = datetime.strptime(query['date'], '%d-%m-%Y')
            except ValueError:
                today = date.today()

        calendar = BookingCalendar(
            year=int(today.strftime("%Y")),
            month=int(today.strftime("%m")),
            day=int(today.strftime("%d"))
        )

        context = {
            'service': service,
            'calendar': calendar,
        }

        if service.service_type.calendar_type == CalendarType.HOURLY:
            context['bookings'] = self.timetable_hour(service)
        if service.service_type.calendar_type == CalendarType.DAILY:
            context['bookings'] = Booking.objects.filter(service=service, date=today)

        for booking in context['bookings']:
            print(booking)

        return render(request, 'service_detail.html', context)
