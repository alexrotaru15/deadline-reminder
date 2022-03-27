import datetime
from numbers import Number
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import ReminderForm
from .models import Reminder

def home(request):
    return render(request, 'reminders/home.html')

@login_required
def add_reminder(request):
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
        