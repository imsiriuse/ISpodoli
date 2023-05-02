from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from podres.models import Service, Booking, Room
from datetime import date, datetime
from podres.widgets.bookingcalendar import BookingCalendar
from podres.widgets.timetable import Timetable

class ServiceDetail(View):
    def get(self, request, pk):
        service = get_object_or_404(Service, id=pk)

        context = {
            'service': service,
            'id': pk,
        }

        query = request.GET.dict()

        if 'date' not in query:
            today = date.today()
        else:
            today = datetime.strptime(query['date'], '%d-%m-%Y')

        context['day'] = int(today.strftime("%d"))
        context['month'] = int(today.strftime("%m"))
        context['year'] = int(today.strftime("%Y"))

        calendar = BookingCalendar(pk, context['year'], context['month'], context['day'])

        context['calendar'] = calendar.gethtml()

        bookings = Booking.objects.filter(service=service, date=today)
        timetable = Timetable(bookings)

        context['timetable'] = timetable.gethtml(service.service_type.hour_min, service.service_type.hour_max)

        return render(request, 'service_detail.html', context)
