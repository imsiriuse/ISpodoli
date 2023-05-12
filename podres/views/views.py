from django.shortcuts import render, redirect
from podres.models import Service, Booking
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'profile.html')


def about(request):
    return render(request, 'about.html')


def homepage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('service_list')


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services})


@login_required
def test(request, service, day, month, year, hour):
    context = {
        'service': service,
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
    }
    return render(request, 'test.html', context)

@login_required
def booking_list(request):
    bookings = Booking.objects.filter()
    return render(request, 'booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = Booking.objects.get(id=pk)

    return render(request, 'booking_detail.html', {'booking': booking})
