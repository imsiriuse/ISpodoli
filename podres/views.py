from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Service, Booking, Room
from django.views.decorators.http import require_POST
from datetime import date, datetime
from .plugins.bookingcalendar import BookingCalendar


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services})


def create_times(start, end):
    if end < start:
        return []

    time_array = []
    for i in range(start, end):
        if i < 10:
            time = '0' + str(i) + ':00'
        else:
            time = str(i) + ':00'

        time_array.append(time)

    return time_array


def service_detail(request, pk):
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

    context['calendar'] = calendar.formatmonth()

    bookings = Booking.objects.filter(service=service, date=today)

    context['bookings'] = bookings

    return render(request, 'service_detail.html', context)


@require_POST
def create_booking(request, pk):
    service = get_object_or_404(Service, id=pk)
    start_date = timezone.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    booking = Booking(start_date=start_date, service=service)
    booking.save()

    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def booking_list(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_list.html', {'bookings': bookings})


def booking_detail(request, pk):
    booking = Booking.objects.get(id=pk)

    return render(request, 'booking_detail.html', {'booking': booking})


def delete_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.delete()

    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def rooms_list(request):
    rooms = Room.objects.filter()
    return render(request, 'rooms_list.html', {'rooms': rooms})
