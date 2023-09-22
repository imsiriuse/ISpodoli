from django.shortcuts import render
from podres.models import Service, ServiceType, Booking, Booker
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.translation import activate, get_language

def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services, 'media_url': settings.MEDIA_URL})

def about(request):
    service_types = ServiceType.objects.filter()
    return render(request, 'about.html', {'service_types': service_types})

@login_required
def booking_detail(request, pk):
    if not request.user.is_staff:
        messages.add_message(request, messages.INFO, "You are not authorized to do this action.")
        return redirect(reverse("service_list"))

    booking = get_object_or_404(Booking, id=pk)
    return render(request, 'booking_detail.html', {'booking': booking})

@login_required
def user_detail(request, pk):
    if not request.user.is_staff:
        messages.add_message(request, messages.INFO, "You are not authorized to do this action.")
        return redirect(reverse("service_list"))

    booker = get_object_or_404(Booker, id=pk)
    bookings = Booking.objects.filter(booker=booker)

    return render(request, 'user_detail.html', {'booker': booker, 'bookings': bookings})

@login_required
def user_list(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.INFO, "You are not authorized to do this action.")
        return redirect(reverse("service_list"))

    bookers = Booker.objects.filter()
    return render(request, 'user_list.html', {'bookers': bookers})

def change_language(request, lang_code):
    activate(lang_code)

    response = redirect("service_list")
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

    return response

def home(request):
    return redirect(reverse("service_list"))

