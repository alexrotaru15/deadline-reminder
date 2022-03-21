from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email']
            )
            # login(request, user)
            return redirect('users:login')
    else:
        if request.user.is_authenticated:
            return redirect(reverse('reminders:home'))
        form = RegisterForm()
    return render(request, 'users/register_user.html', {'form': form})
