from django.shortcuts import render, redirect
from podres.models import Service, Booking
from django.contrib.auth.decorators import login_required
from django.conf import settings


def service_list(request):
    services = Service.objects.filter(is_available=True)

    return render(request, 'service_list.html', {'services': services, 'media_url': settings.MEDIA_URL})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_history.html', {'bookings': bookings})
