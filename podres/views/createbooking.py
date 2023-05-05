from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect

class CreateBookingView(LoginRequiredMixin, View):
    template_name = 'create_booking.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, service, day, month, year, hour):
        context = {
            'service': service,
            'day': day,
            'month': month,
            'year': year,
            'hour': hour,
        }
        return render(request, 'create_booking.html', context)
