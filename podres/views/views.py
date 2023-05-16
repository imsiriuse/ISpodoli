from django.shortcuts import render
from podres.models import Service, ServiceType
from django.conf import settings


def service_list(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service_list.html', {'services': services, 'media_url': settings.MEDIA_URL})

def about(request):
    service_types = ServiceType.objects.all()
    return render(request, 'about.html', {'service_types': service_types})
