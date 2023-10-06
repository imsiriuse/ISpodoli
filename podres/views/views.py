from django.shortcuts import render
from podres.models import Service, ServiceType, Booking, Booker
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import resolve
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils.translation import activate, get_language
from urllib.parse import urlparse
from datetime import datetime

def service_list(request):
    service_types = []
    for service_type in ServiceType.objects.filter():
        service_types.append(Service.objects.filter(service_type=service_type).order_by('name'))

    context = {
        'service_types': service_types,
        'media_url': settings.MEDIA_URL,
    }

    return render(request, 'service_list.html', context)

def about(request):
    service_types = ServiceType.objects.filter()
    return render(request, 'about.html', {'service_types': service_types})

@login_required
def booking_detail(request, pk):
    if not request.user.is_staff:
        messages.add_message(request, messages.INFO, _("You are not authorized to do this action."))
        return redirect(reverse("service_list"))

    booking = get_object_or_404(Booking, id=pk)
    return render(request, 'booking_detail.html', {'booking': booking})


def change_language(request, lang_code):
    reverse_redirect = request.META.get("HTTP_REFERER", None) or "/"
    reverse_redirect = "/" + "/".join(urlparse(reverse_redirect)[2].split("/")[2:])
    reverse_redirect = resolve(reverse_redirect).url_name

    activate(lang_code)
    response = redirect(reverse_redirect)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response

def home(request):
    return redirect(reverse("service_list"))

