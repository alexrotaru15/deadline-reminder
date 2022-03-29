from django import forms
from django.forms import ModelForm
from .models import Reminder


class ReminderForm(ModelForm):
    class Meta:
        model = Reminder
        exclude = ['user', 'reminder_date']
        error_messages = {
            'deadline_date': {
                'invalid': 'Trebuie să introduceți o dată validă.'
            },
            'reminder_time': {
                'required': 'Trebuie să selectați o opțiune.'
            }
        }
