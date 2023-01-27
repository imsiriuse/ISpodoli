from django.shortcuts import render
from .models import Service, ServiceInstance


def index(request):
    # Generate counts of some of the main objects
    num_books = Service.objects.all().count()
    num_instances = ServiceInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = ServiceInstance.objects.filter(active__exact=True).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
    }

    return render(request, 'index.html', context=context)
