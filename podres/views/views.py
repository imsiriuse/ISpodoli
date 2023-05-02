from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from podres.models import Service, Booking, Room
from django.views.decorators.http import require_POST


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services})


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
