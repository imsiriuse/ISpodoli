from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect, reverse, render
from podres.models import Ban
from datetime import date, timedelta

class BansListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'bans_list.html'

    def get(self, request):
        bans = Ban.objects.filter(start_date__lte=date.today()).order_by('-start_date')
        bans = filter(lambda x: x.start_date + timedelta(x.duration) > date.today(), bans)

        past_bans = Ban.objects.filter().order_by('-start_date')
        past_bans = filter(lambda x: x.start_date + timedelta(x.duration) <= date.today(), past_bans)

        context = {
            'bans': bans,
            'past_bans': past_bans,
        }

        return render(request, self.template_name, context)
