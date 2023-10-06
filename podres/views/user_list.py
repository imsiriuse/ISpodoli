from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from podres.models import Booker
from datetime import datetime
from django.contrib import messages
from django.utils.translation import activate, get_language
from django.utils.translation import gettext_lazy as _


class UserListView(LoginRequiredMixin, View):
    template_name = 'user_list.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if not request.user.is_staff:
            messages.add_message(request, messages.INFO, _("You are not authorized to do this action."))
            return redirect(reverse("service_list"))

        bookers = Booker.objects.filter().order_by('room')

        context = {
            'bookers': bookers,
        }

        return render(request, 'user_list.html', context)
