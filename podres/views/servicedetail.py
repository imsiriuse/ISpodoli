from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from datetime import date, datetime
from ..plugins.bookingcalendar import BookingCalendar
from ..models import Service, Booking


class ServiceDetailView(DetailView):

    def get_context_data(self, service_id, **kwargs):
        # get service
        service = get_object_or_404(Service, id=service_id)

        context = {
            'service': service,
            'id': service_id,
        }

        query = request.GET.dict()

        if 'date' not in query:
            today = date.today()
        else:
            today = datetime.strptime(query['date'], '%d-%m-%Y')

        context['day'] = int(today.strftime("%d"))
        context['month'] = int(today.strftime("%m"))
        context['year'] = int(today.strftime("%Y"))

        calendar = BookingCalendar(service_id, context['year'], context['month'], context['day'])

        context['calendar'] = calendar.formatmonth()

        bookings = Booking.objects.filter(service=service, date=today)

        return context