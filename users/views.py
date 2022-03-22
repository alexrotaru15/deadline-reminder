from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
from reminders.models import Phone


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email']
            )
            phone_number = Phone(phone_number=form.cleaned_data['phone'], user=user)
            phone_number.save()
            return redirect('users:login')
    else:
        if request.user.is_authenticated:
            return redirect(reverse('reminders:home'))
        form = RegisterForm()
    return render(request, 'users/register_user.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ProfileForm()
    return render(request, 'users/user_profile.html', {'form': form})