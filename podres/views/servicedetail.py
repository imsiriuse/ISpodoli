from django.views import View
from django.shortcuts import render, get_object_or_404
from podres.models import Service, Booking
from datetime import date, datetime
from podres.plugins.bookingcalendar import BookingCalendar


class ServiceDetail(View):
    def gettimes(self, start, end):
        result = [None] * (end - start + 1)
        for i in range(0, end - start + 1):
            hour = start + i
            if hour < 10:
                result[i] = f"0{hour}:00"
            else:
                result[i] = f"{hour}:00"
        return result

    def timetable(self, service, today):
        start = service.service_type.hour_min
        end = service.service_type.hour_max
        bookings = Booking.objects.filter(service=service, date=today)
        bookings = sorted(bookings, key=lambda b: b.hour)
        bookings = filter(lambda b: start <= b.hour <= end, bookings)

        result = [None] * (end - start + 1)

        for booking in bookings:
            result[booking.hour] = booking

        return result

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

        context['bookings'] = zip(
            self.timetable(service, today),
            self.gettimes(service.service_type.hour_min, service.service_type.hour_max)
        )

        return render(request, 'service_detail.html', context)
