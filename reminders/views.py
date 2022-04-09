import datetime
from numbers import Number
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from sms import send_sms
from .forms import ReminderForm
from .models import Reminder
# from .tasks import new_reminder


def home(request):
    return render(request, 'reminders/home.html', {'title': 'Acasă'})

@login_required
def add_reminder(request):
    # send_mail(
    #     subject='Ola',
    #     message='Ola buenas noces',
    #     from_email='webmaster@localhost',
    #     recipient_list=['alexrotaru1595@gmail.com'],
    # )
    # send_sms(
    #     'mesaj de trimis',
    #     'django-backend-host',
    #     [request.user.phone],
    #     fail_silently=False
    # )
    # new_reminder.delay(request.user.id)
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.reminder_date = timezone.now() + datetime.timedelta(minutes=int(form.cleaned_data['reminder_time']))
            reminder.save()
            print(form.cleaned_data['reminder_time'])
            return redirect(reverse('reminders:home'))
    else:
        form = ReminderForm()
    return render(request, 'reminders/add_reminder.html', {'form': form})


class RemindersView(generic.ListView):
    template_name = 'reminders/reminders.html'
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)
        