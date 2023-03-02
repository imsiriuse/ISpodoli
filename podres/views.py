from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Service, Booking, Room
from django.views.decorators.http import require_POST


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    bookings = Booking.objects.filter(service=service)
    context = {
        'service': service,
        'bookings': bookings,
        'id': service_id,
    }

    return render(request, 'service_detail.html', context)


@require_POST
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    start_date = timezone.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    booking = Booking(start_date=start_date, service=service)
    booking.save()

    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def booking_list(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_list.html', {'bookings': bookings})


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking_detail.html', {'booking': booking})


@require_POST
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.delete()

    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


def rooms_list(request):
    rooms = Room.objects.filter()
    return render(request, 'rooms_list.html', {'rooms': rooms})
