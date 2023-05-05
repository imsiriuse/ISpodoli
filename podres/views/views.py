from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from podres.models import Service, Booking, Room
from django.views.decorators.http import require_POST
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


@login_required
def booking_detail(request, pk):
    booking = Booking.objects.get(id=pk)

    return render(request, 'booking_detail.html', {'booking': booking})


@login_required
def delete_booking(request, pk):
    booking = Booking.objects.get(id=pk)
    booking.delete()

    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)

@login_required
def rooms_list(request):
    rooms = Room.objects.filter()
    return render(request, 'rooms_list.html', {'rooms': rooms})
