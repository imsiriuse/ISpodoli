from django.shortcuts import render
from podres.models import Service, Booking, ServiceType
from django.contrib.auth.decorators import login_required
from django.conf import settings


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services, 'media_url': settings.MEDIA_URL})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_history.html', {'bookings': bookings})

def about(request):
    service_types = ServiceType.objects.all()
    return render(request, 'about.html', {'service_types': service_types})

@login_required
def profile(request):
    return render(request, 'profile.html')
