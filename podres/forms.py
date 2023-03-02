from django import forms
from .models import Booking


class DateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date']
