from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Service, Booking


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services})


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        start_date = timezone.datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        booking = Booking(user=request.user, start_date=start_date)
        booking.save()

    return render(request, 'service_detail.html', {'service': service})


def booking_list(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_list.html', {'bookings': bookings})


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.user != request.user:
        return redirect('booking_list')
    return render(request, 'booking_detail.html', {'booking': booking})

