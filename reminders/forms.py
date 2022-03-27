from django import forms
from django.forms import ModelForm
from .models import Reminder


class ReminderForm(ModelForm):
    timers = [
        (30, '30 de minute'),
        (60, '1 oră'),
        (60 * 3, '3 ore'),
        (60 * 12, '12 ore'),
        (60 * 24, 'o zi'),
        (60 * 48, '2 zile'),
        (60 * 24 * 7, '7 zile')
    ]
    reminder_time = forms.CharField(
        label='Cu cât timp înainte doriți să primiți notificare?',
        error_messages={'required': 'Trebuie să selectați o opțiune'},
        widget=forms.Select(choices=timers)
        )
    class Meta:
        model = Reminder
        exclude = ['user', 'reminder_date']

