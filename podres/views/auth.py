from django.contrib.auth.views import *
from django.utils.translation import get_language

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def get_success_url(self):
        user_language = get_language()
        # Construct the URL for the localized home page
        localized_home_url = f'/{user_language}/accounts/profile/'
        return localized_home_url

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    def get_success_url(self):
        user_language = get_language()
        # Construct the URL for the localized home page
        localized_home_url = f'/{user_language}/accounts/logout/'
        return localized_home_url

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    def get_success_url(self):
        user_language = get_language()
        # Construct the URL for the localized home page
        localized_home_url = f'/{user_language}/accounts/password_change/'
        return localized_home_url
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
    def get_success_url(self):
        user_language = get_language()
        # Construct the URL for the localized home page
        localized_home_url = f'/{user_language}/accounts/password_change/done/'
        return localized_home_url

